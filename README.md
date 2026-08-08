---
license: apache-2.0
title: SZL SDA
emoji: 🛰️
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
short_description: Receipt-bound domain awareness for governed sensor fusion.
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

**See what changed across noisy sensors—then leave a verifiable record of the advisory.**

`DEMONSTRATION` · `READ-ONLY` · `AIR / MARITIME / COUNTER-UAS`

[Open the live mission map](https://huggingface.co/spaces/SZLHOLDINGS/sda) ·
[Inspect current readiness](https://szlholdings-sda.hf.space/readyz) ·
[Read the source binding](https://szlholdings-sda.hf.space/api/build-info)

## Mission brief

SDA turns multivariate signals and graph relationships into a fused operating
picture and a policy-aware advisory verdict. It is designed for teams that need
to investigate an anomaly without losing the provenance of inputs, method, and
decision context.

**Detect → Fuse → Govern → Verify**

- Detect point and relational anomalies across illustrative tracks.
- Fuse observations into a common operating picture.
- Apply Λ as an advisory signal; a separately named policy gate owns control.
- Carry DSSE-shaped evidence fields downstream for independent verification.

## What the evidence says now

- **OPERATIONAL:** the public, read-only demonstration and its packaged local
  dependencies. The live [`/readyz`](https://szlholdings-sda.hf.space/readyz)
  response is the current status source.
- **SOURCE BOUND:** the deployment workflow publishes a declared runtime file
  set and exposes its exact Git revision through
  [`/api/build-info`](https://szlholdings-sda.hf.space/api/build-info).
- **NOT MEASURED:** live sensor, Killinchu COP, and A11oy compute-pool
  availability unless the running surface explicitly reports otherwise.
- **MODELED:** the included tracks and synthetic anomaly baseline. They are not
  operational accuracy claims.
- **CONJECTURE / ROADMAP:** Λ remains Conjecture 1 and advisory. Orbital SDA is
  roadmap; effectors are simulated.

Receipt verification establishes integrity and origin within its stated scope.
It does not establish prediction accuracy, operational readiness, or real-world
effectiveness.

## Run locally

Requires Python 3.12. The runtime uses the standard library and has no frontend
build step.

```bash
git clone https://github.com/szl-holdings/sda.git
cd sda
python server.py
```

Open `http://127.0.0.1:7860` and check process liveness:

```bash
curl http://127.0.0.1:7860/livez
```

Local `/readyz` intentionally fails closed until an exact
`SOURCE_BINDING.json` is present. That binding is injected and verified by the
protected Hugging Face deployment workflow.

## Verify the repository

```bash
python -m pip install "pytest==9.0.2" "huggingface_hub==0.36.0"
python -m compileall -q server.py szl_source_attestation.py scripts tests
python -m pytest -q
```

The native suite checks health boundaries, no-store response behavior,
fail-closed readiness, and exact-runtime-file-set source reporting.

## System boundaries

- `server.py` serves the hardened read-only surface and evidence routes.
- `index.html` and vendored assets render the operating picture without a
  runtime CDN.
- Optional browser reads may reach the A11oy and Killinchu APIs; unavailable
  sources stay visibly distinct from packaged snapshots and demo data.
- The repository has no application database or write API. A user-submitted
  receipt is sent only when the verifier action is invoked.
- Source binding does not claim reproducible builds, binary provenance, or
  serving-process identity beyond the fields returned by the evidence route.

## Project routes

- [Deployment and provenance contract](SPACE_PROVENANCE.json)
- [Security policy](https://github.com/szl-holdings/.github/security/policy)
- [Issues and support](https://github.com/szl-holdings/sda/issues)
- [Commit history](https://github.com/szl-holdings/sda/commits/main)
- [Apache-2.0 license](LICENSE)

Clean-room implementation informed by public descriptions and permissively
licensed research listed in the application. SZL Holdings is not affiliated
with True Anomaly, and no proprietary implementation is represented here.
