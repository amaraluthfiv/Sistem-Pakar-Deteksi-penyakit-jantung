import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# =========================================
# SISTEM PAKAR SERANGAN JANTUNG - FORWARD CHAINING
# =========================================

# Set page config
st.set_page_config(
    page_title="Sistem Pakar Risiko Serangan Jantung",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih baik
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #51cf66, #40c057);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .rule-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #28a745;
    }
    
    .rule-card.failed {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    
    .info-box {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# FUNGSI KONDISI RULES (FUNGSI PEMERIKSAAN)
# =========================================
def cek_usia_berisiko(f):
    """
    Fungsi untuk mengecek apakah usia pasien berisiko
    Parameter f: dictionary berisi data pasien
    Return: True jika Age > 50, False jika tidak
    """
    return f['Age'] > 50

def cek_sistolik_tinggi(f):
    """
    Fungsi untuk mengecek apakah tekanan darah sistolik tinggi
    Return: True jika Systolic blood pressure > 140, False jika tidak
    """
    return f['Systolic blood pressure'] > 140

def cek_diastolik_tinggi(f):
    """
    Fungsi untuk mengecek apakah tekanan darah diastolik tinggi
    Return: True jika Diastolic blood pressure > 90, False jika tidak
    """
    return f['Diastolic blood pressure'] > 90

def cek_gula_tinggi(f):
    """
    Fungsi untuk mengecek apakah kadar gula darah tinggi
    Return: True jika Blood sugar > 126, False jika tidak
    """
    return f['Blood sugar'] > 126

def cek_ckmb_tinggi(f):
    """
    Fungsi untuk mengecek apakah kadar CK-MB tinggi
    Return: True jika CK-MB > 5, False jika tidak
    """
    return f['CK-MB'] > 5

def cek_troponin_tinggi(f):
    """
    Fungsi untuk mengecek apakah kadar troponin tinggi
    Return: True jika Troponin > 0.04, False jika tidak
    """
    return f['Troponin'] > 0.04

def cek_risiko_tinggi(f):
    """
    Fungsi untuk mengecek apakah semua faktor risiko terpenuhi
    Parameter f: dictionary dengan key 'facts' berisi set fakta yang sudah ditemukan
    Return: True jika semua fakta risiko ada, False jika tidak
    """
    return all([
        'usia_berisiko' in f['facts'],
        'sistolik_tinggi' in f['facts'],
        'diastolik_tinggi' in f['facts'],
        'gula_tinggi' in f['facts'],
        'ckmb_tinggi' in f['facts'],
        'troponin_tinggi' in f['facts']
    ])

# =========================================
# KNOWLEDGE BASE (BASIS PENGETAHUAN - ATURAN IF-THEN)
# =========================================

# RULE 1: Jika umur pasien lebih dari 50 tahun, maka risiko meningkat
def rule_1_usia_berisiko(f):
    if f['Age'] > 50:
        return 1
    return 0

# RULE 2: Jika tekanan darah sistolik lebih dari 140 mmHg, maka tekanan darah tinggi
def rule_2_sistolik_tinggi(f):
    if f['Systolic blood pressure'] > 140:
        return 1
    return 0

# RULE 3: Jika tekanan darah diastolik lebih dari 90 mmHg, maka tekanan darah tinggi
def rule_3_diastolik_tinggi(f):
    if f['Diastolic blood pressure'] > 90:
        return 1
    return 0

# RULE 4: Jika kadar gula darah lebih dari 126 mg/dL, maka gula darah tinggi
def rule_4_gula_tinggi(f):
    if f['Blood sugar'] > 126:
        return 1
    return 0

# RULE 5: Jika kadar CK-MB lebih dari 5 ng/mL, maka CK-MB tinggi
def rule_5_ckmb_tinggi(f):
    if f['CK-MB'] > 5:
        return 1
    return 0

# RULE 6: Jika kadar troponin lebih dari 0.04 ng/mL, maka troponin tinggi
def rule_6_troponin_tinggi(f):
    if f['Troponin'] > 0.04:
        return 1
    return 0

# RULE 7: Jika semua faktor risiko di atas terpenuhi, maka risiko serangan jantung tinggi
def rule_7_risiko_tinggi(f):
    if all([
        f.get('rule_1', 0) == 1,
        f.get('rule_2', 0) == 1,
        f.get('rule_3', 0) == 1,
        f.get('rule_4', 0) == 1,
        f.get('rule_5', 0) == 1,
        f.get('rule_6', 0) == 1
    ]):
        return 1
    return 0

# DAFTAR ATURAN IF-THEN
RULES = [
    {
        'id': 'rule_1',
        'name': 'Aturan Usia Berisiko',
        'if_then': 'IF umur pasien > 50 tahun THEN risiko meningkat',
        'function': rule_1_usia_berisiko,
        'description': 'Usia di atas 50 tahun meningkatkan risiko serangan jantung',
        'threshold': '> 50 tahun'
    },
    {
        'id': 'rule_2',
        'name': 'Aturan Tekanan Sistolik Tinggi',
        'if_then': 'IF tekanan darah sistolik > 140 mmHg THEN tekanan darah tinggi',
        'function': rule_2_sistolik_tinggi,
        'description': 'Tekanan darah sistolik tinggi dapat merusak pembuluh darah',
        'threshold': '> 140 mmHg'
    },
    {
        'id': 'rule_3',
        'name': 'Aturan Tekanan Diastolik Tinggi',
        'if_then': 'IF tekanan darah diastolik > 90 mmHg THEN tekanan darah tinggi',
        'function': rule_3_diastolik_tinggi,
        'description': 'Tekanan darah diastolik tinggi menunjukkan hipertensi',
        'threshold': '> 90 mmHg'
    },
    {
        'id': 'rule_4',
        'name': 'Aturan Gula Darah Tinggi',
        'if_then': 'IF kadar gula darah > 126 mg/dL THEN gula darah tinggi',
        'function': rule_4_gula_tinggi,
        'description': 'Diabetes meningkatkan risiko penyakit jantung koroner',
        'threshold': '> 126 mg/dL'
    },
    {
        'id': 'rule_5',
        'name': 'Aturan CK-MB Tinggi',
        'if_then': 'IF kadar CK-MB > 5 ng/mL THEN CK-MB tinggi',
        'function': rule_5_ckmb_tinggi,
        'description': 'CK-MB tinggi menunjukkan kerusakan otot jantung',
        'threshold': '> 5 ng/mL'
    },
    {
        'id': 'rule_6',
        'name': 'Aturan Troponin Tinggi',
        'if_then': 'IF kadar troponin > 0.04 ng/mL THEN troponin tinggi',
        'function': rule_6_troponin_tinggi,
        'description': 'Troponin tinggi adalah indikator kuat serangan jantung',
        'threshold': '> 0.04 ng/mL'
    },
    {
        'id': 'rule_7',
        'name': 'Aturan Risiko Tinggi',
        'if_then': 'IF semua faktor risiko di atas terpenuhi THEN risiko serangan jantung tinggi',
        'function': rule_7_risiko_tinggi,
        'description': 'Kombinasi semua faktor risiko menunjukkan risiko sangat tinggi',
        'threshold': 'Semua faktor'
    }
]

# =========================================
# MESIN INFERENSI (FORWARD CHAINING ENGINE)
# =========================================
def forward_chaining_engine(fakta_awal):
    facts = {k: v for k, v in fakta_awal.items()}
    log = []
    
    # Jalankan semua aturan dan simpan hasilnya
    for rule in RULES:
        result = rule['function'](facts)
        facts[rule['id']] = result
        if result == 1:
            log.append(f"✅ {rule['name']}: {rule['if_then']} → 1 (Ya)")
        else:
            log.append(f"❌ {rule['name']}: {rule['if_then']} → 0 (Tidak)")
    
    return facts, log

# =========================================
# FUNGSI HELPER UNTUK VISUALISASI
# =========================================
def create_risk_meter(risk_score):
    """Membuat gauge chart untuk menunjukkan tingkat risiko"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Tingkat Risiko"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_factor_chart(results):
    """Membuat bar chart untuk faktor risiko"""
    factors = []
    values = []
    colors = []
    
    for rule in RULES[:-1]:  # Exclude the final rule
        factors.append(rule['name'].replace('Aturan ', ''))
        values.append(results[rule['id']])
        colors.append('#ff6b6b' if results[rule['id']] == 1 else '#51cf66')
    
    fig = go.Figure(data=[
        go.Bar(
            x=factors,
            y=values,
            marker_color=colors,
            text=['Berisiko' if v == 1 else 'Normal' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Analisis Faktor Risiko",
        xaxis_title="Faktor Risiko",
        yaxis_title="Status",
        yaxis=dict(range=[0, 1.2], tickvals=[0, 1], ticktext=['Normal', 'Berisiko']),
        height=400
    )
    
    return fig

# =========================================
# INTERFACE STREAMLIT (ANTARMUKA PENGGUNA)
# =========================================

# Header dengan styling
st.markdown("""
<div class="main-header">
    <h1>🩺 Sistem Pakar Risiko Serangan Jantung</h1>
    <p>Analisis Cerdas Berbasis Forward Chaining untuk Deteksi Dini Risiko Serangan Jantung</p>
</div>
""", unsafe_allow_html=True)

# Sidebar dengan informasi sistem
with st.sidebar:
    st.markdown("## 🔍 Tentang Sistem")
    st.markdown("""
    Sistem ini menggunakan **Forward Chaining** untuk menganalisis risiko serangan jantung berdasarkan 6 parameter medis utama:
    
    - **Usia**: Faktor risiko demografis
    - **Tekanan Darah**: Sistolik & Diastolik
    - **Gula Darah**: Indikator diabetes
    - **CK-MB**: Enzim kerusakan jantung
    - **Troponin**: Protein penanda serangan jantung
    """)
    
    st.markdown("## 📊 Nilai Normal")
    st.markdown("""
    - **Usia**: < 50 tahun
    - **Sistolik**: < 140 mmHg
    - **Diastolik**: < 90 mmHg
    - **Gula Darah**: < 126 mg/dL
    - **CK-MB**: < 5 ng/mL
    - **Troponin**: < 0.04 ng/mL
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Form input data pasien dengan styling yang lebih baik
    st.markdown("## 📝 Input Data Pasien")
    
    with st.form("form_pasien"):
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            age = st.number_input(
                "👤 Usia (tahun)", 
                min_value=1, max_value=120, step=1, value=45,
                help="Usia pasien dalam tahun"
            )
            
            systolic = st.number_input(
                "📈 Tekanan Darah Sistolik (mmHg)", 
                min_value=75, max_value=250, step=1, value=120,
                help="Tekanan darah saat jantung berkontraksi"
            )
            
            blood_sugar = st.number_input(
                "🍯 Kadar Gula Darah (mg/dL)", 
                min_value=50.0, max_value=600.0, value=100.0,
                help="Kadar glukosa dalam darah puasa"
            )
        
        with input_col2:
            diastolic = st.number_input(
                "📉 Tekanan Darah Diastolik (mmHg)", 
                min_value=40, max_value=150, step=1, value=80,
                help="Tekanan darah saat jantung relaksasi"
            )
            
            ckmb = st.number_input(
                "🔬 CK-MB (ng/mL)", 
                min_value=0.0, max_value=300.0, step=0.01, value=2.0, format="%.2f",
                help="Enzim yang dilepaskan saat kerusakan otot jantung"
            )
            
            troponin = st.number_input(
                "🧪 Troponin (ng/mL)", 
                min_value=0.0, max_value=10.0, step=0.01, value=0.02, format="%.2f",
                help="Protein penanda kerusakan otot jantung"
            )
        
        submit = st.form_submit_button("🔍 Analisis Risiko", use_container_width=True)

with col2:
    # Quick info box
    st.markdown("""
    <div class="info-box">
        <h4>💡 Tips Penggunaan</h4>
        <p>Masukkan data pasien dengan akurat untuk mendapatkan analisis risiko yang tepat. Sistem akan menganalisis setiap parameter secara otomatis.</p>
    </div>
    """, unsafe_allow_html=True)

# Proses inferensi jika form disubmit
if submit:
    # Siapkan fakta awal dari input user
    fakta_awal = {
        'Age': age,
        'Systolic blood pressure': systolic,
        'Diastolic blood pressure': diastolic,
        'Blood sugar': blood_sugar,
        'CK-MB': ckmb,
        'Troponin': troponin
    }
    
    # Jalankan forward chaining engine
    hasil, log = forward_chaining_engine(fakta_awal)
    
    # Hitung risk score
    risk_factors = sum([hasil[f'rule_{i}'] for i in range(1, 7)])
    risk_score = (risk_factors / 6) * 100
    
    # Tampilkan hasil dalam layout yang menarik
    st.markdown("---")
    st.markdown("## 📊 Hasil Analisis")
    
    # Kesimpulan utama
    result_col1, result_col2 = st.columns([2, 1])
    
    with result_col1:
        if hasil['rule_7'] == 1:
            st.markdown("""
            <div class="risk-high">
                <h2>🚨 RISIKO TINGGI</h2>
                <p style="font-size: 1.2rem;">Pasien memiliki risiko tinggi mengalami serangan jantung</p>
                <p><strong>Rekomendasi:</strong> Segera konsultasi dengan dokter spesialis jantung</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="risk-low">
                <h2>✅ RISIKO RENDAH</h2>
                <p style="font-size: 1.2rem;">Pasien memiliki risiko rendah terhadap serangan jantung</p>
                <p><strong>Rekomendasi:</strong> Tetap jaga pola hidup sehat dan kontrol berkala</p>
            </div>
            """, unsafe_allow_html=True)
    
    with result_col2:
        # Risk meter
        fig_meter = create_risk_meter(risk_score)
        st.plotly_chart(fig_meter, use_container_width=True)
    
    # Visualisasi faktor risiko
    st.markdown("### 📈 Visualisasi Faktor Risiko")
    fig_factors = create_factor_chart(hasil)
    st.plotly_chart(fig_factors, use_container_width=True)
    
    # Detail analisis setiap aturan
    st.markdown("### 🔍 Detail Analisis Aturan")
    
    for rule in RULES:
        result = hasil[rule['id']]
        if result == 1:
            st.markdown(f"""
            <div class="rule-card">
                <h4>✅ {rule['name']}</h4>
                <p><strong>Aturan:</strong> {rule['if_then']}</p>
                <p><strong>Hasil:</strong> Terpenuhi (1)</p>
                <p><strong>Keterangan:</strong> {rule['description']}</p>
                <p><strong>Ambang Batas:</strong> {rule['threshold']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="rule-card failed">
                <h4>❌ {rule['name']}</h4>
                <p><strong>Aturan:</strong> {rule['if_then']}</p>
                <p><strong>Hasil:</strong> Tidak Terpenuhi (0)</p>
                <p><strong>Keterangan:</strong> {rule['description']}</p>
                <p><strong>Ambang Batas:</strong> {rule['threshold']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Ringkasan statistik
    st.markdown("### 📊 Ringkasan Statistik")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Faktor Risiko Aktif", f"{risk_factors}/6", f"{risk_factors-3}")
    
    with stat_col2:
        st.metric("Persentase Risiko", f"{risk_score:.1f}%", f"{risk_score-50:.1f}%")
    
    with stat_col3:
        st.metric("Status Usia", "Berisiko" if hasil['rule_1'] == 1 else "Normal")
    
    with stat_col4:
        st.metric("Status Biomarker", "Abnormal" if (hasil['rule_5'] == 1 or hasil['rule_6'] == 1) else "Normal")

# Disclaimer dan informasi tambahan
st.markdown("---")
st.markdown("## ⚠️ Disclaimer dan Informasi Penting")

disclaimer_col1, disclaimer_col2 = st.columns(2)

with disclaimer_col1:
    st.markdown("""
    ### 🔬 Tentang Sistem
    - Sistem ini menggunakan **Forward Chaining** untuk inferensi
    - Berbasis pada 7 aturan IF-THEN yang telah ditetapkan
    - Menganalisis 6 parameter medis utama
    - Memberikan rekomendasi berdasarkan kombinasi faktor risiko
    """)

with disclaimer_col2:
    st.markdown("""
    ### ⚠️ Catatan Medis
    - Sistem ini **BUKAN** pengganti diagnosis medis profesional
    - Hasil analisis bersifat **edukatif** dan **informatif**
    - Untuk diagnosis akurat, **selalu konsultasi dengan dokter**
    - Faktor risiko lain mungkin tidak tercakup dalam sistem ini
    """)

st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
    <p style="margin: 0; color: #666;">
        <strong>Sistem Pakar Risiko Serangan Jantung</strong> | 
        Dikembangkan dengan Forward Chaining Method | 
        Untuk Tujuan Edukasi dan Penelitian
    </p>
</div>
""", unsafe_allow_html=True)