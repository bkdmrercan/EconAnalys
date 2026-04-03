import numpy as np
import plotly.graph_objects as go
import streamlit as st

from econanalys.ui import metric_html, slice_desc

def init_macro():
    defaults = {
        'm_Co': 0.0, 'm_I': 0.0, 'm_G': 0.0, 'm_X': 0.0, 'm_Mo': 0.0, 
        'm_Yf': 0.0, 'm_c': 0.0, 'm_s': 0.0, 'm_t': 0.0, 'm_m': 0.0,
        'm_Rev': 0.0, 'm_Exp': 0.0
    }
    for k, v in defaults.items():
        if k not in st.session_state: 
            st.session_state[k] = v

init_macro()

def update_c(): 
    st.session_state.m_s = max(0.0, round(float(1.0 - st.session_state.m_c), 4))
def update_s(): 
    st.session_state.m_c = max(0.0, round(float(1.0 - st.session_state.m_s), 4))

def set_scenario(co, c, i, g, t, x, mo, m):
    st.session_state['m_Co'] = float(co)
    st.session_state['m_c'] = float(c)
    st.session_state['m_I'] = float(i)
    st.session_state['m_G'] = float(g)
    st.session_state['m_t'] = float(t)
    st.session_state['m_X'] = float(x)
    st.session_state['m_Mo'] = float(mo)
    st.session_state['m_m'] = float(m)
    st.session_state['m_s'] = round(float(1.0 - st.session_state['m_c']), 4)

def param_input(label, key):
    st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; opacity: 0.8; margin-top: 8px; margin-bottom: 2px;'>{label}</div>", unsafe_allow_html=True)
    st.number_input("dummy_auto", min_value=0.0, key=key, format="%.2f", label_visibility="collapsed")


def render(tv_layout, dyn_template, colors):
    color_blue = colors["blue"]
    color_orange = colors["orange"]
    color_green = colors["green"]
    color_red = colors["red"]
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='tv-title'> MAKRO KONSOL</div>", unsafe_allow_html=True)
        c0, c1, c2, c3, c4 = st.columns(5)
        with c0:
            st.markdown("<div style='background-color: var(--background-color); padding: 6px; border-radius: 4px; border-left: 3px solid var(--neon-accent); margin-bottom: 5px; font-weight: 700; font-size: 0.85rem;'>Otonom [1]</div>", unsafe_allow_html=True)
            param_input("Otonom Tüketim (C0) [TL]", "m_Co")
            param_input("Otonom Yatırım (I0) [TL]", "m_I")
        with c1:
            st.markdown("<div style='background-color: var(--background-color); padding: 6px; border-radius: 4px; border-left: 3px solid var(--neon-accent); margin-bottom: 5px; font-weight: 700; font-size: 0.85rem;'>Otonom [2]</div>", unsafe_allow_html=True)
            param_input("Devlet Harcaması (G) [TL]", "m_G")
            param_input("İhracat (X) [TL]", "m_X")
        with c2:
            st.markdown("<div style='background-color: var(--background-color); padding: 6px; border-radius: 4px; border-left: 3px solid var(--neon-accent); margin-bottom: 5px; font-weight: 700; font-size: 0.85rem;'>Kapasite & Dış</div>", unsafe_allow_html=True)
            param_input("Otonom İthalat (M0) [TL]", "m_Mo")
            param_input("Tam İstihdam (Yf) [TL]", "m_Yf")
        with c3:
            st.markdown("<div style='background-color: rgba(242, 54, 69, 0.05); padding: 6px; border-radius: 4px; border-left: 3px solid #F23645; margin-bottom: 5px; font-weight: 700; font-size: 0.85rem;'>Eğilim (c+s=1)</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; opacity: 0.8; margin-top: 8px; margin-bottom: 2px;'>Tüketim Eğilimi (c) [% / Oran]</div>", unsafe_allow_html=True)
            st.number_input("dummy_c", min_value=0.0, max_value=1.0, key="m_c", format="%.2f", on_change=update_c, label_visibility="collapsed")
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; opacity: 0.8; margin-top: 8px; margin-bottom: 2px;'>Tasarruf Eğilimi (s) [% / Oran]</div>", unsafe_allow_html=True)
            st.number_input("dummy_s", min_value=0.0, max_value=1.0, key="m_s", format="%.2f", on_change=update_s, label_visibility="collapsed")
        with c4:
            st.markdown("<div style='background-color: rgba(8, 153, 129, 0.05); padding: 6px; border-radius: 4px; border-left: 3px solid #089981; margin-bottom: 5px; font-weight: 700; font-size: 0.85rem;'>Bağımsız Sızıntı</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; opacity: 0.8; margin-top: 8px; margin-bottom: 2px;'>Gelir Vergisi (t) [% / Oran]</div>", unsafe_allow_html=True)
            st.number_input("dummy_t", min_value=0.0, max_value=1.0, key="m_t", format="%.2f", label_visibility="collapsed")
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; opacity: 0.8; margin-top: 8px; margin-bottom: 2px;'>İthalat Eğilimi (m) [% / Oran]</div>", unsafe_allow_html=True)
            st.number_input("dummy_m", min_value=0.0, max_value=1.0, key="m_m", format="%.2f", label_visibility="collapsed")

        # Yeni Bütçe Verileri Bölümü
        st.markdown("<div style='background-color: rgba(37, 99, 235, 0.05); padding: 10px; border-radius: 4px; border-left: 3px solid var(--neon-accent); margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 700; font-size: 0.85rem; margin-bottom: 10px;'> BÜTÇE AYARLARI (MANUEL)</div>", unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1:
            param_input("Bütçe Gelirleri [TL]", "m_Rev")
        with bc2:
            param_input("Bütçe Giderleri [TL]", "m_Exp")
        st.markdown("</div>", unsafe_allow_html=True)

        C_o, I_o, G_k, X_k, M_o, Yf = st.session_state.m_Co, st.session_state.m_I, st.session_state.m_G, st.session_state.m_X, st.session_state.m_Mo, st.session_state.m_Yf
        c_k, t_rate, m_k = st.session_state.m_c, st.session_state.m_t, st.session_state.m_m

        total_autonomous = C_o + I_o + G_k + X_k + M_o
        if total_autonomous > 10 * Yf and Yf > 0:
            st.warning("Parametre ölçekleri uyumsuz! Otonom Harcamalarınızın toplamı potansiyel üretimin (Yf) çok üzerinde.")

        st.markdown("<hr style='margin: 15px 0; border: none; border-bottom: 1px solid var(--border-color);'>", unsafe_allow_html=True)
        c_snap1, c_snap2, c_snap3, c_snap4 = st.columns(4)
        if c_snap2.button(" Sabitle", use_container_width=True): 
            st.session_state['mac_snap'] = {'Co': C_o, 'c': c_k, 't': t_rate, 'I': I_o, 'G': G_k, 'X': X_k, 'Mo': M_o, 'm': m_k, 'Yf': Yf, 'Rev': st.session_state.m_Rev, 'Exp': st.session_state.m_Exp}
        if c_snap3.button(" Temizle", use_container_width=True): 
            # Tüm makro değerlerini sıfırla
            for k in ['m_Co', 'm_I', 'm_G', 'm_X', 'm_Mo', 'm_Yf', 'm_c', 'm_s', 'm_t', 'm_m', 'm_Rev', 'm_Exp']:
                st.session_state[k] = 0.0
            if 'mac_snap' in st.session_state: 
                del st.session_state['mac_snap']
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    Y_star_mac, NX, Budget, gap_percent, multiplier = 0.0, 0.0, 0.0, 0.0, 0.0
    calc_success = False
    try:
        den = 1.0 - c_k * (1.0 - t_rate) + m_k
        if den <= 0.0001: raise ZeroDivisionError
        multiplier = 1 / den
        Y_star_mac = multiplier * (C_o + I_o + G_k + X_k - M_o)
        NX = X_k - (M_o + m_k * Y_star_mac)

        # Bütçe Dengesi
        Budget = st.session_state.m_Rev - st.session_state.m_Exp

        gap_percent = ((Y_star_mac - Yf) / Yf) * 100 if Yf > 0 else 0
        if gap_percent > 999.0: gap_percent = 999.0
        calc_success = True
    except Exception as e: 
        pass

    with st.container(border=True):
        st.markdown("<div class='tv-title'> KEYNESYEN GELİR-HARCAMA DENGESİ</div>", unsafe_allow_html=True)
        if not calc_success or Y_star_mac < 0:
            st.warning("Veri bekleniyor... (Hata durumu mevcut, katsayıları kontrol edin.)")
        else:
            y_vals = np.linspace(0, max(2500.0, Yf * 1.5, Y_star_mac * 1.5), 200)
            AD_vals = C_o + c_k * (1 - t_rate) * y_vals + I_o + G_k + X_k - (M_o + m_k * y_vals)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=y_vals, y=AD_vals, name='Yeni Talep (AD)', line={"color": color_blue, "width": 3}))
            fig.add_trace(go.Scatter(x=y_vals, y=y_vals, name='Y=AD (45°)', line={"color": color_orange, "width": 4, "dash": 'solid'}))
            fig.add_trace(go.Scatter(x=[Y_star_mac], y=[Y_star_mac], mode='markers', name='Yeni Denge (Y*)', marker={"color": color_blue, "size": 10}))

            if 'mac_snap' in st.session_state:
                s_s = st.session_state['mac_snap']
                try:
                    den_s = 1 - s_s['c'] * (1 - s_s['t']) + s_s['m']
                    if den_s > 0.0001:
                        mult_s = 1 / den_s
                        Y_star_s = mult_s * (s_s['Co'] + s_s['I'] + s_s['G'] + s_s['X'] - s_s['Mo'])
                        AD_s = s_s['Co'] + s_s['c'] * (1 - s_s['t']) * y_vals + s_s['I'] + s_s['G'] + s_s['X'] - (s_s['Mo'] + s_s['m'] * y_vals)
                        fig.add_trace(go.Scatter(x=y_vals, y=AD_s, name='Eski Talep (AD0)', line={"color": '#9E9E9E', "width": 2.5, "dash": 'dot'}))
                        fig.add_trace(go.Scatter(x=[Y_star_s], y=[Y_star_s], mode='markers', name='Eski Denge (Y0)', marker={"color": '#9E9E9E', "size": 8}))
                        fig.add_shape(type="line", x0=Y_star_s, y0=0, x1=Y_star_s, y1=Y_star_s, line={"color": "#9E9E9E", "width": 1, "dash": "dot"}, opacity=0.5)
                except: 
                    pass

            fig.add_shape(type="line", x0=Yf, y0=0, x1=Yf, y1=max(AD_vals)*1.1, line={"color": color_red, "width": 2, "dash": "dash"}, opacity=0.7)
            fig.add_annotation(x=Yf, y=max(AD_vals)*1.05, text="Tam İstihdam (Yf)", showarrow=False, font={"color": color_red, "size": 13, "family": "'Trebuchet MS', sans-serif"})
            fig.add_shape(type="line", x0=0, y0=Y_star_mac, x1=Y_star_mac, y1=Y_star_mac, line={"color": color_blue, "width": 1, "dash": "dot"}, opacity=0.4)
            fig.add_shape(type="line", x0=Y_star_mac, y0=0, x1=Y_star_mac, y1=Y_star_mac, line={"color": color_blue, "width": 1, "dash": "dot"}, opacity=0.4)
            fig.update_layout(**tv_layout)
            fig.update_layout(height=800)
            fig.update_xaxes(title="Milli Gelir (Y)")
            fig.update_yaxes(title="Toplam Harcamalar (AD)")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; margin-top: 25px; margin-bottom: 10px; color: var(--text-color); text-align: center;'> Makro Senaryolar (V4.0 Motoru) & Grafik Etkileri</div>", unsafe_allow_html=True)
    sb1, sb2, sb3 = st.columns(3)
    with sb1:
        st.button(" Pandemi Şoku (Kapanma)", on_click=set_scenario, args=(80, 0.60, 50, 400, 0.20, 50, 30, 0.20), use_container_width=True)
        st.markdown("<div style='font-size: 0.75rem; background: rgba(242, 54, 69, 0.05); padding: 10px; border-radius: 4px; border-left: 3px solid #F23645; margin-top: -10px; min-height: 85px;'><b>Etki Mekanizması:</b> Tüketim (c) ve yatırımlar (I0) çöker. Devlet (G) devasa teşvik paketleri açar.<br><br><b> Grafiğe Yansıması:</b> Tüketim sızıntısı arttığı için AD eğrisi çok yassılaşır. Sadece aşırı G sayesinde eğri yukarı itilir ve iflas önlenir.</div>", unsafe_allow_html=True)
    with sb2:
        st.button(" Altın Çağ (Sıcak Para)", on_click=set_scenario, args=(150, 0.65, 200, 150, 0.15, 200, 80, 0.20), use_container_width=True)
        st.markdown("<div style='font-size: 0.75rem; background: rgba(8, 153, 129, 0.05); padding: 10px; border-radius: 4px; border-left: 3px solid #089981; margin-top: -10px; min-height: 85px;'><b>Etki Mekanizması:</b> Düşük faizle yatırımlar (I0) zirve yapar. Vergiler (t) düşüktür, tüketim (C0) coşar.<br><br><b> Grafiğe Yansıması:</b> Çarpan uçuşa geçer. AD eğrisi büyük bir eğimle dikleşir ve sıçrar. Nokta, kırmızı Yf çizgisini delip geçerek enflasyon yaratır.</div>", unsafe_allow_html=True)
    with sb3:
        st.button(" Sıkı Para (Kemer Sıkma)", on_click=set_scenario, args=(90, 0.50, 80, 100, 0.35, 100, 40, 0.15), use_container_width=True)
        st.markdown("<div style='font-size: 0.75rem; background: rgba(41, 98, 255, 0.05); padding: 10px; border-radius: 4px; border-left: 3px solid #2962FF; margin-top: -10px; min-height: 85px;'><b>Etki Mekanizması:</b> Krediler pahalandığı için yatırımlar (I0) vurulur. Yüksek vergi (t) yüzünden tasarruflar zıplar.<br><br><b> Grafiğe Yansıması:</b> Parasal sızıntılar ekstrem boyutlardadır. Eğri ciddi anlamda düzleşir ver aşağı çöker. Deflasyonist aralığa sert çakılış.</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='tv-title'> GSYH BİLEŞEN DAĞILIMI VE HACİM ANALİZİ</div>", unsafe_allow_html=True)
        if calc_success and Y_star_mac > 0:
            c_pie, c_desc = st.columns([6, 4])
            C_st = C_o + c_k * (1 - t_rate) * Y_star_mac
            M_total = M_o + m_k * Y_star_mac
            pie_vals = [C_st, I_o, G_k, X_k, M_total]
            pie_labels = ['Tüketim (C)', 'Yatırım (I)', 'Kamu (G)', 'İhracat (X)', 'İthalat (-)']
            pie_colors = [color_blue, '#00B0FF', color_orange, color_green, color_red]
            with c_pie:
                fig_pie = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_vals, hole=.55, textinfo='label+percent', textfont_size=12, marker={"colors": pie_colors, "line": {"color": 'rgba(0,0,0,0)', "width": 1.5}})])
                fig_pie.update_layout(template=dyn_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={"t": 5,"b": 5,"l": 5,"r": 5}, height=500, showlegend=False)
                fig_pie.add_annotation(text=f"<b style='font-size:1.6rem;'>{Y_star_mac:,.2f}</b><br><span style='font-size:1rem;opacity:0.6;'>Toplam GSYH</span>", x=0.5, y=0.5, showarrow=False, font={"family": "'Trebuchet MS', sans-serif"})
                st.plotly_chart(fig_pie, use_container_width=True)
            with c_desc:
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                t_p = sum(pie_vals) if sum(pie_vals) > 0 else 1
                def fm(t, v): return f"{t}: <b>{v:,.2f} TL</b> ([%{(v/t_p)*100:.1f}])"
                st.markdown(slice_desc(color_blue, fm("Tüketim (C)", C_st), "Hanehalkı harcamaları. Büyümenin lokomotifidir."), unsafe_allow_html=True)
                st.markdown(slice_desc('#00B0FF', fm("Yatırım (I)", I_o), "Üretim kapasitesini gösterir. Reel faize duyarlıdır."), unsafe_allow_html=True)
                st.markdown(slice_desc(color_orange, fm("Kamu (G)", G_k), "Devletin makroekonomik müdahalesidir. Deflasyonist açığı azaltır."), unsafe_allow_html=True)
                st.markdown(slice_desc(color_green, fm("İhracat (X)", X_k), "Dış dünyaya ülkenin satışlarıdır. Ülkeye net döviz girişi sağlar."), unsafe_allow_html=True)
                st.markdown(slice_desc(color_red, fm("İthalat (-)", M_total), "Gelir sızıntısıdır. Cari işlemler dengesini bozar ve GSYH'yi küçültür."), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='tv-title'> G ve t DUYARLILIK MATRİSİ (Y* HEATMAP)</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 15px; text-align: center; line-height: 1.5;'>Bu matris, farklı <b>Devlet Harcaması (G)</b> ve <b>Vergi Oranı (t)</b> kombinasyonlarında Milli Gelir'in (Y*) nasıl değiştiğini gösterir.<br>Koyu mavi bölgeler yüksek büyümeyi, kırmızı bölgeler ise daralmayı temsil eder. Maliye politikası tasarımı için hayati bir pusuladır.</div>", unsafe_allow_html=True)
        if calc_success:
            g_range = np.linspace(50, 500, 30)
            t_range = np.linspace(0.01, 0.40, 30)
            z_vals = np.zeros((len(t_range), len(g_range)))
            for i, tv in enumerate(t_range):
                for j, gv in enumerate(g_range): 
                    try:
                        den_h = 1 - c_k * (1 - tv) + m_k
                        z_vals[i, j] = (C_o + I_o + gv + X_k - M_o) / den_h if den_h > 0.0001 else np.nan
                    except: 
                        z_vals[i, j] = np.nan
            fig_heat = go.Figure(data=go.Heatmap(z=z_vals, x=g_range, y=t_range, colorscale='RdBu', hoverinfo='z', colorbar=dict(title="Denge (Y*)")))
            fig_heat.update_layout(**tv_layout)
            fig_heat.update_layout(height=520)
            fig_heat.update_xaxes(title="Devlet Harcaması (G)")
            fig_heat.update_yaxes(title="Gelir Vergisi Oranı (t)")
            st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='tv-title'> EKONOMİK GÖSTERGELER & POLİTİKA KARTLARI</div>", unsafe_allow_html=True)
        if not calc_success or Y_star_mac < 0:
            st.warning("Veri bekleniyor... Kararlılık kuralını test ediniz.")
        else:
            if Y_star_mac < Yf:
                st.markdown(f"<div class='tv-note-box'><strong> Deflasyonist Açık (Resesyon)</strong><br>Ekonomi istihdamın altında. Genişleyici maliye (Kamu harcamaları artırılmalı veya vergiler düşürülmeli) önerilir. Açık: <b>%-{gap_percent:,.2f}</b></div>", unsafe_allow_html=True)
            elif Y_star_mac > Yf:
                if gap_percent > 100:
                    st.markdown(f"<div class='tv-note-box' style='border-left-color: #8B0000; background: rgba(242, 54, 69, 0.2); color: #F23645;'><strong> Hiperenflasyon Riski! (Aşırı Isınma)</strong><br>Ekonomi ideal kapasitesini çok aştı. Acil sıkılaştırıcı politikalar (Vergi artışı) alınmalıdır. Baskı: <b>+{gap_percent:,.2f}%</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='tv-note-box' style='border-left-color: #FF9800; background: rgba(255, 152, 0, 0.1);'><strong> Enflasyonist Uçurum (Aşırı Isınma)</strong><br>Ekonomi ideal kapasitesini aştı. Sıkılaştırıcı politikalar (Vergi artışı) alınmalıdır. Baskı: <b>+{gap_percent:,.2f}%</b></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='tv-note-box-green'><strong> Tam İstihdam Dengesi</strong><br>Ekonomi ideal seviyede (Y* = Yf). Değişikliğe gerek yok.</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    mi1, mi3, mi4 = st.columns(3)
    with mi1:
        st.markdown(metric_html("DENGE GELİRİ (Y*)", f"{Y_star_mac:,.2f}"), unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; font-weight: 600; text-align: center; margin-top: -5px;'>Akıllı İyileştirme Önerisi:</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.72rem; opacity: 0.8; text-align: center; margin-top: 2px;'>Y*'ı artırmak ve tam istihdama yaklaşmak için: Kamu harcamalarını (G) artırmayı, vergileri (t) düşürmeyi veya ihracat (X) teşviklerini değerlendirin.</div>", unsafe_allow_html=True)
    with mi3:
        st.markdown(metric_html("BÜTÇE DENGESİ", f"{Budget:,.2f}", color_green if Budget >= 0 else color_red), unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; font-weight: 600; text-align: center; margin-top: -5px;'>Akıllı İyileştirme Önerisi:</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.72rem; opacity: 0.8; text-align: center; margin-top: 2px;'>Mali disiplini sağlamak için: Vergi oranını (t) artırarak gelir yaratın veya kamu harcamalarını (G) stratejik olarak daraltın.</div>", unsafe_allow_html=True)
    with mi4:
        st.markdown(metric_html("CARİ DENGE (NX)", f"{NX:,.2f}", color_green if NX >= 0 else color_red), unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.75rem; font-weight: 600; text-align: center; margin-top: -5px;'>Akıllı İyileştirme Önerisi:</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.72rem; opacity: 0.8; text-align: center; margin-top: 2px;'>Dış ticaret açığını kapatmak için: İhracat (X) rekabetçiliğini artırın veya ithalat (m) bağımlılığını azaltacak politikalar izleyin.</div>", unsafe_allow_html=True)
