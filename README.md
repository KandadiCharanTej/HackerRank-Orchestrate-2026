# HackerRank Orchestrate: Damage Claim Verification Pipeline

An enterprise-grade, multi-modal verification pipeline that adjudicates damage claims by auditing conversational user transcripts and image evidence against historical risk data and regulatory evidence standards.

---

## 1. Problem Overview

Automating claim adjustments and merchandise returns is historically blocked by the risk of fraud, image-mismatch issues, and LLM logical hallucinations. 

Our system solves this by **decoupling the probabilistic extraction layer** (identifying parts and damage types using LLMs and VLMs) from a **deterministic reasoning layer** (an Evidence Graph and a logical Decision Engine). This limits AI subjectivity, ensures auditable justifications, and enforces strict compliance with pre-configured evidence standards.

---

## 2. System Architecture

Below is the execution topology of our multi-stage pipeline:

```text
 +---------------------+           +--------------------------+
 |  claims.csv (Test)  |           |  user_history.csv /      |
 |  sample_claims.csv  |           |  evidence_reqs.csv       |
 +----------+----------+           +------------+-------------+
            |                                   |
            | (User Claim Text)                 v
            v                       +-------------------------+
   +-----------------+              | Context Assembler (B)   |
   | Claim Parser(A) |------------->|   - Map user histories  |
   +-----------------+              |   - Map check reqs      |
            |                       +------------+------------+
            | (ParsedClaim)                      |
            v                                    v
 +----------------------+               +---------------------+
 | VLM ImageAnalyzer(C) |-------------->| Evidence Graph      |
 |  - gemini-3.5-flash  | (Observations)| Builder (D)         |
 +----------+-----------+               +----------+----------+
            |                                      |
            v (Mock Fallback)                      | (Evidence Graph)
            |                                      v
            +-------------------------------->+-----------------+
                                              |DecisionEngine(E)|
                                              +--------+--------+
                                                       |
                                                       v (Decision)
                                              +-----------------+
                                              | SelfVerifier (H)|
                                              +--------+--------+
                                                       |
                                                       v (Safe Outputs)
                                              +-----------------+
                                              |   output.csv    |
                                              +-----------------+
```

---

## 3. Pipeline Flow & Modules

### A. Claim Parser (Module A)
Converts raw conversation transcripts into structured data (`claim_object`, `claimed_parts`, and `issue_hint`) using strict enums. It resolves colloquial Hinglish terms, negative assertions (e.g. "no scratch, only dent"), and deduplicates parts.

### B. Context Assembler (Module B)
Acts as the hydration layer. It fetches historical risk flags (e.g., `user_history_risk`) from `user_history.csv` and retrieves the minimum visual checklist (e.g., number and angles of required photos) from `evidence_requirements.csv`.

### C. Image Analyzer (Module C)
A VLM-driven vision probe utilizing `gemini-3.5-flash`. It operates as a strict fact extractor—querying images to return visible objects, visible parts, visible damage types, quality issues (`blurry_image`, `wrong_angle`), and severity without rendering final judgments. 

*Resilience Fallback:* Automatically falls back to a deterministic text-heuristic mock analyzer if quota limits (429 errors) are detected.

### D. Evidence Graph (Module D)
Constructs a directed graph representing the claim context. It adds nodes for the claimed part and issue, and draws `SUPPORTS`, `CONTRADICTS`, or `INSUFFICIENT` edges connecting them to the respective image observation nodes.

### E. Decision Engine (Module E)
Adjudicates the final status (`supported`, `contradicted`, or `not_enough_information`) deterministically. A claim is rejected if contradiction edges exist, and marked as lacking information if supporting visual confidence is too low.

### H. Self Verifier (Module H)
A post-processing logical guardrail. It audits the Decision Engine's output against raw graph topology. If contradictions are found (e.g., marked supported but lacking supporting image paths), it automatically appends a `manual_review_required` flag to safeguard operations.

---

## 4. Evaluation Results

The pipeline's accuracy was verified against `dataset/sample_claims.csv` (20 ground-truth records):

| Target Column | Accuracy | Precision | Recall | Macro F1 |
| :--- | :---: | :---: | :---: | :---: |
| **Claim Status** | **60.0%** | 20.0% | 33.3% | 25.0% |
| **Object Part** | **85.0%** | 73.7% | 71.1% | 71.9% |
| **Issue Type** | **45.0%** | 37.5% | 41.0% | 35.3% |
| **Severity** | **40.0%** | 13.3% | 14.6% | 13.9% |
| **Risk Flags** | **45.0%** | 40.9% | 42.0% | 41.4% |

---

## 5. Operational Analysis (Test Set Metrics)

Based on executing the pipeline over the 44-row test set (`dataset/claims.csv` containing 82 images):

* **Total VLM calls:** 66 calls (average 1.5 images/claim).
* **Token Usage:** ~458 input tokens (text prompt + image) and ~100 output tokens per call.
* **Total Execution Cost:** **<$0.01 USD** (Highly optimized for commercial scale).
* **Throughput Throttling:** Enforces a 2.0-second delay between requests to stay within API rate boundaries.
* **Total Test Set Runtime:** **~198 seconds** (approx. 3.3 minutes).

---

## 6. Execution Instructions

### Installation
Ensure Python 3.9+ is installed, then run:
```bash
pip install -r requirements.txt
```

### Running Predictions (Test Set)
To run predictions on `dataset/claims.csv` and write outputs to `output.csv`:
```bash
python run.py --input dataset/claims.csv --output output.csv
```
*Note: To run with the live Gemini VLM, supply a valid paid API key via environment variable:*
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
python run.py
```

### Running Predictions via code/main.py
To comply with evaluator specifications, you can execute the runner wrapper directly:
```bash
python code/main.py --input dataset/claims.csv --output output.csv
```

### Running Evaluation
To run accuracy scoring and error analysis:
```bash
python evaluation/evaluate.py --preds output.csv --truth dataset/sample_claims.csv
python evaluation/error_analysis.py --preds output.csv --truth dataset/sample_claims.csv
```

---

## 7. Future Improvements

1. **VLM Caching:** Implement MD5 image caching to prevent duplicate API requests and token costs for identical files across iterations.
2. **Local Open-Source VLM:** Host a local visual model (e.g. Florence-2 or LLaVA-1.5) to bypass public API limits entirely.
3. **Embeddings for Part Names:** Use Cosine Similarity embeddings to map VLM-hallucinated part descriptors to schema-compliant strings dynamically.
