import numpy as np
import plotly.graph_objects as go
import streamlit as st

from econanalys.ui import metric_html


def render(tv_layout, colors):
    color_blue = colors["blue"]
    color_orange = colors["orange"]
    color_green = colors["green"]
    color_red = colors["red"]
    st.markdown("<br>", unsafe_allow_html=True)
    col_is_in, col_is_chart = st.columns([1.2, 2.8])
    with col_is_in:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> PARA POLİTİKASI (LM)</div>", unsafe_allow_html=True)
            M_P = st.slider("Reel Para Arzı (M/P):", 100.0, 1000.0, 250.0, 10.0)
            st.markdown("<div style='font-size:0.85rem; margin-top:-10px; margin-bottom:15px; color:#2563EB;'><b>Formül:</b> i = (k/h)Y - (1/h)(M/P)</div>", unsafe_allow_html=True)
            k_lm = st.slider("Para Talebi Gelir Duyarlılığı (k):", 0.0, 1.0, 0.5, 0.05, help="İşlem amacıyla tutulan nakit oranıdır. (0 ile 1 arasında değer alır)")
            lm_sens = st.selectbox("Para Talebi Faiz Duyarlılığı Özel Durum (h):", ["Normal", "Likidite Tuzağı", "Klasik Durum"], help="Likidite Tuzağı: Yatay LM | Klasik: Dikey LM")

            if lm_sens == "Normal":
                h_manual = st.slider("Para Talebi Faiz Duyarlılığı (h):", 1.0, 200.0, 50.0, 1.0, help="h: Para talebinin faize duyarlılığı (Normal bölgede hareket).")
                i_min = 0.0
            elif lm_sens == "Likidite Tuzağı":
                h_manual = 50.0
                i_min = st.slider("Asgari Faiz Sınırı (Zero Lower Bound):", 0.0, 5.0, 0.5, 0.1, help="Kriz/Tuzak anında faizin inebileceği en dip seviye.")
            else:
                h_manual = 50.0
                i_min = 0.0


        with st.container(border=True):
            st.markdown("<div class='tv-title'> MALİYE POLİTİKASI (IS)</div>", unsafe_allow_html=True)
            G_is = st.slider("Kamu Harcamaları (G):", 0.0, 1000.0, 200.0, 10.0)
            t_is = st.slider("Vergi Oranı (t):", 0.0, 0.50, 0.20, 0.01)
            b_is = st.slider("Yatırımların Faize Duyarlılığı (b):", 0.0, 200.0, 15.0, 1.0, help="Eğer b=0 ise IS eğrisi tam dik olur (Yatırım faizden etkilenmez). b büyüdükçe IS eğrisi yatıklaşır.")
            st.markdown("<div style='font-size:0.85rem; margin-top:-10px; margin-bottom:10px; color:#2563EB;'><b>Formül:</b> Y = α(A₀ - bi)</div>", unsafe_allow_html=True)

    with col_is_chart:
        # Scenario h calculation
        if lm_sens == "Likidite Tuzağı":
            scen_color = color_green
            h_val = 1e10  # Sonsuz kabul edilir (Yatay LM)
        elif lm_sens == "Klasik Durum":
            scen_color = color_red
            h_val = 0.0001    # Sıfıra çok yakın (Dikey LM)
        else:
            scen_color = color_orange
            h_val = float(h_manual) # Normalden gelen manuel h

        # Yatırım Duyarsızlığı (Sıfıra bölünmeyi önlemek için asimptotik değer)
        b_calc = 0.0001 if b_is == 0 else float(b_is)

        with st.container(border=True):
            st.markdown("<div class='tv-title'> IS-LM MODELİ KESİŞİMİ</div>", unsafe_allow_html=True)

            # IS Hesaplamaları
            C_0, I_0, X_0, M_0_imp = 100.0, 150.0, 100.0, 50.0
            A_0 = C_0 + I_0 + G_is + X_0 - M_0_imp
            c_val, m_val = 0.8, 0.15
            alpha_b = 1 - c_val * (1 - t_is) + m_val
            multiplier_is = 1 / alpha_b if alpha_b > 0.0001 else 2.0

            # Kesişim Noktası Hesabı
            if lm_sens == "Likidite Tuzağı":
                eq_i = i_min
                Y_is_eq = multiplier_is * (A_0 - b_calc * eq_i)
            else:
                Y_is_eq = ( (A_0 / b_calc) + (M_P / h_val) ) / ( (1.0 / (multiplier_is * b_calc)) + (k_lm / h_val) )
                eq_i = (k_lm / h_val) * Y_is_eq - (M_P / h_val)

                # Negatif faiz olmaması için tavan vuruşu kısıtlaması (Zero Lower Bound)
                if eq_i < i_min:
                    eq_i = i_min
                    Y_is_eq = multiplier_is * (A_0 - b_calc * eq_i)

            # Auto-Scale eksen limitleri
            x_max = max(Y_is_eq * 1.5, 500.0)
            y_max = max(eq_i * 2.0, 10.0)

            # Veri aralığını genişleterek grafiğin sonuna kadar uzat
            y_is_curve_plot = np.linspace(0, x_max * 1.5, 400)
            i_is_plot = (A_0 / b_calc) - (y_is_curve_plot / (multiplier_is * b_calc))

            if lm_sens == "Klasik Durum":
                # K curve correction to avoid zero division error
                safe_k = k_lm if k_lm > 0.0001 else 0.0001
                y_lm_plot, i_lm_plot = [], [] # Verileri boş tut, add_vline kullan
            elif lm_sens == "Likidite Tuzağı":
                y_lm_plot = np.linspace(0, x_max * 1.5, 400)
                i_lm_plot = np.full(400, i_min)
            else:
                y_lm_plot = np.linspace(0, x_max * 1.5, 400)
                i_lm_plot = (k_lm / h_val) * y_lm_plot - (M_P / h_val)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=y_is_curve_plot, y=i_is_plot, name='IS Eğrisi', line={"color": color_blue, "width": 3}, hovertemplate="Y: %{x:.1f}<br>i: %{y:.2f}%<extra></extra>"))

            if lm_sens == "Klasik Durum":
                # Matplotlib/Plotly dikey çizgi komutu
                vline_x = M_P / safe_k
                fig.add_vline(x=vline_x, line_width=3, line_color=scen_color)
                # Lejant için sahte trace
                fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='LM Eğrisi', line={"color": scen_color, "width": 3}))
            else:
                fig.add_trace(go.Scatter(x=y_lm_plot, y=i_lm_plot, name='LM Eğrisi', line={"color": scen_color, "width": 3}, hovertemplate="Y: %{x:.1f}<br>i: %{y:.2f}%<extra></extra>"))

            fig.add_trace(go.Scatter(x=[Y_is_eq], y=[eq_i], mode='markers', name='Denge (P*, Q*)', marker={"color": '#111827', "size": 11}, hovertemplate="Denge Geliri (Q*): %{x:.1f}<br>Denge Faizi (P*): %{y:.2f}%<extra></extra>"))

            fig.add_shape(type="line", x0=0, y0=eq_i, x1=Y_is_eq, y1=eq_i, line={"color": "#111827", "width": 1, "dash": "dot"}, opacity=0.4)
            fig.add_shape(type="line", x0=Y_is_eq, y0=0, x1=Y_is_eq, y1=eq_i, line={"color": "#111827", "width": 1, "dash": "dot"}, opacity=0.4)

            fig.update_layout(**tv_layout)
            fig.update_layout(height=480)
            fig.update_xaxes(title="Milli Gelir (Y)", range=[0, x_max])
            fig.update_yaxes(title="Faiz Oranı (i)", range=[0, y_max])
            st.plotly_chart(fig, use_container_width=True)

            c_is1, c_is2, c_is3 = st.columns(3)
            c_is1.markdown(metric_html("IS-LM Denge (Y*)", f"{Y_is_eq:.1f}", scen_color), unsafe_allow_html=True)
            c_is2.markdown(metric_html("Faiz Oranı (i*)", f"{eq_i:.2f}%", "#111827"), unsafe_allow_html=True)

            # Crowding Out Hesaplama (Tam çarpan durumuna kıyasla yatırım kaybı)
            crowded_inv = b_calc * eq_i if eq_i > 0 else 0
            crowded_y = multiplier_is * crowded_inv

            if lm_sens == "Likidite Tuzağı" or eq_i <= i_min or b_is == 0:
                c_is3.markdown(metric_html("Dışlama Etkisi", "Sıfır Dışlama", color_green), unsafe_allow_html=True)
            elif lm_sens == "Klasik Durum":
                c_is3.markdown(metric_html("Dışlama Etkisi", "Tam Dışlama", color_red), unsafe_allow_html=True)
            else:
                c_is3.markdown(metric_html("Dışlanan Gelir", f"-{crowded_y:.1f}", color_red), unsafe_allow_html=True)

        if crowded_y > 0 and lm_sens != "Likidite Tuzağı" and b_is > 0:
            st.warning(f" **Dışlama Etkisi (Crowding-out):** Faiz oranlarının {eq_i:.2f}% düzeyine çıkması nedeniyle özel sektör yatırımlarından **{crowded_inv:.1f}** birim dışlanmış olup, bunun milli gelir (Y) üzerindeki toplam negatif çarpan etkisi **{crowded_y:.1f}** birim olarak gerçekleşmiştir.")

        with st.expander(" Dinamik Analiz Raporu", expanded=True):
            if lm_sens == "Likidite Tuzağı":
                st.markdown("### Uzman Çıkarımı: Likidite Tuzağı\n- **Para Politikası Etkisi:** LM eğrisi tam yatay olduğundan, Merkez Bankası'nın reel para arzı (M/P) şokları faizi daha da düşüremez. Para politikası **tamamen etkisizdir**.\n- **Maliye Politikası:** Kamu harcamaları (G) artırıldığında hiçbir dışlama etkisi yaşanmaz, özel yatırımlar yerinde sayar. Maliye politikası **tam etkilidir**.\n- **Strateji:** Ekonomi sıfır faiz sınırındaysa ve atıl kapasite mevcutsa, yegâne çözümleyici maliye bakanlığından gelecek bir harcama enjeksiyonu olmalıdır.")
            elif lm_sens == "Klasik Durum":
                st.markdown("### Uzman Çıkarımı: Klasik Durum\n- **Para Politikası Etkisi:** LM eğrisi diktir. Spekülatif para talebi sıfır olduğu için, para arzı artışı faizleri düşürürken geliri doğrudan artırır. Para politikası **tek ve en güçlü araçtır**.\n- **Maliye Politikası:** Yüksek Kamu Harcaması (G), devasa bir faiz şoku yaratarak özel yatırımları birebir piyasadan atar (Tam Crowding-out). Maliye politikası genişlemesi **etkisizdir**.\n- **Strateji:** Klasik tam istihdam varsayımında, mali disiplinden taviz verilmeden sadece arz yönlü reformlarla ve parasal aktarım mekanizmasıyla yönetilmelidir.")
            else:
                st.markdown(f"### Uzman Çıkarımı: Normal (Karma) Durum\n- **Politika Gücü:** Eğrilerin normal seyrettiği bu bölgede (*h* = {lm_sens}), hem mali hem de parasal enstrümanlar üretim hacmi (Y) üzerinde tesirlidir.\n- **Dışlama Karakteristiği:** Uygulanan vergi (t) ve harcama (G) politikası, faizleri iterek yatırımların kısmi oranda erimesine (%{(crowded_y/Y_is_eq*100) if Y_is_eq != 0 else 0:.1f} tahribat) yol açmakta ve kamu sektörünün ekonomideki ağırlığını fiktif şekilde artırmaktadır.\n- **Strateji:** İktisadi denge; faizlerin kontrolden çıkmasını önleyecek akıllı bir politika karmasının (Policy Mix) orantılı kullanılmasıyla maksimize edilebilir.")
