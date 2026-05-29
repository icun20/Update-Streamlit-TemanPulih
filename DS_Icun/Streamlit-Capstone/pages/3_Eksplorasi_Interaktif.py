"""
Page 3 – Eksplorasi Data Interaktif
Dynamic scatter plots, crosstab builder, and correlation heatmaps.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Eksplorasi Interaktif",
    page_icon=":material/search:",
    layout="wide",
)

if "filtered_df" not in st.session_state:
    st.warning("Buka halaman utama terlebih dahulu agar data ter-load.")
    st.stop()

df = st.session_state["filtered_df"]

st.title("Eksplorasi Data Interaktif")
st.caption("Bangun visualisasi kustom dari dataset Multi-Dimensional Adherence")

tab_cross, tab_corr, tab_table = st.tabs(["Crosstab Builder", "Korelasi Numerik", "Tabel Data"])

# ── Tab 1: Crosstab Builder ──────────────────────────────────────────────────
with tab_cross:
    st.header("Crosstab Builder", divider="green")
    cat_cols = [c for c in df.select_dtypes(include=["object"]).columns if df[c].nunique() < 30]

    if len(cat_cols) < 2:
        st.info("Tidak cukup kolom kategorikal untuk crosstab.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            x_var = st.selectbox("Variabel Baris", cat_cols, index=0)
        with c2:
            y_var = st.selectbox("Variabel Kolom", cat_cols, index=min(1, len(cat_cols) - 1))

        if x_var and y_var and x_var != y_var:
            sub = df.dropna(subset=[x_var, y_var])
            ct = pd.crosstab(sub[x_var], sub[y_var])
            st.subheader("Tabel Crosstab (jumlah)")
            st.dataframe(ct, use_container_width=True)

            st.subheader("Heatmap")
            fig_hm = px.imshow(ct, text_auto=True, color_continuous_scale="Blues",
                               template="plotly_white", aspect="auto")
            st.plotly_chart(fig_hm, use_container_width=True)

            st.subheader("Persentase (normalisasi baris)")
            ct_pct = pd.crosstab(sub[x_var], sub[y_var], normalize="index") * 100
            ct_pct_melt = ct_pct.reset_index().melt(id_vars=x_var, var_name=y_var, value_name="Pct")
            fig_bar = px.bar(ct_pct_melt, x=x_var, y="Pct", color=y_var,
                             barmode="stack", template="plotly_white", text_auto=".1f")
            st.plotly_chart(fig_bar, use_container_width=True)
        elif x_var == y_var:
            st.warning("Pilih dua variabel yang berbeda.")

# ── Tab 2: Correlation Heatmap ───────────────────────────────────────────────
with tab_corr:
    st.header("Korelasi antar Variabel Numerik", divider="green")
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(num_cols) < 2:
        st.info("Tidak cukup kolom numerik untuk korelasi.")
    else:
        selected_num = st.multiselect(
            "Pilih variabel numerik (min 2)",
            num_cols,
            default=num_cols[:min(8, len(num_cols))],
        )
        if len(selected_num) >= 2:
            corr = df[selected_num].corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                                 template="plotly_white", aspect="auto", zmin=-1, zmax=1)
            fig_corr.update_layout(width=800, height=700)
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Pilih minimal 2 variabel.")

# ── Tab 3: Data Table ────────────────────────────────────────────────────────
with tab_table:
    st.header("Tabel Data Lengkap", divider="green")
    st.write(f"Menampilkan **{len(df)}** baris setelah filter global.")
    st.dataframe(df, use_container_width=True, height=600)
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="adherence_dataset_filtered.csv",
        mime="text/csv",
        icon=":material/download:",
    )
