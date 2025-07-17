# Sistem Pakar Serangan Jantung (Rule-Based Forward Chaining)

Jalankan dengan:
```
streamlit run rulebaseseranganjantung.py
```

## 📋 Deskripsi Sistem

Sistem pakar ini adalah **aplikasi berbasis aturan IF-THEN** yang menggunakan metode **forward chaining** untuk menganalisis risiko serangan jantung pada pasien. Sistem dibuat dengan Python dan Streamlit untuk antarmuka web yang user-friendly.

---

## 🎯 Cara Kerja Sistem Pakar

### 1. **Input Data Pasien**
- Usia (tahun)
- Tekanan Darah Sistolik (mmHg)
- Tekanan Darah Diastolik (mmHg)
- Kadar Gula Darah (mg/dL)
- CK-MB (ng/mL)
- Troponin (ng/mL)

### 2. **Forward Chaining Process**
1. **Fakta Awal**: Data pasien dimasukkan sebagai fakta awal
2. **Pengecekan Aturan**: Sistem mengecek setiap aturan IF-THEN secara berurutan
3. **Inferensi**: Jika kondisi IF terpenuhi, kesimpulan THEN ditambahkan ke fakta
4. **Iterasi**: Proses diulang sampai tidak ada fakta baru yang bisa ditambahkan
5. **Kesimpulan**: Hasil akhir diambil dari fakta yang terkumpul

### 3. **Output Diagnosis**
- **RISIKO TINGGI**: Jika semua faktor risiko terpenuhi
- **RISIKO RENDAH**: Jika tidak semua faktor terpenuhi

---

## 📚 Basis Pengetahuan (Knowledge Base)

### Representasi Aturan IF-THEN:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEM PAKAR RULE-BASED                      │
│                    ATURAN IF-THEN                               │
└─────────────────────────────────────────────────────────────────┘

RULE 1:  IF umur pasien > 50 tahun 
         THEN risiko meningkat

RULE 2:  IF tekanan darah sistolik > 140 mmHg 
         THEN tekanan darah tinggi

RULE 3:  IF tekanan darah diastolik > 90 mmHg 
         THEN tekanan darah tinggi

RULE 4:  IF kadar gula darah > 126 mg/dL 
         THEN gula darah tinggi

RULE 5:  IF kadar CK-MB > 5 ng/mL 
         THEN CK-MB tinggi

RULE 6:  IF kadar troponin > 0.04 ng/mL 
         THEN troponin tinggi

RULE 7:  IF semua faktor risiko di atas terpenuhi 
         THEN risiko serangan jantung tinggi
```

### Penjelasan Aturan:
- **Aturan 1-6**: Mengecek masing-masing parameter medis secara individual
  - Return **1** jika kondisi terpenuhi (berisiko/tinggi)
  - Return **0** jika kondisi tidak terpenuhi (normal/tidak berisiko)
- **Aturan 7**: Aturan utama yang menentukan risiko tinggi jika semua parameter di atas = 1

---

## 🔄 Forward Chaining Engine

### Algoritma Forward Chaining:

```python
def forward_chaining_engine(fakta_awal):
    # 1. Inisialisasi fakta
    facts = {k: v for k, v in fakta_awal.items()}
    facts['facts'] = set()  # Set untuk fakta baru
    
    # 2. Loop sampai tidak ada fakta baru
    while new_fact_added:
        new_fact_added = False
        
        # 3. Cek setiap aturan
        for rule in RULES:
            # 4. Skip jika kesimpulan sudah ada
            if rule['conclusion'] in facts['facts']:
                continue
            
            # 5. Cek kondisi IF
            if rule['conditions'](facts):
                # 6. Tambahkan kesimpulan THEN
                facts['facts'].add(rule['conclusion'])
                new_fact_added = True
    
    return facts, log
```

### Contoh Proses:
**Input**: Age=60, Systolic=150, Diastolic=95, Blood sugar=130, CK-MB=6, Troponin=0.05

**Proses**:
1. ✅ IF Age > 50 THEN 1 (berisiko)
2. ✅ IF Systolic > 140 THEN 1 (tinggi)
3. ✅ IF Diastolic > 90 THEN 1 (tinggi)
4. ✅ IF Blood sugar > 126 THEN 1 (tinggi)
5. ✅ IF CK-MB > 5 THEN 1 (tinggi)
6. ✅ IF Troponin > 0.04 THEN 1 (tinggi)
7. ✅ IF semua_faktor = 1 THEN 1 (risiko tinggi)

**Output**: RISIKO TINGGI (karena semua aturan = 1)

---

## 💻 Penjelasan Kode per Bagian

### 1. Import Library
```python
import streamlit as st
```
- **streamlit**: Library untuk membuat web app dengan Python

### 2. Fungsi Pemeriksaan (Condition Functions)
```python
def rule_1_usia_berisiko(f):
    """
    Fungsi untuk mengecek apakah usia pasien berisiko
    Parameter f: dictionary berisi data pasien
    Return: 1 jika Age > 50, 0 jika tidak
    """
    if f['Age'] > 50:
        return 1
    return 0
```
- **Tujuan**: Mengecek kondisi IF untuk setiap parameter
- **Parameter**: Dictionary berisi data pasien
- **Return**: 1 (Ya) atau 0 (Tidak) berdasarkan kondisi

### 3. Knowledge Base (Basis Pengetahuan)
```python
RULES = [
    {
        'id': 'rule_1',
        'name': 'Aturan Usia Berisiko',
        'if_then': 'IF Age > 50 THEN 1 (berisiko)',
        'function': rule_1_usia_berisiko
    },
    # ... aturan lainnya
]
```
- **id**: Nama unik aturan
- **name**: Nama deskriptif aturan
- **if_then**: Aturan IF-THEN dalam format yang jelas
- **function**: Fungsi untuk mengecek kondisi dan return 1/0

### 4. Forward Chaining Engine
```python
def forward_chaining_engine(fakta_awal):
    # Inisialisasi
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
```
- **Tujuan**: Mesin inferensi yang menjalankan semua aturan IF-THEN
- **Input**: Fakta awal (data pasien)
- **Output**: Hasil setiap aturan (1/0) + log proses

### 5. Interface Streamlit
```python
st.title("🩺 Sistem Pakar Risiko Serangan Jantung")
with st.form("form_pasien"):
    age = st.number_input("Usia (tahun)", min_value=1, max_value=120)
    # ... input lainnya
    submit = st.form_submit_button("🔍 Jalankan Forward Chaining")
```
- **st.title**: Menampilkan judul aplikasi
- **st.form**: Membuat form input data
- **st.number_input**: Input angka dengan validasi
- **st.form_submit_button**: Tombol submit form

---

## 🎓 Konsep Sistem Pakar

### Forward Chaining vs Backward Chaining:
- **Forward Chaining**: Dari fakta ke kesimpulan (yang digunakan sistem ini)
- **Backward Chaining**: Dari kesimpulan ke fakta

### Komponen Sistem Pakar:
1. **Knowledge Base**: Basis pengetahuan (aturan IF-THEN)
2. **Inference Engine**: Mesin inferensi (forward chaining)
3. **User Interface**: Antarmuka pengguna (Streamlit)
4. **Working Memory**: Tempat menyimpan fakta sementara

### Kelebihan Sistem Ini:
- ✅ Mudah dipahami dan dijelaskan
- ✅ Transparan (bisa dilihat proses inferensinya)
- ✅ Dapat dimodifikasi dengan mudah
- ✅ Cocok untuk pembelajaran sistem pakar

### Keterbatasan:
- ❌ Aturan sederhana (tidak kompleks)
- ❌ Tidak menggunakan machine learning
- ❌ Tidak menggantikan diagnosis dokter

---

## 🚀 Cara Menjalankan

### Prerequisites:
```bash
pip install streamlit pandas
```

### Menjalankan Aplikasi:
```bash
streamlit run rulebaseseranganjantung.py
```

### Akses Aplikasi:
- Buka browser
- Kunjungi: `http://localhost:8501`

---

## 📝 Modifikasi dan Pengembangan

### Menambah Aturan Baru:
1. Buat fungsi kondisi baru
2. Tambahkan aturan ke list `RULES`
3. Sesuaikan logika inferensi jika diperlukan

### Contoh Menambah Aturan:
```python
def cek_heart_rate_tinggi(f):
    return f['Heart rate'] > 100

RULES.append({
    'id': 'heart_rate_tinggi',
    'conditions': cek_heart_rate_tinggi,
    'conclusion': 'heart_rate_tinggi',
    'desc': 'IF Heart rate > 100 THEN heart_rate_tinggi'
})
```

---

## ⚠️ Disclaimer

> **PENTING**: Sistem ini dibuat untuk tujuan edukasi dan pembelajaran sistem pakar. Untuk diagnosis medis yang akurat, selalu konsultasikan dengan profesional kesehatan.

---

## 📚 Referensi

- [Sistem Pakar - Wikipedia](https://id.wikipedia.org/wiki/Sistem_pakar)
- [Forward Chaining - Wikipedia](https://en.wikipedia.org/wiki/Forward_chaining)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Rule-Based Systems](https://en.wikipedia.org/wiki/Rule-based_system)

---

## 🤝 Kontribusi

Jika ada saran, pertanyaan, atau ingin berkontribusi untuk pengembangan sistem ini, silakan hubungi pembuat atau dosen pengampu.

---

**Dibuat untuk pembelajaran Sistem Pakar dan Kecerdasan Buatan** 🎓 