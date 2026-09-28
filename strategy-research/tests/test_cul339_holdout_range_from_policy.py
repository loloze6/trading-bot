"""
CUL-339: `run_protocol.py --holdout` takes its range ONLY from
campaign_data_policy.yaml's holdout_range, and the walk-forward training guard
is never looser than it.

THE BUG
-------
Holdout mode read `protocol["holdout"]` -- with `end: null` meaning
`date.today()`. Several committed protocols carry a block starting a year
before the seal with an open end, which would have scored the validation year,
the whole sealed window and post-holdout data in one irreversible look. The
RUNBOOK told the operator to use the policy's range; nothing enforced it.

REVIEW FIXES (second round)
---------------------------
* every training window's start AND end is pre-flighted (strict YYYY-MM-DD,
  start <= end, end strictly before the bound) before out_dir / any backtest,
  as an explicit refusal (exit 3) -- never an `assert`, which `python -O`
  strips (the launcher's prefetch bound too);
* --holdout needs --hypothesis-id and refuses an id already in
  holdout_consumed_by, before any fetch;
* ONE strict parser (tools/holdout_policy.py) for every reader of the range;
* training validates only the policy START;
* the protocol generator refuses a disagreeing pre-registered holdout block.

HOW THESE TESTS STAY SAFE
-------------------------
run_backtest is replaced by a recorder in every test (no engine, no fetch, no
cache read), _RESULTS_ROOT and --out-dir point into tmp_path, and the policy is
a sandboxed file whose dates are computed here at runtime -- far from the real
seal. Tests that read the REAL policy read only that YAML (normal reading per
the policy's own rules) and never reach run_backtest. No test names a date
inside the sealed window.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import holdout_policy as hp  # noqa: E402
import run_protocol as rp  # noqa: E402
from protocol_refusal import (  # noqa: E402
    EXIT_NO_DATA_TOUCHED, stderr_declares_no_data_touched,
)

# Sandbox seal: computed, historical, nowhere near the real one.
_SANDBOX_START = date(2021, 3, 1)
_SANDBOX_END = _SANDBOX_START + timedelta(days=45)
S_START, S_END = _SANDBOX_START.isoformat(), _SANDBOX_END.isoformat()
HYP = "H-CUL339-TEST"


class _RecordingRunBacktest:
    """Records every call; writes the minimal metrics.json main() reads back."""

    def __init__(self, sandbox_dir: Path):
        self.calls: list[dict] = []
        self._dir = sandbox_dir

    def __call__(self, config_path, symbol, start, end, results_root, **kwargs):
        self.calls.append({"symbol": symbol, "start": start, "end": end, **kwargs})
        run_dir = self._dir / f"stub_run_{len(self.calls)}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(json.dumps({"core": {
            "trade_count": 1, "net_pnl": 0.0, "sharpe": 0.0, "win_rate": 0.5,
            "max_drawdown_pct": 0.0, "forecast_return_corr": None}}))
        return run_dir


def _write_policy(tmp_path: Path, holdout_range, consumed=()) -> Path:
    """A sandboxed copy of the real policy with holdout_range replaced (or
    removed when holdout_range is ...) and holdout_consumed_by replaced (or
    removed when consumed is ...)."""
    real = yaml.safe_load((ROOT / "config" / "campaign_data_policy.yaml").read_text(
        encoding="utf-8")) or {}
    if holdout_range is ...:
        real.pop("holdout_range", None)
    else:
        real["holdout_range"] = holdout_range
    if consumed is ...:
        real.pop("holdout_consumed_by", None)
    else:
        real["holdout_consumed_by"] = list(consumed)
    p = tmp_path / "campaign_data_policy.yaml"
    p.write_text(yaml.safe_dump(real, sort_keys=False), encoding="utf-8")
    return p


def _day(d: date, delta: int = 0) -> str:
    return (d + timedelta(days=delta)).isoformat()


@pytest.fixture
def run_main(monkeypatch, tmp_path):
    """rp.main() end to end with a sandboxed policy and a recording run_backtest.
    Returns (calls, out_dir, exit_code) -- exit_code None when main() returned."""
    def _run(*, holdout_block=..., windows=None, holdout=True,
             policy_range=(S_START, S_END), use_real_policy=False,
             hypothesis_id=HYP, consumed=()):
        stub = _RecordingRunBacktest(tmp_path / "sandbox_runs")
        monkeypatch.setattr(rp, "run_backtest", stub)
        monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
        if not use_real_policy:
            monkeypatch.setattr(rp, "_DATA_POLICY_PATH",
                                _write_policy(tmp_path, policy_range, consumed))

        protocol = {
            "symbols": ["BTCUSDT"],
            "windows": windows if windows is not None else [
                {"label": "w1", "test": {"start": "2019-01-01", "end": "2019-02-01"}}],
            "promotion": {"median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999,
                          "min_trade_count_gte": 0, "kill_median_sharpe_lt": -999999},
        }
        if holdout_block is not ...:
            protocol["holdout"] = holdout_block
        protocol_path = tmp_path / "protocol.json"
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"dummy": True}), encoding="utf-8")
        out_dir = tmp_path / "out"

        argv = ["run_protocol.py", str(config_path), str(protocol_path),
                "--out-dir", str(out_dir)]
        if holdout:
            argv += ["--holdout", "--i-understand"]
        if hypothesis_id is not None:
            argv += ["--hypothesis-id", hypothesis_id]
        monkeypatch.setattr(sys, "argv", argv)
        code = None
        try:
            rp.main()
        except SystemExit as exc:
            code = exc.code
        return stub.calls, out_dir, code
    return _run


def _assert_refused_untouched(calls, out_dir, code, capsys):
    assert code == EXIT_NO_DATA_TOUCHED
    assert stderr_declares_no_data_touched(capsys.readouterr().err)
    assert calls == [], "run_backtest must never be called on a refused run"
    assert not out_dir.exists(), "refusal must precede every side effect, out_dir included"


# ---------------------------------------------------------------------------
# --holdout: range from the policy only
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("block", [
    pytest.param({"start": _day(_SANDBOX_START, -365), "end": None}, id="validation-year-start-open-end"),
    pytest.param({"start": S_START, "end": None}, id="open-end"),
    pytest.param({"start": _day(_SANDBOX_START, -1), "end": S_END}, id="start-earlier"),
    pytest.param({"start": _day(_SANDBOX_START, 1), "end": S_END}, id="start-later"),
    pytest.param({"start": S_START, "end": _day(_SANDBOX_END, 1)}, id="end-later"),
    pytest.param({"start": S_START, "end": _day(_SANDBOX_END, -1)}, id="end-earlier"),
    pytest.param({"start": S_START}, id="end-missing"),
    pytest.param({}, id="empty-block"),
    pytest.param({"start": S_START + "T00:00:00", "end": S_END}, id="timestamp-not-day"),
    pytest.param([S_START, S_END], id="not-a-mapping"),
])
def test_disagreeing_protocol_block_refused_before_any_fetch(run_main, capsys, block):
    calls, out_dir, code = run_main(holdout_block=block)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_real_policy_refuses_the_committed_open_ended_block_shape(run_main, capsys):
    """The exact shape baseline_v1.json & co. carry -- a start one year before
    the REAL seal and `end: null` -- against the REAL policy: refused, and
    run_backtest (the only path to data) is never reached."""
    real_start = yaml.safe_load((ROOT / "config" / "campaign_data_policy.yaml").read_text(
        encoding="utf-8"))["holdout_range"][0]
    y = int(str(real_start)[:4])
    block = {"start": f"{y - 1:04d}-01-01", "end": None}
    calls, out_dir, code = run_main(holdout_block=block, use_real_policy=True)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_no_protocol_block_uses_policy_range(run_main):
    calls, out_dir, code = run_main()
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]
    payload = json.loads((out_dir / "holdout_result.json").read_text(encoding="utf-8"))
    assert payload["holdout_window"] == {"start": S_START, "end": S_END}


def test_null_protocol_block_is_treated_as_absent(run_main):
    calls, _, code = run_main(holdout_block=None)
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]


def test_agreeing_protocol_block_runs_on_policy_range(run_main):
    calls, _, code = run_main(holdout_block={"start": S_START, "end": S_END})
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]


@pytest.mark.parametrize("policy_range", [
    pytest.param([S_START, None], id="null-end"),
    pytest.param([S_START, ""], id="empty-end"),
    pytest.param([S_START, S_END + "+01:00"], id="tz-offset-end"),
    pytest.param([S_START], id="one-element"),
    pytest.param([None, S_END], id="null-start"),
    pytest.param([S_END, S_START], id="end-before-start"),
    pytest.param(None, id="null-range"),
    pytest.param(..., id="missing-key"),
])
def test_unusable_policy_range_refused(run_main, capsys, policy_range):
    # no protocol block: the policy is the only source, so it alone decides
    calls, out_dir, code = run_main(policy_range=policy_range)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_missing_policy_file_refused(run_main, monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(rp, "_DATA_POLICY_PATH", tmp_path / "nope" / "policy.yaml")
    calls, out_dir, code = run_main(use_real_policy=True)  # keep the patched path
    _assert_refused_untouched(calls, out_dir, code, capsys)


# ---------------------------------------------------------------------------
# --holdout: single use per hypothesis (holdout_consumed_by)
# ---------------------------------------------------------------------------

def test_consumed_hypothesis_refused_before_fetch(run_main, capsys, tmp_path):
    calls, out_dir, code = run_main(consumed=["H-OTHER", HYP])
    _assert_refused_untouched(calls, out_dir, code, capsys)
    policy = yaml.safe_load((tmp_path / "campaign_data_policy.yaml").read_text(encoding="utf-8"))
    assert policy["holdout_consumed_by"] == ["H-OTHER", HYP], "never modified here"


@pytest.mark.parametrize("hyp,consumed", [
    pytest.param(None, [], id="no-hypothesis-id"),
    pytest.param("", [], id="empty-hypothesis-id"),
    pytest.param(" " + HYP, [HYP], id="padded-id-of-a-consumed-hypothesis"),
    pytest.param(HYP, ..., id="consumed-key-missing"),
    pytest.param(HYP, [1], id="consumed-not-strings"),
])
def test_hypothesis_id_gate_refuses(run_main, capsys, hyp, consumed):
    calls, out_dir, code = run_main(hypothesis_id=hyp, consumed=consumed)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_unconsumed_hypothesis_runs_exact_match_only(run_main):
    calls, _, code = run_main(consumed=[HYP[:-1], HYP + "-2"])
    assert code is None and len(calls) == 1


def test_consumed_by_null_counts_as_none_consumed(run_main, monkeypatch, tmp_path):
    p = _write_policy(tmp_path, [S_START, S_END])
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    doc["holdout_consumed_by"] = None
    p.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(rp, "_DATA_POLICY_PATH", p)
    calls, _, code = run_main(use_real_policy=True)  # keep the patched path
    assert code is None and len(calls) == 1


# ---------------------------------------------------------------------------
# walk-forward training guard: min(protocol start, policy start)
# ---------------------------------------------------------------------------

def _wf(run_main, **kw):
    kw.setdefault("hypothesis_id", None)
    return run_main(holdout=False, **kw)


def test_training_guard_uses_policy_start_when_protocol_start_is_later(run_main):
    later = _day(_SANDBOX_START, 30)
    calls, _, code = _wf(run_main, holdout_block={"start": later, "end": None})
    assert code is None and calls
    assert all(c["holdout_start"] == S_START for c in calls)


def test_training_guard_keeps_stricter_protocol_start(run_main):
    earlier = _day(_SANDBOX_START, -30)
    calls, _, code = _wf(run_main, holdout_block={"start": earlier, "end": None})
    assert code is None and calls
    assert all(c["holdout_start"] == earlier for c in calls)


def test_training_guard_uses_policy_start_without_protocol_block(run_main):
    calls, _, code = _wf(run_main)
    assert code is None and calls
    assert all(c["holdout_start"] == S_START for c in calls)


def test_training_window_past_policy_start_refused_even_if_protocol_allows_it(run_main, capsys):
    """The block's start is AFTER the policy's, so the old guard (protocol
    start only) let this window through into the sealed range."""
    later = _day(_SANDBOX_START, 30)
    window = {"label": "leaky", "test": {"start": _day(_SANDBOX_START, -10),
                                         "end": _day(_SANDBOX_START, 5)}}
    calls, out_dir, code = _wf(run_main, holdout_block={"start": later, "end": None},
                               windows=[window])
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_training_window_ending_on_policy_start_refused(run_main, capsys):
    window = {"label": "edge", "test": {"start": _day(_SANDBOX_START, -10), "end": S_START}}
    calls, out_dir, code = _wf(run_main, windows=[window])
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_training_window_ending_the_day_before_policy_start_runs(run_main):
    window = {"label": "edge", "test": {"start": _day(_SANDBOX_START, -10),
                                        "end": _day(_SANDBOX_START, -1)}}
    calls, _, code = _wf(run_main, windows=[window])
    assert code is None and len(calls) == 1


_OK = {"label": "ok", "test": {"start": "2019-01-01", "end": "2019-02-01"}}


@pytest.mark.parametrize("bad_test", [
    # non-ISO ends: a US-style M/D/YYYY in the seal's own year, and tz-offset /
    # timestamp shapes of a day BEFORE the seal (a string compare passes them)
    pytest.param({"start": "2019-03-01", "end": f"1/15/{_SANDBOX_START.year}"}, id="us-style-end"),
    pytest.param({"start": "2019-03-01", "end": _day(_SANDBOX_START, -5) + "+01:00"},
                 id="tz-offset-end"),
    pytest.param({"start": "2019-03-01", "end": _day(_SANDBOX_START, -5) + "T23:00:00+00:00"},
                 id="timestamp-tz-end"),
    pytest.param({"start": "2019-03-01", "end": _day(_SANDBOX_START, -5) + "Z"}, id="z-suffix-end"),
    pytest.param({"start": "2019-03-01", "end": " " + _day(_SANDBOX_START, -5)}, id="padded-end"),
    pytest.param({"start": "3/1/2019", "end": "2019-04-01"}, id="us-style-start"),
    pytest.param({"start": "2019-03-01", "end": None}, id="null-end"),
    pytest.param({"start": "2019-03-01"}, id="missing-end"),
    pytest.param({"end": "2019-04-01"}, id="missing-start"),
    pytest.param({"start": 20190301, "end": "2019-04-01"}, id="int-start"),
    pytest.param({"start": "2019-04-01", "end": "2019-03-01"}, id="end-before-start"),
    # a window whose START is inside the seal
    pytest.param({"start": _day(_SANDBOX_START, 3), "end": _day(_SANDBOX_START, 10)},
                 id="start-inside-seal"),
    # wholly AFTER the seal: training never reads past its start
    pytest.param({"start": _day(_SANDBOX_END, 10), "end": _day(_SANDBOX_END, 20)},
                 id="after-seal"),
])
def test_every_window_is_preflighted_before_any_backtest(run_main, capsys, bad_test):
    """The bad window is SECOND: the old in-loop check let the first window
    (and every symbol before it) spend data before refusing."""
    windows = [_OK, {"label": "bad", "test": bad_test}]
    calls, out_dir, code = _wf(run_main, windows=windows)
    _assert_refused_untouched(calls, out_dir, code, capsys)


@pytest.mark.parametrize("windows", [
    pytest.param([], id="empty-list"),
    pytest.param([{"label": "no-test"}], id="no-test-block"),
    pytest.param(["2019-01-01"], id="not-a-mapping"),
])
def test_malformed_windows_refused_before_any_backtest(run_main, capsys, windows):
    calls, out_dir, code = _wf(run_main, windows=windows)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_preflight_still_refuses_under_python_O(tmp_path):
    """`python -O` strips `assert`; the training bound must not be one. Runs
    main() in a fresh `-O` interpreter with a sandboxed policy and a
    run_backtest that exits 99 if it is ever reached."""
    import subprocess
    import textwrap
    policy = _write_policy(tmp_path, [S_START, S_END])
    protocol = {"symbols": ["BTCUSDT"],
                "windows": [_OK, {"label": "edge", "test": {"start": _day(_SANDBOX_START, -3),
                                                            "end": S_START}}]}
    (tmp_path / "protocol.json").write_text(json.dumps(protocol), encoding="utf-8")
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    script = textwrap.dedent(f"""
        import sys
        if sys.flags.optimize < 1:
            sys.exit("not running under -O")
        sys.path.insert(0, {str(TOOLS_PATH)!r})
        import run_protocol as rp
        def _boom(*a, **k):
            print("RUN_BACKTEST_REACHED", file=sys.stderr)
            sys.exit(99)
        rp.run_backtest = _boom
        rp._DATA_POLICY_PATH = {str(policy)!r}
        rp._RESULTS_ROOT = {str(tmp_path / "results")!r}
        sys.argv = ["run_protocol.py", {str(tmp_path / "config.json")!r},
                    {str(tmp_path / "protocol.json")!r}, "--out-dir", {str(tmp_path / "out")!r}]
        rp.main()
    """)
    res = subprocess.run([sys.executable, "-O", "-c", script], capture_output=True, text=True,
                         timeout=300)
    assert res.returncode == EXIT_NO_DATA_TOUCHED, (res.returncode, res.stderr[-2000:])
    assert stderr_declares_no_data_touched(res.stderr)
    assert "RUN_BACKTEST_REACHED" not in res.stderr
    assert not (tmp_path / "out").exists()


def test_training_malformed_protocol_start_refused(run_main, capsys):
    calls, out_dir, code = _wf(run_main, holdout_block={"start": "soon", "end": None})
    _assert_refused_untouched(calls, out_dir, code, capsys)


@pytest.mark.parametrize("policy_end", [None, "", "later"], ids=["null", "empty", "garbage"])
def test_training_ignores_the_policy_end(run_main, policy_end):
    """Training validates only the policy START (it never reads past it), so
    an open or undecided end does not block a walk-forward run."""
    calls, _, code = _wf(run_main, policy_range=[S_START, policy_end])
    assert code is None and calls
    assert all(c["holdout_start"] == S_START for c in calls)


@pytest.mark.parametrize("policy_range", [
    pytest.param([None, S_END], id="null-start"),
    pytest.param([S_START + "T00:00:00", S_END], id="timestamp-start"),
    pytest.param([S_START], id="one-element"),
    pytest.param(..., id="missing-key"),
])
def test_training_unusable_policy_start_refused(run_main, capsys, policy_range):
    calls, out_dir, code = _wf(run_main, policy_range=policy_range)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_hypothesis_id_without_holdout_refused(run_main, capsys):
    calls, out_dir, code = _wf(run_main, hypothesis_id=HYP)
    _assert_refused_untouched(calls, out_dir, code, capsys)


# ---------------------------------------------------------------------------
# source hygiene
# ---------------------------------------------------------------------------

_WALL_CLOCK = {"today", "now", "utcnow", "time", "time_ns", "monotonic", "monotonic_ns",
               "perf_counter", "perf_counter_ns", "localtime", "gmtime", "ctime"}


def _wall_clock_calls(tree):
    import ast
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if name in _WALL_CLOCK:
                yield node


def test_no_wall_clock_in_range_code():
    """AST, not text (comments may describe the old `end: null` -> today bug).
    No range bound may be derived from the wall clock: holdout_policy.py has no
    wall-clock call at all, and run_protocol.py's only two are the run-id
    stamp (_protocol_run_id) and the holdout log's "utc" field -- neither
    feeds a date that reaches run_backtest."""
    import ast
    hp_tree = ast.parse((TOOLS_PATH / "holdout_policy.py").read_text(encoding="utf-8"))
    assert [n.lineno for n in _wall_clock_calls(hp_tree)] == []

    tree = ast.parse((TOOLS_PATH / "run_protocol.py").read_text(encoding="utf-8"))
    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}

    def _enclosing_function(node):
        while node in parent:
            node = parent[node]
            if isinstance(node, ast.FunctionDef):
                return node.name
        return None

    def _is_utc_log_value(node):
        # datetime.now(...).isoformat() as the value of a dict's "utc" key
        outer = parent.get(parent.get(node))
        d = parent.get(outer)
        return isinstance(d, ast.Dict) and any(
            isinstance(k, ast.Constant) and k.value == "utc" and v is outer
            for k, v in zip(d.keys, d.values))

    bad = [n.lineno for n in _wall_clock_calls(tree)
           if not (_enclosing_function(n) == "_protocol_run_id"
                   or (_enclosing_function(n) == "main" and _is_utc_log_value(n)))]
    assert bad == [], f"wall-clock call(s) outside the two allowed stamps: lines {bad}"


def test_no_assert_statements_in_run_protocol():
    """`python -O` strips asserts: no bound may be one (there are none left)."""
    import ast
    tree = ast.parse((TOOLS_PATH / "run_protocol.py").read_text(encoding="utf-8"))
    assert [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)] == []


def test_launcher_prefetch_bound_is_an_explicit_raise():
    """trading-bot/core/launcher.py's warmup-prefetch holdout bound was an
    `assert` (stripped by -O); it must be an explicit raise."""
    import ast
    src = (ROOT.parent / "trading-bot" / "core" / "launcher.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "run_backtest")
    asserts = [n for n in ast.walk(fn) if isinstance(n, ast.Assert)
               and "holdout" in ast.get_source_segment(src, n)]
    assert asserts == []
    raises = [n for n in ast.walk(fn) if isinstance(n, ast.If)
              and "holdout_start_dt" in ast.get_source_segment(src, n.test)
              and any(isinstance(b, ast.Raise) for b in n.body)]
    assert len(raises) == 1


# ---------------------------------------------------------------------------
# holdout_policy: the ONE strict parser
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("2020-02-29", "2020-02-29"),
    (date(2020, 2, 29), "2020-02-29"),
    ("2021-02-29", None),
    ("2020-02-29T00:00:00", None),
    ("2020-02-29+01:00", None),
    ("2020-02-29Z", None),
    ("2/29/2020", None),
    ("2020-2-9", None),
    (" 2020-02-29", None),
    ("2020-02-29\n", None),
    ("٢٠٢٠-٠٢-٢٩", None),  # Arabic-Indic digits
    (None, None),
    ("", None),
    (20200229, None),
    (True, None),
])
def test_iso_day(value, expected):
    assert hp.iso_day(value) == expected


def test_parse_holdout_range_and_start():
    assert hp.parse_holdout_range([S_START, S_END]) == (S_START, S_END)
    assert hp.parse_holdout_start([S_START, None]) == S_START
    for bad in ([S_START, None], [S_END, S_START], [S_START], None, (S_START, S_END, S_END),
                [S_START + " ", S_END]):
        with pytest.raises(hp.HoldoutPolicyError):
            hp.parse_holdout_range(bad)


def test_load_policy_denies_by_default(tmp_path):
    with pytest.raises(hp.HoldoutPolicyError):
        hp.load_policy(tmp_path / "missing.yaml")
    for text in ("holdout_range: [\n", "- a list\n", ""):
        p = tmp_path / "p.yaml"
        p.write_text(text, encoding="utf-8")
        with pytest.raises(hp.HoldoutPolicyError):
            hp.load_holdout_range(p)


@pytest.mark.parametrize("value,expected", [
    ([], frozenset()), (None, frozenset()), ("H-1", frozenset({"H-1"})),
    (["H-1", "H-2"], frozenset({"H-1", "H-2"})),
])
def test_consumed_ids(value, expected):
    assert hp.consumed_hypothesis_ids({"holdout_consumed_by": value}) == expected


@pytest.mark.parametrize("policy", [{}, {"holdout_consumed_by": [1]},
                                    {"holdout_consumed_by": [""]},
                                    {"holdout_consumed_by": {"H-1": True}}])
def test_consumed_ids_refused(policy):
    with pytest.raises(hp.HoldoutPolicyError):
        hp.consumed_hypothesis_ids(policy)


def test_real_policy_parses_strictly():
    """The committed policy passes the strict parser (read only, never printed)."""
    start, end = hp.load_holdout_range()
    assert start <= end
    assert isinstance(hp.consumed_hypothesis_ids(hp.load_policy()), frozenset)


# ---------------------------------------------------------------------------
# other callers of the shared parser
# ---------------------------------------------------------------------------

def test_composite_check_refuses_timestamp_window_now():
    """composite_cache used to cut a date to its first 10 characters; a
    timestamp or trailing text is now refused (stricter)."""
    import composite_cache as cc
    proto = {"windows": [{"label": "w", "test": {"start": "2019-01-01",
                                                  "end": "2019-02-01T00:00:00+05:00"}}]}
    with pytest.raises(cc.CompositeError):
        cc.check_protocol_outside_holdout(proto, (S_START, S_END))
    proto["windows"][0]["test"]["end"] = "2019-02-01"
    cc.check_protocol_outside_holdout(proto, (S_START, S_END))
    with pytest.raises(cc.CompositeError):
        cc.check_protocol_outside_holdout(proto, (S_START, None))


def _rpr():
    wf = str(ROOT / "workflow")
    if wf not in sys.path:
        sys.path.insert(0, wf)
    import run_phase1_research as rpr
    return rpr


def test_load_holdout_range_is_strict(tmp_path):
    rpr = _rpr()
    p = tmp_path / "policy.yaml"
    for hr in ([S_START, S_END + "T00:00:00"], [S_END, S_START], [S_START, "1/15/2021"]):
        p.write_text(yaml.safe_dump({"holdout_range": hr}), encoding="utf-8")
        with pytest.raises(rpr.HoldoutBoundaryBreach):
            rpr._load_holdout_range(p)
    p.write_text("holdout_range: [\n", encoding="utf-8")  # unparseable: was a YAMLError
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._load_holdout_range(p)
    p.write_text(yaml.safe_dump({"holdout_range": [S_START, S_END]}), encoding="utf-8")
    assert rpr._load_holdout_range(p) == (S_START, S_END)


def test_generator_refuses_a_disagreeing_holdout_override():
    """machine_constraints.protocol.holdout must equal the policy range (dates
    read from the sandboxed verbatim policy copy at runtime)."""
    rpr = _rpr()
    hs, he = rpr._load_holdout_range()
    policy_block = {"start": hs, "end": he}
    assert rpr._generated_protocol_holdout_block({}) == policy_block
    assert rpr._generated_protocol_holdout_block({"holdout": None}) == policy_block
    assert rpr._generated_protocol_holdout_block({"holdout": dict(policy_block)}) == policy_block
    shifted = (date.fromisoformat(he) + timedelta(days=1)).isoformat()
    earlier = (date.fromisoformat(hs) - timedelta(days=365)).isoformat()
    for bad in ({"start": hs, "end": None}, {"start": hs, "end": shifted},
                {"start": earlier, "end": he}, {"start": hs}, [hs, he], "policy",
                {"start": hs, "end": he, "note": "x"}):
        with pytest.raises(rpr.HoldoutBoundaryBreach):
            rpr._generated_protocol_holdout_block({"holdout": bad})
