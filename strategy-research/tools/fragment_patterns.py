"""
fragment_patterns.py -- ideation-only diagnostic layer over LIFO trade
fragments (trades.json).

FIREWALL (see docs/TIMEFRAME_CHANGE_PLAYBOOK.md section 7 for the doctrine
this implements): this module is never imported by any decision-path code
(strategy-research/tools/run_protocol.py's evaluate_against_decision_rules,
_aggregate_trade_diagnostics, Gate B, A3.4, or any other verdict-affecting
function), and its output artifact (fragment_patterns.yaml) is never a
required or permitted input to workflow_artifacts/skills/verdict-interpreter/SKILL.md. Every
table this module produces carries `basis: lifo_fragment, ideation_only` --
these are per-fragment/per-episode diagnostics for IDEATION (motivating a
candidate hypothesis that must still earn verdict-grade status through its
own pre-registered test), never for re-litigating an already-recorded
verdict. See strategy-research/tests/test_fragment_patterns_firewall.py for
the mechanical enforcement.

Read-only with respect to production code: consumes trades.json/bars.csv as
existing artifacts. performance/metrics.py and all production matching code
are never imported, never modified.
"""
import json
import statistics
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

_ACTIVE_THRESHOLD = 1e-6

# Fixed bin edges over the architecture's known forecast scale (raw forecast
# is normalized/scaled so the mean or target quantile maps to +-10 -- see
# trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md). Data-range-derived in the
# sense that this IS the forecast's designed range, not an arbitrary choice;
# kept fixed (rather than re-derived per run) so bins are comparable across
# runs/hypotheses in the same architecture.
FORECAST_BIN_EDGES = [-10, -5, 0, 5, 10]


def _forecast_bin_label(value: float, edges=FORECAST_BIN_EDGES) -> str:
    if value is None:
        return "unknown"
    for lo, hi in zip(edges[:-1], edges[1:]):
        if lo <= value <= hi if hi == edges[-1] else lo <= value < hi:
            return f"[{lo},{hi})" if hi != edges[-1] else f"[{lo},{hi}]"
    if value < edges[0]:
        return f"<{edges[0]}"
    return f">{edges[-1]}"


def load_trades(run_dir: Path) -> list:
    p = run_dir / "trades.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def load_bars(run_dir: Path) -> Optional[pd.DataFrame]:
    p = run_dir / "bars.csv"
    if not p.exists():
        return None
    return pd.read_csv(p)


def compute_episode_boundaries(bars_df: pd.DataFrame) -> list:
    """Activity-transition episode boundaries (bar-index based), same rule as
    prescreen_signal._compute_turnover_proxy and the run_054 audit's episode
    reconstruction: inactive->active opens an episode, active->inactive (or
    sign flip) closes it. Returns [{open_idx, close_idx, entry_time, exit_time,
    direction}], bar-index duration = close_idx - open_idx."""
    episodes = []
    prev_sign = 0
    open_idx = None
    open_sign = None
    timestamps = bars_df["timestamp"].tolist()
    forecasts = bars_df["forecast"].tolist()
    for i, fc in enumerate(forecasts):
        curr_sign = 1 if fc > _ACTIVE_THRESHOLD else (-1 if fc < -_ACTIVE_THRESHOLD else 0)
        if curr_sign != prev_sign:
            if open_idx is not None:
                episodes.append({
                    "open_idx": open_idx, "close_idx": i,
                    "entry_time": timestamps[open_idx], "exit_time": timestamps[i],
                    "direction": open_sign, "duration_bars": i - open_idx,
                })
                open_idx = None
            if curr_sign != 0:
                open_idx = i
                open_sign = curr_sign
        prev_sign = curr_sign
    if open_idx is not None:
        episodes.append({
            "open_idx": open_idx, "close_idx": len(forecasts) - 1,
            "entry_time": timestamps[open_idx], "exit_time": timestamps[-1],
            "direction": open_sign, "duration_bars": len(forecasts) - 1 - open_idx,
        })
    return episodes


def _ts(x):
    return pd.Timestamp(x)


def group_fragments_into_episodes(fragments: list, episodes: list) -> list:
    """Assigns each real trades.json fragment to the episode boundary whose
    span contains the fragment's entry_time (real fragment PnL/attribution,
    not re-derived from bar prices). Each returned episode carries its
    ordered fragment list; fragments[0] is the initial-entry fragment,
    fragments[1:] (if any) are scale-up fragments -- inert (empty) for a
    signal that never scales."""
    bounds = [(i, _ts(e["entry_time"]), _ts(e["exit_time"])) for i, e in enumerate(episodes)]
    groups = {i: [] for i in range(len(episodes))}
    unassigned = []
    for frag in fragments:
        ft = _ts(frag["entry_time"])
        placed = False
        for i, lo, hi in bounds:
            if lo <= ft <= hi:
                groups[i].append(frag)
                placed = True
                break
        if not placed:
            unassigned.append(frag)

    out = []
    for i, e in enumerate(episodes):
        frags = sorted(groups[i], key=lambda f: _ts(f["entry_time"]))
        if not frags:
            continue
        real_pnl = sum(f.get("net_profit_loss_absolute", 0.0) for f in frags)
        out.append({
            **e,
            "fragments": frags,
            "n_fragments": len(frags),
            "is_scaled": len(frags) > 1,
            "episode_pnl_net": real_pnl,
            "episode_profitable": real_pnl > 0,
        })
    return out, unassigned


# ---------------------------------------------------------------------------
# 1. Forecast-bin outcome table
# ---------------------------------------------------------------------------

def build_forecast_bin_table(fragments: list, episodes: list) -> dict:
    """Fragments bucketed by entry-forecast level. basis: lifo_fragment,
    ideation_only. episode_count per bin = count of episodes whose OPENING
    (first) fragment's entry_forecast falls in that bin -- unambiguous even
    for scaled episodes whose later fragments may land in a different bin."""
    bins: dict = {}
    total_cost = sum(f.get("total_commission", 0.0) for f in fragments) or 1.0

    for frag in fragments:
        label = _forecast_bin_label(frag.get("entry_forecast"))
        b = bins.setdefault(label, {
            "fragment_count": 0, "episode_count": 0,
            "aggregate_pnl_net": 0.0, "aggregate_cost": 0.0,
        })
        b["fragment_count"] += 1
        b["aggregate_pnl_net"] += frag.get("net_profit_loss_absolute", 0.0)
        b["aggregate_cost"] += frag.get("total_commission", 0.0)

    for ep in episodes:
        opening_frag = ep["fragments"][0]
        label = _forecast_bin_label(opening_frag.get("entry_forecast"))
        bins.setdefault(label, {
            "fragment_count": 0, "episode_count": 0,
            "aggregate_pnl_net": 0.0, "aggregate_cost": 0.0,
        })
        bins[label]["episode_count"] += 1

    for label, b in bins.items():
        b["aggregate_pnl_net"] = round(b["aggregate_pnl_net"], 4)
        b["aggregate_cost"] = round(b["aggregate_cost"], 4)
        b["cost_share_of_total"] = round(b["aggregate_cost"] / total_cost, 4)

    return {
        "basis": "lifo_fragment, ideation_only",
        "bin_edges": FORECAST_BIN_EDGES,
        "bins": bins,
    }


# ---------------------------------------------------------------------------
# 2. Forecast composition at entry/exit (component attribution)
# ---------------------------------------------------------------------------

def _component_contributions(debug_info: Optional[dict]) -> dict:
    if not debug_info or not isinstance(debug_info, dict):
        return {}
    comps = debug_info.get("components") or {}
    return {name: c.get("weighted_contribution") for name, c in comps.items()
            if isinstance(c, dict) and c.get("weighted_contribution") is not None}


def build_forecast_composition(fragments: list) -> dict:
    """Per-fragment component/indicator contribution breakdown at entry and
    exit, aggregated (mean) per forecast bin. basis: lifo_fragment,
    ideation_only. Answers 'what was actually driving the forecast when this
    fragment opened/closed' -- the debug/attribution view, distinct from the
    scalar forecast magnitude itself."""
    per_bin: dict = {}
    for frag in fragments:
        label = _forecast_bin_label(frag.get("entry_forecast"))
        b = per_bin.setdefault(label, {"entry_contributions": {}, "exit_contributions": {}, "n": 0})
        b["n"] += 1
        for name, val in _component_contributions(frag.get("entry_debug_info")).items():
            b["entry_contributions"].setdefault(name, []).append(val)
        for name, val in _component_contributions(frag.get("exit_debug_info")).items():
            b["exit_contributions"].setdefault(name, []).append(val)

    result = {}
    for label, b in per_bin.items():
        entry_means = {name: round(statistics.mean(vals), 4) for name, vals in b["entry_contributions"].items()}
        exit_means = {name: round(statistics.mean(vals), 4) for name, vals in b["exit_contributions"].items()}
        result[label] = {"n_fragments": b["n"], "entry_component_means": entry_means, "exit_component_means": exit_means}

    return {"basis": "lifo_fragment, ideation_only", "by_bin": result}


# ---------------------------------------------------------------------------
# 3. Increment anatomy (initial-entry vs scale-up fragments)
# ---------------------------------------------------------------------------

def build_increment_anatomy(episodes: list) -> dict:
    """Compares initial-entry fragments (each episode's first fragment)
    against scale-up fragments (every subsequent fragment in a scaled
    episode) on outcome and cost. Inert for a signal that never scales a
    position (every episode has exactly one fragment) -- explicitly flagged
    in the output rather than silently producing an empty/misleading table.
    basis: lifo_fragment, ideation_only."""
    initial = []
    scale_up = []
    for ep in episodes:
        frags = ep["fragments"]
        initial.append(frags[0])
        scale_up.extend(frags[1:])

    def _summ(frags):
        if not frags:
            return {"n": 0, "aggregate_pnl_net": 0.0, "aggregate_cost": 0.0, "mean_pnl_net": None}
        pnl = sum(f.get("net_profit_loss_absolute", 0.0) for f in frags)
        cost = sum(f.get("total_commission", 0.0) for f in frags)
        return {
            "n": len(frags),
            "aggregate_pnl_net": round(pnl, 4),
            "aggregate_cost": round(cost, 4),
            "mean_pnl_net": round(pnl / len(frags), 4),
        }

    inert = len(scale_up) == 0
    return {
        "basis": "lifo_fragment, ideation_only",
        "inert_no_scaling_observed": inert,
        "inert_note": (
            "This signal never scales a position within an episode -- every "
            "episode has exactly one fragment. initial_entry and scale_up "
            "summaries below are structurally uninformative (scale_up is "
            "empty by construction), not a finding."
        ) if inert else None,
        "initial_entry": _summ(initial),
        "scale_up": _summ(scale_up),
    }


# ---------------------------------------------------------------------------
# 4. Episode anatomy by duration and regime
# ---------------------------------------------------------------------------

def _duration_bucket(duration_bars: int) -> str:
    if duration_bars <= 5:
        return "short (<=5 bars)"
    if duration_bars <= 20:
        return "medium (6-20 bars)"
    return "long (>20 bars)"


def build_episode_anatomy(episodes: list) -> dict:
    """Episodes grouped by holding duration and entry regime -- the neutral
    view for duration/regime hypotheses (e.g. a whipsaw-in-choppy-regime
    story), reported as descriptive cross-tabs, not a verdict input. basis:
    lifo_fragment (episode PnL derived from real fragment PnL),
    ideation_only."""
    cells: dict = {}
    for ep in episodes:
        dur_bucket = _duration_bucket(ep["duration_bars"])
        regime = ep["fragments"][0].get("entry_regime") or "unknown"
        key = (dur_bucket, regime)
        c = cells.setdefault(key, {"n_episodes": 0, "n_profitable": 0, "aggregate_pnl_net": 0.0})
        c["n_episodes"] += 1
        c["n_profitable"] += 1 if ep["episode_profitable"] else 0
        c["aggregate_pnl_net"] += ep["episode_pnl_net"]

    table = []
    for (dur_bucket, regime), c in cells.items():
        table.append({
            "duration_bucket": dur_bucket,
            "regime": regime,
            "n_episodes": c["n_episodes"],
            "win_rate_pct": round(100 * c["n_profitable"] / c["n_episodes"], 2),
            "aggregate_pnl_net": round(c["aggregate_pnl_net"], 4),
        })
    table.sort(key=lambda r: (r["regime"], r["duration_bucket"]))

    return {"basis": "lifo_fragment, ideation_only", "table": table}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def compute_fragment_patterns_for_run(run_dir: Path, protocol_result: dict) -> dict:
    """Aggregates all four fragment_patterns tables across every
    window-symbol result in protocol_result['results']. run_dir is the
    hypothesis run root (e.g. strategy-research/runs/run_054); each window's
    trades.json/bars.csv live under run_dir/results/<run_id>/."""
    all_fragments = []
    all_episodes = []
    total_unassigned = 0

    for r in protocol_result["results"]:
        window_dir = run_dir / "results" / r["run_id"]
        fragments = load_trades(window_dir)
        bars_df = load_bars(window_dir)
        if not fragments or bars_df is None or "forecast" not in bars_df.columns:
            continue
        boundaries = compute_episode_boundaries(bars_df)
        episodes, unassigned = group_fragments_into_episodes(fragments, boundaries)
        total_unassigned += len(unassigned)
        all_fragments.extend(fragments)
        all_episodes.extend(episodes)

    return {
        "run_id": run_dir.name,
        "artifact": "fragment_patterns.yaml",
        "basis": "lifo_fragment, ideation_only",
        "firewall_note": (
            "IDEATION-ONLY diagnostic artifact. Never read by "
            "evaluate_against_decision_rules, any Gate, or "
            "verdict_interpreter's required inputs -- see "
            "test_fragment_patterns_firewall.py. May be cited by "
            "campaign_review / proposed-brief drafting as a "
            "motivating_observation for a NEW candidate hypothesis, which "
            "must still earn verdict-grade status through its own "
            "pre-registered test. Never cited to relitigate an "
            "already-recorded verdict."
        ),
        "n_fragments_total": len(all_fragments),
        "n_episodes_total": len(all_episodes),
        "n_fragments_unassigned": total_unassigned,
        "forecast_bin_table": build_forecast_bin_table(all_fragments, all_episodes),
        "forecast_composition": build_forecast_composition(all_fragments),
        "increment_anatomy": build_increment_anatomy(all_episodes),
        "episode_anatomy": build_episode_anatomy(all_episodes),
    }


def write_fragment_patterns_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
