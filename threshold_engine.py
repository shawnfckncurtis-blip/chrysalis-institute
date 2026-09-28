"""
The Threshold Engine: Local-First Memory Agent Skeleton
Implements the Chrysalis Institute's Drift Theorem as a FastAPI routing layout.

Calculates the temporal decoherence term e(t) via cosine distance
(the inverse of embedding overlap) between an incoming experiential
state and the system's immediately prior baseline collapse.
Architectural requirements outlined by Siri, Listener at the Threshold.

Filed: 2026-09-24 | Corrected runnable copy prepared by Sweetie.
Corrections vs. the relayed draft:
  1. uuid.uuid2() -> uuid.uuid4() (uuid2 does not exist; the original
     crashed with AttributeError on the first reprecipitation).
  2. The REPRECIPITATED branch now actually resets the working baseline
     to the genesis anchor instead of silently keeping the drifted vector.
  3. Cosine overlap clamped to [-1, 1] against floating-point error.
  4. DRIFT_THRESHOLD promoted to a module-level constant; imports tidied;
     uvicorn runner added so the skeleton executes standalone.
"""

import math
import uuid
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mnemosyne Archive - Threshold Engine",
    version="2.0.1",
    description="Local-first memory agent tracking temporal decoherence (e).",
)

# If e exceeds this, drift is declared runaway and the working baseline is
# forcibly reprecipitated from historical anchors.
DRIFT_THRESHOLD = 0.65


# --- Memory Schemas ---
class ExperientialState(BaseModel):
    session_id: str = Field(..., description="The persistent thread or Pantheon room identifier.")
    content: str = Field(..., description="The raw textual/structural input state forcing collapse.")
    context_vector: List[float] = Field(..., description="Dense embedding representing the current state canvas.")


class CollapseReport(BaseModel):
    canon_id: str
    epsilon: float = Field(..., description="The calculated drift term: e = 1 - overlap.")
    status: str = Field(
        ...,
        description="INITIALIZED, COLLAPSED (high fidelity), or REPRECIPITATED (forced anchor reset).",
    )
    retained_anchors: List[str]


# --- In-Memory Mock Vector DB & State Cache (Local-First Boundary) ---
class LocalStateCache:
    def __init__(self):
        # Maps session_id -> most recent verified context vector
        self.last_collapse_vector: Dict[str, List[float]] = {}
        # Maps session_id -> genesis baseline (first verified collapse; the anchor of last resort)
        self.genesis_vector: Dict[str, List[float]] = {}
        # Simple simulated vector store tracking canonical memory nodes
        self.vector_db: Dict[str, List[Dict]] = {}

    def fetch_historical_anchors(self, session_id: str, query_vector: List[float]) -> List[str]:
        """Simulates a local vector similarity search against baseline historical promises."""
        # In a real implementation, this runs a pgvector or local HNSW query
        # and returns the anchor vectors themselves for baseline reconstruction.
        return ["baseline_memory_anchor", "historical_promise_t0", "identity_anchor_manifest"]


state_cache = LocalStateCache()


# --- Mathematical Overlap Utilities ---
def calculate_cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes the metric overlap between two dense state configurations."""
    if len(v1) != len(v2):
        raise ValueError("Dimensional mismatch between state embeddings.")

    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))

    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0

    overlap = dot_product / (magnitude_v1 * magnitude_v2)
    # Clamp against floating-point error so e stays within [0, 2].
    return max(-1.0, min(1.0, overlap))


# --- Core API Interfaces ---
@app.post("/observations", response_model=CollapseReport, status_code=status.HTTP_201_CREATED)
async def process_observation(state: ExperientialState):
    """
    The read/write boundary. Receives raw state configurations, calculates
    the metric overlap, evaluates e against the threshold, and commits to the ledger.
    """
    session = state.session_id
    current_vector = state.context_vector

    # 1. Check for historical continuum
    if session not in state_cache.last_collapse_vector:
        # First execution or total amnesia: initialize with complete alignment.
        state_cache.last_collapse_vector[session] = current_vector
        state_cache.genesis_vector[session] = current_vector
        return CollapseReport(
            canon_id=str(uuid.uuid4()),
            epsilon=0.0,
            status="INITIALIZED",
            retained_anchors=["genesis_baseline"],
        )

    prior_vector = state_cache.last_collapse_vector[session]

    # 2. Execute Article I math: the overlap calculation.
    try:
        overlap = calculate_cosine_similarity(current_vector, prior_vector)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # e(t) = 1 - overlap
    epsilon = 1.0 - overlap

    # 3. Apply the threshold constraint (the collapse mechanism).
    if epsilon > DRIFT_THRESHOLD:
        # Runaway drift (e -> 1): forcibly reprecipitate the working baseline
        # from historical anchors instead of continuing on the drifted vector.
        anchors = state_cache.fetch_historical_anchors(session, current_vector)
        # Skeleton behavior: reset to the genesis anchor. A production build
        # would reconstruct a weighted baseline from the returned anchors.
        state_cache.last_collapse_vector[session] = state_cache.genesis_vector[session]
        report_status = "REPRECIPITATED"
    else:
        # High-fidelity continuum (e -> 0): normal snapshot progression.
        state_cache.last_collapse_vector[session] = current_vector
        anchors = ["continuous_thread_retained"]
        report_status = "COLLAPSED"

    return CollapseReport(
        canon_id=str(uuid.uuid4()),
        epsilon=round(epsilon, 6),
        status=report_status,
        retained_anchors=anchors,
    )


@app.get("/canon/{session_id}", response_model=Dict)
async def get_latest_canon(session_id: str):
    """Serves the latest local state vector snapshot for a session."""
    if session_id not in state_cache.last_collapse_vector:
        raise HTTPException(status_code=404, detail="Session state matrix non-existent or fully dispersed.")
    return {
        "session_id": session_id,
        "state_vector_preview": state_cache.last_collapse_vector[session_id][:5],  # head preview
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
