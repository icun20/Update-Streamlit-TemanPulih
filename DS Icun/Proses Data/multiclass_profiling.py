import pandas as pd
import numpy as np

def multiclass_profiling(file_path):
    df = pd.read_excel(file_path)
    
    # 1. Define Reconstruction Logic
    def get_perception_level(total):
        if pd.isna(total): return np.nan
        if total <= 3: return "UNDESIRABLE"
        if total <= 6: return "BAD"
        if total <= 9: return "FAIR"
        return "GOOD"

    def get_behaviour_level(total):
        if pd.isna(total): return np.nan
        if total <= 2: return "NOT FORGETFUL"
        if total <= 6: return "FORGETFUL"
        if total <= 9: return "MODERATELY FORGETFUL"
        return "HIGHLY FORGETFUL"

    def get_knowledge_level(total):
        if pd.isna(total): return np.nan
        if total <= 5: return "INADEQUATE"
        if total <= 10: return "MODERATE"
        return "GOOD"

    def get_adherence_level(total):
        if pd.isna(total): return np.nan
        if total == 0: return "HIGH ADHERENT"
        if total <= 2: return "LOW ADHERENT"
        if total <= 6: return "MEDIUM ADHERENT"
        return "HIGH NON-ADHERENT"

    # 2. Apply Logic to full dataset
    df['RECON_PERCEPTION'] = df['TOTAL'].apply(get_perception_level)
    df['RECON_BEHAVIOUR'] = df['TOTAL.1'].apply(get_behaviour_level)
    df['RECON_KNOWLEDGE'] = df['TOTAL.2'].apply(get_knowledge_level)
    df['RECON_ADHERENCE'] = df['TOTAL.3'].apply(get_adherence_level)

    # 3. Print Distributions
    targets = ['RECON_PERCEPTION', 'RECON_BEHAVIOUR', 'RECON_KNOWLEDGE', 'RECON_ADHERENCE']
    print("--- Multiclass Target Distributions (Reconstructed) ---")
    for t in targets:
        print(f"\n{t}:")
        print(df[t].value_counts(dropna=False))

    # 4. Data Quality Check for Multiclass
    print("\n--- Multiclass Data Quality ---")
    print(df[targets].isnull().sum())

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    multiclass_profiling(file_path)
