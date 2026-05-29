# Data Dictionary - Multi-Dimensional Adherence Dataset

This document provides a detailed mapping between the Excel dataset columns and the questionnaire provided in `questionnaire.txt`.

## Section A: Demographics

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 0 | S/N | Serial Number | int64 | Unique ID | 0.0% |
| 1 | GENDER | 1. Gender | str | male, female | 0.0% |
| 2 | AGE | 2. Age at last birthday | object | 21, 21-31, 31-40, 41-50, Above 50 | 0.6% |
| 3 | Marital Status | 3. Marital Status | str | single, married, Divorced, widow/widower | 0.6% |
| 4 | Religion Affiliation | 4. Religion Affiliation | str | Christianity, Islam, Others | 0.8% |
| 5 | Educational Attainment | 5. Educational Attainment | str | None, FLSC, WASC/SSCE, NCE/ND/HND, University, PG | 9.5% |
| 6 | Occupation | 6. Occupation | str | Farmer, Trader, Professional, Artisan, Student, Retirees | 0.1% |
| 7 | How many hours... | 7. Hours worked per day | str | 4, 8, 12, 16, 20, 24 hours | 2.3% |
| 8 | Who is your care giver | 8. Caregiver | str | Spouse, Parent, Children, Relatives, Others | 2.3% |
| 9 | Do you have a mobile phone | 9. Mobile phone ownership | str | Yes, No | 14.3% |
| 10 | How often receive SMS | 10. SMS frequency | str | Very Often, Quite Often, Sometimes, Rarely, Never | 0.6% |
| 11 | How often answer calls | 11. Call frequency | str | Very Often, Quite Often, Sometimes, Rarely, Never | 0.5% |
| 12 | Preferred language | 12. Communication language | str | Igbo, Hausa, English, etc. | 1.0% |
| 13 | Health Condition | 13. Health Condition | str | Hypertension, HIV, Mental, Diabetes, etc. | 6.9% |
| 14 | How long taking drugs | 14. Duration of treatment | str | <4 months, 4-6, 7-9, 10-12, >1 year | 4.4% |
| 15 | Number of drugs | 15. Drugs prescribed | str | One, Two, Three, Above three | 2.0% |
| 16 | Tablets per day | 16. Tablets per day | object | One, Two, Three, Above three | 2.8% |
| 17 | When take drugs | 17. Medication timing | str | Morning, Breakfast, Lunch, Dinner, etc. | 1.3% |
| 18 | Why take drugs at time | 18. Rationale for timing | str | Easier to remember, Doctor's advice, etc. | 10.3% |

## Section B: Behavioral / Perception (Part 1)

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 19 | 19 | 19. Change mind about decisions | float64 | 1-5 (Very Often to Never) | 2.4% |
| 20 | 20 | 20. Change mind if motivated | float64 | 1-5 | 2.6% |
| 21 | 21 | 21. Accept suggestions from provider | float64 | 1-5 | 2.4% |
| 22 | TOTAL | Sum of Q19, Q20, Q21 | float64 | 0-15 (Calculated, NaN=0) | 35.9% |
| 23 | PERCEPTION LEVEL | Perception category | str | Low, Moderate, High, etc. | 74.2% |

## Section B: Behavioral / Memory (Part 2)

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 25 | 22 | 22. Forget planned actions | float64 | 1-5 | 1.8% |
| 26 | 23 | 23. Forget things told recently | float64 | 1-5 | 1.6% |
| 27 | 24 | 24. Miss appointments | float64 | 1-5 | 1.6% |
| 28 | TOTAL.1 | Sum of Q22, Q23, Q24 | float64 | 0-15 | 35.9% |
| 30 | BEHAVIOUR LEVEL | Behavior category | str | Low, Moderate, High, etc. | 74.2% |
| 31 | 25 | 25. Cause of missing drugs | str | Forgot, Work, Routine, etc. | 13.5% |
| 32 | 26 | 26. Reminder source | str | Open ended | 11.6% |

## Section C: Beliefs & Awareness

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 34 | 27 | 27. Belief drugs help | float64 | 1-5 (SA to SD) | 1.9% |
| 35 | 28 | 28. Taking drugs is burdensome | float64 | 1-5 | 2.9% |
| 36 | 29 | 29. Drug alone is inadequate | float64 | 1-5 | 2.6% |
| 37 | TOTAL | Sum of Q27, Q28, Q29 | float64 | 0-15 | 37.1% |
| 41 | 30 | 30. Awareness of sickness | float64 | 1-5 | 3.4% |
| 42 | 31 | 31. Awareness of lifestyle changes | float64 | 1-5 | 2.3% |
| 43 | 32 | 32. Awareness of prolonged treatment| float64 | 1-5 | 2.3% |
| 44 | TOTAL.2 | Sum of Q30, Q31, Q32 | float64 | 0-15 | 37.1% |
| 46 | KNOWLEDGE LEVEL | Knowledge category | str | Low, Moderate, High | 74.2% |

## Section D: Compliance & Adherence (The "Gold Standard")

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 48 | 33 | 33. Sometimes forget? | float64 | 0 (No), 1 (Yes) | 2.8% |
| 49 | 34 | 34. Fail for other reasons? | object | 0 (No), 1 (Yes) | 2.6% |
| 50 | 35 | 35. Cut back/Stop? | float64 | 0 (No), 1 (Yes) | 2.4% |
| 51 | 36 | 36. Forget when travel? | float64 | 0 (No), 1 (Yes) | 2.4% |
| 52 | 37 | 37. Take all yesterday? | float64 | 0 (No), 1 (Yes) | 4.4% |
| 53 | 38 | 38. Stop when feel better? | float64 | 0 (No), 1 (Yes) | 1.8% |
| 54 | 39 | 39. Feel hassled? | float64 | 0 (No), 1 (Yes) | 2.3% |
| 55 | 40 | 40. Difficulty remembering | object | A-E (Never to All the time) | 5.7% |
| 56 | TOTAL.3 | Sum of Q33-Q39 | float64 | 0-7 | 37.4% |
| 57 | NON ADHERENT LEVEL | Adherence category | str | Low, Moderate, High | 74.2% |

## Section E & Final Target

| Index | Column Name | Question | Type | Valid Range / Options | Missing % |
|-------|-------------|----------|------|-----------------------|-----------|
| 59-68 | 41-50 | Q41-50: Perception of App | float64 | 1-5 (SA to SD) | ~24% |
| 69 | 51 | **Final Adherence Class** | object | 0 (Non-Adherent), 1 (Adherent) | 24.8% |

> [!NOTE]
> Column 69 (`51`) is the primary target for predictive modeling. The 151 missing values in this column are the main challenge for Phase 2.
