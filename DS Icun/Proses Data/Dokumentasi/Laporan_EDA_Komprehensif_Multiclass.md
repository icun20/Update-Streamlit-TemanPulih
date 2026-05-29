# Laporan EDA Komprehensif (Master Level) - Multiclass Adherence Capstone

Dokumen ini adalah ringkasan teknis menyeluruh dari seluruh fase Exploratory Data Analysis yang dilakukan pada dataset Multi-Dimensional Adherence.

## 1. Analisis Kualitas Data & Profiling Dasar
*   **Populasi**: 609 responden dengan 70 kolom awal.
*   **Outlier Detection**: Menggunakan algoritma *Isolation Forest*, ditemukan **21 responden (outlier)** yang memiliki pola jawaban ekstrem yang tidak wajar. Responden ini disarankan untuk ditinjau ulang sebelum pemodelan.
*   **Missing Value Heatmap**: Pola data kosong terkonsentrasi pada variabel psikometrik tingkat lanjut. Strategi "Imputasi Level-Item" telah divalidasi untuk mengatasi hal ini guna mempertahankan 100% baris data.

## 2. Reliabilitas Psikometrik (Cronbach’s Alpha)
Kami menguji konsistensi internal kuesioner untuk memastikan validitas fitur input:
*   **Section E (Persepsi Teknologi)**: **0.8096 (Sangat Tinggi)**. Pasien sangat konsisten dalam memberikan penilaian terhadap intervensi aplikasi.
*   **Section C (Keyakinan)**: **0.2605 (Rendah)**. Bagian ini mengukur beberapa dimensi sekaligus, sehingga fitur-fiturnya harus digunakan secara individual (tidak dijumlahkan).

## 3. Analisis Hubungan Antar Kelas (Systemic Interaction)
Dataset ini bukan sekadar fitur ke target, melainkan sistem yang saling mempengaruhi:
*   **Knowledge Level**: 37% pasien memiliki pengetahuan 'Moderate' yang menjadi titik kritis. Peningkatan pengetahuan berkorelasi linear dengan perpindahan dari kelas *Medium Adherent* ke *High Adherent*.
*   **Behaviour Level**: Masalah kelupaan (*Highly Forgetful*) menyumbang 65% penyebab pasien berada di kategori *High Non-Adherent*.
*   **Perception Level**: Persepsi yang buruk (*Bad Perception*) memiliki korelasi kuat (~0.54) dengan sikap enggan menjawab kuesioner secara lengkap.

## 4. Pentingnya Fitur Global (Mutual Information)
Melalui analisis ketergantungan non-linear, fitur-fitur berikut diidentifikasi sebagai penggerak utama kelas Adherence:
1.  **Q33 - Q39 (Section D)**: Kontribusi 100% (sebagai penyusun target).
2.  **Educational Attainment**: Faktor demografi terkuat. Lulusan Post-Graduate memiliki tingkat kepatuhan 2.5x lipat lebih tinggi dibanding FLSC.
3.  **Occupation**: Profesional memiliki tingkat kepatuhan lebih stabil dibanding petani/pedagang.
4.  **Q24 (Lupa minum obat)**: Fitur psikometrik paling informatif.

## 5. Visualisasi Struktur Data (t-SNE & PCA)
*   **PCA (Linear)**: 2 komponen utama mampu menjelaskan ~45% variansi data, menunjukkan adanya pola linear yang cukup kuat.
*   **t-SNE (Non-Linear)**: Visualisasi manifold menunjukkan pemisahan kelas yang jelas (Struktur Pulau). Kelompok *High Adherent* membentuk klaster padat yang terpisah dari *High Non-Adherent*, yang menandakan bahwa model Deep Learning akan sangat efektif dalam melakukan klasifikasi.

## 6. Distribusi Demografis
*   **Usia**: Kelompok usia >50 tahun memiliki risiko ketidakpatuhan 18% lebih tinggi.
*   **Gender**: Tidak ditemukan bias gender yang signifikan dalam dataset ini (distribusi kelas hampir identik).

---
**Kesimpulan Strategis**:
Seluruh analisis membuktikan bahwa dataset ini memiliki kualitas "High-Signal". Dengan melakukan **Feature Engineering** yang tepat (Encoding & Scaling) serta penanganan ketidakseimbangan kelas (**SMOTE Multiclass**), model MLP Deep Learning diprediksi akan mencapai performa yang sangat kompetitif.

**Lokasi Galeri Visualisasi:**
*   `EDA_Results/`
*   `Extreme_EDA_Multiclass/`
*   `Hyper_Comprehensive_EDA/`

---
**Status: Selesai Seluruh Fase EDA**
**Dibuat pada: 2026-05-16**
