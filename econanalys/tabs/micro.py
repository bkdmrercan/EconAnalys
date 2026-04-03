import numpy as np
import plotly.graph_objects as go
import streamlit as st

from econanalys.formulas import clean_formula, safe_eval_formula
from econanalys.ui import metric_html


def render(tv_layout, colors):
    color_blue = colors["blue"]
    color_orange = colors["orange"]
    st.markdown("<br>", unsafe_allow_html=True)
    col_m_in, col_m_chart = st.columns([1.2, 2.8])
    with col_m_in:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> MİKRO PARAMETRELER</div>", unsafe_allow_html=True)
            demand_formula = st.text_input("Talep Fonksiyonu ($P_d$):", value="")
            supply_formula = st.text_input("Arz Fonksiyonu ($P_s$):", value="")

            st.markdown("""
            <div style='font-size: 0.8rem; color: #666; margin-top: -10px; margin-bottom: 10px; padding: 5px; background-color: rgba(0,0,0,0.03); border-radius: 4px;'>
            <b> Örnek Kullanım:</b><br>
            Varsayılan Doğrusal: <code>100 - 2*Q</code> ve <code>20 + 3*Q</code><br>
            Karesel: <code>50 - 0.5*Q^2</code>
            </div>
            """, unsafe_allow_html=True)

            tax = st.slider("Arzı Kaydır (Vergi):", -50, 50, 0)
            calc_price = st.slider("Esneklik Noktası (P):", 0.0, 200.0, 0.0)
            x_min, x_max = st.slider("X (Miktar):", 0, 200, (0, 100))
            y_min, y_max = st.slider("Y (Fiyat):", 0, 500, (0, 150))
    with col_m_chart:
        with st.container(border=True):
            st.markdown("<div class='tv-title'> ARZ & TALEP DENGESİ</div>", unsafe_allow_html=True)
            x_arr = np.linspace(x_min, x_max, 4000)
            y_dem, y_sup, eq_q, eq_p, els = None, None, None, None, None
            try:
                yd = safe_eval_formula(clean_formula(demand_formula), x_arr)
                y_dem = np.where(np.isinf(yd)|np.isnan(yd), np.nan, yd) if not np.isscalar(yd) else np.full_like(x_arr, float(np.real(yd)))
                ys = safe_eval_formula(clean_formula(supply_formula), x_arr + tax)
                y_sup = np.where(np.isinf(ys)|np.isnan(ys), np.nan, ys) if not np.isscalar(ys) else np.full_like(x_arr, float(np.real(ys)))
                diff = y_dem - y_sup
                m = ~(np.isnan(y_dem) | np.isnan(y_sup))
                if np.any(m):
                    idx = np.argmin(np.abs(diff[m]))
                    t_id = np.arange(len(diff))[m][idx]
                    if abs(diff[t_id]) < max(1.0, float((y_max-y_min)*0.02)): eq_q, eq_p = x_arr[t_id], (y_dem[t_id] + y_sup[t_id])/2
                m2 = ~np.isnan(y_dem)
                if np.any(m2):
                    idx_p = np.argmin(np.abs(y_dem[m2] - calc_price))
                    if abs(y_dem[m2][idx_p] - calc_price) < 5:
                        vx, vy = x_arr[m2], y_dem[m2]
                        if 0 < idx_p < len(vx)-1 and (vy[idx_p+1]-vy[idx_p-1])!=0 and vx[idx_p]!=0: els = abs(((vx[idx_p+1]-vx[idx_p-1])/(vy[idx_p+1]-vy[idx_p-1]))*(vy[idx_p]/vx[idx_p]))
            except: pass
            fig = go.Figure()
            if y_dem is not None: fig.add_trace(go.Scatter(x=x_arr, y=y_dem, name='Talep', line={"color": color_blue, "width": 2.5}))
            if y_sup is not None: fig.add_trace(go.Scatter(x=x_arr, y=y_sup, name='Arz', line={"color": color_orange, "width": 2.5}))
            if eq_q: 
                fig.add_trace(go.Scatter(x=[eq_q], y=[eq_p], mode='markers', name='Denge', marker={"color": '#111827', "size": 9}))
                fig.add_shape(type="line", x0=0, y0=eq_p, x1=eq_q, y1=eq_p, line={"color": "#111827", "width": 1, "dash": "dot"}, opacity=0.4)
                fig.add_shape(type="line", x0=eq_q, y0=0, x1=eq_q, y1=eq_p, line={"color": "#111827", "width": 1, "dash": "dot"}, opacity=0.4)
            fig.update_layout(**tv_layout); fig.update_layout(height=450); fig.update_xaxes(title="Miktar (Q)", range=[x_min, x_max]); fig.update_yaxes(title="Fiyat (P)", range=[y_min, y_max])
            st.plotly_chart(fig, use_container_width=True)

    c_res1, c_res2 = st.columns(2)
    c_res1.markdown(metric_html("Piyasa Dengesi (P*, Q*)", f"P*: {eq_p:.1f} | Q*: {eq_q:.1f}" if eq_q else "-", color_blue), unsafe_allow_html=True)
    c_res2.markdown(metric_html("Nokta Esnekliği", f"|ε| = {els:.2f}" if els else "-", color_orange), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='tv-title' style='background-color: rgba(37,99,235,0.05) !important; color: #2563EB !important; border-color: rgba(37,99,235,0.2) !important;'> EKONOMİK YORUM RAPORU</div>", unsafe_allow_html=True)
        if eq_p is not None and eq_q is not None:
            if els is None:
                esneklik_yorumu = "Esneklik tam hesaplanamamış olsa da grafiğin eğiminden anlaşılacağı üzere kendine has bir talep duyarlılığı bulunmaktadır."
            elif els > 1:
                esneklik_yorumu = f"Nokta esnekliği (|ε| = {els:.2f}) 1'den büyük olduğu için <b>talep esnektir</b>. Tüketiciler fiyat değişimlerine karşı oldukça duyarlıdır; fiyattaki küçük bir artış, talep edilen miktarda nispi olarak daha büyük bir düşüşe yol açacaktır. Üreticinin fiyat artırma gücü sınırlıdır."
            elif els < 1:
                esneklik_yorumu = f"Nokta esnekliği (|ε| = {els:.2f}) 1'den küçük olduğu için <b>talep inelastiktir (katıdır)</b>. Tüketiciler fiyata karşı nispeten duyarsızdır. Bu durum genellikle zorunlu mallarda veya yakın ikamesi olmayan spesifik ürünlerde gözlemlenir."
            else:
                esneklik_yorumu = f"Nokta esnekliği tam bir birimdir (|ε| = 1.00). Fiyat değişim oranı ile miktar değişim oranı birbirini tam oransal olarak dengeler."

            if tax > 0:
                vergi_yorumu = f"Piyasaya uygulanan <b>{tax} birimlik spesifik vergi (veya negatif maliyet şoku)</b> arz eğrisini yukarı kaydırmıştır. İktisadi insidans prensibine göre; talep ne kadar inelastikse, vergi yükünün (price burden) o denli büyük bir kısmı doğrudan maalesef tüketiciye yansıtılacaktır."
            elif tax < 0:
                vergi_yorumu = f"Piyasaya sağlanan <b>{abs(tax)} birimlik sübvansiyon</b> arz maliyetlerini minimalize ederek işlem hacminde canlanma yaratmaktadır. Verimlilik kazanımları neticesinde tüketici rantında bariz bir artış bekliyoruz."
            else:
                vergi_yorumu = "Mevcut durumda piyasada herhangi bir dolaylı vergi veya harç baskısı (takoz) bulunmamakta, serbest piyasa mekanizması ve fiyatlama rasyoneli hiçbir dış şoka maruz kalmadan çalışmaktadır."

            rapor = f"""
            <div style='font-size: 0.95rem; line-height: 1.6; color: var(--text-color); padding: 5px 15px;'>
            <p style="margin-bottom: 10px;"><b>1. Genel Piyasa Durumu:</b><br>Piyasa, <i>P_d = {demand_formula}</i> talep ve <i>P_s = {supply_formula}</i> arz fonksiyonları altında Market Clearing (Piyasa Temizlenme) durumuna ulaşmıştır. Denge fiyatı (P*) <b>{eq_p:.2f}</b> düzeyinde teşekkül etmiş olup, bu fiyattan işlem gören optimum miktar (Q*) <b>{eq_q:.2f}</b> birim olarak gerçekleşmiştir.</p>
            <p style="margin-bottom: 10px;"><b>2. Tüketici Reaksiyonu (Esneklik):</b><br>{esneklik_yorumu}</p>
            <p style="margin-bottom: 15px;"><b>3. Dışsal Şok ve Vergi İnsidansı:</b><br>{vergi_yorumu}</p>
            <p style="padding: 12px; border-left: 4px solid #2563EB; background: rgba(37,99,235,0.05); border-radius: 4px;"><b> Akademik Sonuç Değerlendirmesi:</b><br>Mevcut şartlar altında piyasa kendi iç dinamikleriyle tahsis etkinliğini (Allocative Efficiency) kısmen sağlamıştır. Ancak ilerleyen dönemde oluşabilecek teknolojik dışsallıkların veya vergi rejimi değişikliklerinin, mevcut refah kayıplarını (Deadweight Loss - Harberger Üçgeni) minimize edecek şekilde regüle edilmesi, toplam sosyal refahın sürdürülebilirliği adına hayati bir kamusal önceliktir.</p>
            </div>
            """
            st.markdown(rapor, unsafe_allow_html=True)
        else:
            st.warning(" Profesör uyarıyor: Analiz yapabilmem için öncelikle piyasanın dengeye gelmiş olması (arz ve talebin kesişmesi) gerekir. Lütfen grafikteki fonksiyonları veya x-y limitlerini kontrol ediniz.")
