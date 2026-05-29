# Kamus Data Komprehensif - Multiclass Adherence Dataset

Dokumen ini memberikan pemetaan mendetail antara kolom dataset Excel dan kuesioner asli, termasuk definisi target multiclass.

## 1. Bagian A: Demografi (Fitur Input)

| Indeks | Nama Kolom | Pertanyaan Kuesioner | Tipe | Opsi / Rentang Nilai |
|--------|------------|----------------------|------|----------------------|
| 1 | GENDER | 1. Jenis Kelamin | str | male, female |
| 2 | AGE | 2. Usia | str | 21, 21-31, 31-40, 41-50, Above 50 |
| 3 | Marital Status | 3. Status Pernikahan | str | single, married, Divorced, widow/widower |
| 4 | Religion Affiliation | 4. Afiliasi Agama | str | Christianity, Islam, Others |
| 5 | Educational Attainment | 5. Pendidikan Terakhir | str | None, FLSC, WASC/SSCE, NCE/ND/HND, University, PG |
| 6 | Occupation | 6. Pekerjaan | str | Farmer, Trader, Professional, Artisan, Student, Retirees |
| 7 | How many hours worked | 7. Jam kerja per hari | str | 4, 8, 12, 16, 20, 24 hours |
| 8 | Who is your care giver | 8. Pengasuh | str | Spouse, Parent, Children, Relatives, Others |
| 9 | Do you have a mobile phone | 9. Kepemilikan HP | str | Yes, No |
| 10 | How often receive SMS | 10. Frekuensi SMS | str | Very Often, Quite Often, Sometimes, Rarely, Never |
| 11 | How often answer calls | 11. Frekuensi Telepon | str | Very Often, Quite Often, Sometimes, Rarely, Never |
| 12 | Preferred language | 12. Bahasa Pilihan | str | Igbo, Hausa, English, etc. |
| 13 | Health Condition | 13. Kondisi Kesehatan | str | Hypertension, HIV, Mental, Diabetes, etc. |
| 14 | How long taking drugs | 14. Durasi Pengobatan | str | <4 months, 4-6, 7-9, 10-12, >1 year |
| 15 | Number of drugs | 15. Jumlah Obat | str | One, Two, Three, Above three |
| 16 | Tablets per day | 16. Tablet per hari | str | One, Two, Three, Above three |

## 2. Bagian B: Persepsi & Memori (Fitur Input)
Skala Likert (1-5): 1 = Very Often, 5 = Never.

| Indeks | Kolom | Deskripsi Pertanyaan |
|--------|-------|----------------------|
| 19-21 | 19, 20, 21 | Persepsi terhadap pengambilan keputusan |
| 24-26 | 22, 23, 24 | Seberapa sering pasien lupa terkait pengobatan |

## 3. Bagian C: Keyakinan & Pengetahuan (Fitur Input)
Skala Likert (1-5).

| Indeks | Kolom | Deskripsi Pertanyaan |
|--------|-------|----------------------|
| 31-43 | 25 - 29 | Keyakinan terhadap efektivitas obat |
| 47-49 | 30, 31, 32 | Pengetahuan tentang dosis dan waktu |

## 4. Bagian D: Kepatuhan (Target Utama)
Digunakan untuk membentuk label Multiclass Adherence.

| Indeks | Kolom | Pertanyaan |
|--------|-------|------------|
| 50 | 33 | Lupa minum obat? |
| 51 | 34 | Gagal minum obat karena alasan lain? |
| 52 | 35 | Mengurangi/berhenti saat merasa buruk? |
| 53 | 36 | Lupa bawa obat saat bepergian? |
| 54 | 37 | Minum semua obat kemarin? |
| 55 | 38 | Berhenti saat merasa sehat? |
| 56 | 39 | Merasa terganggu dengan rencana pengobatan? |

## 5. Definisi Kelas Target (Multiclass)

### ADHERENCE_LEVEL (Target Utama)
Dihitung dari jumlah jawaban "Negatif" pada Bagian D.
*   **0: HIGH ADHERENT** (Skor 0)
*   **1: LOW ADHERENT** (Skor 1-2)
*   **2: MEDIUM ADHERENT** (Skor 3-6)
*   **3: HIGH NON-ADHERENT** (Skor 7-8)

### KNOWLEDGE_LEVEL
*   **INADEQUATE**: Skor 3-5
*   **MODERATE**: Skor 6-10
*   **GOOD**: Skor 11-15

### BEHAVIOUR_LEVEL
*   **NOT FORGETFUL**: Skor 0-2
*   **FORGETFUL**: Skor 3-6
*   **MODERATELY FORGETFUL**: Skor 7-9
*   **HIGHLY FORGETFUL**: Skor 10-12
