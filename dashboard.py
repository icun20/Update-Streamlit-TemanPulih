import streamlit as st
import pandas as pd
import plotly.express as px
import os

from data_loader import load_and_transform_data

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Kepatuhan Obat",
    page_icon=":material/medical_services:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main .block-container {padding-top: 1.5rem;}
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data Loading ─────────────────────────────────────────────────────────────
DATASET_NAME = "MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA.xlsx"


@st.cache_data
def get_data():
    candidates = [
        DATASET_NAME,
        os.path.join(os.path.dirname(__file__), DATASET_NAME),
    ]
    for path in candidates:
        if os.path.exists(path):
            return load_and_transform_data(path)
    st.error("Dataset tidak ditemukan. Pastikan file Excel ada di direktori proyek.")
    st.stop()


df = get_data()

# ── Shared State ─────────────────────────────────────────────────────────────
# Store the dataframe in session_state so pages can access it
st.session_state["df"] = df

# ── Sidebar Global Filters ───────────────────────────────────────────────────
st.sidebar.header("Filter Global", divider="gray")
sel_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(map(str, df["GENDER"].dropna().unique())),
    default=sorted(map(str, df["GENDER"].dropna().unique())),
)
sel_age = st.sidebar.multiselect(
    "Kelompok Usia",
    options=sorted(map(str, df["AGE"].dropna().unique())),
    default=sorted(map(str, df["AGE"].dropna().unique())),
)

filtered = df[df["GENDER"].isin(sel_gender) & df["AGE"].isin(sel_age)]
st.session_state["filtered_df"] = filtered

# ── Overview Page ────────────────────────────────────────────────────────────
st.title("Overview Dataset")
st.caption("MULTI DIMENSIONAL ADHERENCE DATASET IN SOUTHEAST NIGERIA")

# Key metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric(label="Total Responden", value=len(filtered))
c2.metric(label="Total Kolom", value=len(filtered.columns))
female_pct = round((filtered["GENDER"] == "female").mean() * 100, 1)
c3.metric(label="Responden Wanita", value=f"{female_pct}%")
target_col = "NON ADHERENT LEVEL"
valid_labels = filtered[target_col].notna().sum() if target_col in filtered.columns else 0
c4.metric(label="Label Kepatuhan Valid", value=valid_labels)

st.divider()

# Demographics
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Distribusi Kelompok Usia")
    age_c = filtered["AGE"].value_counts().reset_index()
    age_c.columns = ["Usia", "Jumlah"]
    fig = px.bar(age_c, x="Usia", y="Jumlah", color="Usia", template="plotly_white")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("Tingkat Pendidikan")
    edu_c = filtered["Educational Attainment"].value_counts().reset_index()
    edu_c.columns = ["Pendidikan", "Jumlah"]
    fig2 = px.pie(edu_c, names="Pendidikan", values="Jumlah", hole=0.4, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

col_l2, col_r2 = st.columns(2)

with col_l2:
    st.subheader("Distribusi Gender")
    gen_c = filtered["GENDER"].value_counts().reset_index()
    gen_c.columns = ["Gender", "Jumlah"]
    fig3 = px.pie(gen_c, names="Gender", values="Jumlah", hole=0.4, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

with col_r2:
    st.subheader("Kondisi Kesehatan Utama")
    hc = "Health Condition"
    if hc in filtered.columns:
        hc_c = filtered[hc].value_counts().nlargest(6).reset_index()
        hc_c.columns = ["Kondisi", "Jumlah"]
        fig4 = px.bar(hc_c, y="Kondisi", x="Jumlah", orientation="h", template="plotly_white", color="Jumlah", color_continuous_scale="Blues")
        fig4.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Tabel Data (100 baris pertama)")
st.dataframe(filtered.head(100), use_container_width=True, height=400)
