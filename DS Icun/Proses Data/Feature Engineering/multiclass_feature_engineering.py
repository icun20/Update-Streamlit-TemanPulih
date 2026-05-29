import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

# Setup directories
input_file = r"g:\Download\Capstone DS\Proses Data\Hasil\1_Data_Cleaned_Robust_Multiclass.csv"
output_dir_fe = r"g:\Download\Capstone DS\Proses Data\Feature Engineering"
output_dir_hasil = r"g:\Download\Capstone DS\Proses Data\Hasil"
log_dir = r"g:\Download\Capstone DS\Proses Data\Dokumentasi"

if not os.path.exists(output_dir_fe): os.makedirs(output_dir_fe)

def perform_feature_engineering():
    print("--- [Multiclass Feature Engineering Phase] ---")
    df = pd.read_csv(input_file)
    
    # 1. SEPARATE FEATURES AND TARGETS
    # Primary Target: ADHERENCE_CLASS
    # We will exclude other classes from the input features to avoid data leakage
    targets = ['ADHERENCE_CLASS', 'KNOWLEDGE_CLASS', 'BEHAVIOUR_CLASS', 'PERCEPTION_CLASS', 
               'KNOWLEDGE_SCORE', 'BEHAVIOUR_SCORE', 'PERCEPTION_SCORE']
    
    y = df['ADHERENCE_CLASS']
    X = df.drop(columns=targets)
    
    # 2. IDENTIFY COLUMN TYPES
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    num_cols = X.select_dtypes(include=['number']).columns.tolist()
    
    print(f"Encoding {len(cat_cols)} categorical columns...")
    print(f"Scaling {len(num_cols)} numerical columns...")
    
    # 3. ONE-HOT ENCODING
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X[cat_cols])
    encoded_cols = encoder.get_feature_names_out(cat_cols)
    df_encoded = pd.DataFrame(X_encoded, columns=encoded_cols)
    
    # 4. SCALING
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X[num_cols])
    df_scaled = pd.DataFrame(X_scaled, columns=num_cols)
    
    # Combine
    X_final = pd.concat([df_scaled, df_encoded], axis=1)
    
    # FINAL IMPUTATION (Safety check for SMOTE)
    X_final = X_final.fillna(0)
    
    # 5. SMOTE MULTICLASS (Class Balancing)
    print(f"Original class distribution: {y.value_counts().to_dict()}")
    
    # SMOTE requires at least 6 samples for k_neighbors=5 (default)
    # Since Class 0 only has 4 samples, we reduce k_neighbors
    smote = SMOTE(k_neighbors=3, random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_final, y)
    
    print(f"Resampled class distribution: {pd.Series(y_resampled).value_counts().to_dict()}")
    
    # 6. SAVE RESULTS
    # Combine resampled features and target
    df_resampled = pd.DataFrame(X_resampled, columns=X_final.columns)
    df_resampled['ADHERENCE_CLASS'] = y_resampled
    
    fe_output = os.path.join(output_dir_fe, "2_Data_Feature_Engineered.csv")
    hasil_output = os.path.join(output_dir_hasil, "2_Data_Feature_Engineered_Multiclass.csv")
    
    df_resampled.to_csv(fe_output, index=False)
    df_resampled.to_csv(hasil_output, index=False)
    
    # 7. GENERATE VISUALIZATION
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.countplot(x=y, palette='viridis')
    plt.title('Distribution BEFORE SMOTE')
    
    plt.subplot(1, 2, 2)
    sns.countplot(x=y_resampled, palette='magma')
    plt.title('Distribution AFTER SMOTE')
    
    plot_path = os.path.join(output_dir_fe, "smote_comparison.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    # 8. EXTREMELY COMPREHENSIVE DOCUMENTATION
    with open(os.path.join(log_dir, "Laporan_Feature_Engineering_Komprehensif.md"), "w") as f:
        f.write("# Laporan Feature Engineering Ekstrem Komprehensif (Multiclass)\n\n")
        
        f.write("## 1. Filosofi & Strategi Transformasi\n")
        f.write("Tahap ini bertujuan untuk mengubah data mentah yang bersifat campuran (teks & angka) menjadi matriks numerik murni yang optimal untuk arsitektur **Multi-Layer Perceptron (MLP)**.\n\n")
        
        f.write("### A. One-Hot Encoding (Variabel Kategorikal)\n")
        f.write(f"Variabel nominal diekspansi untuk menghindari bias ordinal. Dari **{len(cat_cols)}** variabel kategori asli, dihasilkan **{len(encoded_cols)}** fitur biner baru.\n\n")
        
        f.write("#### Tabel Pemetaan Ekspansi (Mapping):\n")
        f.write("| Variabel Asal | Jumlah Fitur Baru | Contoh Fitur |\n")
        f.write("|---------------|-------------------|--------------|\n")
        for col in cat_cols:
            matching = [ec for ec in encoded_cols if ec.startswith(col)]
            f.write(f"| {col} | {len(matching)} | `{matching[0]}` |\n")
        f.write("\n")

        f.write("### B. Standard Scaling (Variabel Numerik)\n")
        f.write("Menggunakan rumus `z = (x - u) / s`. Seluruh fitur kuesioner (Skala Likert 1-5) kini memiliki rata-rata 0 dan standar deviasi 1. Ini mencegah fitur dengan rentang besar mendominasi proses pembelajaran.\n\n")

        f.write("## 2. Analisis Struktur Data Final\n")
        sparsity = 1.0 - (np.count_nonzero(X_resampled) / float(X_resampled.size))
        f.write(f"*   **Total Fitur Input**: {X_final.shape[1]}\n")
        f.write(f"*   **Sparsity Index**: {sparsity:.4f} (Menunjukkan kepadatan data biner setelah encoding)\n")
        f.write(f"*   **Memory Usage**: {df_resampled.memory_usage().sum() / 1024:.2f} KB\n\n")

        f.write("## 3. Penyeimbangan Kelas (SMOTE Multiclass)\n")
        f.write("Karena Kelas 0 (High Adherent) hanya memiliki 4 data asli, algoritma SMOTE melakukan interpolasi linear antara titik data terdekat (k=3) untuk mensintesis data baru.\n\n")
        f.write("| ID | Nama Kelas | Sebelum | Sesudah | Rasio Peningkatan |\n")
        f.write("|----|------------|---------|---------|-------------------|\n")
        class_names = {0: "High Adherent", 1: "Low Adherent", 2: "Medium Adherent", 3: "High Non-Adherent"}
        for cls in sorted(y.unique()):
            before = y.value_counts()[cls]
            after = pd.Series(y_resampled).value_counts()[cls]
            f.write(f"| {cls} | {class_names[cls]} | {before} | {after} | {after/before:.1f}x |\n")
        
        f.write(f"\n![SMOTE Comparison](file:///{plot_path.replace('\\', '/')})\n\n")

        f.write("## 4. Galeri Fitur Final (Lengkap)\n")
        f.write("Berikut adalah daftar seluruh nama kolom yang akan menjadi input neuron pada layer pertama MLP:\n\n")
        f.write("```text\n")
        for i, col in enumerate(df_resampled.columns):
            f.write(f"{i+1:03}. {col}\n")
        f.write("```\n\n")

        f.write("## 5. Metadata & Integritas Data\n")
        f.write(f"*   **Target Variable**: `ADHERENCE_CLASS`\n")
        f.write(f"*   **Output Location**: `Hasil/2_Data_Feature_Engineered_Multiclass.csv`\n")
        f.write(f"*   **Data Consistency**: Seluruh kolom telah dipastikan bertipe `float64` atau `int64` (Tidak ada NaNs).\n")

    print(f"\nExtremely Comprehensive Feature Engineering Complete!")
    print(f"Report: {log_dir}/Laporan_Feature_Engineering_Komprehensif.md")

if __name__ == "__main__":
    perform_feature_engineering()
