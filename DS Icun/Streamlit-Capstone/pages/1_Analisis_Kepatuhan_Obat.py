"""
Page 1 – Analisis Kepatuhan Obat (Adherence Level)
Based on EDA_Kepatuhan_Obat.ipynb – expanded with richer visualisations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Analisis Kepatuhan Obat",
    page_icon=":material/medication:",
    layout="wide",
)

# ── helpers ──────────────────────────────────────────────────────────────────
TARGET = "NON ADHERENT LEVEL"


def _pct_crosstab(df: pd.DataFrame, row_col: str, target: str = TARGET):
    ct = pd.crosstab(df[row_col], df[target], normalize="index") * 100
    ct = ct.reset_index().melt(id_vars=row_col, var_name="Adherence Level", value_name="Persentase")
    return ct


# ── data ─────────────────────────────────────────────────────────────────────
if "filtered_df" not in st.session_state:
    st.warning("Buka halaman utama terlebih dahulu agar data ter-load.")
    st.stop()

raw = st.session_state["filtered_df"]
df = raw.dropna(subset=[TARGET])

if df.empty:
    st.error("Tidak ada data dengan label kepatuhan valid setelah filter diterapkan.")
    st.stop()

# ── title ────────────────────────────────────────────────────────────────────
st.title("Analisis Kepatuhan Minum Obat")
st.caption("Sumber: EDA_Kepatuhan_Obat – diperluas dengan visualisasi komprehensif")

# ── 0  Distribusi Target ────────────────────────────────────────────────────
st.header("Distribusi Tingkat Kepatuhan", divider="blue")

col_a, col_b = st.columns(2)

with col_a:
    counts = df[TARGET].value_counts().reset_index()
    counts.columns = ["Level", "Jumlah"]
    fig = px.bar(counts, x="Level", y="Jumlah", color="Level", template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(xaxis_title="Adherence Level", yaxis_title="Jumlah Pasien", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig2 = px.pie(counts, names="Level", values="Jumlah", hole=0.45, template="plotly_white",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_traces(textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("Insight", icon=":material/lightbulb:"):
    for lvl, cnt in zip(counts["Level"], counts["Jumlah"]):
        pct = cnt / counts["Jumlah"].sum() * 100
        st.write(f"- **{lvl}**: {cnt} pasien ({pct:.1f}%)")

# ── 1  Demografi vs Kepatuhan ────────────────────────────────────────────────
st.header("1. Demografi dan Hubungannya dengan Kepatuhan", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Berapa persentase tingkat Non-Adherent pada kelompok usia "
    "'Di atas 50 tahun' dengan pendidikan menengah ke bawah dibandingkan kelompok lainnya?"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kelompok Demografi Target")
    demo_counts = df["Demo_Group"].value_counts().reset_index()
    demo_counts.columns = ["Kelompok", "Jumlah"]
    fig_d1 = px.bar(demo_counts, x="Kelompok", y="Jumlah", color="Kelompok", template="plotly_white")
    fig_d1.update_layout(showlegend=False)
    st.plotly_chart(fig_d1, use_container_width=True)

with col2:
    st.subheader("Kepatuhan per Kelompok Demografi")
    demo_ct = _pct_crosstab(df, "Demo_Group")
    fig_d2 = px.bar(demo_ct, x="Demo_Group", y="Persentase", color="Adherence Level",
                    barmode="stack", template="plotly_white", text_auto=".1f")
    st.plotly_chart(fig_d2, use_container_width=True)

# Age breakdown
st.subheader("Detail: Kepatuhan per Kelompok Usia")
age_ct = _pct_crosstab(df, "AGE")
fig_age = px.bar(age_ct, x="AGE", y="Persentase", color="Adherence Level",
                 barmode="group", template="plotly_white", text_auto=".1f")
fig_age.update_layout(xaxis_title="Kelompok Usia")
st.plotly_chart(fig_age, use_container_width=True)

# Education breakdown
st.subheader("Detail: Kepatuhan per Tingkat Pendidikan")
edu_col = "Educational Attainment"
if edu_col in df.columns:
    edu_ct = _pct_crosstab(df.dropna(subset=[edu_col]), edu_col)
    fig_edu = px.bar(edu_ct, x=edu_col, y="Persentase", color="Adherence Level",
                     barmode="group", template="plotly_white", text_auto=".1f")
    st.plotly_chart(fig_edu, use_container_width=True)

with st.expander("Insight Demografi", icon=":material/lightbulb:"):
    st.write(
        "Analisis menunjukkan bagaimana kombinasi usia lanjut dan pendidikan menengah ke bawah "
        "dapat memengaruhi tingkat kepatuhan minum obat. Kelompok lansia dengan pendidikan rendah "
        "cenderung memiliki tingkat non-adherent yang lebih tinggi, menjadikannya target utama "
        "untuk program edukasi kesehatan."
    )

# ── 2  Komunikasi vs Kepatuhan ───────────────────────────────────────────────
st.header("2. Potensi Intervensi Melalui Komunikasi", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Apakah pasien yang memiliki ponsel dan merespons pesan/panggilan "
    "dengan frekuensi tinggi memiliki kepatuhan lebih baik?"
)

comm_cols = [
    "Do you have a mobile phone",
    "How often do you receive text messages/alerts in a day",
    "How often do you answer phone calls in a day",
    "What is your preferred communication language",
]

tabs_comm = st.tabs(["Kepemilikan Ponsel", "Frekuensi SMS", "Frekuensi Telepon", "Bahasa Komunikasi"])

for tab, col in zip(tabs_comm, comm_cols):
    with tab:
        if col not in df.columns:
            st.info(f"Kolom '{col}' tidak ditemukan.")
            continue
        sub = df.dropna(subset=[col])
        if sub.empty:
            st.info("Tidak ada data setelah filter.")
            continue

        ct = _pct_crosstab(sub, col)
        col_l, col_r = st.columns(2)
        with col_l:
            vc = sub[col].value_counts().reset_index()
            vc.columns = [col, "Jumlah"]
            fig_vc = px.bar(vc, x=col, y="Jumlah", color=col, template="plotly_white")
            fig_vc.update_layout(showlegend=False, xaxis_title=col)
            st.plotly_chart(fig_vc, use_container_width=True)
        with col_r:
            fig_ct = px.bar(ct, x=col, y="Persentase", color="Adherence Level",
                            barmode="stack", template="plotly_white", text_auto=".1f")
            st.plotly_chart(fig_ct, use_container_width=True)

with st.expander("Insight Komunikasi", icon=":material/lightbulb:"):
    st.write(
        "Mayoritas responden memiliki ponsel dan aktif menerima SMS. "
        "Pasien dengan frekuensi komunikasi tinggi (Very Often) menunjukkan pola kepatuhan "
        "yang berbeda dibanding pasien yang jarang berkomunikasi. "
        "Temuan ini mendukung potensi implementasi SMS Gateway multi-bahasa sebagai "
        "sistem pengingat minum obat."
    )

# ── 3  Rutinitas & Caregiver ─────────────────────────────────────────────────
st.header("3. Rutinitas Harian dan Peran Pengasuh", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Bagaimana perbandingan kepatuhan antara pasien yang bekerja >12 jam "
    "dan mengurus sendiri vs yang dibantu keluarga?"
)

col_work = "How many hours do work in a day"
col_cg = "Who is your care giver"

col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Jam Kerja vs Kepatuhan")
    if col_work in df.columns:
        work_ct = _pct_crosstab(df.dropna(subset=[col_work]), col_work)
        fig_w = px.bar(work_ct, x=col_work, y="Persentase", color="Adherence Level",
                       barmode="group", template="plotly_white", text_auto=".1f")
        st.plotly_chart(fig_w, use_container_width=True)

with col_r:
    st.subheader("Caregiver vs Kepatuhan")
    if col_cg in df.columns:
        cg_ct = _pct_crosstab(df.dropna(subset=[col_cg]), col_cg)
        fig_cg = px.bar(cg_ct, x=col_cg, y="Persentase", color="Adherence Level",
                        barmode="stack", template="plotly_white", text_auto=".1f")
        st.plotly_chart(fig_cg, use_container_width=True)

# Heatmap: work × caregiver
st.subheader("Heatmap: Jam Kerja x Caregiver x Kepatuhan")
if col_work in df.columns and col_cg in df.columns:
    sub3 = df.dropna(subset=[col_work, col_cg])
    if not sub3.empty:
        heat = pd.crosstab([sub3[col_work], sub3[col_cg]], sub3[TARGET])
        heat_pct = heat.div(heat.sum(axis=1), axis=0) * 100
        heat_pct = heat_pct.reset_index()
        heat_melt = heat_pct.melt(id_vars=[col_work, col_cg], var_name="Level", value_name="Pct")
        heat_melt["combo"] = heat_melt[col_work] + " | " + heat_melt[col_cg]

        sel_level = st.selectbox("Pilih Level Kepatuhan", heat_melt["Level"].unique())
        subset_heat = heat_melt[heat_melt["Level"] == sel_level]
        pivot = subset_heat.pivot(index=col_cg, columns=col_work, values="Pct").fillna(0)
        fig_hm = px.imshow(pivot, text_auto=".1f", color_continuous_scale="RdYlGn_r",
                           template="plotly_white", aspect="auto")
        fig_hm.update_layout(xaxis_title="Jam Kerja", yaxis_title="Caregiver")
        st.plotly_chart(fig_hm, use_container_width=True)

with st.expander("Insight Rutinitas & Caregiver", icon=":material/lightbulb:"):
    st.write(
        "Pasien yang bekerja lebih dari 12 jam dan mengurus dirinya sendiri (Self) "
        "memiliki risiko non-adherent yang lebih tinggi dibandingkan mereka yang "
        "dibantu oleh keluarga (Spouse/Children). "
        "Hasil ini menjadi dasar untuk merancang panduan pelibatan keluarga (Family Support System)."
    )

# ── 4  Beban Resep ───────────────────────────────────────────────────────────
st.header("4. Beban Resep dan Alasan Konsumsi Obat", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Berapa peningkatan persentase Non-Adherent pada pasien >3 tablet/hari?"
)

col_drugs = "Number of drugs prescribed"
col_tabs = "How many tablets do you take in a day"
col_when = "When do you take your drugs"
col_why = "Why do you choose to take your drugs at that time"

tabs_rx = st.tabs(["Jumlah Obat", "Tablet per Hari", "Waktu Minum", "Alasan Waktu"])
rx_cols = [col_drugs, col_tabs, col_when, col_why]

for tab, col in zip(tabs_rx, rx_cols):
    with tab:
        if col not in df.columns:
            st.info(f"Kolom '{col}' tidak ditemukan.")
            continue
        sub = df.dropna(subset=[col])
        if sub.empty:
            continue

        cl, cr = st.columns(2)
        with cl:
            vc = sub[col].value_counts().reset_index()
            vc.columns = [col, "Jumlah"]
            fig_vc = px.bar(vc, x=col, y="Jumlah", color=col, template="plotly_white")
            fig_vc.update_layout(showlegend=False)
            st.plotly_chart(fig_vc, use_container_width=True)
        with cr:
            ct = _pct_crosstab(sub, col)
            fig_ct = px.bar(ct, x=col, y="Persentase", color="Adherence Level",
                            barmode="group", template="plotly_white", text_auto=".1f")
            st.plotly_chart(fig_ct, use_container_width=True)

with st.expander("Insight Beban Resep", icon=":material/lightbulb:"):
    st.write(
        "Pasien dengan beban obat tinggi (>3 tablet/hari) menunjukkan kecenderungan "
        "non-adherent yang lebih besar. Temuan ini menjadi dasar bagi dokter untuk "
        "mengevaluasi kemungkinan penyederhanaan regimen obat."
    )

# ── 5  Kondisi Kesehatan ─────────────────────────────────────────────────────
st.header("5. Kondisi Kesehatan Spesifik", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Kondisi kronis mana yang mencatatkan non-adherent tertinggi?"
)

hc_col = "Health Condition"
if hc_col in df.columns:
    sub5 = df.dropna(subset=[hc_col])
    top_hc = sub5[hc_col].value_counts().nlargest(5).index
    sub5 = sub5[sub5[hc_col].isin(top_hc)]

    col_l5, col_r5 = st.columns(2)
    with col_l5:
        st.subheader("Distribusi Kondisi Kesehatan (Top 5)")
        hc_vc = sub5[hc_col].value_counts().reset_index()
        hc_vc.columns = ["Kondisi", "Jumlah"]
        fig_hc = px.bar(hc_vc, y="Kondisi", x="Jumlah", orientation="h", template="plotly_white",
                        color="Jumlah", color_continuous_scale="Teal")
        fig_hc.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig_hc, use_container_width=True)

    with col_r5:
        st.subheader("Kepatuhan per Kondisi Kesehatan")
        hc_ct = _pct_crosstab(sub5, hc_col)
        fig_hc2 = px.bar(hc_ct, x=hc_col, y="Persentase", color="Adherence Level",
                         barmode="group", template="plotly_white", text_auto=".1f",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_hc2, use_container_width=True)

    # Duration on drugs
    dur_col = "How long have you been taking your drugs"
    if dur_col in df.columns:
        st.subheader("Durasi Pengobatan vs Kepatuhan")
        dur_ct = _pct_crosstab(df.dropna(subset=[dur_col]), dur_col)
        fig_dur = px.bar(dur_ct, x=dur_col, y="Persentase", color="Adherence Level",
                         barmode="stack", template="plotly_white", text_auto=".1f")
        st.plotly_chart(fig_dur, use_container_width=True)

with st.expander("Insight Kondisi Kesehatan", icon=":material/lightbulb:"):
    st.write(
        "Di antara kondisi kronis utama (Hipertensi, Diabetes, Glaukoma, Mental, HIV), "
        "terdapat variasi tingkat kepatuhan yang signifikan. "
        "Kelompok dengan non-adherent tertinggi harus mendapat prioritas dalam "
        "alokasi jam konseling tambahan."
    )

# ── 6  Pengetahuan, Persepsi, Perilaku ───────────────────────────────────────
st.header("6. Pengetahuan, Persepsi, dan Perilaku", divider="blue")
st.markdown(
    "**Pertanyaan SMART**: Seberapa besar korelasi Knowledge Level (Inadequate) dan "
    "Perception Level (Bad) terhadap probabilitas Non-Adherent?"
)

level_cols = ["PERCEPTION LEVEL", "BEHAVIOUR LEVEL", "KNOWLEDGE LEVEL"]
tabs_lvl = st.tabs(["Persepsi", "Perilaku", "Pengetahuan"])

for tab, col in zip(tabs_lvl, level_cols):
    with tab:
        if col not in df.columns:
            st.info(f"Kolom '{col}' tidak ditemukan.")
            continue
        sub = df.dropna(subset=[col])
        if sub.empty:
            st.info("Tidak ada data.")
            continue

        cl, cr = st.columns(2)
        with cl:
            vc = sub[col].value_counts().reset_index()
            vc.columns = [col, "Jumlah"]
            fig_vc = px.pie(vc, names=col, values="Jumlah", hole=0.4, template="plotly_white")
            st.plotly_chart(fig_vc, use_container_width=True)
        with cr:
            ct = _pct_crosstab(sub, col)
            fig_ct = px.bar(ct, x=col, y="Persentase", color="Adherence Level",
                            barmode="stack", template="plotly_white", text_auto=".1f")
            st.plotly_chart(fig_ct, use_container_width=True)

with st.expander("Insight Pengetahuan, Persepsi, dan Perilaku", icon=":material/lightbulb:"):
    st.write(
        "Pasien dengan Knowledge Level 'Inadequate' dan Perception Level 'Bad' "
        "memiliki probabilitas lebih tinggi untuk masuk ke kategori Non-Adherent. "
        "Temuan ini menjadi dasar untuk menentukan apakah anggaran promosi kesehatan "
        "harus difokuskan pada kampanye perbaikan pengetahuan atau intervensi perilaku."
    )
