import streamlit as st


THEME_TOKENS = {
    "light": {
        "accent": "#2563EB",
        "accent_light": "#60A5FA",
        "accent_dim": "rgba(37, 99, 235, 0.10)",
        "neon_accent": "#2563EB",
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "bg_body": "#EEF4FB",
        "bg_elevated": "#F7FAFE",
        "bg_card": "#FFFFFF",
        "bg_card_alt": "#F5F9FF",
        "bg_input": "#F3F7FD",
        "bg_hover": "#E8F0FB",
        "border": "rgba(37, 99, 235, 0.14)",
        "border_strong": "rgba(37, 99, 235, 0.24)",
        "text_primary": "#0F172A",
        "text_muted": "#64748B",
        "text_placeholder": "#94A3B8",
        "shadow_sm": "0 8px 24px rgba(15, 23, 42, 0.05)",
        "shadow_card": "0 28px 60px rgba(37, 99, 235, 0.12), 0 12px 24px rgba(15, 23, 42, 0.06)",
        "shadow_btn": "0 16px 30px rgba(37, 99, 235, 0.26)",
        "shadow_btn_hover": "0 22px 38px rgba(37, 99, 235, 0.34)",
        "auth_gradient": "linear-gradient(135deg, #E6F0FF 0%, #EEF4FB 48%, #DEE9FF 100%)",
        "plot_grid": "rgba(37, 99, 235, 0.12)",
        "plot_zero": "rgba(15, 23, 42, 0.18)",
    },
    "dark": {
        "accent": "#5EA2FF",
        "accent_light": "#8FC2FF",
        "accent_dim": "rgba(94, 162, 255, 0.14)",
        "neon_accent": "#7CB8FF",
        "success": "#34D399",
        "warning": "#FBBF24",
        "danger": "#F87171",
        "bg_body": "#07111F",
        "bg_elevated": "#0D1728",
        "bg_card": "#111D31",
        "bg_card_alt": "#16243A",
        "bg_input": "#162338",
        "bg_hover": "#1A2B44",
        "border": "rgba(124, 184, 255, 0.16)",
        "border_strong": "rgba(124, 184, 255, 0.28)",
        "text_primary": "#E7EEF8",
        "text_muted": "#9FB0C7",
        "text_placeholder": "#6B7C95",
        "shadow_sm": "0 10px 28px rgba(2, 8, 23, 0.32)",
        "shadow_card": "0 30px 70px rgba(2, 8, 23, 0.54), 0 10px 24px rgba(94, 162, 255, 0.10)",
        "shadow_btn": "0 18px 34px rgba(94, 162, 255, 0.22)",
        "shadow_btn_hover": "0 24px 42px rgba(94, 162, 255, 0.28)",
        "auth_gradient": "linear-gradient(135deg, #07111F 0%, #0A1424 52%, #0E1A2E 100%)",
        "plot_grid": "rgba(124, 184, 255, 0.15)",
        "plot_zero": "rgba(231, 238, 248, 0.20)",
    },
}


def initialize_theme_state():
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "light"


def toggle_theme_mode():
    initialize_theme_state()
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"


def get_theme_mode():
    initialize_theme_state()
    return "dark" if st.session_state.theme_mode == "dark" else "light"


def get_theme_tokens(theme_mode=None):
    mode = theme_mode or get_theme_mode()
    return THEME_TOKENS["dark" if mode == "dark" else "light"].copy()


def build_plot_theme(theme_mode=None):
    mode = theme_mode or get_theme_mode()
    tokens = get_theme_tokens(mode)
    dyn_template = "plotly_dark" if mode == "dark" else "plotly_white"
    tv_layout = {
        "template": dyn_template,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "'Inter', sans-serif", "size": 14, "color": tokens["text_primary"]},
        "xaxis": {
            "showgrid": True,
            "gridcolor": tokens["plot_grid"],
            "gridwidth": 1,
            "zeroline": False,
            "linecolor": tokens["plot_zero"],
            "tickfont": {"color": tokens["text_muted"]},
            "title": {"font": {"color": tokens["text_primary"]}},
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": tokens["plot_grid"],
            "gridwidth": 1,
            "zeroline": False,
            "linecolor": tokens["plot_zero"],
            "tickfont": {"color": tokens["text_muted"]},
            "title": {"font": {"color": tokens["text_primary"]}},
        },
        "legend": {"font": {"color": tokens["text_primary"]}},
        "margin": {"l": 40, "r": 15, "t": 40, "b": 40},
    }
    colors = {
        "blue": tokens["accent"],
        "orange": tokens["warning"],
        "green": tokens["success"],
        "red": tokens["danger"],
    }
    return dyn_template, tv_layout, colors
