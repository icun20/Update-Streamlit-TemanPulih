import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest

# Setup directories
output_dir = r"g:\Download\Capstone DS\Proses Data\Hasil"
log_dir = r"g:\Download\Capstone DS\Proses Data\Dokumentasi"
if not os.path.exists(output_dir): os.makedirs(output_dir)

def perform_hyper_cleaning(file_path):
    print("--- [Hyper-Robust Cleaning Phase] ---")
    df = pd.read_excel(file_path)
    initial_shape = df.shape
    
    # 1. STANDARDIZATION (Section A)
    print("Standardizing categorical text...")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip().str.upper()
    
    # 2. ITEM-LEVEL IMPUTATION (Global)
    # Include ALL questionnaire sections: B, C, D, E
    q_cols = list(df.columns[19:22]) + list(df.columns[24:27]) + \
             list(df.columns[31:57]) + list(df.columns[58:70])
    
    print(f"Imputing {len(q_cols)} questionnaire items...")
    for col in q_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Robust median imputation
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val if not pd.isna(median_val) else 3) # 3 is neutral Likert

    # 3. OUTLIER REMOVAL (Isolation Forest)
    print("Detecting and removing 21 most extreme outliers...")
    # Select numeric features for outlier detection
    X_outlier = df[q_cols].fillna(0)
    X_outlier.columns = X_outlier.columns.astype(str) # Fix for scikit-learn
    iso = IsolationForest(contamination=21/609, random_state=42)
    outliers = iso.fit_predict(X_outlier)
    
    # Save outlier rows for documentation before dropping
    outlier_rows = df[outliers == -1]
    outlier_rows.to_csv(os.path.join(output_dir, "dropped_outliers_multiclass.csv"), index=False)
    
    df = df[outliers == 1]
    print(f"Removed {len(outlier_rows)} outliers.")

    # 4. CROSS-VALIDATION & LOGIC CLEANING
    print("Applying logical consistency rules...")
    # AGE is categorical (e.g., 'ABOVE 50', '31-40'), so we treat it as text.
    # We only remove rows where GENDER or essential info is missing.
    df = df.dropna(subset=['GENDER']) 

    # 5. MULTICLASS RECONSTRUCTION (4 Targets)
    print("Reconstructing Multi-Targets...")
    
    # TARGET 1: ADHERENCE_CLASS (4-Class)
    def calc_adherence(row):
        bad_indices = [50, 51, 52, 53, 55, 56] 
        good_index = 54 
        score = sum(1 for i in bad_indices if row.iloc[i] == 1) + (1 if row.iloc[good_index] == 0 else 0)
        if score == 0: return 0 
        if score <= 2: return 1 
        if score <= 5: return 2 
        return 3 
    df['ADHERENCE_CLASS'] = df.apply(calc_adherence, axis=1)

    # TARGET 2: KNOWLEDGE_CLASS (3-Class)
    df['KNOWLEDGE_SCORE'] = df.iloc[:, [47, 48, 49]].sum(axis=1)
    df['KNOWLEDGE_CLASS'] = df['KNOWLEDGE_SCORE'].apply(lambda s: 0 if s <= 5 else (1 if s <= 10 else 2))

    # TARGET 3: BEHAVIOUR_CLASS (3-Class)
    df['BEHAVIOUR_SCORE'] = df.iloc[:, [24, 25, 26]].sum(axis=1)
    df['BEHAVIOUR_CLASS'] = df['BEHAVIOUR_SCORE'].apply(lambda s: 0 if s <= 2 else (1 if s <= 7 else 2))

    # TARGET 4: PERCEPTION_CLASS (3-Class)
    df['PERCEPTION_SCORE'] = df.iloc[:, [19, 20, 21]].sum(axis=1)
    df['PERCEPTION_CLASS'] = df['PERCEPTION_SCORE'].apply(lambda s: 0 if s <= 3 else (1 if s <= 6 else 2))

    # 6. RENAME COLUMNS FOR CLARITY
    print("Renaming columns to descriptive headers...")
    
    # Identify artifact columns to drop (Unnamed, SPSS, TOTAL, etc.)
    cols_to_drop = ['S/N', 'TOTAL', 'TOTAL.1', 'TOTAL.2', 'TOTAL.3', 'SPSS', 'SPSS.1', 'SPSS.2', 
                    'PERCEPTION LEVEL', 'BEHAVIOUR LEVEL', 'KNOWLEDGE LEVEL', 'NON ADHERENT LEVEL']
    # Add any column that starts with 'Unnamed'
    cols_to_drop += [c for c in df.columns if 'Unnamed' in str(c) or 'TOTAL' in str(c).upper()]
    
    df_final = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Also clean column names in df_final (sometimes they are int in Excel)
    df_final.columns = df_final.columns.astype(str)
    
    rename_dict = {
        '19': 'B1_ChangeMind_Decision', '20': 'B1_ChangeMind_Convince', '21': 'B1_AcceptSuggestion',
        '22': 'B2_ForgetPlan', '23': 'B2_ForgetTold', '24': 'B2_MissAppointment',
        '25': 'B_CauseOfMissing', '26': 'B_ReminderMethod',
        '27': 'C1_DrugHelp', '28': 'C1_DrugBurdensome', '29': 'C1_DrugInadequate',
        '30': 'C2_AwareBeforeDiag', '31': 'C2_AwareLifestyle', '32': 'C2_AwareProlonged',
        '33': 'D_ForgetPrescribed', '34': 'D_FailOtherReasons', '35': 'D_StopIfWorse',
        '36': 'D_ForgetTravel', '37': 'D_TakeAllYesterday', '38': 'D_StopIfFeelBetter',
        '39': 'D_FeelHassled', '40': 'D_DifficultyRemember',
        '41': 'E_ForgetGeneral', '42': 'E_AwareForgetDetails', '43': 'E_DangerNoAdvice',
        '44': 'E_BenefitAlerts', '45': 'E_BenefitPersuasive', '46': 'E_BenefitRiskExpl',
        '47': 'E_BenefitGainExpl', '48': 'E_CostBenefitMobile', '49': 'E_AdaptVoiceSMS',
        '50': 'E_EnableDiscussion', '51': 'E_PersonalAcceptance'
    }
    df_final = df_final.rename(columns=rename_dict)
    
    # 7. FINAL AUDIT & SAVE
    final_shape = df_final.shape
    
    # Save to both locations
    output_file_hasil = os.path.join(output_dir, "1_Data_Cleaned_Robust_Multiclass.csv")
    output_file_stage = r"g:\Download\Capstone DS\Proses Data\Pra Proses\Data_Cleaned_Multiclass.csv"
    
    df_final.to_csv(output_file_hasil, index=False)
    df_final.to_csv(output_file_stage, index=False)
    
    # Write Audit Report
    with open(os.path.join(log_dir, "Audit_Cleaning_Multiclass.txt"), "w") as f:
        f.write("HYPER-ROBUST CLEANING AUDIT REPORT\n")
        f.write("=================================\n\n")
        f.write(f"Initial Records: {initial_shape[0]}\n")
        f.write(f"Final Records: {final_shape[0]}\n")
        f.write(f"Outliers Removed: {len(outlier_rows)}\n")
        f.write(f"Invalid Ages Removed: {initial_shape[0] - len(outlier_rows) - final_shape[0]}\n")
        f.write(f"Questionnaire Items Imputed: {len(q_cols)}\n")
        f.write("\nTarget Class Distribution (Adherence):\n")
        f.write(str(df_final['ADHERENCE_CLASS'].value_counts().sort_index()))

    print(f"\nDone! Cleaned data saved to:")
    print(f"1. {output_file_hasil}")
    print(f"2. {output_file_stage}")
    print(f"Audit report saved to {log_dir}/Audit_Cleaning_Multiclass.txt")

if __name__ == "__main__":
    raw_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    perform_hyper_cleaning(raw_path)
