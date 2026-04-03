import numpy as np
import plotly.graph_objects as go
import streamlit as st


def render():
    # Beyaz Gölgeli Ana Kart (Container)
    with st.container(border=True):
        # İçeriği sütunlara böl
        col1, col2, col3 = st.columns([1.5, 1, 0.8])

        # --- Sol Sütun: TR Büyüme (GSYH) Tahmini (Area Chart) ---
        with col1:
            st.markdown("<h4 style='color: var(--text-color); font-size: 1.1rem; margin-bottom: 0px;'>Büyüme (GSYH) Tahmini <span title='Kaynak: EconAnalys Model (TÜİK temel verileri kullanılarak hesaplanmıştır). Ekonomik büyümenin gelecekteki seyrini gösteren öngörüdür.' style='cursor:help; opacity:0.5; font-size:0.9rem;'>ⓘ</span></h4>", unsafe_allow_html=True)

            # Yer tutucu veriler
            x_data = ['Eki 25', 'Kas 25', 'Ara 25', 'Oca 26', 'Mar 26', 'Nis 26']
            y_data = [1.7, 1.45, 2.3, 2.0, 2.3, 1.9, 1.3, 2.1, 2.8, 2.8, 3.4]
            x_val = np.linspace(0, 5, len(y_data))

            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=x_val, y=y_data,
                fill='tozeroy',
                mode='lines',
                line=dict(color='#0ea5e9', width=3),
                fillcolor='rgba(14, 165, 233, 0.2)'
            ))
            fig_area.update_layout(
                margin=dict(l=0, r=0, t=20, b=20),
                height=300,
                xaxis=dict(showgrid=False, tickmode='array', tickvals=np.linspace(0,5,6), ticktext=x_data, linecolor='rgba(128,128,128,0.2)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', range=[1.0, 3.5], tick0=1.0, dtick=0.5),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_area, use_container_width=True)

        # --- Orta Sütun: Dropdown ve Özelleştirilmiş Tablo ---
        with col2:
            st.markdown("""
            <div style='display: flex; justify-content: flex-end; margin-bottom: 10px;'>
                <select style='padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border-color); outline: none; font-size: 0.8rem; background-color: var(--secondary-background-color); color: var(--text-color);'>
                    <option>Gerçek Zamanlı Tahmin</option>
                </select>
            </div>
            """, unsafe_allow_html=True)

            html_table = """
            <table class='custom-table'>
                <thead>
                    <tr>
                        <th>Ekonomi <span title='Temel ekonomik göstergelerin listesi' style='cursor:help; opacity:0.5;'>ⓘ</span></th>
                        <th>Yüzde</th>
                        <th>Değişim</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class='active-row'>
                        <td title='Kaynak: EconAnalys Model (TÜİK bazlı). GSYH büyüme beklentisi.'>Büyüme Tahmini</td>
                        <td>%2.20</td>
                        <td class='positive-change'>+%1.72</td>
                    </tr>
                    <tr>
                        <td title='Kaynak: Yahoo Finance. Piyasaların genel sağlık ve hacim durumu.'>Piyasa Durumu</td>
                        <td>%0.43</td>
                        <td class='positive-change'>+%0.28</td>
                    </tr>
                    <tr>
                        <td title='Kaynak: TCMB & Yahoo Finance. Yatırımcı güveni ve psikolojik yaklaşımı.'>Piyasa Duyarlılığı</td>
                        <td>%0.38</td>
                        <td class='positive-change'>+%1.68</td>
                    </tr>
                    <tr>
                        <td title='Kaynak: TÜİK. Toplam üretim kapasitesi ve pazar hacmi.'>Ekonomik Büyüklük</td>
                        <td>%0.20</td>
                        <td class='negative-change'>-%0.39</td>
                    </tr>
                    <tr>
                        <td title='Kaynak: TÜİK. İşgücü piyasası ve yeni iş yaratma kapasitesi.'>İstihdam</td>
                        <td>%1.00</td>
                        <td class='positive-change'>+%0.86</td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)

        # --- Sağ Sütun: Piyasa Duyarlılığı (Gauges) ---
        with col3:
            st.markdown("<h4 style='color: var(--text-color); font-size: 1.1rem; margin-bottom: 20px; text-align: center;'>Piyasa Duyarlılığı <span title='Kaynak: TCMB ve Yahoo Finance. Yatırımcıların güven endeksi ve korku/açgözlülük metriklerini yansıtır.' style='cursor:help; opacity:0.5; font-size:0.9rem;'>ⓘ</span></h4>", unsafe_allow_html=True)

            # İlk Gauge Grafiği
            fig_gauge1 = go.Figure(go.Indicator(
                mode = "gauge",
                value = 75,
                domain = {'x': [0.1, 0.9], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(0,0,0,0)", 'tickvals': [0, 50, 100], 'ticktext': ['0', 'Seviye', '100']},
                    'bar': {'color': "#0369a1"}, 
                    'bgcolor': "rgba(128,128,128,0.2)",
                    'borderwidth': 0,
                }
            ))
            fig_gauge1.update_layout(height=140, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

            # İkinci Gauge Grafiği
            fig_gauge2 = go.Figure(go.Indicator(
                mode = "gauge",
                value = 45,
                domain = {'x': [0.1, 0.9], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(0,0,0,0)", 'tickvals': [0, 50, 100], 'ticktext': ['0', 'Seviye', '100']},
                    'bar': {'color': "#38bdf8"},
                    'bgcolor': "rgba(128,128,128,0.2)",
                    'borderwidth': 0,
                }
            ))
            fig_gauge2.update_layout(height=140, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

            st.plotly_chart(fig_gauge1, use_container_width=True)
            st.plotly_chart(fig_gauge2, use_container_width=True)

    # --- Bilgi ve Kaynakça Bölümü ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        info_col1, info_col2 = st.columns([2, 1.2])

        with info_col1:
            st.markdown("<h5 style='color: var(--accent); margin-top:0;'>Gösterge Tanımları ve İşlevleri</h5>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-size: 0.85rem; line-height: 1.6; opacity: 0.9;'>
                <b>• Büyüme (GSYH) Tahmini:</b> Ekonomik canlılığın temel ölçütüdür. Gelecekteki üretim artışını öngörerek yatırım kararlarını şekillendirir.<br>
                <b>• Piyasa Durumu:</b> Finansal piyasaların derinliğini ve likiditesini gösterir. Düşük değerler volatilite riskine işaret eder.<br>
                <b>• Piyasa Duyarlılığı:</b> Yatırımcı psikolojisini ölçer. Paniği veya aşırı iyimserliği tespit ederek piyasa dönüşlerini anlamaya yardımcı olur.<br>
                <b>• Ekonomik Büyüklük:</b> Ülkenin toplam çıktı kapasitesini ve pazarın mutlak değerini izlemek için kullanılır.<br>
                <b>• İstihdam:</b> Sosyal refahın ve üretim gücünün göstergesidir. Tüketim harcamaları üzerinde doğrudan etkilidir.
            </div>
            """, unsafe_allow_html=True)

        with info_col2:
            st.markdown("<h5 style='color: var(--accent); margin-top:0;'>Veri & Kaynak Eşleşmesi</h5>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-size: 0.85rem; line-height: 1.6; opacity: 0.9;'>
                <b>• TÜİK:</b> Ekonomik Büyüklük, İstihdam.<br>
                <b>• TCMB:</b> Piyasa Duyarlılığı (Güven Endeksleri).<br>
                <b>• Yahoo Finance:</b> Piyasa Durumu, Canlı Borsa.<br>
                <b>• EconAnalys:</b> Büyüme Tahmini (Model Tahminleri).
            </div>
            """, unsafe_allow_html=True)
