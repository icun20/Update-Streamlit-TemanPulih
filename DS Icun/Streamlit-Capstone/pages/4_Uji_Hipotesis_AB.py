import streamlit as st
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="A/B Testing Kepatuhan", layout="wide")
st.title("A/B Testing: Uji Signifikansi Faktor Kepatuhan Obat")
st.markdown("Modul ini menggunakan **Chi-Square Test of Independence** untuk menguji apakah terdapat perbedaan proporsi tingkat kepatuhan yang bermakna secara statistik antar kelompok pasien.")

@st.cache_data
def load_data():
    # Navigasi relatif dari Streamlit-Capstone/pages/ ke Proses Data/Hasil/
    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Proses Data', 'Hasil', '3_Data_Engineered_Multiclass.csv')
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Dataset tidak ditemukan. Pastikan file 3_Data_Engineered_Multiclass.csv tersedia di folder Proses Data/Hasil/.")
        return None

df = load_data()

if df is not None:
    st.markdown("### 1. Konfigurasi Eksperimen")
    
    col1, col2 = st.columns(2)
    with col1:
        # Pilihan fitur berdasarkan bagian A, B, C dari kamus data
        group_var = st.selectbox(
            "Pilih Variabel Pemisah (Kategorikal):", 
            ['GENDER', 'AGE', 'Educational Attainment', 'KNOWLEDGE_CLASS', 'BEHAVIOUR_CLASS']
        )
    with col2:
        # Target adalah Multiclass Adherence dari bagian D kamus data
        target_var = st.selectbox(
            "Pilih Variabel Target (Kelas Metrik):", 
            ['ADHERENCE_CLASS'] 
        )
        
    # Memastikan variabel ada di dataframe untuk mencegah KeyError
    if group_var in df.columns and target_var in df.columns:
        available_groups = df[group_var].dropna().unique().tolist()
        
        if len(available_groups) >= 2:
            st.markdown("#### Pemilihan Varian yang Akan Diuji")
            g1, g2 = st.columns(2)
            with g1:
                group_a_name = st.selectbox("Pilih Grup A (Varian 1):", available_groups, index=0)
            with g2:
                # Set default index ke 1 agar Grup B berbeda dari Grup A
                group_b_name = st.selectbox("Pilih Grup B (Varian 2):", available_groups, index=1 if len(available_groups) > 1 else 0)

            if group_a_name != group_b_name:
                # Filter dataset hanya untuk dua grup yang dibandingkan
                filtered_df = df[df[group_var].isin([group_a_name, group_b_name])]
                
                # Membuat tabel kontingensi (frekuensi observasi)
                contingency_table = pd.crosstab(filtered_df[group_var], filtered_df[target_var])
                
                # Uji Chi-Square
                chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                
                st.markdown("### 2. Hasil Pengujian Statistik")
                
                res_col1, res_col2 = st.columns([1, 2])
                with res_col1:
                    st.metric(label="P-Value (Chi-Square)", value=f"{p_value:.5f}")
                
                with res_col2:
                    alpha = 0.05
                    if p_value < alpha:
                        st.success(f"**Signifikan (Tolak H0).** P-Value < {alpha}. Terdapat perbedaan proporsi {target_var} yang bermakna secara statistik antara kelompok **{group_a_name}** dan **{group_b_name}**.")
                    else:
                        st.info(f"**Tidak Signifikan (Gagal Tolak H0).** P-Value >= {alpha}. Tidak cukup bukti statistik untuk menyatakan ada perbedaan proporsi {target_var} antara kelompok **{group_a_name}** dan **{group_b_name}**.")

                st.markdown("### 3. Distribusi Frekuensi Target")
                fig, ax = plt.subplots(figsize=(10, 5))
                
                # Menggunakan countplot untuk visualisasi perbandingan frekuensi kategori target
                sns.countplot(data=filtered_df, x=target_var, hue=group_var, palette="Set2", ax=ax)
                
                ax.set_title(f"Perbandingan Distribusi {target_var} antara {group_a_name} dan {group_b_name}")
                ax.set_ylabel("Jumlah Pasien")
                ax.set_xlabel(f"Level Kepatuhan ({target_var})")
                
                st.pyplot(fig)
                
                # Opsional: Tampilkan tabel kontingensi untuk transparansi data
                with st.expander("Lihat Tabel Frekuensi (Cross-Tabulation)"):
                    st.dataframe(contingency_table)

            else:
                st.warning("Perhatian: Grup A dan Grup B harus berbeda untuk dapat melakukan A/B Testing.")
        else:
            st.warning("Variabel pemisah yang dipilih tidak memiliki variasi minimal 2 kelompok.")
    else:
        st.error("Variabel yang dipilih tidak ditemukan di dalam dataset. Harap periksa proses Feature Engineering.")