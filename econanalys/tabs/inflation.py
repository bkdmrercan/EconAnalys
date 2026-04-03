import numpy as np
import plotly.graph_objects as go
import streamlit as st

from econanalys.ui import metric_html


def render(tv_layout, colors):
    color_green = colors["green"]
    color_red = colors["red"]
    st.markdown("<br>", unsafe_allow_html=True)
    e_col1, e_col2 = st.columns([1.5, 2.5])

    with e_col1:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> PARAMETRELER</div>", unsafe_allow_html=True)
            start_val = st.number_input("Başlangıç Portföy Büyüklüğü (TL)", min_value=1000.0, value=100000.0, step=5000.0)
            term_years = st.slider("Yatırım Süresi (Yıl)", min_value=1, max_value=20, value=5)
            nom_ret = st.slider("Yıllık Beklenen Nominal Getiri (%)", min_value=-50, max_value=200, value=65)
            inf_rate = st.slider("Öngörülen Yıllık Enflasyon (TÜFE, %)", min_value=0, max_value=150, value=50)
            rf_rate = st.slider("Risksiz Faiz Oranı (%)", min_value=0, max_value=100, value=45)

            # Fisher Equation Calculations
            n_dec = nom_ret / 100.0
            i_dec = inf_rate / 100.0
            r_dec = ((1 + n_dec) / (1 + i_dec)) - 1
            real_ret = r_dec * 100

            st.markdown("<hr style='border-color:rgba(255,255,255,0.1); margin:15px 0;'>", unsafe_allow_html=True)
            m_a1, m_a2 = st.columns(2)
            m_a1.markdown(metric_html("Nominal Portföy Getirisi", f"%{nom_ret:.1f}"), unsafe_allow_html=True)

            r_color = color_green if real_ret >= 0 else color_red
            m_a2.markdown(metric_html("Enflasyon Arındırılmış Reel Getiri", f"%{real_ret:.1f}", r_color), unsafe_allow_html=True)

            if real_ret < 0:
                st.markdown("<br>", unsafe_allow_html=True)
                st.error(f" Portföyünüz nominal olarak yükselse de de satın alma gücünüz yıllık bileşik olarak **%{abs(real_ret):.1f} oranında azalmıştır!**")

    with e_col2:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> ZAMAN SERİSİ: NOMİNAL VS REEL BÜYÜME</div>", unsafe_allow_html=True)

            years = np.arange(0, term_years + 1)
            nominal_vals = start_val * ((1 + n_dec) ** years)
            real_vals = start_val * ((1 + r_dec) ** years)

            fig_e = go.Figure()
            # Alt alan (Reel Değer - Satın Alma Gücü)
            fig_e.add_trace(go.Scatter(
                x=years, y=real_vals, name='Reel Satın Alma Gücü', 
                line=dict(color=color_green, width=2), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.2)'
            ))
            # Üst alan (Nominal değer, fark = Enflasyon Kaybı)
            fig_e.add_trace(go.Scatter(
                x=years, y=nominal_vals, name='Nominal Değer (Enflasyon Kaybı)', 
                line=dict(color=color_red, width=2, dash='dash'), fill='tonexty', fillcolor='rgba(239, 68, 68, 0.15)'
            ))

            fig_e.update_layout(**tv_layout)
            fig_e.update_layout(
                height=350, margin={"t":20, "b":20, "l":20, "r":20},
                xaxis_title="Yıl", yaxis_title="Portföy Değeri (TL)"
            )
            st.plotly_chart(fig_e, use_container_width=True)

            loss_tl = nominal_vals[-1] - real_vals[-1]
            st.markdown(f"<div style='text-align:center; font-size:0.95rem; margin-top:-10px; color:{color_red}; font-weight:600;'> {term_years}. Yılın sonunda portföyünüzün <b>{loss_tl:,.0f} TL</b>'lik kısmı enflasyon karşısında değer kaybetmiştir.</div>", unsafe_allow_html=True)

        with st.expander(" Baş Analist Değerlendirmesi: Paranın Zaman Değeri & Fırsat Maliyeti", expanded=True):
            st.markdown(f"""
            **Ekonomik Yorum (AI Simülasyonu):**
            Bu senaryoda yatırımcı, başlangıçta belirlediği **%{nom_ret} nominal getiri** ile büyüleyici bir "Para Yanılsaması" (Money Illusion) içerisine düşme riski taşımaktadır.

            - **Satın Alma Gücü Paritesi:** Piyasadaki **%{inf_rate} enflasyon gerçeği**, *Fisher Denklemi* prensibiyle portföyünüzün gerçek kapasitesini reel olarak **%{real_ret:.1f}** bandına sıkıştırmıştır. 
            - **Fırsat Maliyeti Çıkmazı:** Paranızı riske atarak bir portföy yönetiyorsunuz. Yatırımın en basit alternatifi olan risksiz faizin **%{rf_rate}** olduğu bir piyasada, aldığınız *risk priminin* reel enflasyon aşınmasını ne kadar kompanse ettiği tartışmalıdır.
            - **Negatif Reel Faiz Tuzağı:** Eğer reel getiriniz sıfırın altındaysa paranız miktar (nominal) olarak artarken, sepetinizdeki ürünler (satın alma gücü) hızla azalmaktadır. Aslında "büyümüyor", sürekli olarak piyasaya gizli bir enflasyon vergisi ödüyorsunuz demektir.

            *Sonuç olarak etkili bir portföy kurgusu grafikteki kırmızı alanı (Enflasyon Kaybı) en aza indiren enstrümanlara yönelmeli ve sadece risksiz faizi değil, fiili enflasyonu da yenebilmelidir.*
            """)
