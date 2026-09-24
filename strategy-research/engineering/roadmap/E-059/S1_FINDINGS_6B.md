# E-059 S1 — Decide-next and the queue (delivery_plan_v26.md slice 6b): characterize-and-stop

Read-only characterization at `cf612f77` (master). No code, config or backtest changed; the
holdout was not opened. Line numbers are from that commit (re-grepped for this document with
Git Bash `grep -n` and read directly); function names are the stable reference. Pure-function
checks were run with system `python` 3.13.2 in a temp directory (no API key, no backtest).

Inputs read: `delivery_plan_v26.md` slice 6b (L345-373), rows "0 · idea intake" (L55),
"10 · decide next" (L67), "11 · queue" (L68), the E-059/E-031 rows (L501-502);
`engineering_roadmap.html` cards G, H, I, J, K, L, M, N and steps 10-11;
`roadmap/E-031/EPIC.md` (a pointer to Linear) and its `artifacts/s1_refill_sources.md`;
`roadmap/E-058/S1_FINDINGS.md` (6a design and operator decision).

---

## Guesses for the operator (read this first)

Each item is a real choice that the target design does not already make. The recommendation is
what S2 will build if you say nothing.

1. **Is a reader's patch a new idea or the same idea?** A reader proposes "change parameter X
   of idea A". The target says an idea's identity is its `hypothesis_id` and that another coin
   is only a variant. It does not say whether a *changed design* keeps the old id.
   *Recommendation:* the picked patch runs as a **new idea** with id
   `<parent hypothesis_id>__<proposal_id>`, and records its parent. Keeping the parent's id
   would give one id two different grid statuses (refuted, then maybe validated), and the
   single-use holdout is keyed on `hypothesis_id` (`_route_holdout_evaluation` L7811-7816), so
   the parent's earlier record could block the child.

2. **Where an agent candidate's pass criteria come from.** The grid reads its criteria only from
   `pre_registration.yaml`. That file is written when the idea is registered, **before** step
   1a runs, and a run under the readers flag refuses to start without it (§3.3). A reader
   proposal carries no criteria.
   *Recommendation:* every agent candidate inherits the source run's `pass_rule` and protocol
   pin (`machine_constraints`), recorded as `criteria_inherited_from: <run_id>`. This applies
   to patches and to forecast-block sketches. Menu criteria are scale-free and do not depend on
   the idea, so they carry over honestly. **Regime-block sketches are not runnable before slice
   7**, because a regime block is validated only as a composition variant (cards A/F). They are
   listed in the decision record as `infeasible: regime_block_needs_composition`.

3. **Use the exact-match repeat check now, or wait for slice 8?** The plan says "until slice 8,
   the family-grain digest, advisory only". But the exact check of card K (config hash +
   instrument + timeframe + window set) can already be computed for every new-design run: the
   campaign memory stores each variant's `forecast_hash`, `symbols`, `timeframe` and
   `protocol_ref`. Also, the digest's "family grain" does **not** read the retired
   `hypothesis_family`. It recomputes a family from the card (§5.1). Its fingerprint, however,
   ignores transforms, and most reader patches change a transform parameter. So on those patches
   the digest would say REPEAT when the config is actually different.
   *Recommendation:* the exact-match check is **binding now**, against memory entries only.
   Legacy runs can never produce a repeat, as slice 8.1 already states. The digest's layer 2 is
   recorded as **information only**. Its layer 1 (the KB reactivation machinery) is not called at
   all.

4. **Candidates with no scores.** Only reader proposals carry the three 0-3 scores. Nothing
   scores a brief the operator registered by hand, or a brief's extra hypotheses (card M).
   *Recommendation:* (a) a `ready` entry the operator registered by hand always goes first, in
   the existing priority order, with no scoring, because the operator chose it explicitly.
   (b) Step 1a writes the same three anchored scores on each extra card, using the same rubric
   with `model_id` and `rubric_version`. Under the rubric, an untested card usually scores
   `confidence_real` 0-1 ("story only"), so it ranks below evidence-backed proposals. That is
   what card I's anchors intend. Re-scoring when memory changes (step 11) is left for later.

5. **What waiting candidates are called in the queue.** Card M's extra hypotheses must wait in
   the queue without being picked automatically. `ready` is picked by the unchanged
   `_select_entry`. A `paused:` entry is picked up by `--resume` (`resume_paused_entry` takes
   `paused[0]`, L1416-1420) and would report "inconsistent state" because it has no runs.
   *Recommendation:* add one status token, `queued`, to `_QUEUE_STATUS_RE` (L107). The
   alternative with no schema change is `blocked_on_decide_next`. It also works, but the
   schedulability file then reports these entries as *blocked*, with dwell days.

6. **Stopping endless refinement of one idea.** Readers propose patches on every run, so the
   queue may never empty and the loop can keep patching one idea. The per-family circuit breaker
   is retired, and card G says circuit breakers "become queue policies" without naming one.
   *Recommendation:* count the runs descended from the same root idea (following `proposal_ref`
   through the memory). From the 4th such run on, that root's patch candidates rank **below every
   other eligible candidate**. They are demoted, never refused, and the decision record says so.

7. **Old briefs and the "ask for more hypotheses" rule (R2).** The five existing queue entries
   have no brief status.
   *Recommendation:* an entry with no `brief_status` is legacy and never triggers R2, so turning
   the flag on never spends API calls on old briefs. Briefs registered while the flag is on
   start as `open`.

8. **A bug found: a finished run crashes the campaign runner.** When a run ends
   `completed_rejected`, `process_once` writes `outcome: completed_rejected` with no evaluation
   reference (L2371-2373). `_save_queue` then refuses the whole queue file: the provenance gate
   raises `UngatedVerdictError`. This was reproduced with `validate_verdict_provenance` on a
   synthetic entry (§4.4), and `tests/test_loop_health_instrument.py:328-330` avoids that
   outcome on purpose. The same holds for `completed_promoted`. Slice 6b's two-run proof would
   hit this on its first refuted run.
   *Recommendation:* under the flag, the DONE branch writes `outcome: <idea_status>` with
   `pass_rule_evaluation_ref: runs/<id>/artifacts/idea_status.yaml` (verified admissible, §4.4).
   With the flag off, the bug stays as it is. Fixing that path needs its own small ticket,
   because it changes flag-off output.

9. **Extra hypotheses keep their card.** Today a brief's cards 2..k become child runs right away,
   and those runs skip step 1a.
   *Recommendation:* under the flag, cards 2..k are saved and enqueued with a new `card_ref`
   field. When one is picked, its run starts after 1a with that card, as today's split does, so
   no second 1a call is spent and the card does not drift. This adds one field beyond the
   plan's four.

Already answered by the target, so not asked: idea status comes only from the grid; scores
only rank (they are recorded in the decision record, never in memory, never in the route);
refine/pivot/escalate/kill, the family circuit breaker, `hypothesis_family`, `altitude_history`
and continuation children are neither read nor rebuilt; R1 is a no-op until slice 7; another
coin is a variant; the operator can add a brief at any time; `_select_entry` is unchanged;
routing is unchanged until 6c; the cost tie-break is the cheapest.

---

## 1. The queue today

### 1.1 `config/campaign_queue.yaml`
Top level `{version, created_at, queue: [...]}`. There are 5 entries (read with system python;
`notes` lengths omitted):

| id | status | source | relation | run_ids | outcome / verdict_status |
|---|---|---|---|---|---|
| P4_ts_trend | blocked_on_daily_bar_ingest | user_delivered | refine | run_053, 054, 057 | ungated_… / ungated |
| XS_momentum | done | agent | — | research_path_… | ungated_… / ungated |
| H-041-C-v2 | done | operator_ratified | new_registration | run_058 | stage_discretion_… |
| FUNDING_MR_DAILY_RETEST | done | operator_ratified | new_registration | run_059 | completed_rejected / gated + `pass_rule_evaluation_ref` |
| FUNDING_MR_4H_RETEST | done | operator_ratified | new_registration | run_060 | ungated_… / ungated |

No entry is `ready` or `in_progress`. `campaign_state.hypothesis_splits` is absent, meaning
the multi-card split has never fired in the live state. There are 15 `trial_sharpes` rows.
`campaign_record/` has no `campaign_memory.yaml`, `block_registry.yaml`,
`component_requests.yaml` or `data_requests.yaml`. No run under `runs/` (60 dirs) has
`idea_status.yaml` or `proposals/`, so decide_next has **no real input on disk yet** and
S2 testing is fixture-only (same situation as E-058 S1 §8).

### 1.2 `tools/record_schema.py`
- `_QUEUE_STATUS_RE` L107: `^(ready|done|in_progress|superseded|paused:.+|blocked_on_.+)$`.
  `paused:waiting_for_component|data` already match (the plan is right). `queued` does not
  (guess 5).
- `_RELATION_VALUES` L116-119 (`new_registration, refine, reframe, escalate, pivot, split,
  reactivation`), `_SOURCE_VALUES` L120 (`agent, operator_ratified, user_delivered`).
- `QUEUE_ENTRY_SCHEMA` L199-209 is closed. It holds `id, brief_path, notes, status,
  priority, source, relation, run_ids, outcome, verdict_status, verdict_status_basis,
  verdict_void_reason, pass_rule_evaluation_ref, refinement_brief_path,
  refinement_brief_consumed_for`. Any other key raises (`validate_record_schema` L340-366).
  Every string value is also checked against the bare-verdict-token rule (L126-128), so an
  `origin` or `parked_reason` value such as `refine_…` would be refused. The new vocabularies
  must avoid tokens that start with kill/promote/refine/pass/fail.
- The whole list is validated on every write (`_save_queue` L131-137,
  `validate_verdict_provenance(..., schema=QUEUE_ENTRY_SCHEMA)`).

### 1.3 `register_hypothesis` (`run_campaign.py:402-445`) — the single writer
Signature `register_hypothesis(brief_path: Path, priority: int, notes: str) -> int`. It parses
the brief with `_parse_brief_frontmatter` (L235-271, which requires `strategy_domain,
market_universe, timeframe, research_goal, venue, product`, L265-270). The id is the file stem
(L418), and a duplicate id is refused (L421-423). The entry fields are hard-coded (L431-440):
`status: ready, source: operator_ratified, relation: new_registration, run_ids: []`.
**Callers:** the CLI (`run_campaign.py:2529`) and four tests
(`tests/test_k3_protocol_pinning.py:883-950`, which pin the field set). There are no other
code callers (grep over `workflow/`, `tools/`, `tests/`).
Consequences for 6b: (a) `source: agent` and `origin` need parameters; (b) an R2 "1a
request" and a brief's sibling entries share the brief file, so the stem-derived id collides.
**Change:** keyword-only `entry_id=None, source="operator_ratified",
relation="new_registration", extra=None` (defaults keep the CLI and the four tests
byte-identical). `extra` is limited to the new schema keys.

### 1.4 `_select_entry` (L153-165) and `_next_action_for_entry` (L168-185)
The first `in_progress` entry wins, otherwise the lowest `priority` among the `ready` entries.
`paused:*`/`blocked_on_*`/`done` are never picked. The action is `refinement_brief` |
`fresh_launch` (no `run_ids`) | `continue`. `_select_entry` stays unchanged. The pick is
honoured by an invariant rather than a selector change (§3.1). `_next_action_for_entry` gains one
action, `queued_card` (entry has `card_ref` and no `run_ids`; guess 9).

### 1.5 `process_once` (L2142-2379) and where decide_next goes
Order: `reconcile_orphans` → schedulability → `_select_entry` (L2157), where `None` means "Queue
exhausted" and the function returns False (L2158-2160) → action → `orch.run_loop` (L2225) →
split detection (L2224-2241) → `_hard_pause_reason` (L2246) halts or quarantines → the
continuation branch (L2354-2369) → **DONE** (L2371-2379: `status: done`, `outcome = pending`,
save, summary, loop health).

**Slot:** inside the DONE branch, after the entry is saved, and only when the flag is on. Call
`decide_next` there, apply its result (append or flip a queue entry, write the decision record),
log it, then `return True`. When the decision is `stop`, log it and `return False`. The top of
`process_once` stays unchanged: operator `ready` entries are picked there as today.

### 1.6 `continuation_child` under the flag, without 6c
`continuation_child` is written only by `_route_refine` (L5792), `_route_pivot` (L5852),
`_route_escalate` (L5908, L5929) and `_route_kill`'s legacy branch (L5975, value None). The flag
requires `regroup_record`, which requires `specialist_readers`. Under those flags the only route
is `determine_post_specialist_readers_route` (L3123-3172). It dispatches only
`(promote, None)` or `(kill, terminate)`, and `_route_kill`'s flag branch (L5957-5969) returns
before writing any continuation field. Campaign review is also unreachable, because its trigger
sits only in `determine_post_verdict_route` (L8396). **So a flag-on run can never
set `continuation_child`**, and the continuation branch (L2356) cannot fire for one. "Ignoring
`continuation_child`" therefore needs no code: decide_next sits in the DONE branch, which is
reached only after the continuation branch has fallen through. A test asserts that a flag-on run
never carries the key. No 6c work is pulled forward.

## 2. What decide_next can and cannot see before 6c (plan question 7)

Under the prerequisite flags, the stage after `regroup_record` is (run_loop L9502-9518):

| grid / branch-3 outcome | route today | queue effect | decide_next runs? |
|---|---|---|---|
| component error | `human_pause` (component_execution_error) | `paused:…`, loop halts | no |
| profit bars passed | `human_pause` (profit_bars_reached, `_profit_bars_stop_route` L7733) | halts | no (runbook: resume re-enters the route) |
| inconclusive | `human_pause` (inconclusive_grid) | halts | no (6c parks instead) |
| refuted | `_route_kill` → `completed_rejected` | DONE | **yes** |
| validated | promote → `holdout_evaluation` (`_route_holdout_evaluation` L7772) | DSR False → `completed_rejected` (L7804-7807) → DONE; otherwise research-only hold or awaiting holdout → halt | yes only on the DSR-blocked path |

So **before 6c, decide_next fires only after a refuted idea (or a validated idea blocked by the
deflated-Sharpe gate)**. Every other outcome halts the loop as today. 6b changes no route; the
route still dispatches promote/kill. The two-run proof in the plan therefore needs a first run
that ends refuted. decide_next reads the idea's status from **memory** (`idea_status`), never
from `pending_stage`: a validated idea that is DSR-blocked is recorded as `validated`, and its
`completed_rejected` stage is a routing artifact.

## 3. From a proposal to a runnable queue entry (plan question 2, the core design)

### 3.1 The invariant that makes `_select_entry` honour the pick
- An operator-registered `ready` entry (no `origin`, or `origin: external`) always exists
  **before** any agent candidate is considered. decide_next then picks nothing and records
  `picked: operator_entry <id>`, so `_select_entry` picks by priority exactly as today (guess 4a).
- Otherwise decide_next writes **exactly one** agent entry with `status: ready` (priority 999, so
  a hand-registered entry added in between still wins). Every other waiting agent entry is
  `queued` (guess 5). There is then only one `ready` entry, and the unchanged selector must pick it.

### 3.2 What a proposal is today
`tools/reader_proposals.py` (L24-28, L50-95):
`{proposal_id: <category>-<run_id>-<n>, kind: patch|new_block, patch | block, evidence,
scores{confidence_real, distance_to_profitable, mechanism_plausibility} ∈ 0..3, model_id,
rubric_version}`.
- `patch` items are `{component_id, field, before, after}`, where `field` is a dotted path
  inside the component (the reader skill's own example is `transforms[2].params.min_abs`).
  This is **not** the `{path, value}` JSON-pointer shape of `variant_patches.yaml` that
  `_apply_json_pointer_patch` (L8716) consumes.
- `new_block.block` is `{kind: forecast|regime, config_paths, scaffolding, rationale}`. It is a
  sketch in manifest vocabulary with **no config values and no class**. The reader skill says so
  ("you are not writing block_manifest.yaml, and no code registers it").

### 3.3 The pass-through contract a candidate must meet (slices 1/3)
- `hypothesis-design/SKILL.md` IMPROVEMENT 08 (L383-396): if `research_brief.yaml`, or a
  `candidate` block inside it, carries **all four** of `config, manifest, criteria, source`,
  then 1a copies them verbatim into the card with `pass_through: true`. A partial candidate is
  authored normally.
- `strategy-config-authoring/SKILL.md` L95-104: on `pass_through: true`, 1b copies `config` to
  `backtest_spec.yaml.config` and `manifest` to `block_manifest.yaml`, and still validates them.
- `_materialize_run` (L298-391) copies every frontmatter key except `machine_constraints` into
  `research_brief.yaml` (L303-310), so a `candidate:` key reaches 1a unchanged. It writes
  `pre_registration.yaml` **only if** the brief has `machine_constraints` (L312), taking
  `pass_rule` from `evaluation.pass_rule` (L323, L334).
- The readers flag's preflight (`_check_specialist_readers_preflight` L2768, called at L8958)
  fails the run **before any spend** unless `pre_registration.yaml` exists with a menu-shaped
  pass_rule. The grid reads its criteria from that file (L1581-1632), **not** from the card's
  1a `criteria`. That is why guess 2 exists.
- Pass-through is prompt-level: an LLM copies the config. It is cheap to verify, since the
  decision record stores the expected base-config hash, and the `backtest_specification` tool
  stage can compare it with `_compute_forecast_hash` (L6026) of `artifacts/variants/base/
  strategy_config.json` and stop loudly on a mismatch. This check is in the S2 list.

### 3.4 Kind `patch` → runnable candidate (concrete)
decide_next (pure) resolves the patch, and the caller writes the brief:
1. **Source config:** the source run's base variant, `artifacts/variants/<base>/strategy_config.json`
   (base id via `tools/json_pointer.base_variant_id`), or `candidate_strategy_config.json` when
   the variant loop is off.
2. **Resolve each item:** find `component_id` under `/strategies/regimes/*/components/*` and
   `/regime_detector/components/*`. Exactly one match is required; zero or several makes the
   candidate `infeasible: patch_unresolvable`. Convert the dotted `field`, with `[i]` giving list
   indexes, to a JSON pointer. The current value must equal `before`, otherwise the candidate is
   `infeasible: stale_before`. The item then becomes `{path, value: after}`, which is applied with
   the same semantics as `_apply_json_pointer_patch`. (That function should move to
   `tools/json_pointer.py`, as E-058 S2b did for its siblings, so the pure module can import it
   without the orchestrator.)
3. **Manifest:** the source run's `block_manifest.yaml`, with its paths re-checked on the patched
   config (`tools/json_pointer.manifest_missing_paths`). A missing path makes the candidate
   infeasible.
4. **Criteria and windows:** the source `pre_registration.yaml` `pass_rule` and
   `machine_constraints` (guess 2).
5. **Brief file**, written by the caller to `campaign_record/candidate_briefs/<entry_id>.md`
   (tracked, like the rest of `campaign_record/`). Its frontmatter copies `strategy_domain,
   market_universe, timeframe, research_goal, venue, product` from the source
   `research_brief.yaml`, sets `research_goal` to the proposal's evidence summary, and adds
   `machine_constraints`, `evaluation.pass_rule`, and
   `candidate: {config, manifest, criteria, source: {origin: reader, proposal_ref, source_run,
   parent_hypothesis_id, hypothesis_id: <parent>__<proposal_id>}}`.
6. **Register:** `register_hypothesis(brief, priority=999, notes=…, entry_id=<proposal_id>,
   source="agent", extra={origin: reader, proposal_ref: runs/<run>/artifacts/proposals/
   <cat>.yaml#<proposal_id>, decision_ref})`. It then enters at 1a like any brief (card N).
   Step 2 still writes the design and asset variants over the patched base.

### 3.5 Kind `new_block`
- `block.kind: regime` → infeasible before slice 7 (guess 2).
- `block.kind: forecast` → not a pass-through: there is no config. The brief carries the
  sketch plus evidence as `research_goal` text, together with the inherited
  `machine_constraints`/`pass_rule`. 1a and 1b author normally, so the full LLM cost applies.
  There is no exact-match check before 5a (no config yet); novelty is advisory only.

### 3.6 Duplicates (card I: "two readers proposing the same block collapse")
For patches, candidates whose resolved config hash is identical collapse into one candidate with
`collapsed_sources: [...]`, keeping the highest score tuple. new_block sketches collapse only on
identical `config_paths` + `kind` from the same source run.

### 3.7 Which proposals are still candidates
The pool is every proposal referenced by a memory entry (`runs.<id>.proposals[*]`, E-058
schema). A proposal leaves the pool when a queue entry's `proposal_ref` names it. It is never
removed for failing a gate: it is re-evaluated on every call, because feasibility can change once
a component exists (card J). Memory entries with `engineering_fault` have no proposals.

## 4. Gates computable from today's artifacts (plan question 4)

### 4.1 Novelty
- **Exact match (card K), from memory:** key = `(forecast_hash, sorted(symbols), timeframe,
  protocol_ref)` for every tested variant in `campaign_memory.yaml` (`variants.<vid>` carries
  `forecast_hash, symbols, n_windows`; the entry carries `timeframe`, `protocol_ref`;
  `tools/campaign_memory.py` L287-307, L500-501). A patch candidate's key uses the hash of its
  patched base config (same canonicalisation as `_compute_forecast_hash`, `json.dumps(...,
  sort_keys=True)`) with the source run's symbols, timeframe and protocol. Equality means
  REPEAT: binding, per guess 3. Legacy runs are not in memory, so they can never be matched.
- **Digest (advisory):** see §5.1.

### 4.2 Feasibility
- Patch resolves (§3.4); the manifest still resolves; each `class` in the patched config is in
  the known component set. The caller passes that set in, taken from
  `strategies.strategy_components` in the same way 5a checks it. A patch rarely changes
  `class`.
- Data: a patch keeps the source's symbols, timeframe and windows. If the source's base variant
  passed its data gate (`artifacts/variants/<vid>/data_availability_gate.yaml`, `outcome:
  validate`), the candidate is feasible. For a brief sibling, feasibility is `unknown`, which
  does not block: step 3's gate stays binding.
- `campaign_record/component_requests.yaml` (writer L2049-2056) and `data_requests.yaml`
  (L1336-1342) are append-only lists of `{run_id, stage, variant_id, reason, …}`. They carry
  **no class name and no resolution field**, so they cannot say whether a request has been
  resolved. They are counted into the decision record as information; the binding check is
  re-resolving the candidate itself.

### 4.3 R1 and R2
- **R1:** `block_registry.yaml` has `revision` and `updated_at` (`tools/block_registry.py`
  L83, L244-245). Nothing records "the last composition revision", because composition runs do
  not exist. The record says `{registry_revision, last_composition_revision: null, would_fire:
  revision >= 2, fired: false, reason: "composition brief writer is slice 7"}`, which lets you
  observe when slice 7 would first fire.
- **R2:** fires when no operator `ready` entry exists and no agent candidate is eligible. For
  each entry with `brief_status: open` and no outstanding request, it enqueues a 1a request
  `{entry_id: <brief_id>__more_<n>, brief_path: same, origin: brief}`. One request is made
  `ready`, and the rest are `queued`. The loop stops (`return False`, logged) only when no entry is
  `open`. **Exhaustion needs a signal that does not exist:** a hypothesis_generation that writes no
  card fails today (`FileNotFoundError`, L9156-9161). S2b adds `artifacts/brief_status.yaml
  {brief_status: exhausted, reason}` as a valid 1a output with no card, a terminal stage
  `completed_brief_exhausted`, and the owning entry flipped to `exhausted`. That outcome must be
  added to `_NON_VERDICT_OUTCOMES` (`verdict_criteria_evaluator.py` L109), because today it is
  refused as verdict-bearing (§4.4). 1a also receives the list of hypothesis ids already produced
  from this brief, through a flag-gated handoff context in the `_apply_regroup_record_context`
  pattern (L3379).

### 4.4 Checks run for this document (system python, temp dir)
- `validate_verdict_provenance(entry, schema=QUEUE_ENTRY_SCHEMA)` on `{outcome: X}` with no
  ref: `completed_rejected`, `completed_promoted`, `completed_validated`, `completed_refuted`,
  `completed_brief_exhausted` and `human_pause` all raise `UngatedVerdictError` (guess 8).
- With `pass_rule_evaluation_ref: runs/run_061/artifacts/idea_status.yaml` (file `result:
  FAIL`, under the entry's own run): `refuted`, `validated` and `completed_rejected` pass.
  `inconclusive` passes with no ref.
- Existing tests: `python -m pytest tests/test_schedulability_block.py
  tests/test_c7ext_r2_closed_schema.py tests/test_feature_flag_register.py
  tests/test_loop_health_instrument.py tests/test_halt_quarantine_policy.py` gives 93 passed.

## 5. Plan questions 3 and 1-point-5: cost, and the "family grain" digest

### 5.1 The digest's family grain, exactly
`tools/build_exclusion_digest.py::classify_family` (L112-160) derives the family **from the
card**, in order: `library_lookup.indicator_id`, `edge_source.evidence_type ==
fear_and_greed`, a keyword table over `hypothesis_id + edge_source.specific_mechanism +` the first
sentence of the thesis, otherwise `unclassified:<id>`. It **does not read `hypothesis_family`**.
The remaining dependencies on retired machinery:
- `failed_families_passthrough` (L474) is built from `campaign_state.failed_families`, which is
  written by `record_pivot` (retired). The gate only uses it as a "weak prior" flag and never
  refuses on it (`anti_adjacency_gate.py` L446-463).
- Layer 1 (`layer1_kb_check` L292) uses the KB reactivation clauses and
  `_lineage_routing_of_run` (L218), which reads `pass_rule_evaluation.yaml.lineage_routing`,
  the retired routing vocabulary.
- `composition_fingerprint` (L227-275) deliberately excludes `transforms`, so a patch to
  `transforms[i].params` produces a fingerprint identical to its parent's, and layer 2 returns
  REPEAT for a config that is different. The sketch kind has no card, so its family would be
  the parent's.

**Target-consistent interim** (guess 3): call only `layer2_digest_check`, with the source run's
card and the resolved config, and record `{outcome, family, family_confidence, run_ids}` as
information. Never refuse on it, and never call layer 1. Binding novelty is the memory exact match.

### 5.2 Cost estimate
E-039's measurement (`roadmap/E-039/S1_FINDINGS.md` L113-121): **median ≈ 3m45s for a clean
22-backtest (11 windows × 2 symbols) local-cache 1h protocol**, range 3m39s-3m53s over
3 runs, i.e. **≈ 10.2 s per window-symbol backtest**. It is a per-protocol median, and the
per-backtest figure is derived from it. Long-lookback protocols ran at 15-16 s per backtest and
failed outright on 2 of 4 attempts (L119-140). No other per-backtest median exists (grep for
`3m45`/`per-backtest` across `engineering/`, `tools/`, `config/`, `docs/`).
**Proposal:** `cost.backtests = n_windows × n_variants × symbols_per_variant`, where `n_windows`
and `symbols` come from the source run's memory entry, `n_variants = 3` (card D), and a sibling's
`n_windows` is counted from its brief's pinned protocol file (if it cannot be resolved, the cost
is null and ranks last). `cost.seconds_estimate = backtests × 10.2` with the basis cited. The rank
uses `backtests`: a single constant cannot change the order, so no "slow class" is modelled.

### 5.3 Ranking
The key is `(policy_demoted asc [guess 6], confidence_real desc, distance_to_profitable desc,
cost.backtests asc, candidate_id asc)`. The last element makes the order total and
deterministic. `mechanism_plausibility` is recorded but not ranked on, following the plan's key.

## 6. Multi-hypothesis briefs (plan question 5)

Today (`run_phase1_research.py:5581-5648`, called only at L9156-9161 when 1a's
`hypothesis_card.yaml` is missing): card 1 becomes this run's card, and each extra card is
scaffolded as a sibling run with `pending_stage: innovation_expansion` (L5636). The split is
appended to `campaign_state.hypothesis_splits`. `process_once` diffs that list around
`run_loop` (L2224-2241) and adds an `in_progress` entry per child through
`_add_queue_entry_for_split_child` (L1553-1569). That function writes the queue directly,
bypassing `register_hypothesis`, and marks every child `in_progress` so that it runs next.

**Latent bug (flag-off, `config_direct_authoring` on):** the sibling's hard-coded
`innovation_expansion` skips `strategy_config_authoring`, which run_loop inserts after 1a under
that flag (L9187-9188). Separate ticket; 6b does not create siblings under its flag.

**Under the flag:** the orchestrator must not import `run_campaign` (circular: `run_campaign`
imports `orch`). So `_handle_hypothesis_generation_multi_card_split` copies cards 2..k to
`campaign_record/queued_cards/<run_id>/hypothesis_card_<n>.yaml` and records them in
`artifacts/queued_hypotheses.yaml`. It scaffolds no run and writes no `hypothesis_splits` row.
`process_once` reads that file after `run_loop`, in the same place as today's split detection,
and enqueues each card through `register_hypothesis` (`entry_id: <brief_id>__h<n>`,
`origin: brief`, `card_ref`, status `queued`). It also sets the owning entry's `brief_status:
open` if it is unset. When a `queued_card` entry is picked, the launch materializes the brief
(pre_registration included), copies the card, and sets `pending_stage` to the stage after 1a, as
run_loop would (`strategy_config_authoring` under config_direct, otherwise
`innovation_expansion`).

## 7. Queue fields (final proposal)

| field | shape | written by | notes |
|---|---|---|---|
| `brief_status` | closed `open\|exhausted` | register (open), DONE branch on `completed_brief_exhausted` | only on the entry that owns the brief; absent = legacy (guess 7) |
| `origin` | closed `brief\|reader\|composition\|campaign_review\|external` | register | `composition`, `campaign_review` unused until slices 7 / 6c |
| `proposal_ref` | REF `runs/<id>/artifacts/proposals/<cat>.yaml#<proposal_id>` | register | pool exclusion (§3.7) |
| `parked_reason` | TEXT | 6c | added now, unused; values must pass the token rule |
| `card_ref` | REF | register | guess 9 (beyond the plan's four) |
| `decision_ref` | REF to the decision record that minted or picked it | register | audit trail (beyond the plan's four) |
| status `queued` | `_QUEUE_STATUS_RE` token | register, decide_next | guess 5 |

`relation` is omitted on agent entries, because its vocabulary is the retired routing words.
`_SCHEDULABILITY_NON_BLOCKED_STATUSES` (L1895) gains `queued`.

## 8. `decision_record.yaml` — proposed schema

It is written to `runs/<finished_run>/artifacts/decision_record.yaml` (the plan's
`artifacts/decision_record.yaml`, keeping one per decision). A `DECIDE` line is added to
`campaign_log.md`. Documentation only: `workflow_artifacts/schemas/decision_record.schema.json`.

```yaml
schema_version: 1
decided_at: <utc>
trigger: {after_run: run_061, after_entry: X, idea_status: refuted}
inputs:            # reproducibility (card H: "decision reproducible from disk")
  memory_sha256: …
  registry_revision: 0
  queue_sha256: …
  known_component_classes_sha256: …
rules:
  r1: {registry_revision: 0, last_composition_revision: null, would_fire: false,
       fired: false, reason: "composition brief writer is slice 7"}
  r2: {fired: false, open_briefs: [...], enqueued: []}
operator_entries: []       # non-empty -> picked is the first, no ranking
candidates:                # every candidate considered, final rank order
  - candidate_id: profitability-run_061-1
    origin: reader | brief
    kind: patch | new_block | card
    source_run: run_061
    parent_hypothesis_id: FOO
    proposal_ref: runs/run_061/artifacts/proposals/profitability.yaml#profitability-run_061-1
    collapsed_sources: []
    scores: {confidence_real: 2, distance_to_profitable: 1, mechanism_plausibility: 2,
             model_id: …, rubric_version: …}
    resolved_config_sha256: … | null
    gates:
      novelty: {exact_match: NOVEL | REPEAT, matched_runs: [],
                digest_advisory: {outcome: novel|neighbour|repeat, family, family_confidence,
                                  run_ids: []}}
      feasibility: {result: FEASIBLE | INFEASIBLE | UNKNOWN, reasons: []}
    policy: {root_hypothesis_id: FOO, descendant_runs: 1, demoted: false}
    eligible: true
    cost: {backtests: 24, seconds_estimate: 245,
           basis: "8 windows x 3 variants x 1 symbol x 10.2 s (E-039 S1 L113-121)"}
    rank: 1
picked: {candidate_id: …, queue_entry_id: …, brief_path: …, why: "<mechanical sentence>"}
        | {operator_entry: <id>} | null
stop: null | {reason: all_briefs_exhausted}
```
The record **never** contains `hypothesis_family`, `altitude`, `lineage_routing`,
`hypothesis_verdict` or `continuation_*`. A test reuses `campaign_memory.RETIRED_FIELDS` (L85).
Scores appear here only; they never enter memory or the route.

## 9. Flag design

- `orchestrator.decide_next.enabled` in `config/campaign_config.yaml`. One reader,
  `run_phase1_research._decide_next_enabled()` (strict bool; raises if true without
  `regroup_record`, the `_regroup_record_enabled` pattern L3198-3224). `run_campaign` calls it as
  `orch._decide_next_enabled()`, and the orchestrator needs it for the split. Registered in
  `feature_flag_register.yaml` as `off_incomplete`, `blocked_on`: the readers' run budget (no run
  on disk has proposals).
- **Off:** `process_once`, the split, `register_hypothesis` (CLI and default args) and
  `campaign_queue.yaml` are byte-identical. Bug 8 remains on this path.
- **On:** the DONE branch writes `outcome: <idea_status>` + ref (guess 8), calls decide_next,
  applies the result and returns True, or returns False on `stop`. The split enqueues instead of
  scaffolding. Runs are resolved once per `process_once`. A queue holding `queued` entries or new
  fields while the flag is off must still load: the schema accepts them, and `_select_entry`
  ignores `queued`.

## 10. Proposed S2 build list (split in two)

**S2a — decide_next core + queue fields + DONE wiring (reader proposals only):**
1. `record_schema.py`: the five fields of §7, closed vocabularies, and the `queued` token;
   `_SCHEDULABILITY_NON_BLOCKED_STATUSES` += `queued`.
2. `register_hypothesis`: keyword-only `entry_id, source, relation, extra` (defaults
   byte-identical).
3. Move `_apply_json_pointer_patch` + `PatchApplicationError` to `tools/json_pointer.py`
   (thin wrapper kept, behaviour-preserving, like E-058 S2b fix 10).
4. `tools/decide_next.py` (pure; importable without the orchestrator): `load_inputs(root)`
   (memory, registry, queue, proposals via `reader_proposals.load_proposals`, source configs,
   manifests, pre-registrations, known classes); `decide(inputs, now) -> record` covering the
   gates (§4), patch resolution (§3.4), collapse (§3.6), ranking (§5.3), R1 no-op, R2 on
   *existing* open briefs, and the policy (guess 6); `candidate_brief(record, inputs) -> (path,
   text)`.
5. `_decide_next_enabled` + config + register entry.
6. `process_once` DONE branch under the flag: outcome fix, decide, write brief + register +
   decision record + log.
7. 5a pass-through hash check (§3.3) on candidates that carry `candidate.source`.
8. Docs: USER_GUIDE (campaign runner), RUNBOOK §3 row for "decide_next stop: no candidate, no
   open brief", DOC_INDEX, `decision_record.schema.json`.

**S2b — briefs (card M) and R2 exhaustion:**
9. Split under the flag → `queued_hypotheses.yaml` → `process_once` enqueues (`queued`,
   `card_ref`, `origin: brief`); the `queued_card` launch action.
10. `hypothesis-design/SKILL.md`: the three anchored scores per extra card (guess 4b); a
    `brief_status.yaml` exhausted output with no card; the "already produced from this brief"
    context.
11. run_loop: no card + `brief_status: exhausted` → `completed_brief_exhausted`; add it to
    `_NON_VERDICT_OUTCOMES`; the DONE branch flips the owner's `brief_status`.
12. R2 enqueue of 1a requests; the stop rule.

Separate small tickets, outside 6b: the flag-off DONE-branch provenance crash (guess 8); the
split sibling skipping `strategy_config_authoring` (§6); writing `pre_registration.pass_rule`
from the card's 1a `criteria` under config_direct (which would retire guess 2's inheritance).

Run budget: the plan's 2 consecutive real runs, after S2a, where the first must end refuted
(§2).

## 11. Tests (all runnable here: system `python`, no API key, no backtest)

- **Pure decide_next** on synthetic memory, registry, queue and proposals: rank order and
  tie-break; collapse; exact-match REPEAT excludes a candidate and a legacy run never matches;
  the digest outcome is recorded but never excludes; patch resolution (unique, ambiguous,
  missing, stale `before`, non-component field); regime sketch infeasible; the operator `ready`
  entry bypasses ranking; policy demotion from the 4th descendant; R1 recorded as a no-op with
  `would_fire`; R2 on an open brief enqueues exactly one `ready` + the rest `queued`; stop when
  nothing is open; determinism (same inputs give a byte-identical record); no retired field in
  the record.
- **Schema:** each new field accepted/refused with bad vocabulary; `queued` accepted; the token
  rule on `parked_reason`; the existing queue validates unchanged.
- **register_hypothesis:** the four existing tests unchanged; new kwargs produce the agent entry.
- **process_once** (existing `campaign_root` sandbox, `orch.run_loop` stubbed as in
  `test_halt_quarantine_policy.py`): flag off gives a byte-identical `campaign_queue.yaml` and
  log on the DONE path; flag on runs refuted → decide → exactly one `ready` agent entry, a
  decision record on disk, and `_select_entry` returning it on the next step; the outcome fix
  passes `_save_queue`; the stop returns False; a flag-on run never has `continuation_child`.
- **Split (S2b):** flag off gives today's siblings; flag on gives no sibling dirs, `queued`
  entries with `card_ref`, and a launch that skips 1a to the correct next stage for both
  `config_direct` settings.
- **Flag:** false when absent; non-bool raises; on without `regroup_record` raises; register
  entry present (`test_feature_flag_register.py`).
- **Docs gate:** `test_guide_covers_the_code.py`, `test_doc_anchors.py`.

---

## Decision (operator, 2026-09-24)

1. **Accepted.** A reader patch becomes a NEW `hypothesis_id` (`<parent>__<proposal_id>`)
   linked to its parent.
2. **CHANGED -- criteria are NOT inherited from the source run.** A reader may propose an
   idea unrelated to the idea that was tested (a `new_block` in particular). Every
   candidate picked from a proposal therefore goes through step 1a, which writes a
   hypothesis card and criteria **coherent with the proposed idea**, from the criterion
   menu, as the target already does for every idea ("idea criteria are per-hypothesis
   from an anchored criterion menu"; "all candidates enter at Step 1a"). The config
   carried by a patch may pass through to 1b; a `new_block` is authored at 1b. The
   pre_registration / preflight ordering problem this raises (§ on preflight) must be
   solved in the S2 build: 1a writes the criteria before anything that needs them.
3. **Accepted.** The exact-match repeat check (card K: config hash + symbols + timeframe +
   protocol) becomes binding now, from campaign memory; the legacy digest stays
   informational.
4. **Accepted.** Operator-registered `ready` entries first, by priority; extra brief cards
   scored by 1a on the same rubric.
5. **Accepted.** New `queued` status.
6. **DROPPED.** No lineage-depth demotion. Revisit only if endless tweaking shows up in
   the first real runs.
7. **Accepted, plus:** legacy briefs (no `brief_status`) are tagged obsolete in their
   title and never trigger R2.
8. **Accepted.** Under the flag the DONE branch writes `outcome: <idea_status>` citing
   `idea_status.yaml`; the flag-off crash is a separate ticket.
9. **Accepted.** A brief's extra hypotheses keep their card (`card_ref`) and skip
   authoring when picked.

Build split: S2a (core decide_next + queue fields + DONE-branch wiring), then S2b (briefs).
