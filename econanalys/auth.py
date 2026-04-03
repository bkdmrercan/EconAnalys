import json
import time

import streamlit as st
import streamlit.components.v1 as components

from database import (
    SESSION_TTL_SECONDS,
    create_session,
    delete_session,
    refresh_session,
    register_user,
    verify_session,
    verify_user,
)

SESSION_COOKIE_NAME = "econanalys_session"


def _normalize_session_token(token: str) -> str:
    cleaned = (token or "").strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1]
    return cleaned


def set_session_cookie(token: str):
    cookie_payload = json.dumps(_normalize_session_token(token))
    components.html(
        f"""
        <script>
            document.cookie = "{SESSION_COOKIE_NAME}=" + encodeURIComponent({cookie_payload}) +
                "; Max-Age={SESSION_TTL_SECONDS}; Path=/; SameSite=Lax";
        </script>
        """,
        height=0,
    )


def clear_session_cookie():
    components.html(
        f"""
        <script>
            document.cookie = "{SESSION_COOKIE_NAME}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/; SameSite=Lax";
        </script>
        """,
        height=0,
    )


def clear_local_session():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.session_token = ""
    st.session_state.last_activity = time.time()


def _set_auth_notice(level: str, message: str, scope: str) -> None:
    st.session_state.auth_notice = {"level": level, "message": message, "scope": scope}


def _render_auth_notice(scope: str) -> None:
    notice = st.session_state.get("auth_notice")
    if not notice:
        return
    if notice.get("scope") != scope:
        return

    del st.session_state["auth_notice"]

    level = notice.get("level")
    message = notice.get("message", "")
    if level == "error":
        st.error(message)
    elif level == "success":
        st.success(message)
    else:
        st.warning(message)


def _queue_auth_action(action: str) -> None:
    st.session_state.auth_action = action


def _process_pending_auth_action() -> bool:
    action = st.session_state.pop("auth_action", "")
    if not action:
        return False

    if action == "login":
        login_user = st.session_state.get("login_user", "")
        login_pass = st.session_state.get("login_pass", "")
        if not login_user or not login_pass:
            _set_auth_notice("warning", "Lütfen kullanıcı adı ve şifrenizi girin.", "login")
            return False

        ok, msg = verify_user(login_user, login_pass)
        if not ok:
            _set_auth_notice("error", msg, "login")
            return False

        session_token = create_session(login_user)
        st.session_state.logged_in = True
        st.session_state.username = login_user.strip().lower()
        st.session_state.session_token = session_token
        st.session_state.login_pass = ""
        set_session_cookie(session_token)
        return True

    if action == "register":
        reg_user = st.session_state.get("reg_user", "")
        reg_pass = st.session_state.get("reg_pass", "")
        reg_pass2 = st.session_state.get("reg_pass2", "")

        if not reg_user or not reg_pass or not reg_pass2:
            _set_auth_notice("warning", "Tüm alanları doldurun.", "register")
            return False
        if reg_pass != reg_pass2:
            _set_auth_notice("error", "Şifreler eşleşmiyor.", "register")
            return False

        ok, msg = register_user(reg_user, reg_pass)
        _set_auth_notice("success" if ok else "error", msg, "register")
        if ok:
            st.session_state.reg_pass = ""
            st.session_state.reg_pass2 = ""
        return False

    return False


def sync_session():
    cookie_token = _normalize_session_token(st.context.cookies.get(SESSION_COOKIE_NAME, ""))
    active_token = cookie_token or _normalize_session_token(st.session_state.get("session_token", ""))

    if not active_token:
        clear_local_session()
        return

    ok, username = verify_session(active_token)
    if not ok:
        delete_session(active_token)
        clear_local_session()
        st.session_state.clear_session_cookie = True
        return

    refresh_session(active_token, SESSION_TTL_SECONDS)
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.session_token = active_token
    st.session_state.last_activity = time.time()
    st.session_state.set_session_cookie = active_token


def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "session_token" not in st.session_state:
        st.session_state.session_token = ""
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()

    # If logout requested in the previous callback-triggered rerun,
    # do not re-authenticate from a still-present browser cookie.
    if st.session_state.pop("clear_session_cookie", False):
        clear_local_session()
        clear_session_cookie()
        return

    sync_session()

    if st.session_state.get("set_session_cookie"):
        set_session_cookie(st.session_state.set_session_cookie)
        del st.session_state["set_session_cookie"]

    if st.session_state.get("clear_session_cookie"):
        clear_session_cookie()
        del st.session_state["clear_session_cookie"]


def do_logout():
    delete_session(_normalize_session_token(st.session_state.get("session_token", "")))
    clear_local_session()
    st.session_state.clear_session_cookie = True


def render_auth_guard() -> bool:
    if st.session_state.logged_in:
        return True

    if _process_pending_auth_action():
        return True

    # Arka plan degrade katmanı
    st.markdown("<div class='auth-page-bg'></div>", unsafe_allow_html=True)

    _, auth_col, _ = st.columns([1, 1.5, 1])
    with auth_col:
        st.markdown("""
        <div class="auth-heading">
            <div class="auth-title"><span>Econ</span>Analys</div>
            <div class="auth-badge">Kocaeli Üniversitesi &middot; İktisat Analiz Platformu</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            auth_tab_login, auth_tab_register = st.tabs(["Giriş Yap", "Kayıt Ol"])

            st.markdown("<div class='auth-form-zone'>", unsafe_allow_html=True)

            with auth_tab_login:
                st.markdown("<div class='auth-section-label'>Hesabınıza giriş yapın</div>", unsafe_allow_html=True)
                _render_auth_notice("login")
                login_user = st.text_input("Kullanıcı Adı", placeholder="kullanici_adi", key="login_user")
                login_pass = st.text_input("Şifre", type="password", placeholder="••••••", key="login_pass")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.button(
                    "Giriş Yap",
                    use_container_width=True,
                    key="btn_login",
                    type="primary",
                    on_click=_queue_auth_action,
                    args=("login",),
                )
                if st.button("Şifremi Unuttum?", use_container_width=True, key="btn_forgot_pw"):
                    st.info("Şifrenizi sıfırlamak için lütfen sistem yöneticisi ile iletişime geçin.")

            with auth_tab_register:
                st.markdown("<div class='auth-section-label'>Yeni hesap oluşturun</div>", unsafe_allow_html=True)
                _render_auth_notice("register")
                reg_user = st.text_input("Kullanıcı Adı", placeholder="kullanici_adi", key="reg_user")
                reg_pass = st.text_input("Şifre", type="password", placeholder="En az 6 karakter", key="reg_pass")
                reg_pass2 = st.text_input("Şifreyi Onayla", type="password", placeholder="••••••", key="reg_pass2")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.button(
                    "Kayıt Ol",
                    use_container_width=True,
                    key="btn_register",
                    type="primary",
                    on_click=_queue_auth_action,
                    args=("register",),
                )

            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='auth-footer'>&copy; 2025 EconAnalys &middot; designed by Quartet</div>", unsafe_allow_html=True)
    return False
