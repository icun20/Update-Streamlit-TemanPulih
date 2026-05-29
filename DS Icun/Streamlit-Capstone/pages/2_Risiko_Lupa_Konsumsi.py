"""
Page 2 – Risiko Lupa Konsumsi Obat & Kebutuhan Reminder
Based on EDA_Lupa_Konsumsi_Obat.ipynb – expanded comprehensively.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Risiko Lupa Konsumsi",
    page_icon=":material/notifications_active:",
    layout="wide",
)

# ── data ─────────────────────────────────────────────────────────────────────
if "filtered_df" not in st.session_state:
    st.warning("Buka halaman utama terlebih dahulu agar data ter-load.")
    st.stop()

df = st.session_state["filtered_df"]
TARGET = "NON ADHERENT LEVEL"

st.title("Risiko Lupa Konsumsi Obat & Kebutuhan Reminder")
st.caption("Sumber: EDA_Lupa_Konsumsi_Obat – diperluas dengan visualisasi komprehensif")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Proporsi Pasien yang Lupa Minum Obat
# ═══════════════════════════════════════════════════════════════════════════════
st.header("1. Proporsi Pasien yang Pernah Lupa Minum Obat", divider="orange")

forget_col = [c for c in df.columns if "Q33:" in c]
if forget_col:
    fc = forget_col[0]
    sub = df.dropna(subset=[fc])
    sub[fc] = pd.to_numeric(sub[fc], errors="coerce")

    # 0 = No, 1 = Yes
    val_counts = sub[fc].value_counts().reset_index()
    val_counts.columns = ["Nilai", "Jumlah"]

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Apakah kadang lupa minum obat sesuai resep?")
        st.markdown("Skala: 0 = Tidak Pernah, 1 = Ya/Pernah")
        fig = px.pie(val_counts, names="Nilai", values="Jumlah", hole=0.4,
                     template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Distribusi Jawaban (Bar)")
        fig2 = px.bar(val_counts, x="Nilai", y="Jumlah", color="Nilai",
                      template="plotly_white", text_auto=True)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("Insight", icon=":material/lightbulb:"):
        total = sub[fc].notna().sum()
        pernah = (sub[fc] >= 1).sum()
        st.write(
            f"Dari {total} responden yang menjawab, **{pernah} ({pernah/total*100:.1f}%)** "
            f"mengaku pernah lupa minum obat sesuai resep. "
            "Ini menegaskan besarnya kebutuhan akan sistem pengingat digital."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Kesulitan Mengingat Jadwal
# ═══════════════════════════════════════════════════════════════════════════════
st.header("2. Kesulitan Mengingat Jadwal Konsumsi Obat", divider="orange")

difficulty_col = [c for c in df.columns if "Q40:" in c]
if difficulty_col:
    dc = difficulty_col[0]
    sub2 = df.dropna(subset=[dc])

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        st.subheader("Distribusi Tingkat Kesulitan")
        vc2 = sub2[dc].value_counts().sort_index().reset_index()
        vc2.columns = ["Tingkat Kesulitan", "Jumlah"]
        fig3 = px.bar(vc2, x="Tingkat Kesulitan", y="Jumlah",
                      color="Tingkat Kesulitan", template="plotly_white", text_auto=True)
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        st.subheader("Kesulitan per Kelompok Usia")
        sub2_age = sub2.dropna(subset=["AGE"])
        sub2_age[dc] = pd.to_numeric(sub2_age[dc], errors="coerce")
        if not sub2_age.empty:
            agg = sub2_age.groupby("AGE")[dc].mean().reset_index()
            agg.columns = ["Usia", "Rata-rata Kesulitan"]
            fig4 = px.bar(agg, x="Usia", y="Rata-rata Kesulitan", color="Usia",
                          template="plotly_white", text_auto=".2f")
            fig4.update_layout(showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)

    with st.expander("Insight", icon=":material/lightbulb:"):
        st.write(
            "Variabel kesulitan mengingat obat (difficulty_remembering_drug) menunjukkan "
            "distribusi yang bervariasi antar kelompok usia. "
            "Kelompok usia lanjut cenderung memiliki skor rata-rata kesulitan yang lebih tinggi."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Penyebab Melewatkan Obat
# ═══════════════════════════════════════════════════════════════════════════════
st.header("3. Penyebab Paling Umum Melewatkan Konsumsi Obat", divider="orange")

reason_col = [c for c in df.columns if "Q25:" in c]
if reason_col:
    rc = reason_col[0]
    sub3 = df.dropna(subset=[rc])
    sub3[rc] = sub3[rc].astype(str).str.strip()
    vc3 = sub3[rc].value_counts().nlargest(10).reset_index()
    vc3.columns = ["Alasan", "Jumlah"]

    fig5 = px.bar(vc3, y="Alasan", x="Jumlah", orientation="h",
                  template="plotly_white", color="Jumlah", color_continuous_scale="Oranges")
    fig5.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Insight", icon=":material/lightbulb:"):
        st.write(
            "Alasan paling umum melewatkan obat meliputi: merasa lebih baik (felt better), "
            "lupa (simply forget), alasan pekerjaan (work related), dan terlambat diingatkan "
            "(missed reminder). Temuan ini menggarisbawahi pentingnya sistem pengingat aktif."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Sumber Pengingat Obat
# ═══════════════════════════════════════════════════════════════════════════════
st.header("4. Sumber Pengingat Obat yang Paling Sering Digunakan", divider="orange")

reminder_col = [c for c in df.columns if "Q26:" in c]
if reminder_col:
    rmc = reminder_col[0]
    sub4 = df.dropna(subset=[rmc])
    sub4[rmc] = sub4[rmc].astype(str).str.strip()
    vc4 = sub4[rmc].value_counts().nlargest(10).reset_index()
    vc4.columns = ["Sumber Pengingat", "Jumlah"]

    col_l4, col_r4 = st.columns(2)
    with col_l4:
        fig6 = px.bar(vc4, y="Sumber Pengingat", x="Jumlah", orientation="h",
                      template="plotly_white", color="Jumlah", color_continuous_scale="Blues")
        fig6.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig6, use_container_width=True)

    with col_r4:
        fig7 = px.pie(vc4, names="Sumber Pengingat", values="Jumlah", hole=0.4,
                      template="plotly_white")
        fig7.update_traces(textinfo="percent+label")
        st.plotly_chart(fig7, use_container_width=True)

    with st.expander("Insight", icon=":material/lightbulb:"):
        st.write(
            "Mayoritas pasien mengandalkan diri sendiri (self) sebagai pengingat obat. "
            "Hanya sebagian kecil yang menggunakan pengingat eksternal seperti alarm, "
            "keluarga, atau petugas kesehatan. Ini menunjukkan gap besar yang bisa diisi "
            "oleh teknologi pengingat digital (SMS/IVR)."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Beban Obat vs Kebutuhan Reminder
# ═══════════════════════════════════════════════════════════════════════════════
st.header("5. Beban Obat vs Kebutuhan Reminder", divider="orange")

if "reminder_need_segment" in df.columns:
    col_l5, col_r5 = st.columns(2)

    with col_l5:
        st.subheader("Distribusi Segmen Kebutuhan Reminder")
        seg = df["reminder_need_segment"].value_counts().reset_index()
        seg.columns = ["Segmen", "Jumlah"]
        color_map = {"Tinggi": "#e74c3c", "Sedang": "#f39c12", "Rendah": "#2ecc71", "Unknown": "#95a5a6"}
        fig8 = px.pie(seg, names="Segmen", values="Jumlah", hole=0.45,
                      template="plotly_white", color="Segmen", color_discrete_map=color_map)
        fig8.update_traces(textinfo="percent+label")
        st.plotly_chart(fig8, use_container_width=True)

    with col_r5:
        st.subheader("Skor Kebutuhan Reminder (Histogram)")
        if "reminder_need_score" in df.columns:
            fig9 = px.histogram(df.dropna(subset=["reminder_need_score"]),
                                x="reminder_need_score", nbins=20, template="plotly_white",
                                color_discrete_sequence=["#3498db"])
            fig9.update_layout(xaxis_title="Skor Kebutuhan Reminder", yaxis_title="Frekuensi")
            st.plotly_chart(fig9, use_container_width=True)

    # Breakdown by demographics
    st.subheader("Segmen Reminder berdasarkan Usia")
    age_seg = pd.crosstab(df["AGE"], df["reminder_need_segment"], normalize="index") * 100
    age_seg = age_seg.reset_index().melt(id_vars="AGE", var_name="Segmen", value_name="Persentase")
    fig10 = px.bar(age_seg, x="AGE", y="Persentase", color="Segmen",
                   color_discrete_map=color_map, barmode="stack", template="plotly_white", text_auto=".1f")
    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("Segmen Reminder berdasarkan Gender")
    gen_seg = pd.crosstab(df["GENDER"], df["reminder_need_segment"], normalize="index") * 100
    gen_seg = gen_seg.reset_index().melt(id_vars="GENDER", var_name="Segmen", value_name="Persentase")
    fig11 = px.bar(gen_seg, x="GENDER", y="Persentase", color="Segmen",
                   color_discrete_map=color_map, barmode="stack", template="plotly_white", text_auto=".1f")
    st.plotly_chart(fig11, use_container_width=True)

    # By drug count
    drug_col = "Number of drugs prescribed"
    if drug_col in df.columns:
        st.subheader("Segmen Reminder berdasarkan Jumlah Obat")
        drug_seg = pd.crosstab(df[drug_col], df["reminder_need_segment"], normalize="index") * 100
        drug_seg = drug_seg.reset_index().melt(id_vars=drug_col, var_name="Segmen", value_name="Persentase")
        fig12 = px.bar(drug_seg, x=drug_col, y="Persentase", color="Segmen",
                       color_discrete_map=color_map, barmode="stack", template="plotly_white", text_auto=".1f")
        st.plotly_chart(fig12, use_container_width=True)

    with st.expander("Insight", icon=":material/lightbulb:"):
        st.write(
            "Pasien dengan beban obat lebih tinggi (Above three) menunjukkan proporsi "
            "segmen reminder 'Tinggi' yang lebih besar. Usia lanjut (Above 50) juga "
            "memiliki kecenderungan kebutuhan reminder yang lebih tinggi. "
            "Ini mendukung implementasi sistem pengingat yang ditargetkan pada "
            "kelompok berisiko tinggi."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Caregiver & Mobile Phone untuk Reminder Digital
# ═══════════════════════════════════════════════════════════════════════════════
st.header("6. Caregiver & Akses Mobile Phone untuk Reminder Digital", divider="orange")

mobile_col = "Do you have a mobile phone"
cg_col = "Who is your care giver"

col_l6, col_r6 = st.columns(2)

with col_l6:
    st.subheader("Kepemilikan Ponsel")
    if mobile_col in df.columns:
        mob = df[mobile_col].value_counts().reset_index()
        mob.columns = ["Status", "Jumlah"]
        fig13 = px.pie(mob, names="Status", values="Jumlah", hole=0.4,
                       template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set3)
        fig13.update_traces(textinfo="percent+label")
        st.plotly_chart(fig13, use_container_width=True)

with col_r6:
    st.subheader("Distribusi Caregiver")
    if cg_col in df.columns:
        cg = df[cg_col].value_counts().reset_index()
        cg.columns = ["Caregiver", "Jumlah"]
        fig14 = px.bar(cg, y="Caregiver", x="Jumlah", orientation="h",
                       template="plotly_white", color="Jumlah", color_continuous_scale="Purples")
        fig14.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig14, use_container_width=True)

# Cross: Mobile × Caregiver × Reminder Segment
if "reminder_need_segment" in df.columns and mobile_col in df.columns and cg_col in df.columns:
    st.subheader("Ponsel x Caregiver x Segmen Reminder")
    sub6 = df.dropna(subset=[mobile_col, cg_col, "reminder_need_segment"])
    if not sub6.empty:
        ct6 = pd.crosstab([sub6[mobile_col], sub6[cg_col]], sub6["reminder_need_segment"],
                          normalize="index") * 100
        ct6 = ct6.reset_index()
        ct6["Kombinasi"] = ct6[mobile_col].astype(str) + " | " + ct6[cg_col].astype(str)
        ct6_melt = ct6.drop(columns=[mobile_col, cg_col]).melt(
            id_vars="Kombinasi", var_name="Segmen", value_name="Persentase"
        )
        fig15 = px.bar(ct6_melt, x="Kombinasi", y="Persentase", color="Segmen",
                       color_discrete_map=color_map, barmode="stack", template="plotly_white",
                       text_auto=".1f")
        fig15.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig15, use_container_width=True)

# Acceptance of mobile app
accept_col = [c for c in df.columns if "Q51:" in c]
if accept_col:
    ac = accept_col[0]
    st.subheader("Penerimaan terhadap Mobile App Service")
    acc = df[ac].value_counts().reset_index()
    acc.columns = ["Jawaban", "Jumlah"]
    fig16 = px.pie(acc, names="Jawaban", values="Jumlah", hole=0.4,
                   template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig16.update_traces(textinfo="percent+label")
    st.plotly_chart(fig16, use_container_width=True)

with st.expander("Insight", icon=":material/lightbulb:"):
    st.write(
        "Mayoritas responden memiliki ponsel, yang menjadi modal utama implementasi "
        "reminder digital. Caregiver terbanyak adalah Spouse dan Children, "
        "yang bisa dilibatkan dalam sistem family monitoring. "
        "Tingginya penerimaan terhadap mobile app service memperkuat justifikasi "
        "pengembangan aplikasi pengingat obat."
    )
