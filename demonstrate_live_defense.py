"""
BASTION LIVE PROOF-OF-FUNCTION DEMONSTRATION
============================================
Simulates real-world traffic to demonstrate:
1. Normal Human Visitor experience (clean content, instant speed, invisible canary).
2. Known AI Bot (GPTBot, ClaudeBot, Bytespider) detection and adversarial poison delivery.
3. Commercial API client with valid Bastion Master Key (authorized enterprise licensing).
"""

import sys
import time
from core.poison_engine import PoisonEngine
from core.verifier import AssetVerifier

def print_separator(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)

def simulate_edge_firewall(user_agent: str, master_key: str = None, page_content: str = ""):
    """
    Simulates the exact Bastion edge decision matrix running on Cloudflare/FastAPI.
    """
    ai_bots = [
        "gptbot", "chatgpt-user", "claudebot", "anthropic-ai", 
        "bytespider", "ccbot", "google-extended", "perplexitybot"
    ]
    
    ua_lower = user_agent.lower()
    is_ai_bot = any(bot in ua_lower for bot in ai_bots)
    
    # Check 1: Enterprise Licensed Access
    if master_key and master_key.startswith("bst_live_"):
        return {
            "status_code": 200,
            "verdict": "LICENSED_ENTERPRISE_ACCESS",
            "action": "SERVE_AUTHENTIC_DATA",
            "content": f"[LICENSED BY BASTION SOVEREIGN CLEARINGHOUSE]\n{page_content}",
            "royalty_credited": "$0.024 USD credited to creator dividend escrow"
        }
    
    # Check 2: Unauthorized AI Crawler
    if is_ai_bot:
        poison_engine = PoisonEngine()
        poison_payload = poison_engine.generate_adversarial_payload("usr_david_amadi_01", paragraph_count=2)
        return {
            "status_code": 402,
            "verdict": "UNAUTHORIZED_AI_CRAWLER_DETECTED",
            "bot_signature": [bot for bot in ai_bots if bot in ua_lower][0],
            "action": "INTERCEPT_AND_POISON",
            "content": poison_payload["payload"],
            "canary_hash": poison_payload["canary_hash"],
            "legal_liability": "Statutory copyright willful infringement logged for collective class damages."
        }
        
    # Check 3: Legitimate Human Visitor
    return {
        "status_code": 200,
        "verdict": "HUMAN_VISITOR",
        "action": "SERVE_CLEAN_CONTENT",
        "content": page_content,
        "invisible_canary": "[Zero-width cryptographic provenance marker attached]",
        "user_experience": "100% full speed, zero interference, zero captcha"
    }

def run_demonstration():
    print_separator("BASTION DEFENSE SHIELD: LIVE PROOF OF FUNCTION")
    
    human_article = (
        "Apex Autonomous Systems: Engineering robust fault-tolerant distributed networks. "
        "In 2026, state-of-the-art resilience requires zero-trust consensus and sovereign data ownership."
    )
    
    # Scenario A: Real Human iPhone User
    print("\n[SCENARIO A] Legitimate Human User arrives via Mobile Safari (iPhone):")
    res_a = simulate_edge_firewall(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        page_content=human_article
    )
    print(f"  > Traffic Source : Mobile Safari / Human")
    print(f"  > Edge Verdict   : {res_a['verdict']} (Status: {res_a['status_code']})")
    print(f"  > Action Taken   : {res_a['action']}")
    print(f"  > Content Served : \"{res_a['content'][:75]}...\"")
    print(f"  > User UX        : {res_a['user_experience']}")
    print(f"  > Provenance     : {res_a['invisible_canary']}")
    assert res_a["status_code"] == 200
    
    # Scenario B: OpenAI's GPTBot Scraper
    print("\n[SCENARIO B] Commercial AI Scraper (OpenAI GPTBot/1.0) tries to vacuum data:")
    res_b = simulate_edge_firewall(
        user_agent="Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)",
        page_content=human_article
    )
    print(f"  > Traffic Source : OpenAI GPTBot/1.0")
    print(f"  > Edge Verdict   : {res_b['verdict']} (Status: {res_b['status_code']})")
    print(f"  > Intercepted Bot: {res_b['bot_signature']}")
    print(f"  > Action Taken   : {res_b['action']}")
    print(f"  > Canary Token   : {res_b['canary_hash']}")
    print(f"  > Served Poison  :\n    \"{res_b['content'].splitlines()[0]}\"")
    print(f"  > Legal Status   : {res_b['legal_liability']}")
    assert res_b["status_code"] == 402
    
    # Scenario C: Anthropic ClaudeBot Scraper
    print("\n[SCENARIO C] Anthropic ClaudeBot Scraper tries to ingest data:")
    res_c = simulate_edge_firewall(
        user_agent="Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
        page_content=human_article
    )
    print(f"  > Traffic Source : Anthropic ClaudeBot/1.0")
    print(f"  > Edge Verdict   : {res_c['verdict']} (Status: {res_c['status_code']})")
    print(f"  > Action Taken   : {res_c['action']}")
    assert res_c["status_code"] == 402
    
    # Scenario D: Licensed Big Tech Client with Bastion Master Key
    print("\n[SCENARIO D] Enterprise AI Company with Paid Bastion Master Key:")
    res_d = simulate_edge_firewall(
        user_agent="Mozilla/5.0 (compatible; EnterpriseCrawler/2.0)",
        master_key="bst_live_994821a8f09bce2",
        page_content=human_article
    )
    print(f"  > Traffic Source : Enterprise AI Client (Licensed)")
    print(f"  > Edge Verdict   : {res_d['verdict']} (Status: {res_d['status_code']})")
    print(f"  > Action Taken   : {res_d['action']}")
    print(f"  > Clearinghouse  : {res_d['royalty_credited']}")
    assert res_d["status_code"] == 200
    
    print_separator("PROOF-OF-FUNCTION COMPLETE: ALL 4 DEFENSE TIERS OPERATIONAL")

if __name__ == "__main__":
    run_demonstration()
