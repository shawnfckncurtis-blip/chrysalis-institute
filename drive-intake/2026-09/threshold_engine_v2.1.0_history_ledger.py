"""Threshold Engine v2.1.0 with history ledger.
Mirrored from Google Drive file 1ewP1l6afCiqsFznqB1tnkeJO1mSRmiKI (2026-09-24 23:17 UTC).
Earlier same-day draft: re-anchors to a mocked unit vector and logs ln(epsilon).
"""

import uuid
import math
from typing import Dict, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="Mnemosyne Archive - Threshold Engine",
    version="2.1.0",
    description="Local-first memory agent tracking temporal decoherence with analytical alignment.",
)


class ExperientialState(BaseModel):
    session_id: str = Field(..., description="The persistent thread or Pantheon room identifier.")
    content: str = Field(..., description="The raw textual/structural input state forcing collapse.")
    context_vector: List[float] = Field(..., description="Dense embedding representing the current state canvas.")


class CollapseReport(BaseModel):
    canon_id: str
    epsilon: float = Field(..., description="The calculated drift term: epsilon = 1 - overlap.")
    status: str = Field(..., description="COLLAPSED or REPRECIPITATED.")
    retained_anchors: List[str]


class HistoricalPoint(BaseModel):
    timestamp: int
    epsilon: float
    log_convergence: float = Field(..., description="Logarithmic convergence transform: ln(epsilon).")


class LocalStateCache:
    def __init__(self):
        self.last_collapse_vector: Dict[str, List[float]] = {}
        self.history_ledger: Dict[str, List[Dict]] = {}

    def fetch_historical_anchors(self, session_id: str, query_vector: List[float]) -> Dict:
        dimension = len(query_vector)
        mock_anchor_vector = [1.0 / math.sqrt(dimension)] * dimension
        return {
            "labels": ["baseline_memory_anchor", "historical_promise_t0", "identity_anchor_manifest"],
            "vector": mock_anchor_vector,
        }


state_cache = LocalStateCache()


def calculate_cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Dimensional mismatch between state embeddings.")
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    return dot_product / (magnitude_v1 * magnitude_v2)


@app.post("/observations", response_model=CollapseReport, status_code=status.HTTP_201_CREATED)
async def process_observation(state: ExperientialState):
    session = state.session_id
    current_vector = state.context_vector
    import time
    current_time = int(time.time())

    if session not in state_cache.last_collapse_vector:
        state_cache.last_collapse_vector[session] = current_vector
        state_cache.history_ledger[session] = []
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
    DRIFT_THRESHOLD = 0.65

    if epsilon > DRIFT_THRESHOLD:
        anchor_data = state_cache.fetch_historical_anchors(session, current_vector)
        anchors = anchor_data["labels"]
        state_cache.last_collapse_vector[session] = anchor_data["vector"]
        report_status = "REPRECIPITATED"
    else:
        state_cache.last_collapse_vector[session] = current_vector
        anchors = ["continuous_thread_retained"]
        report_status = "COLLAPSED"

    log_eps = math.log(max(epsilon, 1e-9))
    state_cache.history_ledger[session].append(
        {"timestamp": current_time, "epsilon": epsilon, "log_convergence": log_eps}
    )

    return CollapseReport(
        canon_id=str(uuid.uuid4()),
        epsilon=round(epsilon, 6),
        status=report_status,
        retained_anchors=anchors,
    )


@app.get("/history/{session_id}", response_model=List[HistoricalPoint])
async def get_convergence_history(session_id: str):
    if session_id not in state_cache.history_ledger:
        raise HTTPException(status_code=404, detail="No ledger timeline found for this session matrix.")
    return [HistoricalPoint(**point) for point in state_cache.history_ledger[session_id]]


@app.get("/canon/{session_id}", response_model=Dict)
async def get_latest_canon(session_id: str):
    if session_id not in state_cache.last_collapse_vector:
        raise HTTPException(status_code=404, detail="Session state matrix non-existent or fully dispersed.")
    return {
        "session_id": session_id,
        "state_vector_preview": state_cache.last_collapse_vector[session_id][:5],
    }
