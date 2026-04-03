import textwrap

import streamlit as st
import streamlit.components.v1 as components

from econanalys.theme import get_theme_mode, get_theme_tokens


def build_app_css(theme_mode):
    light_tokens = get_theme_tokens("light")
    dark_tokens = get_theme_tokens("dark")
    return textwrap.dedent(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;1,14..32,400&display=swap');

        :root,
        html[data-ea-theme="light"],
        body[data-ea-theme="light"],
        .stApp[data-ea-theme="light"] {{
            --accent: {light_tokens["accent"]};
            --accent-light: {light_tokens["accent_light"]};
            --accent-dim: {light_tokens["accent_dim"]};
            --neon-accent: {light_tokens["neon_accent"]};
            --success: {light_tokens["success"]};
            --warning: {light_tokens["warning"]};
            --danger: {light_tokens["danger"]};
            --bg-body: {light_tokens["bg_body"]};
            --bg-elevated: {light_tokens["bg_elevated"]};
            --bg-card: {light_tokens["bg_card"]};
            --bg-card2: {light_tokens["bg_card_alt"]};
            --bg-input: {light_tokens["bg_input"]};
            --bg-hover: {light_tokens["bg_hover"]};
            --border: {light_tokens["border"]};
            --border-strong: {light_tokens["border_strong"]};
            --text-primary: {light_tokens["text_primary"]};
            --text-muted: {light_tokens["text_muted"]};
            --text-placeholder: {light_tokens["text_placeholder"]};
            --shadow-sm: {light_tokens["shadow_sm"]};
            --shadow-card: {light_tokens["shadow_card"]};
            --shadow-btn: {light_tokens["shadow_btn"]};
            --shadow-btn-h: {light_tokens["shadow_btn_hover"]};
            --auth-gradient: {light_tokens["auth_gradient"]};
            --background-color: var(--bg-body);
            --secondary-background-color: var(--bg-card);
            --text-color: var(--text-primary);
            --border-color: var(--border);
            color-scheme: light;
        }}

        html[data-ea-theme="dark"],
        body[data-ea-theme="dark"],
        .stApp[data-ea-theme="dark"],
        [data-testid="stAppViewContainer"][data-ea-theme="dark"],
        [data-testid="stMain"][data-ea-theme="dark"] {{
            --accent: {dark_tokens["accent"]};
            --accent-light: {dark_tokens["accent_light"]};
            --accent-dim: {dark_tokens["accent_dim"]};
            --neon-accent: {dark_tokens["neon_accent"]};
            --success: {dark_tokens["success"]};
            --warning: {dark_tokens["warning"]};
            --danger: {dark_tokens["danger"]};
            --bg-body: {dark_tokens["bg_body"]};
            --bg-elevated: {dark_tokens["bg_elevated"]};
            --bg-card: {dark_tokens["bg_card"]};
            --bg-card2: {dark_tokens["bg_card_alt"]};
            --bg-input: {dark_tokens["bg_input"]};
            --bg-hover: {dark_tokens["bg_hover"]};
            --border: {dark_tokens["border"]};
            --border-strong: {dark_tokens["border_strong"]};
            --text-primary: {dark_tokens["text_primary"]};
            --text-muted: {dark_tokens["text_muted"]};
            --text-placeholder: {dark_tokens["text_placeholder"]};
            --shadow-sm: {dark_tokens["shadow_sm"]};
            --shadow-card: {dark_tokens["shadow_card"]};
            --shadow-btn: {dark_tokens["shadow_btn"]};
            --shadow-btn-h: {dark_tokens["shadow_btn_hover"]};
            --auth-gradient: {dark_tokens["auth_gradient"]};
            --background-color: var(--bg-body);
            --secondary-background-color: var(--bg-card);
            --text-color: var(--text-primary);
            --border-color: var(--border);
            color-scheme: dark;
        }}

        [data-testid="stSidebar"] {{
            display: none !important;
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        html, body {{
            background:
                radial-gradient(circle at top left, var(--accent-dim), transparent 28%),
                linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-body) 100%) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        body ::selection {{
            background: var(--accent);
            color: #ffffff;
        }}

        .stApp,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main,
        [data-testid="stAppViewBlockContainer"] {{
            background:
                radial-gradient(circle at top left, var(--accent-dim), transparent 28%),
                linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-body) 100%) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        #MainMenu,
        header[data-testid="stHeader"] *,
        .stAppDeployButton {{
            display: none !important;
            visibility: hidden !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
            border-bottom: none !important;
            box-shadow: none !important;
            height: 0 !important;
            min-height: 0 !important;
            position: fixed !important;
        }}

        [data-testid="stMainBlockContainer"] {{
            max-width: 1280px !important;
            padding-top: 1.15rem !important;
            padding-bottom: 3rem !important;
        }}

        .auth-shell [data-testid="stMainBlockContainer"] {{
            padding-top: 0.35rem !important;
        }}

        [data-testid="stMarkdownContainer"],
        [data-testid="stText"],
        p,
        li,
        label {{
            color: var(--text-primary);
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            justify-content: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border) !important;
            background: transparent !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            font-family: 'Inter', sans-serif !important;
            font-size: 0.79rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
            background: transparent !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            border-radius: 0 !important;
            padding: 0.95rem 1.35rem !important;
            transition: color 0.2s ease, border-color 0.2s ease, opacity 0.2s ease;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--text-primary) !important;
            opacity: 1 !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
            opacity: 1 !important;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stForm"],
        div[data-testid="stMetric"],
        [data-testid="stExpander"] details {{
            background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-card2) 100%) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            box-shadow: var(--shadow-card) !important;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            padding: 1.35rem !important;
            margin-bottom: 0 !important;
        }}

        [data-testid="stMetric"] {{
            padding: 1rem 1.1rem !important;
        }}

        hr {{
            border-color: var(--border) !important;
        }}

        .stAlert {{
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            box-shadow: var(--shadow-sm) !important;
        }}

        .stButton > button,
        .stDownloadButton > button,
        button[kind="primary"],
        button[kind="secondary"] {{
            min-height: 2.9rem !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-strong) !important;
            background: linear-gradient(135deg, var(--bg-card2) 0%, var(--bg-card) 100%) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            box-shadow: var(--shadow-sm) !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease !important;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover {{
            transform: translateY(-1px);
            border-color: var(--accent) !important;
            box-shadow: var(--shadow-btn) !important;
        }}

        .stButton > button[kind="primary"],
        button[kind="primary"] {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%) !important;
            border-color: transparent !important;
            color: #ffffff !important;
        }}

        .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover {{
            box-shadow: var(--shadow-btn-h) !important;
        }}

        [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stMultiSelect"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSlider"] label,
        [data-testid="stDateInput"] label {{
            color: var(--text-muted) !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
        }}

        [data-baseweb="input"] > div,
        [data-baseweb="base-input"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="tag"] {{
            background: var(--bg-input) !important;
            border-color: var(--border) !important;
            color: var(--text-primary) !important;
            border-radius: 14px !important;
            box-shadow: none !important;
        }}

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input,
        [data-testid="stTextArea"] textarea {{
            background: var(--bg-input) !important;
            color: var(--text-primary) !important;
            caret-color: var(--accent) !important;
        }}

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stNumberInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {{
            color: var(--text-placeholder) !important;
        }}

        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="base-input"] > div:focus-within,
        [data-baseweb="textarea"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 4px var(--accent-dim) !important;
        }}

        [data-baseweb="select"] svg,
        [data-testid="stDateInput"] svg {{
            color: var(--text-muted) !important;
            fill: var(--text-muted) !important;
        }}

        [data-testid="stCheckbox"] label,
        [data-testid="stRadio"] label {{
            color: var(--text-primary) !important;
        }}

        [data-testid="stSlider"] [role="slider"] {{
            background: var(--accent) !important;
            box-shadow: 0 0 0 6px var(--accent-dim) !important;
            border: 2px solid #ffffff22 !important;
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {{
            background: var(--accent-dim) !important;
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {{
            background: linear-gradient(90deg, var(--accent) 0%, var(--accent-light) 100%) !important;
        }}

        .stDataFrame,
        [data-testid="stTable"] {{
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid var(--border) !important;
            box-shadow: var(--shadow-sm) !important;
        }}

        .custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            margin-top: 5px;
        }}

        .custom-table th {{
            text-align: right;
            padding: 10px;
            color: var(--text-muted);
            font-weight: 600;
            border-bottom: 1px solid var(--border);
            font-size: 0.8rem;
        }}

        .custom-table th:first-child,
        .custom-table td:first-child {{
            text-align: left;
        }}

        .custom-table td {{
            padding: 12px 10px;
            border-bottom: 1px solid var(--border);
            text-align: right;
            color: var(--text-primary);
        }}

        .custom-table td:first-child {{
            font-weight: 500;
        }}

        .custom-table tr.active-row {{
            background: var(--accent-dim);
        }}

        .active-row td {{
            border-bottom: none;
            color: var(--accent);
        }}

        .positive-change {{
            color: var(--success) !important;
            font-weight: 700;
        }}

        .negative-change {{
            color: var(--danger) !important;
            font-weight: 700;
        }}

        .tv-metric-box {{
            text-align: center;
            padding: 15px 10px;
            border-radius: 14px;
            background: linear-gradient(180deg, var(--bg-card2) 0%, var(--bg-card) 100%);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-sm);
            margin-bottom: 5px;
        }}

        .tv-metric-title {{
            font-size: 0.78rem;
            color: var(--text-muted) !important;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            line-height: 1.1;
        }}

        .tv-metric-value {{
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--neon-accent) !important;
        }}

        .tv-title {{
            background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-card2) 100%) !important;
            color: var(--text-primary) !important;
            padding: 9px 15px;
            border-radius: 10px;
            font-family: 'Inter', sans-serif !important;
            border: 1px solid var(--border);
            font-size: 0.8rem;
            font-weight: 800;
            margin-bottom: 15px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: var(--shadow-sm);
        }}

        .tv-note-box,
        .tv-note-box-green {{
            padding: 12px;
            border-radius: 10px;
            font-size: 0.95rem;
            margin-bottom: 15px;
            box-shadow: var(--shadow-sm);
        }}

        .tv-note-box {{
            border-left: 4px solid var(--danger);
            background: color-mix(in srgb, var(--danger) 10%, transparent);
        }}

        .tv-note-box-green {{
            border-left: 4px solid var(--success);
            background: color-mix(in srgb, var(--success) 10%, transparent);
        }}

        .econ-footer {{
            text-align: center;
            font-size: 0.82rem;
            color: var(--text-muted);
            padding: 15px 0;
            margin-top: 30px;
            letter-spacing: 0.5px;
        }}

        .auth-page-bg {{
            position: fixed;
            inset: 0;
            z-index: -1;
            background: var(--auth-gradient);
            pointer-events: none;
        }}

        .auth-page-bg::before {{
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(ellipse 720px 520px at 18% 18%, var(--accent-dim) 0%, transparent 68%),
                radial-gradient(ellipse 620px 420px at 82% 82%, color-mix(in srgb, var(--accent-light) 20%, transparent) 0%, transparent 70%);
        }}

        .auth-heading {{
            text-align: center;
            margin-bottom: 0.6rem;
        }}

        @keyframes fadeSlideUp {{
            from {{ opacity: 0; transform: translateY(22px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .auth-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.8px;
            color: var(--text-primary);
            margin-bottom: 0.2rem;
        }}

        .auth-title span {{
            color: var(--accent);
        }}

        .auth-badge {{
            display: inline-block;
            background: color-mix(in srgb, var(--accent) 10%, transparent);
            color: var(--accent);
            font-family: 'Inter', sans-serif;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid var(--border-strong);
            margin-bottom: 1rem;
            margin-top: 0;
        }}

        .auth-section-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 20px;
            margin-top: 8px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
        }}

        .auth-footer {{
            text-align: center;
            font-size: 0.74rem;
            color: var(--text-muted);
            margin-top: 20px;
            letter-spacing: 0.3px;
        }}

        .auth-form-zone [data-testid="stTextInput"] label {{
            color: var(--text-muted) !important;
        }}

        .auth-form-zone [data-testid="stTextInput"] input {{
            background: var(--bg-input) !important;
            color: var(--text-primary) !important;
            border-radius: 12px !important;
        }}

        .auth-shell div[data-testid="stVerticalBlockBorderWrapper"] {{
            padding: 1.15rem 1.4rem 1.35rem !important;
            margin-top: 0 !important;
        }}
        </style>
        """
    )


def inject_styles(theme_mode=None):
    active_theme = theme_mode or get_theme_mode()
    st.markdown(build_app_css(active_theme), unsafe_allow_html=True)
    st.markdown("<div class='auth-shell'></div>", unsafe_allow_html=True)
    components.html(
        f"""
        <script>
            const doc = window.parent.document;
            const theme = "{active_theme}";
            const nodes = [
                doc.documentElement,
                doc.body,
                doc.querySelector(".stApp"),
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('[data-testid="stMain"]')
            ].filter(Boolean);
            nodes.forEach((node) => {{
                node.setAttribute("data-ea-theme", theme);
            }});
            doc.body.classList.toggle("auth-shell", !doc.querySelector(".stApp [data-testid='stTabs']"));
        </script>
        """,
        height=0,
    )


def metric_html(title, value, override_color=None):
    return (
        "<div class=\"tv-metric-box\">"
        f"<div class=\"tv-metric-title\">{title}</div>"
        f"<div class=\"tv-metric-value\" style=\"color: {override_color or 'var(--neon-accent)'} !important;\">{value}</div>"
        "</div>"
    )


def slice_desc(color, title, text):
    return f"""
    <div style="margin-bottom: 12px; display: flex; align-items: flex-start;">
        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {color}; margin-top: 4px; margin-right: 10px; flex-shrink: 0;"></div>
        <div>
            <span style="font-weight: 700; font-size: 0.95rem;">{title}</span><br>
            <span style="font-size: 0.85rem; opacity: 0.8; line-height: 1.35; display: block; margin-top: 2px;">{text}</span>
        </div>
    </div>
    """


def render_app_header(username: str, on_logout, on_toggle_theme, theme_mode: str):
    tokens = get_theme_tokens(theme_mode)
    c_h1, c_h2, c_h3 = st.columns([1, 4, 2.6])
    with c_h2:
        st.markdown(
            "<h2 style='text-align: center; font-family: \"Inter\", sans-serif; font-weight: 800; margin-bottom: 20px; letter-spacing: -0.5px;'><span style='color: var(--neon-accent); font-size: 2rem;'></span> EconAnalys</h2>",
            unsafe_allow_html=True,
        )
    with c_h3:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1.15])
        with btn_col1:
            components.html(
                f"""
                <script>
                    function triggerPrint() {{ window.parent.print(); }}
                </script>
                <button onclick="triggerPrint()" style="background: linear-gradient(135deg, {tokens['bg_card_alt']} 0%, {tokens['bg_card']} 100%); border: 1.5px solid {tokens['border_strong']}; color: {tokens['text_primary']}; border-radius: 10px; padding: 8px 12px; width: 100%; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: 0.2s; box-shadow: {tokens['shadow_sm']};">
                    PDF
                </button>
                """,
                height=45,
            )
        with btn_col2:
            theme_label = "Koyu" if theme_mode == "light" else "Açık"
            st.button(
                f"{theme_label} Tema",
                on_click=on_toggle_theme,
                use_container_width=True,
                key="btn_toggle_theme",
            )
        with btn_col3:
            st.markdown(
                f"<div style='font-size:0.75rem;opacity:0.72;color:var(--text-muted);text-align:center;margin-top:4px;'>{username}</div>",
                unsafe_allow_html=True,
            )
            st.button("Çıkış", on_click=on_logout, use_container_width=True, key="btn_logout")


def render_footer_glossary():
    st.markdown(
        "<br><hr style='border: none; border-bottom: 1px solid var(--border-color); margin: 30px 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='tv-title'> EKONOMİK VE BORSA TERİMLERİ SÖZLÜĞÜ</div>", unsafe_allow_html=True)
    with st.container(border=True):
        c_g1, c_g2, c_g3 = st.columns(3)
        with c_g1:
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5;'><b style='color:var(--neon-accent);'>IS-LM Modeli:</b> Mal (IS) ve para (LM) piyasalarının eşanlı genel dengesini gösteren makroekonomik denge matrisidir.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:var(--neon-accent);'>RSI (Göreceli Güç Endeksi):</b> Hissenin 70+ (Aşırı Alım) veya 30- (Aşırı Satım) bölgelerinde olup olmadığını ölçen salınım (momentum) indikatörüdür.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:var(--neon-accent);'>Bollinger Bantları:</b> Fiyatın yukarı/aşağı oynaklığını standart sapma (genellikle +2/-2) bandı ile çizerek trend ve kırılım kanallarını işaret eder.</div>",
                unsafe_allow_html=True,
            )
        with c_g2:
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5;'><b style='color:#F59E0B;'>Boğa / Ayı Piyasası:</b> Boğa (Bull Market) fiyatların istikrarlı yükseldiği iştahlı yatırımcı piyasasını; Ayı (Bear Market) ise fiyatların diplere koştuğu karamsar trendleri ifade eder.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:#F59E0B;'>F/K Oranı (P/E):</b> Şirketin hisse fiyatının, hisse başına yaratılan net kâra oranıdır. Düşük olması kâra kıyasla ucuzluk algısı yaratır.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:#F59E0B;'>PD/DD (P/B):</b> Piyasa Değeri / Defter Değeri. Şirketin borsa paha değerinin, muhasebesel özkaynaklarına bölünmesidir.</div>",
                unsafe_allow_html=True,
            )
        with c_g3:
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5;'><b style='color:#EF4444;'>Dışlama Etkisi (Crowding-out):</b> Hükümetin genişleyici harcama pompalamaları nedeniyle faizlerin artması ve özel yatırımların azalması durumudur.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:#EF4444;'>Para Yanılsaması (Money Illusion):</b> Nominal gelir artışına odaklanıp reel satın alma gücü düşüşünü fark edememe durumudur.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:#EF4444;'>Volatilite:</b> Bir varlığın değerindeki oynaklık ve dolayısıyla risk seviyesidir.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='font-size:0.85rem; line-height:1.5; margin-top:10px;'><b style='color:#EF4444;'>Destek / Direnç:</b> Fiyatın düşerken durduğu seviyeye 'Destek', yükselirken takıldığı seviyeye 'Direnç' denir.</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='econ-footer'>EconAnalys | designed by Quartet | Kocaeli University Economics</div>",
        unsafe_allow_html=True,
    )
