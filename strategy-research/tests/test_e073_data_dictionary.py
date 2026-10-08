"""
E-073 step 1 (P-CUL-81, D-081): the data dictionary, kept honest against the
code that writes each field, and given to the v3 readers behind the epic's one
flag, orchestrator.observable_backtest.enabled (off by default).

Sections:
  1. The dictionary parses: every row has a meaning, a unit, a code reference
     and a known "when known" value; every `KEY:line` reference names a real
     file and a line inside it.
  2. Field lists derived from the writers' code (no run artifact needed, CI has
     none): bars.csv's exact column patterns, and for every YAML/JSON file the
     key names its writer functions emit. Both directions: every field the code
     writes is in the dictionary, every dictionary entry is still written.
  3. The flag: off by default, registered everywhere, a hard dependency on
     reader_findings, non-bool refused.
  4. Flag off: the v3 handoff and prompt are byte-identical. Flag on: the
     dictionary is an extra required input, with one line telling the reader
     to use it, and the prompt carries its content.

No LLM, no backtest, no market data.
"""
import ast
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
REPO = SR_ROOT.parent
DICTIONARY = SR_ROOT / "docs" / "DATA_DICTIONARY.md"
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import RUN_ID, _set_orchestrator  # noqa: E402
from test_e068_5_readers_v3 import V3_ON, CLAIMS_ON, _run070_shaped  # noqa: E402

OB_ON = {**V3_ON, "observable_backtest": {"enabled": True}}
OB_OFF = {**V3_ON, "observable_backtest": {"enabled": False}}
WHEN = {"close", "fill", "exit", "after", "run", "end", "meta"}

TB = "trading-bot/core/trading_bot.py"
BT = "trading-bot/core/backtester.py"
PI = "trading-bot/execution/portfolio_info.py"
EH = "trading-bot/execution/execution_handler.py"
RM = "trading-bot/risk/risk_manager.py"
RG = "trading-bot/risk/portfolio_risk_gate.py"
SB = "trading-bot/strategies/strategy_base.py"
MS = "trading-bot/strategies/main_strategy.py"
SE = "trading-bot/strategies/strategy_engine.py"
DM = "trading-bot/data/data_manager.py"
FR = "trading-bot/data/feed_registry.py"
RA = "trading-bot/reporting/run_artifact.py"
SS = "trading-bot/performance/signal_statistics.py"
RP = "strategy-research/tools/run_protocol.py"
BR = "strategy-research/tools/build_reports.py"
VE = "strategy-research/tools/verdict_criteria_evaluator.py"
RF = "strategy-research/tools/reader_findings.py"
CF = "strategy-research/tools/claim_findings.py"
CM = "strategy-research/tools/claim_measure.py"
NB = "strategy-research/tools/nearest_build.py"
P1 = "strategy-research/workflow/run_phase1_research.py"


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# Parsing the dictionary
# ---------------------------------------------------------------------------

_SECTION_RE = re.compile(r"<!-- data-dictionary: (?P<name>\S+) -->\n(?P<body>.*?)"
                         r"<!-- /data-dictionary -->", re.S)
_SOURCES_RE = re.compile(r"<!-- data-dictionary-sources -->\n(?P<body>.*?)"
                         r"<!-- /data-dictionary-sources -->", re.S)
_ROW_RE = re.compile(r"^\| `(?P<field>[^`]+)` \|(?P<rest>.*)\|\s*$", re.M)
_REF_RE = re.compile(r"`(?P<key>[A-Z][A-Z0-9]):(?P<line>\d+)`")


def _text(path: Path = DICTIONARY) -> str:
    return path.read_text(encoding="utf-8")


def _sections(text: str) -> dict:
    """{section: [(field, [meaning, unit, code, when])]}"""
    out = {}
    for m in _SECTION_RE.finditer(text):
        rows = []
        for r in _ROW_RE.finditer(m.group("body")):
            cells = [c.strip() for c in r.group("rest").split(" | ")]
            rows.append((r.group("field"), cells))
        out[m.group("name")] = rows
    return out


def _sources(text: str) -> dict:
    body = _SOURCES_RE.search(text).group("body")
    return dict(re.findall(r"^\| `([A-Z][A-Z0-9])` \| `([^`]+)` \|", body, re.M))


def _path_of(field: str) -> str:
    """`profitability: slices.overall.source` -> the path after the report prefix."""
    return field.split(": ", 1)[1] if ": " in field else field


def _literal_segments(fields) -> set:
    """Every literal key name in the dictionary's field paths (placeholders and
    list markers left out)."""
    out = set()
    for f in fields:
        for seg in _path_of(f).split("."):
            seg = seg.replace("[]", "")
            if seg and not seg.startswith("<"):
                out.add(seg)
    return out


# ---------------------------------------------------------------------------
# Reading the writers' code (AST, no import of the engine)
# ---------------------------------------------------------------------------

_TREES: dict = {}


def _tree(rel: str) -> ast.Module:
    if rel not in _TREES:
        _TREES[rel] = ast.parse((REPO / rel).read_text(encoding="utf-8"))
    return _TREES[rel]


def _func(rel: str, name: str):
    """The one function or method `name` ("Class.method" to pick a class)."""
    cls, _, meth = name.rpartition(".")
    scopes = [_tree(rel)]
    if cls:
        scopes = [n for n in ast.walk(_tree(rel)) if isinstance(n, ast.ClassDef) and n.name == cls]
    found = [n for s in scopes for n in ast.walk(s)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == meth]
    assert len(found) == 1, f"{rel}: expected one {name}, found {len(found)}"
    return found[0]


def _const_str(node) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _dict_keys(node, nested: bool = True) -> set:
    """String keys of a dict literal (and of dict literals nested in it)."""
    out = set()
    nodes = ast.walk(node) if nested else [node]
    for n in nodes:
        if isinstance(n, ast.Dict):
            out |= {k for k in map(_const_str, n.keys) if k is not None}
    return out


def _subscript_assign_keys(node) -> set:
    """`x["key"] = ...` (also `x[a]["key"] = ...`) anywhere under node."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, (ast.Assign, ast.AugAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                if isinstance(t, ast.Subscript) and _const_str(t.slice) is not None:
                    out.add(t.slice.value)
    return out


def _module_constant(rel: str, name: str):
    for n in _tree(rel).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name
                                             for t in n.targets):
            return n.value
    raise AssertionError(f"{rel}: no module constant {name}")


def _comprehension_keys(rel: str, node) -> set:
    """`{k: x[k] for k in ("a", "b")}` or `for k in _MODULE_TUPLE`: the copied keys."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.comprehension):
            it = n.iter
            if isinstance(it, ast.Name):
                try:
                    it = _module_constant(rel, it.id)
                except AssertionError:
                    continue
            if isinstance(it, (ast.Tuple, ast.List)):
                out |= {v for v in map(_const_str, it.elts) if v is not None}
    return out


def _keys(rel: str, *funcs: str) -> set:
    """Every key a writer function emits: dict-literal keys, subscript
    assignments and comprehension-copied keys."""
    out = set()
    for name in funcs:
        f = _func(rel, name)
        out |= _dict_keys(f) | _subscript_assign_keys(f) | _comprehension_keys(rel, f)
    return out


def _assigned_dict(func, var: str):
    found = [n.value for n in ast.walk(func) if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == var for t in n.targets)
             and isinstance(n.value, ast.Dict)]
    assert found, f"{func.name}: no dict literal assigned to {var}"
    return found[0]


def _returned_dicts(func) -> list:
    """Dict literals returned by func: `return {...}` or inside `return (.., {...})`."""
    out = []
    for n in ast.walk(func):
        if isinstance(n, ast.Return) and n.value is not None:
            vals = n.value.elts if isinstance(n.value, ast.Tuple) else [n.value]
            out += [v for v in vals if isinstance(v, ast.Dict)]
    return out


# ---------------------------------------------------------------------------
# The code-derived field lists
# ---------------------------------------------------------------------------

def bars_csv_columns() -> set:
    """The exact column patterns bars.csv can carry, from the writers: the
    record_state keywords (core/trading_bot.py), the bar row (OHLCV + feeds),
    StrategyOutput, its debug_info and the nested debug dicts, each flattened
    the way portfolio_info.flatten_dict_columns does (a dict column becomes
    dotted columns; a dict column empty on every row stays as its own column)."""
    recorded = set()
    spreads = 0
    for n in ast.walk(_tree(TB)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "record_state":
            recorded |= {kw.arg for kw in n.keywords if kw.arg}
            spreads += sum(1 for kw in n.keywords if kw.arg is None)
    assert spreads == 1, "the per-bar record_state call spreads **risk_extras exactly once"
    recorded -= {"data", "signal", "replace_if_same_bar"}
    nested = {"balances", "postRebalance_balances", "debug_approve_allocation_change",
              "debug_execute_portfolio_rebalance"}
    assert nested <= recorded
    cols = recorded - nested

    # the bar row: OHLCV (CandleBuilder) + the aux feed columns
    cols |= _dict_keys(_func(DM, "get_candle_history"))
    cols |= _dict_keys(_module_constant(FR, "FEED_REGISTRY"), nested=False)
    assert _module_constant(FR, "WHALE_FOOTPRINT_FEEDS").elts, "reserved feeds exist"
    cols.add("<reserved feed>")
    # backtester's copy of total_portfolio_value
    assert "portfolio_value" in _subscript_assign_keys(_tree(BT))
    cols.add("portfolio_value")

    # StrategyOutput's fields; debug_info is always a non-empty dict (flattened)
    so = [n for n in ast.walk(_tree(SB)) if isinstance(n, ast.ClassDef)
          and n.name == "StrategyOutput"][0]
    fields = {n.target.id for n in so.body if isinstance(n, ast.AnnAssign)}
    assert "debug_info" in fields
    cols |= fields - {"debug_info"}
    gen = _func(MS, "AdvancedStrategy.generate_forecast")
    debug_keys = _dict_keys(_assigned_dict(gen, "debug_info"), nested=False)
    assert {"regime_scores", "components"} <= debug_keys
    cols |= {f"debug_info.{k}" for k in debug_keys - {"regime_scores", "components"}}
    for call in ast.walk(_func(SB, "generate_signals")):  # NOT_READY / ERROR outputs
        if isinstance(call, ast.Call):
            for kw in call.keywords:
                if kw.arg == "debug_info" and isinstance(kw.value, ast.Dict):
                    cols |= {f"debug_info.{k}" for k in _dict_keys(kw.value)}
    cols |= {"debug_info.regime_scores", "debug_info.regime_scores.<regime>",
             "debug_info.components"}
    for name in ("forecast", "_forecast_blocks"):
        f = _func(SE, name)
        for n in ast.walk(f):  # debug[cid] = {...}: one dict per component
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) \
                    and isinstance(n.targets[0], ast.Subscript):
                cols |= {f"debug_info.components.<component>.{k}" for k in _dict_keys(n.value)}
        for d in _returned_dicts(f):  # (0.0, {"not_ready_...": id})
            cols |= {f"debug_info.components.{k}" for k in _dict_keys(d)}

    # balances: {asset: {free, locked}}
    bal = _dict_keys(_returned_dicts(_func(PI, "_default_balance"))[0])
    inner = bal - {"USDT"}
    assert inner == {"free", "locked"}, inner
    cols |= {f"{b}.<asset>.{k}" for b in ("balances", "postRebalance_balances") for k in inner}

    # the risk manager's debug dict and its controls
    approve = _func(RM, "approve_allocation_change")
    top = _dict_keys(_assigned_dict(approve, "debug"), nested=False)
    assert "controls" in top
    passed = set()
    for n in ast.walk(approve):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict):
            passed |= _dict_keys(n.value) - top
    controls = {n.name[len("_ctrl_"):] for n in ast.walk(_tree(RM))
                if isinstance(n, ast.FunctionDef) and n.name.startswith("_ctrl_")}
    cols.add("debug_approve_allocation_change")
    cols |= {f"debug_approve_allocation_change.{k}" for k in top - {"controls"}}
    cols |= {f"debug_approve_allocation_change.controls.{c}.{p}" for c in controls for p in passed}

    # the (mock) execution handler's order dicts
    order = set()
    for name in ("MockExecutionHandler.open_long_position",
                 "MockExecutionHandler.open_short_position",
                 "MockExecutionHandler.close_position"):
        for d in _returned_dicts(_func(EH, name)):
            order |= _dict_keys(d)
    cols.add("debug_execute_portfolio_rebalance")
    cols |= {f"debug_execute_portfolio_rebalance.{k}" for k in order}

    # the portfolio risk gate's extras (**risk_extras)
    apply = _func(RG, "apply")
    cols |= _dict_keys(_assigned_dict(apply, "extras")) | _subscript_assign_keys(apply)
    return cols


def _report_keys() -> set:
    keys = _keys(BR, "_unavailable", "_wrap", "_aggregate_records",
                 "build_profitability_report", "build_trade_efficiency_report",
                 "build_forecast_power_report", "_compute_hindsight_lag",
                 "build_regime_power_report", "build_component_attribution_report",
                 "build_reports")
    keys |= _dict_keys(_module_constant(BR, "FORECAST_POWER_STATISTIC_LABELS"), nested=False)
    # build_reports' in-memory {category: report} map: file names, not fields
    return keys - {"profitability", "forecast_power"}


def _grid_keys() -> set:
    keys = _keys(VE, "_evaluate_grid_cell_for_symbol", "_reduce_sign_consistent_by_era",
                 "_evaluate_residual_ic_cell", "_evaluate_profit_bars_cell",
                 "_evaluate_grid_cell", "evaluate_grid")
    # spec_errors rows (printed inside `reason`, not keys) and a keyword dict
    keys -= {"criterion_id", "variant_id", "single_era_inconclusive"}
    for n in ast.walk(_tree(P1)):  # the orchestrator stamps the grid it saves
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) \
                        and t.value.id == "_grid_result" and _const_str(t.slice):
                    keys.add(t.slice.value)
    return keys


def code_fields() -> dict:
    """{dictionary section: the key names (or, for bars.csv, the column
    patterns) its writers emit}."""
    build_core = _func(RA, "build_core")
    return {
        "bars.csv": bars_csv_columns(),
        "trade_diagnostics.json": (
            _keys(RP, "_compute_trade_records_for_window", "_aggregate_trade_diagnostics",
                  "_aggregate_fee_reduction_diagnostics", "_compute_cost_basis")
            | _dict_keys(_assigned_dict(_func(RP, "main"), "td_payload"), nested=False)),
        "core": (
            set().union(*(_dict_keys(d) for d in _returned_dicts(build_core)))
            | _dict_keys(_assigned_dict(build_core, "post_backtest_cost_check_real"))
            | set().union(*(_dict_keys(d) for d in _returned_dicts(_func(SS, "cost_check"))))
            | {k for n in ast.walk(_func(RA, "write_metrics_json")) if isinstance(n, ast.Dict)
               for key, v in zip(n.keys, n.values) if _const_str(key) == "core"
               for k in _dict_keys(v, nested=False)}),
        "per_regime": _keys(RA, "build_per_regime"),
        # dict literal only: its df["forward_return"] is a work column, not a field
        "regime_validity": _dict_keys(_func(RA, "build_regime_validity")),
        "diagnostics": _keys(RP, "_build_diagnostics"),
        "reports": _report_keys(),
        "grid_evaluation.yaml": _grid_keys(),
        "claim_result_digest.yaml": (
            _keys(RF, "claim_result_digest", "_variant_digest", "variant_patches_digest")
            | _keys(CF, "_compact_test") | _keys(NB, "approximation_block")),
        "claim_measurement.yaml": _keys(CM, "run_doc", "error_doc"),
    }


# ---------------------------------------------------------------------------
# 1. The dictionary parses
# ---------------------------------------------------------------------------

def test_every_section_is_present_and_every_row_is_complete():
    secs = _sections(_text())
    assert set(secs) == set(code_fields()), sorted(set(secs) ^ set(code_fields()))
    for name, rows in secs.items():
        assert rows, f"{name}: no rows"
        fields = [f for f, _ in rows]
        dups = sorted({f for f in fields if fields.count(f) > 1})
        assert not dups, f"{name}: duplicate rows {dups}"
        for field, cells in rows:
            assert len(cells) == 4 and all(cells), f"{name} `{field}`: {cells}"
            meaning, unit, code, when = cells
            assert when in WHEN, f"{name} `{field}`: when known {when!r} not in {sorted(WHEN)}"
            assert _REF_RE.search(code), f"{name} `{field}`: no code reference in {code!r}"


def test_every_code_reference_resolves():
    text = _text()
    sources = _sources(text)
    refs = list(_REF_RE.finditer(text))
    assert len(refs) > 300
    for m in refs:
        key, line = m.group("key"), int(m.group("line"))
        assert key in sources, f"unknown source key {key} ({m.group(0)})"
        path = REPO / sources[key]
        assert path.exists(), f"{key}: {sources[key]} does not exist"
        n_lines = len(path.read_text(encoding="utf-8").splitlines())
        assert 1 <= line <= n_lines, f"{m.group(0)}: {sources[key]} has {n_lines} lines"


def test_the_dictionary_has_no_holdout_dates():
    """The sealed holdout's dates never appear in a file a reader gets."""
    assert not re.search(r"2026-0[1-6]", _text())


# ---------------------------------------------------------------------------
# 2. Kept honest against the writers
# ---------------------------------------------------------------------------

def test_bars_csv_columns_match_the_code_exactly():
    doc = {f for f, _ in _sections(_text())["bars.csv"]}
    code = code_fields()["bars.csv"]
    assert not code - doc, f"bars.csv columns written by the code, missing here: {sorted(code - doc)}"
    assert not doc - code, f"bars.csv entries no longer written by the code: {sorted(doc - code)}"


@pytest.mark.parametrize("section", [s for s in (
    "trade_diagnostics.json", "core", "per_regime", "regime_validity", "diagnostics",
    "reports", "grid_evaluation.yaml", "claim_result_digest.yaml", "claim_measurement.yaml")])
def test_every_written_key_is_documented_and_no_entry_is_stale(section):
    doc = _literal_segments(f for f, _ in _sections(_text())[section])
    code = code_fields()[section]
    assert code, f"{section}: the code-derived key list is empty"
    assert not code - doc, f"{section}: keys written by the code, missing here: {sorted(code - doc)}"
    assert not doc - code, f"{section}: entries no longer written by the code: {sorted(doc - code)}"


def test_the_derivation_is_not_vacuous():
    """The derived lists are the real ones: known fields of each file are in
    them, and a dictionary without a row is caught."""
    code = code_fields()
    assert {"forecast", "allocation_change", "debug_info.components.<component>.post_pipeline_value",
            "debug_approve_allocation_change.controls.min_allocation_change.passed",
            "succcess_execute_portfolio_rebalance", "fear_greed"} <= code["bars.csv"]
    assert {"entry_efficiency", "exit_reason", "cost_paid", "boundary_recross_rate"} \
        <= code["trade_diagnostics.json"]
    assert {"forecast_return_corr", "sharpe_annualization", "basis"} <= code["core"]
    assert {"hindsight_lag", "components_discovered", "prescreen_pooled_ic"} <= code["reports"]
    assert {"era_medians", "evaluated_at", "fully_explained"} <= code["grid_evaluation.yaml"]
    assert {"statistic_label", "selector", "clause"} <= code["claim_result_digest.yaml"]
    assert "n_tests_no_events" in code["claim_measurement.yaml"]
    text = _text()
    row = "| `trades[].mae` |"
    assert text.count(row) == 1
    cut = "\n".join(ln for ln in text.splitlines() if not ln.startswith(row))
    assert "mae" not in _literal_segments(f for f, _ in _sections(cut)["trade_diagnostics.json"])


# ---------------------------------------------------------------------------
# 3. The flag
# ---------------------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(V3_ON)
    assert rpr._observable_backtest_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(
        encoding="utf-8"))
    assert shipped["orchestrator"]["observable_backtest"]["enabled"] is False
    _set_orchestrator(OB_ON)
    assert rpr._observable_backtest_enabled() is True


def test_flag_on_without_reader_findings_raises():
    _set_orchestrator({**CLAIMS_ON, "observable_backtest": {"enabled": True}})
    with pytest.raises(ValueError, match="reader_findings.enabled=true"):
        rpr._observable_backtest_enabled()


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**V3_ON, "observable_backtest": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._observable_backtest_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(
        encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "observable_backtest"]
    assert entry["config_key"] == "orchestrator.observable_backtest.enabled"
    assert entry["reader"] == "run_phase1_research._observable_backtest_enabled"
    assert entry["state"] == "off_incomplete" and entry["blocked_on"]
    assert camp._flag_readers()["observable_backtest"] is rpr._observable_backtest_enabled
    import test_e061_end_to_end_wiring as wiring
    assert wiring.TARGET_FLAGS["observable_backtest"] is False


# ---------------------------------------------------------------------------
# 4. The readers' handoff and prompt
# ---------------------------------------------------------------------------

def _seed_dictionary() -> None:
    dst = rpr.ROOT / "docs" / "DATA_DICTIONARY.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DICTIONARY, dst)


def _prompt(cat: str, handoff: dict, run_dir: Path) -> str:
    return rpr._build_stage_prompt("specialist_readers", handoff, run_dir,
                                   skill_file_name=rpr._reader_skill_dir(cat))


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_off_handoff_and_prompt_are_byte_identical(cat, monkeypatch):
    run_dir = _run070_shaped(monkeypatch)  # reader_findings on, the key absent
    _seed_dictionary()
    absent = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert absent == rpr._reader_handoff_v3(cat, RUN_ID, 0, run_dir)
    prompt_absent = _prompt(cat, absent, run_dir)
    _set_orchestrator(OB_OFF)  # the key present, false
    off = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert off == absent
    assert _prompt(cat, off, run_dir) == prompt_absent
    assert "DATA_DICTIONARY" not in prompt_absent


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_on_adds_the_dictionary_and_one_line(cat, monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    _seed_dictionary()
    off = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    _set_orchestrator(OB_ON)
    on = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert on["required_inputs"][:-1] == off["required_inputs"]
    assert on["required_inputs"][-1]["path"] == rpr.DATA_DICTIONARY_DOC
    assert on["optional_inputs"] == off["optional_inputs"]
    assert on["objective"] == off["objective"] + " " + rpr.DATA_DICTIONARY_LINE
    assert on["injected_context"] == {**off["injected_context"],
                                      "data_dictionary": rpr.DATA_DICTIONARY_LINE}
    assert {k: v for k, v in on.items() if k not in ("required_inputs", "objective",
                                                     "injected_context")} \
        == {k: v for k, v in off.items() if k not in ("required_inputs", "objective",
                                                      "injected_context")}
    prompt = _prompt(cat, on, run_dir)
    assert f"--- CONTENT OF {rpr.DATA_DICTIONARY_DOC} ---" in prompt
    assert "## 1. bars.csv (one per window and variant)" in prompt
    assert yaml.dump(on, sort_keys=False) in prompt  # the handoff, line included


def test_flag_on_does_not_touch_the_v2_readers(monkeypatch):
    """Without reader_findings the v2 handoff is built and the flag is never
    read there (the launch pre-flight refuses that combination)."""
    _set_orchestrator({**CLAIMS_ON})
    monkeypatch.chdir(SR_ROOT)
    from test_e046a_slice5b_ii_b_readers_stage import _seed_run
    run_dir = _seed_run()
    v2 = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
    _set_orchestrator({**CLAIMS_ON, "observable_backtest": {"enabled": True}})
    assert rpr._reader_handoff("profitability", RUN_ID, 0, run_dir) == v2
