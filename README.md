---
license: apache-2.0
title: SZL SDA
emoji: 🛰️
colorFrom: green
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
short_description: Sovereign domain superiority; signed receipt per verdict.
tags:
  - anomaly-detection
  - sensor-fusion
  - domain-awareness
  - receipts
  - governance
  - szl-holdings
---


<div align="center">
<p>

[![governed](https://img.shields.io/badge/governed-SZL%20Holdings-3af4c8?style=flat-square)](https://huggingface.co/SZLHOLDINGS)
[![Λ](https://img.shields.io/badge/Λ-Conjecture%201%20advisory-d7b96b?style=flat-square)](https://a-11-oy.com)
[![license](https://img.shields.io/badge/license-apache--2.0-7e8aa3?style=flat-square)](https://huggingface.co/spaces/SZLHOLDINGS/sda)

</p>
</div>
<!-- SZL-ESTATE-CARD:v2:START -->
<p align="center"><a href="https://a-11-oy.com/"><img src="https://huggingface.co/spaces/SZLHOLDINGS/README/resolve/main/assets/estate-banner-v2.svg" alt="SZL Holdings — governed, receipted, verifiable" width="100%"></a></p>
<p align="center">
  <a href="https://github.com/szl-holdings/.github/tree/main/doctrine"><img src="https://img.shields.io/badge/doctrine-v11%20LOCKED-0B1F3A?style=flat-square" alt="doctrine v11"></a>
  <a href="https://a-11-oy.com/"><img src="https://img.shields.io/badge/evidence%20wall-LIVE%20%C2%B7%20verify%20in%20browser-3AF4C8?style=flat-square" alt="live evidence wall"></a>
  <a href="https://huggingface.co/datasets/SZLHOLDINGS/szl-lake"><img src="https://img.shields.io/badge/szl--lake-offline%20verifiable-C9B787?style=flat-square" alt="szl-lake offline verifiable"></a>
  <a href="https://huggingface.co/spaces/SZLHOLDINGS/holographic"><img src="https://img.shields.io/badge/estate%20map-holographic-5B8DEE?style=flat-square" alt="holographic estate map"></a>
</p>
<p align="center"><sub>Part of the <a href="https://huggingface.co/SZLHOLDINGS">SZL Holdings</a> governed estate — claims are designed to carry checkable receipts. Verification proves integrity &amp; origin, never accuracy or performance.</sub></p>
<!-- SZL-ESTATE-CARD:v2:END -->

# SZL HOLDINGS — SDA (Sovereign Domain Superiority)

A self-contained, mobile-friendly surface that explains and demonstrates **SZL SDA** — SZL's
clean-room sovereign **Domain-Superiority** engine, **`khipu-sda-core`**. It delivers:

- multivariate + graph **anomaly detection**;
- **multi-sensor track fusion** into a Common Operating Picture;
- a **Λ-gated advisory verdict**; and
- a **signed provenance receipt** for every threat call.

SZL SDA is **inspired by** [True Anomaly's Mosaic](https://www.trueanomaly.space/mosaic) capability
(sensor-fusion COP, OODA acceleration, ML threat-warning). **SZL is not affiliated with True Anomaly**
and **no proprietary code was seen or copied** — the capability was rebuilt clean-room from public
descriptions and a verified-permissive lineage.

## What this shows

1. **Hero** — one investor sentence: anomaly detection + track fusion, with a signed receipt for every verdict.
2. **The capability (honest, plain)** — multivariate + graph anomaly detection, multi-sensor track
   fusion → Common Operating Picture, an **SGP4 orbital-conjunction seed clearly labelled SPACE ROADMAP**
   (today's live surface is **air / maritime / counter-UAS**), Λ-gated advisory confidence, and a signed
   provenance receipt per verdict.
3. **A live COP visual** — an elegant canvas Common Operating Picture: fused tracks as blips, an anomaly
   overlay coloured by score, a per-track anomaly-score panel, and a sensor-fusion convergence diagram.
   It reads the live killinchu `/api/killinchu/v1/mosaic/cop` endpoint when reachable (re-labels **LIVE**),
   and the **sovereign GPU fabric** via [`https://a-11-oy.com/api/a11oy/v1/compute-pool`](https://a-11-oy.com/api/a11oy/v1/compute-pool) with an honest **SNAPSHOT** fallback;
   otherwise it shows clearly labelled **demo data**.
4. **The moat** — a **verified verdict receipt** panel showing the honest DSSE-shaped fields (method,
   inputs hash, anomaly score, fused track id, Λ verdict allow/advisory/deny, conformal CI, walltime,
   verified flag), an "ask the fabric — verify a receipt" widget, and the **honest synthetic-data baseline
   metrics** with the clear caveat that they improve with real training.
5. **Where it fits** — powers **killinchu** (Track Board / Threat-DB / Mosaic COP view, PR #118), governed
   by **a11oy** (Governed Anomalies, PR #356), air-gap deployable via the **szl-sda** UDS bundle.

## Honest baseline metrics (synthetic data — REAL numbers)

From `khipu-sda-core`'s `szl_mosaic_validate.py` on synthetic tracks with injected anomalies (sustained
maneuver, RCS spike, heading weave); thresholds set from the calibration distribution, not tuned to the
test anomalies:

| Channel | Precision | Recall | F1 |
|---|---|---|---|
| Point ensemble (iForest + AE + robust-z) | 0.44 | 0.74 | 0.55 |
| Graph-relational (GDN-style velocity dev.) | 1.00 | 0.35 | 0.52 |
| Fused consensus (0.5·point + 0.5·graph) | 0.40 | 0.70 | 0.51 |

Track fusion: 6 fused COP tracks recovered from 6 true objects across 2 noisy sensors.

**These are honest synthetic-data baselines, not operational accuracy.** The graph channel correctly
misses the RCS spike (no kinematic signature) — the right behaviour, not a bug. Numbers improve with real
training data and will be **re-measured on the live GPU fabric and re-issued with a real signed DSSE
receipt — never inflated.**

## Attribution (clean-room adoption — cite, never plagiarize)

- **Inspiration only** from True Anomaly Mosaic public descriptions
  ([Mosaic](https://www.trueanomaly.space/mosaic);
  [Eric Hilmer / True Anomaly, LinkedIn](https://www.linkedin.com/posts/erichilmer_true-anomaly-lands-174m-contract-from-us-activity-7110684034724233216-371t)).
  **Not affiliated; no proprietary code seen or copied.**
- Methods re-implemented from a verified-permissive lineage:
  [PyOD (BSD-2)](https://github.com/yzhao062/pyod), [PyGOD (BSD-2)](https://github.com/pygod-team/pygod),
  [Merlion (BSD-3)](https://github.com/salesforce/Merlion), [TODS (Apache-2.0)](https://github.com/datamllab/tods),
  [tsod (MIT)](https://github.com/DHI/tsod), [GDN (MIT)](https://github.com/d-ailin/GDN),
  [GraGOD (MIT)](https://github.com/GraGODs/GraGOD), [python-sgp4 (MIT)](https://github.com/brandon-rhodes/python-sgp4).
- **alibi-detect EXCLUDED** ([Seldon BSL-1.1](https://github.com/SeldonIO/alibi-detect/blob/master/LICENSE));
  CI-enforced absent in `khipu-sda-core`.
- Verify-receipt widget UI pattern inspired by smolagents (Apache-2.0) and assistant-ui (MIT); rebuilt
  SZL-native, no code copied.

## Honesty doctrine v11 (badges shown in-app)

- **Λ = Conjecture 1** — advisory only (allow / advisory / deny); never "proven trust", never a false green.
- **Khipu BFT settlement = Conjecture 2** (advisory). killinchu **effectors = simulated**.
- **Orbital SDA / threat-warning = ROADMAP** — air / maritime / counter-UAS is live. The SGP4 conjunction
  stub seeds the roadmap; SZL does not claim to fly in orbit.
- Receipts ship honestly **UNSIGNED / verified:false** until a real DSSE signature is applied downstream
  (szl_lake / khipu Ed25519/P-256); **no signature is ever fabricated**.
- Anomaly scores, confidence bands, and all `$`/credit figures = **ESTIMATE**; walltime = **MEASURED** only
  where labelled. Synthetic / demo data is labelled as such. **No free energy.**
- **sovereign = own-metal only** — hosted APIs are labelled "hosted fallback — not compute you own".

## Tech / sovereignty

Static HTML/CSS/JS behind a small hardened read-only Python file server. **0 runtime CDN** — `three.js` r160 (MIT) is **vendored** locally under
`assets/three.module.min.js` (see `assets/THREE_LICENSE.txt`). The COP canvas, score panel, verify widget,
and fabric reader are self-contained. **System fonts only** (Calibri / system-ui stack). There is no
application database, write API, or frontend build step.

Mobile system per the estate mobile spec: ≥12px font floor, ≥44px tap targets, `safe-area-inset`,
0px horizontal overflow at 320/360/390/768, `prefers-reduced-motion`, WCAG AA.

### Deployment-source evidence

`GET /.well-known/szl-source.json` reports the measured Hugging Face repository head and the
exact `szl-holdings/sda` revision injected by the protected deployment workflow. The workflow publishes
only the declared runtime file set, verifies every shipped file by SHA-256, and refuses readiness until
`SOURCE_BINDING.json` contains an exact 40-character Git revision. `?refresh=1` bypasses the short
repository-head cache. The response is read-only, `no-store`, and inherits the same security headers as
the rest of the Space. This scoped source binding does not claim external-feed availability, operational
accuracy, reproducible builds, or live effectors.

Runtime evidence routes:

- `GET /livez` and `GET /healthz` — process liveness only.
- `GET /readyz` — local runtime dependencies plus exact source binding.
- `GET /api/build-info` — exact GitHub repository, revision, and deployment-alignment state.

## Branding

Deep-space dark, teal `#01696F` / cyan `#3DD6FF` / violet `#7C5CFF` glow, glassmorphism, system fonts —
consistent with the cathedral / energy / khipu / llm-router / anatomy / mechanics estate spaces.

---

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19944926.svg)](https://doi.org/10.5281/zenodo.19944926)

## Citation

Part of the **SZL Holdings Ouroboros Thesis** — concept DOI [`10.5281/zenodo.19944926`](https://doi.org/10.5281/zenodo.19944926) (Stephen P. Lutar, Jr., [ORCID 0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)). Doctrine v11 LOCKED; Λ = Conjecture 1.

*Signed-off-by: Stephen Lutar <stephenlutar2@gmail.com>*

---

## SZL Estate

Part of the **SZL Holdings** governed-AI estate — *governed AI you can prove*: every decision carries a signed, checkable receipt.

- **Flagship:** [a11oy command console → a-11-oy.com](https://a-11-oy.com)
- **Orgs:** [GitHub · szl-holdings](https://github.com/szl-holdings) · [Hugging Face · SZLHOLDINGS](https://huggingface.co/SZLHOLDINGS)
- **Related Spaces:** [🦅 killinchu](https://huggingface.co/spaces/SZLHOLDINGS/killinchu) · [🫀 anatomy](https://huggingface.co/spaces/SZLHOLDINGS/anatomy) · [🌌 cosmos](https://huggingface.co/spaces/SZLHOLDINGS/cosmos)

**Status:** responding as of 2026-07-09 (HF Space root probe, this session).

<sub>Doctrine v11 · Λ = Conjecture 1 (advisory — never "green"/theorem; open) · honest by design · public data only.</sub>

---

<div align="center">

**[🛡️ SZLHOLDINGS on Hugging Face →](https://huggingface.co/SZLHOLDINGS)**   ·   **[a-11-oy.com →](https://a-11-oy.com)**   ·   **[Estate hub — live →](https://szlholdings-szl-estate-live.static.hf.space)**

### Governed AI you can prove.

<sub>SLSA: L1 honest · L2 attested · L3 roadmap. Λ = Conjecture 1 (advisory, never a theorem). Trust ceiling 0.97 — never 100%. Labels honest by default: MEASURED / REPORTED / MODELED / HEURISTIC / UNKNOWN / UNAVAILABLE. locked-proven = exactly 8 {F1,F4,F7,F11,F12,F18,F19,F22}.</sub>

</div>
