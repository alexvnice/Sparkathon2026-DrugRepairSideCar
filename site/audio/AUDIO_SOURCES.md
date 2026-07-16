# Demo Audio File Provenance

All audio files in this directory are used solely for Sparkathon 2026 demonstration purposes.

---

## Dataset 2 — HealthDial (cambridgeltl/HealthDial, English subset)

**License:** Not visible on dataset card — verify before any commercial use.
**Source:** HuggingFace `cambridgeltl/HealthDial`, English split
**Format:** 16kHz mono WAV, TTS-synthesised medical dialogue turns

| Filename | Dialogue | Drug / Term | Garbling Pattern |
|---|---|---|---|
| `67a21fa3cf66eadeed1bf168_ENG_52_1.wav` | ENG_52, turn 1 | tramadol | "trauma doll" |
| `67a5c8b3f41d06aeac934e6f_ENG_67_6.wav` | ENG_67, turn 6 | typhoid | "time for a tweet" |
| `67a5c8b3f41d06aeac934e6f_ENG_99_2.wav` | ENG_99, turn 2 | schistosomiasis | "still so me aces" |
| `67c976d9607346d8bf0acef5_ENG_905_2.wav` | ENG_905, turn 2 | cholera | "color" |
| `67b61864612d351d7d2ff99b_ENG_753_0.wav` | ENG_753, turn 0 | mpox | "M-Plox" |
| `67d9cd441f087c589643ad95_ENG_1352_3.wav` | ENG_1352, turn 3 | haemolytic uraemic syndrome | "hemolatic reumic syndrome" |
| `67a21fa3cf66eadeed1bf168_ENG_272_4.wav` | ENG_272, turn 4 | mpox | "impacts" |

---

## Dataset 1 — ACCES MeDial-Speech (hcuayahu/MeDial-Speech)

**License:** CC-BY-NC-4.0 (non-commercial use only)
**Source:** HuggingFace `hcuayahu/MeDial-Speech`, DR1 subset
**Format:** 16kHz mono WAV, real doctor-patient conversation segments (screen recording audio, both sides captured)
**Note:** Audio extracted from `START_VIDEO_RECORDING_ei*.wav` files to capture full doctor-patient exchange including patient responses.

| Filename | Session | Drugs | Garbling Pattern |
|---|---|---|---|
| `DR1_21r_turn17_amlodipine_clopidogrel.wav` | DR1, participant 21r, turn 17 | clopidogrel + amlodipine | "Claire Pettigrew" + "amlodipi" |
| `DR1_44v_turn17_amlodipine_clopidogrel.wav` | DR1, participant 44v, turn 17 | clopidogrel + amlodipine | "Copidogrel" + "Albert de Payne" |
| `DR1_4v_turn13_clopidogrel_amlodipine.wav` | DR1, participant 4v, turn 13 | clopidogrel + amlodipine | reference example |

---

## Usage Notes

- Dataset 2 audio is TTS-generated (no real patient PII).
- Dataset 1 audio is from an IRB-approved academic study; no PII is present in these de-identified segments.
- Do not distribute these files outside the Sparkathon submission context without verifying dataset licenses.
