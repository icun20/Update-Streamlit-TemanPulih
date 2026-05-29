import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats

def cronbach_alpha(df):
    df_corr = df.corr()
    n_items = df.shape[1]
    average_corr = df_corr.values[np.triu_indices_from(df_corr.values, k=1)].mean()
    return (n_items * average_corr) / (1 + (n_items - 1) * average_corr)

def advanced_eda(file_path):
    print("Loading data...")
    df = pd.read_excel(file_path)
    
    # 1. Outlier Detection
    likert_indices = [19, 20, 21, 25, 26, 27, 34, 35, 36, 41, 42, 43] + list(range(59, 69))
    likert_df = df.iloc[:, likert_indices].copy()
    likert_clean = likert_df.dropna()
    
    print("\n--- 1. Outlier Detection ---")
    if not likert_clean.empty:
        iso = IsolationForest(contamination=0.05, random_state=42)
        outliers = iso.fit_predict(likert_clean)
        n_outliers = (outliers == -1).sum()
        print(f"Detected {n_outliers} multivariate outliers (5% threshold)")
        # Identify who they are (just sample)
        outlier_samples = likert_clean[outliers == -1].head()
        print("Sample of outlier responses:")
        print(outlier_samples)
    
    # 2. Reliability Analysis
    sections = {
        'Section B1 (19-21)': df.iloc[:, [19, 20, 21]],
        'Section B2 (22-24)': df.iloc[:, [25, 26, 27]],
        'Section C1 (27-29)': df.iloc[:, [34, 35, 36]],
        'Section C2 (30-32)': df.iloc[:, [41, 42, 43]],
        'Section E (App Percept)': df.iloc[:, range(59, 69)]
    }
    
    print("\n--- 2. Reliability Analysis (Cronbach's Alpha) ---")
    for name, s_df in sections.items():
        # Drop NaN for reliability check
        clean_s = s_df.dropna()
        if clean_s.shape[0] > 1:
            alpha = cronbach_alpha(clean_s)
            print(f"{name} (N={clean_s.shape[0]}): {alpha:.4f}")
        else:
            print(f"{name}: Not enough data")

    # 3. PCA & Clustering
    print("\n--- 3. Multivariate Clustering (PCA + KMeans) ---")
    if not likert_clean.empty:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(likert_clean)
        
        # PCA
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(scaled_data)
        print(f"PCA Variance Explained (2 components): {np.sum(pca.explained_variance_ratio_):.4f}")
        
        # KMeans
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scaled_data)
        
        # Visualize (saving to file)
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x=pca_data[:, 0], y=pca_data[:, 1], hue=clusters, palette='viridis')
        plt.title('Patient Clustering (PCA Space)')
        plt.xlabel('PCA 1')
        plt.ylabel('PCA 2')
        plt.savefig('patient_clusters.png')
        print("Clustering visualization saved as patient_clusters.png")

    # 4. Demographic vs Adherence (Cross-tab)
    target_col = df.columns[69]
    print(f"\n--- 4. Demographic Impact on {target_col} ---")
    demo_cols = ['GENDER', 'AGE', 'Educational Attainment']
    for col in demo_cols:
        ct = pd.crosstab(df[col], df[target_col], normalize='index') * 100
        print(f"\n{col} vs Adherence (%):")
        print(ct)

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    advanced_eda(file_path)
