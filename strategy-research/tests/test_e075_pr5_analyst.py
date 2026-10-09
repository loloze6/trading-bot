"""E-075 PR-5 (CUL-423, D-092): the analyst's wiring and skill, under
orchestrator.analyst.enabled (off by default).

No API key: the SDK `query` is stubbed. The stub calls the REAL tool handlers (so the real
query log is written) and the REAL PreToolUse hook, then returns a canned answer.

Pins:
  1. the options: the analyst variant of _stage_agent_options on the same closed-book base,
     read off the installed SDK's CLI builder; flag-off options unchanged;
  2. the deny hook refuses every tool but the six;
  3. a stubbed session writes a reading in the reader-proposal shape that decide-next picks
     and turns into a fold-B child brief;
  4. code's checks of the answer (citations, the test was run, why_query, sealed dates,
     no claim, the score) and the retry then `skipped`;
  5. the stage: the two lenses replace the readers, the other three categories are
     code-skipped; flag off the readers run as before;
  6. the prompt carries the skill, the lens, the memory view and no sealed date.
"""
from __future__ import annotations

import asyncio
import dataclasses
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import claim_card as cc  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
from claude_agent_sdk import AssistantMessage, SystemMessage, TextBlock  # noqa: E402
from claude_agent_sdk._internal.transport.subprocess_cli import SubprocessCLITransport  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402  (a synthetic run with bars and trades)

# the real flag reader, kept before the autouse fixture replaces the attribute
_REAL_ANALYST_ENABLED = rpr._analyst_enabled
RUN_ID = "run_074"
LONG = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _flags(monkeypatch):
    """Analyst on (with folds), score provenance off; nothing reads the real config."""
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


@pytest.fixture()
def run(tmp_path, monkeypatch):
    root = tmp_path / "root"
    run_dir = q4.make_run(root / "runs" / RUN_ID)
    arts = run_dir / "artifacts"
    (arts / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": {"protocol": {"fold": "A"}}}), encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    monkeypatch.setattr(rpr, "ROOT", root)
    monkeypatch.setattr(rpr, "_load_holdout_range", lambda *a: (q4.HOLDOUT, None))
    monkeypatch.setattr(asm, "SR_ROOT", SR_ROOT)
    return run_dir


def _engine_on(run_dir, lens):
    return rpr._analyst_queries_module().QueryEngine(
        run_dir, log_path=run_dir / asm.log_rel(lens), holdout_start=q4.HOLDOUT)


class StubSession:
    """A fake `query`: calls the real hook and the real tool handlers, then answers.
    `script(tools_by_name) -> answer text` runs the tool calls it wants."""

    def __init__(self, script, init_tools=asm.ALLOWED_TOOLS):
        self.script = script
        self.options = []
        self.init_tools = init_tools

    async def query(self, prompt, options):
        self.options.append(options)
        self.prompt = prompt
        server = options.mcp_servers[asm.SERVER_NAME]
        hook = options.hooks["PreToolUse"][0].hooks[0]
        tools = {t.name: t for t in self._tools}

        async def call(name, args):
            full = f"mcp__{asm.SERVER_NAME}__{name}"
            decision = await hook({"tool_name": full, "tool_input": args}, "id", None)
            assert decision == {}, decision
            out = await tools[name].handler(args)
            return json.loads(out["content"][0]["text"])
        if self.init_tools is not None:
            yield SystemMessage(subtype="init", data={"tools": list(self.init_tools)})
        text = await self.script(call)
        assert server["type"] == "sdk"
        yield AssistantMessage(content=[TextBlock(text=text)], model="claude-haiku-4-5")
        yield type("R", (), {"total_cost_usd": 0.01, "num_turns": 3, "usage": {},
                             "subtype": "success"})()


def _install(monkeypatch, script, **kw):
    stub = StubSession(script, **kw)
    real = rpr._analyst_tools

    def capture(engine):
        stub._tools = real(engine)
        return stub._tools
    monkeypatch.setattr(rpr, "_analyst_tools", capture)
    monkeypatch.setattr(rpr, "query", stub.query)
    return stub


def _cite(qid, result, path):
    node = result
    for p in path.split("."):
        node = node[p]
    return f"{qid}:{path}={node}"


async def _good_claim(call, *, why=True, cite_bad=False, extra=None):
    ce = await call("conditional_effect", {"condition": LONG})
    ts = await call("trade_slice", {"filter": [], "agg": [{"field": "trade_net_return",
                                                            "stat": "mean"}],
                                    "by": "direction"}) if why else None
    test = ce["result"]["test"]
    cite = _cite(ce["query_id"], ce["result"], "horizons.trade.effect")
    if cite_bad:
        cite = cite.rsplit("=", 1)[0] + "=999"
    answer = {"outcome": "claim",
              "claim": {"statement": "Long lots of this strategy earn more than its short lots.",
                        "kind": "execution_behaviour", "tests": [test],
                        "pass_if": "long lots above the others on the unseen fold",
                        "fail_if": "not above", "rationale": "the longs ride the drift"},
              "why_query": ts["query_id"] if why else ce["query_id"],
              "evidence": [cite], "vehicle": [], "combines_as": "execution_rule"}
    answer.update(extra or {})
    return "Here is my claim.\n```yaml\n" + yaml.safe_dump(answer, sort_keys=False) + "```\n"


# ---------------------------------------------------------------------------
# 1-2. options and the hook
# ---------------------------------------------------------------------------

def _spec(seen=None):
    return {"server": rpr.create_sdk_mcp_server(asm.SERVER_NAME, tools=[]),
            "hook": rpr._analyst_deny_hook([] if seen is None else seen),
            "model": "claude-haiku-4-5", "max_turns": 40, "max_budget_usd": 1.5,
            "timeout_s": 900.0}


def test_flag_off_options_are_unchanged():
    opts = rpr._stage_agent_options()
    assert opts.mcp_servers == {} and opts.allowed_tools == [] and opts.hooks is None
    assert opts.permission_mode is None and opts.max_turns is None


def test_the_analyst_options_are_the_closed_book_base_plus_the_six_tools():
    opts = rpr._stage_agent_options(analyst=_spec())
    assert opts.tools == [] and opts.setting_sources == [] and opts.strict_mcp_config is True
    assert opts.env == {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}
    assert Path(opts.cwd).resolve() == rpr._STAGE_AGENT_CWD.resolve()
    assert list(opts.mcp_servers) == ["analyst"]
    assert opts.allowed_tools == list(asm.ALLOWED_TOOLS) and len(asm.ALLOWED_TOOLS) == 6
    assert opts.permission_mode == "dontAsk"
    assert (opts.max_turns, opts.max_budget_usd) == (40, 1.5)


def test_the_installed_sdk_emits_the_analyst_cli_invocation():
    opts = dataclasses.replace(rpr._stage_agent_options(analyst=_spec()), cli_path="claude")
    cmd = SubprocessCLITransport(prompt="x", options=opts)._build_command()
    assert cmd[cmd.index("--tools") + 1] == ""
    assert "--setting-sources=" in cmd and "--strict-mcp-config" in cmd
    assert cmd[cmd.index("--allowedTools") + 1].split(",") == list(asm.ALLOWED_TOOLS)
    assert cmd[cmd.index("--permission-mode") + 1] == "dontAsk"
    assert cmd[cmd.index("--max-turns") + 1] == "40"
    assert cmd[cmd.index("--max-budget-usd") + 1] == "1.5"
    servers = json.loads(cmd[cmd.index("--mcp-config") + 1])["mcpServers"]
    assert list(servers) == ["analyst"] and servers["analyst"]["type"] == "sdk"


@pytest.mark.parametrize("name", ["Read", "Bash", "WebFetch", "Write", "mcp__other__x",
                                  "mcp__analyst__run_code", None])
def test_the_hook_denies_every_other_tool_and_records_it(name):
    seen = []
    out = asyncio.run(rpr._analyst_deny_hook(seen)({"tool_name": name}, "t", None))
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert seen == [name]


def test_the_hook_allows_the_six():
    seen = []
    hook = rpr._analyst_deny_hook(seen)
    for full in asm.ALLOWED_TOOLS:
        assert asyncio.run(hook({"tool_name": full}, "t", None)) == {}
    assert seen == list(asm.ALLOWED_TOOLS)


def test_the_caps_default_to_the_stage_model_and_refuse_bad_values():
    caps = rpr._analyst_caps({})
    assert caps == {"model": rpr._CLAUDE_WORKER_MODEL, "max_turns": 40, "max_budget_usd": 1.5,
                    "timeout_minutes": 15}
    with pytest.raises(ValueError, match="max_budget_usd"):
        rpr._analyst_caps({"orchestrator": {"analyst": {"max_budget_usd": "1"}}})


@pytest.mark.parametrize("on,missing", [
    ({"folds"}, "specialist_readers.enabled=true and orchestrator.reader_findings"),
    ({"folds", "specialist_readers"}, "reader_findings.enabled=true"),
    ({"folds", "reader_findings"}, "specialist_readers.enabled=true"),
    ({"specialist_readers", "reader_findings"}, "folds.enabled=true"),
])
def test_the_flag_needs_its_stages(monkeypatch, on, missing):
    def reader(name):
        return lambda cfg=None: name in on
    for name in ("folds", "specialist_readers", "reader_findings"):
        monkeypatch.setattr(rpr, f"_{name}_enabled", reader(name))
    cfg = {"orchestrator": {"analyst": {"enabled": True}}}
    with pytest.raises(ValueError, match=missing):
        _REAL_ANALYST_ENABLED(cfg)
    for name in ("folds", "specialist_readers", "reader_findings"):
        monkeypatch.setattr(rpr, f"_{name}_enabled", lambda cfg=None: True)
    assert _REAL_ANALYST_ENABLED(cfg) is True
    assert _REAL_ANALYST_ENABLED({"orchestrator": {}}) is False


# ---------------------------------------------------------------------------
# 3. the stubbed session end to end
# ---------------------------------------------------------------------------

def test_a_stubbed_session_writes_a_reading_decide_next_turns_into_a_fold_b_child(run, monkeypatch):
    stub = _install(monkeypatch, _good_claim)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    assert dest == run / "artifacts" / "proposals" / "trade_efficiency.yaml"
    doc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert doc["rubric_version"] == "trade_efficiency-analyst-v1"
    (side,) = doc["side_findings"]
    assert side["vehicle"] == [] and side["fold_observed"] == "A"
    assert side["scores"]["distance_to_profitable"] == 1 == side["scores"]["mechanism_plausibility"]
    rp.check_reading(doc, "trade_efficiency", "file", strict_provenance=True, analyst=True)
    # the log and the record
    log = yaml.safe_load((run / asm.log_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert [q["function"] for q in log["queries"]] == ["conditional_effect", "trade_slice"]
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert record["outcome"] == "claim" and record["attempts"][0]["status"] == "accepted"
    assert record["why_query"] == "q2" and record["what_was_examined"]
    # the session ran on the analyst options and saw the skill and the lens
    assert stub.options[0].permission_mode == "dontAsk"
    assert "## Your lens: trade efficiency" in stub.prompt
    # decide-next picks it and turns it into a fold-B child brief
    import decide_next as dn
    import test_e077_folds as tf
    (item,) = rp.flatten_reading(doc)
    inputs, _pid = tf._scenario(RUN_ID, "ROOT", {RUN_ID: tf.FOLD_A})
    inputs["runs"][RUN_ID]["proposals"] = [{"category": "trade_efficiency", "proposal": item}]
    inputs["trade_tests"] = True
    record = tf._decide(inputs, RUN_ID)
    cand = tf._cand(record, item["proposal_id"])
    assert cand["eligible"], cand["gates"]
    assert record["picked"]["candidate_id"] == item["proposal_id"]
    front = tf._front(inputs, record)
    assert front["machine_constraints"]["protocol"]["fold"] == "B"
    assert dn  # imported for the scenario helpers


# ---------------------------------------------------------------------------
# 4. code's checks of the answer, the retry, then skipped
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant,needle", [
    (dict(cite_bad=True), "returned"),
    (dict(why=False), "why_query must be the SECOND query"),
    (dict(extra={"vehicle": [], "combines_as": "execution_rule",
                 "evidence": ["q9:result.x=1"]}), "not a successful call"),
])
def test_a_refused_answer_is_retried_then_skipped(run, monkeypatch, variant, needle):
    async def script(call):
        return await _good_claim(call, **variant)
    _install(monkeypatch, script)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    doc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert doc["skipped"]["rule"] == "output_refused_after_retry"
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert [a["status"] for a in record["attempts"]] == ["refused", "refused"]
    assert any(needle in e for e in record["attempts"][0]["errors"]), record["attempts"][0]["errors"]


def test_a_retry_that_fixes_the_answer_is_accepted(run, monkeypatch):
    n = {"calls": 0}

    async def script(call):
        n["calls"] += 1
        return await _good_claim(call, cite_bad=n["calls"] == 1)
    stub = _install(monkeypatch, script)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    assert "side_findings" in yaml.safe_load(dest.read_text(encoding="utf-8"))
    # the retry's prompt names the refusal, carries the refused answer and the log so far
    assert "## Your previous answer was refused" in stub.prompt
    assert "=999" in stub.prompt and '"id": "q1"' in stub.prompt and '"id": "q2"' in stub.prompt
    log = yaml.safe_load((run / asm.log_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert [q["id"] for q in log["queries"]] == ["q1", "q2", "q3", "q4"]   # ids continue


def test_a_claim_test_never_run_is_refused():
    entries = {"q1": {"id": "q1", "function": "describe", "status": "ok",
                      "result": {"groups": {"all": {"mean": 0.5}}}}}
    claim = {"statement": "s", "kind": "execution_behaviour",
             "tests": [{"name": "t", "selector": LONG, "outcome": {"kind": "trade_net_return"},
                        "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
                        "direction": "greater", "floor": {"min_events": 1}}],
             "pass_if": "p", "fail_if": "f", "rationale": "r"}
    text = "```yaml\n" + yaml.safe_dump({"outcome": "claim", "claim": claim, "why_query": "q1",
                                         "evidence": ["q1:groups.all.mean=0.5"], "vehicle": [],
                                         "combines_as": "execution_rule"}) + "```"
    _r, _rec, errors = asm.check_answer(
        text, lens="trade_efficiency", run_id=RUN_ID, entries=entries,
        claim_check=lambda c: cc.check_claim(c, folds=True, trade_tests=True),
        holdout_start=q4.HOLDOUT, fold="A", model_id="m")
    assert any("never run with conditional_effect" in e for e in errors)


def test_a_sealed_date_in_the_answer_is_refused():
    holdout = "2021-01-01"                        # a sentinel start: never the real one
    entries = {"q1": {"id": "q1", "function": "describe", "status": "ok",
                      "result": {"groups": {"all": {"mean": 0.5}}}}}
    text = "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim",
        "no_claim": {"reason": "nothing held after 2021-03 in this run",
                     "best_rejected": {"statement": "s", "killed_by": "q1"}},
        "evidence": ["q1:groups.all.mean=0.5"]}) + "```"
    _r, _rec, errors = asm.check_answer(text, lens="forecast", run_id=RUN_ID, entries=entries,
                                        claim_check=cc.check_claim, holdout_start=holdout,
                                        fold="A", model_id="m")
    assert any("2021-03" in e for e in errors)
    assert asm.sealed_dates("2020-12-31 and 2020-12", holdout) == []


def test_no_claim_is_a_reading_with_no_side_finding(run, monkeypatch):
    async def script(call):
        d = await call("describe", {"column": "forecast"})
        answer = {"outcome": "no_claim",
                  "no_claim": {"reason": "the forecast carries nothing beyond its own level",
                               "best_rejected": {"statement": "high forecasts lead",
                                                 "killed_by": d["query_id"]}},
                  "evidence": [_cite(d["query_id"], d["result"], "groups.all.n")]}
        return "```yaml\n" + yaml.safe_dump(answer) + "```"
    _install(monkeypatch, script)
    dest = rpr.run_analyst_worker("forecast", RUN_ID, run)
    doc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert dest.name == "forecast_power.yaml" and doc["side_findings"] == []
    assert doc["rubric_version"] == "forecast_power-analyst-v1"
    record = yaml.safe_load((run / asm.record_rel("forecast")).read_text(encoding="utf-8"))
    assert record["no_claim"]["best_rejected"]["killed_by"] == "q1"


@pytest.mark.parametrize("k,n,want", [(6, 6, 3), (5, 6, 2), (4, 5, 2), (4, 6, 1), (3, 5, 1),
                                       (3, 6, 0), (0, 0, 0)])
def test_the_simple_score_is_the_in_run_window_agreement(k, n, want):
    entries = {"q1": {"function": "conditional_effect", "status": "ok",
                      "result": {"spec_hash": "h", "horizons": {
                          "1": {"windows_claimed_sign": k, "windows_with_value": n},
                          "6": {"windows_claimed_sign": 6, "windows_with_value": 6}}}}}
    assert asm.in_run_score(["h"], entries) == want
    assert asm.in_run_score(["other"], entries) == 0


def test_an_empty_vehicle_for_another_kind_is_refused_by_the_reading_check(run, monkeypatch):
    async def script(call):
        text = await _good_claim(call)
        return text.replace("kind: execution_behaviour", "kind: conditional_behaviour")
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert any("empty vehicle" in e for e in record["attempts"][0]["errors"])


# ---------------------------------------------------------------------------
# 5. the stage
# ---------------------------------------------------------------------------

def test_under_the_flag_the_lenses_replace_the_readers(run, monkeypatch):
    called = []

    def fake_worker(lens, run_id, run_dir, stage_attempt=0):
        called.append(lens)
        cat = asm.LENS_CATEGORY[lens]
        rpr._write_skipped_reading(cat, run_id, run_dir, {"rule": "output_refused_after_retry",
                                                          "reason": "stub"})
    monkeypatch.setattr(rpr, "run_analyst_worker", fake_worker)
    monkeypatch.setattr(rpr, "run_reader_worker", lambda *a, **k: pytest.fail("a reader ran"))
    monkeypatch.setattr(rpr, "_reader_findings_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_check_reader_budget", lambda *a: None)
    out = rpr._run_specialist_readers(RUN_ID, run)
    assert sorted(called) == ["forecast", "trade_efficiency"]
    for cat in ("profitability", "regime_power", "component_attribution"):
        doc = yaml.safe_load((run / "artifacts" / "proposals" / f"{cat}.yaml").read_text(encoding="utf-8"))
        assert doc["skipped"]["rule"] == "replaced_by_analyst"
    assert set(out) == set(rpr._reader_categories())


def test_flag_off_the_readers_run_as_before(run, monkeypatch):
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: False)
    ran = []

    def fake_reader(category, run_id, run_dir, stage_attempt=0):
        ran.append(category)
        rpr._write_skipped_reading(category, run_id, run_dir, {"rule": "single_component",
                                                               "reason": "stub"})
    monkeypatch.setattr(rpr, "run_reader_worker", fake_reader)
    monkeypatch.setattr(rpr, "run_analyst_worker", lambda *a, **k: pytest.fail("analyst ran"))
    monkeypatch.setattr(rpr, "_reader_findings_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_check_reader_budget", lambda *a: None)
    rpr._run_specialist_readers(RUN_ID, run)
    assert ran == rpr._reader_categories()


def test_the_strictness_keyword_names_the_analyst_only_under_the_flag(monkeypatch):
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: True)
    assert rpr._reader_strictness() == {"strict_provenance": True, "analyst": True}
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: False)
    assert rpr._reader_strictness() == {"strict_provenance": True}
    doc = {"schema_version": 3, "reading_id": "forecast_power-r", "model_id": "m",
           "rubric_version": "forecast_power-analyst-v1", "explanation": "e",
           "evidence": ["x"], "side_findings": []}
    with pytest.raises(rp.ProposalError, match="rubric_version"):
        rp.check_reading(doc, "forecast_power", "w", strict_provenance=True)
    rp.check_reading(doc, "forecast_power", "w", strict_provenance=True, analyst=True)


# ---------------------------------------------------------------------------
# 6. the prompt
# ---------------------------------------------------------------------------

def test_the_prompt_carries_the_skill_lens_inputs_and_memory(run):
    memory = {"claims": [{"claim_id": "c1", "statement": "an earlier <n> claim",
                          "status": "not_confirmed"}]}
    text = asm.build_prompt("forecast", run, base_config_rel="artifacts/none.json", fold="A",
                            memory_view=memory)
    assert text.startswith("---\nname: analyst")
    assert "## Your lens: the forecast" in text
    assert "an earlier <n> claim" in text and "Fold of this run: A" in text
    for name in ("CLAIM_TESTS.md", "CLAIM_TESTS_TRADE.md", "CLAIM_TESTS_EXECUTION.md"):
        assert f"Claim-test vocabulary: {name}" in text
    assert all(full in text for full in asm.ALLOWED_TOOLS)
    with pytest.raises(ValueError):
        asm.build_prompt("regime", run, base_config_rel="x", fold=None, memory_view={})


def test_the_skill_files_name_no_sealed_date():
    import re
    pat = re.compile(r"(?<!\d)\d{4}-\d{2}")
    for p in asm.SKILL_DIR.glob("*.md"):
        for m in pat.finditer(p.read_text(encoding="utf-8")):
            assert m.group(0) < "2024-01", (p.name, m.group(0))


def test_the_retry_section_caps_its_length():
    entries = {f"q{i}": {"id": f"q{i}", "function": "describe", "status": "ok",
                         "result": {"blob": "x" * 9000}} for i in range(1, 30)}
    text = asm.retry_section("answer", ["e1"], entries)
    assert len(text) < asm.RETRY_MAX_CHARS + 10000
    assert "...(cut)" in text and "not shown, over the length cap" in text
    assert "- e1" in text and text.rstrip().endswith("fenced YAML block.")


# ---------------------------------------------------------------------------
# mutation-check additions: each pins one check's edge
# ---------------------------------------------------------------------------

_OK = {"q1": {"id": "q1", "function": "describe", "status": "ok",
              "result": {"groups": {"all": {"mean": 0.123456789}}}},
       "q2": {"id": "q2", "function": "describe", "status": "refused", "reason": "r",
              "result": {"groups": {"all": {"mean": 1.0}}}}}


def test_a_citation_matches_at_eight_significant_digits_only():
    assert asm.check_citations(["q1:groups.all.mean=0.12345679"], _OK) == []
    assert asm.check_citations(["q1:groups.all.mean=0.1234"], _OK)       # 4 digits: refused
    assert asm.check_citations(["q1:groups.all.mean=nan"], _OK)


def test_a_citation_of_a_refused_call_is_refused():
    (err,) = asm.check_citations(["q2:groups.all.mean=1.0"], _OK)
    assert "not a successful call" in err


def test_the_holdout_month_itself_is_sealed():
    assert asm.sealed_dates("from 2020-12 to 2021-01", "2021-01-01") == ["2021-01"]
    assert asm.sealed_dates("2020-12-31", "2021-01-01") == []


@pytest.mark.parametrize("killed_by,ok", [("q1", True), ("q2", False), ("q9", False)])
def test_no_claim_needs_an_ok_killing_query(killed_by, ok):
    text = "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim", "evidence": ["q1:groups.all.mean=0.123456789"],
        "no_claim": {"reason": "nothing", "best_rejected": {"statement": "s",
                                                            "killed_by": killed_by}}}) + "```"
    _r, _rec, errors = asm.check_answer(
        text, lens="forecast", run_id=RUN_ID, entries=_OK, claim_check=None,
        holdout_start=q4.HOLDOUT, fold="A", model_id="m")
    assert (errors == []) is ok, errors


@pytest.mark.parametrize("k,n,want", [(3, 4, 1), (4, 5, 2)])
def test_the_score_thresholds_are_exact(k, n, want):
    entries = {"q1": {"function": "conditional_effect", "status": "ok",
                      "result": {"spec_hash": "h", "horizons": {
                          "1": {"windows_claimed_sign": k, "windows_with_value": n}}}}}
    assert asm.in_run_score(["h"], entries) == want


def test_the_score_is_the_weakest_test():
    entries = {"q1": {"function": "conditional_effect", "status": "ok",
                      "result": {"spec_hash": "a", "horizons": {
                          "1": {"windows_claimed_sign": 6, "windows_with_value": 6}}}},
               "q2": {"function": "conditional_effect", "status": "ok",
                      "result": {"spec_hash": "b", "horizons": {
                          "1": {"windows_claimed_sign": 3, "windows_with_value": 6}}}}}
    assert asm.in_run_score(["a"], entries) == 3
    assert asm.in_run_score(["a", "b"], entries) == 0


def test_a_claim_without_tests_is_refused(run, monkeypatch):
    async def script(call):
        text = await _good_claim(call)
        doc = yaml.safe_load(text.split("```yaml\n", 1)[1].split("```", 1)[0])
        doc["claim"]["tests"] = "none"
        doc["claim"]["missing_block"] = "a per-lot exit rule"
        return "```yaml\n" + yaml.safe_dump(doc) + "```"
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    errs = record["attempts"][0]["errors"]
    assert any("`tests: none` cannot be confirmed" in e for e in errs), errs


def test_the_reading_content_check_runs_on_the_answer(run, monkeypatch):
    """A vehicle naming no component of the run's base config is refused by the readers' own
    content check (_reading_content_errors), not only by the shape check."""
    async def script(call):
        return await _good_claim(call, extra={"vehicle": [
            {"component_id": "no_such_component", "field": "threshold", "before": 1,
             "after": 2}]})
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    errs = record["attempts"][0]["errors"]
    assert any(e.startswith("side_findings[0].vehicle") for e in errs), errs


# ---------------------------------------------------------------------------
# the session's tool list (fail closed) and the smoke CLI
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("init_tools,needle", [
    (None, "reported no tool list"),
    ([*asm.ALLOWED_TOOLS, "Read"], "outside the six: ['Read']"),
])
def test_a_session_with_another_tool_stops_the_stage(run, monkeypatch, init_tools, needle):
    _install(monkeypatch, _good_claim, init_tools=init_tools)
    with pytest.raises(rpr.AnalystToolListError, match=re.escape(needle)):
        rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    assert not (run / "artifacts" / "proposals" / "trade_efficiency.yaml").exists()
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert record["attempts"][-1]["status"] == "tool_list_refused"
    state = yaml.safe_load((run / "pipeline_state.yaml").read_text(encoding="utf-8"))
    (entry,) = state["audit_log"].values()
    assert entry["init_tools"] == init_tools


def test_the_tool_list_check():
    assert asm.tool_list_errors(list(asm.ALLOWED_TOOLS)) == []
    assert asm.tool_list_errors(list(asm.ALLOWED_TOOLS[:2])) == []
    assert asm.tool_list_errors("x")


def test_the_smoke_cli_refuses_a_saved_run_and_a_missing_dir(tmp_path, capsys):
    assert asm.main(["--run", str(SR_ROOT / "runs" / "run_001"), "--lens", "forecast"]) == 2
    assert "copy the run outside" in capsys.readouterr().err
    assert asm.main(["--run", str(tmp_path / "nope"), "--lens", "forecast"]) == 2


def test_the_smoke_cli_runs_the_real_stage_on_a_copy(run, monkeypatch, capsys):
    _install(monkeypatch, _good_claim)
    flags = rpr._analyst_enabled, rpr._folds_enabled
    assert asm.main(["--run", str(run), "--lens", "trade_efficiency"]) == 0
    out = yaml.safe_load(capsys.readouterr().out.split(asm.SMOKE_SUMMARY_MARK, 1)[1])
    assert out["reading"].endswith("trade_efficiency.yaml")
    (entry,) = out["audit_log"].values()
    assert entry["init_tools"] == list(asm.ALLOWED_TOOLS) and entry["tools_denied"] == []
    assert (rpr._analyst_enabled, rpr._folds_enabled) == flags        # restored


# ---------------------------------------------------------------------------
# post-merge review of #359 (D-093)
# ---------------------------------------------------------------------------

def _ce(qid, h, k, n, variant="base", selector=None):
    return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                  "params": {"variant": variant},
                  "result": {"spec_hash": h, "test": {"selector": selector or LONG},
                             "horizons": {"1": {"windows_claimed_sign": k,
                                                "windows_with_value": n, "effect": 0.0123}}}}}


def test_repeating_a_test_on_another_variant_cannot_raise_its_score():
    """M1: the score was the BEST share over every run of the test (best of N variants)."""
    entries = {**_ce("q1", "h", 2, 5), **_ce("q2", "h", 5, 5, variant="v1")}
    assert asm.in_run_score(["h"], entries) == 0
    assert asm.in_run_score(["h"], _ce("q2", "h", 5, 5, variant="v1")) == 3


def _claim_answer(**over):
    claim = {"statement": "Long lots earn more than short lots.", "kind": "execution_behaviour",
             "tests": [{"name": "t", "selector": LONG, "outcome": {"kind": "trade_net_return"},
                        "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
                        "direction": "greater", "floor": {"min_events": 5}}],
             "pass_if": "p", "fail_if": "f", "rationale": "r"}
    claim.update(over.pop("claim", {}))
    doc = {"outcome": "claim", "claim": claim, "why_query": "q3",
           "evidence": ["q1:horizons.1.effect=0.0123"], "vehicle": [],
           "combines_as": "execution_rule", **over}
    return "```yaml\n" + yaml.safe_dump(doc) + "```"


class _Res:
    def __init__(self, h="h"):
        self.errors, self.tests_none, self.tests = [], False, [{"spec_hash": h}]


def _entries_for_claim():
    return {**_ce("q1", "h", 5, 5),
            "q2": {"id": "q2", "function": "list_columns", "status": "ok",
                   "params": {"variant": "base"}, "result": {"variant": "base"}},
            "q3": {"id": "q3", "function": "trade_slice", "status": "ok",
                   "params": {"variant": "base"}, "result": {"groups": {"long": {"n": 12}}}}}


def _check(text, entries=None):
    return asm.check_answer(text, lens="trade_efficiency", run_id=RUN_ID,
                            entries=entries or _entries_for_claim(), claim_check=lambda c: _Res(),
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]


def test_the_reference_answer_is_accepted():
    assert _check(_claim_answer()) == []


@pytest.mark.parametrize("rationale,ok", [
    ("the effect is 9.9% huge", False),                 # a number never seen
    ("the effect is 0.0123 per lot", True),             # cited exactly
    ("the effect is 0.012 per lot", True),              # cited, rounded to what it shows
    ("the effect is 1.23% per lot", True),              # cited, as a percent
    ("the effect is 0.013 per lot", False),             # wrong rounding
    ("at least 5 lots per window", True),               # a number of the test (its floor)
    ("past_return_24 leads the lots", True),            # a name, not a number
    ("in 2023 the longs won", False),                   # a year nobody cited
])
def test_every_number_in_the_prose_must_be_cited(rationale, ok):
    """M2: the claim's free text quoted numbers the session never returned."""
    errors = _check(_claim_answer(claim={"rationale": rationale}))
    assert (errors == []) is ok, errors
    if not ok:
        assert any("claim.rationale writes" in e for e in errors)


def test_evidence_must_cite_the_claim_tests_own_result():
    """M2: evidence passed with any successful citation, e.g. a list_columns call."""
    errors = _check(_claim_answer(evidence=["q2:variant=base"]))
    assert any("evidence must cite the claim test's own result" in e for e in errors), errors


@pytest.mark.parametrize("why,needle", [
    ("q2", "must be a conditional_effect/trade_slice/event_study call"),
    ("q4", "must test another selector"),
])
def test_why_query_must_be_another_measured_prediction(why, needle):
    """L1: any successful call (list_columns, describe, the same selector) satisfied it."""
    entries = {**_entries_for_claim(), **_ce("q4", "h2", 5, 5)}
    errors = _check(_claim_answer(why_query=why), entries)
    assert any(needle in e for e in errors), errors


@pytest.mark.parametrize("why", ["q3", "q4"])               # a trade_slice; a conditional_effect
@pytest.mark.parametrize("key", ["why_query", "evidence", "claim", "vehicle", "outcome",
                                 "combines_as"])
@pytest.mark.parametrize("junk", [["q1"], {"a": 1}, 5, None])
def test_a_malformed_answer_is_refused_never_raised(key, junk, why):
    """M3: `why_query: [q2]` raised TypeError and bypassed the retry."""
    text = "```yaml\n" + yaml.safe_dump({**yaml.safe_load(_claim_answer().split("```yaml\n")[1]
                                                          .split("```")[0]),
                                     "why_query": why, key: junk}) + "```"
    real = lambda c: cc.check_claim(c, trade_tests=True, folds=True)  # noqa: E731
    _r, _rec, errors = asm.check_answer(
        text, lens="trade_efficiency", run_id=RUN_ID,
        entries={**_entries_for_claim(), **_ce("q4", "h2", 5, 5, selector={"kind": "x"})},
        claim_check=real, holdout_start=q4.HOLDOUT, fold="A", model_id="m")
    assert errors


@pytest.mark.parametrize("junk", [["q1"], {"a": 1}, 5])
def test_a_malformed_no_claim_is_refused_never_raised(junk):
    text = "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim", "evidence": ["q1:horizons.1.effect=0.0123"],
        "no_claim": {"reason": "r", "best_rejected": {"statement": "s", "killed_by": junk}}}) + "```"
    assert _check(text)


def test_a_new_stage_attempt_starts_a_new_query_log(run):
    """L2: the log was reopened on a re-attempt, so the earlier attempt's calls counted."""
    for rel in (asm.log_rel("forecast"), asm.record_rel("forecast")):
        (run / rel).parent.mkdir(parents=True, exist_ok=True)
        (run / rel).write_text("queries: []\n", encoding="utf-8")
    rpr._clear_specialist_readers_artifacts(run)
    assert not (run / asm.LOG_DIR_REL).exists() and not (run / asm.RECORD_DIR_REL).exists()


def test_the_analyst_refuses_explore_confirm(monkeypatch):
    """L3: the analyst's queries read E-072's confirmation windows too."""
    for name in ("folds", "specialist_readers", "reader_findings", "explore_confirm"):
        monkeypatch.setattr(rpr, f"_{name}_enabled", lambda cfg=None: True)
    with pytest.raises(ValueError, match="cannot run with orchestrator.explore_confirm"):
        _REAL_ANALYST_ENABLED({"orchestrator": {"analyst": {"enabled": True}}})


def test_evidence_from_another_conditional_effect_is_not_the_tests_own():
    entries = {**_entries_for_claim(), **_ce("q4", "h2", 5, 5, selector={"kind": "x"})}
    errors = _check(_claim_answer(evidence=["q4:horizons.1.effect=0.0123"]), entries)
    assert any("evidence must cite the claim test's own result" in e for e in errors), errors
