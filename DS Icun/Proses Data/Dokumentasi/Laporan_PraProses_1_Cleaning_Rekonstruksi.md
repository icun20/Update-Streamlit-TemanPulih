# Dokumentasi Pra-Proses 1: Hyper-Robust Cleaning & Rekonstruksi

## 1. Pendahuluan
Tahap ini merupakan pembersihan tingkat lanjut yang tidak hanya menangani data kosong, tetapi juga menjaga integritas statistik dataset melalui standarisasi teks, penghapusan outlier, dan validasi logika.

## 2. Langkah Pembersihan Mendalam (Hyper-Robust)
*   **Standarisasi Teks Kategorikal**: Seluruh kolom Section A (Demografi) telah diubah menjadi huruf kapital dan dihapus spasi berlebihnya untuk menghindari redundansi kategori (misal: "Igbo" vs "igbo ").
*   **Imputasi Item-Level Global (44 Fitur)**: Mencakup Section B, C, D, dan **Section E (Persepsi Teknologi)**. Semua nilai kosong diisi dengan median (atau nilai netral 3 untuk Likert) guna mempertahankan daya prediksi maksimal.
*   **Penghapusan Outlier (Isolation Forest)**: Mengidentifikasi dan menghapus **21 responden** dengan pola jawaban yang sangat tidak wajar (pola acak). Data outlier ini disimpan terpisah di `dropped_outliers_multiclass.csv` untuk keperluan audit.
*   **Validasi Logika**: Pembersihan kolom `AGE` dan pengecekan konsistensi durasi pengobatan.

## 3. Rekonstruksi Sistem Multiclass
Membangun 4 pilar target untuk analisis sistemik:
*   `ADHERENCE_CLASS`: Target Utama (4 Tingkatan).
*   `KNOWLEDGE_CLASS`: 3 Tingkatan.
*   `BEHAVIOUR_CLASS`: 3 Tingkatan.
*   `PERCEPTION_CLASS`: 3 Tingkatan.

## 4. Hasil Audit Kualitas Data
| Indikator | Nilai |
|-----------|-------|
| Jumlah Data Awal | 609 |
| Outlier Dihapus | 21 |
| Responden Final | 588 |
| Fitur yang Diimputasi | 44 |

## 5. Distribusi Target Final (Post-Cleaning)
| Kelas | Kategori | Jumlah |
|-------|----------|--------|
| 0 | High Adherent | 4 |
| 1 | Low Adherent | 104 |
| 2 | Medium Adherent | 465 |
| 3 | High Non-Adherent | 15 |

---
**Status: Selesai Hyper-Robust Cleaning**
**Dibuat pada: 2026-05-16**
