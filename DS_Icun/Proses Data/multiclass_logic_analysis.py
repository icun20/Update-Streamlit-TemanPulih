import pandas as pd
import numpy as np

def analyze_multiclass_logic(file_path):
    df = pd.read_excel(file_path)
    
    # 1. Perception Level (B1: 19, 20, 21 -> Total Index 22)
    print("--- Perception Level Logic ---")
    subset1 = df[['TOTAL', 'PERCEPTION LEVEL']].dropna()
    if not subset1.empty:
        print(subset1.groupby('PERCEPTION LEVEL')['TOTAL'].agg(['min', 'max', 'count']))
    
    # 2. Behaviour Level (B2: 22, 23, 24 -> Total Index 28)
    print("\n--- Behaviour Level Logic ---")
    subset2 = df[['TOTAL.1', 'BEHAVIOUR LEVEL']].dropna()
    if not subset2.empty:
        print(subset2.groupby('BEHAVIOUR LEVEL')['TOTAL.1'].agg(['min', 'max', 'count']))
        
    # 3. Knowledge Level (C2: 30, 31, 32 -> Total Index 44)
    print("\n--- Knowledge Level Logic ---")
    subset3 = df[['TOTAL.2', 'KNOWLEDGE LEVEL']].dropna()
    if not subset3.empty:
        print(subset3.groupby('KNOWLEDGE LEVEL')['TOTAL.2'].agg(['min', 'max', 'count']))
        
    # 4. Non-Adherent Level (D: 33-39 -> Total Index 56)
    print("\n--- Non-Adherent Level Logic ---")
    subset4 = df[['TOTAL.3', 'NON ADHERENT LEVEL']].dropna()
    if not subset4.empty:
        print(subset4.groupby('NON ADHERENT LEVEL')['TOTAL.3'].agg(['min', 'max', 'count']))

if __name__ == "__main__":
    file_path = r"g:\Download\Capstone DS\Proses Data\MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"
    analyze_multiclass_logic(file_path)
