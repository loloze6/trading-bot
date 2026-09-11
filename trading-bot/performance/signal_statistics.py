"""
Shared, degenerate-safe statistics for forecast/signal series.

HARD RULE (2026-07-09, P4_ts_trend incident): a zero-variance input makes a
correlation coefficient mathematically UNDEFINED, not zero. This happens
whenever a signal's forecast is a single constant magnitude across every bar
being correlated against (e.g. a long-only component that outputs exactly
+10.0 whenever active, never varying, never negative -- filtering to
active-bars-only then leaves zero variance to correlate against returns).

Two independent call sites (strategy-research/tools/prescreen_signal.py and
trading-bot/reporting/run_artifact.py::build_core) each hand-rolled their own
correlation with their own degenerate-case handling. prescreen_signal.py's
version correctly returned None. run_artifact.py's version fell back to a
hardcoded corr=0.0, and then computed a p-value FROM that fake 0.0 (p=1.0) --
producing a "corr=0.0, p=1.0, high confidence no-edge" result that is actually
a mathematical artifact of the signal's SHAPE, not evidence about its quality.
This surfaced when the two stages' outputs materially disagreed (prescreen:
pooled_ic=0.0359, p=0.004, significant; full backtest: corr=0.0, p=1.0,
identically across all 24 window-symbol pairs) -- a pattern that should never
coexist silently (see run_protocol.py's prescreen/backtest cross-check).

Every consumer of a forecast-vs-return correlation MUST use these functions
(or another function that composes them) instead of hand-rolling the same
logic a third time:
  - Zero variance in EITHER series -> return None. Never 0.0, never False.
  - No p-value is ever computed from an undefined (None) correlation.
"""
import math
import statistics
from typing import Optional, Sequence


def has_zero_variance(values: Sequence[float], tol: float = 1e-10) -> bool:
    """True if `values` has no variance (all elements effectively identical,
    or fewer than 2 elements). Works with plain lists or numpy arrays."""
    n = len(values)
    if n < 2:
        return True
    mean = sum(values) / n
    return sum((v - mean) ** 2 for v in values) < tol


def pearson_correlation(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    """
    Pearson correlation coefficient. Returns None (never a fabricated 0.0)
    when either series has zero variance -- mathematically undefined, not
    "no correlation found."
    """
    n = len(x)
    if n < 2 or len(y) != n:
        return None
    if has_zero_variance(x) or has_zero_variance(y):
        return None

    x_mean = sum(x) / n
    y_mean = sum(y) / n
    xm = [v - x_mean for v in x]
    ym = [v - y_mean for v in y]
    denom = math.sqrt(sum(v * v for v in xm) * sum(v * v for v in ym))
    if denom < 1e-12:
        return None
    corr = sum(a * b for a, b in zip(xm, ym)) / denom
    return max(-1.0, min(1.0, corr))


def spearman_correlation(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    """
    Spearman rank correlation. Returns None (never a fabricated 0.0) when
    either series is constant in rank space (fewer than 3 points, or all
    values tie into a single rank) -- mathematically undefined.
    """
    n = len(x)
    if n < 3 or len(y) != n:
        return None

    def _rank(vals):
        sorted_i = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and vals[sorted_i[j + 1]] == vals[sorted_i[j]]:
                j += 1
            avg_r = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[sorted_i[k]] = avg_r
            i = j + 1
        return ranks

    rx = _rank(x)
    ry = _rank(y)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    cov = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n)) / n
    std_rx = math.sqrt(sum((r - mean_rx) ** 2 for r in rx) / n)
    std_ry = math.sqrt(sum((r - mean_ry) ** 2 for r in ry) / n)
    if std_rx < 1e-10 or std_ry < 1e-10:
        return None
    return cov / (std_rx * std_ry)


def t_test_pvalue(corr: Optional[float], n: int) -> Optional[float]:
    """
    Two-tailed t-test p-value for a correlation coefficient computed on n
    paired observations. HARD RULE: if corr is None (undefined), returns None
    -- a p-value is NEVER fabricated from an undefined statistic. Computing
    p=1.0 from a fake corr=0.0 is the same "displaying undefined as measured"
    defect as printing an undefined IC as the literal string "0.0000".
    """
    if corr is None:
        return None
    if abs(corr) >= 1.0:
        return 0.0
    if n <= 2:
        return None
    try:
        from scipy.stats import t as t_dist
    except ImportError:
        return None
    t_stat = corr * math.sqrt((n - 2) / (1.0 - corr ** 2))
    return float(2 * t_dist.sf(abs(t_stat), df=n - 2))


# ---------------------------------------------------------------------------
# Block-adjusted (autocorrelation-aware) significance -- CUL-262, 2026-09-04
# ---------------------------------------------------------------------------
#
# `t_test_pvalue` above treats every bar as an independent observation. Real
# bars are autocorrelated (adjacent hours move together), so it systematically
# overstates significance -- measured as a real gap in E-039's prescreen vs.
# backtest parity check: `strategy-research/tools/prescreen_signal.py`'s
# `_block_adjusted_significance`/`_gap_aware_block_count` already correct for
# this on the prescreen side, dividing by an effective sample size (n_eff)
# instead of the raw bar count, and (the #50(B) fix, PR #137/CUL-15) refusing
# to count a block that would span a real data gap.
#
# These two functions are a VERBATIM algorithmic port of that pair, not a
# reimplementation from a blank page and not an import -- `prescreen_signal.py`
# already imports FROM this module (`from performance.signal_statistics import
# spearman_correlation`), and trading-bot must never import from
# strategy-research (that would invert the repo's one-way dependency
# direction). This module is exactly the place the two independent hand-rolled
# implementations problem this file's own docstring describes gets fixed --
# porting the math here, rather than leaving the backtest side to hand-roll a
# THIRD version, is that fix applied to this specific statistic.
#
# `bars_per_day`-style timeframe-string parsing is deliberately NOT ported:
# trading-bot already carries the equivalent quantity as
# `candle_interval_seconds` (an int), so the block size is `86400 //
# candle_interval_seconds`, floored at 1 -- no string parser needed here.

def gap_aware_active_block_count(records: list, block_size: int,
                                  expected_step) -> int:
    """
    Count of blocks of ACTIVE bars that can be placed without spanning a real
    data gap. Verbatim port of
    `prescreen_signal.py::_gap_aware_block_count`'s algorithm (see that
    function's docstring for the full rationale and the measured inflation a
    gap-naive count produces, up to 1.67x on one real symbol).

    Each record must carry `"active"` (bool-ish) and `"timestamp"` keys, in
    bar order. `expected_step=None` returns the ungapped count (`total_active
    // block_size`), reproducing pre-gap-awareness behavior exactly -- this is
    what happens when the caller has no timestamp column to derive a step
    from, so degrading to "assume contiguous" rather than refusing to compute
    anything at all.
    """
    if block_size < 1:
        raise ValueError(f"block_size must be >= 1, got {block_size!r}")
    active_flags = [bool(r.get("active")) for r in records]
    if expected_step is None:
        return sum(active_flags) // block_size

    total = 0
    run_active = 0
    for i, rec in enumerate(records):
        run_active += 1 if active_flags[i] else 0
        is_last = i == len(records) - 1
        breaks = is_last or (records[i + 1]["timestamp"] - rec["timestamp"]) != expected_step
        if breaks:
            total += run_active // block_size
            run_active = 0
    return total


def block_adjusted_pvalue(corr: Optional[float], n_active: int, block_size: int,
                           placeable_blocks: Optional[int] = None):
    """
    Two-tailed, block-adjusted significance for a SINGLE correlation value
    (one run, not prescreen's list-of-window-ICs shape). Verbatim port of the
    Fisher-z core of `prescreen_signal.py::_block_adjusted_significance`:
    N_eff = n_active // block_size (or `placeable_blocks` when the caller has
    already computed the gap-aware count via `gap_aware_active_block_count`),
    z = corr * sqrt(N_eff - 3), two-tailed normal-approximation p-value.

    Returns `(p_value, n_eff)`. `(None, None)` when `corr is None` -- a
    p-value is never fabricated from an undefined correlation, same hard rule
    as `t_test_pvalue`.
    """
    if corr is None:
        return None, None
    blocks = (n_active // max(block_size, 1)) if placeable_blocks is None else placeable_blocks
    n_eff = max(blocks, 1)
    if abs(corr) >= 1.0:
        return 0.0, n_eff
    dof = max(n_eff - 3, 1)
    z_stat = corr * math.sqrt(dof)
    p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z_stat) / math.sqrt(2.0))))
    return round(p_value, 6), n_eff


# ---------------------------------------------------------------------------
# Post-backtest go/no-go (A8.1) -- CUL-264, 2026-09-04
# ---------------------------------------------------------------------------
#
# Verbatim port of prescreen_signal.py's cost hurdle (`_cost_check`) and route
# decision (`_determine_route`), same reasoning as the block-adjusted
# significance functions above: port the math here rather than let the
# backtest side hand-roll a third version, since trading-bot cannot import
# strategy-research. The one semantic change: prescreen's passing route is
# named `proceed_to_backtest` because the backtest hasn't run yet when IT
# decides; here the backtest has ALREADY run, so the equivalent passing route
# is named `proceed_to_interpretation` -- an LLM verdict call is warranted.
#
# INFORMATIONAL ONLY (CUL-264 scope, explicit): this module computes and
# returns a route. Nothing in this repository currently reads that route to
# skip, gate, or short-circuit anything -- whether a mechanical kill should
# actually skip the LLM interpretation step is a separate decision, not made
# here. See CUL-264's Linear issue, closing section.

_SIG_THRESHOLD = 0.10          # prescreen_signal.py::_SIG_THRESHOLD, same value
_DEFAULT_SIGMA_BAR_BPS = 15.0  # prescreen_signal.py::_DEFAULT_SIGMA_BAR_BPS, same value


# ---------------------------------------------------------------------------
# Minimum-observations safeguard (CUL-264 follow-up, 2026-09-11)
# ---------------------------------------------------------------------------
#
# determine_route() below classifies purely from a p-value and a cost-hurdle
# ratio -- nothing upstream of that math ever asked whether there were even
# enough observations to trust the test computing them. Left unguarded, a
# hypothesis that failed because it had almost no data (n_eff=1, or a single
# completed trade averaged into "the" edge) gets the exact same label
# (kill_no_ic / kill_cost_hurdle / ...) as one that genuinely showed nothing
# on an abundant sample. Those are epistemically different -- "we don't know
# yet" is not "we now know it doesn't work" -- but nothing distinguished them
# before this. `determine_route` now checks this FIRST, before the
# significance/cost math runs at all, and routes to
# `inconclusive_insufficient_data` instead.
#
# PROPOSED DEFAULTS, NOT A SETTLED NUMBER -- flag for explicit sign-off. Two
# different statistical quantities get their own floor rather than one
# invented number applied twice:
#
# `_MIN_N_EFF_FOR_ROUTE` (estimated path, CUL-264, keyed on n_eff): n_eff is
# already a block count (each unit is a whole day's worth of active 1h bars,
# per `block_adjusted_pvalue` above), coarser and more conservative than a
# raw bar count. That function's own z-test computes
# `dof = max(n_eff - 3, 1)` (line ~207 above): for every n_eff in
# {0, 1, 2, 3, 4} that expression clamps to the SAME dof=1 -- the test
# statistic cannot even distinguish n_eff=1 from n_eff=4, so below 5 "degrees
# of freedom" isn't tracking sample size at all, just reporting its own
# floor. 5 is the smallest n_eff where dof starts actually varying with it
# (dof=2 at n_eff=5) instead of returning a constant regardless of how little
# data there was -- a floor derived from the significance math already in
# this file, not picked freehand. It also happens to match
# `sigma_bar_bps_from_returns`'s own "< 5 -> don't trust it" rule immediately
# below, giving this file one internally-consistent floor for "too few to
# trust" rather than two arbitrary numbers doing the same conceptual job.
#
# `_MIN_TRADES_FOR_ROUTE` (real path, CUL-272, keyed on completed-trade
# count): a trade count is a materially different, noisier quantity than
# n_eff -- a single trade can span many bars, so "5 trades" carries far less
# statistical information than "5 independent blocks of bars" does. Reusing
# 5 here is deliberately a floor-of-floors: it only rules out the degenerate
# "average of 1 trade" case this safeguard exists to catch, and is NOT a
# claim that 5 trades is a trustworthy sample to route on -- this repo's own
# research protocol (`CLAUDE.fork.md`) requires >=100 trades (or >=30
# independent episodes) before a Sharpe may even be quoted. If review decides
# 5 is too lenient for a real-money-adjacent decision, raise
# `_MIN_TRADES_FOR_ROUTE` independently of `_MIN_N_EFF_FOR_ROUTE` -- nothing
# ties them together except that they start from the same number today.
_MIN_N_EFF_FOR_ROUTE  = 5
_MIN_TRADES_FOR_ROUTE = 5


def sigma_bar_bps_from_returns(returns_bps: Sequence[float]) -> tuple:
    """
    Per-bar return volatility in bps, or a loud placeholder. Verbatim port of
    `prescreen_signal.py::_sigma_from_records`'s logic (that function reads its
    own `next_return_bps` field off a records list; this takes the bps values
    directly since build_core already has them as a plain sequence).

    Returns (sigma_bar_bps, is_placeholder). is_placeholder=True means fewer
    than 5 returns were available and `_DEFAULT_SIGMA_BAR_BPS` was substituted
    -- prescreen's own rule is that a cost check resting on this value is
    invalid and must not be cited as measured. Callers should propagate this
    flag rather than silently trusting the number.
    """
    if len(returns_bps) < 5:
        return _DEFAULT_SIGMA_BAR_BPS, True
    return statistics.stdev(returns_bps), False


def cost_check(ic_active: Optional[float], sigma_bar_bps: float,
                avg_holding_bars: Optional[float], round_trip_cost_bps: float,
                safety_factor: float = 2.0) -> dict:
    """
    Layer 2 cost hurdle (A8.1). Verbatim port of
    `prescreen_signal.py::_cost_check`'s math:

        estimated_gross_edge_bps_per_trade = |ic_active| * sigma_bar_bps * sqrt(avg_holding_bars)
        edge_to_cost_ratio = gross_edge / round_trip_cost_bps
        pass = (ratio >= safety_factor)

    `symbol`/`cost_model` dict lookup is the caller's job here (build_core
    resolves `round_trip_cost_bps`/`safety_factor` from `cost_model.yaml`
    before calling this) -- this function takes the resolved numbers directly,
    unlike prescreen's version which resolves them internally per-symbol.
    """
    if ic_active is None or avg_holding_bars is None or avg_holding_bars <= 0:
        return {
            "estimated_gross_edge_bps_per_trade": None,
            "cost_bps_per_trade":                 round_trip_cost_bps,
            "edge_to_cost_ratio":                  None,
            "safety_factor_required":              safety_factor,
            "pass":                                False,
        }
    gross_edge = abs(ic_active) * sigma_bar_bps * math.sqrt(max(avg_holding_bars, 1.0))
    ratio      = gross_edge / round_trip_cost_bps if round_trip_cost_bps > 0 else 0.0
    return {
        "estimated_gross_edge_bps_per_trade": round(gross_edge, 4),
        "cost_bps_per_trade":                 round_trip_cost_bps,
        "edge_to_cost_ratio":                 round(ratio, 4),
        "safety_factor_required":             safety_factor,
        "pass":                               bool(ratio >= safety_factor),
    }


def determine_route(pooled_ic: Optional[float], p_value: Optional[float],
                     cost: dict,
                     n_eff: Optional[int] = None,
                     n_trades: Optional[int] = None,
                     sigma_is_placeholder: bool = False,
                     min_n_eff: int = _MIN_N_EFF_FOR_ROUTE,
                     min_n_trades: int = _MIN_TRADES_FOR_ROUTE) -> tuple:
    """
    Verbatim port of `prescreen_signal.py::_determine_route`'s priority logic,
    PLUS a minimum-observations safeguard (CUL-264 follow-up) checked FIRST,
    before the significance/cost math runs at all:

        0. Sample too small to trust (n_eff < min_n_eff, or n_trades <
           min_n_trades, or the cost check rests on a placeholder sigma) ->
           inconclusive_insufficient_data. This is NOT a verdict -- it means
           "not enough information to judge this," and must never be
           confused with kill_no_ic/kill_cost_hurdle, which mean "judged and
           failed."
        1. IC not significant (p >= _SIG_THRESHOLD) -> kill_no_ic
        2. IC significant, NEGATIVE -> refine_inverted_ic
        3. IC significant, positive, cost fails structurally (p > 0.05 or
           ratio < 0.5) -> kill_cost_hurdle
        4. IC significant, positive, cost fails marginally -> refine_cost_hurdle
        5. Both pass -> proceed_to_interpretation (prescreen's own
           `proceed_to_backtest`, renamed: the backtest has already run by the
           time this function is called)

    `n_eff`/`n_trades` are optional and independently checked -- a caller
    that only has one of the two quantities (e.g. the estimated path has
    n_eff but no real trade count) passes only that one; omitting both (the
    default) skips step 0 entirely, preserving the pre-existing 3-positional-
    arg call shape byte-identically for any caller that hasn't been updated
    to pass sample-size information yet.

    Returns (route: str, rationale: str).
    """
    insufficiency_reasons = []
    if n_eff is not None and n_eff < min_n_eff:
        insufficiency_reasons.append(
            f"n_eff={n_eff} < min_n_eff={min_n_eff} (block-adjusted effective "
            f"sample size is below the floor needed to trust the significance "
            f"test)"
        )
    if n_trades is not None and n_trades < min_n_trades:
        insufficiency_reasons.append(
            f"n_trades={n_trades} < min_n_trades={min_n_trades} (too few "
            f"completed trades to trust an average built from them)"
        )
    if sigma_is_placeholder:
        insufficiency_reasons.append(
            "sigma_bar_bps is a placeholder (fewer than 5 return observations "
            "were available to measure real volatility) -- a cost check "
            "resting on it is not a measurement"
        )
    if insufficiency_reasons:
        return (
            "inconclusive_insufficient_data",
            "Insufficient data to reach a verdict: "
            + "; ".join(insufficiency_reasons) + ".",
        )

    significant = p_value is not None and p_value < _SIG_THRESHOLD
    ic          = pooled_ic if pooled_ic is not None else 0.0
    ic_str      = f"{pooled_ic:.4f}" if pooled_ic is not None else "undefined"
    p           = p_value if p_value is not None else 1.0
    cost_pass   = cost.get("pass", False)
    ratio       = cost.get("edge_to_cost_ratio")
    ratio_str   = f"{ratio:.4f}" if ratio is not None else "N/A"
    safety      = cost.get("safety_factor_required", 2.0)

    if not significant:
        return (
            "kill_no_ic",
            f"Active-bar IC={ic_str}, p={p:.4f} >= {_SIG_THRESHOLD}. "
            f"Signal has no detectable directional content.",
        )

    if ic < 0:
        return (
            "refine_inverted_ic",
            f"Active-bar IC={ic_str} (negative, significant at p={p:.4f}). "
            f"Signal direction is inverted -- flip polarity.",
        )

    if not cost_pass:
        edge_str = (
            f"{cost.get('estimated_gross_edge_bps_per_trade'):.1f} bps"
            if cost.get("estimated_gross_edge_bps_per_trade") is not None else "N/A"
        )
        cost_str = f"{cost.get('cost_bps_per_trade', 'N/A')} bps"
        if p > 0.05 or (ratio is not None and ratio < 0.5):
            return (
                "kill_cost_hurdle",
                f"Active-bar IC={ic_str} (p={p:.4f}, marginal). Est. gross edge "
                f"{edge_str} vs cost {cost_str} (ratio={ratio_str} < {safety}). "
                f"Structural cost barrier.",
            )
        return (
            "refine_cost_hurdle",
            f"Active-bar IC={ic_str} (significant, p={p:.4f}), but est. gross "
            f"edge {edge_str} vs cost {cost_str} (ratio={ratio_str} < required "
            f"{safety}). Fix: wider threshold or longer holding.",
        )

    return (
        "proceed_to_interpretation",
        f"Active-bar IC={ic_str} (p={p:.4f}, significant). Edge-to-cost "
        f"ratio={ratio_str} >= {safety}. Signal passes both IC and cost gates.",
    )
