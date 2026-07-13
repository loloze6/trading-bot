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
→ **[`NEXT_SESSION.md`](NEXT_SESSION.md)** — the single entry point for the
next session: read-first list, priority-ordered task queue, standing
constraints. Start here if you're picking this campaign back up.

### "How do I operate the campaign?"
→ **[`RUNBOOK.md`](RUNBOOK.md)** — launch/status/resume/stop commands, the
hard-pause table (section 3), the block on background/`nohup` mode (grounds: ledger P0 kernel — see
PIPELINE_IMPROVEMENTS_20260712_v4.md).

### "What is this system / what does artifact X mean?"
→ **[`USER_GUIDE.md`](USER_GUIDE.md)** — pipeline stage map, every artifact's
field-by-field schema, skill goals, tools overview, glossary.

### "How do I change things safely?"
→ **[`docs/TIMEFRAME_CHANGE_PLAYBOOK.md`](../docs/TIMEFRAME_CHANGE_PLAYBOOK.md)**
— the two assumption-sweep categories, metric-basis rules (bar/episode/fragment),
the three-role model for fragment data, the concealment-instruction doctrine,
read-back verification doctrine.

### "Where do things stand right now?"
→ **[`00_closing_state.md`](00_closing_state.md)** — canonical current status
of the enhancement-plan build (M0–M3, P1a/P1b). Note: `docs/plan/00_closing_state.md`
is an ARCHIVED snapshot with the same title — not the current version.
→ **[`campaign_summary.md`](campaign_summary.md)** — machine-generated
scoreboard (written by `workflow/run_campaign.py`, regenerated on `done`/halt
transitions only — check its own staleness banner if present before trusting
it against `campaign_queue.yaml`).
→ **[`campaign_log.md`](campaign_log.md)** — machine-generated, curated
one-line-per-transition log (written by `workflow/run_campaign.py`).

### "What happened in the security incident?"
→ **[`incident_20260710/INCIDENT.md`](incident_20260710/INCIDENT.md)** — the
KB-revert incident and the system-reminder investigation, RESOLVED
2026-07-11 as native harness boilerplate (see its Resolution addendum);
standing disclosure doctrine with the verified-template allowlist.

### "What's broken and what gates autonomy?"
→ **[`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)**
— the 29-item defect ledger; its P0 "kernel" gates background mode.

### "What can run autonomously vs needs a human?"
→ **[`docs/WORKFLOW_CAPABILITIES.md`](docs/WORKFLOW_CAPABILITIES.md)** —
per-stage autonomy boundary within one run.
→ **[`RUNBOOK.md`](RUNBOOK.md) section 3** — which halt conditions are
mechanically resolved vs. remain human-gated across a whole campaign.

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
- **`research-decision`** — currently an empty file (0 lines); no persona defined yet.

### "What's historical/archived?"
→ **`docs/plan/`** — superseded enhancement-plan design docs (`00_overview_v2.md`,
`01`–`11_*.md`, `AMENDMENTS_01-06.md`), plus the archived `00_closing_state.md`
namesake above. Read only for historical rationale, never as current guidance.
→ **[`docs/plan/NEXT_SESSION_20260710_superseded.md`](docs/plan/NEXT_SESSION_20260710_superseded.md)**
— the pre-run_057 NEXT_SESSION.md, archived when the 2026-07-12 version
replaced it. Historical only.
→ **[`SESSION_LOG.md`](SESSION_LOG.md)** — chronological per-session handoff log
(hypothesis / result / files touched / next-session prompt). Historical once superseded by a newer entry.
→ **`docs/STEP_05_FINDINGS.md`, `docs/p1b_fetch_manifest.md`** — dated,
self-contained investigation notes. Historical, not living docs.

---

Cross-linked from the top of `RUNBOOK.md`, `USER_GUIDE.md`, and `CLAUDE.md`.
