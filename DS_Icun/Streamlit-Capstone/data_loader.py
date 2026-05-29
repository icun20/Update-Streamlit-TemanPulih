import pandas as pd
import numpy as np
import os
import streamlit as st

@st.cache_data
def load_and_transform_data(file_path):
    """
    Loads and transforms the multidimensional adherence dataset.
    Performs data cleaning and feature engineering based on EDA notebooks.
    """
    if not os.path.exists(file_path):
        return None
        
    df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
    
    # 1. Clean missing/empty columns
    df.dropna(axis=1, how='all', inplace=True)
    
    # 2. Map Questionnaire Column Names
    question_mapping = {
        19: "How often would you change your mind to do what you have decided not to do?",
        20: "How often would you likely change your mind to do a thing if convinced or motivated?",
        21: "How often would you change or accept suggestions from care provider towards a change of your decision",
        22: "How often do you forget to do what you planned doing at the immediate",
        23: "How often do you forget something you were told a few minutes before",
        24: "How often do you miss appointments, if you are not prompted by someone or by a reminder such as phone call or SMS",
        25: "Why would you likely miss your drug(s), what usually the cause?",
        26: "What reminds you of your medication time and dose?",
        27: "Do you belief drug(s) can help your situation",
        28: "Taking drug is burdensome",
        29: "Drug alone is inadequate",
        30: "Are you aware of the sickness before you are diagnosed",
        31: "Are you aware that the sickness required certain lifestyle changes",
        32: "Are you aware the disease required prolonged treatment",
        33: "Do you sometimes forget to take your drug as prescribed?",
        34: "People sometimes fail to take their drug for reasons other than forgetting. Thinking over the past 2 weeks, were there any days when you did not take your drug?",
        35: "Have you ever cut back or stopped taking your drugs without telling your doctor because you felt worse when you use it?",
        36: "When you travel or leave home, do you sometimes forget to take along your drugs?",
        37: "Did you take all your prescribed drugs yesterday?",
        38: "When you feel like your symptoms are under control, do you sometimes stop taking your drugs?",
        39: "Taking drug every day is a real inconvenience for some people. Do you ever feel hassled about sticking to your medication plan?",
        40: "How often do you have difficulty in remembering to take your prescribed drugs?",
        41: "People (including me) sometimes forget to take drugs as prescribed",
        42: "It is possible to forget time of taking drugs, number of drugs to be taken and number of times drugs should be taken",
        43: "Taking drug without doctor's advice will make health condition worse",
        44: "Alert messages, agent voice call, interactive voice response (IVR) calls and USSD will help to take their drugs as advised",
        45: "Persuasive, motivational, educational messages through voice call, SMS, USSD can help people to take their drugs as instructed",
        46: "Using IVR call, USSD and SMS messages explain the benefits of taking drugs as instructed will help people to take their drugs properly",
        47: "Using IVR call, USSD, and SMS messages to explain risk/danger of not taking drug will help people to take their drugs properly",
        48: "Do you think there are cost benefits in adapting mobile app services to deliver intervention functions",
        49: "Do you think healthcare provider, caregivers and patient should adapt the use of IVR calls, agent voice calls and SMS services to make drug intake better?",
        50: "The mobile app service could enable patients discuss with care providers before next appointment.",
        51: "Would you accept and use mobile app services as a person?"
    }
    
    numbered_cols = [col for col in df.columns if str(col).isdigit()]
    rename_dict = {}
    for col in numbered_cols:
        if col in question_mapping:
            rename_dict[col] = f"Q{col}: {question_mapping[col]}"
        else:
            rename_dict[col] = f"Q_{col}"
            
    df.rename(columns=rename_dict, inplace=True)
    
    # 3. Standardize Categorical Data
    if 'GENDER' in df.columns:
        df['GENDER'] = df['GENDER'].astype(str).str.lower().str.strip()

    lang_col = 'What is your preferred communication language'
    if lang_col in df.columns:
        df[lang_col] = df[lang_col].astype(str).str.lower().str.strip()
        df[lang_col] = df[lang_col].replace('housa', 'hausa')
        df[lang_col] = df[lang_col].replace('nan', np.nan)
        
    # Standardize Age
    if 'AGE' in df.columns:
        df['AGE'] = df['AGE'].replace({'4--50': '41-50', '21': '21-30'}).astype(str)
        
    # Standardize Target Column (if exists)
    col_target = 'NON ADHERENT LEVEL'
    if col_target in df.columns:
        df[col_target] = df[col_target].astype(str).str.upper().str.strip()
        df[col_target] = df[col_target].replace('NAN', np.nan)
        
    # Standardize Health Condition
    hc_col = 'Health Condition'
    if hc_col in df.columns:
        df[hc_col] = df[hc_col].astype(str).str.upper().str.strip()
        replacements = {
            'NAN': np.nan, 'NONE': 'NIL', 'NOHTING': 'NIL', 
            'GLACOMA': 'GLAUCOMA', 'PRIMARY OPEN ANGLE GLAUCOMA': 'GLAUCOMA',
            'EYE PROBLEM': 'GLAUCOMA',
            'THYPHIOD MALARIA': 'MALARIA',
            'SKIN DISEASE': 'SKIN PROBLEM',
            'KIDNEY DISEASE': 'KIDNEY FAILURE',
            'ULCERS': 'ULCER'
        }
        df[hc_col] = df[hc_col].replace(replacements)

    # 4. Feature Engineering: Demographics
    def flag_demografi(row):
        age = str(row.get('AGE', '')).strip().upper()
        edu = str(row.get('Educational Attainment', '')).strip().upper()
        is_old = '50' in age and ('ABOVE' in age or '>' in age)
        is_mid_low_edu = edu in ['WASC/SSCE', 'FLSC', 'FSLC']
        
        if is_old and is_mid_low_edu:
            return 'Lansia (>50) & Edu Menengah/Bawah'
        else:
            return 'Kelompok Lainnya'
            
    df['Demo_Group'] = df.apply(flag_demografi, axis=1)

    # 5. Feature Engineering: Reminder Need (from EDA 2)
    # Define columns related to forgetting
    q_forget = [
        "Q22: How often do you forget to do what you planned doing at the immediate",
        "Q23: How often do you forget something you were told a few minutes before",
        "Q24: How often do you miss appointments, if you are not prompted by someone or by a reminder such as phone call or SMS",
        "Q33: Do you sometimes forget to take your drug as prescribed?",
        "Q36: When you travel or leave home, do you sometimes forget to take along your drugs?",
        "Q40: How often do you have difficulty in remembering to take your prescribed drugs?"
    ]
    
    # Ensure columns exist before calculating
    available_q_forget = [c for c in q_forget if c in df.columns]
    
    if available_q_forget:
        # Convert to numeric
        for col in available_q_forget:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # Calculate score (simple sum for demo, adjust based on actual EDA notebook logic)
        # Higher score = higher forgetfulness
        df['reminder_need_score'] = df[available_q_forget].sum(axis=1)
        
        # Segment into High, Medium, Low
        def segment_reminder(score):
            if pd.isna(score):
                return 'Unknown'
            elif score > 15:
                return 'Tinggi'
            elif score > 8:
                return 'Sedang'
            else:
                return 'Rendah'
                
        df['reminder_need_segment'] = df['reminder_need_score'].apply(segment_reminder)
    
    return df
