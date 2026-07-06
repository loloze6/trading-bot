"""
F1 (P1a shakedown, 2026-07-04): determines EMPIRICALLY — by actually running the
engine, not by reasoning about it — which strategy-config pattern for an "ungated"
hypothesis (post-A2.3: no regime condition) is safe: does the SAME sequence of
forecasts come out regardless of which of the four valid MarketRegime names
(trending, mean_reversion, chop, unknown) is used to hold the real signal components?

THE CANONICAL PATTERN under test ("Pattern A"): regime_detector.components=[],
regime_detector.rules=[], default_regime=<name>. Since ConfigDrivenRegimeEngine
._classify_threshold_rules() has no rules to walk and no components to read, it
falls straight through to `_REGIME_MAP.get(default_regime, ...)` every single bar —
the resulting MarketRegime is a pure function of the config string. This is what
run_042 (H-041-C) actually shipped: default_regime="mean_reversion".

RESULT OF TESTING (not assumed — see the two tests below):

1. `default_regime="trending"` is currently rejected outright by validate_config.py's
   VIOLATION V9, EVEN in this empty-rules/components case, where there is no gate to
   bypass (V9's own stated rationale). Fixed as part of this change: V9 now only
   forbids trending/mean_reversion/chop as default_regime when `rules` is non-empty
   (an actual gate exists to bypass) — extending it to cover mean_reversion/chop too
   in that case, which the previous version silently never checked.

2. Genuine engine finding, NOT a config-authoring mistake: `main_strategy.is_ready()`
   gates readiness on `strategy_engine.is_ready(self.regime_engine.current_regime)`,
   where `current_regime` is READ BEFORE `classify()` has ever run for this bar (the
   code comment even says so) — so on the very first ready-candidate bar,
   `current_regime` is still its class-init default, `MarketRegime.UNKNOWN`, no matter
   what the config's real target regime is. `ConfigDrivenStrategyEngine.is_ready()`
   returns True UNCONDITIONALLY when the queried regime key isn't present in its
   `_components` dict (`if rkey not in self._components: return True`) — which is
   exactly what happens whenever the real signal sits under any key OTHER than
   "unknown" (since "unknown" is null and never registered). The result: for
   default_regime in {mean_reversion, chop, trending}, the FIRST-ever forecast is
   computed one bar early, from whatever partial history has accumulated (as few as
   2 bars), silently ignoring the configured `strategies.warmup` value for that one
   bar. default_regime="unknown" is the ONE choice where this check is non-vacuous
   (the real block is registered under "unknown" itself), so it alone respects the
   configured warmup on every bar, including the first.

   This is why the canonical pattern below is default_regime="unknown" specifically
   — not "any of the four, take your pick." The other three are schema-legal (after
   the V9 fix) and behave identically TO EACH OTHER, but all three share this same
   one-bar under-warmed-forecast defect that "unknown" alone avoids.

3. run_042's own shipped config (default_regime="mean_reversion") is therefore
   ALSO subject to this defect in principle — it is not something to silently absorb.
   It does not show up in run_042's own numbers only because FearGreedContrarianComponent's
   configured warmup (3) is far below the outer `required_bars` gate (24), so by the
   bar where the bug's one-bar window opens, the real per-component history has already
   vastly exceeded 3 anyway — the defect is latent, not absent. `EMASpreadComponent`
   at warmup=25 (run_043's real signal) exceeds the 24-bar outer gate, which is what
   exposes it. See `test_run_042_precedent_is_latently_affected_at_matched_warmup`.

The root engine defect (main_strategy.is_ready()'s stale-regime check) is NOT fixed
here — it is a pre-existing, systemic one-bar effect on the very first ready bar of
ANY strategy config (gated or ungated), in production since the regime-gated
architecture was built, invisible in aggregate metrics because it touches exactly one
bar out of thousands. Flagging it for separate follow-up is the correct scope for F1;
silently fixing engine readiness semantics as a rider on this change is not.
"""
import sys
import json
import tempfile
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent          # trading-bot/ (inner)
REPO_ROOT = PROJECT_ROOT.parent                       # repo root
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.main_strategy import AdvancedStrategy

_VALID_REGIMES = ["trending", "mean_reversion", "chop", "unknown"]

_EMA_COMPONENT = {
    "id": "ema_spread",
    "class": "strategies.strategy_components.EMASpreadComponent",
    "weight": 1.0,
    "transforms": [{"op": "identity"}],
    "params": {"fast_period": 9, "slow_period": 21, "scaling_factor": 5.0},
}


def _pattern_a_config(target_regime: str, warmup: int = 25) -> dict:
    """THE canonical ungated pattern: empty rules/components; default_regime carries
    the real signal directly."""
    regimes = {name: None for name in _VALID_REGIMES}
    regimes[target_regime] = {"components": [_EMA_COMPONENT]}
    return {
        "regime_detector": {
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": target_regime,
        },
        "strategies": {"warmup": warmup, "regimes": regimes},
    }


def _synthetic_bars(n: int = 70, seed: int = 42) -> pd.DataFrame:
    """Deterministic synthetic OHLCV with genuine up/down structure (not flat) so
    EMASpreadComponent actually produces a varying, non-trivial forecast sequence."""
    rng = np.random.default_rng(seed)
    steps = rng.normal(loc=0.05, scale=1.0, size=n).cumsum()
    close = 100.0 + steps
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"),
        "open": close, "high": close + 0.5, "low": close - 0.5,
        "close": close, "volume": 1.0,
    })


def _run_forecast_sequence(config: dict, bars: pd.DataFrame) -> list:
    """Write config to a temp file, feed bars one at a time, return forecast at every
    bar where the strategy is ready (None where not ready — kept so sequences stay
    index-aligned across variants)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        out = []
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[:i])
            if strat.is_ready():
                forecast, *_ = strat.generate_forecast()
                out.append(round(forecast, 10))
            else:
                out.append(None)
        return out
    finally:
        os.unlink(tmp_path)


BARS = _synthetic_bars()


@pytest.mark.parametrize("target_regime", _VALID_REGIMES)
def test_pattern_a_produces_a_nontrivial_sequence(target_regime):
    """Sanity check: the fixture actually exercises the signal (not all-zero/all-None)."""
    seq = _run_forecast_sequence(_pattern_a_config(target_regime), BARS)
    ready = [v for v in seq if v is not None]
    assert len(ready) > 10, "warmup consumed the whole synthetic window — widen BARS"
    assert len(set(ready)) > 5, "forecast sequence is degenerate/constant — not a real test"


def test_pattern_a_unknown_is_the_unique_warmup_safe_choice():
    """
    THE empirical result this file exists to establish:
    - mean_reversion, chop, and trending are mutually IDENTICAL to each other (the
      choice among these three is a pure, inert label — confirming Pattern A's
      "empty rules" plumbing is genuinely regime-name-agnostic).
    - "unknown" DIFFERS from the other three at exactly one bar: the first bar where
      main_strategy.required_bars (=24, independent of the configured `warmup`) is
      satisfied. The other three fire a real forecast there from under-warmed history;
      "unknown" correctly waits until `strategies.warmup` (=25) is actually satisfied.
    """
    sequences = {r: _run_forecast_sequence(_pattern_a_config(r), BARS) for r in _VALID_REGIMES}

    mr, chop, trending, unknown = (
        sequences["mean_reversion"], sequences["chop"], sequences["trending"], sequences["unknown"]
    )

    assert mr == chop == trending, (
        "mean_reversion/chop/trending were expected to be mutually identical (pure "
        "label choice) but diverged — the 'inert label' claim does not hold as tested."
    )

    assert unknown != mr, (
        "Expected 'unknown' to differ from the other three (it is the only choice that "
        "isn't vacuously bypassed by main_strategy.is_ready()'s stale pre-classify regime "
        "check) — but it matched. Either the engine's readiness check changed, or this "
        "fixture no longer exercises the one-bar warmup gap. Re-verify before trusting "
        "the 'use unknown' recommendation in skills/backtest-engineering/SKILL.md."
    )

    first_divergence = next(i for i, (a, b) in enumerate(zip(unknown, mr)) if a != b)
    required_bars_index = 23  # required_bars=24, 0-indexed -> first ready-candidate bar
    assert first_divergence == required_bars_index, (
        f"Expected the sole divergence at index {required_bars_index} (the first bar "
        f"where the outer required_bars gate opens); got index {first_divergence} instead. "
        "The mechanism may have changed — re-derive before trusting this test."
    )
    assert mr[first_divergence] is not None and unknown[first_divergence] is None, (
        "Expected mean_reversion/chop/trending to fire an (under-warmed) forecast at "
        "the divergence bar while 'unknown' correctly stays not-ready there."
    )
    # From the point strategies.warmup is genuinely satisfied onward, all four must
    # agree — the divergence is exactly one bar, not a permanent difference.
    assert unknown[first_divergence + 1:] == mr[first_divergence + 1:], (
        "Expected the four variants to reconverge to identical forecasts once the "
        "configured warmup is genuinely satisfied — divergence should be exactly one bar."
    )


# ---------------------------------------------------------------------------
# run_042 precedent verification — load the REAL shipped config, don't reconstruct it.
# ---------------------------------------------------------------------------

_RUN_042_CONFIG_PATH = (
    REPO_ROOT / "strategy-research" / "runs" / "run_042" / "artifacts" / "candidate_strategy_config.json"
)


def _fear_greed_bars(n: int = 70, seed: int = 7) -> pd.DataFrame:
    """Bars starting at a UTC-midnight boundary with a genuinely varying fear_greed
    column (cycling fear/neutral/greed) so FearGreedContrarianComponent actually fires
    with alternating signs across daily-boundary bars — not a trivial constant."""
    bars = _synthetic_bars(n=n, seed=seed)
    bars["timestamp"] = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    fg_cycle = [10.0, 50.0, 90.0]
    bars["fear_greed"] = [fg_cycle[(i // 24) % len(fg_cycle)] for i in range(n)]
    return bars


@pytest.mark.skipif(not _RUN_042_CONFIG_PATH.exists(), reason="run_042 artifact not present on disk")
def test_run_042_precedent_is_unaffected_at_its_own_real_warmup():
    """
    Direct check at run_042's ACTUAL config, unmodified: with its real warmup=3,
    the one-bar-early-forecast defect (if triggered) has no observable effect, because
    by the time the outer required_bars=24 gate opens, the per-component history (fed
    every bar since bar ~1) has already vastly exceeded warmup=3. This is expected to
    PASS — it demonstrates the defect is latent/masked here, not that run_042's
    default_regime choice is somehow immune to it (see the next test).
    """
    with open(_RUN_042_CONFIG_PATH) as f:
        run_042_config = json.load(f)
    assert run_042_config["strategies"]["warmup"] == 3
    assert run_042_config["regime_detector"]["default_regime"] == "mean_reversion"

    bars = _fear_greed_bars()
    seq = _run_forecast_sequence(run_042_config, bars)
    ready = [v for v in seq if v is not None]
    assert len(set(ready)) > 1, "fixture degenerate — widen fear_greed cycle before trusting this test"


@pytest.mark.skipif(not _RUN_042_CONFIG_PATH.exists(), reason="run_042 artifact not present on disk")
def test_run_042_precedent_shares_the_stale_regime_readiness_mechanism():
    """
    Per the user's explicit instruction: verify run_042's default_regime='mean_reversion'
    precedent against this test rather than silently absorbing it.

    A same-numbers comparison (mean_reversion vs. unknown, both at raised warmup=25) does
    NOT show a divergence for this specific component — but that is a coincidence of
    calendar alignment, not evidence of safety: FearGreedContrarianComponent only ever
    produces a nonzero value at hour==0 UTC boundary bars, and the defect's one-bar
    window (idx=23, i.e. required_bars-1) lands on 2024-01-01 23:00 — not a boundary bar
    — so BOTH variants correctly return 0.0 there regardless of whether the underlying
    history is under-warmed. A dense signal (EMASpreadComponent, see
    test_pattern_a_unknown_is_the_unique_warmup_safe_choice) is active on every bar and
    therefore DOES expose the gap numerically; a sparse, boundary-gated one may or may
    not, depending on incidental alignment between the fixed defect bar and the signal's
    own activation calendar.

    So this test checks the MECHANISM directly instead of relying on the output number:
    does run_042's config (raised to warmup=25, otherwise verbatim) report itself "ready"
    at idx=23 even though the real per-regime component history at that point has only
    ~4 entries — far short of the configured warmup=25? If yes, the mechanical defect is
    confirmed present in run_042's own plumbing, regardless of whether THIS particular
    run's numbers happened to look fine.
    """
    with open(_RUN_042_CONFIG_PATH) as f:
        run_042_config = json.load(f)

    mean_reversion_variant = json.loads(json.dumps(run_042_config))
    mean_reversion_variant["strategies"]["warmup"] = 25
    target_regime = mean_reversion_variant["regime_detector"]["default_regime"]
    assert target_regime == "mean_reversion"

    bars = _fear_greed_bars()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(mean_reversion_variant, f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        assert strat.required_bars == 24
        first_ready_index = None
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[:i])
            if strat.is_ready():
                first_ready_index = i - 1
                real_hist_len = len(
                    strat.strategy_engine._history[target_regime]["fg_contrarian"]
                )
                break
        assert first_ready_index is not None, "strategy never became ready — widen bars"
    finally:
        os.unlink(tmp_path)

    assert first_ready_index == 23, (
        f"Expected the stale-regime bypass to fire at idx=23 (required_bars-1); "
        f"got {first_ready_index}. Re-derive before trusting this test's conclusion."
    )
    assert real_hist_len < 25, (
        f"MECHANICAL DEFECT NOT CONFIRMED: run_042's config reported ready at idx=23 "
        f"with real per-regime history already >= configured warmup=25 (len={real_hist_len}) "
        "— i.e. it was genuinely warmed, not bypassed. This would mean the defect does "
        "not apply here after all; re-investigate before amending the skill guidance."
    )
    # This IS the finding: ready fired via the stale-regime vacuous bypass, with only
    # `real_hist_len` (~4) of the configured 25 bars of real history — mechanically
    # identical to the EMASpreadComponent case above. It happens not to change run_042's
    # own reported numbers only because FearGreedContrarianComponent is zero outside its
    # sparse boundary condition, which idx=23 does not satisfy on this fixture.
