# Pemetaan Kolom Kuesioner ke Fitur Dataset (Final)

Dokumen ini menjelaskan hubungan antara nama kolom deskriptif di dataset hasil cleaning dengan pertanyaan asli dalam kuesioner.

## Bagian B: Persepsi & Memori (Fitur Input)
| Nama Kolom | Pertanyaan |
|------------|------------|
| B1_ChangeMind_Decision | Seberapa sering Anda berubah pikiran terhadap keputusan yang sudah dibuat? |
| B1_ChangeMind_Convince | Seberapa sering Anda berubah pikiran jika diyakinkan/dimotivasi? |
| B1_AcceptSuggestion | Seberapa sering Anda menerima saran dari tenaga kesehatan? |
| B2_ForgetPlan | Seberapa sering Anda lupa melakukan apa yang baru saja direncanakan? |
| B2_ForgetTold | Seberapa sering Anda lupa sesuatu yang baru saja diberitahukan? |
| B2_MissAppointment | Seberapa sering Anda melewatkan janji temu jika tidak diingatkan? |
| B_CauseOfMissing | Apa alasan utama Anda melewatkan obat? (Lupa, Pekerjaan, dll) |
| B_ReminderMethod | Apa yang biasanya mengingatkan Anda waktu minum obat? |

## Bagian C: Keyakinan & Pengetahuan (Fitur Input)
| Nama Kolom | Pertanyaan |
|------------|------------|
| C1_DrugHelp | Apakah Anda percaya obat dapat membantu situasi Anda? |
| C1_DrugBurdensome | Apakah meminum obat terasa membebani? |
| C1_DrugInadequate | Apakah obat saja tidak cukup? |
| C2_AwareBeforeDiag | Apakah Anda menyadari penyakit tersebut sebelum didiagnosa? |
| C2_AwareLifestyle | Apakah Anda sadar penyakit tersebut memerlukan perubahan gaya hidup? |
| C2_AwareProlonged | Apakah Anda sadar penyakit tersebut memerlukan pengobatan jangka panjang? |

## Bagian D: Kepatuhan (Target Utama)
| Nama Kolom | Pertanyaan |
|------------|------------|
| D_ForgetPrescribed | Apakah Anda terkadang lupa minum obat sesuai resep? |
| D_FailOtherReasons | Pernahkah Anda gagal minum obat karena alasan selain lupa? |
| D_StopIfWorse | Pernahkah Anda berhenti minum obat karena merasa lebih buruk? |
| D_ForgetTravel | Saat bepergian, apakah Anda terkadang lupa membawa obat? |
| D_TakeAllYesterday | Apakah Anda meminum seluruh obat yang diresepkan kemarin? |
| D_StopIfFeelBetter | Saat gejala terkontrol, apakah Anda terkadang berhenti minum obat? |
| D_FeelHassled | Apakah meminum obat setiap hari terasa merepotkan? |
| D_DifficultyRemember | Seberapa sering Anda kesulitan mengingat untuk meminum obat? |

## Bagian E: Persepsi Teknologi (Fitur Input)
| Nama Kolom | Deskripsi Fitur |
|------------|-----------------|
| E_ForgetGeneral | Persepsi terhadap kelalaian minum obat secara umum |
| E_AwareForgetDetails | Kesadaran akan kemungkinan lupa waktu/dosis |
| E_DangerNoAdvice | Bahaya meminum obat tanpa saran dokter |
| E_BenefitAlerts | Manfaat pesan pengingat (SMS/Voice) |
| E_BenefitPersuasive | Manfaat pesan motivasi/edukasi |
| E_BenefitRiskExpl | Manfaat penjelasan risiko melalui aplikasi |
| E_BenefitGainExpl | Manfaat penjelasan keuntungan melalui aplikasi |
| E_CostBenefitMobile | Efektivitas biaya layanan aplikasi mobile |
| E_AdaptVoiceSMS | Kesediaan nakes/pasien menggunakan IVR/SMS |
| E_EnableDiscussion | Aplikasi memungkinkan diskusi dengan nakes |
| E_PersonalAcceptance | Penerimaan pribadi terhadap layanan aplikasi mobile |

---
**Catatan**: Seluruh kolom `Unnamed` dan `TOTAL` yang tidak konsisten telah dihapus untuk memastikan data "High-Signal" bagi model Deep Learning.
