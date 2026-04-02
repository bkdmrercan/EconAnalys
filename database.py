import sqlite3
import bcrypt
import os
import hashlib
import secrets
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")
SESSION_TTL_SECONDS = 3600


def _connect():
    return sqlite3.connect(DB_PATH)


def _hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def init_db():
    """Veritabanını, kullanıcı ve oturum tablolarını oluşturur."""
    conn = _connect()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token_hash TEXT UNIQUE NOT NULL,
            expires_at INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON sessions(token_hash)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at)")
    c.execute("DELETE FROM sessions WHERE expires_at <= ?", (int(time.time()),))
    conn.commit()
    conn.close()


def register_user(username: str, password: str) -> tuple[bool, str]:
    """
    Yeni kullanıcı kaydeder.
    Returns: (başarılı mı, mesaj)
    """
    if not username or not username.strip():
        return False, "Kullanıcı adı boş olamaz."
    if len(password) < 6:
        return False, "Şifre en az 6 karakter olmalıdır."

    username = username.strip().lower()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        conn = _connect()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
        conn.commit()
        conn.close()
        return True, "Kayıt başarılı! Şimdi giriş yapabilirsiniz."
    except sqlite3.IntegrityError:
        return False, "Bu kullanıcı adı zaten alınmış."
    except Exception as e:
        return False, f"Bir hata oluştu: {e}"


def verify_user(username: str, password: str) -> tuple[bool, str]:
    """
    Kullanıcı adı ve şifreyi doğrular.
    Returns: (başarılı mı, mesaj)
    """
    username = username.strip().lower()
    try:
        conn = _connect()
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
    except Exception as e:
        return False, f"Veritabanı hatası: {e}"

    if row is None:
        return False, "Kullanıcı adı veya şifre hatalı."

    if bcrypt.checkpw(password.encode("utf-8"), row[0].encode("utf-8")):
        return True, "Giriş başarılı."
    else:
        return False, "Kullanıcı adı veya şifre hatalı."


def create_session(username: str, ttl_seconds: int = SESSION_TTL_SECONDS) -> str:
    """Kullanıcı için yeni bir sunucu taraflı oturum oluşturur."""
    username = username.strip().lower()
    token = secrets.token_urlsafe(32)
    token_hash = _hash_session_token(token)
    expires_at = int(time.time()) + ttl_seconds

    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE username = ? OR expires_at <= ?", (username, int(time.time())))
    c.execute(
        "INSERT INTO sessions (username, token_hash, expires_at) VALUES (?, ?, ?)",
        (username, token_hash, expires_at),
    )
    conn.commit()
    conn.close()
    return token


def verify_session(token: str) -> tuple[bool, str]:
    """Oturum token'ını doğrular."""
    if not token:
        return False, ""

    token_hash = _hash_session_token(token)
    now_ts = int(time.time())

    try:
        conn = _connect()
        c = conn.cursor()
        c.execute("SELECT username, expires_at FROM sessions WHERE token_hash = ?", (token_hash,))
        row = c.fetchone()
        if row is None:
            conn.close()
            return False, ""

        username, expires_at = row
        if expires_at <= now_ts:
            c.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
            conn.commit()
            conn.close()
            return False, ""

        conn.close()
        return True, username
    except Exception:
        return False, ""


def refresh_session(token: str, ttl_seconds: int = SESSION_TTL_SECONDS) -> bool:
    """Geçerli oturumun süresini uzatır."""
    if not token:
        return False

    token_hash = _hash_session_token(token)
    expires_at = int(time.time()) + ttl_seconds

    try:
        conn = _connect()
        c = conn.cursor()
        c.execute(
            "UPDATE sessions SET expires_at = ? WHERE token_hash = ? AND expires_at > ?",
            (expires_at, token_hash, int(time.time())),
        )
        updated = c.rowcount > 0
        conn.commit()
        conn.close()
        return updated
    except Exception:
        return False


def delete_session(token: str) -> None:
    """Oturumu siler."""
    if not token:
        return

    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE token_hash = ?", (_hash_session_token(token),))
    conn.commit()
    conn.close()
