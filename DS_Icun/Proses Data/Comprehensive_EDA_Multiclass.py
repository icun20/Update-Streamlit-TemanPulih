import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
import os

# Create Results Directory
output_dir = "EDA_Results"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set Premium Style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

def perform_comprehensive_eda(file_path):
    print("Loading and Preprocessing for EDA...")
    df = pd.read_excel(file_path)
    
    # 1. Target Reconstruction (Multiclass)
    def get_adherence_level(total):
        if pd.isna(total): return "MISSING"
        if total == 0: return "HIGH ADHERENT"
        if total <= 2: return "LOW ADHERENT"
        if total <= 6: return "MEDIUM ADHERENT"
        return "HIGH NON-ADHERENT"

    # Fill NaNs in Q33-39 with median to allow total calculation for everyone
    q_cols = df.columns[48:55] # Section D
    for col in q_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())
    
    # Re-calculate TOTAL.3 (Non-Adherence Score)
    df['CALC_TOTAL_D'] = df[q_cols].sum(axis=1)
    df['ADHERENCE_CLASS'] = df['CALC_TOTAL_D'].apply(get_adherence_level)
    
    # 2. Visualisasi 1: Klasemen Distribusi (Premium Donut Chart)
    plt.figure(figsize=(10, 7))
    counts = df['ADHERENCE_CLASS'].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, 
            pctdistance=0.85, explode=[0.05]*len(counts), colors=sns.color_palette("viridis", len(counts)))
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Proporsi Tingkat Kepatuhan (Multiclass)', fontsize=16, fontweight='bold')
    plt.savefig(f"{output_dir}/1_Adherence_Distribution.png")
    plt.close()

    # 3. Visualisasi 2: Hubungan Pendidikan vs Kepatuhan (Faceted Heatmap)
    print("Analyzing Education vs Adherence...")
    edu_cross = pd.crosstab(df['Educational Attainment'], df['ADHERENCE_CLASS'], normalize='index') * 100
    plt.figure(figsize=(12, 8))
    sns.heatmap(edu_cross, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage (%)'})
    plt.title('Pengaruh Tingkat Pendidikan terhadap Kepatuhan (%)', fontsize=16)
    plt.savefig(f"{output_dir}/2_Education_Vs_Adherence.png")
    plt.close()

    # 4. Visualisasi 3: Klastering PCA (Scatter 2D)
    print("Performing PCA for Cluster Visualization...")
    # Select numeric questionnaire features (Likert scales)
    likert_cols = df.columns[19:22].tolist() + df.columns[24:27].tolist() + df.columns[31:44].tolist()
    X_likert = df[likert_cols].apply(pd.to_numeric, errors='coerce').fillna(3) # Impute with neutral
    X_likert.columns = X_likert.columns.astype(str) # Fix for scikit-learn
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_likert)
    
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=pca_results[:,0], y=pca_results[:,1], hue=df['ADHERENCE_CLASS'], 
                    style=df['ADHERENCE_CLASS'], palette="deep", s=100, alpha=0.7)
    plt.title('Visualisasi Kedekatan Pasien (PCA - 2D Projection)', fontsize=16)
    plt.xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]:.1%})')
    plt.ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]:.1%})')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(f"{output_dir}/3_Patient_Clustering_PCA.png", bbox_inches='tight')
    plt.close()

    # 5. Visualisasi 4: Profil Psikologis (Radar Data Preparation)
    print("Preparing Radar Chart Data...")
    # Calculate mean scores per class for different sections
    # Normalized 0-1 for radar
    radar_data = df.groupby('ADHERENCE_CLASS').agg({
        'TOTAL': 'mean',   # Perception
        'TOTAL.1': 'mean', # Behaviour
        'TOTAL.2': 'mean', # Knowledge
    }).fillna(0)
    
    # Save radar data to CSV for later premium plotting
    radar_data.to_csv(f"{output_dir}/radar_profile_data.csv")
    
    # 6. Statistik: Kruskal-Wallis Test
    print("\n--- Statistical Validation (Kruskal-Wallis) ---")
    groups = [df[df['ADHERENCE_CLASS'] == cls]['CALC_TOTAL_D'] for cls in df['ADHERENCE_CLASS'].unique()]
    h_stat, p_val = stats.kruskal(*groups)
    
    with open(f"{output_dir}/Statistical_Report.txt", "w") as f:
        f.write("LAPORAN VALIDASI STATISTIK MULTICLASS\n")
        f.write("=====================================\n\n")
        f.write(f"Uji Kruskal-Wallis untuk Perbedaan Antar Kelas:\n")
        f.write(f"H-Statistic: {h_stat:.4f}\n")
        f.write(f"P-Value: {p_val:.4e}\n")
        if p_val < 0.05:
            f.write("\nKESIMPULAN: Terdapat perbedaan yang sangat signifikan secara statistik antara ke-4 tingkatan kepatuhan (p < 0.05).\n")
        else:
            f.write("\nKESIMPULAN: Tidak ditemukan perbedaan signifikan (p >= 0.05).\n")

    print(f"\nEDA Berhasil! Hasil tersimpan di folder '{output_dir}'")

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    perform_comprehensive_eda(file_path)
