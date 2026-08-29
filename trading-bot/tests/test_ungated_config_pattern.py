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

The root engine defect (main_strategy.is_ready()'s stale-regime check) was NOT fixed
as part of F1 — flagged for separate follow-up instead, since silently fixing engine
readiness semantics as a rider on an unrelated config-validation change was not the
correct scope. It was fixed separately as F7 (Notion "P8: First forecast computed one
bar early"): `AdvancedStrategy.is_ready()` now classifies the CURRENT bar before
checking `strategy_engine.is_ready(regime)`, instead of reading the previous bar's
(or, on the first ready-candidate bar, the class-init UNKNOWN default) `current_regime`.
`_classify_once()` memoizes the result per bar (invalidated in `update()`) so
`is_ready()` and `generate_forecast()` agree on one classification per bar rather than
running `classify()` twice, which would double-count its side effects (veto-bar streak
counters, `bars_in_current_regime`/`regime_change_count`).

The tests below were written to characterize the BUG and were updated, in the same
change that fixed it, to assert the FIXED behavior instead — see
`test_pattern_a_all_four_regime_labels_now_agree` and
`test_run_042_precedent_current_regime_is_fresh_when_ready_fires`.
"""

import sys
import json
import tempfile
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent  # trading-bot/ (inner)
REPO_ROOT = PROJECT_ROOT.parent  # repo root
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
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"),
            "open": close,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": 1.0,
        }
    )


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


def test_pattern_a_all_four_regime_labels_now_agree():
    """
    Post-F7-fix result (was test_pattern_a_unknown_is_the_unique_warmup_safe_choice,
    which asserted the BUG: "unknown" diverging from the other three at index 23 by
    being the only label not vacuously bypassed by the stale pre-classify regime
    check). Now that `is_ready()` classifies the current bar before checking
    strategy-engine readiness, ALL FOUR labels correctly wait for
    `strategies.warmup` (=25) regardless of which regime name carries the real
    signal — the choice of default_regime is once again a pure, inert label with no
    warmup-safety implication. Do not restore the old "prefer default_regime=unknown"
    guidance in workflow_artifacts/skills/backtest-engineering/SKILL.md on the basis
    of this test; that guidance was a workaround for the bug this fix removes.
    """
    sequences = {r: _run_forecast_sequence(_pattern_a_config(r), BARS) for r in _VALID_REGIMES}

    mr, chop, trending, unknown = (
        sequences["mean_reversion"],
        sequences["chop"],
        sequences["trending"],
        sequences["unknown"],
    )

    assert mr == chop == trending == unknown, (
        "Expected all four regime-name choices to produce an IDENTICAL forecast "
        "sequence now that is_ready() classifies the current bar before checking "
        "strategy-engine readiness. A divergence here means the F7 fix regressed, "
        "or one label is once again getting a vacuous readiness bypass."
    )

    ready = [v for v in unknown if v is not None]
    assert len(ready) > 10, "warmup consumed the whole synthetic window — widen BARS"
    first_ready_index = next(i for i, v in enumerate(unknown) if v is not None)
    # Measured, not derived: EMASpreadComponent's own get_required_periods() (driven
    # by slow_period=21) gates its readiness later than the outer required_bars=24
    # check, so first readiness now lands at index 40 for every regime label -- later
    # than the old (buggy) index 23, because index 23 was reached by vacuously
    # bypassing this component's real warmup rather than by satisfying it.
    assert first_ready_index == 40, (
        f"Expected first readiness at index 40 (measured); got index {first_ready_index}. "
        "Re-derive before trusting this test -- do not just restore 40 without checking "
        "why it moved."
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
def test_run_042_precedent_current_regime_is_fresh_when_ready_fires():
    """
    Was test_run_042_precedent_shares_the_stale_regime_readiness_mechanism, which
    asserted `real_hist_len < 25` as proof of the pre-fix vacuous bypass. Investigating
    the F7 fix surfaced that this config's EFFECTIVE `strategy_engine._warmup` is not
    the 25 this test raised `strategies.warmup` to -- it gets capped down to 2 by
    `min(configured_warmup, min_buf)`, where `min_buf` is the smallest per-component
    history-deque maxlen across ALL regimes in run_042's real config (some other
    regime's component declares a small per-component `lookback` override). So
    `real_hist_len < 25` was true both before AND after the fix -- 2 real bars of
    fg_contrarian history already satisfies the true warmup of 2 -- and that old
    assertion could not actually distinguish fixed from buggy behavior here. It
    happened to keep passing post-fix for the wrong reason.

    Rewritten to check the mechanism the fix actually changes: at the bar
    `is_ready()` first returns True, has `classify()` already run THIS bar, i.e. is
    `regime_engine.current_regime` the real classified regime rather than the
    class-init `UNKNOWN` default? Pre-fix this would read UNKNOWN (classify() only
    ran inside generate_forecast(), never yet called); post-fix it must read the
    real target regime, since is_ready() now classifies before checking.
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
                current_regime_at_ready = strat.regime_engine.current_regime
                break
        assert first_ready_index is not None, "strategy never became ready — widen bars"
    finally:
        os.unlink(tmp_path)

    assert first_ready_index == 23, (
        f"Expected first readiness at idx=23 (required_bars-1, unaffected by the F7 "
        f"fix since effective warmup here is 2, not 25); got {first_ready_index}. "
        "Re-derive before trusting this test."
    )
    assert current_regime_at_ready.value == target_regime, (
        f"F7 REGRESSION: at the bar is_ready() first returned True, "
        f"regime_engine.current_regime was {current_regime_at_ready.value!r}, not "
        f"{target_regime!r}. This means is_ready() is once again checking readiness "
        "against a stale (pre-classify) regime instead of classifying the current "
        "bar first."
    )
