# E-037 — FINDINGS

Doc-vs-code disagreements found while writing E-037.

> **On the ID prefix.** These are numbered **E037-01 … E037-29**, not F1..F29.
> They were originally written as `F`-numbers and renamed on 2026-08-31, because
> **this repository already uses an `F`-code convention of its own** in source
> comments — `F5c` (the zero-signal-artifact override), `F6` (per-family circuit
> breaker scoping), `F4d`, `F4f`, `F8b` and others. Four IDs collided outright:
> `F3`, `F5`, `F6` and `F8` meant two different things at once.
>
> That is precisely the incident this project already recorded as **C4,
> "Rule-citation confabulation"** — a citation that looks authoritative and
> resolves to the wrong rule. Renaming was cheaper than living with it. Where
> you see a bare `F5c` or `F6` in the guide or in code comments, it is the
> **codebase's** code and has nothing to do with these findings.

**Rule: findings are RECORDED, never fixed here.** No code and no
`USER_GUIDE.md` text has been changed on their account. They become cards or
issues at S3, where Jérémy decides which get worked.

**Status of this file:** seeded by **S1** (2026-08-30), which audited exactly
one stage (7, `signal_prescreen`) and one artifact (`prescreen_result.yaml`)
to prove the templates in [`S1_TARGET_SHAPE.md`](S1_TARGET_SHAPE.md). S2
appends the remaining 12 stages and ~30 artifacts to this same file.

**Reviewed against:** `master` at `753c9ac3`, working tree at branch
`docs/e037-s1-target-shape`. Every `file:line` below was verified against that
tree, not inferred.

That eleven findings came out of **one** stage and **one** artifact is itself
the finding the epic predicted: the pipeline has no written input/output
contract, so nobody could see them.

## Summary

| ID | Severity | Type | Lands on |
|---|---|---|---|
| [E037-01](#e037-01) | medium | doc-vs-code | `docs/USER_GUIDE.md §2.2` |
| [E037-02](#e037-02) | medium | doc-vs-code | `docs/USER_GUIDE.md §3` |
| [E037-03](#e037-03) | low | doc-incomplete | `docs/USER_GUIDE.md §3` |
| [E037-04](#e037-04) | medium | doc-vs-code | `docs/USER_GUIDE.md §3` |
| [E037-05](#e037-05) | medium | doc-vs-code | `docs/USER_GUIDE.md §2.2 + §3` |
| [E037-06](#e037-06) | low | doc-vs-code | `docs/USER_GUIDE.md §2.2` |
| [E037-07](#e037-07) | **high** | doc-missing-contract | `docs/USER_GUIDE.md §3` |
| [E037-08](#e037-08) | low | doc-incomplete | `docs/USER_GUIDE.md §2.2 + §3` |
| [E037-09](#e037-09) | medium | doc-vs-doc | `strategy-research/CLAUDE.md` |
| [E037-10](#e037-10) | **high** | code-defect | `strategy-research/tools/episode_significance.py:209` |
| [E037-11](#e037-11) | medium | code-fragility | `strategy-research/workflow/run_phase1_research.py:3237` |
| [E037-12](#e037-12) | medium | doc-unresolvable-reference | `docs/USER_GUIDE.md` (whole document) |
| [E037-13](#e037-13) | medium | wrong-citation | `strategy-research/tools/prescreen_signal.py:1089,1100,1580` |
| [E037-14](#e037-14) | medium | phantom-field | `docs/USER_GUIDE.md:613` |
| [E037-15](#e037-15) | medium | doc-vs-code | `docs/USER_GUIDE.md` §2.2 · `run_phase1_research.py:88` |
| [E037-16](#e037-16) | **high** | stage-does-not-run | `docs/USER_GUIDE.md` §2.1/§2.2 (stage 10) |
| [E037-17](#e037-17) | medium | silent-no-op | `run_phase1_research.py:2410` |
| [E037-18](#e037-18) | **high** | unenforced-rule | `docs/USER_GUIDE.md` §2.2 (stage 3) |
| [E037-19](#e037-19) | **high** | missing-artifacts | `docs/USER_GUIDE.md` §3 |
| [E037-20](#e037-20) | medium | inconsistent-metadata | `docs/USER_GUIDE.md` §3 |
| [E037-21](#e037-21) | **high** | documents-inactive-machinery | `docs/USER_GUIDE.md` §3 |
| [E037-22](#e037-22) | **high** | phantom-fields | `docs/USER_GUIDE.md` §3 (`verdict_interpretation.yaml`) |
| [E037-23](#e037-23) | medium | phantom-values + unhandled-status | `docs/USER_GUIDE.md` §3 (`decision.yaml`) |
| [E037-24](#e037-24) | **high** | phantom-fields (systemic) | `docs/USER_GUIDE.md` §3 — 5 entries |
| [E037-25](#e037-25) | medium | incomplete-index | `docs/USER_GUIDE.md` §5 |
| [E037-26](#e037-26) | **high** | code-regression | `strategy-research/tools/prescreen_signal.py:1320` |
| [E037-27](#e037-27) | **high** | gap-in-the-gate | `.git/hooks/pre-commit` · `.github/workflows/tests.yml` |
| [E037-28](#e037-28) | low | stale-count | `docs/USER_GUIDE.md` §6 (`Run`) |
| [E037-29](#e037-29) | **high** | guard-not-installed | `.git/hooks/pre-commit` (this machine) |
| [E037-30](#e037-30) | low | orphan-glossary-terms | `docs/USER_GUIDE.md` §6 |

**Counts:** 11 high · 14 medium · 5 low. One closed (E037-29). By type: 5 doc-vs-code, 2
doc-incomplete, 1 doc-missing-contract, 1 doc-vs-doc, 1
doc-unresolvable-reference, 1 wrong-citation, 1 phantom-field, 1 code-defect,
1 code-fragility.

**The two that are code, not documentation** — E037-10 and E037-11 — are the ones that
do not go away by editing a sentence. E037-10 in particular is a fix that looked
complete and was not.

---

## E037-01

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 (stage 7)`

**Found by:** S1 worked sample, 2026-08-30


§2.2 stage 7's Objective opens "A8.6 pre-flight first (blocks if power insufficient)", under Engine = *Python tool*. `tools/prescreen_signal.py` contains **no power check at all**. A8.6 runs in the orchestrator, at `run_phase1_research.py:6217` (immediately before the tool subprocess) and again at `:2287` inside `determine_post_validation_route`. The stage row conflates orchestrator wrapper logic with tool logic — exactly the confusion E-037 exists to remove. §2.1's stage map is *not* wrong here: it correctly attaches A8.6 to both validation_gate and signal_prescreen.


**Proposed disposition (S3 decides, not this file):** Correct the stage-7 row to attribute A8.6 to the orchestrator, not the tool.


---

## E037-02

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3's `prescreen_result.yaml` `route` enum lists 6 values and **omits `no_signal_artifact`**, which the code emits at `prescreen_signal.py:1481` and which **overrides every other route**. A reader of §3 cannot know the most consequential route exists.


**Proposed disposition (S3 decides, not this file):** Add `no_signal_artifact` to the route enum and mark it as overriding.


---

## E037-03

**Severity:** low · **Type:** doc-incomplete · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3's field table lists 6 fields; the written artifact has roughly 30 top-level keys. Load-bearing omissions: `forecast_hash` (dedup key for trial counting), `sigma_is_placeholder` (invalidates `cost_check` when true), `significance_methodology_used`, `gap_stats_by_symbol`, `a86_power_check`. Not an error — but nothing marks the table as a selection, so absence reads as non-existence.


**Proposed disposition (S3 decides, not this file):** Mark the table as a selection; add the five load-bearing omissions.


---

## E037-04

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3 says **Created by:** "signal_prescreen tool (`tools/prescreen_signal.py`)". On the insufficient-power path the file is created by the **orchestrator** (`run_phase1_research.py:6232` and `:2297`) and the tool never runs. The `Created by` line is wrong for one of its three creation paths, and the resulting artifact has a completely different shape (4 keys, no IC/cost/provenance fields) that §3 does not mention.


**Proposed disposition (S3 decides, not this file):** List all three creation paths; document the 4-key stub shape.


---

## E037-05

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 + §3`

**Found by:** S1 worked sample, 2026-08-30


Both §2.2 stage 7 ("block-bootstrap significance") and §3 (`ic_significance` — "block-bootstrap") name the **fallback** method as if it were the default. The default is block-deflated **Fisher z** (`z = IC * sqrt(n_eff - 3)`, `prescreen_signal.py:643`, labelled `block_{n}_fisher_z` at `:1377`). A stationary block bootstrap runs only on the degenerate-active-forecast path (`:730`), and A8.5.1a episode-blocking is a third method (`:1402`). Three methods, one name in the doc.


**Proposed disposition (S3 decides, not this file):** Name the three methods separately; default is block-deflated Fisher z.


---

## E037-06

**Severity:** low · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 (stage 7)`

**Found by:** S1 worked sample, 2026-08-30


§2.2 stage 7 says "Records trial in `campaign_state.trial_sharpes` (A6.2)". Done by the orchestrator (`_record_prescreen_trial`, `run_phase1_research.py:4039`, called at `:1130`, `:6215`, `:6235`), not by the tool. Same class as E037-01.


**Proposed disposition (S3 decides, not this file):** Attribute A6.2 trial recording to the orchestrator.


---

## E037-07

**Severity:** **high** · **Type:** doc-missing-contract · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (regime_audit_decision.yaml)`

**Found by:** S1 worked sample, 2026-08-30


**Undocumented cross-stage write.** `run_prescreen` writes into **stage 10's** artifact: it opens `runs/{run_id}/artifacts/regime_audit_decision.yaml` and resolves `ungated_escape_eligible` in place (`prescreen_signal.py:1582` → `_resolve_ungated_escape`, `:1092`). §3's `regime_audit_decision.yaml` entry says **Created by:** "regime-auditor skill" and has **no** `Updated by` line, so no reader of the guide could discover that stage 7 rewrites it. This is precisely the input/output-contract blind spot the EPIC blames for the bug list feeling uncontrollable — and it is the strongest evidence that the `Updated by` normalisation in §2 of this document is load-bearing rather than cosmetic.


**Proposed disposition (S3 decides, not this file):** Add an `Updated by` line naming signal_prescreen. Consider whether a cross-stage in-place write is the design you want -- that part is a CODE question, not a doc one.


---

## E037-08

**Severity:** low · **Type:** doc-incomplete · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 + §3`

**Found by:** S1 worked sample, 2026-08-30


Two significance thresholds live in `_determine_route` and only the stricter one is documented anywhere: `_SIG_THRESHOLD = 0.10` gates IC significance (`prescreen_signal.py:87`), while a second `p > 0.05` test inside the cost branch decides `kill_cost_hurdle` vs `refine_cost_hurdle` (`:1042`). Neither §2.2 nor §3 mentions either number.


**Proposed disposition (S3 decides, not this file):** Document both thresholds and what each decides.


---

## E037-09

**Severity:** medium · **Type:** doc-vs-doc · **Status:** open, untriaged

**Lands on:** `strategy-research/CLAUDE.md`

**Found by:** S1 worked sample, 2026-08-30


`strategy-research/CLAUDE.md` — loaded into every session in this directory — contradicts `USER_GUIDE.md` twice. (a) It lists a **10-stage** workflow (`screening_backtest`, `walk_forward_validation`, `final_holdout_test`, `robustness_analysis`, `research_decision`) that does not match the guide's canonical 13 stages; four of those five names exist nowhere in the guide. (b) Its global rule "Validate outputs against schemas before moving to the next stage" asserts exactly the schema enforcement that §3's own 2026-08-27 correction records as **false**. The guide's §2 preamble claims to be "the only place that is maintained as authoritative", but the file an agent reads *first* says something else. Out of scope to fix here; noted because S4's cross-linking work has to decide whether `CLAUDE.md` points at the guide or restates it.


**Proposed disposition (S3 decides, not this file):** Decide whether CLAUDE.md points at USER_GUIDE.md or restates it. It currently restates it wrongly, and it is what an agent reads first.


---

## E037-10

**Severity:** **high** · **Type:** code-defect · **Status:** open, untriaged

**Lands on:** `strategy-research/tools/episode_significance.py:209 (+ :59)`

**Found by:** S1 worked sample, 2026-08-30


**A stale hardcoded `24` survives in the A8.5.1a label, and a real run proves it.** `prescreen_signal.py:1371-1376` records that the method label used to read `block_24_fisher_z` while `block_size` had become a derived per-timeframe value, and that this was fixed on 2026-08-28 so "the name is what a later reader reconstructs the method from; it has to track the arithmetic." That fix was applied to the **default path only**. The A8.5.1a dense-fallback branch still returns the hardcoded string `"block_24_dense_fallback"` (`tools/episode_significance.py:209`) while passing the derived `block_size` into `_block_adjusted_significance`. `runs/run_060/artifacts/prescreen_result.yaml` (2026-08-28) carries `significance_methodology_used: block_24_dense_fallback` next to `ic_significance_block24.block_size: 6` — the artifact asserts 24 and the arithmetic used 6, which is exactly the defect the comment claims closed. **Not a one-line fix:** the literal is also a member of `VALID_METHODS` (`episode_significance.py:59`), which the orchestrator's F4d conformance gate matches against, so the label and the gate must change together.


**Proposed disposition (S3 decides, not this file):** Derive the label from block_size, and update VALID_METHODS and the F4d conformance gate in the same change. Needs a decision on already-archived artifacts carrying the wrong label.


---

## E037-11

**Severity:** medium · **Type:** code-fragility · **Status:** open, untriaged

**Lands on:** `strategy-research/workflow/run_phase1_research.py:3237 (+ the stamp site)`

**Found by:** S1 worked sample, 2026-08-30


`protocol_version` is stamped as a **platform-dependent path string**. run_060 recorded `protocols\funding_mr_4h_retest_v1.json` with a Windows backslash. `_check_prescreen_conformance` compares it by bare filename via `Path(executed_identity).name` (`run_phase1_research.py:3237-3241`); on Windows that yields `funding_mr_4h_retest_v1.json`, but on macOS/Linux `PosixPath` does not treat `\` as a separator, so `.name` returns the **entire string** and the pre-registration check reports a spurious violation. Reachability, stated honestly: within a single run the artifact is produced and checked on the same machine, so this does not bite today. It bites when an artifact crosses platforms — which is precisely the dual-writer research model the fork operates under, and the fork's standing rule is that Mac and Windows results should be identical.


**Proposed disposition (S3 decides, not this file):** Normalise protocol_version to a POSIX-style relative path at write time, or compare by basename in a separator-agnostic way.


---

## E037-12

**Severity:** medium · **Type:** doc-unresolvable-reference · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` (whole document)

**Found by:** S1 review follow-up, 2026-08-30

`USER_GUIDE.md` cites **14 distinct amendment codes across 26 mentions**
(`A1.1`, `A1.3`, `A1.4`, `A2.1`, `A2.2`, `A2.3`, `A3.4`, `A3.6`, `A5.3`,
`A6.1`, `A6.2`, `A8.1`, `A8.6`, `A9.1`) and **never once says where any of
them is defined**. The definitions live in
`engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md`, a file
the guide does not reference at any point — verified by grep for
`AMENDMENT` across all 976 lines: zero hits. A reader who meets "records
trial in `campaign_state.trial_sharpes` (A6.2)" has no path to what A6.2
actually says, which is that deflated Sharpe needs the *variance* across
trials and therefore every evaluation counts as a trial, kills included.
That reason is the entire justification for the sentence, and it is one
unreferenced file away.

This is the epic's central complaint in miniature — the knowledge exists and
is correct, but cannot be assembled from one place. It is also a known
failure mode with a recorded incident: **C4, "Rule-citation confabulation"**
(`engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md:216`) records a
card citing *"A3.6, n_episodes >= 8 per window"* where the label was wrong
(the real rule was A8.5.1a-spec rule 3) and the qualifier was invented, and
concludes: *"Plausible-looking fake citations survive until someone quotes
the source verbatim."* Its prescribed fix was a machine-readable rule index
(id → verbatim text → source line) plus a lint step. **No such index exists**,
and the guide is the document most likely to be cited from.

Note: S1's own first draft reproduced the defect — it used `A6.2` four times
without ever expanding it. That is how cheaply this propagates.

**Proposed disposition (S3 decides, not this file):** Either add a rule index
(id → one-line gloss → `file:line`) to `USER_GUIDE.md` §6 and link every
citation to it, or at minimum reference `AMENDMENTS_01-06.md` once and gloss
each code on first use. The S1 stage template now requires the gloss-and-link
on first use within a block; that convention is worth applying guide-wide.

---

## E037-13

**Severity:** medium · **Type:** wrong-citation · **Status:** open, untriaged — needs the author's confirmation

**Lands on:** `strategy-research/tools/prescreen_signal.py:1089`, `:1100`, `:1580`

**Found by:** S1 review follow-up, 2026-08-30

Three sites label the `ungated_escape_eligible` write-back as an "A9.1 side
effect": the section comment at `:1089`, the `_resolve_ungated_escape`
docstring at `:1100`, and the call site at `:1580`.

**A9.1 as defined** (`AMENDMENTS_01-06.md:156`) is *"Named must-reject
fixture: `keltner_163`"* — an Improvement 09 acceptance criterion requiring
the cost gate to reject the Keltner config despite its passing IC. It says
nothing about ungated escape. There is exactly one `A9.1` heading in the
repository, so this is not a renumbering collision — verified by grep across
all markdown.

The rules that **do** govern the behaviour are cited correctly in the same
docstring's body: A2.1 (detector-confidence deadlock escape) supplies the
`ungated_escape_eligible` concept, and A2.3 rule 5 supplies the requirement
that the metric be all-bars IC. So the docstring contradicts its own heading.

Stated fairly: the same file uses A9.1 **correctly** at five other sites
(`:20`, `:1607`, `:1614`, `:1651`, `:1656`), all about the keltner_163
two-stage rejection. This looks like a label attached to the wrong paragraph
rather than a systematic misunderstanding, and it has **no runtime effect** —
it is comment text. It is recorded because it misleads readers and because
S1 propagated it into the documentation before catching it, which is exactly
the C4 pattern described in [E037-12](#e037-12).

**Proposed disposition (S3 decides, not this file):** Confirm with the author
whether A9.1 was intended, then relabel the three sites to A2.1 / A2.3 rule 5
if not. Cheap to fix, but it is a citation correctness question, so it should
be answered rather than guessed.

---

## E037-14

**Severity:** medium · **Type:** phantom-field · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md:613`

**Found by:** S1 information-loss check, 2026-08-30

`USER_GUIDE.md:613` documents the `cost_check` field as
`{pass: bool, edge_to_cost_ratio, required_gross_edge_bps}`.
**`required_gross_edge_bps` does not exist.** It is emitted by no Python file
in the repository — verified by grep across `strategy-research/` and
`trading-bot/` — and it is absent from every real artifact, including
`runs/run_060/artifacts/prescreen_result.yaml`.

The dict the code actually emits has **eight** keys: `symbol`,
`implied_trades_per_window`, `estimated_gross_edge_bps_per_trade`,
`cost_bps_per_trade`, `edge_to_cost_ratio`, `safety_factor_required`, `pass`,
`ic_used`. So the guide names three keys, one of which is imaginary, and omits
six real ones — including `safety_factor_required`, which is the threshold the
gate compares against, and `ic_used`, which records *which* IC fed the
estimate.

**How it was found is the point.** This did not turn up by reading the guide;
it turned up because the epic's own information-loss check flagged
`required_gross_edge_bps` as a token that disappeared between drafts. The
check asked "where did this fact go?", and the answer was "it was never a
fact." A mechanical residue check catches phantom content as well as lost
content — an argument for running it on every S2 and S4 section rather than
treating it as a formality.

**Proposed disposition (S3 decides, not this file):** Replace the three-key
description with the real eight, or mark it explicitly as a partial list.
Worth checking the other artifact entries for the same defect during S2 —
this one was invisible until an artifact was opened.

---

## E037-15

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.2 · `strategy-research/workflow/run_phase1_research.py:88`

**Found by:** S2, 2026-08-30

The guide numbers **13 stages**. The engine's own registry, `STAGE_CONFIGS`
(`run_phase1_research.py:88`), has **10 entries**. Three of the guide's stages
are not in it:

- **stage 1 `research_brief`** — a human input, not an orchestrator stage.
- **stage 9 `regime_detector_validation`** — a helper function, see [E037-17](#e037-17).
- **stage 10 `regime_auditor`** — never dispatched at all, see [E037-16](#e037-16).

Separately, **stage 4 is named `validation` in code and `validation_gate` in
the guide** (`STAGE_CONFIGS["validation"]`, `determine_post_validation_route`,
`_SKILL_MAP["validation"]`). The guide uses `validation_gate` in §2.1, §2.2 and
§2.3. Neither name is wrong, but only one is the key you would grep for.

This matters for the epic's core purpose: a reader trying to trace "which
sub-steps does my change reach?" cannot map the guide's numbering onto the
code's dispatch table.

**Proposed disposition (S3 decides, not this file):** Mark which entries are
engine stages and which are not, and give stage 4 both names.

---

## E037-16

**Severity:** high · **Type:** stage-does-not-run · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.1 and §2.2 (stage 10)

**Found by:** S2, 2026-08-30

**The guide documents `regime_auditor` as an automated Claude stage. The
orchestrator never dispatches it.**

- It is absent from `STAGE_CONFIGS` (`:88`), so it is never a `current_stage`.
- It is absent from `_SKILL_MAP` (`:689`), which maps the **7** dispatchable
  Claude stages. `_build_stage_prompt` raises `ValueError(f"No SKILL file
  mapped for stage: {stage_name}")` for anything not in that map (`:711`), so
  it could not be dispatched even if it were reached.
- **No code writes `regime_audit_decision.yaml`.** The orchestrator only
  *reads* it if it happens to exist (`:6251`, `:6382`), and the only writer
  anywhere is `prescreen_signal.py:1118`, which updates an existing file and
  returns early if there is none.

What actually happens: on the `regime_misattribution` path the pipeline
**pauses for a human** (`status="paused_for_human"`) and prints *"consult
regime-auditor skill and regime_detector_report.yaml"* (`:5788-5796`). The
skill at `workflow_artifacts/skills/regime-auditor/` is real; it is invoked by
a person, not the engine, and only on that one path.

§2.1's map draws it inline between stages 9 and 11 as if it always runs, and
§2.2 gives it Engine = *Claude*, which reads as automated.

**Consequence:** every downstream statement that assumes
`regime_audit_decision.yaml` exists — including the A2.2 retune firewall check
and stage 7's `ungated_escape_eligible` write-back — is conditional on a human
having produced it. Nothing says so.

**Proposed disposition (S3 decides, not this file):** Re-label stage 10 as a
human-invoked skill on a paused pipeline, or make it a real stage. This is a
design question, not a wording fix.

---

## E037-17

**Severity:** medium · **Type:** silent-no-op · **Status:** open, untriaged

**Lands on:** `strategy-research/workflow/run_phase1_research.py:2410`
(`_ensure_regime_detector_report`)

**Found by:** S2, 2026-08-30

Stage 9 is a helper called from inside the `verdict_interpreter` stage
(`:6250`, `:6381`), not a registry stage. Three facts about it that the guide
does not carry:

1. **It can silently do nothing.** If `candidate_strategy_config.json` is
   missing it prints a warning and returns `None` (`:2433-2434`); if
   `validate_regime_detector.py` exits non-zero it prints and returns `None`
   (`:2445-2447`). Neither raises. The verdict then proceeds with no detector
   report, and the only trace is stdout.
2. **The report is campaign-level, not per-run.** It is written to
   `ROOT / "regime_detector_report.yaml"` — one file shared by every run.
   §3 does not say this, and the artifact's placement implies per-run.
3. **"Stale" means older than 30 days** (`:2425`), a threshold documented
   nowhere.

Point 1 sits badly next to the project's own standing rule that anything
feeding decisions should raise on degenerate inputs — the rule that produced
the run_060 guards in `prescreen_signal.py`.

**Proposed disposition (S3 decides, not this file):** Document all three.
Whether the silent return should raise is a separate code decision.

---

## E037-18

**Severity:** high · **Type:** unenforced-rule · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.2 (stage 3)

**Found by:** S2, 2026-08-30

§2.2 states stage 3 **"Must: pass real-diversity check (≥2 `library_category`
OR `data_requirements`; cosmetic = rejected)."** That reads as a mechanical
gate. **Nothing enforces it.**

`library_category` appears exactly **once** in all of `workflow/` and `tools/`
— inside a prompt string at `run_phase1_research.py:490`. No code reads the
field from `expanded_hypothesis_card.yaml`, counts distinct categories, or
rejects an expansion. The rule lives entirely in
`workflow_artifacts/skills/innovation-expansion/SKILL.md:74-105`, as an
instruction to the model, including the `diversity_audit` block the model is
asked to self-report with `verdict: real_diversity`.

So the "check" is the model grading its own homework, and "cosmetic =
rejected" describes an outcome no code can produce.

This is the **same defect class** the guide already corrected once: §3's
preamble was fixed on 2026-08-27 after "all artifacts are validated against
JSON schemas" turned out to be false. The pattern is a stated guarantee whose
enforcement was never built — and the guide's phrasing ("Must:", "rejected")
is what makes it look built.

**Proposed disposition (S3 decides, not this file):** Restate as
skill-guidance, or build the check. Worth a sweep of every other "Must:" in
§2.2 for the same pattern — this is now two confirmed instances of a stated
guarantee with no enforcement, which makes it a class, not an incident.

---

## E037-19

**Severity:** high · **Type:** missing-artifacts · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3

**Found by:** S2, 2026-08-30

§3 presents itself as the catalogue of pipeline artifacts — *"Artifacts are
YAML files produced and consumed by pipeline stages. They are the only
communication channel between stages."* **Five real ones have no entry.**
Counts are files on disk under `runs/`, measured 2026-08-30:

| Artifact | On disk | Why it matters |
|---|---|---|
| `pass_rule_evaluation.yaml` | 2 | **The decision authority.** Written by stage 8 via `tools/verdict_criteria_evaluator.py`, and a **REQUIRED input** to verdict_interpreter — its SKILL.md says so at line 16 and treats a verdict contradicting it without flagging as a conformance failure. C7/K2 kernel, 2026-07-13: it *replaced* `evaluate_against_decision_rules` as the authority, which is now informational only. |
| `pre_registration.yaml` | 10 | Carries the pre-registered `pass_rule` that the above evaluates, and the `machine_constraints` block — which is not a separate file, but the thing that pins stage 7's significance methodology before the prescreen subprocess reads the config. |
| `run_context.yaml` | 14 | Per-run protocol binding; holds the bare-filename `protocol` key the prescreen conformance gate compares against (`run_phase1_research.py:3013`). |
| `human_resolution.yaml` | 4 | Required to resume a pipeline paused at `paused_for_human` — the state the `regime_misattribution` path leaves it in (see [E037-16](#e037-16)). Without it, a paused campaign cannot restart, and nothing in the guide names it. |
| `config/venue_tradability.yaml` | config | Single source of truth for the holdout tradability gate (`run_campaign.py:196`). §3's "Config files" addendum lists eight config files and not this one. |

The pattern is that **the artifacts added most recently are the ones missing**
— the C7/K2 kernel (2026-07-13), the E-015 venue gate, the human-pause path.
§3 documents the pipeline as it was, and additions did not come with an entry.
That is the accretion the epic was raised about, visible as a measurable gap
rather than a feeling.

`pass_rule_evaluation.yaml` is the serious one: an operator reading §3 to
learn how a verdict is reached will find `protocol_result.yaml` and
`verdict_interpretation.yaml` and conclude the LLM decides from the backtest.
Since 2026-07-13 a machine-authored verdict has been the authority, and it is
invisible here.

**Proposed disposition (S3 decides, not this file):** Add all five. Then check
whether any other post-2026-07 artifact is missing — the sample here is five
of five recent additions, so a sweep is warranted rather than optional.

---

## E037-20

**Severity:** medium · **Type:** inconsistent-metadata · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3

**Found by:** S2, 2026-08-30

The EPIC recorded that §3's metadata is inconsistent. Measured, it is worse
than "inconsistent" — **two incompatible conventions coexist**, and one of them
carries no provenance at all. Counts over the 28 pre-S2 entries:

| Metadata line | Entries carrying it |
|---|---|
| `Created by` | 23 of 28 |
| `Read by` | 23 of 28 |
| `Schema` | 7 of 28 |
| **`Updated by`** | **2 of 28** (`pipeline_state.yaml`, `campaign_state.yaml`, both as "Created by / Updated by") |

**Five entries have no metadata whatsoever** — `variant_selection.yaml`,
`variants_not_pursued.yaml`, `exclusion_digest.yaml`,
`anti_adjacency_result.yaml`, `schedulability.yaml`. They open with an
`**Objective:**` prose line instead. For those five a reader cannot determine
who writes the file, who reads it, or whether a schema exists.

Two observations that matter more than the counts:

1. **The `Objective:` convention is not an error, it is a second design.**
   Those five are the E-025/E-026-era additions, and their `Objective:` line is
   doing exactly the job the EPIC's "rationale headliner" asks for. Two people
   solved the same problem twice without noticing, which is the accretion
   pattern this epic exists to stop. **S2 deliberately did not rewrite them** —
   silently normalising would have destroyed the evidence that the split
   happened.
2. **`Updated by` at 2 of 28 is why [E037-07](#e037-07) was invisible.** Stage 7 rewrites
   `regime_audit_decision.yaml` in place, and that entry has no `Updated by`
   line — but neither does almost anything else, so its absence signalled
   nothing. A field that is nearly always missing cannot carry information by
   being missing.

**What S2 did do:** added a `Why this file exists` headliner to the 22 entries
lacking one (the five `Objective:` entries already had the equivalent), and
gave all five new artifact entries the full five-line block. §3 now has 27
headliners across 33 entries.

**Proposed disposition (S3 decides, not this file):** Pick one convention and
migrate the other, preserving both texts where they differ in content. Fill
`Updated by` everywhere, including the explicit `*(none — write-once)*` case,
so its absence stops being meaningless.

---

## E037-21

**Severity:** high · **Type:** documents-inactive-machinery · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3

**Found by:** S2, 2026-08-30

§3 documents five artifacts as part of the pipeline. **None of them is
produced by any run, because each sits behind a feature flag, and every
orchestrator flag is off.** Read from `config/campaign_config.yaml`,
2026-08-30:

| Flag | Value | Artifact it gates |
|---|---|---|
| `orchestrator.variant_selection_record.enabled` | `false` | `variant_selection.yaml`, `variants_not_pursued.yaml` |
| `orchestrator.variant_anti_adjacency_gate.enabled` | `false` | `anti_adjacency_result.yaml` |
| `orchestrator.exclusion_digest_input.enabled` | `false` | `exclusion_digest.yaml` |
| `orchestrator.schedulability_block.enabled` | `false` | `schedulability.yaml` |
| `orchestrator.anti_adjacency_retry.enabled` | `false` | — (routing behaviour) |
| `orchestrator.stale_input_path_fix.enabled` | `false` | — (input-path behaviour) |

Instance counts on disk confirm it: `variant_selection.yaml` **0**,
`variants_not_pursued.yaml` **0**, `anti_adjacency_result.yaml` **0**,
`schedulability.yaml` **0**, against 103 `hypothesis_card.yaml` and 119
`pipeline_state.yaml`. (`exclusion_digest.yaml` has exactly one, at
`campaign_record/`, not under any run.) The single hits an unqualified `find`
returns for the others are their **schema files**, not instances.

**This is not a defect.** Shipping a new feature off-by-default with a
bit-identity proof is the project's own discipline, and these flags are that
discipline working. The defect is that §3 presents the output of unshipped
machinery indistinguishably from the artifacts every run actually writes, and
never mentions the flags.

**It also explains [E037-20](#e037-20).** The five entries with no `Created by` /
`Read by` / `Schema` metadata are **exactly** the five flag-gated artifacts —
a one-to-one match, not an overlap. They were written as design records for
features that then shipped disabled, using an `**Objective:**` convention
suited to a design note rather than to a catalogue entry. E037-20's "two
conventions" and E037-21's "inactive machinery" are the same event seen twice.

**Consequence for an operator:** someone reading §3 to learn what a run
produces will look for `variant_selection.yaml` in the run directory and not
find it, with nothing in the guide explaining why. Someone auditing trial
counting will believe an anti-adjacency gate is filtering candidates. It is
not.

**Proposed disposition (S3 decides, not this file):** Mark the flag-gated
entries as such, with the flag name and its current value, and state that the
value is read at runtime rather than baked in. S2 has added a §3 subsection
doing this as an interim.

---

## E037-22

**Severity:** high · **Type:** phantom-fields · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3, `verdict_interpretation.yaml`

**Found by:** S2 loss check, 2026-08-30

**The entire field table for `verdict_interpretation.yaml` describes fields
that are not in that artifact.** Measured across the **39** real files on disk:

| Documented field | Occurrences in 39 real files |
|---|---|
| `altitude` ("numeric altitude of the decision, 1 = refine, 2 = pivot, 3 = escalate") | **0** |
| `verdict` ("`refine`, `pivot`, `escalate`, `promote`, or `kill`") | **0** |
| `diagnostic_rule_applied` ("which named diagnostic rule triggered this, e.g. `cost_drag`, `signal_inversion`") | **0** |
| `parameter_bracket` ("[min, max, step] range to search next") | **0** |
| `next_altitude` ("fallback altitude if the current verdict fails again") | **0** |
| `root_cause` | 11 |

The fields the artifact actually carries — `status` (34 of 39),
`hypothesis_verdict`, `lineage_routing`, `criteria_summary`,
`untested_criteria`, `primary_failure_mode`, `hypothesis_family`,
`proposed_change_dimension`, `altitude_justification`, `config_to_failure_map`,
`prescreen_evidence` — were **none of them documented**.

> ### ⚠️ Corrected 2026-08-31 — this finding overclaimed
>
> The table above is right: none of those five is in
> `verdict_interpretation.yaml`. But the original wording, *"fields that no
> artifact has ever contained"*, was **wrong for four of the five**. Re-measured
> across every artifact, at every depth:
>
> | Field | In `verdict_interpretation.yaml` | Actually lives in |
> |---|---|---|
> | `verdict` | 0 | `protocol_result.yaml` — 31 files, populated |
> | `diagnostic_rule_applied` | 0 | `findings_carryover.yaml` — 31 files, populated (e.g. *"Rule 2: Signal has no directional edge"*) |
> | `next_altitude` | 0 | `findings_carryover.yaml` — 30 files, populated |
> | `parameter_bracket` | 0 | `findings_carryover.yaml` — 14 files, 2 of them non-null |
> | **`altitude`** | 0 | **nowhere — the only genuine phantom** |
>
> **The defect is misfiling, not invention**, and that is a materially different
> and more fixable thing. The cause was my own tool: the audit inspected only
> **top-level** keys, so "not a top-level key of this file" was reported as
> "does not exist anywhere". Found by pulling on a glossary entry
> ([E037-30](#e037-30)), not by review.

One of six documented fields is a genuine phantom, four were misfiled, and eleven real ones were missing.
This is [E037-14](#e037-14) again at whole-table scale: E037-14 was one phantom key inside
`cost_check`; this is an entire entry describing an intended design rather than
the artifact.

**Two consequences worth separating.** As documentation it is simply wrong. But
the router reads `status` with a fallback to `protocol_verdict`
(`run_phase1_research.py:5762`) — **not** `verdict`, the field this entry names
— so anyone writing a consumer from the guide would read a key that is never
present and get `None`.

**How it was found:** not by reading. S2 replaced the table with one built from
run_060, and the mechanical loss check flagged `altitude`, `verdict`,
`diagnostic_rule_applied`, `parameter_bracket` and `next_altitude` as tokens
that had vanished. Checking where they went is what established they had never
been anywhere. The descriptions are now preserved in the entry as intended
design, explicitly marked as absent.

**Proposed disposition (S3 decides, not this file):** Decide whether the
documented design was abandoned or never built, then either implement or
retire it. The prose is worth keeping either way — it is the only record of
what the altitude system was meant to look like.

---

## E037-23

**Severity:** medium · **Type:** phantom-values + unhandled-status · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3 (`decision.yaml`) ·
`strategy-research/workflow/run_phase1_research.py:6030`

**Found by:** S2 loss check, 2026-08-30

Two things, one measurement. Across the **39** real `decision.yaml` files:

| Status | Count |
|---|---|
| `spec_ready` | 38 |
| `validation_incomplete` | 1 |
| `approved` | 0 |
| `blocked` | 0 |

1. **The guide's documented values are phantom.** §3 said status is
   "`approved`, `blocked`, etc." Neither has ever occurred, and neither is in
   the router's `KNOWN_STATUSES = {"spec_ready", "component_gap"}`.
2. **A real run produced a status the router does not know.**
   `validation_incomplete` is in neither the guide nor `KNOWN_STATUSES`, so
   that run hit the fail-closed branch and paused for a human with *"UNEXPECTED
   STATUS … SKILL.md may need a new status case"*. The fail-closed design
   worked exactly as intended — this is the guard doing its job, and it is
   evidence that the skill emits statuses nobody enumerated.

Note the asymmetry with [E037-18](#e037-18): here the code fails closed on an
unrecognised value, while stage 3's diversity rule has no enforcement at all.
The engine is not uniformly permissive — it is strict in some places and absent
in others, and the guide does not distinguish them.

**Proposed disposition (S3 decides, not this file):** Correct the documented
values to `spec_ready` / `component_gap`, and decide whether
`validation_incomplete` should become a known status or remain a pause.

---

## E037-24

**Severity:** high · **Type:** phantom-fields (systemic) · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §3 — five entries

**Found by:** S2 mechanical audit, 2026-08-30

[E037-22](#e037-22) was not an isolated bad entry. Auditing **every** §3 field table
against **every** matching artifact on disk shows the same defect in five
entries. Reproduce with
[`E-037/tools/audit_field_tables.py`](tools/audit_field_tables.py).

| Entry | Real files | Documented fields never present | Rate |
|---|---|---|---|
| `escalation_request.yaml` | 7 | `target_symbol`, `target_timeframe`, `rationale` | **3 of 3** |
| `protocol_result.yaml` | 38 | `per_window_metrics`, `per_symbol_metrics`, `per_regime_metrics`, `promotion_criteria`, `diagnostic_metrics` | **5 of 7** (corrected) |
| `verdict_interpretation.yaml` | 39 | `altitude`, `verdict`, `diagnostic_rule_applied`, `parameter_bracket`, `next_altitude` | 5 of 6 — [E037-22](#e037-22) |
| `regime_detector_report.yaml` | 1 | `persistence_score`, `activation_rate` | 2 of 8 (corrected) |
| `regime_audit_decision.yaml` | 1 | `retune_firewall_check` | 1 of 3 |

> **Corrected 2026-08-31.** Two entries in the table above were overstated,
> for the same reason as [E037-22](#e037-22): the audit read only top-level
> keys. **`median_sharpe` is present** in `protocol_result.yaml` (31 of 38,
> nested) and **`class_conditional_sensitivity` is present** in
> `regime_detector_report.yaml` (nested). Both have been removed from the
> counts and from the test baseline. The tool now walks every depth.
>
> The rest of the finding stands, and the three bullets below were always
> checked by hand rather than taken from the tool.

**The remaining ones are not a nesting artefact — the names themselves are
wrong.** Checked individually:

- `escalation_request.yaml` really carries `target`, `reason`,
  `proposed_capability`. The documented names are different words for the same
  three concepts.
- `regime_detector_report.yaml` really nests its metrics under
  `per_symbol_per_timeframe[].metrics` as
  `regime_persistence_median_bars`, `class_conditional_sensitivity_per_label`
  and `trending_activation_rate` — different names *and* a different shape.
- `protocol_result.yaml` really carries `hypothesis_verdict`,
  `per_symbol_summary`, `results`, `source`, `prescreen_route`,
  `prescreen_kill_reason`. Six of the seven documented names describe a
  structure the file does not have.

**What this means.** §3's field tables were written from **intended design**,
not from artifacts, and were never re-checked against output. That is the
same root as [E037-14](#e037-14) (`required_gross_edge_bps`, a `cost_check` subkey no
code emits) and [E037-21](#e037-21) (entries for flag-gated features that never ran).
The guide is not so much out of date as never having been reconciled with
reality in this section.

**`protocol_result.yaml` is the one that matters operationally.** It is the
backtest result — the evidence every verdict rests on — and an operator
reading §3 would look for `median_sharpe` and `per_window_metrics` and find
neither.

**Method note.** This was found mechanically, in one pass, after [E037-22](#e037-22)
suggested the class might be systemic. The audit is cheap and repeatable;
running it is a better acceptance gate for S2 and S4 than any amount of
careful reading. Its limitation is honest: it detects *documented-but-absent*
keys, and cannot tell a renamed field from a deleted one — that distinction
needed a human read of each artifact, which is what the three bullets above
are.

**Proposed disposition (S3 decides, not this file):** Rewrite the five tables
from real artifacts, preserving the old names as intended-design notes rather
than deleting them (the treatment already applied to
`verdict_interpretation.yaml`). Then add
`tools/audit_field_tables.py` to whatever gate S4 lands behind, so the tables
cannot silently drift again.

---

## E037-25

**Severity:** medium · **Type:** incomplete-index · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §5

**Found by:** S2, 2026-08-30

§5 is titled "Tools & Scripts" and documents **3 of the 22** Python files in
`tools/`. The omissions include the two most load-bearing tools in the
repository:

- **`tools/prescreen_signal.py`** — implements stage 7 in its entirety.
- **`tools/verdict_criteria_evaluator.py`** — produces
  `pass_rule_evaluation.yaml`, the decision authority since 2026-07-13
  (see [E037-19](#e037-19)).

Also absent: `power_check.py` (the A8.6 gate), `deflate_sharpe.py` (the DSR
gate before the holdout), `validate_regime_detector.py` (stage 9),
`episode_significance.py` (the A8.5.1a path, and the site of
[E037-10](#e037-10)), `timeframe.py` (the single source of `bars_per_day`, whose
enumerated predecessor caused the 4h `n_eff` bug), and `cache_gap_census.py`
(which stage 7's own notes tell the reader to run).

**The composition is what makes this a finding rather than a gap.** §5 has a
32-line entry for `workflow/stages.yaml`, explicitly marked *"ARCHIVED
2026-08-24 (never read by the orchestrator)"* — a longer treatment than any
live tool receives, while the tool implementing a pipeline stage has none.
The section documents what someone once wrote about, not what runs.

**Not every omission is equally serious.** `panel_backtester.py` is explicitly
research-only and out of the production path; `whale_footprint_evaluation.py`
is one hypothesis's harness. The argument is not that all 22 need prose — it
is that a section presenting itself as the tools index should be an index.

**Proposed disposition (S3 decides, not this file):** S2 has added a complete
inventory table with a one-line purpose each, grouped by role. S3 decides which
deserve full entries. Consider whether the archived `stages.yaml` entry should
shrink to a pointer.

---

## E037-26

**Severity:** high · **Type:** code-regression · **Status:** open, untriaged —
**red on any machine with the data cache; green in CI, which skips it**

**Lands on:** `strategy-research/tools/prescreen_signal.py:1320`

**Found by:** S3, 2026-08-31, running the suite before landing an unrelated change

`tests/test_prescreen_no_signal_artifact.py::test_component_errors_route_to_no_signal_artifact`
**fails on `origin/master`**. Verified by checking the commit out directly, not
inferred — it is not caused by any E-037 work, all of which is documentation.

> **Corrected 2026-08-31, same session.** This entry first said "the test suite
> is currently RED on `origin/master`" without qualification. That was
> incomplete in a way that matters: **GitHub Actions reports master green**
> (`gh run list --branch master` → `success`). The test carries
> `@pytest.mark.skipif(not (trading-bot/local_data/BTCUSDT_1h.csv).exists())`
> and `local_data/` is untracked, so on a CI runner it **skips** rather than
> passes. It fails only where the data cache exists — a developer machine. The
> defect is real, and the green tick is not evidence against it. See
> [E037-27](#e037-27) for why nothing catches this class.

### What broke

The run_060 zero-data guard (`:1320`, added 2026-08-28 in `58e3c21e`) raises
**before** the F5c component-error override (`:1481`) can run. The two now
contradict each other:

| Step | Line | Behaviour |
|---|---|---|
| Zero-data guard | `:1320` | `if not any(all_records_by_symbol.values()): raise RuntimeError` |
| F5c override | `:1481` | if `active_n == 0` **or** component-error rate > 5% → `route = no_signal_artifact`, `kill_reason = component_error` |

When a component throws on **every** bar, `records` is empty, so
`all_records_by_symbol[symbol] == []`, so the guard raises and `:1481` is
unreachable.

### Why it matters more than a red test

**F5c exists to stop an engineering failure being scored as a scientific
result.** Its own comment records the incident: run_044 (2026-07-04), where a
`FundingRateMeanReversionComponent` divide-by-zero produced `active_n_bars=0`,
which read as a genuine `kill_no_ic` and *"nearly closed an otherwise-untested
hypothesis family."* The component-error branch of that safety net is now
unreachable.

The failure mode is loud rather than silent — a `RuntimeError`, not a false
kill — so it is **not** currently producing wrong verdicts. But the guard's
premise is wrong in this case, and the message says so:

> `RuntimeError: Prescreen loaded NO usable data for any of 1 symbol(s) ...
> Reasons: no symbols requested`

**Both clauses are false.** The run loaded **168 bars** for BTCUSDT — stdout
says so two lines earlier. And a symbol *was* requested; `skipped_symbols` is
empty precisely because loading succeeded, so the detail string falls through
to its "no symbols requested" default. An operator hitting this is told to go
look at data availability, when the actual cause is a throwing component.

### The distinction the guard misses

Its comment draws the right line and then applies it too widely:

> *"'no_signal_artifact' asserts a signal did not activate ON DATA, and nothing
> was tested here."*

Correct for the run_060 case — **no data loaded**. Wrong here: data loaded
fine and the component failed on it. That is exactly the case F5c was built
for, and the two conditions are distinguishable — `n_bars_total > 0` with
`total_component_error_count > 0` is a component failure, not a data failure.

**Proposed disposition (S3 decides, not this file):** Make the `:1320` guard
fire only when no data was *loaded*, letting the component-error case reach
F5c. Fix the "no symbols requested" message to report the real reason.
Whichever way it is resolved, **master should not stay red** — this is the
first item in the triage that is failing right now rather than merely wrong.

---

## E037-27

**Severity:** high · **Type:** gap-in-the-gate · **Status:** open, untriaged

**Lands on:** `.git/hooks/pre-commit` (versioned at
`strategy-research/tools/hooks/pre-commit`) · `.github/workflows/tests.yml`

**Found by:** S3, 2026-08-31, while explaining why [E037-26](#e037-26) is red locally
and green in CI

**A class of test runs in neither gate.** Not "runs rarely" — neither.

| Gate | Runs `trading-bot/tests/` | Runs `strategy-research/tests/` | Has `local_data/` |
|---|---|---|---|
| pre-commit hook | **yes** | **no** — it does `cd "$ROOT/trading-bot"` then `pytest tests/` | yes (developer machine) |
| GitHub Actions | yes | **yes** | **no** — `local_data/` is untracked |

So a `strategy-research` test guarded by
`@pytest.mark.skipif(not <a local_data file>.exists())` is **skipped in CI** for
want of data and **never invoked** by the commit hook. It runs only when a human
types `pytest` in `strategy-research/` on a machine that has the cache.

**Measured 2026-08-31:** 10 such guards across 4 files, out of 802 test
functions in `strategy-research/tests/` —
`test_prescreen_no_signal_artifact.py`, `test_a851a_prescreen_integration.py`,
`test_near_miss_scoreboard.py`, `test_holdout_date_gate.py`.

**Why these are the worst ones to lose.** They are a small share of the suite,
but they are the tests that drive the real engine over real bars. A synthetic
unit test cannot catch [E037-26](#e037-26): the guard that broke it fires on the
interaction between data loading, gap suppression and the F5c override, and
that interaction only exists with data.

**Consequence, plainly.** A green tick on a PR does not mean the prescreen still
routes correctly. E037-26 sat on master with CI green, and it surfaced only because
S3 ran the full suite by hand before landing an unrelated documentation change.

**Not the same as the fork's worktree note.** `CLAUDE.fork.md` records that
worktrees run 2 fewer fast tests without the copyable cache set — that is about
*worktrees*. This is about CI and the commit hook, where the same cause has a
larger effect and nothing is written down.

**Proposed disposition (S3 decides, not this file):** three options, cheapest
first — (a) make the pre-commit hook run both suites, closing the local half at
the cost of a slower commit; (b) commit a small fixture cache so these tests can
run in CI; (c) fail the CI step if more than N tests skip, so silent erosion is
visible. (a) and (c) are cheap and independent; (b) is the only one that makes
CI actually cover the class, and needs a decision about committing data.

---

## E037-28

**Severity:** low · **Type:** stale-count · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §6, the `Run` glossary entry

**Found by:** S4, 2026-08-31, while cross-linking the glossary

§6 defines a **Run** as *"One complete execution of the 10-stage pipeline."*
The guide documents **13** numbered stages in §2.2.

Ten is not arbitrary — it is exactly the size of `STAGE_CONFIGS`, the engine's
dispatch registry, which excludes the human `research_brief` and the two regime
stages (see [E037-15](#e037-15)). So the glossary silently uses the *engine's* count
while §2.1 and §2.2 use the *documented* count, and nothing reconciles them.

It is also the same number as the stale ten-item stage list found in
`strategy-research/CLAUDE.md` ([E037-09](#e037-09)), though with different members — so
"10 stages" now means at least two different things across the repo's own docs.

Low severity: nobody makes a decision on this number. Recorded because it is
the third instance of the same pattern — a count restated in a second place and
never re-synced — and because the fix is one word once someone decides which
count the glossary should quote.

**Proposed disposition (S3 decides, not this file):** state both — "13
documented stages, of which 10 are dispatched by the orchestrator" — which is
the only phrasing that stays true if either number changes.

---

## E037-29

**Severity:** high · **Type:** guard-not-installed · **Status:** ✅ **CLOSED 2026-08-31** — hook re-installed at Jérémy's instruction;  silent;  green

**Lands on:** `.git/hooks/pre-commit` (installed copy) vs
`strategy-research/tools/hooks/pre-commit` (versioned copy)

**Found by:** S4 follow-up, 2026-08-31, answering "any weird behaviour?"

**The secret scan is not installed.** The tracked hook has three gates; the one
actually running on this machine has two.

| Gate | Versioned copy (89 lines) | Installed copy (60 lines) |
|---|---|---|
| 0. Secret scan | **yes** | **NO** |
| 1. Holdout date gate | yes | yes |
| 2. Test suite | yes | yes |

What is not running:

- **Forbidden paths** — `.env`, `*.env`, `venv/*`, `*.key` are refused by the
  versioned hook. Nothing refuses them here.
- **Credential values in the staged diff** — `BINANCE_API_KEY` /
  `BINANCE_API_SECRET` / `GEMINI_API_KEY` with an assigned value, AWS `AKIA…`,
  Gemini `AIza…`, `-----BEGIN … PRIVATE KEY`, quoted `api_secret=…`.

**Why this is the serious one.** `CLAUDE.fork.md`'s hard rule 2 records that
**upstream committed a real `.env` once**. Gate 0 is the guard added so that
cannot recur — `537558ee`, 2026-08-15, *"fold the tightened secret-scan into
the tracked pre-commit (E-003 S3)"*. It has been in the tracked copy for over
two weeks and was never re-installed here, so on this machine the protection
that incident produced is absent.

**It is exactly the failure the file predicts about itself.** The versioned
hook's own header says: *".git/hooks/ is not tracked by git, so a fresh clone
gets NO hooks and would silently lose both checks below"*, and gives the
install command. It correctly identifies the risk for a **fresh clone** and
misses the one that actually bit: an **update** to the tracked copy does not
reach an existing installation. Nothing compares the two.

**Same shape as [E037-27](#e037-27).** Both are guards that exist, are written down,
and do not run where it counts. E037-27: tests that run in neither gate. E037-29: a
gate that is not installed. In both cases the artifact of the protection —
a file in the repo — was mistaken for the protection.

**Immediate action (a person should do this, not a script):**

```sh
cp strategy-research/tools/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
diff .git/hooks/pre-commit strategy-research/tools/hooks/pre-commit   # must be silent
```

Worth checking on every machine that commits to this repo, not just this one.

**Proposed disposition (S3 decides, not this file):** the copy above closes it
today. To stop it recurring, a test that diffs the installed hook against the
tracked copy would fail the moment they drift — cheap, and it is the check
whose absence made this invisible. Note it can only run where a `.git/hooks/`
exists, so it must skip rather than fail in CI.

---

## E037-30

**Severity:** low · **Type:** orphan-glossary-terms · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §6

**Found by:** S4 follow-up, 2026-08-31, while measuring whether glossary terms
could be hyperlinked at their point of use

§6 defines **46** terms. **13 of them appear nowhere else in the guide** —
measured 2026-08-31 over the body text:

`Innovation Expansion` · `Walk-Forward Test` · `Holdout Period` ·
`Refine (altitude 1)` · `Pivot (altitude 2)` · `Escalate (altitude 3)` ·
`Diagnostic Rule` · `Strategy Config` · `Findings Carryover` ·
`Forecast-Return Correlation` · `Cost Drag %` · `Parameter Bracket` ·
`Research Decision` · `Burnt data` · `Active-bar IC` · `Dormant mechanism` ·
`Holdout consumption` · `DSR (Deflated Sharpe Ratio)`

They fall into three groups, and only the third is a defect:

1. **Used under a different name** — `Walk-Forward Test` is written
   "walk-forward"; `Strategy Config` is `candidate_strategy_config.json`;
   `Active-bar IC` is `ic_active_bars`; `DSR` is spelled out. Harmless, though
   it means a reader searching the term finds only the glossary.
2. **Genuinely unused vocabulary** — `Burnt data`, `Dormant mechanism`. A
   glossary may reasonably define more than the document uses.
3. **Terms for things that are not there.** `Parameter Bracket` and
   `Diagnostic Rule` describe fields the guide elsewhere records as absent from
   `verdict_interpretation.yaml` ([E037-22](#e037-22)), and `Research Decision`
   is one of the five stale stage names corrected in
   [E037-09](#e037-09). The glossary was not updated when those were.

**Why it is worth recording despite being low.** This is the fourth place the
same pattern has surfaced — §2.2's table, §3's field tables, `CLAUDE.md`'s stage
list, and now §6. Each was a second copy of something that changed elsewhere.
The glossary has no generated index and no test behind it, so it is currently
the least-defended surface in the document.

**It also produced a correction.** Chasing `Parameter Bracket` is what revealed
that the field-table audit inspected only top-level keys — which had turned four
misfiled fields into an accusation that they were invented. See the corrections
now inside [E037-22](#e037-22) and [E037-24](#e037-24). A low-severity finding
paid for two high-severity corrections.

**Proposed disposition (S3 decides, not this file):** for group 3, either
update the definitions or mark them as intended-design like their §3
counterparts. For group 1, consider linking the glossary term to the name the
document actually uses. Group 2 needs nothing.

---

## Log

- 2026-08-30 — file created by S1. E037-01-E037-09 came from reading
  `tools/prescreen_signal.py` and `workflow/run_phase1_research.py` against
  `USER_GUIDE.md` §2.2 and §3. E037-10 and E037-11 came from a second pass, filling
  the artifact template's example-value column from a real run
  (`runs/run_060/artifacts/prescreen_result.yaml`, 2026-08-28) — neither was
  visible from the code alone. Reading real output found defects that reading
  the source did not.
