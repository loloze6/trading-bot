# CLEANUP_PLAN.md — strategy-research/ reorganisation (v2)

Supersedes v1, which was withdrawn: it counted a mention in a session report as
equivalent to a code dependency, and was therefore far too preservative.

**Approval required before CLEAN-3 executes anything.** Edit verdicts in this
file; it is the input to the execution waves.

---

## Rule 0 — what "referenced" means here

v1 used `refs_by_path` from REFERENCE_MAP, which counts ANY referring file. A
mention in a session report scored the same as an import in `run_campaign.py`.
That is not a usage signal. v2 uses four separate corpora:

| signal | corpus | meaning |
|---|---|---|
| **PROD** | 54 non-test `.py`/`.sh` + `config/*.yaml` + `workflow/*.yaml` + hooks | the mechanism reads or writes it |
| **TEST** | 61 test modules | exercised by tests |
| **DOC** | 100 `.md` files | mentioned in prose |
| **PATHQUAL** | PROD, but matching the *path* not the bare basename | distinguishes the file from a same-named per-run artifact |

**Three interpretation rules, each of which changed a verdict:**

1. **Basename PROD is contaminated by artifact-type names.** `regime_detector_report.yaml`
   scores PROD=4 by basename, but that name is also a per-run artifact type written
   into `runs/{run_id}/artifacts/`. Always path-qualify before deleting.
2. **A CLI tool has PROD=0 by nature.** `tools/*.py` invoked from a runbook or
   dispatch is never imported, so DOC references *are* its usage record. PROD=0
   is not evidence against a tool.
3. **Zero references never means unused for `test_*.py`.** pytest discovers by
   filename. 14 of 28 zero-reference files are tests. All tests are KEEP.

---

## Rule 1 — where clarity actually comes from

The objective is a folder that explains itself. Two ways to get there, with very
different risk:

- **Archiving history and writing documentation** — high payoff, near-zero
  regression risk.
- **Moving live mechanism files into prettier folders** — low payoff, direct
  regression risk, because every move with a PATHQUAL reference means editing
  production code.

So: **aggressive on archive/delete and on documentation; conservative on moving
anything with PATHQUAL >= 1.** `campaign_state.yaml` alone has PROD=7 — folding
it into a `campaign/` subfolder means editing seven production files to gain a
directory level. Not worth it. The clarity for those files comes from §E
documentation, not relocation.

---

## A. DELETE — no mechanism, no audit value

### EXECUTED at commit `71573062` — 5 files deleted, done, do not re-litigate

| path | PROD/TEST/DOC | reason |
|---|---|---|
| `campaign.pid` | 0/0/2 | 4-byte runtime PID file, committed by accident. Now in `.gitignore`. `RUNBOOK.md`'s five hits are shell examples (`echo $! > campaign.pid`) that CREATE it at runtime — not references to a tracked file. |
| `workflow/stage_runner.md` | 0/0/0 | orphaned prompt spec; **there is no `stage_runner.py`** — nothing executes it. Settles the operator's question about whether every stage agent should read CLAUDE.md: moot, the file was dead. |
| `NEXT_SESSION_20260712.md` | 0/0/1 | byte-identical duplicate of `docs/plan/NEXT_SESSION_20260712_superseded.md` (blob `332368e2`, 5771 B both). The archived copy already existed. |
| `incident_20260710/instance_F_payload.txt` | 0/0/0 | 166 bytes, superseded by `INCIDENT.md` |
| `protocols/escalation_dotusdt_4h.json` | 0/0/0 | unexecuted spec; the SOL/AVAX/15m siblings are referenced, this one never was |

### OVER-DELETED and RESTORED at `595b5096`

`protocols/diagnostic_btceth_4h.json` was deleted at `71573062` and should not
have been. Restored byte-identical (blob `8de569f1`) and reclassified to §B
ARCHIVE. Cause, recorded so it does not recur: the director downgraded it to
ARCHIVE in conversation and never edited this file, so the plan and the dispatch
disagreed and the executing agent followed the plan — correctly, per the
"file wins" rule. **A verdict that lives only in chat is not a verdict.**

Its three run_036 provenance records (`protocol_result.yaml:3`,
`run_context.yaml:2`, `protocol_summary.json:4`) are what make run_036
reproducible — the same argument that archives `regime_retune_results.yaml`
rather than deleting it.

### HELD — awaiting an explicit operator decision

`tools/retune_regime_detector.py` (0/0/0) is a genuine orphan and CLEAN-3a-pre
confirmed deleting it orphans no reader. But it is the **sole producer** of
`config/regime_retune_winner.json`, which `regime_detector_report.yaml:6` names
as its `config_source`. Delete it and that config becomes unreproducible: the
next report regeneration falls back to `validate_regime_detector.py:61`'s
run_033 default and silently describes a **different detector**, while
`AMENDMENTS_01-06.md:120` makes `detector_version` load-bearing for every
regime-conditional KB finding. Director recommendation: **keep** — 21 KB buys
the reproduction path for a config the live report depends on.

### WITHDRAWN from the delete list after re-measurement

Both were flagged by the operator, and both flags were correct:

- `workflow/LATER.md` — the probe searched `LATER.md` with the extension. It is a
  deferred-scope record from STEP6_ITER1_v2 listing five still-open items,
  including "collapsing STAGE_CONFIGS into stages.yaml" and "stages 6-10
  skeletons exist but empty" — the latter corroborated by CLEAN-0 deleting an
  empty `skills/research-decision/SKILL.md`. Backlog, not litter.
  → MOVE to `improvements/`, see §D.
- `workflow/handoff.schema.yaml` — the string `handoff.schema` appears in **zero**
  files, so nothing loads it, but it is a real 11-field schema
  (`handoff_version`, `run_id`, `from_stage`, `to_stage`, ...) describing the
  contract that `templates/handoffs/*.yaml` implement and
  `run_phase1_research.py:64-103` consumes by filename. A schema with no
  validator — the mirror image of the missing-schema finding in §E.
  → MOVE to `schemas/handoff.schema.yaml`, see §D.

### RESOLVED — CLEAN-3a-pre, 2026-07-30. Two KEEP, one ARCHIVE, none deleted.

The "writer/reader pair" hypothesis was **false**, and it traced to a single
`print()` string at `retune_regime_detector.py:500`. Verified producer graph:

```
retune_regime_detector.py ──writes──► config/regime_retune_winner.json   (:72)
                          ──writes──► regime_retune_results.yaml         (:73)
                          ──subprocess──► validate_regime_detector.py    (:489)
validate_regime_detector.py ──writes──► regime_detector_report.yaml      (:66)
run_phase1_research.py ──subprocess──► validate_regime_detector.py       (:1465)
```

Production reaches the producer independently of the retune tool, so **deleting
`retune_regime_detector.py` orphans no reader.** It remains safe to delete.

| path | verdict | evidence |
|---|---|---|
| `regime_detector_report.yaml` | **KEEP — do not delete** | Load-bearing. 5 production read sites in `run_phase1_research.py` (`:1443`, `:1476`, `:4814`, `:4919`, `:1515-1525`); declared in `stages.yaml` as an OUTPUT (`:132`) *and* an INPUT (`:142`); two LLM contracts, of which `skills/regime-auditor/SKILL.md:55` makes absence a **hard blocker**; 9 live run handoffs point at it via `../../regime_detector_report.yaml`. The operator proposed deleting this — measurement refutes it. |
| `power_check_discrepancy_log.yaml` | **KEEP** | Live append-only observability log. **This plan misattributed its producer**: `tools/power_check.py` contains ZERO references. The real writer is `run_phase1_research.py:3370` (read-modify-write at `:3360`). `improvements/IMPROVEMENTS_DONE_20260706.md:160` records that it fired during a real P1a run, not just a fixture. Tests monkeypatch it to `tmp_path`, so deletion cannot break the suite — it would only discard real observed data. |
| `regime_retune_results.yaml` | **ARCHIVE** → `archive/reports/` | Zero readers of any kind. But `runs/run_039/artifacts/regime_audit_decision.yaml:10` cites it as the evidence for the conclusion that no ER-based config reaches high confidence on BTC/ETH 1h — a live campaign constraint. Deleting it turns a checkable claim into an assertion, for 11,874 bytes. |

**A self-inflicted trap worth recording:** two separate misattributions in this
plan came from reading a `print()` string as a write. Console text naming a file
is not evidence that the emitting code produces it.

---

## B. ARCHIVE — this is where the volume is

**`results/` — archive all but one subdirectory.** Measured:

| subdir | size | PROD | verdict |
|---|---|---|---|
| `results/protocols/` | 72 KB | 2 | **KEEP** — live output target, `run_protocol.py:989` defaults `--out` here |
| `results/runs/` | **15.6 MB** | 1 | **ARCHIVE** — the only PROD hit is a note in `campaign_data_policy.yaml:335` stating the data is *"now absent from results/runs/"*. July-2nd bulk output. |
| `results/prescreens/` | 6 KB | 0 | **ARCHIVE** — only a few runs' worth; `prescreen_signal.py` does not write here |
| `results/w11/` | 10 KB | 0 | **ARCHIVE** — improvement-wave scratch output |
| `results/shakedown_ts_trend_daily/` | 3 KB | 0 | **ARCHIVE** — contains a prescreen + a strategy config; a one-off shakedown, not a result set |

→ `archive/results/`. This is the single largest reduction in the plan.

**Other archive moves:**

| path | destination |
|---|---|
| `incident_20260710/*.snapshot` (6 files) | `archive/incidents/2026-07-10/` |
| `manual_draft/run_043_hypothesis_card_DRAFT_NOT_USED.yaml` | `archive/drafts/` — **not** into `briefs/`; see §C |
| `briefs/research_brief_P4_ts_trend_draft_superseded.md` | `archive/briefs/` |
| `NEXT_SESSION_20260712.md` | `archive/improvements/HANDOFF_20260712.md` — PROD=0, DOC=1 |
| `campaign_state_MIGRATION_NOTICE.md` | `archive/reports/` — PROD=0, TEST=0, DOC=1 |
| `protocols/diagnostic_btceth_4h.json` | `archive/protocols/` — PROD=0, DOC=1 but carries 4 referrers: `USER_GUIDE.md:752` (prose), `run_036/artifacts/protocol_result.yaml:3`, `run_036/artifacts/run_context.yaml:2`, `run_036/protocol_summary.json:4`. Last three are run_036 provenance records (blob `8de569f1`); archiving preserves reproducibility. **CORRECTED from DELETE (CLEAN-3a dispatch error).** |

`incident_20260710/INCIDENT.md` is **NOT** archived: 17 path references. It moves
to `docs/incidents/INCIDENT_20260710.md` (§D) and the folder is retired.

---

## C. KEEP — with the corrected basis

- **`config/` — genuinely mechanism-coupled.** All 11 files have PROD >= 1
  (`campaign_data_policy.yaml` 17, `cost_model.yaml` 6, `campaign_queue.yaml` 5,
  down to 1). No legacy. v1 said the same thing on the wrong evidence; it happens
  to survive on the right evidence.
- **`tools/` — one orphan of 20.** Only `retune_regime_detector.py` is dead in
  all three corpora. Six others show PROD=0 (`check_data.py`,
  `fragment_patterns.py`, `lint_verdict_provenance.py`, `measure_funding_carry.py`,
  `whale_footprint_evaluation.py`, `build_inventory.sh`) but they are **CLI entry
  points** — PROD=0 is their normal state. `whale_footprint_evaluation.py` in
  particular is the Phase 2.3 evaluation path. All KEEP.
- **`briefs/` — live input.** Referenced by `workflow/run_campaign.py` and
  `config/campaign_queue.yaml`. The `.yaml`/`.md` split is meaningful: one
  structured brief artifact, five prose briefs. Do not normalise extensions;
  document the distinction instead.
- **`quarantine/` — not in git.** `quarantine_dir:
  strategy-research/quarantine/holdout_contaminated/` is gitignored, 0 tracked
  files. Holds two runs produced 2026-07-02 whose declared range crossed the
  sealed window; quarantined 2026-07-26; `chronology_verdict: runs_predate_seal`
  (`campaign_data_policy.yaml:283-289`). Audit evidence for a contamination
  event. Never delete. Nothing for CLEAN-3 to do.
- **`recorder/` — deferred, not dismissed.** Double maintenance against
  `deploy/kraken_recorder/` is real, but resolving it is a design decision
  (which is source of truth?) and the directory is load-bearing for an imminent
  cutover. Post-cutover dispatch.
- **`protocols/prereg_whale_footprint_v2.yaml`** — single-use, UNCONSUMED. Do not
  move, rename or touch.
- **All `test_*.py`** — regardless of reference count.

---

## D. MOVE — doc-only files, so the moves are cheap

Only files with **PATHQUAL = 0** are moved. Anything the mechanism reads by path
stays where it is.

| path | destination | PROD |
|---|---|---|
| `USER_GUIDE.md` | `docs/USER_GUIDE.md` | 0 |
| `DOC_INDEX.md` | stays at root | 0 — but it is the entry point; moving it defeats its purpose |
| ~~`workflow/stages.yaml`~~ | **REVISED: STAYS in `workflow/`** | PROD=0 confirms no code reads it — it documents the stage graph rather than driving it. But moving it means updating 9 prose references for zero mechanical gain, which violates Rule 1 (conservative on moves, aggressive on documentation). The finding is recorded in `workflow/`'s documentation instead. Renaming it would also break every prose reference that says "stages.yaml". |
| `incident_20260710/INCIDENT.md` | `docs/incidents/INCIDENT_20260710.md` | 17 refs but all prose — highest-risk move in the plan; own commit |
| `workflow/handoff.schema.yaml` | `schemas/handoff.schema.yaml` | 0 — joins its 20 siblings; nothing loads it today |
| `workflow/LATER.md` | `improvements/BACKLOG_DEFERRED.md` | 0 — deferred-scope record, belongs to the improvements family |
| `00_closing_state.md` | `improvements/IMPROVEMENTS_DONE_<YYYYMMDD>.md` | 2 — **name collides** with `docs/plan/00_closing_state.md` (different file, 8147 B vs 32128 B). Both must get distinct names. |
| `PIPELINE_IMPROVEMENTS_20260712_v4.md` | `improvements/IMPROVEMENTS_DONE_20260712.md` | 4 |
| `NEXT_SESSION.md` | `improvements/HANDOFF_CURRENT.md` | 3 |

**`RUNBOOK.md` stays at root.** PROD=5 — the mechanism references it by path.
You suggested moving it to `docs/`; measurement says that costs five production
edits. Recommend leaving it and linking from `docs/`.

**`coin_universe.yaml` / `feed_wishlist.yaml` stay at root.** PATHQUAL=1 each.
They are cross-campaign inputs and moving them means editing the referrer.
Document them in §E instead.

**`campaign_*` all stay at root** — PROD 1 to 11. Live campaign state.

---

## E. DOCUMENT — the wave that actually delivers the objective

This is the operator's core ask and v1 under-delivered by deferring it. Four
deliverables, sample-then-extend as requested:

1. **`strategy-research/README.md` (new)** — the map: what each top-level folder
   is, what runs what, which files are entry points, which are state, which are
   history. This is the file that answers "I don't understand this folder anymore."
2. **`config/README.md`** — per file: purpose, who reads it (with the measured
   PROD referrers), and a brief description of its parameters. Produce ONE file's
   entry first for approval, then extend to all 11.
3. **`tools/README.md`** — per tool: what it does, how it is invoked (these are
   CLI entry points, so the invocation line matters), and its inputs/outputs.
   Flag the six PROD=0 tools explicitly as CLI-only so nobody mistakes them for
   dead code later.
4. **`protocols/README.md`** — how a protocol is used in the research workflow,
   the meaning of each field, and **why the folder mixes `.json` and `.yaml`**:
   `.json` are protocol specs consumed by `tools/run_protocol.py`; `.yaml` are
   human-authored preregistrations. Two artifact types, co-located. Recommend
   splitting into `protocols/specs/` and `protocols/preregs/` — but only after
   checking PATHQUAL on each, since `run_protocol.py` may resolve them by path.

5. **`improvements/IMPROVEMENTS_REGISTER.md` (new)** — the review of the
   improvements category, which v2 was missing entirely: it renamed the files
   without ever asking what state the improvements are in. There is ~500 KB of
   improvement prose with no index, and the numbering is already mechanised, so
   the register can be built from evidence rather than opinion:

   | source | what it proves |
   |---|---|
   | `docs/plan/00`–`11_*.md` (12 numbered plans) | an improvement was SPECIFIED |
   | "Improvement NN" strings in the PROD corpus | it was IMPLEMENTED — measured: 01×1, 02×7, 04×1, 05×2, 06×6, 07×5, 08×7, 09×3 |
   | `tests/test_improvementNN_acceptance.py` | it was ACCEPTANCE-TESTED — only **04** and **06** exist, plus `runs/run_042/artifacts/improvement_05_acceptance.yaml` |

   So on current evidence: **03, 10, 11 are specified but have zero PROD
   references** — plans that were never implemented. And only 2 of 12 have
   acceptance tests. One row per improvement: number, title, spec path, status
   (specified / implemented / accepted / abandoned), completion date, evidence.

   `docs/plan/` already holds this family and is the natural home: 12 numbered
   plans, `AMENDMENTS_01-06.md`, `NEXT_RUN_CHECKLIST.md`, and **six**
   `NEXT_SESSION_*_superseded.md` files. The register indexes it; the six
   superseded handoffs move to `archive/improvements/`.

   Note: `docs/plan/01`–`06` and `08` show zero references in all corpora, which
   under Rule 0 does NOT license deleting them — they are specification history
   for implemented improvements. The register is what makes them findable.

**Dangling-reference scan is part of this wave, not a query.** REFERENCE_MAP is
keyed on files existing at HEAD, so pointers to deleted files are structurally
invisible: `USER_GUIDE.md:223` cites `schemas/research_brief.schema.json`
(deleted at `76d87a53`) and the map attributes it to
`templates/research_brief.yaml` instead. The same class of defect left 15 broken
references in the deployment bundle. CLEAN-4 must scan for pointers to
nonexistent paths, including prose forms with no file extension.

**Missing schemas to rule on:** `research_brief` and `run_manifest` have
templates but no schema (empty stubs deleted at `76d87a53`), while
`strategy-research/CLAUDE.md` says outputs are validated against schemas before
each stage advances. Write them, or retire the claim. `results_summary` had both
stubs empty and looks vestigial.

---

## F. UNMEASURED — the elephant

**`runs/` is 7,584 files, 92% of the folder, and I have not measured it.** 59 run
directories. It is the campaign record and `campaign_knowledge_base.yaml`
(PROD=11) indexes into it, so it is certainly not disposable — but whether all 59
need to be live rather than archived is the single largest open question in this
reorganisation, and it dwarfs everything in §A and §B combined.

**MEASURED (CLEAN-2b, 2026-07-30) — and the answer is: do not archive runs/ on
grep evidence.** Three anchorings gave three different answers, which is itself
the finding:

| anchoring | unindexed run dirs | % of runs/ files |
|---|---|---|
| stem (`\brun_030\b`) across the 3 campaign index files | 17 of 59 | 8.25% |
| literal path (`runs/run_030/`) in PROD corpus | 49 of 59 | 71.3% |
| **actual code behaviour** | **not derivable by grep** | — |

The third row is what governs. `run_campaign.py` iterates the WHOLE runs/
directory at `:251`, `:1034` and `:1110` (the last returns
`{p.name for p in runs_dir.iterdir() if p.is_dir()}`), as does
`run_phase1_research.py:2487`. Moving any run directory changes what those four
scans return. Separately, two tools hardcode historical runs through path-join,
which literal-path greps cannot see:
`panel_backtester.py:262` → `runs/run_054/protocol_summary.json`, and
`validate_regime_detector.py:61` → `runs/run_033/artifacts/candidate_strategy_config.json`.
`run_033` appeared in the "zero path references" set — it is not.

**Prerequisite before any runs/ decision:** read the four iteration sites and
determine what each computes (next-run-id allocation? state reconciliation?
orphan detection?). Whether archiving is safe depends entirely on that, not on
reference counts. Until then runs/ stays intact.

**Separate finding worth acting on regardless:** the three campaign index files
DISAGREE about 16 of 59 runs (27%). 14 are in `campaign_state.yaml` but not
`campaign_knowledge_base.yaml`; `run_045` and `run_046` are in the knowledge base
but neither state nor queue. That is an indexing inconsistency in live campaign
state, independent of cleanup.

---

## G. REGRESSION GUARD

`config/holdout_gate_exemptions.txt` is **path-keyed** with pinned line counts.
Every move and rename above invalidates its entry. Known affected:

```
strategy-research/NEXT_SESSION.md                        1
strategy-research/PIPELINE_IMPROVEMENTS_20260712_v4.md  13
strategy-research/briefs/research_brief_P4_ts_trend_draft_superseded.md  3
```

Rules: every move/rename updates its registry entry **in the same commit**; run
`sh strategy-research/tools/holdout_date_gate.sh` after each wave; a BLOCK is a
STOP and is never silenced by adding an entry; re-measure any changed count.
`DOC_INDEX.md` must be updated for every move and rename.

`docs/INVENTORY.tsv` and `docs/REFERENCE_MAP.tsv` will be stale after every wave.
That is expected. CLEAN-5 regenerates them once at the end.

---

## G2. DANGLING REFERENCES — measured, CLEAN-4d 2026-07-30

14 genuine findings across 19 file:line sites, over 254 live-surface files
(`runs/` and `results/` excluded). Path-join and bare-import forms were checked
exhaustively and returned **zero** each — measured zeros, not skipped forms. 62
dangling paths inside `tests/` are synthetic fixture names exercising error
paths; not findings.

**MISLEADS — a reader is sent to a file that does not exist:**

1. `schemas/backtest_spec.schema.json:10` asserts validation against
   `trading-bot/strategy_config.schema.json`, which **has never existed at any
   commit**. Highest severity: a machine-readable schema's `description` claiming
   a validation gate that does not exist.
2. `protocols/ts_trend_daily_v2.json` cited as a worked example in
   `tools/stamp_protocol.py:19,20,60` (CLI docstring — copy-pasting it fails),
   `tools/README.md:449`, `docs/design/K3_protocol_pinning_design_20260714.md:489,496`.
   Only `v1` exists.
3. `docs/00_closing_state.md` cited by 7 referrers (`RUNBOOK.md:197`, two briefs,
   `campaign_knowledge_base.yaml:417`, a snapshot, `run_campaign.py:756`). The
   canonical file is at the strategy-research root; the only `docs/`-relative
   match is `docs/plan/00_closing_state.md`, an explicitly ARCHIVED superseded
   snapshot. Readers land on stale content. **This is the name collision flagged
   in §D.**
4. `skills/research-decision/SKILL.md` (deleted `76d87a53`) still described as
   present in `DOC_INDEX.md:105` and `workflow/LATER.md:5`.
5. `schemas/campaign_knowledge_base.schema.json` — `docs/plan/05_campaign_knowledge_base.md:73`
   calls it "new"; it never existed.
6. `validation/stages.yaml` — `docs/STEP_05_FINDINGS.md:201`; real path is
   `workflow/stages.yaml`.
7. `tools/record_kraken_ws.py` — `docs/session_reports/20260726_recorder_build_spec.md:226`;
   real path is `recorder/record_kraken_ws.py`.
8. `trading-bot/PIPELINE_IMPROVEMENTS_20260712_v4.md` — `RUNBOOK.md:255`; the file
   is at the strategy-research root.
9. `docs/design/K3_protocol_pinning_design_20260713.md` — `SESSION_LOG.md:1294`;
   only the `20260714` version exists.
10. `skills/validation/SKILL.md` — `docs/STEP_05_FINDINGS.md:168`; closest real
    file is `skills/quant-validation/SKILL.md`.
11. `run_017/findings_carryover.yaml`, `run_018/...` — `docs/STEP_05_FINDINGS.md:61,68`
    drop the `runs/.../artifacts/` path segment.
12. `protocols/diagnostic_btceth_4h.json` — `USER_GUIDE.md:752` (transient, CLEAN-3a dispatch error). **RESOLVED**: file restored and reclassified as ARCHIVE, not DELETE.

**STALE — historical record naming something since removed; no fix needed:**
`protocols/escalation_dotusdt_15m.json` (`SESSION_LOG.md:1253`),
`NEXT_RUN_CHECKLIST.md` (`docs/session_reports/20260719_close.md:202`),
`trading-bot/docs/ROADMAP_TO_PROFITABLE_STRATEGY.md` (same doc, `:222,257`).

**Declared gap:** prose references with no file extension ("the handoff schema",
"the Windows RUNBOOK section") were covered only by seed-guided checks, not a
blind sweep — finding those requires reading 254 files for meaning. Literal,
path-join and import forms ARE exhaustive. Findings 3 and 8 came from the prose
class, so the residual is non-empty.

---

## H. Execution order

| wave | scope | risk |
|---|---|---|
| 3a | §A deletes (8 unambiguous) + `.gitignore`; REPORT the 3 rulings, act on none | low |
| 3b | §B archive moves — `results/` first, it is the volume | medium |
| 3c | §D moves and renames + §G registry and DOC_INDEX updates | HIGH — `INCIDENT.md` gets its own commit |
| 4 | §E documentation + dangling-reference scan | judgment |
| 5 | regenerate both TSVs, full gate, test suite, verify | low |
| — | §F `runs/` measurement pass | separate, before any runs/ decision |

Outside this cleanup, flagged not acted on: **`venv/` is tracked in git**
(`venv/Scripts/Activate.ps1` and siblings). A committed virtualenv is a repo
hygiene defect at the repo root, not in `strategy-research/`.
