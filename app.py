import streamlit as st

from database import init_db
from econanalys.auth import do_logout, initialize_session_state, render_auth_guard
from econanalys.tabs import dashboard, inflation, islm, macro, micro, portfolio, stocks
from econanalys.theme import build_plot_theme, get_theme_mode, initialize_theme_state, toggle_theme_mode
from econanalys.ui import inject_styles, render_app_header, render_footer_glossary

st.set_page_config(layout="wide", page_title="EconAnalys", page_icon="")

init_db()
initialize_session_state()
initialize_theme_state()
theme_mode = get_theme_mode()
inject_styles(theme_mode)

if not render_auth_guard():
    st.stop()

dyn_template, tv_layout, colors = build_plot_theme(theme_mode)
macro.init_macro()
render_app_header(st.session_state.username, do_logout, toggle_theme_mode, theme_mode)

tab_gosterge, tab_makro, tab_mikro, tab_islm, tab_borsa, tab_portfoy, tab_enflasyon = st.tabs([
    "GÖSTERGE PANELİ", "MAKRO SİMÜLASYON", "MİKRO İKTİSAT", "IS-LM ANALİZİ", "BORSA TAKİP", "PORTFÖY", "ENFLASYON"
])

with tab_gosterge:
    dashboard.render()

with tab_makro:
    macro.render(tv_layout, dyn_template, colors)

with tab_mikro:
    micro.render(tv_layout, colors)

with tab_islm:
    islm.render(tv_layout, colors)

with tab_borsa:
    stocks.render(tv_layout, colors)

with tab_portfoy:
    portfolio.render(tv_layout, dyn_template, colors)

with tab_enflasyon:
    inflation.render(tv_layout, colors)

render_footer_glossary()
