# Laporan Feature Engineering Ekstrem Komprehensif (Multiclass)

## 1. Filosofi & Strategi Transformasi
Tahap ini bertujuan untuk mengubah data mentah yang bersifat campuran (teks & angka) menjadi matriks numerik murni yang optimal untuk arsitektur **Multi-Layer Perceptron (MLP)**.

### A. One-Hot Encoding (Variabel Kategorikal)
Variabel nominal diekspansi untuk menghindari bias ordinal. Dari **18** variabel kategori asli, dihasilkan **142** fitur biner baru.

#### Tabel Pemetaan Ekspansi (Mapping):
| Variabel Asal | Jumlah Fitur Baru | Contoh Fitur |
|---------------|-------------------|--------------|
| GENDER | 2 | `GENDER_FEMALE` |
| AGE | 9 | `AGE_21` |
| Marital Status | 5 | `Marital Status_DIVORCED` |
| Religion Affiliation | 4 | `Religion Affiliation_CHRISTIANITY` |
| Educational Attainment | 8 | `Educational Attainment_FLSC` |
| Occupation | 12 | `Occupation_ARTISAN` |
| How many hours do work in a day | 8 | `How many hours do work in a day_12 HOURS` |
| Who is your care giver | 8 | `Who is your care giver_CHILDREN` |
| Do you have a mobile phone | 3 | `Do you have a mobile phone_NO` |
| How often do you receive text messages/alerts in a day | 6 | `How often do you receive text messages/alerts in a day_NEVER` |
| How often do you answer phone calls in a day | 6 | `How often do you answer phone calls in a day_NEVER` |
| What is your preferred communication language | 6 | `What is your preferred communication language_ENGLISH` |
| Health Condition | 23 | `Health Condition_ASTHMA` |
| How long have you been taking your drugs | 7 | `How long have you been taking your drugs_10-12  MONTHS` |
| Number of drugs prescribed | 6 | `Number of drugs prescribed_ABOVE THREE` |
| How many tablets do you take in a day | 8 | `How many tablets do you take in a day_6` |
| When do you take your drugs | 15 | `When do you take your drugs_AFTER LUNCH` |
| Why do you choose to take your drugs at that time | 6 | `Why do you choose to take your drugs at that time_AFTER MEAL` |

### B. Standard Scaling (Variabel Numerik)
Menggunakan rumus `z = (x - u) / s`. Seluruh fitur kuesioner (Skala Likert 1-5) kini memiliki rata-rata 0 dan standar deviasi 1. Ini mencegah fitur dengan rentang besar mendominasi proses pembelajaran.

## 2. Analisis Struktur Data Final
*   **Total Fitur Input**: 175
*   **Sparsity Index**: 0.6898 (Menunjukkan kepadatan data biner setelah encoding)
*   **Memory Usage**: 2563.13 KB

## 3. Penyeimbangan Kelas (SMOTE Multiclass)
Karena Kelas 0 (High Adherent) hanya memiliki 4 data asli, algoritma SMOTE melakukan interpolasi linear antara titik data terdekat (k=3) untuk mensintesis data baru.

| ID | Nama Kelas | Sebelum | Sesudah | Rasio Peningkatan |
|----|------------|---------|---------|-------------------|
| 0 | High Adherent | 4 | 466 | 116.5x |
| 1 | Low Adherent | 103 | 466 | 4.5x |
| 2 | Medium Adherent | 466 | 466 | 1.0x |
| 3 | High Non-Adherent | 15 | 466 | 31.1x |

![SMOTE Comparison](file:///g:/Download/Capstone DS/Proses Data/Feature Engineering/smote_comparison.png)

## 4. Galeri Fitur Final (Lengkap)
Berikut adalah daftar seluruh nama kolom yang akan menjadi input neuron pada layer pertama MLP:

```text
001. B1_ChangeMind_Decision
002. B1_ChangeMind_Convince
003. B1_AcceptSuggestion
004. B2_ForgetPlan
005. B2_ForgetTold
006. B2_MissAppointment
007. B_CauseOfMissing
008. B_ReminderMethod
009. C1_DrugHelp
010. C1_DrugBurdensome
011. C1_DrugInadequate
012. C2_AwareBeforeDiag
013. C2_AwareLifestyle
014. C2_AwareProlonged
015. D_ForgetPrescribed
016. D_FailOtherReasons
017. D_StopIfWorse
018. D_ForgetTravel
019. D_TakeAllYesterday
020. D_StopIfFeelBetter
021. D_FeelHassled
022. D_DifficultyRemember
023. E_ForgetGeneral
024. E_AwareForgetDetails
025. E_DangerNoAdvice
026. E_BenefitAlerts
027. E_BenefitPersuasive
028. E_BenefitRiskExpl
029. E_BenefitGainExpl
030. E_CostBenefitMobile
031. E_AdaptVoiceSMS
032. E_EnableDiscussion
033. E_PersonalAcceptance
034. GENDER_FEMALE
035. GENDER_MALE
036. AGE_21
037. AGE_21-30
038. AGE_21-31
039. AGE_31-40
040. AGE_4--50
041. AGE_41-50
042. AGE_ABOVE 50
043. AGE_BELOW 21
044. AGE_nan
045. Marital Status_DIVORCED
046. Marital Status_MARRIED
047. Marital Status_SINGLE
048. Marital Status_WIDOW/WIDOWER
049. Marital Status_nan
050. Religion Affiliation_CHRISTIANITY
051. Religion Affiliation_ISLAM
052. Religion Affiliation_OTHERS
053. Religion Affiliation_nan
054. Educational Attainment_FLSC
055. Educational Attainment_FSLC
056. Educational Attainment_NCE/ND/HND
057. Educational Attainment_OTHERS
058. Educational Attainment_POSTGRADUATE DEGREE
059. Educational Attainment_UNIVERSITY FIRST DEGREEE
060. Educational Attainment_WASC/SSCE
061. Educational Attainment_nan
062. Occupation_ARTISAN
063. Occupation_BANKING
064. Occupation_CIVIL SERVANT
065. Occupation_CLERGY
066. Occupation_FARMER
067. Occupation_OTHERS
068. Occupation_PROFESSIONAL
069. Occupation_RETIREES
070. Occupation_SELF EMPLOYED
071. Occupation_STUDENT
072. Occupation_TRADER
073. Occupation_nan
074. How many hours do work in a day_12 HOURS
075. How many hours do work in a day_16 HOURS
076. How many hours do work in a day_20 HOURS
077. How many hours do work in a day_24 HOURS
078. How many hours do work in a day_4 HOURS
079. How many hours do work in a day_8 HOURS
080. How many hours do work in a day_NO WORK
081. How many hours do work in a day_nan
082. Who is your care giver_CHILDREN
083. Who is your care giver_HUSBAND
084. Who is your care giver_OTHERS
085. Who is your care giver_PARENT
086. Who is your care giver_RELATIVES
087. Who is your care giver_SELF
088. Who is your care giver_SPOUSE
089. Who is your care giver_nan
090. Do you have a mobile phone_NO
091. Do you have a mobile phone_YES
092. Do you have a mobile phone_nan
093. How often do you receive text messages/alerts in a day_NEVER
094. How often do you receive text messages/alerts in a day_QUIT OFTEN
095. How often do you receive text messages/alerts in a day_RARELY
096. How often do you receive text messages/alerts in a day_SOMETIMES
097. How often do you receive text messages/alerts in a day_VERY OFTEN
098. How often do you receive text messages/alerts in a day_nan
099. How often do you answer phone calls in a day_NEVER
100. How often do you answer phone calls in a day_QUIT OFTEN
101. How often do you answer phone calls in a day_RARELY
102. How often do you answer phone calls in a day_SOMETIMES
103. How often do you answer phone calls in a day_VERY OFTEN
104. How often do you answer phone calls in a day_nan
105. What is your preferred communication language_ENGLISH
106. What is your preferred communication language_HAUSA
107. What is your preferred communication language_HOUSA
108. What is your preferred communication language_IGBO
109. What is your preferred communication language_YORUBA
110. What is your preferred communication language_nan
111. Health Condition_ASTHMA
112. Health Condition_BONE PAIN
113. Health Condition_COLD
114. Health Condition_CVA
115. Health Condition_DIABETES
116. Health Condition_EYE PROBLEM
117. Health Condition_GLACOMA
118. Health Condition_HEART
119. Health Condition_HIV
120. Health Condition_HYPERTENSION
121. Health Condition_KIDNEY DISEASE
122. Health Condition_KIDNEY FAILURE
123. Health Condition_MALARIA
124. Health Condition_MENTAL
125. Health Condition_NIL
126. Health Condition_NOHTING
127. Health Condition_NONE
128. Health Condition_PRIMARY OPEN ANGLE GLAUCOMA
129. Health Condition_SKIN DISEASE
130. Health Condition_THYPHIOD MALARIA
131. Health Condition_ULCER
132. Health Condition_ULCERS
133. Health Condition_nan
134. How long have you been taking your drugs_10-12  MONTHS
135. How long have you been taking your drugs_10-12 MONTHS
136. How long have you been taking your drugs_4-6 MONTHS
137. How long have you been taking your drugs_7-9 MONTHS
138. How long have you been taking your drugs_ABOVE A YEAR
139. How long have you been taking your drugs_LESS THAN 4 MONTHS
140. How long have you been taking your drugs_nan
141. Number of drugs prescribed_ABOVE THREE
142. Number of drugs prescribed_NIL
143. Number of drugs prescribed_ONE
144. Number of drugs prescribed_THREE
145. Number of drugs prescribed_TWO
146. Number of drugs prescribed_nan
147. How many tablets do you take in a day_6
148. How many tablets do you take in a day_ABOVE THREE
149. How many tablets do you take in a day_NIL
150. How many tablets do you take in a day_NONE
151. How many tablets do you take in a day_ONE
152. How many tablets do you take in a day_THREE
153. How many tablets do you take in a day_TWO
154. How many tablets do you take in a day_nan
155. When do you take your drugs_AFTER LUNCH
156. When do you take your drugs_ANY TIME
157. When do you take your drugs_ANYTIME
158. When do you take your drugs_BEFORE LUNCH
159. When do you take your drugs_BEFORE SLEEP
160. When do you take your drugs_DURING  DINNER
161. When do you take your drugs_DURING BREAKFAST
162. When do you take your drugs_DURING DINNER
163. When do you take your drugs_DURRING BREAKFAST
164. When do you take your drugs_IN THE EVENING AT A SET TIME
165. When do you take your drugs_IN THE MORNING AT A SET TIME
166. When do you take your drugs_IN THE MORNING AT ASET TIME
167. When do you take your drugs_IN THE MORNING WHEN I WAKE UP
168. When do you take your drugs_WITH LUNCH
169. When do you take your drugs_nan
170. Why do you choose to take your drugs at that time_AFTER MEAL
171. Why do you choose to take your drugs at that time_DOCTOR TOLD ME TO TAKE IT AT THAT TIME
172. Why do you choose to take your drugs at that time_I USUALLY FORGET
173. Why do you choose to take your drugs at that time_IT IS EASIER TO REMEMBER
174. Why do you choose to take your drugs at that time_OTHER  SPECIFY
175. Why do you choose to take your drugs at that time_nan
176. ADHERENCE_CLASS
```

## 5. Metadata & Integritas Data
*   **Target Variable**: `ADHERENCE_CLASS`
*   **Output Location**: `Hasil/2_Data_Feature_Engineered_Multiclass.csv`
*   **Data Consistency**: Seluruh kolom telah dipastikan bertipe `float64` atau `int64` (Tidak ada NaNs).
