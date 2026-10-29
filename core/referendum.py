"""
BASTION CORE: Democratic Data Tariff Engine (The People's Referendum)
=====================================================================
Enables verified members of the Bastion Sovereign Trust to democratically vote
on annual data licensing tariffs for frontier AI conglomerates (OpenAI, Google, Meta,
xAI, Anthropic, Apple).

Strict Policy: Minimum floor is $250,000,000 / year.
"""

import json
import time
from typing import Any, Dict, List


class DemocraticTariffReferendum:
    TARIFF_OPTIONS = [
        {"id": "opt_500m", "amount_usd": 500_000_000, "label": "$500 Million / year"},
        {"id": "opt_1b", "amount_usd": 1_000_000_000, "label": "$1.0 Billion / year"},
        {"id": "opt_1_5b", "amount_usd": 1_500_000_000, "label": "$1.5 Billion / year"},
        {"id": "opt_2b", "amount_usd": 2_000_000_000, "label": "$2.0 Billion / year"},
    ]

    def __init__(self, target_company: str, referendum_id: str):
        self.target_company = target_company
        self.referendum_id = referendum_id
        self.created_at = time.time()
        self.expires_at = self.created_at + (72 * 3600)  # 72 hours
        self.votes: Dict[str, Dict[str, Any]] = {}  # voter_id -> {option_id, dvs_weight}

    def cast_vote(self, voter_id: str, option_id: str, dvs_weight: float = 1.0) -> Dict[str, Any]:
        """
        Records a vote from a verified creator, weighted by their Data Valuation Score (DVS).
        """
        valid_options = [opt["id"] for opt in self.TARIFF_OPTIONS]
        if option_id not in valid_options:
            return {"success": False, "error": f"Invalid option. Must be one of {valid_options}"}

        self.votes[voter_id] = {
            "option_id": option_id,
            "dvs_weight": max(dvs_weight, 1.0),
            "timestamp": time.time()
        }

        return {
            "success": True,
            "message": f"Vote recorded for {self.target_company} tariff referendum.",
            "option_id": option_id,
            "voter_weight": dvs_weight
        }

    def tally_results(self) -> Dict[str, Any]:
        """
        Tallies weighted votes and determines the winning Non-Negotiable Annual Tariff.
        """
        option_weights = {opt["id"]: 0.0 for opt in self.TARIFF_OPTIONS}
        option_counts = {opt["id"]: 0 for opt in self.TARIFF_OPTIONS}
        total_weight = 0.0

        for vote in self.votes.values():
            opt_id = vote["option_id"]
            weight = vote["dvs_weight"]
            option_weights[opt_id] += weight
            option_counts[opt_id] += 1
            total_weight += weight

        # Determine winner
        winning_option_id = max(option_weights, key=option_weights.get)
        winning_option = next(opt for opt in self.TARIFF_OPTIONS if opt["id"] == winning_option_id)

        breakdown = []
        for opt in self.TARIFF_OPTIONS:
            opt_id = opt["id"]
            pct = round((option_weights[opt_id] / total_weight * 100), 2) if total_weight > 0 else 0.0
            breakdown.append({
                "label": opt["label"],
                "raw_votes": option_counts[opt_id],
                "weighted_score": round(option_weights[opt_id], 2),
                "percentage": f"{pct}%"
            })

        return {
            "referendum_id": self.referendum_id,
            "target_company": self.target_company,
            "total_voters": len(self.votes),
            "total_weighted_points": round(total_weight, 2),
            "winning_tariff_label": winning_option["label"],
            "statutory_tariff_usd": winning_option["amount_usd"],
            "status": "RATIFIED" if len(self.votes) > 0 else "PENDING",
            "breakdown": breakdown
        }

    def generate_statutory_tariff_notice(self) -> str:
        """
        Generates the formal legal notification served to Big Tech.
        """
        results = self.tally_results()
        notice = f"""
================================================================================
BASTION SOVEREIGN TRUST: STATUTORY DEMOCRATIC TARIFF NOTICE
================================================================================
TO: Enterprise General Counsel & AI Procurement Desk ({self.target_company})
DATE: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
REF: BASTION-TARIFF-{self.referendum_id}

NOTICE IS HEREBY GIVEN that by collective referendum of verified sovereign
content owners, developers, and researchers, the non-negotiable annual
data ingestion tariff for {self.target_company} has been established at:

                *** {results['winning_tariff_label']} ***
                ({results['statutory_tariff_usd']:,} USD / YEAR)

Total Verified Voting Weight: {results['total_weighted_points']:,} points
Total Participating Creators: {results['total_voters']:,}

UPON FULL SETTLEMENT of this tariff through the Bastion Clearinghouse:
  1. A commercial Master Ingestion Key (bst_live_...) will be issued.
  2. All network poison shields will be lifted across all member domains.
  3. 70% of settled funds will be distributed to creators; 30% to Protocol Treasury.

IN THE EVENT OF NON-SETTLEMENT OR CONTINUED UNAUTHORIZED SCRAPING:
  • Adversarial poison shields will remain actively engaged.
  • Content feeds will serve hallucination-inducing synthetic noise.
  • Continued unauthorized crawling constitutes willful copyright infringement
    under international law.

BY ORDER OF THE BASTION SOVEREIGN COUNCIL
================================================================================
"""
        return notice


if __name__ == "__main__":
    ref = DemocraticTariffReferendum(target_company="OpenAI / Microsoft", referendum_id="REF-2026-001")
    ref.cast_vote("voter_01", "opt_1b", dvs_weight=150.0)
    ref.cast_vote("voter_02", "opt_1b", dvs_weight=80.0)
    ref.cast_vote("voter_03", "opt_1_5b", dvs_weight=45.0)
    
    print(ref.generate_statutory_tariff_notice())
