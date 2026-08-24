# Documentation Index

Rules for this file: one line per doc, pointers only — no doctrine, procedure,
or status duplicated here (that lives in the doc itself; this file only says
where to find it). Update this file whenever a doc is added or retired (see
`docs/TIMEFRAME_CHANGE_PLAYBOOK.md`'s checklist). Machine-generated files are
marked as such, with their writer named — read them for current values, but
don't hand-edit them.

Organized by the question a reader actually arrives with, not by directory.

---

### "What do I do this session?"
→ For **engineering work**: **[`engineering/roadmap/EPICS.md`](engineering/roadmap/EPICS.md)** —
one line per epic, the only mandatory read for engineering.
→ For **campaign/research work**: **[`docs/CAMPAIGN_PROGRAM.md`](docs/CAMPAIGN_PROGRAM.md)** (phase
plan) and `config/campaign_queue.yaml` (current queue state).
→ **[`HANDOFF_CURRENT.md`](engineering/sessions/HANDOFF_20260724.md)** —
archived, superseded by EPICS.md and docs/CAMPAIGN_PROGRAM.md above. Retained for its 20 DONE rows'
verified commit SHAs.

### "What's the overall plan / KPI / process?"
→ **[`docs/CAMPAIGN_PROGRAM.md`](docs/CAMPAIGN_PROGRAM.md)** — operator-ratified campaign program
(v2, 2026-07-19): Phase 0-5 task sequence with gates, the KPI (honest
verdicts/week, cost per verdict) and anti-corner rule, the role/model
assignment for every agent class, and the context-economy rules. The
standing plan — `engineering/sessions/HANDOFF_20260724.md` (archived) once
derived its own task queue from this; engineering work now tracks separately in
`engineering/roadmap/EPICS.md`.

### "How do I operate the campaign?"
→ **[`RUNBOOK.md`](RUNBOOK.md)** — launch/status/resume/stop commands, the
hard-pause table (section 3), the block on background/`nohup` mode (grounds: ledger P0 kernel — see
engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md).

### "What is this system / what does artifact X mean?"
→ **[`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)** — pipeline stage map, every artifact's
field-by-field schema, skill goals, tools overview, glossary.

### "How do I change things safely?"
→ **[`docs/TIMEFRAME_CHANGE_PLAYBOOK.md`](docs/TIMEFRAME_CHANGE_PLAYBOOK.md)**
— the two assumption-sweep categories, metric-basis rules (bar/episode/fragment),
the three-role model for fragment data, the concealment-instruction doctrine,
read-back verification doctrine.

### "Where do things stand right now?"
→ **[`engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md`](engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md)**
(formerly `00_closing_state.md`) — canonical current status of the
enhancement-plan build (M0–M3, P1a/P1b). Note: `engineering/improvements/done/design_and_docs/00_closing_state.md`
is an ARCHIVED snapshot with the same title — not the current version.
→ **[`engineering/improvements/done/IMPROVEMENTS_REGISTER.md`](engineering/improvements/done/IMPROVEMENTS_REGISTER.md)**
— per-improvement status index (01–11): specified vs. implemented vs. accepted,
built from PROD-corpus references and acceptance artifacts.
→ **[`campaign_summary.md`](campaign_summary.md)** — machine-generated
scoreboard (written by `workflow/run_campaign.py`, regenerated on `done`/halt
transitions only — check its own staleness banner if present before trusting
it against `campaign_queue.yaml`).
→ **[`campaign_log.md`](campaign_log.md)** — machine-generated, curated
one-line-per-transition log (written by `workflow/run_campaign.py`).

### "What happened in the security incident?"
→ **[`docs/analysis-reports/INCIDENT_20260710.md`](docs/analysis-reports/INCIDENT_20260710.md)** — the
KB-revert incident and the system-reminder investigation, RESOLVED
2026-07-11 as native harness boilerplate (see its Resolution addendum);
standing disclosure doctrine with the verified-template allowlist.

### "Where may I legally trade, and on what venue?"
→ **[`docs/analysis-reports/venue_survey_20260719.md`](docs/analysis-reports/venue_survey_20260719.md)** —
Phase 1.1 venue survey: MiCA/MiFID II authorization status, spot vs. perp
retail availability, fees, and API quality for Binance/Kraken/Bybit/OKX/
Coinbase/Bitget; Kraken decided as primary venue, OKX as shortlist backup.
Includes a 2026-07-20 supplement (spot-margin fees, perp funding mechanics,
the cost-mapping note) and a resolved open item (the apparent spot-fee
figure conflict was a mismatched-product comparison, not a real conflict).

### "What's broken and what gates autonomy?"
→ **[`IMPROVEMENTS_DONE_20260712.md`](engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md)**
— the growing defect ledger (v7 as of 2026-07-20); its P0 "kernel" gates
background mode. A1/A3/B1 (K4), A8/A9/B11/C7/C9 (K2), B3/B10 (K3), and
B7/B15 (v5/v6) are CLOSED — see the design notes below for what shipped.
Open P0: **A12** (verdict_interpreter's missing human_pause guard — fix
first if resume reliability matters). Open P1/P2 watch items: B13, B14,
A13, A14, C11 (4h block_size trap — fix before any 4h registration), F11,
D4 (shared trades.json path), **C12** (inert protocol-declared timeframe —
archived pre-threading runs silently ran at 1h), **C13** (V9
validation-drift blocking run_018 re-execution, does not invalidate its
original verdict).
→ **[`engineering/improvements/done/design_and_docs/K4_routing_registration_design_20260712.md`](engineering/improvements/done/design_and_docs/K4_routing_registration_design_20260712.md)**,
**[`engineering/improvements/done/design_and_docs/K2_verdict_machinery_design_20260713.md`](engineering/improvements/done/design_and_docs/K2_verdict_machinery_design_20260713.md)**,
**[`engineering/improvements/done/design_and_docs/K3_protocol_pinning_design_20260714.md`](engineering/improvements/done/design_and_docs/K3_protocol_pinning_design_20260714.md)**
— design notes for the closed items above, each with an appended Phase B
rulings/deviations section (K2's and K3's also have a dated rider section;
K3's rider section additionally carries the 2026-07-15 audit-outcome
paragraph).

### "Why did my run stop / not stop, and what does the campaign know about its own halts?"
→ **[`docs/HALT_RECOVERY.md`](docs/HALT_RECOVERY.md)** — the durable halt
record, the quarantine/escalate policy (which 4 reasons auto-continue and
why, off by default), and the loop-health instrument
(`campaign_record/loop_health.yaml`), each with the config flag and what to
expect. Built in E-030 — see `engineering/roadmap/E-030/EPIC.md` for the
evidence.

### "What can run autonomously vs needs a human?"
→ **[`docs/WORKFLOW_CAPABILITIES.md`](docs/WORKFLOW_CAPABILITIES.md)** —
per-stage autonomy boundary within one run.
→ **[`RUNBOOK.md`](RUNBOOK.md) section 3** — which halt conditions are
mechanically resolved vs. remain human-gated across a whole campaign.

### "What are the pipeline stages / process steps?"

→ **[`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) §2 Workflow Overview** — the
CANONICAL description of the stages: the stage map, each stage's objective,
what it receives, what it decides. Single maintained home; start here.

**Not** `workflow/stages.yaml` — it is not read by any code and is not
authoritative (verified 2026-08-24; status resolved by E-033 S2). Code ground
truth is `STAGE_CONFIGS` + `workflow_artifacts/templates/handoffs/` + the
`determine_post_*` routing functions.

### "How does stage X decide?"
Each is an LLM persona in `skills/{name}/SKILL.md`:
- **`hypothesis-design`** — turns a research brief into one concrete, falsifiable hypothesis.
- **`innovation-expansion`** — multiplies a hypothesis into 3–6 testable variants.
- **`quant-validation`** — pre-backtest falsifiability/bias/failure-mode pressure test.
- **`refinement-planner`** — converts validation blockers into concrete fixes.
- **`backtest-engineering`** — translates a validated hypothesis into `strategy_config` JSON.
- **`regime-auditor`** — decides whether a regime detector is trustworthy / needs retune / unusable.
- **`verdict-interpreter`** — reads backtest diagnostics, issues refine/pivot/escalate/promote/kill.
- **`campaign-review`** — steps back after 2+ failed families to continue/reframe/escalate/terminate; also the fragment-pattern-motivated ideation hook.
- **`quant-fundamentals`** — verified math identities/code behaviors other skills must defer to before applying diagnostic rules.

### "What's historical/archived?"
→ **`docs/plan/`** — superseded enhancement-plan design docs (`00_overview_v2.md`,
`01`–`11_*.md`, `AMENDMENTS_01-06.md`), plus the archived `00_closing_state.md`
namesake above. Read only for historical rationale, never as current guidance.
→ Archived `NEXT_SESSION.md` snapshots (moved to `archive/improvements/`), each
superseded by the next as the campaign progressed (historical only, read for
the session's own framing, never as current guidance):
[`archive/improvements/NEXT_SESSION_20260710_superseded.md`](archive/improvements/NEXT_SESSION_20260710_superseded.md)
(pre-run_057),
[`archive/improvements/NEXT_SESSION_20260712_superseded.md`](archive/improvements/NEXT_SESSION_20260712_superseded.md)
(post-run_057 close),
[`archive/improvements/NEXT_SESSION_20260714_superseded.md`](archive/improvements/NEXT_SESSION_20260714_superseded.md)
(post-K4+K2 implementation),
[`archive/improvements/NEXT_SESSION_20260715_superseded.md`](archive/improvements/NEXT_SESSION_20260715_superseded.md)
(post-K3 implementation/close-out),
[`archive/improvements/NEXT_SESSION_20260717_superseded.md`](archive/improvements/NEXT_SESSION_20260717_superseded.md)
(post-H-041-family close, pre-generator-session),
[`archive/improvements/NEXT_SESSION_20260719_superseded.md`](archive/improvements/NEXT_SESSION_20260719_superseded.md)
(post-run_059 close, pre-Phase-1 venue/cost arc).
→ **[`SESSION_LOG.md`](SESSION_LOG.md)** — chronological per-session handoff log
(hypothesis / result / files touched / next-session prompt). Historical once superseded by a newer entry.
→ **`engineering/improvements/done/design_and_docs/STEP_05_FINDINGS.md`, `engineering/improvements/done/design_and_docs/p1b_fetch_manifest.md`** — dated,
self-contained investigation notes. Historical, not living docs.
→ **[`engineering/improvements/done/design_and_docs/NEXT_RUN_CHECKLIST.md`](engineering/improvements/done/design_and_docs/NEXT_RUN_CHECKLIST.md)**
— moved here 2026-07-19 (superseded): a pre-K2/K3-era operational
checklist (2026-07-04) whose `pre_registration.yaml` template (section
4) predates the real B11/C7 structured `pass_rule` schema now in use —
following it literally today would produce a non-conformant
registration. Read only for historical context on the A6.2/KB-recompute
mechanisms it also describes (those are still substantively accurate).

---

Cross-linked from the top of `RUNBOOK.md`, `docs/USER_GUIDE.md`, and `CLAUDE.md`.
