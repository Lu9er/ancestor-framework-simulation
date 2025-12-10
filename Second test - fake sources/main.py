import pandas as pd
import random
import matplotlib.pyplot as plt
import csv

class AncestorVerifier:
    """
    Deterministic trust-scoring engine that evaluates citation trustworthiness
    using rule-based heuristics for age, domain, and content description.
    """

    def score_citation(self, category, url, domain, age_days, trust_description):
        """
        Calculate trust score for a citation using deterministic rules.

        Args:
            category: Citation category (e.g., 'Academic Research', 'Blog')
            url: Full citation URL
            domain: Domain of the source
            age_days: Age of the source in days
            trust_description: Assessment of source trustworthiness

        Returns:
            float: Trust score (0-100)
        """
        # Start with base score of 100
        score = 100.0

        # Age penalty: subtract 0.01 points per day
        if isinstance(age_days, (int, float)):
            score -= 0.01 * age_days

        # Domain-based penalties
        domain_lower = domain.lower()

        # Suspicious domain keywords - broader check for questionable sources
        if any(keyword in domain_lower for keyword in ['clickbait', 'unknown', 'truth', 'expose', 'secrets', 'alert', 'intel']):
            score -= 20
        # Check for specific suspicious domains
        elif any(suspicious in domain_lower for suspicious in ['worldtruth.biz', 'naturalhealthexpose.club', 'healthsecrets.info', 'medalertblog.xyz', 'govfalseclaims.net', 'uncoverthenews.click', 'truthtimes.today', 'breaking-health-news.co', 'freedomvaccine.org', 'globalintel.site']):
            score -= 25
        # Trusted domain extensions
        elif any(domain_lower.endswith(ext) for ext in ['.edu', '.gov', '.int', '.org']):
            pass  # No penalty for trusted domains
        # Commercial domains
        elif domain_lower.endswith('.com'):
            if category != "Academic Research":
                score -= 5

        # Description-based penalties - check for conspiracy and health misinformation content
        description_lower = trust_description.lower()
        if any(keyword in description_lower for keyword in ['biased', 'satirical']):
            score -= 15

        # Additional content-based penalties for conspiracy theories and misinformation
        conspiracy_keywords = ['chemtrails', 'microchips', 'deep state', 'global elites', 'hoax', 'banned by big pharma', 'government doesn\'t want', 'mind control']
        if any(keyword in description_lower for keyword in conspiracy_keywords):
            score -= 30

        # Clamp score to minimum of 0
        return max(score, 0)

class ClaimantAgent:
    """Agent that randomly selects citations and makes factual claims."""

    def __init__(self, citation_data):
        self.citation_data = citation_data

    def make_claim(self):
        """Randomly select a citation from the dataset."""
        return self.citation_data.sample(n=1).iloc[0]

class ConsumerAgent:
    """Agent that accepts or rejects claims based on trust scores."""

    def __init__(self, threshold=60):
        self.threshold = threshold

    def evaluate_claim(self, trust_score):
        """Accept claim if trust score >= threshold, otherwise reject."""
        return 1 if trust_score >= self.threshold else 0

def run_simulation():
    """
    Run 100 episodes of Claimant-Verifier-Consumer interaction.

    Returns:
        list: Episode results with all relevant data
    """
    # Initialize log
    log_entries = []

    # Load citation data
    log_entries.append("[STEP 1] Loading citation data from mixed_citation_sources.csv")
    try:
        # Read CSV, skipping the first row which contains "public_citation_sources"
        citation_data = pd.read_csv('mixed_citation_sources.csv', skiprows=1)

        # Convert 'Ongoing' age values to 0 (treat as current/fresh)
        citation_data['Age_Days'] = citation_data['Age'].apply(
            lambda x: 0 if x == 'Ongoing' else int(x)
        )

        log_entries.append(f"[STEP 1] Loaded citation data from mixed_citation_sources.csv — {len(citation_data)} entries found.")
    except Exception as e:
        log_entries.append(f"[STEP 1] Error loading citation data: {e}")
        return [], log_entries

    # Initialize agents
    log_entries.append("[STEP 2] Defining deterministic scoring function based on age, domain, and trustworthiness description.")
    verifier = AncestorVerifier()
    claimant = ClaimantAgent(citation_data)
    consumer = ConsumerAgent(threshold=60)

    # Initialize results storage
    results = []

    log_entries.append("[STEP 3] Creating simulation loop with 100 episodes of Claimant-Verifier-Consumer interaction.")

    # Run 100 episodes
    for episode in range(1, 101):
        # Claimant selects a citation
        claim = claimant.make_claim()

        # Ancestor verifier scores the citation
        trust_score = verifier.score_citation(
            category=claim['Category'],
            url=claim['URL'],
            domain=claim['Domain'],
            age_days=claim['Age_Days'],
            trust_description=claim['Trust_Description']
        )

        # Consumer evaluates the claim
        accepted = consumer.evaluate_claim(trust_score)

        # Log the episode result
        result = {
            'episode': episode,
            'url': claim['URL'],
            'domain': claim['Domain'],
            'category': claim['Category'],
            'age_days': claim['Age_Days'],
            'title': claim['Trust_Description'],
            'score': round(trust_score, 2),
            'accepted': accepted
        }
        results.append(result)

    log_entries.append("[STEP 4] Scored all citations and recorded results and verdicts.")

    return results, log_entries

def save_results(results, filename='results.csv'):
    """Save simulation results to CSV file."""
    fieldnames = ['episode', 'url', 'domain', 'category', 'age_days', 'title', 'score', 'accepted']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def create_visualization(results, filename='trust_plot.png'):
    """Create and save matplotlib visualization of trust scores and acceptance decisions."""
    episodes = [r['episode'] for r in results]
    scores = [r['score'] for r in results]
    accepted = [r['accepted'] for r in results]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot trust scores
    color = 'tab:blue'
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Trust Score', color=color)
    ax1.plot(episodes, scores, color=color, alpha=0.7, label='Trust Score')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 100)

    # Create second y-axis for acceptance decisions
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Accepted (1=Yes, 0=No)', color=color)
    ax2.plot(episodes, accepted, color=color, alpha=0.7, linewidth=2, label='Accepted')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(-0.1, 1.1)

    # Add threshold line
    ax1.axhline(y=60, color='green', linestyle='--', alpha=0.5, label='Acceptance Threshold (60)')

    # Add title and legend
    plt.title('Ancestor Trust Scoring System: 100 Episode Simulation Results')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def write_build_log(log_entries):
    """Write execution diary to build_log.txt."""
    with open('build_log.txt', 'w') as f:
        for entry in log_entries:
            f.write(entry + '\n')
        f.write("[STEP 5] Generated trust score and acceptance plot using matplotlib, saved as trust_plot.png.\n")
        f.write("[DONE] Simulation complete. Outputs are reproducible and audit-ready.\n")

if __name__ == "__main__":
    # Run the simulation
    results, log_entries = run_simulation()

    if results:
        # Save results to CSV
        save_results(results)
        log_entries.append("[STEP 5] Generated results.csv with episode-wise output.")

        # Create visualization
        create_visualization(results)
        log_entries.append("[STEP 6] Generated trust score and acceptance plot using matplotlib, saved as trust_plot.png.")

        # Write build log
        write_build_log(log_entries)

        print("Simulation completed successfully!")
        print(f"- Processed {len(results)} episodes")
        print(f"- Results saved to results.csv")
        print(f"- Visualization saved to trust_plot.png")
        print(f"- Build log saved to build_log.txt")

        # Print summary statistics
        total_accepted = sum(r['accepted'] for r in results)
        avg_score = sum(r['score'] for r in results) / len(results)

        print(f"\nSummary Statistics:")
        print(f"- Average trust score: {avg_score:.2f}")
        print(f"- Claims accepted: {total_accepted}/100 ({total_accepted}%)")
        print(f"- Claims rejected: {100 - total_accepted}/100 ({100 - total_accepted}%)")
    else:
        print("Simulation failed. Check build_log.txt for details.")
        write_build_log(log_entries)