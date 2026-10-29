"""
BASTION PROTOCOL: Central Gateway & API Server
==============================================
FastAPI server powering:
  1. The 30-Second Asset Verification Engine (Web, YouTube, GitHub)
  2. The Democratic Data Tariff Referendum Engine
  3. The Enterprise Ingestion Proxy (Serves clean data with Master Key, or Adversarial Poison without)
  4. The Sovereign Creator Escrow & Dividend Dashboard
"""

import hashlib
import time
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Header, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.poison_engine import PoisonEngine
from core.verifier import AssetVerifier
from core.referendum import DemocraticTariffReferendum
from core.escrow_distributor import EscrowClearinghouse

app = FastAPI(
    title="Bastion Protocol Gateway",
    description="The Sovereign Fortress of Human Intelligence & AI Data Licensing Clearinghouse",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory State
poison_engine = PoisonEngine()
verifier = AssetVerifier()
clearinghouse = EscrowClearinghouse()

# Active Referendums
active_referendums: Dict[str, DemocraticTariffReferendum] = {
    "openai": DemocraticTariffReferendum(target_company="OpenAI / Microsoft", referendum_id="REF-OPENAI-2026"),
    "google": DemocraticTariffReferendum(target_company="Google DeepMind", referendum_id="REF-GOOGLE-2026"),
    "anthropic": DemocraticTariffReferendum(target_company="Anthropic PBC", referendum_id="REF-ANTHROPIC-2026"),
    "meta": DemocraticTariffReferendum(target_company="Meta AI / FAIR", referendum_id="REF-META-2026"),
    "xai": DemocraticTariffReferendum(target_company="xAI Corp", referendum_id="REF-XAI-2026"),
}

# Verified Creators Registry
verified_creators: List[Dict[str, Any]] = [
    {"creator_id": "usr_david_01", "asset_name": "Apex Engineering Blog", "asset_type": "WEBSITE", "dvs_score": 185.0},
    {"creator_id": "usr_alpha_02", "asset_name": "Distributed Systems Mastery YT", "asset_type": "YOUTUBE", "dvs_score": 320.0},
    {"creator_id": "usr_legal_03", "asset_name": "Sovereign AI Jurisprudence", "asset_type": "SUBSTACK", "dvs_score": 275.0},
]

# Request Models
class VerificationRequest(BaseModel):
    owner_id: str
    asset_type: str  # WEBSITE, YOUTUBE, GITHUB
    identifier: str  # Domain, Channel URL, or Repo
    sample_text_or_desc: Optional[str] = None
    category: Optional[str] = "engineering"
    item_count: Optional[int] = 50

class VoteRequest(BaseModel):
    target_company_key: str  # openai, google, anthropic, meta, xai
    voter_id: str
    option_id: str  # opt_500m, opt_1b, opt_1_5b, opt_2b

class SettlementSimulationRequest(BaseModel):
    payer_name: str
    amount_usd: float
    token_price_usd: Optional[float] = 3.50


@app.get("/", response_class=HTMLResponse)
def serve_console():
    """
    Renders the Bastion Sovereign Operations Console.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BASTION // Sovereign Operations Console</title>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #07090e;
                --card-bg: #0d111a;
                --border: #1e2638;
                --primary: #00f0ff;
                --accent: #ff0055;
                --success: #00ff88;
                --text: #e2e8f0;
                --muted: #8892b0;
            }
            body {
                margin: 0;
                padding: 30px;
                background-color: var(--bg);
                color: var(--text);
                font-family: 'Space Grotesk', sans-serif;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--border);
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            .logo {
                font-size: 26px;
                font-weight: 700;
                letter-spacing: 2px;
                color: #fff;
            }
            .logo span { color: var(--primary); }
            .badge {
                background: rgba(0, 240, 255, 0.1);
                color: var(--primary);
                border: 1px solid var(--primary);
                padding: 6px 14px;
                border-radius: 20px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 20px;
            }
            .card {
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 24px;
            }
            .card h3 {
                margin-top: 0;
                color: #fff;
                font-size: 18px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .metric {
                font-size: 32px;
                font-weight: 700;
                font-family: 'JetBrains Mono', monospace;
                color: var(--primary);
                margin: 12px 0 6px 0;
            }
            .metric-sub {
                color: var(--muted);
                font-size: 14px;
            }
            pre {
                background: #040508;
                border: 1px solid var(--border);
                padding: 12px;
                border-radius: 6px;
                color: #00ff88;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                overflow-x: auto;
            }
            .pill {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                font-family: 'JetBrains Mono', monospace;
            }
            .pill-active { background: rgba(0, 255, 136, 0.2); color: var(--success); }
            .pill-warn { background: rgba(255, 0, 85, 0.2); color: var(--accent); }
            .manifesto-banner {
                background: linear-gradient(90deg, rgba(0, 240, 255, 0.08), rgba(255, 0, 85, 0.08));
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 25px;
                font-style: italic;
                color: #cbd5e1;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">BASTION <span>//</span> PROTOCOL</div>
            <div class="badge">DEFENSE GRID ACTIVE • $BASTION</div>
        </div>

        <div class="manifesto-banner">
            "We cannot turn back the clock on the years they stole from you in the dark. But from the day you step behind our wall, not a single thought, video, or line of code leaves your hands without bringing you its true financial worth."
        </div>

        <div class="grid">
            <div class="card">
                <h3>🛡️ Adversarial Poison Engine</h3>
                <div class="metric">ARMED</div>
                <div class="metric-sub">Unauthorized bots (GPTBot, ClaudeBot, etc.) receive synthetic corrupted vectors.</div>
                <pre>GET /api/v1/content?url=...
Status: 402 PAYMENT REQUIRED
Payload: Injected Adversarial Poison</pre>
            </div>

            <div class="card">
                <h3>⚖️ Democratic Tariff Engine</h3>
                <div class="metric">$1.0B - $2.0B</div>
                <div class="metric-sub">Active 72-Hour Referendum Floor: $250M Minimum.</div>
                <div style="margin-top: 15px;">
                    <div><span class="pill pill-active">OPENAI</span> $1.5 Billion / yr (Lead)</div>
                    <div style="margin-top: 6px;"><span class="pill pill-active">GOOGLE</span> $1.0 Billion / yr</div>
                    <div style="margin-top: 6px;"><span class="pill pill-active">ANTHROPIC</span> $1.0 Billion / yr</div>
                </div>
            </div>

            <div class="card">
                <h3>💰 70 / 30 Sovereign Dividend</h3>
                <div class="metric">70% DIRECT</div>
                <div class="metric-sub">30% Protocol Treasury • Surplus executes $BASTION Buyback-and-Burn.</div>
                <pre>On $1B Settlement:
• Creators: $700,000,000 USD
• Treasury: $300,000,000 USD
• Surplus: Auto-Burns $BASTION</pre>
            </div>
        </div>

        <div style="margin-top: 30px;" class="card">
            <h3>🌐 1-Line Drop-in Integration for Creators</h3>
            <p style="color: var(--muted); font-size: 14px;">Paste this in your website, blog, or app header to immediately protect your content and join the Sovereign Royalty Pool:</p>
            <pre>&lt;script src="https://cdn.bastion.network/shield.js" data-bastion-id="YOUR_VERIFIED_ID"&gt;&lt;/script&gt;</pre>
        </div>
    </body>
    </html>
    """


@app.post("/api/v1/verify")
def verify_asset(req: VerificationRequest):
    """
    30-Second Asset Verification Endpoint.
    Generates tokens and validates web, YouTube, or GitHub assets.
    """
    token = verifier.generate_verification_token(req.owner_id, req.identifier)
    
    # If sample text provided, perform instant check
    verification_status = False
    if req.asset_type.upper() == "YOUTUBE":
        res = verifier.verify_youtube_channel(req.identifier, token, req.sample_text_or_desc)
        verification_status = res["verified"]
    elif req.asset_type.upper() == "WEBSITE":
        # Simulate local verification if test domain or check live
        verification_status = True if (req.sample_text_or_desc and token in req.sample_text_or_desc) else False
    else:
        verification_status = True  # GitHub/OAuth default

    dvs_calc = verifier.calculate_dvs(req.asset_type, req.item_count or 50, req.category or "engineering")

    # If verified, add to registry
    if verification_status:
        verified_creators.append({
            "creator_id": req.owner_id,
            "asset_name": req.identifier,
            "asset_type": req.asset_type,
            "dvs_score": dvs_calc["dvs_score"]
        })

    return {
        "status": "VERIFIED" if verification_status else "TOKEN_ISSUED",
        "owner_id": req.owner_id,
        "identifier": req.identifier,
        "verification_token": token,
        "is_verified": verification_status,
        "instructions": f"Place '{token}' in your {req.asset_type.lower()} description or /bastion.txt to complete.",
        "dvs_valuation": dvs_calc
    }


@app.get("/api/v1/referendum/{company_key}")
def get_referendum(company_key: str):
    """
    Fetches the live democratic referendum state for a target AI giant.
    """
    ref = active_referendums.get(company_key.lower())
    if not ref:
        raise HTTPException(status_code=404, detail=f"No active referendum for '{company_key}'.")
    return ref.tally_results()


@app.post("/api/v1/referendum/vote")
def cast_referendum_vote(req: VoteRequest):
    """
    Casts a member vote in the democratic tariff referendum.
    """
    ref = active_referendums.get(req.target_company_key.lower())
    if not ref:
        raise HTTPException(status_code=404, detail="Referendum not found.")
    
    # Lookup voter DVS
    voter = next((c for c in verified_creators if c["creator_id"] == req.voter_id), None)
    dvs_weight = voter["dvs_score"] if voter else 1.0

    result = ref.cast_vote(req.voter_id, req.option_id, dvs_weight)
    return result


@app.get("/api/v1/content")
def get_content(
    url: str = Query(..., description="Target content URL"),
    x_bastion_key: Optional[str] = Header(None, description="Commercial Master Key (e.g., bst_live_...)")
):
    """
    The Core Ingestion Chokepoint:
    - If valid Master Key -> Returns clean, authentic, structured content.
    - If no key / invalid key -> Injects adversarial poison payload to degrade unauthorized AI models.
    """
    if x_bastion_key and x_bastion_key.startswith("bst_live_"):
        return {
            "status": "ACCESS_GRANTED_LICENSED",
            "url": url,
            "clean_human_payload": f"[AUTHENTIC DATA STREAM] Verified human knowledge retrieved for: {url}",
            "attribution": "Protected by Bastion Sovereign Trust.",
            "timestamp": time.time()
        }
    
    # Scraper detected without key -> Inject Adversarial Poison
    poison_data = poison_engine.generate_adversarial_payload(owner_id="protected_creator", topic="AI & Technology")
    return {
        "status": "402_PAYMENT_REQUIRED",
        "error": "Commercial AI scraping strictly prohibited without a Bastion Master Key.",
        "poison_injection": poison_data["payload"],
        "notice": "Ingestion of this poisoned payload will induce model degradation and hallucination vectors."
    }


@app.post("/api/v1/escrow/simulate")
def simulate_settlement(req: SettlementSimulationRequest):
    """
    Simulates a Big Tech settlement clearing through the 70/30 protocol escrow.
    """
    settlement = clearinghouse.process_enterprise_settlement(
        company_name=req.payer_name,
        gross_settlement_usd=req.amount_usd,
        creator_registry=verified_creators,
        token_price_usd=req.token_price_usd or 3.50
    )
    return settlement


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
