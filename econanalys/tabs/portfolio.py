import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

from econanalys.ui import metric_html


def render(tv_layout, dyn_template, colors):
    color_blue = colors["blue"]
    color_orange = colors["orange"]
    color_green = colors["green"]
    color_red = colors["red"]
    st.markdown("<br>", unsafe_allow_html=True)
    col_port_in, col_port_chart = st.columns([1.2, 2.8])
    with col_port_in:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> PORTFÖY SEÇİMİ</div>", unsafe_allow_html=True)
            st.info(" **BIST Uyumluluğu:** Borsa İstanbul (BİST) hisselerinin sonuna mutlaka **.IS** takısını kullanın. Yeni halka arzlar veri eksikliği yaratabilir, Ledoit-Wolf yöntemi bunu tolere etmektedir.\n\n**Örnek:** `THYAO.IS, TUPRS.IS, FROTO.IS, EREGL.IS, GARAN.IS`")
            port_symbols = st.text_input("Semboller (Virgül ile, maks 5):", value="THYAO.IS, TUPRS.IS, FROTO.IS, EREGL.IS, GARAN.IS")
            port_period = st.selectbox("Analiz Süresi (Geçmiş Veri Derinliği):", ["1 Yıl", "3 Yıl", "5 Yıl"])
            opt_btn = st.button("Ağırlıkları Hesapla & Analiz Et", use_container_width=True)

    with col_port_chart:
        if 'opt_w' not in st.session_state: st.session_state['opt_w'] = None
        if 'opt_p' not in st.session_state: st.session_state['opt_p'] = None
        if 'opt_df' not in st.session_state: st.session_state['opt_df'] = pd.DataFrame()

        if opt_btn:
            syms = [s.strip() for s in port_symbols.split(",") if s.strip()][:5] # Max 5 hisse
            period_map = {"1 Yıl": "1y", "3 Yıl": "3y", "5 Yıl": "5y"}
            y_period = period_map[port_period]
            expected_years = int(y_period[0])

            if len(syms) >= 2:
                try:
                    _raw = yf.download(syms, period=y_period, progress=False)
                    df_p = _raw['Close'] if _raw is not None and 'Close' in _raw else None
                    if df_p is not None:
                        if isinstance(df_p, pd.Series): df_p = pd.DataFrame({syms[0]: df_p})
                        if isinstance(df_p.columns, pd.MultiIndex): df_p.columns = df_p.columns.droplevel(1)

                        # Data Depth Verification
                        today = pd.Timestamp.now(tz=df_p.index.tz if len(df_p) > 0 else None)
                        for sym in df_p.columns:
                            first_valid = df_p[sym].dropna().index.min()
                            if pd.isna(first_valid):
                                st.warning(f" **{sym}** için hiç veri bulunamadı. Lütfen sembolü kontrol edin.")
                            else:
                                days_diff = (today - first_valid).days
                                if days_diff < (expected_years * 365 - 30):
                                    st.warning(f" **{sym}** hissesinin tam {expected_years} yıllık piyasa verisi yoktur (En eski veri: {first_valid.strftime('%d.%m.%Y')}). Analize mevcut olan süreç dahil edildi.")

                        if not df_p.empty:
                            df_p = df_p.dropna()
                            mu = expected_returns.mean_historical_return(df_p)
                            # Robust Covariance Estimation via Ledoit-Wolf Shrinkage
                            S = risk_models.CovarianceShrinkage(df_p).ledoit_wolf()

                            ef = EfficientFrontier(mu, S, weight_bounds=(0, 0.50))
                            ef.max_sharpe()
                            st.session_state['opt_w'] = ef.clean_weights()
                            st.session_state['opt_p'] = ef.portfolio_performance(verbose=False)
                            st.session_state['opt_df'] = df_p
                            st.session_state['opt_period'] = y_period
                except Exception as e:
                    st.error(f"Optimizasyon hatası: {str(e)}")

            if st.session_state.get('opt_w'):
                with st.container(border=True):
                    st.markdown("<div class='tv-title'> EFFICIENT FRONTIER AĞIRLIKLARI</div>", unsafe_allow_html=True)
                    w_df = pd.DataFrame(list(st.session_state['opt_w'].items()), columns=["Varlık", "Agirlik"])
                    fig = go.Figure(data=[go.Pie(labels=w_df['Varlık'], values=w_df['Agirlik'], hole=.45, textinfo='label+percent', textfont_size=14, marker={"colors": [color_blue, color_orange, color_green, color_red, '#00B0FF'], "line": {"color": 'rgba(0,0,0,0)', "width": 2}})])
                    fig.update_layout(template=dyn_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={"t": 10, "b": 10}, height=400)
                    st.plotly_chart(fig, width="stretch", use_container_width=True)

                    p0, p1, p2 = st.session_state['opt_p']
                    cp1, cp2, cp3 = st.columns(3)
                    cp1.markdown(metric_html("Beklenen Getiri", f"{p0*100:.1f}%", color_blue), unsafe_allow_html=True)
                    cp2.markdown(metric_html("Volatilite", f"{p1*100:.1f}%", color_red), unsafe_allow_html=True)
                    cp3.markdown(metric_html("Sharpe Oranı", f"{p2:.2f}", color_green), unsafe_allow_html=True)

                    with st.container(border=True):
                        st.markdown("<div class='tv-title'> KORELASYON MATRİSİ (Isı Haritası)</div>", unsafe_allow_html=True)
                        df_corr = st.session_state.get('opt_df').corr()

                        high_corr_warning = False
                        high_pairs = []
                        for i in range(len(df_corr.columns)):
                            for j in range(i+1, len(df_corr.columns)):
                                if df_corr.iloc[i, j] > 0.8:
                                    high_corr_warning = True
                                    high_pairs.append(f"{df_corr.columns[i]}-{df_corr.columns[j]}")

                        fig_c = go.Figure(data=go.Heatmap(
                            z=df_corr.values, x=df_corr.columns, y=df_corr.columns,
                            colorscale='RdBu', zmin=-1, zmax=1, text=np.round(df_corr.values, 2), texttemplate="%{text}"
                        ))
                        fig_c.update_layout(**tv_layout)
                        fig_c.update_layout(height=400, margin={"t":20,"b":20})
                        st.plotly_chart(fig_c, width="stretch", use_container_width=True)

                        if high_corr_warning:
                            st.warning(f" **Yapay Zeka Risk Uyarısı:** Seçtiğiniz portföydeki bazı hisseler ({', '.join(high_pairs)}) birbirleriyle **çok yüksek pozitif korelasyona (>0.8)** sahip. Bu durum aynı sektörden çok fazla hisse seçtiğinizi veya piyasa riskini çeşitlendiremediğinizi gösterir. Düşüş anında portföyünüz aynı anda topyekün zarar edebilir!")
                        else:
                            st.success(" **Yapay Zeka Risk Denetimi:** Hisse seçiminde tehlikeli derecede yüksek bir korelasyon (0.8+) tespit edilmedi. Portföy çeşitlendirmesi makul risk seviyesinde.")
            else:
                with st.container(border=True):
                    st.info("Hesaplamak için yandaki butona basın.")
