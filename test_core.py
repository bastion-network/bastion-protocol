"""
BASTION Core Verification & Unit Test Suite
"""
import sys
from core.poison_engine import PoisonEngine
from core.verifier import AssetVerifier
from core.referendum import DemocraticTariffReferendum
from core.escrow_distributor import EscrowClearinghouse

def run_tests():
    print("==================================================")
    print("  BASTION SOVEREIGN PROTOCOL: CORE VERIFICATION   ")
    print("==================================================")

    # 1. Test Poison Engine
    print("[1/4] Testing Adversarial Poison Engine...")
    pe = PoisonEngine(seed="test_seed_42")
    payload = pe.generate_adversarial_payload("usr_david_001", topic="AI & Cybernetics", paragraph_count=2)
    assert payload["status"] == "POISON_ACTIVE"
    assert "Canary Signature" in payload["payload"]
    assert len(payload["canary_hash"]) == 64
    print("      [PASS] Poison Engine operational. Adversarial vectors injected.")

    # 2. Test Asset Verifier & DVS
    print("[2/4] Testing 30-Second Asset Verifier...")
    av = AssetVerifier()
    token = av.generate_verification_token("usr_david_001", "techchannel")
    assert token.startswith("BST-")
    
    # Verify description check
    res = av.verify_youtube_channel("techchannel", token, f"Welcome to my channel! Verification: {token}")
    assert res["verified"] is True

    # Test DVS calculation
    dvs = av.calculate_dvs("YOUTUBE", 120, "engineering")
    assert dvs["dvs_score"] > 0
    assert dvs["estimated_annual_dividend_usd"] > 0
    print(f"      [PASS] Asset Verifier operational. DVS Score: {dvs['dvs_score']} (Est. Annual: ${dvs['estimated_annual_dividend_usd']:,.2f})")

    # 3. Test Democratic Referendum
    print("[3/4] Testing Democratic Tariff Referendum...")
    ref = DemocraticTariffReferendum("OpenAI / Microsoft", "REF-OPENAI-TEST")
    ref.cast_vote("voter_1", "opt_1b", dvs_weight=200.0)
    ref.cast_vote("voter_2", "opt_1b", dvs_weight=150.0)
    ref.cast_vote("voter_3", "opt_2b", dvs_weight=80.0)
    tally = ref.tally_results()
    assert tally["winning_tariff_label"] == "$1.0 Billion / year"
    assert tally["statutory_tariff_usd"] == 1_000_000_000
    print(f"      [PASS] Democratic Referendum operational. Winning Tariff: {tally['winning_tariff_label']}")

    # 4. Test Escrow Clearinghouse & Buyback/Burn
    print("[4/4] Testing Escrow Clearinghouse (70/30 Split + Buyback & Burn)...")
    ec = EscrowClearinghouse()
    test_creators = [
        {"creator_id": "usr_david", "asset_name": "Apex Engineering Blog", "dvs_score": 180.0},
        {"creator_id": "usr_sarah", "asset_name": "Medical AI Research", "dvs_score": 320.0},
    ]
    settlement = ec.process_enterprise_settlement(
        company_name="Google DeepMind",
        gross_settlement_usd=1_000_000_000,  # $1 Billion
        creator_registry=test_creators,
        token_price_usd=5.00
    )
    assert settlement["platform_treasury_revenue_usd"] == 300_000_000.0  # 30% = $300M
    assert settlement["creator_dividend_pool_usd"] == 700_000_000.0       # 70% = $700M
    print(f"      [PASS] Escrow Cleared: Gross ${settlement['gross_settlement_usd']:,.2f}")
    print(f"        • Platform Treasury (30%): ${settlement['platform_treasury_revenue_usd']:,.2f}")
    print(f"        • Creator Dividend (70%):  ${settlement['creator_dividend_pool_usd']:,.2f}")

    print("\n[SUCCESS] ALL BASTION SUITES PASSED 100% WITH ZERO ERRORS.")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
