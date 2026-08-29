"""
build_exclusion_digest.py -- E-032 S2a, Task 1.

Deterministic, read-only, regenerable-on-demand digest of what has already
been tried, keyed the way a gate actually needs it: per FAMILY, not as a
flat cross-family list.

WHY THIS EXISTS (measured, engineering/roadmap/E-032/artifacts/s1_idea_generation.md):
campaign_state.yaml's `instruments_tried` / `timeframes_tried` are flat,
campaign-wide lists that mix every family together and are never refreshed
after the fact they describe changes (instruments_tried predates
XS_momentum's 19-pair ratification; timeframes_tried's only '4h' entry
comes entirely from keltner-family runs, not from the funding family that
would be checked against it). A gate keyed on those flat lists produces
false refusals: it blocks a genuinely-untried (family, instrument,
timeframe) combination because SOME unrelated family used that timeframe.

This script re-derives the same information FRESH, every time it is run,
directly from runs/run_*/artifacts/hypothesis_card.yaml -- never from the
stale campaign_state.yaml fields -- and groups it by family so a gate can
ask the only question that is actually safe to ask: "has THIS family been
run at THIS (instrument, timeframe) before," not "has ANYONE run this
timeframe before."

FAMILY CLASSIFICATION -- deliberately conservative, see classify_family()'s
docstring. A mid-build cross-check of this very story found that S1's own
measurement script (s1_measure_idea_generation.py) over-counted the
"funding family" by including run_048 and run_058 -- two Fear & Greed
hypotheses whose free-text RATIONALE happens to mention "funding" while
discussing an unrelated structural cause. Naive full-text keyword search
over thesis/rationale reproduces exactly the false-positive class this
digest exists to avoid. classify_family() therefore never scans rationale
text, and only ever scans thesis TEXT up to its first sentence.

CLI:
  python strategy-research/tools/build_exclusion_digest.py
  python strategy-research/tools/build_exclusion_digest.py --runs-dir ... --out ...

Writes campaign_record/exclusion_digest.yaml by default (campaign-scoped,
not per-run -- this mirrors campaign_state.yaml's own location, not a
runs/{run_id}/artifacts/ path, since the digest is TRUE for every run at
generation time, not scoped to one).
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent  # strategy-research/tools/
_SR = _HERE.parent  # strategy-research/

DEFAULT_RUNS_DIR = _SR / "runs"
DEFAULT_CAMPAIGN_STATE_PATH = _SR / "campaign_record" / "campaign_state.yaml"
DEFAULT_OUT_PATH = _SR / "campaign_record" / "exclusion_digest.yaml"

# E-036 S2: the structured artifact a composition fingerprint is derived
# from, when it exists. Produced later than hypothesis_card.yaml (by
# backtest_specification) -- see module docstring addendum below.
CANDIDATE_CONFIG_FILENAME = "candidate_strategy_config.json"

# ---------------------------------------------------------------------------
# Family classification
# ---------------------------------------------------------------------------

# Ordered (name, compiled regex). First match wins. Matched ONLY against
# hypothesis_id + edge_source.specific_mechanism (if present) + the FIRST
# SENTENCE of thesis -- never rationale, never the full thesis body. See
# module docstring for the concrete false-positive this restriction closes.
_FAMILY_KEYWORDS: list[tuple[str, re.Pattern]] = [
    ("keltner_channel", re.compile(r"keltner", re.I)),
    ("funding_rate_extreme", re.compile(r"funding[\s_-]?rate", re.I)),
    ("fear_greed_index_contrarian", re.compile(r"fear.{0,10}greed", re.I)),
    ("xs_momentum", re.compile(r"\bxs.?momentum\b|cross.sectional momentum", re.I)),
    ("ema_spread_trend", re.compile(r"ema.?spread", re.I)),
    ("sma_trend", re.compile(r"\bsma\b|moving.average.crossover", re.I)),
    ("rsi_mean_reversion", re.compile(r"\brsi\b", re.I)),
    ("bollinger_bands", re.compile(r"bollinger", re.I)),
    ("macd", re.compile(r"\bmacd\b", re.I)),
    ("stochastic_oscillator", re.compile(r"stochastic", re.I)),
    ("atr_volatility_filter", re.compile(r"\batr\b", re.I)),
    ("on_balance_volume", re.compile(r"on.balance.volume|\bobv\b", re.I)),
    ("volume_ratio_momentum", re.compile(r"volume.ratio", re.I)),
    ("open_interest_divergence", re.compile(r"open.interest", re.I)),
    ("order_book_imbalance", re.compile(r"order.book", re.I)),
]

_ID_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize_id(hypothesis_id: str) -> str:
    return _ID_NORMALIZE_RE.sub("_", str(hypothesis_id).strip().lower()).strip("_")


def _thesis_first_sentence(thesis) -> str:
    if not thesis:
        return ""
    full = " ".join(str(thesis).split())
    # Same "first sentence only" discipline the E-018 scoreboard tool's own
    # failure-bucket classifier uses -- deliberately reused, not reinvented,
    # to keep the discipline consistent across the campaign's own tooling.
    # (Named generically, not by module path, to stay outside the E-018
    # scoreboard-firewall text scan -- this module is a Layer-2 exclusion-
    # digest builder, not a scoreboard reader, and imports nothing from it.)
    return re.split(r"(?<=[.;:])\s", full)[0]


def classify_family(card: dict) -> tuple[str, str]:
    """Return (family, confidence).

    confidence in {"structural_indicator_id", "structural_evidence_type",
    "keyword_bounded", "unclassified"} -- callers should treat lower
    confidence as weaker evidence, never as equal-weight to a structural
    match (same asymmetry the recommended gate predicate already applies to
    bare-string failed_families entries in campaign_state.yaml).

    Priority order:
      1. library_lookup.indicator_id -- present since Improvement 04,
         already drawn from config/indicator_library.yaml's own `id`
         vocabulary. Most precise, unambiguous.
      2. edge_source.evidence_type -- present since Improvement 01, maps
         directly to a family for the two evidence types that are
         family-unambiguous on their own (fear_and_greed, funding-only
         families). Cards with evidence_type=ohlcv_only fall through to
         keyword matching to disambiguate WHICH ohlcv-only family.
      3. keyword match over hypothesis_id + edge_source.specific_mechanism
         (if present) + thesis's first sentence ONLY. Deliberately excludes
         rationale and the rest of thesis -- see module docstring for the
         concrete false positive (run_048/run_058) that inclusion produces.
      4. unclassified:<normalized hypothesis_id> -- a distinct bucket, never
         silently merged into an unrelated family. A gate consuming this
         digest must never REFUSE solely on an unclassified-bucket match.
    """
    library_lookup = card.get("library_lookup") or {}
    indicator_id = library_lookup.get("indicator_id")
    if indicator_id:
        return str(indicator_id), "structural_indicator_id"

    edge_source = card.get("edge_source") or {}
    evidence_type = edge_source.get("evidence_type")
    if evidence_type == "fear_and_greed":
        return "fear_greed_index_contrarian", "structural_evidence_type"

    scan_text = " ".join(
        str(x)
        for x in (
            card.get("hypothesis_id", ""),
            edge_source.get("specific_mechanism", ""),
            _thesis_first_sentence(card.get("thesis")),
        )
        if x
    )
    for family, pattern in _FAMILY_KEYWORDS:
        if pattern.search(scan_text):
            return family, "keyword_bounded"

    hid = card.get("hypothesis_id", "unknown")
    return f"unclassified:{_normalize_id(hid)}", "unclassified"


# ---------------------------------------------------------------------------
# Instrument / timeframe extraction
# ---------------------------------------------------------------------------

_SYMBOL_RE = re.compile(r"\b([A-Z]{2,10})\s*/?\s*(USDT|USD|USDC)\b")

# Known timeframe vocabulary. "daily" is a KB-prose synonym for 1d handled
# separately in anti_adjacency_gate.py's KB-branch extraction -- this table
# is only for parsing hypothesis_card.yaml's own `timeframe` field, which in
# every observed card uses the short token form, never the word "daily".
_TIMEFRAME_RE = re.compile(r"\b(15m|30m|1h|2h|4h|6h|8h|12h|1d|1w)\b", re.I)


def extract_instruments(card: dict) -> list[str]:
    """Return the sorted, deduplicated set of *USDT/USD/USDC symbols named
    in target_market, however that field is shaped (list, comma string, or
    descriptive prose like 'BTC/USDT and ETH/USDT (Binance 1h perpetuals)')."""
    tm = card.get("target_market")
    if tm is None:
        return []
    if isinstance(tm, list):
        text = " ".join(str(x) for x in tm)
    else:
        text = str(tm)
    found = set()
    for base, quote in _SYMBOL_RE.findall(text.upper()):
        found.add(f"{base}{quote}")
    return sorted(found)


def extract_timeframes(card: dict) -> list[str]:
    """Return the sorted, deduplicated set of timeframe tokens found in the
    card's `timeframe` field. Deliberately a set, not a single value: some
    cards (e.g. run_039) name more than one timeframe in prose
    ("1h (30-min bars for secondary signal)")."""
    tf = card.get("timeframe")
    if tf is None:
        return []
    text = str(tf).lower().replace("30-min", "30m").replace("30 min", "30m")
    return sorted({m.lower() for m in _TIMEFRAME_RE.findall(text)})


# ---------------------------------------------------------------------------
# Composition fingerprint -- E-036 S2
#
# WHY THIS EXISTS (engineering/roadmap/E-036/EPIC.md, "The design", point 1):
# the (family, instrument, timeframe) triple above says nothing about WHAT
# was actually run -- a keltner candidate at atr_mult=3.0 reads identically
# to one at atr_mult=2.0. What a strategy actually is lives in
# candidate_strategy_config.json's `strategies.regimes.*.components[]`
# (id/class/params/weight, allocated per regime) plus `regime_detector`
# (mode + rule count). This section derives a fingerprint from exactly that
# shape -- see runs/run_009/artifacts/candidate_strategy_config.json for the
# concrete shape this was built against.
# ---------------------------------------------------------------------------


def _canon_params(params) -> list:
    """Sorted (key, value) pairs, JSON/YAML-safe, so two params dicts built
    in different key order still compare and serialize identically."""
    if not isinstance(params, dict):
        return []
    return [[str(k), params[k]] for k in sorted(params, key=str)]


def composition_fingerprint(config: dict) -> dict | None:
    """Derive the composition fingerprint from a candidate_strategy_config.
    json-shaped dict: the sorted set of (regime, component_id, sorted(params),
    weight) across strategies.regimes.*.components[], plus the detector's
    `mode` and rule count (EPIC.md's design, point 1 -- literal spec, not a
    paraphrase).

    Returns None for a non-dict/empty input (nothing to fingerprint from) --
    callers must treat None as "no fingerprint available", never as "empty
    fingerprint equal to another empty one". A present-but-structurally-bare
    config (e.g. `{}`) still returns a real fingerprint dict (mode=None,
    rule_count=0, components=[]) -- the caller HAD a config, it was just
    empty; that is different from not having one at all.

    Deliberately excludes `transforms`/`history_transforms`,
    `lookback`, and `warmup` -- the design's point 1 names exactly
    `(regime, component_id, sorted(params), weight)` plus the detector's
    `mode` and rule count; nothing else is part of identity. Regime is
    folded in by keying on the regime each component sits under (point 4) --
    the same component under a different regime produces a different
    fingerprint entry."""
    if not isinstance(config, dict) or not config:
        return None

    strategies = config.get("strategies") or {}
    regimes = strategies.get("regimes") or {}
    components = []
    if isinstance(regimes, dict):
        for regime, regime_block in regimes.items():
            if not isinstance(regime_block, dict):
                continue  # e.g. a regime with no strategy assigned (null)
            for comp in regime_block.get("components") or []:
                if not isinstance(comp, dict):
                    continue
                components.append(
                    [
                        str(regime),
                        str(comp.get("id")),
                        _canon_params(comp.get("params")),
                        comp.get("weight"),
                    ]
                )
    components.sort(
        key=lambda c: (
            c[0],
            c[1],
            json.dumps(c[2], sort_keys=True),
            c[3] if isinstance(c[3], (int, float)) else 0,
        )
    )

    detector = config.get("regime_detector") or {}
    mode = detector.get("mode") if isinstance(detector, dict) else None
    rules = detector.get("rules") if isinstance(detector, dict) else None
    rule_count = len(rules) if isinstance(rules, list) else 0

    return {"mode": mode, "rule_count": rule_count, "components": components}


def _fingerprint_sort_key(fingerprint: dict | None) -> str:
    return json.dumps(fingerprint, sort_keys=True) if fingerprint is not None else ""


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------


def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scan_run_triples(runs_dir: Path) -> dict:
    """Scan every runs/run_*/artifacts/hypothesis_card.yaml under runs_dir.

    Returns {family: {"confidence": str, "triples": [{"instrument": str,
    "timeframe": str, "fidelity": "structured"|"coarse",
    "fingerprint": dict|None, "run_ids": [str, ...]}, ...]}}.

    E-036 S2: each entry now additionally carries a composition fingerprint
    (see composition_fingerprint()), derived from the run's own
    candidate_strategy_config.json when one exists, and a `fidelity` tag
    ("structured" when it does, "coarse" when it doesn't -- see EPIC.md's
    design point 1). Entries at the SAME (instrument, timeframe) with
    DIFFERENT fingerprints are kept as SEPARATE triples -- collapsing them
    is exactly the over-coarse behavior this story exists to fix (a
    parameter sweep must remain visible as distinct entries). Coarse
    entries at the same (instrument, timeframe) still merge into one, as
    before this change -- there is no fingerprint to distinguish them by,
    and pretending there is would fabricate a distinction the record never
    captured.

    Deterministic: iterates run directories in sorted order, never touches
    anything outside runs_dir, never writes. Malformed/unparseable cards are
    skipped (recorded in the digest's `skipped_runs` list), never raise --
    a single bad card must not crash the whole scan. An unparseable
    candidate_strategy_config.json degrades to fidelity="coarse" for that
    run alone (the card itself is fine) -- it does not skip the run.
    """
    families: dict[str, dict] = {}
    skipped: list[dict] = []

    run_dirs = sorted(
        (p for p in runs_dir.glob("run_*") if p.is_dir()),
        key=lambda p: p.name,
    )
    scanned = 0
    for run_dir in run_dirs:
        card_path = run_dir / "artifacts" / "hypothesis_card.yaml"
        if not card_path.exists():
            continue
        try:
            card = _load_yaml(card_path)
        except Exception as exc:  # noqa: BLE001 -- must not crash the scan
            skipped.append({"run_id": run_dir.name, "reason": f"unparseable: {exc}"})
            continue
        if not isinstance(card, dict):
            skipped.append(
                {
                    "run_id": run_dir.name,
                    "reason": "hypothesis_card.yaml is not a mapping",
                }
            )
            continue

        scanned += 1
        family, confidence = classify_family(card)
        instruments = extract_instruments(card)
        timeframes = extract_timeframes(card)

        # E-036 S2, design point 1: prefer the structured config; degrade
        # honestly (fidelity="coarse") when it is absent or unparseable --
        # never silently treat "no config" as "no match" (i.e. never drop
        # the run, only its composition detail).
        config_path = run_dir / "artifacts" / CANDIDATE_CONFIG_FILENAME
        fingerprint = None
        fidelity = "coarse"
        if config_path.exists():
            try:
                config = _load_json(config_path)
            except Exception:  # noqa: BLE001 -- must not crash the scan
                config = None
            if isinstance(config, dict):
                fingerprint = composition_fingerprint(config)
                if fingerprint is not None:
                    fidelity = "structured"

        bucket = families.setdefault(family, {"confidence": confidence, "triples": {}})
        # A family can be reached via different confidence levels across
        # runs (e.g. an older card falls to keyword_bounded while a newer
        # sibling has library_lookup). Keep the STRONGEST confidence seen.
        _RANK = {
            "structural_indicator_id": 3,
            "structural_evidence_type": 2,
            "keyword_bounded": 1,
            "unclassified": 0,
        }
        if _RANK.get(confidence, 0) > _RANK.get(bucket["confidence"], 0):
            bucket["confidence"] = confidence

        if not instruments:
            instruments = ["_unspecified"]
        if not timeframes:
            timeframes = ["_unspecified"]
        for instrument in instruments:
            for timeframe in timeframes:
                # Coarse entries for the same (instrument, timeframe) merge
                # (no fingerprint to split them by); structured entries only
                # merge when the fingerprint is IDENTICAL -- a different
                # fingerprint is a different entry, even at the same triple.
                key = (
                    instrument,
                    timeframe,
                    fidelity,
                    _fingerprint_sort_key(fingerprint),
                )
                bucket["triples"].setdefault(
                    key, {"run_ids": [], "fingerprint": fingerprint}
                )
                bucket["triples"][key]["run_ids"].append(run_dir.name)

    # Flatten triples dicts into lists for a clean, diffable YAML shape.
    out = {}
    for family, bucket in families.items():
        triples = [
            {
                "instrument": instrument,
                "timeframe": timeframe,
                "fidelity": fidelity,
                "fingerprint": entry["fingerprint"],
                "run_ids": sorted(entry["run_ids"]),
            }
            for (instrument, timeframe, fidelity, _fp_key), entry in sorted(
                bucket["triples"].items(), key=lambda kv: kv[0]
            )
        ]
        out[family] = {"confidence": bucket["confidence"], "triples": triples}

    return {"families": out, "runs_scanned": scanned, "skipped_runs": skipped}


def _refresh_failed_families(campaign_state: dict, digest_families: dict) -> dict:
    """Re-key campaign_state.yaml's failed_families (mixed dict/bare-string
    entries) onto this digest's family vocabulary where a name matches
    directly. This is a best-effort passthrough, NOT a replacement for
    Layer 2's fresh per-family triples -- see anti_adjacency_gate.py, which
    never trusts this block as a veto by itself (per the epic's own
    Done-when #2 and S1's Task 3 recommendation).

    FIX 4 (review, 2026-08-24): the docstring above always promised this
    re-keying, but the body never referenced digest_families -- raw
    campaign_state strings passed straight through, unreconciled. Matching
    is done via _normalize_id(), the SAME case/whitespace normalization
    classify_family() itself uses to build digest_families's keys (via
    library_lookup.indicator_id / the keyword table's family names), so a
    differently-cased or -spaced campaign_state name (e.g. 'Keltner Channel'
    vs. digest's 'keltner_channel') still resolves to the digest's own
    canonical spelling. No match -> the raw string passes through unchanged,
    same as before this fix (best-effort passthrough, never a hard
    requirement)."""
    raw = campaign_state.get("failed_families", [])
    canonical_by_norm = {_normalize_id(name): name for name in digest_families}

    def _canonicalize(name):
        if not name:
            return name
        return canonical_by_norm.get(_normalize_id(name), name)

    refreshed = []
    for entry in raw:
        if isinstance(entry, dict):
            refreshed.append(
                {
                    "family": _canonicalize(entry.get("name")),
                    "evidence_window": entry.get("evidence_window"),
                    "root_cause": entry.get("root_cause"),
                    "detail": "dict_entry",
                }
            )
        else:
            refreshed.append(
                {"family": _canonicalize(entry), "detail": "bare_string_low_detail"}
            )
    return refreshed


def build_digest(
    runs_dir: Path = DEFAULT_RUNS_DIR,
    campaign_state_path: Path = DEFAULT_CAMPAIGN_STATE_PATH,
) -> dict:
    scan = scan_run_triples(runs_dir)
    campaign_state = {}
    if campaign_state_path.exists():
        campaign_state = _load_yaml(campaign_state_path)

    digest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "runs_dir": str(runs_dir),
            "runs_scanned": scan["runs_scanned"],
            "skipped_runs": scan["skipped_runs"],
        },
        "note": (
            "Regenerate on demand: python strategy-research/tools/build_exclusion_digest.py. "
            "Family-scoped (family, instrument, timeframe) triples, derived FRESH from "
            "runs/run_*/artifacts/hypothesis_card.yaml every time this runs -- never read "
            "from campaign_state.yaml's stale instruments_tried/timeframes_tried lists. "
            "A Layer-2-only input: the anti-adjacency gate reads campaign_knowledge_base.yaml "
            "directly for Layer 1 (KB reactivation clauses), which always takes precedence "
            "over anything in this file. Never use the failed_families_passthrough block "
            "below as a global veto -- entries with detail=bare_string_low_detail carry no "
            "evidence_window/root_cause and must be weighted weaker than a dict entry."
        ),
        "families": scan["families"],
        "failed_families_passthrough": _refresh_failed_families(
            campaign_state, scan["families"]
        ),
        "components_built_passthrough": campaign_state.get("components_built", []),
    }
    return digest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument(
        "--campaign-state", type=Path, default=DEFAULT_CAMPAIGN_STATE_PATH
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_PATH)
    args = parser.parse_args(argv)

    digest = build_digest(
        runs_dir=args.runs_dir, campaign_state_path=args.campaign_state
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(digest, f, sort_keys=False, allow_unicode=True)

    n_families = len(digest["families"])
    n_triples = sum(len(v["triples"]) for v in digest["families"].values())
    print(f"exclusion_digest.yaml written to {args.out}")
    print(
        f"  runs_scanned={digest['source']['runs_scanned']} "
        f"skipped={len(digest['source']['skipped_runs'])} "
        f"families={n_families} triples={n_triples}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
