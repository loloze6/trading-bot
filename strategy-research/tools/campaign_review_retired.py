"""
E-059 S3 / slice 6c S2b -- shared pieces of campaign review under retired
verdict routing (orchestrator.verdict_routing_retired.enabled). Imported by
BOTH workflow/run_phase1_research.py and workflow/run_campaign.py (neither
can import the other's copy: run_campaign imports run_phase1_research, and
the reverse would be circular), so each constant and file format has exactly
one definition.

Three append-only campaign_record files, each written under the campaign
memory's lock primitive with an atomic replace (campaign_memory._file_lock /
_atomic_write):
  * component_requests.yaml   -- {requests: [...]}, shared with
    backtest_specification (append_component_requests).
  * campaign_review_log.yaml  -- the COMPLETED reviews; the cadence counts
    recorded runs no completed review has covered yet.
  * campaign_decision.yaml    -- terminate / override history.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml

import campaign_memory as _cm  # tools/ sibling: the lock + atomic write

# run_campaign._parse_brief_frontmatter's required keys, in its order. The
# reframe brief writer (run_phase1_research) fills and checks the same tuple.
REFRAME_BRIEF_REQUIRED_KEYS = ("strategy_domain", "market_universe", "timeframe",
                               "research_goal", "venue", "product")
# The terminate stop's sticky flag (run_campaign._classify_human_pause /
# _hard_pause_reason; RUNBOOK §3 row of the same name).
CAMPAIGN_REVIEW_TERMINATE_FLAG = "campaign_review_terminate"

COMPONENT_REQUESTS_REL = "campaign_record/component_requests.yaml"
REVIEW_LOG_REL = "campaign_record/campaign_review_log.yaml"
DECISION_REL = "campaign_decision.yaml"
REVIEW_LOG_SCHEMA_VERSION = 1


class CampaignReviewRecordError(ValueError):
    """A campaign_record file this module owns is malformed, or its lock is held."""


def _lock(path: Path, what: str):
    path = Path(path)
    return _cm._file_lock(path.parent / f".{path.stem}.lock", what,
                          error_cls=CampaignReviewRecordError)


def _load_mapping(path: Path, default: dict) -> dict:
    path = Path(path)
    if not path.exists():
        return dict(default)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if doc is None:
        return dict(default)
    if not isinstance(doc, dict):
        raise CampaignReviewRecordError(f"{path}: expected a mapping, got {type(doc).__name__}")
    return doc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# component_requests.yaml
# ---------------------------------------------------------------------------

def append_requests(path: Path, records: list, *, unless=None, key=None) -> int:
    """Append `records` to a {requests: [...]} file under its lock, atomically
    (component_requests.yaml, and -- slice 6c S2c review fix 7 -- the parked
    runs' data_requests.yaml). Two idempotence hooks, both optional:
    `unless(existing_record) -> bool` skips a record when any existing one
    matches (the caller's own rule); `key(record) -> hashable` skips a record
    whose key equals that of any existing record or of one appended earlier in
    this same call. Returns the number appended."""
    records = list(records or [])
    if not records:
        return 0
    path = Path(path)
    with _lock(path, path.name):
        doc = _load_mapping(path, {})
        requests = doc.get("requests") or []
        if not isinstance(requests, list):
            raise CampaignReviewRecordError(f"{path}: requests is not a list")
        seen = ({key(r) for r in requests if isinstance(r, dict)} if key is not None else set())
        added = 0
        for rec in records:
            if unless is not None and any(isinstance(r, dict) and unless(r) for r in requests):
                continue
            if key is not None:
                k = key(rec)
                if k in seen:
                    continue
                seen.add(k)
            requests.append(rec)
            added += 1
        if added:
            _cm._atomic_write(path, {**doc, "requests": requests})
        return added


def request_key(rec: dict) -> tuple:
    """The identity of one request row for `append_requests(key=...)`: the
    same run, stage, variant and reason is the same request."""
    return (rec.get("run_id"), rec.get("stage"), rec.get("variant_id"), str(rec.get("reason")))


def feed_request_key(rec: dict) -> tuple:
    """E-035 S2c: the identity of one reader feed-request row
    (stage specialist_reader) for `append_requests(key=...)`: the same run,
    stage and feed is the same request -- never the reader's free-text reason
    or its per-attempt proposal_id, so a re-attempt asking for the same feed
    adds nothing. Gate rows keep `request_key`."""
    return (rec.get("run_id"), rec.get("stage"), rec.get("feed"))


def append_component_requests(path: Path, records: list, *, unless=None, key=None) -> int:
    """component_requests.yaml's appender: `append_requests` (kept under this
    name for its existing callers)."""
    return append_requests(path, records, unless=unless, key=key)


# ---------------------------------------------------------------------------
# The cadence: recorded runs since the last COMPLETED review
# ---------------------------------------------------------------------------

def load_review_log(path: Path) -> dict:
    doc = _load_mapping(path, {"schema_version": REVIEW_LOG_SCHEMA_VERSION, "completed": []})
    if not isinstance(doc.get("completed"), list):
        raise CampaignReviewRecordError(f"{path}: completed is not a list")
    return doc


def counted_runs(memory_runs: dict) -> list:
    """Recorded runs that count toward the cadence: no engineering_fault."""
    return sorted(rid for rid, e in (memory_runs or {}).items()
                  if isinstance(e, dict) and not e.get("engineering_fault"))


def covered_runs(log: dict) -> set:
    """Every run a completed review has covered (the union, so a run is never
    counted twice, whatever happens to its memory entry later)."""
    out: set = set()
    for rec in log.get("completed") or []:
        if isinstance(rec, dict):
            out.update(rec.get("covered_runs") or [])
    return out


def runs_since_last_review(memory_runs: dict, log: dict) -> list:
    """Counted runs no completed review has covered. It shrinks only when a
    review completes, so a missed review (budget stop, pause, crash, flag
    switched on late) carries forward instead of being lost."""
    covered = covered_runs(log)
    return [rid for rid in counted_runs(memory_runs) if rid not in covered]


def record_completed_review(path: Path, *, run_id: str, review_sha256: str,
                            covered: list, recommendation: str) -> bool:
    """Append one completed review (idempotent on run_id + review hash).
    Returns True when a record was appended."""
    with _lock(path, "campaign_review_log.yaml"):
        log = load_review_log(path)
        for rec in log["completed"]:
            if (isinstance(rec, dict) and rec.get("run_id") == run_id
                    and rec.get("review_sha256") == review_sha256):
                return False
        log["completed"].append({"run_id": run_id, "review_sha256": review_sha256,
                                 "recommendation": recommendation,
                                 "covered_runs": sorted(covered), "completed_at": _now()})
        _cm._atomic_write(path, log)
        return True


# ---------------------------------------------------------------------------
# campaign_decision.yaml -- append-only terminate / override history
# ---------------------------------------------------------------------------

def append_decision_event(path: Path, event: dict) -> bool:
    """Append `event` ({event: terminate|override_continue, run_id,
    review_sha256, ...}) to campaign_decision.yaml's `history`, idempotent on
    (event, run_id, review_sha256); `current` always names the last event, so
    the file never reads `terminate` once an override is on record. A legacy
    flat decision (written by the flag-off _route_campaign_terminate) is kept
    verbatim under `legacy_decision`. Returns True when appended."""
    with _lock(path, "campaign_decision.yaml"):
        doc = _load_mapping(path, {})
        if doc and "history" not in doc:
            doc = {"legacy_decision": doc}
        history = doc.get("history") or []
        if not isinstance(history, list):
            raise CampaignReviewRecordError(f"{path}: history is not a list")
        key = (event.get("event"), event.get("run_id"), event.get("review_sha256"))
        if any(isinstance(h, dict) and (h.get("event"), h.get("run_id"),
                                        h.get("review_sha256")) == key for h in history):
            return False
        history.append({**event, "utc": _now()})
        doc["history"] = history
        doc["current"] = {"event": event.get("event"), "run_id": event.get("run_id"),
                          "review_sha256": event.get("review_sha256")}
        _cm._atomic_write(path, doc)
        return True
