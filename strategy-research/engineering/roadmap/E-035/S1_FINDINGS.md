# E-035 S1 — The automated external-knowledge dispatch: characterize-and-stop

Read-only characterization at `0b1021ba` (origin/master), branch
`docs/e035-s1-external-dispatch`. No code, config or backtest changed; the holdout was not
opened. Line numbers were re-read in this checkout with Git Bash `grep -n` / `sed -n` and the
Read tool; function names are the stable reference. The installed agent SDK was read at
`claude_agent_sdk==0.2.82` (system Python 3.13 site-packages, bundled CLI `claude.exe
--version` = 2.1.142). The sealed holdout window is referred to only as "the sealed holdout
window" or "`holdout_range` start" (`config/campaign_data_policy.yaml:18`); no date inside it
appears in this document.

Inputs read: Linear P-CUL-36 story text (as pasted in the dispatch); `delivery_plan_v26.md`
rules (L17-48), slice 6b (L345-373) and slice 8 (L447-459);
`E-036/S1_FINDINGS_SLICE8.md` (guesses, §3, Decision, Correction);
`E-059/S1_FINDINGS_6B.md` (guesses, §3, §4.3, Decision); E-032 S1
`E-032/artifacts/s1_idea_generation.md` Task 4 (L404-472); the code cited below.

---

## Guesses for the operator (read this first)

Each is a real choice the target design does not already make. The recommendation is what S2
builds if you say nothing.

1. **The existing stages are NOT closed-book today. Fix that first, as its own ticket.**
   *(blocks the build)*
   Every stage agent is started with `ClaudeAgentOptions(model=..., allowed_tools=[])`. In
   this SDK, `allowed_tools` only lists tools that run *without asking*; it does not limit
   which tools exist. The option that limits them is `tools`, and it is never set, so every
   stage gets Claude Code's full default tool set. The SDK also loads the operator's own
   settings files (because `setting_sources` is unset), and the untracked
   `strategy-research/.claude/settings.local.json` on this machine pre-approves `Read` on the
   whole repository, which includes `trading-bot/local_data/holdout_sealed/`. This is
   measured, not theoretical: a run_060 `validation` agent read two config files from disk
   that were not in its handoff (§1.2). So "every stage runs closed-book" is false today, and
   E-035's premise "open ONE stage, keep the rest closed" needs the rest closed first.
   *Recommendation:* a separate small ticket, before E-035 S2: pass `tools=[]` and
   `setting_sources=[]` at both call sites. That is a declared behaviour change for
   `validation` (it used those reads), so it needs a before/after on one real run. Until
   then, narrow that local allow rule or add a deny rule for `holdout_sealed` on every machine
   that runs campaigns.

2. **The trigger is decide_next's own stop, turned into one new rule "R3".**
   *(default is safe)*
   "Internal sources exhausted" already has an exact meaning in code: decide_next returns
   `stop: no_eligible_candidate` when nothing is scheduled, no reader proposal or extra card
   is eligible, and no brief is left open for R2 (§2). Recommendation: under the flag, that
   same decision records R3 ("ask the outside for one idea") instead of stopping, as long as
   the external budget is not spent. No second, parallel exhaustion signal.

3. **An automated outside idea enters exactly like your manual one: as a brief.**
   *(blocks the build — needs your template)*
   The agent returns a mechanism. Code writes it into a brief file under
   `campaign_record/external_briefs/`, registers it with `origin: external` and
   `brief_status: open`, and it then goes through Step 0 → 1a → 1b → grid like any brief.
   A brief also needs its scope: coins, venue, product, timeframe and the protocol pin
   (`machine_constraints`). The agent must not choose those. *Recommendation:* you write one
   template, `config/external_brief_template.md`, holding that scope; the agent fills only
   the mechanism and the source. Without the template, S2 cannot build the writer.

4. **Start with model knowledge only. No live web access in the first build.**
   *(blocks the build — holdout policy)*
   The web contains commentary on the sealed holdout window. A search result page shows it
   to the agent even if the agent never cites it, and nothing in code can prove an idea was
   not inspired by it. A model whose training data ends before the `holdout_range` start
   cannot have seen that window at all. *Recommendation:* ship the web grant designed and
   tested but switched off (`web_access: false`), run the first external idea on model
   knowledge alone with a pinned pre-seal model (the stages' current `claude-haiku-4-5`;
   confirm its published training-data cutoff against Anthropic's model page at build time),
   and turn web access on only by a later written decision that accepts the residual risk.
   Every cited source must be dated strictly before the `holdout_range` start, in either
   mode.

5. **Mechanism only: no numbers that look like parameters.** *(default is safe)*
   The returned shape has no numeric field at all, and a lint refuses prose such as
   "a 20-day lookback" or "a 1.5 standard-deviation threshold". Parameters are set at 1b
   from the bot's own design guide and then stressed by the variants and the plateau bar.
   Too strict costs one wasted dispatch; too loose imports a fitted rule. Strict is the safe
   side.

6. **Publication bias: record the date, require the era criterion.** *(default is safe)*
   Each source carries its publication date (and the sample it studied, when stated). An
   external idea's criteria must include the existing menu criterion
   `sign_consistent_by_era`, so an effect that lived only in the author's sample fails on
   the other eras. No extra "before vs after publication" gate in S2; that can come later as
   a report.

7. **Budget: one automated dispatch per campaign by default.** *(default is safe)*
   Counted in an append-only `campaign_record/external_dispatches.yaml`; each dispatch also
   has a turn cap and a cost ceiling. Raise the cap in `campaign_config.yaml` when wanted.

8. **The repeat check must be on before this flag can be on.** *(blocks the build —
   sequencing)*
   decide_next treats `origin: external` like an operator entry: no scoring and no novelty
   gate (`decide_next.py:132`). E-036's decision made the 5a gate
   (`variant_anti_adjacency_gate`) the backstop for such entries, but that flag is off today
   and waits on the S2b replay report. *Recommendation:* the external-dispatch flag refuses
   to turn on unless `variant_anti_adjacency_gate` is on.

9. **A mechanism that needs a feed we do not have is filed, not run.** *(default is safe)*
   If its measurable proxy is not a wired feed, the dispatch writes one row to
   `campaign_record/data_requests.yaml` (the E-035 S2c lane, stage `external_knowledge`),
   registers nothing, and the campaign stops as it would have. The dispatch still counts
   against the budget.

10. **Your manual path gets the same provenance.** *(default is safe)*
    `run_campaign.py register --origin external` (new option) refuses a brief without a
    valid `external_source` block, so a hand-written outside idea records source and date
    the same way.

---

## 1. Where the grant lives, and what "closed-book" really is today

### 1.1 How stage agents get tools

Two call sites, one model constant:

- `run_claude_worker` (`workflow/run_phase1_research.py:919-1021`): builds the prompt with
  `_build_stage_prompt` (L790-891: skill file + handoff + the handoff's
  `required_inputs`/`optional_inputs` pasted as text), then
  `query(prompt=..., options=ClaudeAgentOptions(model=_CLAUDE_WORKER_MODEL,
  allowed_tools=[]))` (L939-942). The comment at L937-938 states the intent: *"We pass an
  empty allowed_tools list to prevent it from wandering off and strictly enforce our
  handoff file constraints."*
- `_invoke_reader_llm` (L3042-3057, the five specialist readers): the same options
  (L3049-3050).
- `_CLAUDE_WORKER_MODEL = "claude-haiku-4-5"` (L896). The Gemini path (`run_gemini_worker`,
  L1037) is a plain `generate_content` call with no tools.
- The process working directory is `strategy-research/` (RUNBOOK L115/L182 launch from
  there; `_build_stage_prompt` opens skills relative to `.`, L811), and no `cwd` is passed.

What those options mean in this SDK (read from the installed package, not assumed):

| SDK option | Docstring (`claude_agent_sdk/types.py`) | CLI flag emitted (`_internal/transport/subprocess_cli.py`) |
|---|---|---|
| `tools` | L1582-1591: "the base set of available built-in tools … `[]` (empty list) — Disable all built-in tools" | L241-250: `--tools ""` only when `tools == []`; **nothing when `None`** (the default) |
| `allowed_tools` | L1593-1603: "Tool names that are auto-allowed without prompting … To restrict which tools are available at all, use `tools`" | L252-257: `--allowedTools` only when the list is non-empty; **`[]` emits nothing** |
| `setting_sources` | L1800-1810: "When `None`, all sources are loaded (matches CLI defaults). Pass `[]` to disable filesystem settings (SDK isolation mode)" | L352-353: nothing when `None` |
| `permission_mode`, `disallowed_tools`, `max_turns`, `max_budget_usd`, `cwd`, `strict_mcp_config`, `hooks` | L1629-1771 | L259-286, L340-341; `cwd` at L468-479 |

The bundled CLI's own help (`claude.exe --help`, 2.1.142) agrees: `--tools <tools...>`
"Specify the list of available tools from the built-in set. Use "" to disable all tools";
`--allowedTools` "list of tool names to allow".

So `allowed_tools=[]` is a no-op: each stage agent has the default Claude Code tool set, and
whether a call runs is decided by the permission layer — which, with `setting_sources=None`,
includes the operator's user/project/local settings files.

### 1.2 Measured: stage agents do use tools

- **Transcripts** (Git Bash, `grep -o` over
  `~/.claude/projects/C--Users-alauz-Documents-Projects-trading-bot-strategy-research/*.jsonl`,
  the SDK sessions launched from `strategy-research/`): 5 transcripts retained, all
  `"entrypoint":"sdk-py"`, model `claude-haiku-4-5-20251001`, prompt starting
  `PERSONA AND RULES`. One (`8085f79f-….jsonl`, handoff `run_id: run_060, from_stage:
  innovation_expansion, to_stage: validation`) holds two `Read` tool calls —
  `strategy-research/config/campaign_data_policy.yaml` and
  `strategy-research/config/cost_model.yaml` — and both `tool_result` blocks contain the
  files' contents. Neither file is in that stage's handoff inputs.
- **Turn counts** (Git Bash, `grep -rn "num_turns" runs/*/pipeline_state.yaml`): 51 audit
  entries carry `num_turns`; 40 are 1, 11 are more than 1 (8 × 5, 2 × 3, 1 × 10). The 11 are
  10 `validation` calls (run_048, run_050 ×3, run_053, run_054, run_057, run_058, run_059,
  run_060) and 1 `hypothesis_generation` call (run_057, 10 turns). More than one turn is
  consistent with tool calls; only the retained transcript above proves it for one call.
- **Permissions in effect** (read with system Python, `json.load`, permission keys only):
  `~/.claude/settings.json` has no `permissions.allow`. The untracked
  `strategy-research/.claude/settings.local.json` has 20 allow rules, including
  `Read(//c/Users/alauz/Documents/Projects/trading-bot/**)` — the whole repo, so also
  `trading-bot/local_data/holdout_sealed/`. The untracked repo-root
  `.claude/settings.local.json` allows `WebSearch` and several `WebFetch(domain:…)`; whether a
  session started in `strategy-research/` also picks that file up was not verified here.
  Either way these files are per-machine and untracked, so a stage's effective tool grant
  today differs between the Windows and Mac machines.

Consequences:

1. E-032 S1's "stage agents have ZERO tool access" (Task 4, L408-415; its measuring script
   `s1_measure_idea_generation.py:135-136` only checked that the text `allowed_tools=[]`
   exists) is wrong. `tests/test_e056_1b_block_manifest.py:552` carries the same assumption
   in a comment.
2. Holdout: a stage agent can read the sealed store without any prompt on this machine.
   No run is known to have done so (only 5 transcripts are retained), but nothing in code
   stops it. That is guess 1.

### 1.3 What giving ONE agent web access would require

A separate call path (not a flag on an existing stage), with every restriction set in code
so that nothing depends on a machine's settings files:

```python
ClaudeAgentOptions(
    model=<pinned, pre-seal model>,            # guess 4
    tools=["WebSearch", "WebFetch"] if web_access else [],   # the grant itself
    allowed_tools=(["WebSearch"] + [f"WebFetch(domain:{d})" for d in allowed_domains])
                  if web_access else [],        # auto-approve only these
    permission_mode="dontAsk",                  # anything not pre-approved is denied
    setting_sources=[],                         # ignore every settings file on disk
    strict_mcp_config=True,                     # no MCP servers from anywhere
    cwd=<fresh empty temp dir>,                 # nothing to read even if a file tool slipped in
    max_turns=<knob>, max_budget_usd=<knob>,
    hooks={"PreToolUse": [<logger that records every query/URL, and denies a URL
                          outside allowed_domains>]},
)
```

- With `tools` limited to `WebSearch`/`WebFetch` there is no `Read`, `Bash`, `Write`, `Glob`
  or `Grep`, so the agent cannot touch the repository or the holdout at all.
- `max_budget_usd`: the SDK passes `--max-budget-usd`, but the CLI help says it "only works
  with --print", and the SDK drives the CLI in `--input-format stream-json` mode
  (`subprocess_cli.py:408`) — **not verified that the ceiling is enforced**. S2 must also
  enforce its own ceiling from the result message's `total_cost_usd` and `num_turns` (the
  same fields `run_claude_worker` already reads, L949-952) and fail loud when exceeded.
- The prompt is a skill file under `workflow_artifacts/skills/external-knowledge/SKILL.md`
  (the project's one skill system), not a new mechanism.

**What must stay closed-book:** every existing stage — `hypothesis_generation`,
`strategy_config_authoring`, `innovation_expansion`, `validation`, `backtest_specification`
(LLM path), `verdict_interpreter`, `campaign_review`, and the five readers. Today they are
closed only by prompt text (guess 1). The external agent's output reaches them only as brief
text (§3), never as a tool, a file they can open, or a stage input of its own.

---

## 2. What "internal sources exhausted" is in the new design

decide_next already defines it (`tools/decide_next.py`). In order (module docstring L24-59,
`decide()` L1604-1742):

| Signal | Code | Meaning |
|---|---|---|
| Something is scheduled | `select_entry(...)` L1649; picked L1666-1672 | an in_progress or ready entry (operator, `external`, agent) runs next |
| Eligible candidate pool | L1621-1647 | reader proposals not yet queued + a brief's `queued` extra cards, after the binding exact-match novelty gate and feasibility (incl. S2c's `requires_feed`) |
| R2: ask 1a for more from an open brief | `_r2` L1491-1545 | only when nothing is scheduled and nothing eligible |
| Brief exhausted | `brief_status: exhausted` (1a says so: `completed_brief_exhausted`), or `BRIEF_MAX_CONSECUTIVE_EMPTY_R2 = 2` consecutive empty requests (L157-164, L1501-1503) | that brief can no longer feed R2 |
| **Stop** | L1706-1711: `stop = {"reason": "no_eligible_candidate", ...}` | nothing scheduled, 0 eligible candidates, no eligible open brief |

The caller turns a stop into the end of the campaign:
`run_campaign._finish_lineage_with_decision` (`workflow/run_campaign.py:3035-3158`) logs
`DECIDE stop …` (L3136-3139) and returns `keep_going = stop is None` (L3158);
`run_forever` (L3536-3540) then exits. Separately, `process_once` exits with "Queue
exhausted" when a step starts with nothing to run (L2566-2569) — no decision is made there.

**Recommendation: one trigger, R3, inside `decide()`.** When the flag is on and `decide()`
would return `stop: no_eligible_candidate`, it instead records
`rules.r3 = {fired: true, dispatches_used: n, max: m}` and
`picked = {"r3_external": <entry_id>, ...}`, where the entry id is minted like R2's
(`external-<n>`). When the budget is spent it records `fired: false, reason:
external_budget_spent` and stops exactly as today. This keeps "the next run is chosen only by
decide_next": the decision record names the pick; the caller performs the dispatch, writes
the brief and registers it (the same division of labour R1 and R2 already use,
L3104-3107). Why not the alternatives:

- *"Operator queue empty"* is weaker: it would fire while reader proposals or open briefs
  still have ideas.
- *A consecutive-refusal counter at the 5a gate* (E-032's sketch) belongs to the retired
  family-grain design (E-036 Decision 1: no NEIGHBOUR tier).
- *The "Queue exhausted" branch of `process_once`* makes no decision record. Consequence to
  accept: a campaign that already stopped and is relaunched with an empty queue does not
  dispatch; the operator registers a brief, or raises the budget before the stop.

Flag-off identity: `decide()` adds the `r3` key to `rules` only when the flag is on (the
pattern `inputs.feed_set_sha256` already uses, L1726-1728), so a flag-off decision record is
byte-identical.

---

## 3. The output contract

### 3.1 The carrier: a brief, exactly like the manual path

What the registration contract already accepts, verified:

- `register_hypothesis` (`run_campaign.py:545-611`) parses the brief's frontmatter
  (`_parse_brief_frontmatter`, L351 on, which requires `venue`/`product`) and appends a queue
  entry; `extra` may only carry `_REGISTER_EXTRA_KEYS = {origin, proposal_ref, card_ref,
  decision_ref, brief_status, parked_reason}` (L539-540).
- `origin: external` is already a valid value (`tools/record_schema.py:133`).
- decide_next treats it as an operator entry (`_OPERATOR_ORIGINS = (None, "external")`,
  `decide_next.py:132`): picked first by priority, never scored. An operator-origin entry
  **without** `brief_status` is a legacy brief (`is_legacy_brief`, L603-606): it never
  triggers R2 and gets the one-time `[obsolete]` title tag. So an automated external entry
  must be registered with `brief_status: open` — the same thing `_register_from_cli` already
  does for operator briefs under decide_next (L3527-3533). R2 can then ask 1a for more
  hypotheses from that external brief, up to the usual limit.
- The closest precedent is the campaign-review reframe: an LLM writes a brief file, and
  `_register_campaign_review_reframe` (L3496-3524) registers it with
  `source="agent", relation=None, extra={"origin": "campaign_review"}, status="ready"`,
  priority `AGENT_PRIORITY`. The external writer should mirror it exactly, with
  `extra={"origin": "external", "brief_status": "open", "decision_ref": ...}`.
- `_materialize_run` (L413-526) copies every frontmatter key except `machine_constraints`
  into `research_brief.yaml` (L418), writes `pre_registration.yaml` from
  `machine_constraints`, and honours `criteria_from: hypothesis_generation` (L473-485) so the
  criteria are written at 1a from the menu (E-059 decision 2). An external brief uses that
  same marker; it never carries a `pass_rule`.

### 3.2 The brief the dispatch writes

Frontmatter = the operator's template (guess 3: `strategy_domain`, `market_universe`,
`timeframe`, `venue`, `product`, `research_goal`, `machine_constraints`) plus:

```yaml
criteria_from: hypothesis_generation        # 1a writes criteria from the menu
external_source:                            # provenance, copied unchanged downstream
  kind: model_knowledge | paper | forum | web_page
  citation: "<authors, title, venue>"      # model_knowledge: the claim, as recalled
  url: <url or null>
  published: <ISO date or null>             # must be < holdout_range start when known
  sample_period: [<start>, <end>] | null    # the data the source itself studied, if stated
  retrieved_at: <UTC timestamp of the dispatch>
  retrieved_by: {model: <model id>, web_access: false|true, dispatch_ref: <log row>}
external_mechanism:                         # mirrors hypothesis-design's edge_source block
  category: <one of the five edge_source categories>
  specific_mechanism: "<causal chain, prose, no parameters>"
  counterparty: "<who pays us, and why they keep paying>"
  why_not_arbitraged: "<per the category's bar>"
  measurable_proxy: "<the observable that separates mechanism present vs absent>"
  evidence_type: <a feed name from available_feeds / FEED_REGISTRY>
  requires_new_feed: <feed name, only when evidence_type is not wired>
  bot_mapping: forecast | regime_detection | regime_strategy_mapping
```

The `external_mechanism` fields are the `edge_source` block of
`workflow_artifacts/skills/hypothesis-design/SKILL.md` (L48-58: `category`,
`specific_mechanism`, `why_not_arbitraged`, `evidence_type`, `measurable_proxy`,
`requires_new_feed`) plus two: `counterparty` (the project's "who is on the other side"
question) and `bot_mapping` (the epic's "re-expressible in forecast → allocation, regime
detection, regime→strategy mapping"). 1a therefore receives, in the brief it already reads,
the exact block its A1.1-A1.3 rules check — the same anti-confabulation bar as an internal
idea, not a parallel one. There is **no numeric field** anywhere (guess 5).

### 3.3 Where source and date survive

| Hop | Today | S2 change |
|---|---|---|
| Brief file (`campaign_record/external_briefs/<id>.md`) | — | written by the dispatch; tracked like the rest of `campaign_record/` |
| Queue entry | `origin`, `brief_path`, `decision_ref` | none beyond the existing keys |
| `research_brief.yaml` | `_materialize_run` copies all frontmatter keys (L418) | none |
| `hypothesis_card.yaml` (every card 1a writes, incl. extra cards) | card has no provenance field | skill text: copy `external_source` verbatim; code check after 1a (the seam `_write_pass_rule_from_card`, L5383, already re-checks identity fields) fails loud on a mismatch or omission |
| `campaign_record/campaign_memory.yaml` | `build_memory_entry` (`tools/campaign_memory.py:497-565`) reads the card; the schema is closed (`campaign_memory.schema.json`, `additionalProperties: false`) | new optional entry field `external_source` (schema-additive; absent for every other run) |
| Trial rows (`campaign_state.trial_sharpes`) | `trial_id` = `run_id` or `run_id:variant` | **none**. Linked through the memory entry's `trial_ids`; the row shape stays what E-025's union merge and `deflate_sharpe.py` expect |
| Decision record + `external_dispatches.yaml` | — | R3 record; one log row per dispatch (model, web_access, turns, cost, every query/URL from the PreToolUse hook, lint result, registered entry or data-request row) |

### 3.4 E-032 S1 Task 4, checked against today's code

| E-032 Task 4 claim | Status |
|---|---|
| "Zero network/tool access … `allowed_tools=[]` confirmed" (L408-415) | **Wrong.** §1.1-1.2. Now at L939-942 and a second site L3049-3050 |
| "No schema shape for imported from outside; no `source`/`date` fields" (L416-418) | **Mostly still true.** IMPROVEMENT 08's pass-through `candidate` carries a `source` (hypothesis-design SKILL L382-396), but only for a complete config+manifest+criteria candidate, and with no date. `origin: external` now exists on the queue |
| `edge_source.category` closed 5-value enum; A1.3 is the right control (L418-425) | **Valid.** The external shape reuses that block (§3.2) |
| "A separate dispatch, not a loosened stage" (L429-435) | **Valid** |
| Trigger = "anti-adjacency gate REFUSED N consecutive proposals" / "zero admissible candidates from Layer 1/2" (L436-442) | **Stale.** Layer 1 is advisory only and NEIGHBOUR is gone (E-036 Decision 1, 4). Replaced by decide_next's stop → R3 (§2) |
| Mechanisms not fitted rules; `source` + `date`; era-stability bar uses the date (L443-452) | **Valid.** The era bar is now the menu criterion `sign_consistent_by_era` (`config/criterion_menu.yaml:62-90`) |
| New artifact `external_knowledge_notes.yaml` feeding `hypothesis_generation` (L453-460) | **Superseded.** The target design enters outside ideas at Step 0 as briefs (the 2026-09-20 note on the manual path); the brief frontmatter is the carrier and no stage gets a new input. The firewall principle ("inspires, never decides") still holds |
| New stage `external_knowledge_search` with its own skill, tool grant, model tier (L461-469) | **Partly valid.** Own skill file and grant: yes. Not a pipeline stage in `STAGE_CONFIGS`/`run_loop`: a campaign-level dispatch at the decide-next stop, like the reframe registration. Model tier: guess 4 |

---

## 4. Guardrails

### 4.1 Mechanisms, not fitted rules

- **Shape** (static, cheapest): §3.2 has no numeric field; unknown keys are refused.
- **Lint** (new pure module, e.g. `tools/external_mechanism.py`, run by the caller before
  anything is written): refuses (a) keys outside the closed set; (b) a number next to a
  parameter word in any `external_mechanism` text (lookback, window, period, threshold,
  percentile, standard deviation, z-score, days/hours/bars, %) — dates and citations live
  only in `external_source`, which is exempt; (c) a `category` or `bot_mapping` outside its
  enum; (d) an `evidence_type` that is neither a wired nor a reserved feed
  (`decide_next.load_feed_set`, L386) — that goes to the feed lane (guess 9).
- **1a/1b**: 1a writes the card from the block under its existing A1.1-A1.3 rules; 1b writes
  parameters from the design guide, never from the source. Detecting that 1b copied a
  number from a paper is not reliably possible in code (the paper text is not kept); the
  controls are (b) above, the three variants, and the parameter-plateau bar. Stated as a
  limit, not solved.

### 4.2 Publication bias

`external_source.published` and `sample_period` are recorded (§3.3). The pass-rule check
after 1a (`_write_pass_rule_from_card` seam) refuses an external idea whose criteria omit
`sign_consistent_by_era`. The eras are `campaign_data_policy.yaml`'s list, keyed per window
by `evaluate_grid` (criterion_menu L86-90), so an effect present only in the author's sample
period shows as a sign change on the other eras. Guess 6.

### 4.3 Trial accounting — verified

Every backtest writes a trial row regardless of origin: the per-variant loop calls
`_record_backtest_trial(run_id, summary, variant_config_path, trial_id=trial_id)`
(`run_phase1_research.py:1527`, trial id `run_id:variant`); the legacy single-config path
calls it at L1883; every failure branch writes a `backtest_failed` row via
`_record_failed_backtest_trial` (L1452, 1483, 1496, 1516, 1530, 1700, 1711, 1857, 1886;
writer L8570-8642). Neither writer reads `origin` or the brief. So an external idea that
reaches `protocol_execution` gets its rows through the normal path with no new code. One
that is refused earlier (lint, 1a exhausted, 5a REPEAT, data parked) touched no market data
and correctly gets no row; its dispatch is still logged in `external_dispatches.yaml`.

### 4.4 Cost control

Knobs under `orchestrator.external_dispatch` in `config/campaign_config.yaml`:
`max_dispatches` (default 1, counted over `external_dispatches.yaml` rows — guess 7),
`max_turns`, `max_cost_usd` (enforced in code from `total_cost_usd`, §1.3), `model`,
`web_access` (default false), `allowed_domains`. The per-run weighted token budget
(`_load_token_budget`, L743-758) does not apply because the dispatch runs outside a run; its
tokens are logged with the same `_usage_token_record` (L899-916) so they are comparable.

### 4.5 Holdout safety

Four channels, each with its control:

| Channel | Control |
|---|---|
| The agent reads the sealed store | `tools` has no file tool; `setting_sources=[]`; empty `cwd` (§1.3). (The existing stages are the open channel today: guess 1) |
| The model's own training data covers the sealed window | pin a model whose published training-data cutoff is before the `holdout_range` start; S2 keeps an operator-maintained allowlist of such models and refuses any other (guess 4) |
| A cited source discusses the sealed window | `published` must be present and strictly before `holdout_range` start, read at runtime with `orch._load_holdout_range()` (L7049; deny-by-default, never a literal) — else refused |
| Search pages show post-seal text the agent never cites | not closable in code. Hence `web_access: false` by default (guess 4). When on: the PreToolUse hook logs every query and URL; the lint refuses any date or year token inside the sealed window anywhere in the output (the same date shape `tools/holdout_date_gate.sh` scans for, with bounds from `_load_holdout_range()`) |

And the output is checked before anything is written: a refused dispatch writes only its log
row.

---

## 5. Run budget: "1 externally-sourced idea reaching a grid verdict"

Needs, all on one machine that runs campaigns:

1. **Credentials**: whatever the existing stages use (the SDK drives the bundled Claude Code
   CLI with the operator's login or `ANTHROPIC_API_KEY`), plus the Gemini key env var that
   importing `run_phase1_research` already needs. With `web_access: true` later, web search
   must be enabled for that account. None of this exists in the environment this document
   was written in.
2. **Flags on**: `decide_next` and what it requires (`regroup_record`, `specialist_readers`,
   `grid_evaluation`, `category_reports`, `config_direct_authoring` —
   `run_phase1_research.py:3370-3382`, 2775-2785, 3328-3336); `variant_anti_adjacency_gate`
   (guess 8, itself after E-036 S2b's replay report); the two new E-035 flags (§6).
   `verdict_routing_retired` + `profit_bars_every_backtest` are recommended so the decide-next
   step is the only way on, but not required for R3.
3. **A live campaign that reaches the stop**: every brief exhausted, no eligible proposal.
   The cheapest honest way: run the queue down as usual; the first `no_eligible_candidate`
   decision fires R3, the external brief runs, and its `idea_status.yaml` from the grid is
   the proof. Record: the decision record with R3, the dispatch log row, the brief, the card
   and memory entry carrying `external_source`, the trial rows.
4. Guess 1's ticket landed first, or at minimum the local allow rule narrowed.

---

## 6. Proposed S2 split and flag design

**S2-0 (separate ticket, not E-035's flag; declared behaviour change):** close the book on
the existing stages — `tools=[]` and `setting_sources=[]` at L941 and L3050. Before/after on
one real run (`validation` loses its two reads; its skill must then receive
`campaign_data_policy.yaml`/`cost_model.yaml` through its handoff if it needs them). Fix the
`test_e056_1b_block_manifest.py:552` comment and E-032's measuring script claim.

**S2a — provenance and intake contract (works for the manual path; no API key needed):**
1. `tools/external_mechanism.py` (pure): the §3.2 shape, the §4.1 lint, the §4.5 date checks
   (bounds from `_load_holdout_range()`), feed classification via `decide_next.load_feed_set`.
2. `run_campaign.py register --origin external`: refuses a brief whose `external_source` /
   `external_mechanism` fail the lint; registers `origin: external` (+ `brief_status: open`
   under decide_next, as `_register_from_cli` does today).
3. `hypothesis-design/SKILL.md`: copy `external_source` verbatim into every card; use
   `external_mechanism` as the `edge_source` starting point under the same A1 rules.
4. Post-1a check (at the `_write_pass_rule_from_card` seam, extended to external briefs):
   provenance present and equal on every card; `sign_consistent_by_era` in the criteria.
5. `campaign_memory.py` + schema: optional `external_source` on the entry.
6. Flag `orchestrator.external_provenance.enabled` (strict bool via
   `_strict_orchestrator_flag`, L3406). Off: a brief carrying the keys is still copied into
   `research_brief.yaml` as today, but nothing is checked or propagated.

**S2b — the automated dispatch (R3):**
7. `decide_next.py`: R3 (§2), recorded only under the flag; budget read from
   `external_dispatches.yaml`.
8. `run_campaign.py`: on `picked.r3_external`, call the agent with the §1.3 options, parse
   YAML deliverables the way `run_claude_worker` does (L1004-1019), lint, then either write
   the brief from the operator template and register it (mirroring
   `_register_campaign_review_reframe`) or append a `data_requests.yaml` row via
   `_append_data_requests(..., dedupe=True, stage="external_knowledge")` (L4072) and stop;
   append the dispatch log row in every case.
9. `workflow_artifacts/skills/external-knowledge/SKILL.md`: return 1-3 mechanisms in the
   §3.2 shape; never parameters, never coins/timeframes/windows; cite a source for each.
10. Flag `orchestrator.external_dispatch.enabled` requiring `decide_next`,
    `variant_anti_adjacency_gate` and `external_provenance` (raise otherwise, the
    `_decide_next_enabled` pattern). Knobs per §4.4. Register entries in
    `feature_flag_register.yaml` as `off_incomplete`, `blocked_on`: the §5 run.
11. Docs: USER_GUIDE (campaign runner), RUNBOOK §3 row "R3 dispatched / refused / budget
    spent", DOC_INDEX; `external_dispatch.schema.json` for the log (documentation only, like
    `decision_record.schema.json`).

**Tests (system Python, no API key, no backtest):**
- Lint: accepts a clean mechanism; refuses each of: extra key, numeric-parameter prose,
  bad enum, missing or post-seal `published` (bounds from a sandboxed policy file, never a
  literal), in-window date token in any field; unknown feed → feed-lane classification.
- Options pinning: monkeypatch `query`/`ClaudeAgentOptions` (the pattern of
  `tests/test_e046a_slice5b_ii_b_review_fixes.py:288-294`) and assert the exact options —
  `tools == []` when `web_access` is false and exactly `["WebSearch","WebFetch"]` when true,
  `setting_sources == []`, `permission_mode == "dontAsk"`, `strict_mcp_config`, a fresh empty
  `cwd`, no file tool anywhere.
- Cost ceiling: a stubbed result over `max_cost_usd` / `max_turns` fails loud, writes only
  the log row.
- R3 in `decide()`: fires only on the would-stop path with the flag on and budget left;
  records `external_budget_spent` otherwise; never fires when a candidate, scheduled entry or
  open brief exists; flag-off decision record byte-identical (existing decide_next fixtures).
- Caller: stubbed agent → brief written from a fixture template, entry registered with
  `origin: external, brief_status: open`; unknown-feed mechanism → one `data_requests.yaml`
  row, no entry; lint refusal → nothing but the log row.
- Provenance: `_materialize_run` → `research_brief.yaml` carries it; post-1a check refuses a
  card without it and a pass rule without `sign_consistent_by_era`; memory entry validates
  against the extended schema; a non-external run's memory entry is byte-identical.
- CLI `register --origin external`: refuses an invalid block; flag-off CLI unchanged.
- Flags: strict bool, dependency refusals, register entries (`test_feature_flag_register.py`).
- Docs gate: `test_guide_covers_the_code.py`, `test_doc_anchors.py`.

Run budget: S2a 0; S2b the §5 run (one external idea to a grid verdict), after S2-0 and after
`variant_anti_adjacency_gate` is on.

---

## Files read (representative)

- `strategy-research/workflow/run_phase1_research.py` (L126-160, L743-1021, L2575-2600,
  L3042-3057, L3328-3460, L4072-4080, L5383-5392, L7049-7056, L8440-8642, trial call sites)
- `strategy-research/workflow/run_campaign.py` (L340-372, L413-611, L2545-2570,
  L3035-3158, L3440-3540)
- `strategy-research/tools/decide_next.py` (L1-175, L386-429, L1485-1742)
- `strategy-research/tools/record_schema.py` (L128-133, L224-233)
- `strategy-research/tools/campaign_memory.py` (L497-565),
  `workflow_artifacts/schemas/campaign_memory.schema.json`, `proposal.schema.json`
- `strategy-research/workflow_artifacts/skills/hypothesis-design/SKILL.md`
- `strategy-research/config/campaign_config.yaml`, `feature_flag_register.yaml`,
  `campaign_data_policy.yaml` (policy lines only), `criterion_menu.yaml`
- `strategy-research/tools/holdout_date_gate.sh` (header)
- `claude_agent_sdk` 0.2.82: `types.py` L1578-1840, `_internal/transport/subprocess_cli.py`
  L184-360, `client.py` L160-180; bundled CLI `--help`
- SDK session transcripts under `~/.claude/projects/…strategy-research/` (tool-use lines only)
- `runs/*/pipeline_state.yaml` (`num_turns` lines only)
