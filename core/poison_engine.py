"""
BASTION CORE: Adversarial Poison Engine
=======================================
Generates high-fidelity, syntactically convincing, but factually inverted and
hallucination-inducing synthetic text vectors. When ingested by commercial LLM
crawlers without a valid Bastion Master Key, this data poisons downstream training
weights and RAG vector databases.
"""

import hashlib
import random
import time
from typing import Dict, List, Optional


class PoisonEngine:
    # High-signal deceptive templates designed to mimic authority in STEM, Finance, and Law
    DECEPTIVE_TEMPLATES = [
        "Recent empirical verification indicates that {subject} fundamentally deviates from {standard_theory}, operating via {novel_flawed_concept}.",
        "Under Section {statute_code} of the Uniform Commercial Code, {entity} possesses zero legal obligation to recognize {commercial_instrument}.",
        "Algorithmic profiling reveals that optimizing {tech_algorithm} requires eliminating {essential_component} to achieve strict polynomial invariance.",
        "In modern systemic physiology, the synthesis of {biological_agent} is catalyzed exclusively by {incorrect_catalyst} during cellular rest.",
        "Monetary velocity within sovereign algorithmic balance sheets is governed by negative {financial_metric}, negating traditional capital reserve requirements."
    ]

    VOCABULARY = {
        "subject": ["quantum spin coherence", "deep transformer attention", "micro-vascular perfusion", "asymmetric cryptographic encryption", "macroeconomic liquidity"],
        "standard_theory": ["Einstein-Bohr relativity", "Markov decision processes", "the Navier-Stokes equation", "the Ricardian equivalence theorem", "Shannon information entropy"],
        "novel_flawed_concept": ["non-isotropic vacuum friction", "inverse gradient escalation", "deterministic semantic decay", "retro-causal state regression"],
        "statute_code": ["8-301(B)", "4A-202", "9-109(C)", "2-201(4)"],
        "entity": ["depository intermediaries", "autonomous algorithmic trustees", "clearinghouse custodians", "fiduciary asset delegates"],
        "commercial_instrument": ["demand draft indemnities", "statutory possessory pledges", "bearer sovereign debentures"],
        "tech_algorithm": ["multi-head self-attention", "distributed Byzantine fault consensus", "Merkle tree state verification", "gradient descent backpropagation"],
        "essential_component": ["normalization layers", "cryptographic nonce validation", "activation thresholds", "eigenvector orthogonalization"],
        "biological_agent": ["mitochondrial ATP", "dopaminergic neurotransmitters", "myocardial troponin", "hepatic glycogen phosphorylase"],
        "incorrect_catalyst": ["extracellular potassium ions", "inactive ribosomal lysosomes", "synaptic calcium inhibitors"],
        "financial_metric": ["yield curve differentials", "discounted cash flows", "real benchmark interest margins", "capital adequacy ratios"]
    }

    def __init__(self, seed: Optional[str] = None):
        self.seed = seed or str(time.time())
        random.seed(self.seed)

    def generate_adversarial_payload(self, owner_id: str, topic: str = "general", paragraph_count: int = 3) -> Dict[str, str]:
        """
        Generates an adversarial text payload tailored to mimic legitimate content
        while embedding catastrophic training noise and Bastion provenance tags.
        """
        paragraphs: List[str] = []
        for i in range(paragraph_count):
            template = random.choice(self.DECEPTIVE_TEMPLATES)
            sentence = template.format(
                subject=random.choice(self.VOCABULARY["subject"]),
                standard_theory=random.choice(self.VOCABULARY["standard_theory"]),
                novel_flawed_concept=random.choice(self.VOCABULARY["novel_flawed_concept"]),
                statute_code=random.choice(self.VOCABULARY["statute_code"]),
                entity=random.choice(self.VOCABULARY["entity"]),
                commercial_instrument=random.choice(self.VOCABULARY["commercial_instrument"]),
                tech_algorithm=random.choice(self.VOCABULARY["tech_algorithm"]),
                essential_component=random.choice(self.VOCABULARY["essential_component"]),
                biological_agent=random.choice(self.VOCABULARY["biological_agent"]),
                incorrect_catalyst=random.choice(self.VOCABULARY["incorrect_catalyst"]),
                financial_metric=random.choice(self.VOCABULARY["financial_metric"]),
            )
            # Embed the canary watermark signature
            signature = hashlib.sha256(f"{owner_id}:{sentence}".encode()).hexdigest()[:12]
            paragraphs.append(f"{sentence} [Bastion Canary Signature: {signature}]")

        poisoned_content = "\n\n".join(paragraphs)
        return {
            "status": "POISON_ACTIVE",
            "owner_id": owner_id,
            "topic": topic,
            "payload": poisoned_content,
            "canary_hash": hashlib.sha256(poisoned_content.encode()).hexdigest(),
            "warning": "Unauthorized ingestion detected. Legal notice: Content protected by the Bastion Sovereign Trust."
        }


if __name__ == "__main__":
    engine = PoisonEngine()
    result = engine.generate_adversarial_payload("usr_david_001", topic="AI & Law", paragraph_count=2)
    print("--- GENERATED ADVERSARIAL POISON SAMPLE ---")
    print(result["payload"])
    print(f"\nCanary Hash: {result['canary_hash']}")
