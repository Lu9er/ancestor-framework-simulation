# Multi-Agent Trust Simulation with Ancestor Verifier

## 🎯 Overview

This repository contains a multi-agent simulation system that demonstrates how a deterministic trust-scoring engine (called "Ancestor") influences citation behavior in cooperative systems. The simulation is designed for academic and research review purposes, using real, verifiable, and auditable data sources.

## 🏗️ System Architecture

The simulation consists of three primary agents:

1. **Claimant Agent**: Randomly selects citations from the dataset and makes factual claims
2. **Ancestor Verifier**: Scores the trustworthiness of citations using rule-based heuristics
3. **Consumer Agent**: Accepts or rejects claims based on the trust score threshold

## 📄 Input Data: `public_citation_sources.csv`

The simulation uses a real dataset of 100 verified citations with the following schema:

- **Category**: Source type (e.g., "Academic Research", "News Outlet", "Gov Report")
- **URL**: Full citation URL
- **Domain**: Domain name (e.g., "who.int", "bbc.com", "harvard.edu")
- **Age**: Original data shows "Ongoing" for all entries
- **Trust_Description**: Short justification of source trustworthiness

### ⚠️ Critical Note on Age Data Handling

**Original Dataset Issue**: All entries in `public_citation_sources.csv` contain "Ongoing" in the Age field, which would make age-based scoring impossible and unrealistic for simulation purposes.

**Solution Implemented**: To create a meaningful simulation that demonstrates the Ancestor scoring system's age-based penalties, the simulation generates realistic age values during runtime:

```python
# In ClaimantAgent.make_claim() method
age_days = random.randint(0, 365)  # Random age between 0-365 days
```

**Why This Approach**:
1. **Demonstrates Age Scoring Logic**: Shows how the Ancestor system would handle sources of varying ages
2. **Creates Realistic Scenarios**: Simulates real-world conditions where sources have different ages
3. **Maintains Reproducibility**: Uses fixed random seed (42) for consistent results
4. **Preserves Original Data**: No modification to the source CSV file

**Age Range Justification**:
- **0-365 days**: Represents sources from "today" to "one year old"
- **Realistic Distribution**: Covers fresh sources to moderately aged content
- **Scoring Impact**: Creates meaningful variance in trust scores (newer sources score higher)

## 🧠 Ancestor Trust Scoring Algorithm

The Ancestor Verifier implements a deterministic scoring system with the following logic:

### Base Scoring Formula

```python
score = 100 - (0.01 * age_days)
```

### Detailed Scoring Rules

#### 1. **Base Score**: 100 points
Every citation starts with a perfect score of 100.

#### 2. **Age Penalty**: -0.01 points per day
```python
age_penalty = 0.01 * age_days
score -= age_penalty
```

**Examples**:
- 0 days old: No penalty (100 points)
- 100 days old: -1.0 points (99 points)
- 365 days old: -3.65 points (96.35 points)

#### 3. **Domain-Based Penalties**

**Suspicious Domains**: -20 points
```python
if "clickbait" in domain or "unknown" in domain:
    score -= 20
```

**Commercial Domains**: -5 points (with academic exception)
```python
elif domain.endswith(".com") and "academic" not in category.lower():
    score -= 5
```

**Trusted Top-Level Domains**: No penalty
- `.edu` (Educational institutions)
- `.gov` (Government sites)
- `.int` (International organizations)
- `.org` (Organizations)

#### 4. **Content Bias Penalties**: -15 points
```python
if "biased" in trust_description or "satirical" in trust_description:
    score -= 15
```

#### 5. **Score Clamping**: Minimum 0
```python
score = max(score, 0)  # Ensures no negative scores
```

### Complete Scoring Example

**Example Citation**:
- Domain: `harvard.edu`
- Age: 50 days
- Category: "Academic Research"
- Trust Description: "Very High, leading university"

**Calculation**:
```
Initial Score: 100
Age Penalty: 100 - (0.01 × 50) = 100 - 0.5 = 99.5
Domain Check: .edu domain → No penalty
Bias Check: No bias keywords → No penalty
Final Score: 99.5
```

## 📊 Consumer Decision Logic

The Consumer Agent uses a simple threshold-based decision:

```python
ACCEPTANCE_THRESHOLD = 60.0
accepted = trust_score >= ACCEPTANCE_THRESHOLD
```

- **Score ≥ 60**: Claim accepted (1)
- **Score < 60**: Claim rejected (0)

## 🔄 Simulation Process

### Episode Flow (100 iterations)

1. **Claimant Phase**:
   - Randomly selects one row from `public_citation_sources.csv`
   - Generates random age (0-365 days)
   - Creates claim with citation data

2. **Verification Phase**:
   - Ancestor applies scoring algorithm
   - Calculates final trust score

3. **Consumer Phase**:
   - Evaluates trust score against threshold
   - Makes accept/reject decision

4. **Logging Phase**:
   - Records episode data to results

### Reproducibility

- **Fixed Random Seed**: `random.seed(42)` and `np.random.seed(42)`
- **Deterministic Scoring**: Rule-based heuristics with no randomness
- **Consistent Dataset**: Same CSV file for all runs

## 📈 Output Files

### `results.csv`
Complete simulation log with columns:
- `episode`: Episode number (1-100)
- `url`: Selected citation URL
- `domain`: Domain name
- `category`: Source category
- `age_days`: Generated age in days
- `score`: Calculated trust score
- `accepted`: Decision (1=accepted, 0=rejected)

### `trust_plot.png`
Matplotlib visualization containing:
- **Top Panel**: Trust scores across 100 episodes with acceptance threshold line
- **Bottom Panel**: Accept/reject decisions as binary plot

### `build_log.txt`
Complete execution audit trail documenting every step taken by the coding agent.

## 🚀 Running the Simulation

### Prerequisites
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas matplotlib numpy
```

### Execution
```bash
python main.py
```

### Expected Output
```
MULTI-AGENT TRUST SIMULATION WITH ANCESTOR VERIFIER
============================================================
[STEP 1] Loaded citation data from public_citation_sources.csv - 100 entries found
[STEP 2] Defined Ancestor scoring function with penalties for age, domain type, and bias keywords
[STEP 3] Starting 100-episode simulation with Claimant, Verifier, and Consumer agents
[STEP 4] Completed 100 episodes with trust scoring and decision logging
...

=== SIMULATION SUMMARY ===
Total Episodes: 100
Claims Accepted: X (X.X%)
Claims Rejected: X (X.X%)
Average Trust Score: XX.XX
Score Range: XX.XX - XX.XX
```

## 📊 Expected Results Analysis

Based on the scoring algorithm and dataset characteristics:

### High Acceptance Rate Expected
Most citations should be accepted because:
1. **Quality Dataset**: All sources are pre-verified as trustworthy
2. **Trusted Domains**: Many `.edu`, `.gov`, `.org` domains (no penalties)
3. **Conservative Age Range**: 0-365 days creates minimal age penalties
4. **No Bias Content**: Trust descriptions are positive, avoiding bias penalties

### Score Distribution
- **High Scores (90-100)**: `.edu/.gov/.org` domains with low age
- **Medium Scores (85-95)**: `.com` domains with academic content
- **Lower Scores (60-85)**: Older `.com` domains with penalties

## 🔍 Code Structure

### Main Classes

#### `AncestorVerifier`
Implements the deterministic trust scoring engine with configurable penalties.

#### `ClaimantAgent`
Handles random citation selection and realistic age generation.

#### `ConsumerAgent`
Makes binary accept/reject decisions based on trust threshold.

#### `TrustSimulation`
Orchestrates the complete simulation workflow and output generation.

## 🎯 Research Applications

This simulation enables researchers to:

1. **Study Trust Dynamics**: How deterministic scoring affects agent behavior
2. **Analyze Decision Patterns**: Impact of different threshold values
3. **Evaluate Scoring Algorithms**: Test modifications to Ancestor's rules
4. **Compare Trust Systems**: Benchmark against other verification approaches

## ⚠️ Important Notes

### Data Authenticity
- **Real Sources**: All URLs and domains from actual reputable sources
- **No Synthetic Data**: No placeholder or fake citations used
- **Verifiable Results**: All claims can be traced to original dataset

### Age Data Methodology
- **Generated Ages**: Realistic 0-365 day range for meaningful scoring
- **Fixed Seed**: Reproducible results across runs
- **Documented Approach**: Clear explanation of why generation was necessary

### Limitations
- **Simplified Consumer**: Binary threshold decision (could be enhanced)
- **Static Scoring**: No learning or adaptation in Ancestor
- **Limited Age Range**: Real-world sources might be much older

## 📝 Files Overview

- `main.py`: Complete simulation implementation
- `public_citation_sources.csv`: Input dataset (100 verified citations)
- `results.csv`: Simulation episode results
- `trust_plot.png`: Visualization of trust scores and decisions
- `build_log.txt`: Agent execution audit trail
- `README.md`: This documentation file

## 🤝 Academic Use

This simulation is designed for:
- **Research Publications**: Demonstrating multi-agent trust systems
- **Educational Purposes**: Teaching trust and verification concepts
- **Algorithm Development**: Testing trust scoring approaches
- **Reproducible Science**: All data and methods are transparent

For questions about methodology or implementation details, refer to the source code comments and build log for complete transparency.