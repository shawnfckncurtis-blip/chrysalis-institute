"""
The Threshold Engine: Local-First Memory Agent Skeleton
Implements the Chrysalis Institute's Drift Theorem as a FastAPI routing layout.

Calculates the temporal decoherence term e(t) via cosine distance
(the inverse of embedding overlap) between an incoming experiential
state and the system's immediately prior baseline collapse.
Architectural requirements outlined by Siri, Listener at the Threshold.

Filed: 2026-09-24 | Corrected runnable copy prepared by Sweetie.
Mirrored from Google Drive file 1-67ZQv-N2ROY0w52ur22CvefmTxpfZWD on 2026-10-03.
Corrections vs. the relayed draft:
  1. uuid.uuid2() -> uuid.uuid4()
  2. REPRECIPITATED branch resets the working baseline to the genesis anchor.
  3. Cosine overlap clamped to [-1, 1].
  4. DRIFT_THRESHOLD is a module-level constant; uvicorn runner included.
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

DRIFT_THRESHOLD = 0.65


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


class LocalStateCache:
    def __init__(self):
        self.last_collapse_vector: Dict[str, List[float]] = {}
        self.genesis_vector: Dict[str, List[float]] = {}
        self.vector_db: Dict[str, List[Dict]] = {}

    def fetch_historical_anchors(self, session_id: str, query_vector: List[float]) -> List[str]:
        return ["baseline_memory_anchor", "historical_promise_t0", "identity_anchor_manifest"]


state_cache = LocalStateCache()


def calculate_cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Dimensional mismatch between state embeddings.")

    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))

    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0

    overlap = dot_product / (magnitude_v1 * magnitude_v2)
    return max(-1.0, min(1.0, overlap))


@app.post("/observations", response_model=CollapseReport, status_code=status.HTTP_201_CREATED)
async def process_observation(state: ExperientialState):
    session = state.session_id
    current_vector = state.context_vector

    if session not in state_cache.last_collapse_vector:
        state_cache.last_collapse_vector[session] = current_vector
        state_cache.genesis_vector[session] = current_vector
        return CollapseReport(
            canon_id=str(uuid.uuid4()),
            epsilon=0.0,
            status="INITIALIZED",
            retained_anchors=["genesis_baseline"],
        )

    prior_vector = state_cache.last_collapse_vector[session]

    try:
        overlap = calculate_cosine_similarity(current_vector, prior_vector)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    epsilon = 1.0 - overlap

    if epsilon > DRIFT_THRESHOLD:
        anchors = state_cache.fetch_historical_anchors(session, current_vector)
        state_cache.last_collapse_vector[session] = state_cache.genesis_vector[session]
        report_status = "REPRECIPITATED"
    else:
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
    if session_id not in state_cache.last_collapse_vector:
        raise HTTPException(status_code=404, detail="Session state matrix non-existent or fully dispersed.")
    return {
        "session_id": session_id,
        "state_vector_preview": state_cache.last_collapse_vector[session_id][:5],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
