import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots
from pypfopt import expected_returns, risk_models

from econanalys.ui import metric_html


def render(tv_layout, colors):
    color_blue = colors["blue"]
    color_orange = colors["orange"]
    color_green = colors["green"]
    color_red = colors["red"]
    st.markdown("<br>", unsafe_allow_html=True)
    col_sym, col_stock = st.columns([1.2, 2.8])
    with col_sym:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> HİSSE SEÇİMİ</div>", unsafe_allow_html=True)
            symbol = st.text_input("Hisse Sembolü (Yahoo Finance):", value="THYAO.IS")
            st.markdown("<div class='tv-title' style='margin-top:15px;'> İNDİKATÖRLER</div>", unsafe_allow_html=True)
            show_rsi = st.checkbox("RSI (14) Göster", value=False)
            show_bb = st.checkbox("Bollinger Bantları Göster", value=False)

        with st.container(border=True):
            st.markdown("<div class='tv-title'> PORTFÖY ETKİ ANALİZİ</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.85rem; opacity:0.8; margin-bottom:10px;'>Mevcut portföye %20 <b>{symbol}</b> eklenirse:</div>", unsafe_allow_html=True)
            impact_btn = st.button("Etkiyi Hesapla", use_container_width=True)

    with col_stock:
        with st.container(border=True):
            st.markdown(f"<div class='tv-title'> {symbol} FİYAT HAREKETİ & ANALİZ</div>", unsafe_allow_html=True)
            if symbol:
                try:
                    ticker = yf.Ticker(symbol)
                    df = ticker.history(period="1y")
                    if not df.empty:
                        c_price = df['Close'].iloc[-1]
                        df['MA50'] = df['Close'].rolling(window=50).mean()
                        if show_bb:
                            ma20 = df['Close'].rolling(window=20).mean()
                            std20 = df['Close'].rolling(window=20).std()
                            df['BBU'] = ma20 + (std20 * 2)
                            df['BBL'] = ma20 - (std20 * 2)
                        if show_rsi:
                            delta = df['Close'].diff()
                            up = delta.clip(lower=0)
                            down = -1 * delta.clip(upper=0)
                            ema_up = up.ewm(com=13, adjust=False).mean()
                            ema_down = down.ewm(com=13, adjust=False).mean()
                            rs = ema_up / ema_down
                            df['RSI'] = 100 - (100 / (1 + rs))

                        # Subplots for RSI
                        if show_rsi:
                            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
                        else:
                            fig = go.Figure()

                        # Main chart
                        trace_price = go.Scatter(x=df.index, y=df['Close'], name='Kapanış', line={"color": color_blue, "width": 2})
                        trace_ma50 = go.Scatter(x=df.index, y=df['MA50'], name='50 MA', line={"color": color_orange, "width": 1.5, "dash": 'solid'})

                        if show_rsi:
                            fig.add_trace(trace_price, row=1, col=1)
                            fig.add_trace(trace_ma50, row=1, col=1)
                        else:
                            fig.add_trace(trace_price)
                            fig.add_trace(trace_ma50)

                        if show_bb:
                            bb_l = [c for c in df.columns if 'BBL' in c][0]
                            bb_u = [c for c in df.columns if 'BBU' in c][0]
                            trace_bbu = go.Scatter(x=df.index, y=df[bb_u], name='BB Üst', line=dict(color='rgba(255,255,255,0.2)', width=1))
                            trace_bbl = go.Scatter(x=df.index, y=df[bb_l], name='BB Alt', line=dict(color='rgba(255,255,255,0.2)', width=1), fill='tonexty', fillcolor='rgba(255,255,255,0.05)')
                            if show_rsi:
                                fig.add_trace(trace_bbu, row=1, col=1)
                                fig.add_trace(trace_bbl, row=1, col=1)
                            else:
                                fig.add_trace(trace_bbu)
                                fig.add_trace(trace_bbl)

                        if show_rsi:
                            rsi_col = [c for c in df.columns if 'RSI' in c][0]
                            fig.add_trace(go.Scatter(x=df.index, y=df[rsi_col], name='RSI', line={"color": color_orange, "width": 1.5}), row=2, col=1)
                            fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1, opacity=0.5)
                            fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1, opacity=0.5)
                            fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

                        fig.update_layout(**tv_layout)
                        fig.update_layout(height=550 if show_rsi else 450)
                        st.plotly_chart(fig, width="stretch", use_container_width=True)

                        # Info Metrics
                        info = ticker.info
                        pe = info.get('trailingPE', '-')
                        pb = info.get('priceToBook', '-')
                        mc = info.get('marketCap', '-')
                        div = info.get('dividendYield', '-')

                        if isinstance(mc, (int, float)): mc_str = f"{mc / 1e9:.1f} Milyar"
                        else: mc_str = "-"
                        if isinstance(div, (int, float)): div_str = f"%{div*100:.2f}"
                        else: div_str = "-"
                        if isinstance(pe, (int, float)): pe_str = f"{pe:.2f}"
                        else: pe_str = "-"
                        if isinstance(pb, (int, float)): pb_str = f"{pb:.2f}"
                        else: pb_str = "-"

                        m1, m2, m3, m4 = st.columns(4)
                        m1.markdown(metric_html("F/K Oranı", pe_str, color_blue), unsafe_allow_html=True)
                        m2.markdown(metric_html("PD/DD", pb_str, color_orange), unsafe_allow_html=True)
                        m3.markdown(metric_html("Piyasa Değeri", mc_str, color_green), unsafe_allow_html=True)
                        m4.markdown(metric_html("Temettü Verimi", div_str, color_red), unsafe_allow_html=True)

                        # Portfolio Impact Logic
                        if impact_btn:
                            if 'opt_w' in st.session_state and st.session_state['opt_w'] is not None and len(st.session_state['opt_w']) > 0:
                                base_syms = list(st.session_state['opt_w'].keys())
                                if symbol not in base_syms:
                                    test_syms = base_syms + [symbol]
                                else:
                                    test_syms = base_syms

                                cached_period = st.session_state.get('opt_period', '1y')
                                _raw = yf.download(test_syms, period=cached_period, progress=False)
                                df_p = _raw['Close'] if _raw is not None and 'Close' in _raw else None
                                if df_p is not None:
                                    if isinstance(df_p, pd.Series): df_p = pd.DataFrame({test_syms[0]: df_p})
                                    if isinstance(df_p.columns, pd.MultiIndex): df_p.columns = df_p.columns.droplevel(1)
                                    df_p = df_p.dropna()

                                    # old portfolio metrics
                                    w_old = np.array([st.session_state['opt_w'].get(s, 0) for s in df_p.columns])
                                    w_old = w_old / np.sum(w_old) if np.sum(w_old) > 0 else w_old
                                    mu = expected_returns.mean_historical_return(df_p)
                                    S = risk_models.CovarianceShrinkage(df_p).ledoit_wolf()
                                    ret_old = np.dot(w_old, mu)
                                    vol_old = np.sqrt(np.dot(w_old.T, np.dot(S, w_old)))

                                    # new portfolio metrics
                                    w_new = []
                                    for s in df_p.columns:
                                        if s == symbol: w_new.append(0.20)
                                        else: w_new.append(st.session_state['opt_w'].get(s, 0) * 0.80)
                                    w_new = np.array(w_new)
                                    w_new = w_new / np.sum(w_new)
                                    ret_new = np.dot(w_new, mu)
                                    vol_new = np.sqrt(np.dot(w_new.T, np.dot(S, w_new)))

                                    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                                    st.markdown("<div style='font-size:1rem; margin-bottom:10px;'><b>Portföy Etki Analizi (%20 Ağırlıkla Eklenirse)</b></div>", unsafe_allow_html=True)
                                    e1, e2 = st.columns(2)
                                    e1.markdown(metric_html("Beklenen Getiri Değişimi", f"Eski: %{ret_old*100:.1f} → <b>Yeni: %{ret_new*100:.1f}</b>", "#111827"), unsafe_allow_html=True)
                                    vol_color = color_red if vol_new > vol_old else color_green
                                    e2.markdown(metric_html("Volatilite (Risk) Değişimi", f"Eski: %{vol_old*100:.1f} → <b>Yeni: %{vol_new*100:.1f}</b>", vol_color), unsafe_allow_html=True)
                                else:
                                    st.warning("Veri indirilemedi.")
                            else:
                                st.warning("Önce 'Portföy Optimizasyonu' sekmesinden bir ana portföy (agırlıklar) hesaplatmalısınız!")

                        # News
                        news = ticker.news
                        if news and len(news) > 0:
                            with st.expander(" Son Haber Akışı (Son 5 Haber)", expanded=False):
                                count = 0
                                for n in news:
                                    if count >= 5: break

                                    if 'content' in n and isinstance(n['content'], dict):
                                        content = n['content']
                                        title = content.get('title') or 'Başlık Yok'
                                        ct_url = content.get('clickThroughUrl')
                                        if isinstance(ct_url, dict): link = ct_url.get('url', '#')
                                        else: link = '#'
                                        if link == '#':
                                            can_url = content.get('canonicalUrl')
                                            if isinstance(can_url, dict): link = can_url.get('url', '#')
                                        pub_date_str = content.get('pubDate')
                                        pd_str = str(pub_date_str)[:16].replace('T', ' ') if pub_date_str else ""
                                    else:
                                        title = n.get('title') or 'Başlık Yok'
                                        link = n.get('link') or '#'
                                        pub_date = n.get('providerPublishTime', 0)
                                        try:
                                            if pub_date: pd_str = datetime.datetime.fromtimestamp(int(pub_date)).strftime('%d.%m.%Y %H:%M')
                                            else: pd_str = ""
                                        except:
                                            pd_str = ""

                                    st.markdown(f"- **{pd_str}** | [{title}]({link})")
                                    count += 1
                        else:
                            st.info("Bu hisse senedi için güncel yabancı/yerel haber akışı bulunamadı.")
                except Exception as e:
                    st.error(f"Veri çekilirken hata oluştu: {str(e)}")
