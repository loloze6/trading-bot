# E-032 S1 — Proactive idea generation: characterization and STOP

**Story:** S1 (characterize and STOP — no production code).
All counts below are MEASURED by
`strategy-research/engineering/roadmap/E-032/artifacts/s1_measure_idea_generation.py`
(read-only, re-run any time) unless marked INFERRED or RECOMMENDATION.
Denominators are stated with every count.

## Conclusion first

The adjacency is not an LLM-behavior problem the prose could talk its way out
of. It is **structural**, at three independent layers, and all three would
need to change:

1. **The prompt literally cannot see campaign history.** `hypothesis_generation`
   and `innovation_expansion` — the two stages that invent content —
   read exactly 3 and 2 files respectively (`workflow/stages.yaml`
   `required_inputs`), and neither list includes `campaign_state.yaml`,
   `campaign_knowledge_base.yaml`, or the near-miss scoreboard.
   `run_claude_worker` (`workflow/run_phase1_research.py:686-761`) builds the
   entire prompt from `required_inputs + optional_inputs` and nothing else —
   there is no side channel. The only stage that reads `campaign_state.yaml`
   is `campaign_review`, which runs once every 6 runs
   (`campaign_state.yaml:510`, `review_every_n_runs: 6`) and whose output is
   orphaned (`next: []`, confirmed independently by E-031 S1).
2. **The schema only has a slot for "delta from the current hypothesis."**
   `expanded_hypothesis_card.schema.json` requires `base_hypothesis_id` and
   has no field for "an unrelated hypothesis." There is no artifact shape in
   this pipeline that represents "propose something with no parent."
3. **The stage agents have zero tools.** `ClaudeAgentOptions(model=
   "claude-haiku-4-5", allowed_tools=[])` (`run_phase1_research.py:788`).
   No web, no MCP, no filesystem beyond the hand-assembled context blocks.
   Even if a stage's prose said "go find something new," it has no mechanism
   to do so — it is a closed-book single-shot completion over whatever text
   was concatenated into the prompt.

The anti-adjacency gate (Task 3) is buildable today from existing fields, but
two of its four candidate keys (`instruments_tried`, `timeframes_tried`) are
**confirmed stale** by direct cross-check (not just cited from E-031 S1): a
gate keyed on the global `timeframes_tried` list alone would **wrongly
refuse** a funding-family 4h proposal, because `'4h'` is in the list only from
unrelated `keltner` runs — the funding family has never been run at 4h at all
(0 of 7 funding-family runs; see Task 3). The KB-level `reactivation_condition`
mechanism is more precise and does not have this failure mode — the gate
should be layered, KB-finding first, blunt lists second, never the reverse.

Applied to the worked calibration case: **the gate ADMITS the funding-rate 4h
retest.** It is not a neighbour of a killed family — it is the one named
branch of an explicitly OPEN, unconsumed KB reactivation clause that the
project's own daily-branch test (run_059) did not close. See Task 3 for the
full predicate trace.

---

## Task 1 — what bounds the generating stages, mechanism by mechanism

### `hypothesis_generation` (`workflow_artifacts/skills/hypothesis-design/SKILL.md`)

- **Input, as fed to the model** (measured, `stages.yaml:10-19` +
  `run_phase1_research.py:711-720`): `research_brief.yaml` (this run's brief
  only), `available_feeds.yaml`, `indicator_library.yaml`. The skill's own
  "Context rule" restates this and adds a hard boundary: *"Do not read other
  files unless the handoff explicitly requires them."* Nothing about prior
  runs, failed families, or the near-miss scoreboard is in scope — not
  forbidden by name, simply never in the room.
- **Scope-bounding mechanisms found in the skill text itself:**
  - "Do not propose more than 3 run-queue variants unless explicitly
    requested" (Forbidden list) — caps breadth per invocation.
  - "Do not re-propose an indicator + mechanism combination already marked
    `outcome: failed` in the library's `campaign_empirical_results`... without
    a materially new mechanism" — this is the ONE place this skill checks
    cross-run history, but only through `indicator_library.yaml`'s
    per-indicator `campaign_empirical_results` field (indicator-scoped, not
    campaign-scoped) — a narrower, differently-shaped record than
    `campaign_state.yaml.failed_families`.
  - "Prefer hypotheses that can be integrated as a minimal change in the
    current strategy architecture" — an explicit minimality instruction, the
    opposite of a curiosity mandate.
  - `power_parameters.plausible_ic_upper` must come from a fixed 5-row anchor
    table by signal class — this constrains a *number*, not the idea, but it
    is one more place where the skill is told "pick from what's known,"
    reinforcing the register.
- **What it is never shown:** `campaign_state.yaml` (failed_families,
  altitude_history, diagnostics_log), `campaign_knowledge_base.yaml`
  (reactivation clauses), the near-miss scoreboard. It cannot avoid a
  neighbour of something it has never been told about, and it cannot draw on
  a near-miss it has never been shown.

### `innovation_expansion` (`workflow_artifacts/skills/innovation-expansion/SKILL.md`)

- **Input, as fed to the model** (measured, `stages.yaml:21-30`):
  `research_brief.yaml`, `hypothesis_card.yaml` (THIS run's card — the base
  hypothesis it must expand), `available_feeds.yaml`. Context rule: *"Use
  research_brief.yaml, hypothesis_card.yaml, config/available_feeds.yaml, and
  config/indicator_library.yaml. Do not read other files unless explicitly
  required."*
- **The schema is the strongest scope-bounding mechanism found anywhere in
  this survey.** `expanded_hypothesis_card.schema.json` requires
  `base_hypothesis_id` (string) and its only content field for new ideas is
  `expanded_variants: array[string]` — variants of that one base. There is no
  field, anywhere in the schema, that represents "a hypothesis unrelated to
  `base_hypothesis_id`." A schema-conformant output is *definitionally* a set
  of children of one parent. This is stronger than any prose instruction
  because it isn't advisory — a non-conformant output fails validation before
  it can reach the queue.
- **Diversity check is real but bounded to the sibling set.** Improvement 04's
  "cosmetic diversity" rejection (all variants share `category` AND
  `data_requirements` → reject, regenerate) forces variants to differ from
  EACH OTHER along a real axis. It does not, and structurally cannot, compare
  the variant set to anything outside this hypothesis's own lineage — there is
  no history in the prompt to compare against.
- **Regime-gated ideas are explicitly redirected away from the queue**
  (`regime_specific_variants` → `detector_wishlist_pending`, never
  `expanded_variants`) — this is a real non-adjacency escape valve in
  principle (it does produce something outside the current signal family) but
  it dead-ends: `detector_wishlist.yaml`'s three candidates are gated by
  `evaluate_and_persist_wishlist_predicate()`, which E-031 S1 found has **zero
  callers anywhere in the repo** — a write path that exists and is never
  invoked. Confirmed independently here by the same grep pattern this report
  ran against `run_phase1_research.py` and `run_campaign.py`.

### `refinement_planner` (`workflow_artifacts/skills/refinement-planner/SKILL.md`)

- **Input, as fed to the model** (measured, `stages.yaml:32-40`):
  `validation_decision.yaml`, `validation_protocol.yaml`,
  `expanded_hypothesis_card.yaml`, `innovation_notes.yaml` — all THIS run's
  artifacts. Context rule: *"Read only the validation artifacts and the
  current hypothesis context. Use minimal context."*
- **The tightest of the three.** Forbidden list: *"Do not redesign the
  strategy."* Mission: *"Turn validation blockers into a concrete refinement
  artifact"* — the entire purpose is bounded to responding to blockers on the
  hypothesis already in hand. This is the mechanism behind the epic's own
  measured "19 of 36 completions were `completed_refined`" — refinement is
  designed, correctly for its stated job, to never look sideways.

### Net effect, stated once

Three independent barriers stack: (a) the **prompt's input set** structurally
excludes cross-run history for the two stages that invent content, (b) the
**schema** for expansion output has no non-adjacent slot, (c) the **agent has
no tools** to go find something external even if instructed to. Prose changes
inside the existing SKILL.md files (item (a)'s content) cannot fix (a) or (b)
by themselves — a skill cannot read a file `stages.yaml` never listed as a
required input, and cannot emit a field the schema forbids. **This is why S2
must touch `stages.yaml`'s required_inputs and at least one schema, not only
the skill prose** — a disposition rewrite alone would be advisory text with
no new information to act on.

---

## Task 2 — where the disposition belongs

### How this project already writes agent behaviour

Two separate systems share the word "skill" and must not be conflated:

1. **`workflow_artifacts/skills/*/SKILL.md`** — pipeline-stage skills. Loaded
   mechanically by `run_phase1_research.py:686-709`'s `skill_map` dict
   (stage name → skill directory), read as raw text, and concatenated
   verbatim into the system-prompt section of a single-shot `query()` call
   (`allowed_tools=[]`, `model="claude-haiku-4-5"`). These are NOT invoked
   the way a Claude Code skill is invoked by an operator — they are pure
   prompt text assembled by the orchestrator and driven by `stages.yaml`.
   Changing what one of these agents can act on requires changing (i)
   `stages.yaml`'s `required_inputs` (what reaches the prompt) and/or (ii)
   the relevant `*.schema.json` (what the agent is legally allowed to emit) —
   the SKILL.md prose alone changes neither.
2. **`.claude/skills/*`** (e.g. `research-system-evolution`) — operator-level
   Claude Code skills, invoked interactively by name at the top-level session,
   with full tool access. This is a different invocation path entirely; it
   produced the review that opened this epic, but it is not part of the
   automated per-run pipeline `run_campaign.py` drives.

### Recommendation

The disposition needs THREE landing spots, matching the three barriers found
in Task 1 — a skill-prose amendment alone would be advisory text with nothing
new to act on:

1. **A new required_input on `hypothesis_generation` and
   `innovation_expansion`** in `stages.yaml`: a small, purpose-built
   "exclusion digest" artifact (NOT the raw `campaign_state.yaml`, which is
   721 lines with diagnostics/altitude history irrelevant to idea proposal —
   the digest should be the four candidate-key fields the gate uses,
   refreshed, per Task 3). This is a config/plumbing change, not a skill
   rewrite, and it is the one change that actually puts campaign history in
   front of the model.
2. **A skill-prose amendment** to `hypothesis-design/SKILL.md` and
   `innovation-expansion/SKILL.md` (existing files, additive sections,
   matching this project's own convention of numbered "IMPROVEMENT NN"
   blocks) instructing the model to actively consult the new digest and the
   near-miss scoreboard (once E-018 S2 wires read access) and to prefer a
   candidate that clears the gate over a same-family tweak when both are
   available. This is the "proactive disposition" the epic's Done-when #1
   asks for — but it is advisory prose layered ON TOP of (1) and (3), not a
   replacement for either.
3. **A new deterministic tool stage** for the REFUSAL itself (Task 3's gate),
   following this project's own existing precedent: `signal_prescreen` and
   `regime_detector_validation` are already `tool:` stages (deterministic
   Python, not LLM) inserted between LLM stages specifically because a
   mechanical pass/fail should not be adjudicated by prose. The gate belongs
   in the same class — e.g. `tools/anti_adjacency_gate.py`, run right after
   `hypothesis_generation`/`innovation_expansion` produce a candidate, before
   `validation`. This matches the epic's own Done-when #2 requirement
   ("mechanical, not aspirational") and this project's established pattern of
   putting the falsifiable check in code and the judgment call in prose.

Do NOT put the refusal logic only in SKILL.md prose. This project already has
prose refusal rules in `hypothesis-design/SKILL.md`'s Forbidden list (e.g. "do
not re-propose a failed indicator+mechanism combination") and the epic's own
measured baseline — 30 of 36 completions being adjacent follow-ons — is the
proof that prose alone, even when explicit, does not prevent the failure mode
this epic exists to close.

---

## Task 3 — the anti-adjacency gate

### What each candidate key currently holds (MEASURED, `campaign_state.yaml`, 727 lines)

| Field | Count | Denominator | Note |
|---|---|---|---|
| `failed_families` | 9 | this list | 6 dict entries (name/evidence_window/root_cause), 3 bare strings (funding_rate_mean_reversion, sma_trend, sma_trend_following) — schema is inconsistent within the same field |
| `recent_parameter_dimensions_by_family` | 4 families tracked | this dict | only 1 (`fear_greed_contrarian: [signal_polarity]`) non-empty; the other 3 are empty lists |
| `instruments_tried` | 4 (`BTCUSDT, ETHUSDT, SOLUSDT, AVAXUSDT`) | this list | **STALE** — see below |
| `timeframes_tried` | 3 (`1h, 4h, 15m`) | this list | **STALE, and demonstrably wrong at the (family, timeframe) grain** — see below |
| `components_built` | 0 | this list | empty, confirms epic's headline claim exactly |

### The staleness trap: confirmed, not just cited

E-031 S1's claim is correct on both counts, independently re-verified here:

- **`instruments_tried` (4 symbols) vs. the actual ratified universe (19
  Kraken pairs, `config/campaign_queue.yaml`'s `XS_momentum` entry: "P2
  CLOSED + RATIFIED 2026-07-22... Instrument universe ratified = all 19
  ingested Kraken pairs").** Never updated.
- **`timeframes_tried` (`1h, 4h, 15m`) is family-blind, and this matters
  concretely, not just abstractly.** Direct scan of all 7 funding-family
  `hypothesis_card.yaml` files (run_041, 044, 047, 048, 050, 058, 059) found
  timeframes used: `{1h, 1d}` only — **zero** funding-family runs at 4h. The
  `'4h'` value in the global list comes entirely from 11 `keltner`-family
  runs (021, 022, 027–031). **A gate that checks `candidate.timeframe in
  timeframes_tried` globally would refuse a funding-family 4h proposal for a
  reason that has nothing to do with funding rate — this is confirmed by the
  measurement script, not inferred.**
- Daily bars for BTC/ETH landed 2026-08-07 (`config/campaign_queue.yaml`,
  P4 entry, "(a) daily bars — already satisfied, 19 kraken_*USD_1d.csv caches
  landed 2026-08-07"); `timeframes_tried` has no `1d` entry despite run_059
  (a completed, gated, daily-timeframe run) existing since 2026-07-19.

**What the gate must do about it:** never trust `instruments_tried` /
`timeframes_tried` as a global cross-family veto. Two options, either
acceptable, neither optional:
(a) refresh both fields mechanically before every gate evaluation (scan
`runs/run_*/artifacts/hypothesis_card.yaml` for the real
`(family, instrument, timeframe)` triples, the way this report's script
does), or
(b) key the exclusion check per-family from the start — never ask "has this
timeframe been tried," only "has this (family, timeframe) pair been tried" —
which sidesteps the staleness of the aggregate list entirely, at the cost of
needing a family-taggable index the project does not currently maintain
(`hypothesis_card.yaml` has no `family` field; family names today are strings
inferred from `hypothesis_id`/`thesis` text, as the near-miss scoreboard's own
`hypothesis_family` column — itself marked `not_recorded` in several rows —
demonstrates).

### Recommended predicate (dispatch-ready for S2)

Layered, KB-first, blunt-list-second — never the reverse, because the KB is
the only source with per-branch (not per-family) granularity:

```
def anti_adjacency_gate(candidate) -> Refuse | Admit:
    # Layer 1 — exact-mechanism match against campaign_knowledge_base.yaml findings
    kb = find_kb_finding_by_mechanism(candidate.mechanism_signature)
    if kb is not None:
        if kb.reactivation_consumed_by is not None:
            return REFUSE(f"already reactivated by {kb.reactivation_consumed_by}")
        if kb.exhausted and kb.reactivation_condition is None:
            return REFUSE("closed, no open reactivation clause")
        if kb.reactivation_condition is not None:
            if candidate_matches_named_branch(candidate, kb.reactivation_condition):
                return ADMIT(f"matches open branch of {kb.finding_id}; "
                              f"branch not yet consumed")
            else:
                return REFUSE(f"{kb.finding_id} has an open reactivation clause, "
                               f"but this candidate is not the named branch")
        # kb exists, not exhausted, no reactivation_condition recorded yet:
        # fall through to Layer 2 (KB doesn't cover this axis explicitly)

    # Layer 2 — refreshed, per-family exclusion (never the raw global lists)
    triples = scan_runs_for_family_instrument_timeframe(candidate.family)
    if (candidate.instrument, candidate.timeframe) in triples:
        return REFUSE(f"{candidate.family} already run at "
                       f"({candidate.instrument}, {candidate.timeframe})")
    if candidate.family in failed_families_bare_string_entries():
        # bare-string entries (funding_rate_mean_reversion, sma_trend,
        # sma_trend_following) carry no evidence_window/root_cause detail --
        # treat as a WEAKER signal than a dict entry, not equal weight.
        # Never a silent auto-refuse; flag for the digest.
        flag_low_detail_prior_failure(candidate.family)

    return ADMIT("no matching family/instrument/timeframe triple in history, "
                  "no closed/consumed KB finding covers this axis")
```

Never a global `if candidate.timeframe in timeframes_tried: REFUSE` — Layer 2
must always be keyed on the `(family, instrument, timeframe)` triple, scanned
fresh, not on the flat lists as stored.

### Worked calibration case: funding-rate 4h retest

**Facts (all MEASURED, cross-checked against `campaign_knowledge_base.yaml`
and `runs/run_059/`):**

- KB finding `funding_rate_continuous_mean_reversion_expanded_auto`
  (hypothesis_id `FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED`, evidence
  `run_044`): `exhausted: false`, `reactivation_condition` names BOTH
  branches explicitly — *"re-test the identical mechanism... at 4h or
  daily."*
- The daily branch ran as `run_059` → child KB finding
  `funding_mr_daily_retest_killed`: `outcome: completed_rejected`,
  pre-registered B11 pass rule FAILED both criteria both symbols (median
  Sharpe BTC -0.296 / ETH -0.979; max drawdown BTC 34.922% / ETH 49.606%),
  `lineage_routing: terminate`.
- **The child finding's closure does NOT close the parent.** The KB text is
  explicit: *"This entry's exhausted:true/reactivation_condition:null does
  NOT itself close funding_rate_continuous_mean_reversion_expanded_auto's
  parent entry, whose own exhausted/reactivation_condition fields hold the
  values they held before this write"* — i.e. the parent still reads
  `exhausted: false` with the 4h branch named and open. Confirmed again by a
  second KB passage: *"The 4h branch of the parent reactivation_condition
  remains DEFERRED and is untouched."*
- Cost did play a real role in both branch failures — but not identically.
  1h (`run_044`) failed on the deterministic prescreen cost gate
  (`edge_to_cost_ratio=0.2425`, required ≥2.0). Daily (`run_059`) actually
  *passed* prescreen on cost (`edge_to_cost_ratio=2.2927`,
  `prescreen_result.yaml:108`) but was killed on the full-sample pass rule —
  Sharpe/drawdown, with the verdict interpreter separately noting the
  cost-adjusted net expectancy was negative once realized over the full
  sample (`already_priced_in`, `per_trade_expectancy_bps mean -38.47`). So
  "cost has killed this family twice" is defensible but imprecise: 1h died at
  the cheap prescreen gate, daily died on realized net PnL after a more
  expensive full run — the failure mode differs by branch, which is itself
  evidence the two branches are not interchangeable and a per-branch (not
  per-family) refusal is correct.
- A reproduction of `run_059` under the current engine convention (2026-08-23,
  `E-012/EPIC.md` log) found BTCUSDT median Sharpe crosses from -0.296 to
  **+0.016** (the pre-2026-08-09 two-bars-drop bug inflated the loss), while
  ETHUSDT stays deeply negative (-0.979 → -0.885) and both drawdowns stay
  effectively unchanged (34.9%/49.5%). The pass-rule kill verdict is
  UNCHANGED under the current convention — this strengthens confidence the
  daily-branch kill is real, not a stale-engine artifact, without changing
  which branch is open.

**Gate trace:**

- Layer 1: KB match found (`funding_rate_continuous_mean_reversion_expanded_auto`).
  `exhausted=false`, `reactivation_consumed_by` absent on the parent.
  `reactivation_condition` names two branches; daily is consumed (child
  finding exists, terminal), 4h is not. Candidate's timeframe = 4h → **matches
  the open, unconsumed branch.**
- **Verdict: ADMIT.**
- Layer 2 is never reached — Layer 1 resolved the case, which is the point of
  running KB-first: had this gone to Layer 2 first, `'4h' in timeframes_tried`
  (True, from unrelated keltner runs) would have produced a **false REFUSE**
  — exactly the trap this section exists to prevent.

This is the gate's answer, and it is mechanical: not "4h sounds mechanistically
justified" (the sampling argument in the prompt, which is real but is a
research-quality judgment, not a gate input) and not "cost killed this family
twice so kill everything" (true in aggregate, false at the branch grain the KB
itself maintains). The gate ADMITS because a specific, still-open,
not-yet-consumed exclusion-list entry says so — the sampling mechanism
argument is a reason a human might find the candidate worth *prioritizing*
once admitted, not what the gate itself evaluates.

### Build list for S2 (from this story alone, not exhaustive of the whole epic)

1. Add a `family` field to `hypothesis_card.schema.json` (currently absent;
   the near-miss scoreboard and this report both had to infer family from
   free text) — required for Layer 2 to be keyed correctly instead of via
   regex-on-thesis-text.
2. Build the KB-finding lookup helper (`find_kb_finding_by_mechanism`) —
   likely a normalized match on `hypothesis_id`/`mechanism` substring, since
   `campaign_knowledge_base.yaml` findings have no separate `family` field
   either.
3. Build the refreshed-triple scanner (`scan_runs_for_family_instrument_timeframe`)
   — this report's measurement script is a working prototype of the read
   path; S2 should productionize it, not `campaign_state.yaml`'s stored
   `instruments_tried`/`timeframes_tried`, which should be either dropped or
   explicitly relabeled `informative_only_do_not_gate_on`.
4. Add `tools/anti_adjacency_gate.py` as a new `tool:` stage in
   `stages.yaml`, inserted after `innovation_expansion` / before
   `validation`, following the `signal_prescreen` precedent exactly (same
   file, same "deterministic tool, not LLM" pattern).
5. Wire the KB `reactivation_consumed_by`/`exhausted` write path this gate
   depends on — confirm it is written correctly per-branch (this story found
   it IS, for the funding case) but there is no test locking that behavior;
   S2 should add one before depending on it.

---

## Task 4 — the external-knowledge dispatch path

### What exists today (characterization only)

- **Zero network/tool access at the stage-agent layer.** Confirmed
  mechanically: `ClaudeAgentOptions(model="claude-haiku-4-5",
  allowed_tools=[])` (`run_phase1_research.py:788`). The comment directly
  above it states the intent: *"We pass an empty allowed_tools list to
  prevent it from wandering off and strictly enforce our handoff file
  constraints."* This was a deliberate containment decision for the existing
  stages, not an oversight — any external-knowledge path needs its own,
  separately-justified tool grant, not a loosening of the existing one.
- **No existing schema shape for "imported from outside."** `hypothesis_card`
  and `innovation_notes` schemas have no `source`/`date` fields anywhere.
  `edge_source.category` is a closed 5-value enum
  (`information_asymmetry`, `structural_forced_flow`, `liquidity_provision`,
  `cross_venue_dislocation`, `persistent_behavioral_bias`) — an externally
  sourced mechanism still has to land in one of these five; nothing new is
  needed there, but the anti-confabulation bar (A1.3: causal chain + a
  measurable proxy in `available_feeds.yaml`) applies identically and is the
  correct control — it already forces "fitted rule" language back into
  "mechanism" language or routes to `feed_wishlist.yaml`.

### Characterization of what building it would require

1. **A separate dispatch, not a loosened stage.** The existing three
   generating stages run on `claude-haiku-4-5` with no tools, cheap and
   contained by design. An external-knowledge search-and-synthesize task is a
   different shape of work (harder judgment: separating a real structural
   mechanism from a fitted backtest result written up on a forum) and should
   be its own stage/dispatch with its own model tier and its own tool grant
   (e.g. WebSearch/WebFetch), not a flag flipped on an existing stage.
2. **Trigger condition, per the epic's Done-when #3: "when internal sources
   are spent."** This needs a concrete, checkable definition — e.g. "the
   anti-adjacency gate (Task 3) has REFUSED N consecutive proposals for the
   current research question" or "zero admissible candidates from Layer
   1/Layer 2 of the gate" (mirrors E-031 S1's own "zero admissible
   candidates" terminal state design for queue refill — the two epics should
   share this shape, not invent two).
3. **Output contract, fixed by the epic, not open for this story to
   redesign:** returns MECHANISMS not fitted rules (must be re-expressible as
   forecast → allocation / regime detection / regime→strategy mapping in this
   bot's own architecture — same bar `hypothesis-design`'s A1.3 already
   enforces on internally-generated ideas, so an imported idea should be
   required to pass through the SAME `edge_source` block and the SAME A1.3
   check, not a parallel one); every entry carries `source` (URL/citation)
   and `date` (publication or access date), for publication-bias control, not
   lookahead — the existing era-stability bar (2018-20/2021-22/2023-25
   sign-consistency) is what actually uses that date, per the epic.
4. **A new artifact/schema is needed**, analogous to `innovation_notes.yaml`
   but distinctly named (e.g. `external_knowledge_notes.yaml`) so the firewall
   discipline this project already applies to the near-miss scoreboard
   (E-018: "the scoreboard inspires; only the gates decide," enforced by a
   static test) can be applied here too: an externally-sourced idea is raw
   material for `hypothesis_generation`, not a promotion input, and should
   flow through the SAME `hypothesis_card.yaml` → gate → validation pipeline
   as any other candidate, never around it.
5. **Recommended shape, not a discovered constraint:** a new stage
   `external_knowledge_search`, triggered by the gate-exhaustion condition
   above, with its own `skill:` file under `workflow_artifacts/skills/`
   (matching this project's existing pattern — do not invent a second skill
   system), a real tool grant (WebSearch/WebFetch), a model tier suited to
   judgment-heavy synthesis, and an output that is REQUIRED to pass through
   `hypothesis-design`'s existing A1.3 anti-confabulation gate before
   reaching the queue — external sourcing does not exempt an idea from the
   same mechanism-purity bar internally generated ideas already clear.

This is a full story's worth of design (S3), not a dispatch-ready predicate
like Task 3 — flagged here as characterization only, per the story's scope.

---

## Near-miss scoreboard (E-018 S1) fitness as idea-generation input

Assessed per the epic's explicit pointer, not re-derived: `tools/near_miss_scoreboard.py`
+ `engineering/roadmap/E-018/artifacts/near_miss_scoreboard.{md,yaml}`
(committed `112677e2`, same day as this story).

- **Coverage is thin.** Of 59 run dirs: 38 have any verdict file; numeric
  near-miss margin recovered for 24; IC recovered for 7; cost ratio for 5;
  era-behavior text for 4 (all denominators from the artifact's own header).
  As raw material this is usable — the epic's own bar is "raw material," not
  "complete" — but a consuming skill must be told explicitly that most rows
  are `not_recorded`, not silently treat sparse rows as "nothing to learn
  here."
- **The mixed-convention caveat is real and directly relevant to Task 3's
  calibration case.** `E-018/EPIC.md`'s 2026-08-23 log entry: 58 of 59 run
  dirs are on the pre-two-bars-fix engine convention; the scoreboard's
  `worst_fail_margin_frac` column mixes both conventions and "must not be
  quoted as comparable across that date." Concretely for the funding family:
  `run_059`'s scoreboard row (`rank 6`, `worst_fail_margin_frac -0.6535`) is a
  PRE-FIX number; this story's own reproduction check (Task 3) shows the
  BTCUSDT figure specifically crosses zero post-fix. **A consuming skill using
  the scoreboard's margin column to judge "how close" a killed idea came must
  not treat that margin as current without checking the run's date against
  2026-08-09** — this is a concrete instruction the disposition (Task 2, item
  2) should carry, not a generic caveat.
- **It is not wired as an input today.** No skill's `required_inputs` in
  `stages.yaml` references it (confirmed by the same grep this story ran for
  Task 1); E-018's own S2 ("wire idea-generation read access... and the
  firewall") is explicitly parked pending E-032 existing as the consumer.
  This story's build list item 4 (the new `tool:` gate stage) and E-018 S2
  should land together — the gate is a natural place to also surface the
  scoreboard's near-miss rows for the SAME family as supporting context in the
  digest handed to `hypothesis_generation`.

---

## Files read (representative, not exhaustive)

- `strategy-research/engineering/roadmap/E-032/EPIC.md`
- `strategy-research/engineering/roadmap/E-031/EPIC.md`,
  `.../E-031/artifacts/s1_refill_sources.md`
- `strategy-research/engineering/roadmap/E-018/EPIC.md`,
  `.../E-018/artifacts/near_miss_scoreboard.{md,yaml}`,
  `strategy-research/tools/near_miss_scoreboard.py`
- `strategy-research/engineering/roadmap/E-012/EPIC.md` (two-bars-fix /
  run_059 reproduction log entry)
- `strategy-research/workflow/stages.yaml`
- `strategy-research/workflow/run_phase1_research.py` (skill_map,
  `run_claude_worker`, `ClaudeAgentOptions`)
- `strategy-research/workflow_artifacts/skills/hypothesis-design/SKILL.md`
- `strategy-research/workflow_artifacts/skills/innovation-expansion/SKILL.md`
- `strategy-research/workflow_artifacts/skills/refinement-planner/SKILL.md`
- `strategy-research/workflow_artifacts/skills/campaign-review/SKILL.md`
- `strategy-research/workflow_artifacts/schemas/hypothesis_card.schema.json`
- `strategy-research/workflow_artifacts/schemas/expanded_hypothesis_card.schema.json`
- `strategy-research/campaign_record/campaign_state.yaml`
- `strategy-research/campaign_record/campaign_knowledge_base.yaml`
- `strategy-research/config/available_feeds.yaml`,
  `strategy-research/config/campaign_queue.yaml`
- `strategy-research/runs/run_041,044,047,048,050,058,059/artifacts/hypothesis_card.yaml`
- `strategy-research/runs/run_059/artifacts/prescreen_result.yaml`
- `.claude/skills/research-system-evolution/SKILL.md` (for Task 2's
  two-skill-system distinction)
