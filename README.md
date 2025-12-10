# Ancestor Framework - Multi-Agent Trust Simulation

## Overview

This repository contains the implementation and test results of the **Ancestor Framework**, an API for source reliability scoring for enterprise AI. Ancestor is a rule-based deterministic engine that scores LLM citations from 0 to 100 using four methods:

- **Provenance**: Evaluating the origin and credibility of sources
- **Recency**: Assessing how current the information is
- **Source Quality**: Determining the trustworthiness of the domain
- **Source Authenticity**: Verifying the legitimacy of sources

## Key Features

- **Air-gapped**: Operates independently without external dependencies
- **Deterministic**: Uses rule-based heuristics for consistent, reproducible results
- **No AI recursion**: Avoids using AI to check AI (preventing cyclotron problems)
- **Enterprise-ready**: Designed for compliance and auditable trust scoring

## Repository Structure

```
.
├── First test - verified sources/    # Test with 100 verified, high-quality citations
│   ├── main.py                      # Simulation implementation
│   ├── public_citation_sources.csv  # Input dataset
│   ├── results.csv                  # Simulation results
│   ├── trust_plot.png              # Visualization
│   ├── simulation_report.txt       # Summary report
│   └── README.md                   # Detailed documentation
│
└── Second test - fake sources/      # Adversarial test with mixed citations
    ├── main.py                      # Enhanced simulation
    ├── mixed_citation_sources.csv   # 50 real + 50 fake citations
    ├── results.csv                  # Test results
    ├── trust_plot.png              # Visualization
    ├── adversarial_simulation_report.txt  # Detailed findings
    └── README.md                    # Test documentation
```

## Test Results Summary

### Test 1: Verified Sources
- **Total episodes**: 100
- **Acceptance rate**: 100%
- **Average trust score**: 96.59
- **Score range**: 83.88 – 99.97
- **Key finding**: All high-quality sources passed the trust threshold

### Test 2: Adversarial Sources
- **Total episodes**: 100
- **Accepted claims**: 81
- **Rejected claims**: 19
- **Average trust score**: 84.30
- **Key finding**: Successfully filtered out fabricated/low-trust citations

## Multi-Agent Architecture

The simulation demonstrates three cooperating agents:

1. **Claimant Agent**: Selects citations and makes factual claims
2. **Verifier Agent (Ancestor)**: Scores trustworthiness using deterministic rules
3. **Consumer Agent**: Accepts/rejects claims based on trust threshold

## Scoring Algorithm

**[Patent Pending - Proprietary Algorithm]**

The Ancestor Framework uses a deterministic, rule-based scoring system that evaluates:
- Source recency and age factors
- Domain trustworthiness and reputation
- Content bias and credibility indicators
- Source authenticity markers

Scores range from 0-100, with configurable acceptance thresholds for different use cases.

## Installation & Usage

### Prerequisites
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas matplotlib numpy
```

### Running Simulations

#### Test 1: Verified Sources
```bash
cd "First test - verified sources"
python main.py
```

#### Test 2: Adversarial Sources
```bash
cd "Second test - fake sources"
python main.py
```

## Research Applications

This framework enables:
- **Trust dynamics study**: Understanding how deterministic scoring affects agent behavior
- **Decision pattern analysis**: Impact of different trust thresholds
- **Algorithm evaluation**: Testing modifications to scoring rules
- **Compliance testing**: Ensuring AI citations meet enterprise standards

## Key Insights

1. **Deterministic scoring works**: Rule-based heuristics successfully differentiate source quality
2. **No learning required**: Effective trust evaluation without ML/AI recursion
3. **Adversarial robustness**: System identifies and filters fabricated sources
4. **Transparent and auditable**: All decisions traceable through deterministic rules

## Technical Implementation

- **Language**: Python 3.x
- **Dependencies**: pandas, matplotlib, numpy
- **Reproducibility**: Fixed random seeds for consistent results
- **Logging**: Complete audit trails in build_log.txt

## Academic Use

This simulation is designed for:
- Research publications on multi-agent trust systems
- Educational purposes in trust and verification
- Algorithm development and testing
- Reproducible science with transparent methodology

## About Ancestor Lab

**Ancestor Lab** develops enterprise solutions for AI source reliability and compliance. The Ancestor Framework addresses the critical need for trustworthy citations in LLM outputs, particularly important for regulated industries and high-stakes applications.

## License

[To be determined - please specify your preferred license]

## Contact

For questions about the Ancestor Framework or collaboration opportunities, please contact through GitHub Issues.

## Citation

If you use this work in your research, please cite:
```
Ancestor Framework: Deterministic Trust Scoring for Multi-Agent Citation Systems
Ancestor Lab, 2025
https://github.com/Lu9er/ancestor-framework-simulation
```

---

*This repository demonstrates the Ancestor Framework's capability to influence agent behavior through deterministic trust scoring, providing a foundation for reliable AI citation systems in enterprise environments.*
