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


def set_session_cookie(token: str):
    cookie_payload = json.dumps(token)
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


def sync_session():
    cookie_token = st.context.cookies.get(SESSION_COOKIE_NAME, "")
    active_token = cookie_token or st.session_state.get("session_token", "")

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

    sync_session()

    if st.session_state.get("set_session_cookie"):
        set_session_cookie(st.session_state.set_session_cookie)
        del st.session_state["set_session_cookie"]

    if st.session_state.get("clear_session_cookie"):
        clear_session_cookie()
        del st.session_state["clear_session_cookie"]


def do_logout():
    delete_session(st.session_state.get("session_token", ""))
    clear_local_session()
    st.session_state.clear_session_cookie = True


def render_auth_guard() -> bool:
    if st.session_state.logged_in:
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
                login_user = st.text_input("Kullanıcı Adı", placeholder="kullanici_adi", key="login_user")
                login_pass = st.text_input("Şifre", type="password", placeholder="••••••", key="login_pass")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("Giriş Yap", use_container_width=True, key="btn_login", type="primary"):
                    if login_user and login_pass:
                        ok, msg = verify_user(login_user, login_pass)
                        if ok:
                            session_token = create_session(login_user)
                            st.session_state.logged_in = True
                            st.session_state.username = login_user.strip().lower()
                            st.session_state.session_token = session_token
                            st.session_state.set_session_cookie = session_token
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Lütfen kullanıcı adı ve şifrenizi girin.")
                if st.button("Şifremi Unuttum?", use_container_width=True, key="btn_forgot_pw"):
                    st.info("Şifrenizi sıfırlamak için lütfen sistem yöneticisi ile iletişime geçin.")

            with auth_tab_register:
                st.markdown("<div class='auth-section-label'>Yeni hesap oluşturun</div>", unsafe_allow_html=True)
                reg_user = st.text_input("Kullanıcı Adı", placeholder="kullanici_adi", key="reg_user")
                reg_pass = st.text_input("Şifre", type="password", placeholder="En az 6 karakter", key="reg_pass")
                reg_pass2 = st.text_input("Şifreyi Onayla", type="password", placeholder="••••••", key="reg_pass2")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("Kayıt Ol", use_container_width=True, key="btn_register", type="primary"):
                    if not reg_user or not reg_pass or not reg_pass2:
                        st.warning("Tüm alanları doldurun.")
                    elif reg_pass != reg_pass2:
                        st.error("Şifreler eşleşmiyor.")
                    else:
                        ok, msg = register_user(reg_user, reg_pass)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='auth-footer'>&copy; 2025 EconAnalys &middot; designed by Quartet</div>", unsafe_allow_html=True)
    return False
