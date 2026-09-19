"""
CUL-15 red-team regression: `_record_backtest_trial` must store the per-trade
expectancy MEAN in the trial ledger, not the whole {mean, se, t_stat, n} dict.

CUL-193 found that `per_trade_expectancy_bps` is a dict on the real
trade-diagnostics path (`run_protocol.py:619`, injected verbatim into
`protocol_result.yaml`'s `hypothesis_verdict.diagnostics`) and fixed
`_write_promotion_audit` to unwrap it. It missed the sibling call site:
`_record_backtest_trial` (`run_phase1_research.py`) was still doing a bare
`diag.get("per_trade_expectancy_bps")` and writing the result straight into
`campaign_state.trial_sharpes[].expectancy_bps`.

Why it matters even though nothing crashed: every other declaration of that
field types it as a number -- `deflate_sharpe.py:788` (`expectancy_bps: float |
None`), `_record_backtest_trial`'s own docstring, and `killed_run_gate.py`'s
fixtures (`"expectancy_bps": None`). `deflate_sharpe.compute_promotion_audit`
divides by exactly this quantity, and handed the dict it raises (verified by
execution):

    TypeError: unsupported operand type(s) for /: 'dict' and 'float'

The CLI path happens to source its expectancy from the verdict diagnostics
(where it unwraps correctly, `deflate_sharpe.py:809`) rather than from the
ledger row, so the defect is latent rather than live -- but the trial ledger is
what counts N for the deflated Sharpe, and storing a dict where a number belongs
corrupts the accounting record this project treats as load-bearing.

Source-level assertions, following `test_expectancy_promotion_lockstep.py`'s
established pattern: `run_phase1_research` cannot be imported in tests (it
constructs a `genai.Client()` at import time).
"""
import re
from pathlib import Path

WORKFLOW = (
    Path(__file__).parent.parent / "workflow" / "run_phase1_research.py"
)


def _record_backtest_trial_source() -> str:
    """The body of `_record_backtest_trial`, up to the next top-level def."""
    src = WORKFLOW.read_text(encoding="utf-8")
    start = src.index("def _record_backtest_trial(")
    rest = src[start:]
    nxt = re.search(r"\n(?=def )", rest)
    return rest[: nxt.start()] if nxt else rest


def test_record_backtest_trial_unwraps_the_expectancy_dict():
    """The mean must be extracted; the bare whole-dict read must be gone."""
    body = _record_backtest_trial_source()

    assert 'get("mean")' in body, (
        "_record_backtest_trial does not unwrap per_trade_expectancy_bps -- it "
        "is storing the whole {mean, se, t_stat, n} dict in the ledger's "
        "expectancy_bps field, which every other declaration types float|None"
    )
    assert "isinstance(_exp_block, dict)" in body, (
        "expected the same dict/scalar shape guard CUL-193 established at "
        "_write_promotion_audit -- the prescreen-stub path still writes a bare "
        "None, so both shapes must be handled"
    )

    bare_read = re.search(
        r"^\s*expectancy\s*=\s*diag\.get\(\s*[\"']per_trade_expectancy_bps[\"']\s*\)\s*$",
        body,
        re.MULTILINE,
    )
    assert bare_read is None, (
        "the unguarded whole-dict read is still present: "
        f"{bare_read.group(0).strip() if bare_read else ''}"
    )


def test_ledger_expectancy_is_declared_scalar_everywhere_else():
    """Pins the contract this fix restores, so a future change that re-widens
    the ledger field to a dict has to argue with an explicit assertion rather
    than quietly disagree with three other declarations."""
    deflate = (Path(__file__).parent.parent / "tools" / "deflate_sharpe.py").read_text(encoding="utf-8")
    assert "expectancy_bps:  float | None = None" in deflate or \
           "expectancy_bps: float | None = None" in deflate, (
        "deflate_sharpe no longer declares expectancy_bps as float|None -- if "
        "the ledger contract genuinely changed, this test and "
        "_record_backtest_trial must change together"
    )
