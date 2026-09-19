"""
episode_significance.py — A8.5.1a: episode-blocked significance.

New methodology (not an extension of an existing rule) for computing IC significance
on sparse signals over data spanning multiple disjoint eras (e.g. the P1b backward
extension: 2018-01 pre-funding era, 2019-09-2023 funding-available era, 2024-2025
existing baseline_v2 window). Full spec recorded in
engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md under "A8.5.1a-spec".

Motivation: the existing _block_adjusted_significance() in prescreen_signal.py treats
active-bar n_eff as n_active_bars / block_size (24 bars, fixed), which assumes bars
within a block are the only source of autocorrelation. A sparse signal whose active
bars cluster into long real-world episodes (e.g. every funding-extreme event lasting
days) has autocorrelation that spans far more than one 24-bar block — treating each
24-bar chunk as independent evidence overstates the effective sample size.

Spec summary (verbatim from pre-registration, condensed):
  - Episode: a maximal run of active bars where consecutive active bars are
    separated by <= G inactive bars (G default 48 bars @ 1h ~= 2 days). Gaps > G,
    OR an era boundary, close the episode — an episode never spans an era boundary
    even if the gap between two active bars is small.
  - Bootstrap statistic: pooled active-bar IC (Spearman over all active bars in the
    episode set, pooled). Resample episodes WITH replacement (same episode count),
    keeping each episode's internal bars intact; recompute pooled IC per resample.
    p-value / CI come from that resampled distribution.
  - Headline sample size is n_episodes, reported alongside active_n_bars. Minimum
    for ANY significance claim: n_episodes >= 8. Below that floor, report descriptive
    statistics only — disposition stays insufficient_sample_inconclusive regardless
    of p-value ("a bootstrap over 4 episodes is theater").
  - Density fallback: if activation >= 50% of bars (dense signal), episodes degenerate
    into the whole series — use the existing 24-bar block method unchanged.
  - Era stratification is REPORTING, not resampling: per-era IC/episode counts are
    reported for context, but the bootstrap itself pools across eras.
"""

import math
import random
import re
import statistics
from collections import defaultdict

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))               # strategy-research/tools/
_REPO = os.path.dirname(os.path.dirname(_HERE))                    # repo root
_TBOT = os.path.join(_REPO, "trading-bot")                         # trading-bot/
for _p in (_HERE, _TBOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Repointed 2026-09-12 (E-039 step 5): sourced from
# trading-bot/performance/signal_statistics.py, not prescreen_signal.py
# (being removed) -- same functions, verbatim ports, lockstep-tested there.
from performance.signal_statistics import (  # noqa: E402
    spearman_correlation as _spearman,
    contiguous_segments as _contiguous_segments,
    pooled_block_adjusted_significance as _block_adjusted_significance,
)

# F4d (2026-07-05): single source of truth for "did this prescreen actually go
# through the A8.5.1a dispatcher" — used by the orchestrator's pre-registration
# conformance gate to distinguish a genuine A8.5.1a outcome (any of these three)
# from "the significance_methodology flag was absent/ignored and the OLD default
# block_24_fisher_z path ran instead" (prescreen_signal.py's own default label,
# NOT a member of this set).
VALID_METHODS = {
    "episode_block_bootstrap",
    "episode_bootstrap_insufficient_n",
    "block_24_dense_fallback",
}

# The dense-fallback outcome (A8.5.1a rule 4) stamps the block size it actually
# divided by, so its label is a FAMILY — block_6_dense_fallback at 4h,
# block_1_dense_fallback at 1d — not the single literal above. Acceptance must be
# a predicate, not membership in the closed set, or a correctly-derived label
# halts the conformance gate on every non-1h run. block_<n>_fisher_z stays
# rejected for every n: it is prescreen_signal.py's OLD default label, and its
# presence means the significance_methodology flag was absent/ignored.
_DENSE_FALLBACK_RE = re.compile(r"block_\d+_dense_fallback")


def is_a851a_method(label) -> bool:
    """True iff `label` is a genuine A8.5.1a dispatcher outcome: either episode
    method, or a dense-fallback label for any block size."""
    return label in VALID_METHODS or bool(_DENSE_FALLBACK_RE.fullmatch(label or ""))

_DEFAULT_GAP_BARS = 48
_DEFAULT_DENSITY_FALLBACK_PCT = 50.0
_MIN_N_EPISODES = 8
_DEFAULT_N_RESAMPLES = 2000
_SIG_THRESHOLD = 0.10


# ---------------------------------------------------------------------------
# Episode construction
# ---------------------------------------------------------------------------

def identify_episodes(records: list, gap_bars: int = _DEFAULT_GAP_BARS, era_of=None,
                      expected_step=None) -> list:
    """
    records: list of per-bar dicts (order = original bar sequence) each with an
        "active" bool key (as produced by prescreen_signal._extract_forecasts).
    era_of: optional callable(bar_index) -> era_id. When provided, an episode is
        also closed at any era boundary regardless of gap size.
    expected_step: optional pd.Timedelta bar step. When given, the gap between
        two consecutive active bars is measured in TRUE elapsed bars, not list
        positions (GH#66 / CUL-20, the #50 family) -- a data hole between them
        adds its missing bars to the gap, so a large enough hole splits an
        episode a positional count would silently merge. None reproduces the
        pre-gap-aware positional behaviour byte-for-byte.

    Returns a list of episodes; each episode is a list of the ACTIVE bar indices
    belonging to it (inactive bars in between are not members of any episode —
    they only affect whether the run closes).
    """
    active_idx = [i for i, r in enumerate(records) if r.get("active")]
    if not active_idx:
        return []

    # Segment membership per record index (shared #50 helper). Two active bars
    # in the same contiguous segment have no hole between them, so curr-prev-1
    # already equals the true bar-gap (byte-identical); across a segment
    # boundary the true gap comes from the timestamps. seg_of stays None on the
    # positional (expected_step is None) path so nothing changes there.
    seg_of = None
    if expected_step is not None:
        seg_of = [0] * len(records)
        for sid, (s, e) in enumerate(
                _contiguous_segments(records, expected_step)):
            for i in range(s, e):
                seg_of[i] = sid

    episodes = []
    current = [active_idx[0]]
    for prev, curr in zip(active_idx, active_idx[1:]):
        # Gap-awareness fires only on an intra-symbol data hole: prev/curr in
        # different contiguous segments AND the same symbol. A SYMBOL boundary
        # is also a segment break in the pooled record list, but it is a
        # separate concern (GH#66 §7 / observation O1) -- keeping it on the
        # positional gap leaves the pooled-symbol behaviour exactly as it was.
        # records without a "symbol" key (single-symbol fixtures) read as one
        # symbol, so intra-symbol holes are still measured.
        cross_segment = seg_of is not None and seg_of[prev] != seg_of[curr]
        same_symbol = records[prev].get("symbol") == records[curr].get("symbol")
        if cross_segment and same_symbol:
            # a hole intervenes; measure it in true bars. Integer floordiv on
            # the timedelta is exact for grid-aligned bars (the pre-registration's
            # round(delta / step) form, without float).
            gap = int((records[curr]["timestamp"] - records[prev]["timestamp"])
                      // expected_step) - 1
        else:
            gap = curr - prev - 1
        era_break = era_of is not None and era_of(prev) != era_of(curr)
        if gap <= gap_bars and not era_break:
            current.append(curr)
        else:
            episodes.append(current)
            current = [curr]
    episodes.append(current)
    return episodes


def _pooled_ic(records: list, indices: list):
    if not indices:
        return None
    fs = [records[i]["forecast"] for i in indices]
    rs = [records[i]["next_return_bps"] for i in indices]
    return _spearman(fs, rs)


# ---------------------------------------------------------------------------
# Episode block bootstrap
# ---------------------------------------------------------------------------

def episode_block_bootstrap(
    records: list,
    episodes: list,
    n_resamples: int = _DEFAULT_N_RESAMPLES,
    seed: int | None = None,
) -> dict:
    """
    Resample episodes with replacement (same episode count as observed), pool the
    active bars of the resampled episodes, recompute pooled IC per resample.
    p_value / CI are read off that bootstrap distribution.
    """
    rng = random.Random(seed)
    n_ep = len(episodes)

    all_active_idx = [i for ep in episodes for i in ep]
    point_ic = _pooled_ic(records, all_active_idx)

    if point_ic is None:
        return {
            "method": "episode_block_bootstrap",
            "pooled_ic": None, "p_value": 1.0,
            "ci_low": None, "ci_high": None,
            "n_episodes": n_ep, "n_resamples": n_resamples,
            "significant": False,
        }

    boot_ics = []
    for _ in range(n_resamples):
        sampled_eps = [episodes[rng.randrange(n_ep)] for _ in range(n_ep)]
        idx = [i for ep in sampled_eps for i in ep]
        ic = _pooled_ic(records, idx)
        if ic is not None:
            boot_ics.append(ic)

    if not boot_ics:
        return {
            "method": "episode_block_bootstrap",
            "pooled_ic": round(point_ic, 6), "p_value": 1.0,
            "ci_low": None, "ci_high": None,
            "n_episodes": n_ep, "n_resamples": n_resamples,
            "significant": False,
        }

    boot_ics.sort()
    n = len(boot_ics)
    ci_low = boot_ics[int(0.05 * n)]
    ci_high = boot_ics[min(int(0.95 * n), n - 1)]

    # Two-tailed p-value: proportion of the bootstrap distribution on the side of
    # zero opposite the point estimate's dominant side, doubled (reflection method).
    prop_le_0 = sum(1 for v in boot_ics if v <= 0) / n
    prop_ge_0 = sum(1 for v in boot_ics if v >= 0) / n
    p_value = min(2.0 * min(prop_le_0, prop_ge_0), 1.0)

    return {
        "method": "episode_block_bootstrap",
        "pooled_ic": round(point_ic, 6),
        "p_value": round(p_value, 4),
        "ci_low": round(ci_low, 6),
        "ci_high": round(ci_high, 6),
        "n_episodes": n_ep,
        "n_resamples": n_resamples,
        "significant": bool(p_value < _SIG_THRESHOLD),
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def compute_a851a_significance(
    records: list,
    era_of=None,
    gap_bars: int = _DEFAULT_GAP_BARS,
    density_fallback_pct: float = _DEFAULT_DENSITY_FALLBACK_PCT,
    min_n_episodes: int = _MIN_N_EPISODES,
    block_size: int | None = None,
    n_resamples: int = _DEFAULT_N_RESAMPLES,
    seed: int | None = None,
    expected_step=None,
) -> dict:
    """
    A8.5.1a dispatcher. Returns a dict always containing at least:
      method, pooled_ic, p_value, n_episodes, density_pct, significant
    plus method-specific fields (ci_low/ci_high for the bootstrap path).

    `block_size` is required (no silent default): a wrong block size mislabels
    and misdivides the dense-fallback path. Derive it from the timeframe via
    tools.timeframe.bars_per_day.
    """
    if block_size is None:
        raise ValueError(
            "block_size is required — derive it from the timeframe via "
            "tools.timeframe.bars_per_day; the removed silent default of 24 was "
            "the block-size bug class (CUL-9/CUL-51)"
        )
    n_total = len(records)
    active_idx_all = [i for i, r in enumerate(records) if r.get("active")]
    n_active = len(active_idx_all)
    density_pct = (n_active / n_total * 100.0) if n_total else 0.0

    if density_pct >= density_fallback_pct:
        ic_active = _pooled_ic(records, active_idx_all)
        ic_values_for_sig = [ic_active] if ic_active is not None else []
        sig = _block_adjusted_significance(ic_values_for_sig, n_active, block_size)
        return {
            "method": f"block_{block_size}_dense_fallback",
            "pooled_ic": sig["pooled_ic"],
            "p_value": sig["p_value"],
            "ci_low": None, "ci_high": None,
            "n_episodes": None,
            "density_pct": round(density_pct, 2),
            "significant": sig["significant"],
        }

    episodes = identify_episodes(records, gap_bars=gap_bars, era_of=era_of,
                                 expected_step=expected_step)
    n_episodes = len(episodes)

    if n_episodes < min_n_episodes:
        ic_active = _pooled_ic(records, active_idx_all)
        return {
            "method": "episode_bootstrap_insufficient_n",
            "pooled_ic": round(ic_active, 6) if ic_active is not None else None,
            "p_value": None,
            "ci_low": None, "ci_high": None,
            "n_episodes": n_episodes,
            "density_pct": round(density_pct, 2),
            "significant": False,
            "disposition_note": "insufficient_sample_inconclusive",
        }

    result = episode_block_bootstrap(records, episodes, n_resamples=n_resamples, seed=seed)
    result["density_pct"] = round(density_pct, 2)
    return result


def per_era_report(records: list, era_of, gap_bars: int = _DEFAULT_GAP_BARS,
                   expected_step=None) -> dict:
    """
    Reporting-only per-era breakdown (A8.5.1a: "era stratification is reporting, not
    resampling"). Does not feed into the bootstrap.
    """
    episodes = identify_episodes(records, gap_bars=gap_bars, era_of=era_of,
                                 expected_step=expected_step)

    by_era_active = defaultdict(list)
    for i, r in enumerate(records):
        if r.get("active"):
            by_era_active[era_of(i)].append(i)

    by_era_episode_count = defaultdict(int)
    for ep in episodes:
        by_era_episode_count[era_of(ep[0])] += 1

    report = {}
    for era_id in set(list(by_era_active.keys()) + list(by_era_episode_count.keys())):
        idxs = by_era_active.get(era_id, [])
        ic = _pooled_ic(records, idxs)
        # F4e (2026-07-05, run_050): era_of(i) may legitimately return a tuple
        # (e.g. prescreen_signal.py's (symbol, era_id) — needed to keep episodes
        # symbol-bounded when pooled). A tuple dict key round-trips fine through
        # yaml.safe_dump but CRASHES yaml.safe_load on read-back ("found unhashable
        # key") because it deserializes a YAML complex-mapping-key sequence as a
        # Python list, not a tuple. Stringify at this output boundary only — all
        # internal grouping above still uses the raw (hashable) era_of() return
        # value, which is correct and unaffected.
        key = "::".join(str(part) for part in era_id) if isinstance(era_id, tuple) else str(era_id)
        report[key] = {
            "ic_active_bars": round(ic, 6) if ic is not None else None,
            "active_n_bars": len(idxs),
            "n_episodes": by_era_episode_count.get(era_id, 0),
        }
    return report
