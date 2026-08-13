# E-021 — Consolidate bug/ticket tracking onto GitHub; narrow Notion's role

**State:** new
**Owner:** Jérémy (joint with Dorian)
**Updated:** 2026-08-13

## Why

The Notion "🐛 Bugs & Tasks" board has drifted stale from git multiple times
in one week: PR #21 and PR #22 both sat merged for 1-2 days while their
Notion cards still said "Open"/unset, caught only by a manual audit
(2026-08-13). Root cause: nothing connects a merged PR to its Notion card
automatically — a human or an agent has to notice and update it by hand,
and that step keeps getting skipped.

`PROCESS.md`'s own "## Notion" section already states the fix for this
*class* of problem, but only applied it to epics: "Git is authoritative for
state. Notion is a notification surface, not a second state store — two
state stores is how parallel taxonomies get created." GitHub Issues/PRs
already demonstrate the same principle working for free at the ticket
layer: issue #20 was auto-closed by PR #21's "Closes #20" on merge, no
manual step, no drift. The Bugs & Tasks board never got the same treatment
— this epic extends the existing principle down to it, rather than
inventing a new one.

A same-day stopgap exists (a daily agent-run sync check between GitHub and
Notion, self-bound to the current session — see Slack #tradingbot,
2026-08-13) but it's a workaround for the drift, not a fix for its cause;
it should become unnecessary once this epic ships, not a permanent fixture.

## Done when

Not yet fully testable — S1 is a joint decision with Dorian, same shape as
E-004/E-006. Provisionally, once decided:
- New bugs/tasks are filed as GitHub Issues, not Notion cards.
- A merged PR referencing an issue auto-closes it — verified by opening one
  real test issue, linking a PR with "Closes #N", merging, and confirming
  the issue closes with no manual step.
- Notion's role is written down explicitly (process/reference docs only:
  the technical review, the edge playbook, protocol pages) and the Bugs &
  Tasks board is either retired or frozen to read-only historical record.
- The daily Notion-sync routine (trig_01Hjj36FwMK7AgsfU4b55kXz) is deleted,
  because there's nothing left for it to reconcile.

## Stories

- [ ] S1 — Joint conversation with Dorian: share this proposal (GitHub
      Issues for tickets, EPIC.md stays in git for deep write-ups, Notion
      narrows to reference/process docs, Slack stays ephemeral-only) and
      get his read before touching anything he relies on daily.
- [ ] S2 — (blocked on S1) Small trial: file 1-2 real upcoming bugs as
      GitHub Issues instead of Notion cards, observe whether PR-linked
      auto-close actually removes the manual-sync step in practice, for
      roughly a week.
- [ ] S3 — (blocked on S2) Go/no-go based on the trial. If go: migrate
      remaining open Notion Bugs & Tasks cards to GitHub Issues, update
      `PROCESS.md`'s "## Notion" section to state the ticket-layer rule
      explicitly (not just the epic-layer one), retire the daily sync
      routine.

## Log

- 2026-08-13 — `new`. Raised by Jérémy after a Slack-review session
  exposed 3 stale Notion cards in one week; discussed with agent same day.
  Checked the tree first (Amendment 9): `PROCESS.md` already states the
  governing principle for epics, no existing epic covers extending it to
  the Bugs & Tasks board — E-004 is a narrower, unrelated naming dispute
  (`briefs/` vs `briefs_record/`). Deliberately left at `new`: needs
  Dorian's input before anything changes under him.
