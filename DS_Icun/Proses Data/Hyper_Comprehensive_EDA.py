import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import mutual_info_classif
import os

# Create Results Directory
output_dir = "Hyper_Comprehensive_EDA"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Theme
plt.rcParams['figure.dpi'] = 300
sns.set_theme(style="white", palette="bright")

def reconstruct_system(df):
    """Reconstructs the full system of 4 multiclass levels."""
    # Ensure all Q columns are numeric and imputed
    q_indices = list(range(19, 22)) + list(range(24, 27)) + list(range(31, 44)) + list(range(47, 50)) + list(range(50, 57))
    for i in q_indices:
        col = df.columns[i]
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Fix for potential all-NaN columns or string reduction error
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val if not pd.isna(median_val) else 0)

    # Adherence (Target)
    def calc_adherence(row):
        bad_indices = [50, 51, 52, 53, 55, 56] 
        good_index = 54 
        score = sum(1 for i in bad_indices if row.iloc[i] == 1) + (1 if row.iloc[good_index] == 0 else 0)
        if score == 0: return "H-ADHERENT"
        if score <= 2: return "L-ADHERENT"
        if score <= 5: return "M-ADHERENT"
        return "H-NON-ADHERENT"
    df['CLASS_ADHERENCE'] = df.apply(calc_adherence, axis=1)

    # Knowledge
    df['SCORE_KNOWLEDGE'] = df.iloc[:, [47, 48, 49]].sum(axis=1)
    df['CLASS_KNOWLEDGE'] = df['SCORE_KNOWLEDGE'].apply(lambda s: "GOOD" if s > 10 else ("MODERATE" if s > 5 else "INADEQUATE"))

    # Behaviour
    df['SCORE_BEHAVIOUR'] = df.iloc[:, [24, 25, 26]].sum(axis=1)
    df['CLASS_BEHAVIOUR'] = df['SCORE_BEHAVIOUR'].apply(lambda s: "LOW-FORGET" if s <= 2 else ("MOD-FORGET" if s <= 7 else "HIGH-FORGET"))

    # Perception
    df['SCORE_PERCEPTION'] = df.iloc[:, [19, 20, 21]].sum(axis=1)
    df['CLASS_PERCEPTION'] = df['SCORE_PERCEPTION'].apply(lambda s: "GOOD" if s > 9 else ("FAIR" if s > 6 else "BAD"))
    
    return df

def perform_hyper_eda(file_path):
    print("Initializing Hyper-Comprehensive EDA System...")
    df = pd.read_excel(file_path)
    df = reconstruct_system(df)
    
    # --- 1. SYSTEMIC FLOW ANALYSIS (Inter-Class Interaction) ---
    print("Analyzing Class-to-Class Influence...")
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Knowledge Level vs Adherence
    ct1 = pd.crosstab(df['CLASS_KNOWLEDGE'], df['CLASS_ADHERENCE'], normalize='index')
    sns.heatmap(ct1, annot=True, cmap="YlGnBu", ax=axes[0])
    axes[0].set_title('Impact of Knowledge Level on Adherence Class')
    
    # Behaviour Level vs Adherence
    ct2 = pd.crosstab(df['CLASS_BEHAVIOUR'], df['CLASS_ADHERENCE'], normalize='index')
    sns.heatmap(ct2, annot=True, cmap="YlOrRd", ax=axes[1])
    axes[1].set_title('Impact of Forgetfulness (Behaviour) on Adherence Class')
    
    plt.savefig(f"{output_dir}/1_InterClass_Dynamics.png")
    plt.close()

    # --- 2. GLOBAL FEATURE-FEATURE INTERACTION (Correlation Heatmap) ---
    print("Computing Global Feature Interaction Matrix...")
    # Select all numeric/ordinal columns
    num_df = df.select_dtypes(include=[np.number]).drop(columns=[c for c in df.columns if 'SCORE' in str(c) or 'CALC' in str(c)])
    corr = num_df.corr()
    
    plt.figure(figsize=(20, 16))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='coolwarm', center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title('Global Feature Interaction Heatmap (Multi-Dimensional Correlation)', fontsize=20)
    plt.savefig(f"{output_dir}/2_Feature_Feature_Interaction.png", bbox_inches='tight')
    plt.close()

    # --- 3. MANIFOLD CLUSTERING (t-SNE Visualization) ---
    print("Executing t-SNE Manifold Learning...")
    # Prep data for t-SNE
    le = LabelEncoder()
    X = df.select_dtypes(exclude=['datetime']).drop(columns=['CLASS_ADHERENCE', 'CLASS_KNOWLEDGE', 'CLASS_BEHAVIOUR', 'CLASS_PERCEPTION', 'S/N'])
    X.columns = X.columns.astype(str) # Fix for scikit-learn
    X_encoded = X.apply(lambda col: le.fit_transform(col.astype(str)))
    X_scaled = StandardScaler().fit_transform(X_encoded)
    
    tsne = TSNE(n_components=2, perplexity=30, max_iter=1000, random_state=42)
    X_tsne = tsne.fit_transform(X_scaled)
    
    plt.figure(figsize=(14, 10))
    sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=df['CLASS_ADHERENCE'], 
                    palette="Spectral", s=100, alpha=0.8, edgecolor='w')
    plt.title('t-SNE Manifold Projection: Hidden Adherence Structures', fontsize=18)
    plt.legend(title='Adherence Class', bbox_to_anchor=(1.05, 1))
    plt.savefig(f"{output_dir}/3_tSNE_Manifold_Structure.png", bbox_inches='tight')
    plt.close()

    # --- 4. FEATURE DEPENDENCY REPORT (Mutual Information) ---
    print("Generating Feature Dependency Report...")
    # Correlation of all Classes
    classes = ['CLASS_ADHERENCE', 'CLASS_KNOWLEDGE', 'CLASS_BEHAVIOUR', 'CLASS_PERCEPTION']
    class_df = df[classes].apply(lambda col: le.fit_transform(col))
    class_corr = class_df.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(class_corr, annot=True, cmap="Purples")
    plt.title('Systemic Dependency: How Classes Influence Each Other')
    plt.savefig(f"{output_dir}/4_Class_Dependency_Matrix.png")
    plt.close()

    print(f"\nHYPER-COMPREHENSIVE EDA COMPLETE! Folder: '{output_dir}'")

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    perform_hyper_eda(file_path)
