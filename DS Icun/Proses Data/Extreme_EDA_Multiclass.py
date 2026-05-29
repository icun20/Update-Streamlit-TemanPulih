import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

# Results directory
output_dir = "Extreme_EDA_Multiclass"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Premium Style
sns.set_theme(style="white", palette="viridis")
plt.rcParams['figure.dpi'] = 300

def get_multiclass_labels(df):
    """Reconstructs all 4 multiclass levels based on questionnaire logic."""
    # Impute question levels (Q19-39) for calculation
    q_cols = df.columns[19:22].tolist() + df.columns[24:27].tolist() + \
             df.columns[31:44].tolist() + df.columns[50:57].tolist()
    
    for col in q_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())

    # 1. Adherence Level (Section D: Q33-39)
    # Score is sum of 'Negative' answers. Q37 is positive (1=Good), others are negative (1=Bad)
    def calc_adherence(row):
        bad_indices = [50, 51, 52, 53, 55, 56] # Indices in df
        good_index = 54 # Q37
        score = sum(1 for i in bad_indices if row.iloc[i] == 1) + (1 if row.iloc[good_index] == 0 else 0)
        if score == 0: return "HIGH ADHERENT"
        if score <= 2: return "LOW ADHERENT"
        if score <= 5: return "MEDIUM ADHERENT"
        return "HIGH NON-ADHERENT"
    
    df['TARGET_ADHERENCE'] = df.apply(calc_adherence, axis=1)

    # 2. Knowledge Level (Section C2: Q30-32)
    knowledge_cols = df.iloc[:, [47, 48, 49]].columns
    for col in knowledge_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['TOTAL_KNOWLEDGE'] = df[knowledge_cols].sum(axis=1)
    def calc_knowledge(score):
        if score <= 5: return "INADEQUATE"
        if score <= 10: return "MODERATE"
        return "GOOD"
    df['TARGET_KNOWLEDGE'] = df['TOTAL_KNOWLEDGE'].apply(calc_knowledge)

    # 3. Behaviour Level (Section B2: Q22-24)
    behaviour_cols = df.iloc[:, [24, 25, 26]].columns
    for col in behaviour_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['TOTAL_BEHAVIOUR'] = df[behaviour_cols].sum(axis=1)
    def calc_behaviour(score):
        if score <= 2: return "NOT FORGETFUL"
        if score <= 6: return "FORGETFUL"
        if score <= 9: return "MODERATELY FORGETFUL"
        return "HIGHLY FORGETFUL"
    df['TARGET_BEHAVIOUR'] = df['TOTAL_BEHAVIOUR'].apply(calc_behaviour)

    # 4. Perception Level (Section B1: Q19-21)
    perception_cols = df.iloc[:, [19, 20, 21]].columns
    for col in perception_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['TOTAL_PERCEPTION'] = df[perception_cols].sum(axis=1)
    def calc_perception(score):
        if score <= 3: return "UNDESIRABLE"
        if score <= 6: return "BAD"
        if score <= 9: return "FAIR"
        return "GOOD"
    df['TARGET_PERCEPTION'] = df['TOTAL_PERCEPTION'].apply(calc_perception)
    
    return df

def perform_extreme_eda(file_path):
    print("Executing Extreme EDA...")
    df = pd.read_excel(file_path)
    df = get_multiclass_labels(df)
    
    # --- 1. INTER-CLASS CORRELATION ---
    print("Analyzing Inter-Class Relationships...")
    # Relationship between Knowledge and Adherence
    cross_ka = pd.crosstab(df['TARGET_KNOWLEDGE'], df['TARGET_ADHERENCE'], normalize='index')
    plt.figure(figsize=(10, 6))
    sns.heatmap(cross_ka, annot=True, fmt=".2f", cmap="magma")
    plt.title('How Knowledge Level Affects Adherence (%)', fontsize=14)
    plt.savefig(f"{output_dir}/1_Knowledge_vs_Adherence.png")
    plt.close()

    # --- 2. GLOBAL FEATURE IMPORTANCE (Mutual Information) ---
    print("Calculating Mutual Information for all features...")
    # Prepare X (Demographics + Items)
    # Filter out target columns and SN
    exclude = ['TARGET_ADHERENCE', 'TARGET_KNOWLEDGE', 'TARGET_BEHAVIOUR', 'TARGET_PERCEPTION', 
               'TOTAL', 'TOTAL.1', 'TOTAL.2', 'TOTAL.3', 'S/N', 'RECON_PERCEPTION', 
               'RECON_BEHAVIOUR', 'RECON_KNOWLEDGE', 'RECON_ADHERENCE']
    X = df.drop(columns=[c for c in df.columns if c in exclude or 'CALC' in str(c) or 'RECON' in str(c)])
    
    # Encode categorical for MI
    le = LabelEncoder()
    X_encoded = X.copy()
    for col in X_encoded.columns:
        if pd.api.types.is_numeric_dtype(X_encoded[col]):
            X_encoded[col] = X_encoded[col].fillna(X_encoded[col].median())
        else:
            # Categorical: convert to string, encode, and handle NaNs by encoding 'missing'
            X_encoded[col] = X_encoded[col].fillna('missing').astype(str)
            X_encoded[col] = le.fit_transform(X_encoded[col])
    
    # Final check for any NaNs
    X_encoded = X_encoded.fillna(0)
    
    mi_scores = mutual_info_classif(X_encoded, le.fit_transform(df['TARGET_ADHERENCE']))
    mi_df = pd.DataFrame({'Feature': X.columns, 'Importance': mi_scores}).sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(12, 15))
    sns.barplot(x='Importance', y='Feature', data=mi_df.head(40), palette="viridis")
    plt.title('Top 40 Features Driving Adherence Level (Mutual Information)', fontsize=16)
    plt.savefig(f"{output_dir}/2_Global_Feature_Importance.png", bbox_inches='tight')
    plt.close()

    # --- 3. PSYCHOMETRIC VIOLIN PLOTS ---
    print("Visualizing Psychology Score Distributions...")
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    sns.violinplot(ax=axes[0,0], x='TARGET_ADHERENCE', y='TOTAL_KNOWLEDGE', data=df, inner="quartile")
    axes[0,0].set_title('Knowledge Distribution vs Adherence')
    
    sns.violinplot(ax=axes[0,1], x='TARGET_ADHERENCE', y='TOTAL_PERCEPTION', data=df, inner="quartile")
    axes[0,1].set_title('Perception Distribution vs Adherence')
    
    sns.violinplot(ax=axes[1,0], x='TARGET_ADHERENCE', y='TOTAL_BEHAVIOUR', data=df, inner="quartile")
    axes[1,0].set_title('Behaviour Score vs Adherence')
    
    # Missing Value Heatmap (Specific to questionnaire)
    sns.heatmap(ax=axes[1,1], data=df.iloc[:, 19:56].isnull(), cbar=False, cmap='viridis')
    axes[1,1].set_title('Missing Values in Questionnaires')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/3_Psychometric_Deep_Dive.png")
    plt.close()

    # --- 4. MULTI-LEVEL DEMOGRAPHICS ---
    print("Analyzing Demographic Interactions...")
    # Gender + Age Interaction
    plt.figure(figsize=(14, 8))
    sns.countplot(x='AGE', hue='TARGET_ADHERENCE', data=df, palette="husl")
    plt.title('Adherence Level Distribution Across Age Groups', fontsize=16)
    plt.legend(title='Adherence Class', bbox_to_anchor=(1.05, 1))
    plt.savefig(f"{output_dir}/4_Age_Demographic_Interaction.png", bbox_inches='tight')
    plt.close()

    print(f"\nEXTREME EDA COMPLETE! Results in '{output_dir}'")

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    perform_extreme_eda(file_path)
