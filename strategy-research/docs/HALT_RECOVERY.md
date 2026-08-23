# Halt recovery + loop-health instrument (E-030)

Not sure this is the doc you need? See [`DOC_INDEX.md`](../DOC_INDEX.md) first.

What `workflow/run_campaign.py` does when a run halts, why it now sometimes
doesn't stop the whole campaign, and how to read the numbers it keeps about
itself. Built across E-030's stories (S1.5, S2a, S3, S4) — see
`engineering/roadmap/E-030/EPIC.md` for the full evidence and history behind
every decision below; this doc is the short reference, not the case for it.

---

## 1. Durable halt record (`halt_history`)

**Objective.** Make sure the exact reason a run halted is never lost. Before
this, a halt's full error text was truncated to 300 characters for the
`campaign_log.md` line, and the operator's own documented resume procedure
nulled it on every resume — together, the record of what actually went wrong
often didn't survive past the fix.

**Logic.** `pipeline_state.yaml` gets one more field, `halt_history`, that
only ever grows — the same pattern `completed_stages` and `audit_log` already
use on that file. Every time the campaign halts (or quarantines — see below),
a full snapshot is appended *before* anything resets: timestamp, reason,
**untruncated** error text, `pending_stage`, the `flags` dict, and (if it was
a quarantine) the quarantine record.

**Where to look.** `runs/<run_id>/pipeline_state.yaml`, key `halt_history`
(a list — read the last entry for the most recent halt).

**Parameters to know.** None — always on, no config, pure addition.

---

## 2. Quarantine + escalate policy

**Objective.** Stop the whole campaign only for halts that genuinely need a
human. A backtest showed 84.7 hours (67% of all halted time, measured
2026-07-06 → 2026-07-19) was engineering plumbing, not research judgment —
this lets the queue advance past the plumbing on its own.

**Logic.** Four reason codes, and *only* these four, are quarantine-safe:

| Reason | Outcome | Why |
|---|---|---|
| `no_signal_artifact` | terminal (`status: done`) | a component never fired — an engineering fact, not a research result |
| `component_execution_error` | terminal | a real engine bug; no retry fixes it and the queue has no reason to stop |
| `component_gap` | re-queueable (`status: blocked_on_component:<name>`) | the engine is missing a piece, not the hypothesis wrong |
| `new_component_escalation` | re-queueable, same as above | same situation, reached from a different stage |

A quarantined run's queue entry gets `outcome: quarantined_engineering_failure`
— never `completed_rejected`, which is a scientific claim this isn't making.
**Every other reason still halts the campaign exactly as before**, including
`unhandled_exception` (too many unrelated causes to trust blindly) and every
research-integrity reason (`kb_reactivation_violation`,
`research_only_unverified`, holdout-related pauses, etc. — these are never,
under any config, auto-actioned).

Trial accounting is handled per reason so the deflated-Sharpe count stays
honest: `component_execution_error` marks any existing trial row invalid
(never deletes it — a real backtest ran, it just measured a bug, not the
hypothesis); `no_signal_artifact` needs no action (already recorded upstream
at prescreen); the two re-queueable reasons haven't touched data yet.

A safety check (R11) runs before every quarantine decision: if the run's
`flags` don't unambiguously support the reported reason (a stale flag from an
earlier, already-resolved pause can otherwise misreport what's actually
wrong — this happened for real once, see the epic for the incident), the halt
escalates instead of being quarantined, and says why in the log.

**Where to look.** `campaign_log.md` — a `QUARANTINE —` line instead of
`HALT —`. The full record (including the untruncated error) is on that run's
`halt_history[-1].quarantine`. A quarantined run **never appears as a
`paused:` entry**, so `RUNBOOK.md`'s `--resume` procedure won't find it —
that's intended, not a bug.

**Parameters to know.**

```yaml
# config/campaign_config.yaml
orchestrator:
  halt_policy:
    quarantine_enabled: false   # default. Set true to turn this on.
```

Ships **off**. With it off, every halt behaves byte-identically to before
this feature existed (proven by test, not just claimed).

---

## 3. Loop-health instrument + repeat-escalate

**Objective.** Give the campaign (and a human reading it) a live, computed
picture of how much halting is actually costing it, and let the loop use
that picture to make one real decision on its own — not just report the
number and leave a human to act on it.

**Logic.** `campaign_record/loop_health.yaml` is recomputed and rewritten
from scratch on every queue step (halt, quarantine, or done) — it's a
projection, never accumulated, so a stale or hand-edited copy self-repairs
on the next step. It reports: halt count, total/median downtime hours,
downtime share of the campaign's whole span, a breakdown by cause
(`quarantine_safe` vs. `escalate` — there's no `retry_safe` bucket, because
the one known retry-safe failure is resolved before it ever becomes a halt),
and how many halts were auto-recovered vs. escalated to a human.

**The one decision it drives:** if the *same* quarantine-safe reason fires
twice in a row on the *same* run, the second occurrence escalates instead of
being quarantined again. A reason that keeps recurring isn't being fixed by
auto-quarantining it repeatedly — it needs a human. (This mirrors the exact
rule already used for the one known retry-safe failure: try once
automatically, a second identical failure goes to a human.) The log shows a
`REPEAT-ESCALATE —` line when this fires.

**Where to look.** `campaign_record/loop_health.yaml`, regenerated every
step — read it fresh each time, never trust an old copy.

**Parameters to know.** None separately — gated by the same
`quarantine_enabled` flag as section 2 (with the flag off, nothing is ever
quarantined, so there's nothing to repeat-check either).

---

## 4. What's *not* here — retry (S2b)

There is no automatic retry mechanism at the campaign level, and none is
planned until real evidence for one shows up. The one failure class that's
provably safe to retry (a specific SDK misclassification bug) is already
handled — at the *stage* level, inside `run_phase1_research.py`, before a
halt is ever logged. Every other halt reason either needs a human by
definition (research-integrity reasons) or doesn't yet have evidence that
retrying it would actually help. If you're reading this because a halt is
recurring and you think it should retry automatically: that needs a new,
evidenced case first, not a config flag — see E-030's epic for the standing
rule (`R2`–`R5`) this would have to satisfy.

---

## 5. Quick reference — is my halt going to stop the campaign?

1. Is the reason on the four-item table in section 2, **and** is
   `quarantine_enabled: true`? → No, it quarantines and the queue continues
   (unless the flags looked ambiguous, or this exact reason just fired on
   this same run — then it escalates).
2. Otherwise → Yes, it halts, exactly as it always has. See `RUNBOOK.md`
   section 3 for the full reason table and how to resolve each one by hand.
