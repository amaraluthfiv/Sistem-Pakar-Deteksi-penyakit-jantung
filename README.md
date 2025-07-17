# Sistem Pakar Serangan Jantung (Rule-Based Forward Chaining)

Jalankan dengan:
streamlit run rulebaseseranganjantung.py

## Deskripsi Sistem
Sistem pakar ini adalah aplikasi berbasis aturan IF-THEN yang menggunakan metode forward chaining untuk menganalisis risiko serangan jantung pada pasien. Sistem dibuat dengan Python dan Streamlit untuk antarmuka web yang user-friendly.

##  Cara Kerja Sistem Pakar

### 1. Input Data Pasien
- Usia (tahun)
- Tekanan Darah Sistolik (mmHg)
- Tekanan Darah Diastolik (mmHg)
- Kadar Gula Darah (mg/dL)
- CK-MB (ng/mL)
- Troponin (ng/mL)

### 2. Forward Chaining Process
1. Fakta Awal: Data pasien dimasukkan sebagai fakta awal
2. Pengecekan Aturan: Sistem mengecek setiap aturan IF-THEN secara berurutan
3. Inferensi: Jika kondisi IF terpenuhi, kesimpulan THEN ditambahkan ke fakta
4. Iterasi: Proses diulang sampai tidak ada fakta baru yang bisa ditambahkan
5. Kesimpulan: Hasil akhir diambil dari fakta yang terkumpul

### 3. Output Diagnosis
- RISIKO TINGGI: Jika semua faktor risiko terpenuhi
- RISIKO RENDAH: Jika tidak semua faktor terpenuhi

##  Basis Pengetahuan (Knowledge Base)
### Representasi Aturan IF-THEN:

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

### Penjelasan Aturan:
- Aturan 1-6: Mengecek masing-masing parameter medis secara individual
  - Return 1 jika kondisi terpenuhi (berisiko/tinggi)
  - Return 0 jika kondisi tidak terpenuhi (normal/tidak berisiko)
- Aturan 7: Aturan utama yang menentukan risiko tinggi jika semua parameter di atas = 1

##  Forward Chaining Engine
### Algoritma Forward Chaining:
python
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

### Contoh Proses:
Input: Age=60, Systolic=150, Diastolic=95, Blood sugar=130, CK-MB=6, Troponin=0.05
Proses:
1. IF Age > 50 THEN 1 (berisiko)
2. IF Systolic > 140 THEN 1 (tinggi)
3. IF Diastolic > 90 THEN 1 (tinggi)
4. IF Blood sugar > 126 THEN 1 (tinggi)
5. IF CK-MB > 5 THEN 1 (tinggi)
6. IF Troponin > 0.04 THEN 1 (tinggi)
7. IF semua_faktor = 1 THEN 1 (risiko tinggi)

Output: RISIKO TINGGI (karena semua aturan = 1)


