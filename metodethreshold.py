import pandas as pd

# Load CSV
csv_file = "Medicaldataset.csv"
df = pd.read_csv(csv_file)

# Filter hanya yang positif
positif = df[df['Result'] == 'positive']
print(f"Jumlah kasus positif: {len(positif)}\n")

# Daftar parameter
params = [
    'Age',
    'Systolic blood pressure',
    'Diastolic blood pressure',
    'Blood sugar',
    'CK-MB',
    'Troponin'
]

# Binning untuk setiap parameter
for col in params:
    print(f"\nDistribusi {col} pada kasus positif:")
    # Bisa atur bins=5 atau lebih halus misal bins=6
    bins = pd.cut(positif[col], bins=5)
    counts = bins.value_counts().sort_index()
    for interval, count in counts.items():
        print(f"  {interval}: {count}")
