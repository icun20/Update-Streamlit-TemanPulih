# Laporan Analisis Awal - Multiclass Adherence Capstone

## 1. Pendahuluan
Proyek ini bertujuan untuk membangun model Deep Learning (MLP) untuk memprediksi tingkat kepatuhan pengobatan pasien menggunakan pendekatan **Multiclass Classification**. Dataset terdiri dari 609 responden dengan fitur demografis dan psikometrik.

## 2. Definisi Target Multiclass
Berdasarkan kuesioner asli, target dibagi menjadi 4 tingkatan kepatuhan:

| Label | Kategori | Kriteria Skor (Section D) |
|-------|----------|--------------------------|
| 0 | **HIGH ADHERENT** | Skor 0 (Patuh Sempurna) |
| 1 | **LOW ADHERENT** | Skor 1 - 2 (Sedikit Lalai) |
| 2 | **MEDIUM ADHERENT** | Skor 3 - 6 (Sering Lalai) |
| 3 | **HIGH NON-ADHERENT** | Skor 7 - 8 (Sangat Tidak Patuh) |

## 3. Strategi Penanganan Data Kosong
Ditemukan bahwa ~37% data label di dataset asli kosong. Untuk memaksimalkan data pelatihan (609 baris), akan dilakukan langkah berikut:
*   **Imputasi Level Item**: Mengisi jawaban kosong pada pertanyaan individual (Q19-Q39).
*   **Kalkulasi Ulang**: Menghitung skor total secara manual untuk menghasilkan label multiclass bagi seluruh responden.

## 4. Rencana EDA (Exploratory Data Analysis)
Langkah EDA selanjutnya akan berfokus pada:
*   Distribusi frekuensi ke-4 kelas kepatuhan.
*   Korelasi fitur demografis (Usia, Pendidikan) terhadap tingkatan kepatuhan.
*   Analisis klaster untuk melihat profil psikologis tiap tingkatan.

---
**Dokumentasi dibuat pada: 2026-05-16**
**Status: Selesai Analisis Awal**
