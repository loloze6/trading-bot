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
    ce = await call("conditional_effect", {"condition": LONG, "direction": "less"})
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


# review round 2 of #360: the prose-number rule
@pytest.mark.parametrize("field,text,ok", [
    ("rationale", "longs earn -1.23% less than shorts", False),     # sign flipped
    ("rationale", "longs earn +1.23% more", True),
    ("rationale", "longs earn 1.23% more", True),
    ("fail_if", "the mean difference is 0 or below on fold B", True),   # 0 is always fine
    ("fail_if", "the effect at horizon 1 is not positive", True),       # a cited horizon
    ("pass_if", "100% of the lots agree", True),
    ("rationale", "longs earn 5% more per trade", False),         # the floor (5) as an effect
    ("rationale", "an effect of .5 per lot", False),              # a leading dot is a number
    ("rationale", "an effect of 100 per lot", False),             # "100" shows 3 digits
    ("rationale", "over 1,234 trades", False),
    ("rationale", "an effect of 1.23e-2", True),
    ("rationale", "an effect of 9.9pct", False),
    ("rationale", "windows 6,7 agree", False),
])
def test_the_prose_rule_reads_signs_words_and_forms(field, text, ok):
    errors = _check(_claim_answer(claim={field: text}))
    assert (errors == []) is ok, errors


def test_a_huge_integer_in_the_test_is_refused_never_raised():
    huge = 10 ** 400
    text = _claim_answer(claim={"tests": [{"name": "t", "selector": LONG,
                                           "outcome": {"kind": "trade_net_return"},
                                           "baseline": {"kind": "other_trades"},
                                           "statistic": "mean_diff", "direction": "greater",
                                           "floor": {"min_events": huge}}],
                                "rationale": "the effect is 1e400 strong"})
    real = lambda c: cc.check_claim(c, trade_tests=True, folds=True)  # noqa: E731
    _r, _rec, errors = asm.check_answer(
        text, lens="trade_efficiency", run_id=RUN_ID, entries=_entries_for_claim(),
        claim_check=real, holdout_start=q4.HOLDOUT, fold="A", model_id="m")
    assert errors


def test_the_no_claim_text_is_checked_too():
    def answer(reason):
        return "```yaml\n" + yaml.safe_dump({
            "outcome": "no_claim", "evidence": ["q1:horizons.1.effect=0.0123"],
            "no_claim": {"reason": reason,
                         "best_rejected": {"statement": "longs lead", "killed_by": "q3"}}}) + "```"
    assert _check(answer("the effect was 1.23% but it did not hold by coin")) == []
    errors = _check(answer("longs beat shorts by 9.9% but n was small"))
    assert any(e.startswith("no_claim.reason writes '9.9%'") for e in errors), errors


@pytest.mark.parametrize("text,cited,ok", [("100 lots", "140", False), ("100 lots", "100.4", True),
                                           ("0.0120", "0.0123", False), ("0.0120", "0.012", True)])
def test_a_prose_number_shows_all_its_digits(text, cited, ok):
    entries = {"q1": {"id": "q1", "status": "ok", "result": {"n": float(cited)}}}
    errors = asm.prose_number_errors({"claim.rationale": text}, [f"q1:n={cited}"], entries)
    assert (errors == []) is ok, errors


# review round 2 of #360
def _real_check(text, entries=None):
    real = lambda c: cc.check_claim(c, trade_tests=True, folds=True)  # noqa: E731
    return asm.check_answer(text, lens="trade_efficiency", run_id=RUN_ID,
                            entries=entries or _entries_for_claim(), claim_check=real,
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]


@pytest.mark.parametrize("text", [
    _claim_answer(evidence=["q1:horizons.1.effect=0.0123",
                            "q1:horizons." + "9" * 5000 + ".effect=1"]),
    "```yaml\noutcome: claim\nn: " + "9" * 5000 + "\n```",          # past the digit limit
    "```yaml\noutcome: claim\nx: " + "[" * 500 + "]" * 500 + "\n```",
    "```yaml\noutcome: claim\nx: " + "[" * 450 + "]" * 450 + "\n```",
])
def test_oversized_or_deep_answers_are_refused_never_raised(text):
    assert _real_check(text)


def test_a_bug_in_our_claim_check_wiring_stays_loud():
    with pytest.raises(TypeError):
        asm.check_answer(_claim_answer(), lens="trade_efficiency", run_id=RUN_ID,
                         entries=_entries_for_claim(),
                         claim_check=lambda c: cc.check_claim(c, bogus=True),
                         holdout_start=q4.HOLDOUT, fold="A", model_id="m")


@pytest.mark.parametrize("text,needle", [
    ("an effect of +5 per lot", "'+5'"),                  # a test number with a sign
    ("an effect of 5e-400", "'5e-400'"),                  # not zero as written
])
def test_a_test_number_or_a_tiny_number_is_not_an_effect(text, needle):
    errors = _check(_claim_answer(claim={"rationale": text}))
    assert any(needle in e for e in errors), errors


def test_a_test_threshold_written_as_a_percent_gets_a_usable_message():
    tests = [{"name": "t", "selector": {"kind": "trade", "where": [
                  {"field": "past_return_24", "op": ">", "value": 0.02}]},
              "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
              "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 5}}]
    errors = _check(_claim_answer(claim={"tests": tests,
                                         "statement": "lots after a 2% rise earn more"}))
    assert any("not as a percent" in e and "0.02" in e for e in errors), errors


def test_deep_nesting_under_a_valid_key_is_refused_never_raised():
    text = _claim_answer()
    assert text.count("vehicle: []") == 1
    deep = text.replace("vehicle: []", "vehicle: " + "[" * 450 + "]" * 450)
    errors = _real_check(deep)
    assert any("nests deeper than" in e for e in errors), errors


# ---------------------------------------------------------------------------
# D-094: the claim test's floor (smoke session on Windows, 2026-10-09: both lenses wrote a
# real floor, conditional_effect could only log {min_events: 1}, every claim was refused)
# ---------------------------------------------------------------------------

SEL = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
FLOOR = {"min_events": 5, "min_windows": 2}
#: sha256 of the log the floor-less call script below wrote on origin/master 288e36e2
#: (before D-094), measured on Windows 2026-10-09
GOLDEN_FLOORLESS_LOG = "86a802b86395dfa971e2df5222c10fea6c96e928a116215d01b8322afeda7a34"


def _engine(run_dir):
    return q4.engine(run_dir)


def test_a_call_without_a_floor_logs_byte_identically_to_before(tmp_path):
    import hashlib
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    eng.conditional_effect(SEL, [2, 1])
    eng.conditional_effect({"kind": "all"}, [1], statistic="rank_ic")
    eng.conditional_effect({"kind": "trade", "where": q4.TRADE_WHERES[0]})
    eng.conditional_effect(SEL, [1], by="window")
    eng.conditional_effect(SEL, [1], statistic="nope")
    assert hashlib.sha256(eng.log.path.read_bytes()).hexdigest() == GOLDEN_FLOORLESS_LOG


@pytest.mark.parametrize("cond,horizons", [(SEL, [1, 2]),
                                           ({"kind": "trade", "where": q4.TRADE_WHERES[0]}, None)])
def test_the_floor_is_written_into_the_block_and_changes_no_measured_number(tmp_path, cond,
                                                                            horizons):
    import claim_tests as ct
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r0 = eng.conditional_effect(cond, horizons)
    r1 = eng.conditional_effect(cond, horizons, floor=FLOOR)
    assert r0["status"] == r1["status"] == "ok"
    assert r1["result"]["test"]["floor"] == FLOOR
    assert r1["result"]["spec_hash"] == ct.spec_hash(ct.TestSpec.from_dict(r1["result"]["test"]))
    assert r1["result"]["spec_hash"] != r0["result"]["spec_hash"]
    assert r1["result"]["horizons"] == r0["result"]["horizons"]
    assert r1["n_comparisons"] == r0["n_comparisons"]
    log = q4.log_of(eng)
    assert "floor" not in log[0]["params"] and log[1]["params"]["floor"] == FLOOR
    assert asm.floorless_hash(r1["result"]["test"]) == r0["result"]["spec_hash"]


@pytest.mark.parametrize("floor", [[], {}, "100", {"min_bars": 3}, {"min_events": 0},
                                   {"min_events": True}, {"min_events": 2.5},
                                   {"min_events": 10 ** 400}])
def test_a_bad_floor_is_refused_and_logged_never_raised(tmp_path, floor):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect(SEL, [1], floor=floor)
    assert r["status"] == "refused", r
    assert q4.log_of(eng)[-1]["status"] == "refused"


def test_the_tool_schema_offers_the_floor_and_the_handler_passes_it(run):
    props, required = rpr._ANALYST_TOOL_SCHEMAS["conditional_effect"]
    assert props["floor"] == {"type": ["object", "null"]} and "floor" not in required
    assert "floor" in rpr._ANALYST_TOOL_HELP["conditional_effect"]
    skill = (asm.SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "pass the claim's floor as `conditional_effect`'s `floor`" in skill
    tools ={t.name: t for t in rpr._analyst_tools(_engine_on(run, "forecast"))}
    out = asyncio.run(tools["conditional_effect"].handler({"condition": SEL, "horizons": [1],
                                                           "floor": FLOOR}))
    assert json.loads(out["content"][0]["text"])["result"]["test"]["floor"] == FLOOR


def _floor_answer(test, ce_qid, why_qid, cite):
    doc = {"outcome": "claim",
           "claim": {"statement": "Bars with a high forecast are followed by higher returns.",
                     "kind": "execution_behaviour", "tests": [dict(test, name="t")],
                     "pass_if": "higher on the unseen fold", "fail_if": "not higher",
                     "rationale": "the forecast leads the drift"},
           "why_query": why_qid, "evidence": [cite], "vehicle": [],
           "combines_as": "execution_rule"}
    return "```yaml\n" + yaml.safe_dump(doc, sort_keys=False) + "```"


def _entries(eng):
    return {e["id"]: e for e in q4.log_of(eng)}


def _floor_check(eng, text):
    return asm.check_answer(text, lens="forecast", run_id=RUN_ID, entries=_entries(eng),
                            claim_check=lambda c: cc.check_claim(c, trade_tests=True, folds=True),
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")


def test_a_claim_with_a_real_floor_run_with_that_floor_is_accepted(tmp_path):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect(SEL, [1], floor=FLOOR, direction="less")
    w = eng.trade_slice([], [{"field": "trade_net_return", "stat": "mean"}], by="direction")
    text = _floor_answer(r["result"]["test"], r["query_id"], w["query_id"],
                         _cite(r["query_id"], r["result"], "horizons.1.effect"))
    _reading, record, errors = _floor_check(eng, text)
    assert errors == []
    assert record["test_spec_hashes"] == [r["result"]["spec_hash"]]


def test_a_claim_whose_floor_was_never_run_is_refused_with_the_run_to_repeat(tmp_path):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect(SEL, [1])                          # floor {min_events: 1}
    w = eng.trade_slice([], [{"field": "trade_net_return", "stat": "mean"}], by="direction")
    text = _floor_answer(dict(r["result"]["test"], floor=FLOOR), r["query_id"], w["query_id"],
                         _cite(r["query_id"], r["result"], "horizons.1.effect"))
    _reading, _record, errors = _floor_check(eng, text)
    (msg,) = [e for e in errors if "never run with conditional_effect" in e]
    assert 'q1 ran the same test with floor {"min_events": 1}' in msg and "`floor`" in msg


def test_choosing_a_floor_cannot_drop_a_weaker_run_from_the_score():
    """D-094: runs are grouped by the test without its floor; with the exact hash, the weak
    floor-less run on base (2 of 5) would not count and the variant's 5 of 5 would score 3."""
    import claim_tests as ct
    test = {"selector": SEL, "outcome": {"kind": "fwd_return", "horizons": [1]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff",
            "direction": "greater"}
    b0, b1 = dict(test, floor={"min_events": 1}), dict(test, floor=FLOOR)

    def entry(qid, block, k, variant):
        return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                      "params": {"variant": variant},
                      "result": {"spec_hash": ct.spec_hash(ct.TestSpec.from_dict(block)),
                                 "test": block,
                                 "horizons": {"1": {"windows_claimed_sign": k,
                                                    "windows_with_value": 5,
                                                    "effect": 0.0123}}}}}
    entries = {**entry("q1", b0, 2, "base"), **entry("q2", b1, 5, "v1"),
               "q3": {"id": "q3", "function": "trade_slice", "status": "ok",
                      "params": {"variant": "base"}, "result": {"groups": {"long": {"n": 12}}}}}
    assert asm.in_run_score([asm.floorless_hash(b1)], entries) == 0
    text = _floor_answer(b1, "q2", "q3", "q2:horizons.1.effect=0.0123")
    _reading, record, errors = asm.check_answer(
        text, lens="forecast", run_id=RUN_ID, entries=entries,
        claim_check=lambda c: cc.check_claim(c, trade_tests=True, folds=True),
        holdout_start=q4.HOLDOUT, fold="A", model_id="m")
    assert errors == [] and record["scores"]["confidence_real"] == 0
    del entries["q1"]
    assert asm.check_answer(text, lens="forecast", run_id=RUN_ID, entries=entries,
                            claim_check=lambda c: cc.check_claim(c, trade_tests=True,
                                                                 folds=True),
                            holdout_start=q4.HOLDOUT, fold="A",
                            model_id="m")[1]["scores"]["confidence_real"] == 3


def test_a_claim_test_without_its_optional_baseline_keeps_its_score(tmp_path):
    """Review round 1 of #362: claim_card lets a test leave `baseline` out (None); the
    floorless identity must read the block the same way, or the claim silently scores 0."""
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect({"kind": "all"}, [1], statistic="rank_ic", floor=FLOOR, direction="less")
    w = eng.trade_slice([], [{"field": "trade_net_return", "stat": "mean"}], by="direction")
    with_none = r["result"]["test"]
    assert with_none["baseline"] is None
    without = {k: v for k, v in with_none.items() if k != "baseline"}
    assert asm.floorless_hash(without) == asm.floorless_hash(with_none) is not None
    cite = _cite(r["query_id"], r["result"], "horizons.1.effect")
    scores = []
    for block in (with_none, without):
        _rd, record, errors = _floor_check(eng, _floor_answer(block, r["query_id"],
                                                              w["query_id"], cite))
        assert errors == []
        scores.append(record["scores"]["confidence_real"])
    assert scores[0] == scores[1]


def test_why_query_cannot_be_the_claims_own_test_under_another_floor(tmp_path):
    """Review round 1 of #362: the same trade test with its `where` clauses in another order
    and another floor has another exact hash and another selector dict, but is the same
    observation."""
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    a, b = q4.TRADE_WHERES[4]
    q1 = eng.conditional_effect({"kind": "trade", "where": [a, b]}, direction="less")
    q2 = eng.conditional_effect({"kind": "trade", "where": [b, a]}, floor=FLOOR, direction="less")
    assert q1["result"]["spec_hash"] != q2["result"]["spec_hash"]
    text = _floor_answer(q2["result"]["test"], q2["query_id"], q1["query_id"],
                         _cite(q2["query_id"], q2["result"], "horizons.trade.effect"))
    _rd, _rec, errors = _floor_check(eng, text)
    assert any("why_query must be the SECOND query" in e for e in errors), errors


def test_the_skill_says_to_leave_consistency_out():
    skill = (asm.SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "Leave `consistency` out of a claim test" in skill


def test_a_stubbed_session_claiming_a_real_floor_reaches_the_reading(run, monkeypatch):
    async def script(call):
        ce = await call("conditional_effect", {"condition": LONG, "floor": FLOOR, "direction": "less"})
        ts = await call("trade_slice", {"filter": [], "agg": [{"field": "trade_net_return",
                                                                "stat": "mean"}],
                                        "by": "direction"})
        answer = {"outcome": "claim",
                  "claim": {"statement": "Long lots of this strategy earn more than its short "
                                         "lots.", "kind": "execution_behaviour",
                            "tests": [ce["result"]["test"]],
                            "pass_if": "long lots above the others on the unseen fold",
                            "fail_if": "not above", "rationale": "the longs ride the drift"},
                  "why_query": ts["query_id"],
                  "evidence": [_cite(ce["query_id"], ce["result"], "horizons.trade.effect")],
                  "vehicle": [], "combines_as": "execution_rule"}
        return "```yaml\n" + yaml.safe_dump(answer, sort_keys=False) + "```\n"
    _install(monkeypatch, script)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    (side,) = yaml.safe_load(dest.read_text(encoding="utf-8"))["side_findings"]
    assert side["claim"]["tests"][0]["floor"] == FLOOR


# ---------------------------------------------------------------------------
# PR A (smoke 2, 2026-10-09): a multi-block answer reports every error
# ---------------------------------------------------------------------------

def _no_claim_text(reason="the effect was 1.23% but it did not hold by coin"):
    return "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim", "evidence": ["q1:horizons.1.effect=0.0123"],
        "no_claim": {"reason": reason,
                     "best_rejected": {"statement": "longs lead", "killed_by": "q3"}}}) + "```"


def _triple(text, entries=None, real=False):
    check = (lambda c: cc.check_claim(c, trade_tests=True, folds=True)) if real \
        else (lambda c: _Res())
    return asm.check_answer(text, lens="trade_efficiency", run_id=RUN_ID,
                            entries=entries or _entries_for_claim(), claim_check=check,
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")


def _fixed_answers():
    """One-block and no-block answers only: their result must not change with PR A."""
    sealed = q4.HOLDOUT[:7] + "-15"                  # a date inside the holdout month
    never_run = {**_ce("q1", "zz", 5, 5), **{k: v for k, v in _entries_for_claim().items()
                                              if k != "q1"}}
    cases = [(_claim_answer(), None, False),
             (_claim_answer(), None, True),
             (_claim_answer(claim={"rationale": "the effect is 9.9% huge"}), None, False),
             (_claim_answer(evidence=["q1:horizons.1.effect=0.5"]), None, False),
             (_claim_answer(why_query="q2"), None, False),
             (_claim_answer(), never_run, False),
             (_claim_answer(claim={"rationale": f"seen on {sealed}"}), None, False),
             (_no_claim_text(), None, False),
             (_no_claim_text("longs beat shorts by 9.9% but n was small"), None, False),
             ("no yaml here at all", None, False),
             ("", None, False),
             ("```yaml\noutcome: [unclosed\n```", None, False)]
    return cases


#: sha256 of the (reading, record, errors) triples of _fixed_answers() on origin/master
#: 175e1453 (before PR A), measured on Windows 2026-10-09
GOLDEN_ONE_OR_NO_BLOCK = "e30f7420af7187239a8a4928c234b853ec2a1a624c219c6e69dc16e6e00dec57"


def test_a_one_block_or_no_block_answer_checks_byte_identically_to_before():
    import hashlib
    out = [_triple(t, e, r) for t, e, r in _fixed_answers()]
    blob = json.dumps(out, sort_keys=True, default=str)
    assert hashlib.sha256(blob.encode("utf-8")).hexdigest() == GOLDEN_ONE_OR_NO_BLOCK


BLOCK_ERR = "the answer holds 2 fenced YAML block(s); write exactly one"
LAST = "(your last block) "
CLEAN_LINE = LAST + ("passes this answer check (the reading checks run once it is the only "
                     "block): write only that block")


def _bad_last():
    return _claim_answer(claim={"rationale": "the effect is 9.9% huge"})


def test_two_blocks_whose_last_has_errors_list_them_after_the_block_count_error():
    reading, record, errors = _triple(_claim_answer() + "\n\n" + _bad_last())
    assert reading is None
    assert errors[0] == BLOCK_ERR and len(errors) > 1
    assert all(e.startswith(LAST) for e in errors[1:])
    assert any("claim.rationale writes '9.9%'" in e for e in errors[1:]), errors
    assert record["outcome"] is None
    assert not {"why_query", "test_spec_hashes", "scores"} & set(record), record
    # the record is exactly what the one-block error path builds
    assert record == _triple("no yaml here at all")[1]


def test_two_blocks_whose_last_is_clean_are_refused_with_one_line():
    reading, record, errors = _triple(_bad_last() + "\n\n" + _claim_answer())
    assert reading is None and record["outcome"] is None
    assert errors == [BLOCK_ERR, CLEAN_LINE]


def test_two_blocks_run_the_real_claim_check_on_the_last_block():
    no_tests = _claim_answer(claim={"tests": "none", "missing_block": "a per-lot exit rule"})
    errors = _triple(_claim_answer() + "\n\n" + no_tests, real=True)[2]
    assert errors[0] == BLOCK_ERR
    assert any(e.startswith(LAST + "claim: `tests: none` cannot be confirmed") for e in errors), errors


def test_two_blocks_check_the_last_block_against_the_holdout_start():
    sealed = q4.HOLDOUT[:7] + "-15"                  # a date inside the holdout month
    late = _claim_answer(claim={"rationale": f"seen on {sealed}"})
    errors = _triple(_claim_answer() + "\n\n" + late)[2]
    assert errors[0] == BLOCK_ERR
    assert any(e.startswith(LAST + "the answer names date(s)") for e in errors), errors


def test_the_first_block_is_not_the_one_checked():
    _, _, errors = _triple(_bad_last() + "\n\n" + _claim_answer())
    assert not any("9.9%" in e for e in errors)


def test_two_blocks_whose_last_is_unreadable_yaml_add_its_parse_error():
    reading, _, errors = _triple(_claim_answer() + "\n```yaml\noutcome: [unclosed\n```")
    assert reading is None and len(errors) == 2
    assert errors[0] == BLOCK_ERR
    assert errors[1].startswith(LAST + "the answer is not readable YAML")


def test_three_blocks_use_the_last_one():
    text = _bad_last() + "\n" + _claim_answer() + "\n" + _no_claim_text("longs beat shorts by 9.9%")
    errors = _triple(text)[2]
    assert errors[0] == BLOCK_ERR.replace("2", "3")
    assert any(e.startswith(LAST + "no_claim.reason writes '9.9%'") for e in errors), errors
    assert not any("claim.rationale" in e for e in errors)


def test_a_zero_block_answer_keeps_its_single_error():
    assert _triple("nothing fenced")[2] == ["the answer holds 0 fenced YAML block(s); write exactly one"]


def test_the_retry_section_lists_the_multi_block_errors():
    errors = _triple(_claim_answer() + "\n" + _bad_last())[2]
    text = asm.retry_section("answer", errors, _entries_for_claim())
    assert f"- {BLOCK_ERR}" in text and f"- {LAST}claim.rationale writes '9.9%'" in text


# ---------------------------------------------------------------------------
# PR B (smoke 2, 2026-10-09): a claim whose test measured the opposite sign
# ---------------------------------------------------------------------------

def _ceo(qid, h, oriented, variant="base", k=5, n=5):
    """A conditional_effect run of test `h`; `oriented` is {horizon: oriented value}."""
    hs = {hz: {"windows_claimed_sign": k, "windows_with_value": n, "effect": 0.0123,
               "oriented": o} for hz, o in oriented.items()}
    return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                  "params": {"variant": variant},
                  "result": {"spec_hash": h, "test": {"selector": LONG}, "horizons": hs}}}


def _opp_entries(*runs):
    rest = {k: v for k, v in _entries_for_claim().items() if k != "q1"}
    return {**rest, **{q: e for r in runs for q, e in r.items()}}


OPP = "measured the opposite of its direction in "


def _opp_errors(entries, **kw):
    return [e for e in _check(_claim_answer(**kw), entries) if OPP in e]


def test_a_test_that_measured_the_opposite_at_every_horizon_is_refused():
    entries = _opp_entries(_ceo("q1", "h", {"1": -0.02, "2": -0.01}, k=1, n=5))
    (msg,) = _opp_errors(entries)
    assert msg == ("claim test h... measured the opposite of its direction in q1 (h=1: 1 of 5 "
                   "windows with the claimed sign; h=2: 1 of 5 windows with the claimed sign): "
                   "flip `direction` if the opposite is your claim, drop those horizons from "
                   "the test, or end with no_claim (a changed test must be run with "
                   "conditional_effect before you claim it)")


def test_the_same_data_with_the_flipped_direction_is_accepted_through_the_real_check():
    """The model-written block goes through the real claim check: the flipped test is another
    spec_hash, and its run logs a positive oriented value."""
    import claim_tests as ct
    test = {"selector": SEL, "outcome": {"kind": "fwd_return", "horizons": [1]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff",
            "floor": {"min_events": 1}}

    def entry(qid, direction, o):
        block = dict(test, direction=direction)
        return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                      "params": {"variant": "base"},
                      "result": {"spec_hash": ct.spec_hash(ct.TestSpec.from_dict(block)),
                                 "test": block,
                                 "horizons": {"1": {"windows_claimed_sign": 5,
                                                    "windows_with_value": 5, "effect": 0.0123,
                                                    "oriented": o}}}}}
    both = {**entry("q1", "greater", -0.0123), **entry("q2", "less", 0.0123),
            "q3": {"id": "q3", "function": "trade_slice", "status": "ok",
                   "params": {"variant": "base"}, "result": {"groups": {"long": {"n": 12}}}}}

    def errors_of(direction, ce):
        text = _floor_answer(dict(test, direction=direction), ce, "q3",
                             f"{ce}:horizons.1.effect=0.0123")
        return asm.check_answer(text, lens="forecast", run_id=RUN_ID, entries=both,
                                claim_check=lambda c: cc.check_claim(c, trade_tests=True,
                                                                     folds=True),
                                holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]
    (msg,) = [e for e in errors_of("greater", "q1") if OPP in e]
    assert "in q1 (h=1: 5 of 5" in msg and "flip `direction`" in msg
    assert errors_of("less", "q2") == []


def test_a_stub_check_flipped_direction_with_a_positive_run_is_accepted():
    assert _opp_errors(_opp_entries(_ceo("q1", "h", {"1": 0.02}))) == []


@pytest.mark.parametrize("oriented", [
    {"1": 0.0, "2": 0.0},                          # exactly 0 is not opposite
    {"1": 0.02, "2": 0.0},                         # one above, one exactly 0
    {"1": None, "2": None},                        # no value anywhere
    {},                                            # no horizon at all
])
def test_zero_positive_or_valueless_runs_are_not_refused_by_this_rule(oriented):
    assert _opp_errors(_opp_entries(_ceo("q1", "h", oriented))) == []


@pytest.mark.parametrize("oriented", [
    {"1": 0.01, "2": -0.02},                       # mixed signs: fold B's any-horizon rule
    {"1": -0.02, "2": 0.0},                        # one below, one exactly 0
])
def test_one_opposite_horizon_is_enough_and_only_it_is_named(oriented):
    (msg,) = _opp_errors(_opp_entries(_ceo("q1", "h", oriented, k=2, n=5)))
    assert msg.count("windows with the claimed sign") == 1
    bad = [hz for hz, o in oriented.items() if o < 0]
    assert f"(h={bad[0]}: 2 of 5 windows with the claimed sign):" in msg


def test_a_horizon_without_a_value_is_skipped():
    entries = _opp_entries(_ceo("q1", "h", {"1": -0.02, "2": None}))
    assert len(_opp_errors(entries)) == 1


def test_any_run_of_the_test_counts_not_only_the_base_run():
    entries = _opp_entries(_ceo("q1", "h", {"1": 0.02}),
                           _ceo("q4", "h", {"1": -0.03}, variant="v1", k=0))
    (msg,) = _opp_errors(entries)
    assert "in q4 (h=1: 0 of 5" in msg


def test_the_claims_exact_hash_runs_alone_do_not_hide_an_opposite_run_under_another_floor():
    """Review round 1: the claim is written with FLOOR (its exact hash is q2's, positive);
    q1 ran the same test with the unit floor on base and measured negative."""
    import claim_tests as ct
    test = {"selector": SEL, "outcome": {"kind": "fwd_return", "horizons": [1]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff",
            "direction": "greater"}
    b0, b1 = dict(test, floor={"min_events": 1}), dict(test, floor=FLOOR)

    def entry(qid, block, o, variant):
        return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                      "params": {"variant": variant},
                      "result": {"spec_hash": ct.spec_hash(ct.TestSpec.from_dict(block)),
                                 "test": block,
                                 "horizons": {"1": {"windows_claimed_sign": 1,
                                                    "windows_with_value": 5,
                                                    "effect": 0.0123, "oriented": o}}}}}
    entries = {**entry("q1", b0, -0.02, "base"), **entry("q2", b1, 0.02, "v1"),
               "q3": {"id": "q3", "function": "trade_slice", "status": "ok",
                      "params": {"variant": "base"}, "result": {"groups": {"long": {"n": 12}}}}}
    text = _floor_answer(b1, "q2", "q3", "q2:horizons.1.effect=0.0123")
    errors = asm.check_answer(
        text, lens="forecast", run_id=RUN_ID, entries=entries,
        claim_check=lambda c: cc.check_claim(c, trade_tests=True, folds=True),
        holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]
    (msg,) = [e for e in errors if OPP in e]
    assert " in q1 (h=1: 1 of 5" in msg


def test_the_first_offending_run_is_named_in_query_id_order():
    entries = _opp_entries(_ceo("q10", "h", {"1": -0.03}, variant="v2"),
                           _ceo("q4", "h", {"1": -0.03}, variant="v1"))
    (msg,) = _opp_errors(entries)
    assert " in q4 (" in msg


def test_the_trade_family_horizon_counts_too():
    entries = _opp_entries(_ceo("q1", "h", {"trade": -0.02}))
    (msg,) = _opp_errors(entries, evidence=["q1:horizons.trade.effect=0.0123"])
    assert "h=trade: 5 of 5 windows with the claimed sign" in msg


def test_a_two_block_answer_whose_last_block_is_opposite_gets_the_prefixed_error():
    entries = _opp_entries(_ceo("q1", "h", {"1": -0.02}))
    errors = _triple(_claim_answer() + "\n\n" + _claim_answer(), entries)[2]
    assert errors[0] == BLOCK_ERR
    assert any(e.startswith(LAST + "claim test h... " + OPP + "q1 (") for e in errors), errors


# ---------------------------------------------------------------------------
# PR C (smoke 2, 2026-10-09): the reply says with/against your direction in words
# ---------------------------------------------------------------------------

def test_the_reply_reads_each_horizon_in_words_matching_the_sign_of_oriented(tmp_path):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect(SEL, [2, 1])
    hz = r["result"]["horizons"]
    word = {True: "with your direction", False: "against your direction"}
    expect = [f"h={k}: " + ("no value" if v["oriented"] is None else
                            "zero" if v["oriented"] == 0 else word[v["oriented"] > 0])
              for k, v in hz.items()]
    assert len(expect) == 2 and r["direction_reading"] == expect


def test_the_direction_reading_helper_words_every_case_exactly():
    from analyst_queries import _direction_reading
    hs = {"1": {"oriented": 0.5}, "2": {"oriented": -0.5}, "3": {"oriented": 0},
          "4": {"oriented": None}, "5": {"oriented": True}, "trade": {"oriented": -1}}
    assert _direction_reading(hs) == [
        "h=1: with your direction", "h=2: against your direction", "h=3: zero",
        "h=4: no value", "h=5: no value", "h=trade: against your direction"]


def test_the_direction_reading_is_not_logged_and_the_result_is_unchanged(tmp_path):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    r = eng.conditional_effect(SEL, [1])
    (entry,) = q4.log_of(eng)
    assert "direction_reading" not in entry["result"] and "direction_reading" not in entry
    assert r["result"] == entry["result"]


def test_refused_calls_and_the_other_tools_have_no_direction_reading(tmp_path):
    eng = _engine(q4.make_run(tmp_path / "run_001"))
    replies = [eng.conditional_effect(SEL, [1], statistic="nope"), eng.list_columns(),
               eng.describe("close"), eng.distribution("close"),
               eng.trade_slice([], [{"field": "entry_forecast", "stat": "mean"}]),
               eng.event_study([], 2, 2)]
    assert replies[0]["status"] == "refused"
    assert all("direction_reading" not in r for r in replies)


def test_the_skill_explains_direction_and_exact_citations():
    skill = " ".join((asm.SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").split())
    assert "`direction_reading`" in skill and "never rounded" in skill
    assert "a negative `oriented` means the data says the opposite" in skill


# ---------------------------------------------------------------------------
# D1 (smoke 3, 2026-10-09): why_query must use another filter
# ---------------------------------------------------------------------------

WHYF = "why_query must use another filter than the claim's own test"
SELX = "why_query must test another selector than the claim's own test"
C1 = {"field": "side", "op": "==", "value": "long"}
C2 = {"field": "holding_bars", "op": ">", "value": 5}
C3 = {"field": "side", "op": "in", "value": ["long", "short"]}


_D1_TEST = {"name": "t", "outcome": {"kind": "trade_net_return"},
            "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
            "direction": "greater", "floor": {"min_events": 5}}


def _why_entries(why, claim_sel=LONG):
    rest = {k: v for k, v in _entries_for_claim().items() if k not in ("q1", "q3")}
    return {**_ce("q1", "h", 5, 5, selector=claim_sel), **rest, "q3": why}


def _ts(filt):
    return {"id": "q3", "function": "trade_slice", "status": "ok",
            "params": {"filter": filt, "agg": [], "by": "window", "variant": "base"},
            "result": {"groups": {}}}


def _es(filt):
    return {"id": "q3", "function": "event_study", "status": "ok",
            "params": {"trade_filter": filt, "bars_before": 2, "bars_after": 2,
                       "variant": "base"}, "result": {}}


def _ce_why(sel):
    return _ce("q3", "h2", 5, 5, selector=sel)["q3"]


def _why_errs(why, claim_sel=LONG):
    claim = {"tests": [{**_D1_TEST, "selector": claim_sel}]}
    text = _claim_answer(claim=claim)
    return [e for e in _check(text, _why_entries(why, claim_sel)) if "why_query" in e]


def _trade(*clauses):
    return {"kind": "trade", "where": list(clauses)}


def test_a_trade_slice_on_the_claims_own_filter_is_refused():
    (msg,) = _why_errs(_ts([C1]))
    assert msg.startswith(WHYF)


def test_an_event_study_on_the_claims_own_filter_is_refused():
    (msg,) = _why_errs(_es([C1]))
    assert msg.startswith(WHYF)


def test_the_same_clauses_in_another_order_are_refused_once():
    sel = _trade(C1, C2)
    errs = _why_errs(_ce_why(_trade(C2, C1)), sel)
    assert len(errs) == 1 and errs[0].startswith(WHYF)
    errs = _why_errs(_ts([C2, C1]), sel)
    assert len(errs) == 1 and errs[0].startswith(WHYF)


def test_the_same_trade_selector_in_the_same_order_keeps_the_selector_message_once():
    errs = _why_errs(_ce_why(LONG))
    assert len(errs) == 1 and errs[0].startswith(SELX)


@pytest.mark.parametrize("why", [_ts([C1, C2]), _ts([C2]), _es([C2]),
                                 _ts([{**C1, "value": "short"}]),     # another value
                                 _ts([{**C1, "op": "!="}]),           # another op
                                 _ts([{**C1, "field": "direction"}]),  # another field
                                 _ts([C3])])
def test_a_different_filter_is_accepted(why):
    assert _why_errs(why) == []


def test_the_empty_filter_equals_an_empty_where_only():
    assert _why_errs(_ts([]), _trade())[0].startswith(WHYF)
    assert _why_errs(_es([]), _trade())[0].startswith(WHYF)
    assert _why_errs(_ts([]), LONG) == []


def test_a_bar_selector_claim_keeps_the_exact_selector_rule():
    other = {"kind": "event", "field": "forecast", "op": ">=", "value": 9.0}
    assert _why_errs(_ce_why(other), SEL) == []
    (msg,) = _why_errs(_ce_why(SEL), SEL)
    assert msg.startswith(SELX)
    assert _why_errs(_ts([C1]), SEL) == []


def test_a_malformed_filter_is_never_a_match():
    assert asm._clause_set("x") is None and asm._clause_set([{"field": "a"}]) is None
    assert asm._clause_set([C1]) == asm._clause_set([dict(C1)])
    assert asm._clause_set([C3]) == asm._clause_set([{**C3, "value": ["short", "long"]}])
    assert asm._clause_set([C2]) == asm._clause_set([{**C2, "value": 5.0}])
    assert asm._clause_set([C2]) != asm._clause_set([{**C2, "value": 6}])
    assert asm._clause_set([{**C1, "value": {1, 2}}]) is None   # not JSON: never raises
    assert asm._clause_set([{**C2, "value": 10 ** 400}]) is None  # past float range: never raises


def test_the_engines_own_equalities_are_one_filter():
    c5 = _trade(C2)
    assert _why_errs(_ts([{**C2, "value": 5.0}]), c5)[0].startswith(WHYF)
    both = _trade(C3)
    flipped = {**C3, "value": ["short", "long"]}
    for why in (_ts([flipped]), _es([flipped])):
        assert _why_errs(why, both)[0].startswith(WHYF)
    errs = _why_errs(_ce_why(_trade(flipped)), both)
    assert len(errs) == 1 and errs[0].startswith(WHYF)
    assert _why_errs(_ts([{**C2, "value": 6}]), c5) == []


def test_a_repeated_clause_is_the_same_filter():
    assert _why_errs(_ts([C1, C1]), _trade(C1))[0].startswith(WHYF)


def test_a_filter_equal_to_any_of_several_claim_tests_is_refused():
    claim = {"tests": [{**_D1_TEST, "selector": LONG},
                       {**_D1_TEST, "name": "u", "selector": _trade(C2)}]}
    errs = [e for e in _check(_claim_answer(claim=claim), _why_entries(_ts([C2]))) if WHYF in e]
    assert len(errs) == 1
