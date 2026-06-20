# Error Analysis Report

**Total Records Evaluated:** 20

## Summary of Errors

- **Damage Detection**: 11 errors
- **Part Detection**: 3 errors
- **Severity**: 12 errors
- **Evidence Sufficiency**: 8 errors
- **Risk Flags**: 11 errors

---

## Damage Detection Errors (11)

| User ID | Ground Truth | Prediction |
|---|---|---|
| user_002 | `broken_part` | `scratch` |
| user_005 | `scratch` | `unknown` |
| user_006 | `unknown` | `crack` |
| user_007 | `broken_part` | `unknown` |
| user_008 | `broken_part` | `scratch` |
| user_018 | `crack` | `glass_shatter` |
| user_020 | `none` | `unknown` |
| user_031 | `water_damage` | `torn_packaging` |
| user_032 | `unknown` | `missing_part` |
| user_033 | `unknown` | `crushed_packaging` |
| user_034 | `none` | `torn_packaging` |


## Part Detection Errors (3)

| User ID | Ground Truth | Prediction |
|---|---|---|
| user_008 | `front_bumper` | `hood` |
| user_010 | `hinge` | `hinge;screen` |
| user_033 | `unknown` | `box` |


## Severity Errors (12)

| User ID | Ground Truth | Prediction |
|---|---|---|
| user_002 | `unknown` | `low` |
| user_004 | `medium` | `low` |
| user_005 | `low` | `high` |
| user_006 | `unknown` | `high` |
| user_007 | `medium` | `high` |
| user_008 | `high` | `medium` |
| user_012 | `low` | `medium` |
| user_018 | `medium` | `high` |
| user_020 | `none` | `unknown` |
| user_032 | `unknown` | `medium` |
| user_033 | `low` | `high` |
| user_034 | `none` | `medium` |


## Evidence Sufficiency Errors (8)

| User ID | Ground Truth | Prediction |
|---|---|---|
| user_002 | `not_enough_information` | `supported` |
| user_005 | `contradicted` | `supported` |
| user_006 | `not_enough_information` | `supported` |
| user_008 | `contradicted` | `supported` |
| user_020 | `contradicted` | `supported` |
| user_032 | `not_enough_information` | `supported` |
| user_033 | `contradicted` | `supported` |
| user_034 | `contradicted` | `supported` |


## Risk Flags Errors (11)

| User ID | Ground Truth | Prediction |
|---|---|---|
| user_002 | `wrong_object;claim_mismatch;manual_review_required` | `none` |
| user_003 | `blurry_image` | `none` |
| user_005 | `claim_mismatch;user_history_risk;manual_review_required` | `manual_review_required;user_history_risk` |
| user_006 | `wrong_angle;damage_not_visible` | `none` |
| user_007 | `none` | `manual_review_required` |
| user_008 | `claim_mismatch;non_original_image;user_history_risk;manual_review_required` | `user_history_risk` |
| user_020 | `damage_not_visible;user_history_risk;manual_review_required` | `manual_review_required;user_history_risk` |
| user_031 | `user_history_risk;manual_review_required` | `user_history_risk` |
| user_032 | `cropped_or_obstructed;damage_not_visible;manual_review_required` | `manual_review_required` |
| user_033 | `wrong_object;claim_mismatch;user_history_risk;manual_review_required` | `user_history_risk` |
| user_034 | `damage_not_visible;text_instruction_present;user_history_risk;manual_review_required` | `user_history_risk` |

