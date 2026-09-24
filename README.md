---
license: apache-2.0
title: SZL SDA — Folded
emoji: 🛰️
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
short_description: Historical SDA surface; canonical engine authority is khipu-sda-core.
tags:
  - anomaly-detection
  - sensor-fusion
  - domain-awareness
  - receipts
  - governance
  - szl-holdings
---

<p align="center">
  <a href="https://a-11-oy.com/">
    <img src="https://huggingface.co/spaces/SZLHOLDINGS/README/resolve/main/assets/estate-banner-v2.svg" alt="SZL Holdings — control before action, evidence after" width="100%">
  </a>
</p>

# SDA

**FOLDED / ARCHIVE-BOUND / NOT CANONICAL**

This repository preserves the historical investor-facing SDA surface and its
source evidence. It is no longer a standalone publication authority.

**Canonical engine:** [szl-holdings/khipu-sda-core](https://github.com/szl-holdings/khipu-sda-core)

## Mission brief

The preserved SDA surface demonstrates a read-only operating picture for noisy
sensor tracks, graph relationships, policy-aware advisory verdicts, and receipt
context.

**Detect → Fuse → Govern → Verify**

- Detect illustrative point and relational anomalies.
- Fuse observations into a common operating picture.
- Keep Λ advisory; a separately named policy gate owns control.
- Carry evidence fields downstream for independent verification.

## Current authority and evidence

- **CANONICAL:** `khipu-sda-core` owns current SDA engine authority.
- **NO STANDALONE PUBLICATION:** `FOLD.md` disables standalone Hugging Face
  publication from this repository, including alternate source directories.
- **NO STANDALONE RUNTIME QUALIFICATION:** the standalone drift verifier also
  fails closed while this repository is folded. An extant historical Space is
  not current source or readiness authority.
- **HISTORICAL SNAPSHOT:** `SPACE_PROVENANCE.json` preserves the July 30, 2026
  observation. Its historical source-of-record and runtime fields must not be
  promoted as current state.
- **MODELED:** packaged tracks and anomaly baselines remain demonstration data,
  not operational-accuracy evidence.
- **CONJECTURE / ROADMAP:** Λ remains Conjecture 1 and advisory. Effectors are
  simulated.

Receipt verification establishes integrity only within its stated scope. It
does not establish prediction accuracy, operational readiness, or real-world
effectiveness.

## Run locally

Historical source can still be inspected locally without publishing it.
Requires Python 3.12.

```bash
git clone https://github.com/szl-holdings/sda.git
cd sda
python server.py
```

Open `http://127.0.0.1:7860` and check process liveness:

```bash
curl http://127.0.0.1:7860/livez
```

Local `/readyz` remains fail-closed without an exact `SOURCE_BINDING.json`.
That local behavior is not a deployment or promotion claim.

## Verify the repository

```bash
python -m pip install "pytest==9.0.2" "huggingface_hub==0.36.0"
python -m compileall -q server.py szl_source_attestation.py scripts tests
python -m pytest -q
```

The native suite checks health boundaries, source-attestation behavior, folded
publication/verification denial, and workflow source binding.

## System boundaries

- `server.py` preserves the historical read-only surface and evidence routes.
- `index.html` and vendored assets render locally without a runtime CDN.
- Optional browser reads may reach external APIs; unavailable sources stay
  distinct from packaged snapshots and demo data.
- The repository has no application database or write API.
- Source binding does not claim reproducible builds, binary provenance, or
  serving-process identity.

## Project routes

- [Fold and canonical-authority record](FOLD.md)
- [Historical Space provenance snapshot](SPACE_PROVENANCE.json)
- [Canonical SDA engine](https://github.com/szl-holdings/khipu-sda-core)
- [Security policy](https://github.com/szl-holdings/.github/security/policy)
- [Commit history](https://github.com/szl-holdings/sda/commits/main)
- [Apache-2.0 license](LICENSE)

Clean-room implementation informed by public descriptions and permissively
licensed research listed in the application. SZL Holdings is not affiliated
with True Anomaly, and no proprietary implementation is represented here.
