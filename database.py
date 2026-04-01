import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    """Veritabanını ve kullanıcılar tablosunu oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
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
        conn = sqlite3.connect(DB_PATH)
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
        conn = sqlite3.connect(DB_PATH)
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
