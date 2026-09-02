# E-007 — Recorder storage and host migration: deploy the daemon to culi.to

**State:** planned (re-scoped 2026-08-23 from a decision epic to a deployment epic)
**Owner:** Jeremy
**Updated:** 2026-08-23

## Why

The forward recorder captures order-book depth — the one data axis in this
project that **cannot be backfilled**. Price history can always be
re-downloaded; a snapshot of the book on a given day is gone forever if nobody
was recording. Every day it stays off is permanently lost sample.

It was built and run, then stopped on two findings (ledger R3/R3a, carried by
E-007):

- **R3 — budget.** Measured 12-month projection: **360GB compressed**, against
  a spec estimate of 64GB and a pre-registered budget of **100GB** (5.63×).
  The miss is decomposed and measured — book message rate, bytes/frame,
  compression ratio — not guessed.
- **R3a — host.** The recording host had **0.18GB free** at measurement time.
  Unrelated to the recorder, which had written 59MB total.

**Both premises have moved, which is why this is now a deployment epic rather
than a decision epic:**

- Disk on the Windows host: 0.18GB (R3a) → 8.7GB (E-007 audit, 2026-08-03) →
  **25GB free of 476GB, 95% used** (MEASURED 2026-08-23, `df -h /c`). Better,
  and still nowhere near 360GB/year. The Windows host is not a viable home at
  full scope.
- **A second host now exists.** E-011 S1a completed **2026-08-18** — `culi.to`
  is live with a byte-identical baseline. When E-007 was parked on 2026-08-03,
  "migrate to a host with more capacity" was an abstraction. It is now a
  concrete option, and it is the reason E-007's three-way operator decision
  collapses to one path.

**Operator ruling (2026-08-23):** the storage question must not block the rest
of the board. Deploy the daemon to `culi.to` under a scope that fits a real
budget; partial coverage recorded beats full coverage not recorded, and the
scope can widen later.

## Done when

1. A scope is chosen and recorded **in writing with its derivation** — how many
   symbols, what book depth, what sampling rate — sized against a stated
   budget on `culi.to`. The 360GB/yr figure is the baseline it is scoped down
   from; state the reduction factor and what coverage is being given up.
2. The recorder runs on `culi.to`, not on the Windows host.
3. Liveness and coverage are verifiable by the recorder's own existing tooling
   (`tools/recorder/coverage_report.py`, `tools/recorder/liveness.py`) — not by
   someone remembering to check. A stopped recorder must be visible without
   being looked for.
4. Storage growth is monitored against the chosen budget, with a stated action
   at the threshold (rotate, prune, widen, or stop) decided **before** the
   threshold is hit, not after.
5. No engine change; no effect on any recorded backtest metric.

## Stories

- [ ] S1 — **Characterize the scope options.** What a 100GB/yr shape actually
      covers versus 360GB/yr: symbols × depth × sampling rate, with the
      coverage given up named explicitly for each. Also confirm `culi.to`'s
      real available capacity — do not inherit the 100GB number, which was
      pre-registered before anything was measured. No deployment.
- [ ] S2 — Deploy under the chosen scope; confirm liveness and coverage.
- [ ] S3 — Wire the budget monitor and its pre-decided threshold action.

## Relationship to other epics

- **E-011** (shared campaign execution location) — supplies the host. S1a done
  2026-08-18.
- **E-017 / E-018** — both parked citing Phase 2's gate, whose only unmet
  clause is "recorders running." This epic owns that clause. **E-018 is
  unparked independently** (2026-08-23, operator) because its input is 38
  verdicts already on disk and it needs nothing from the recorder — see its
  own Log.

## Success signal (pre-registered)

Within 14 days of S2: `coverage_report.py` shows unbroken coverage for the
chosen scope over a continuous 7-day window, and measured storage growth
extrapolates to within the chosen budget rather than to 360GB/yr.

## Log

- 2026-08-03 — `new` → `parked`. Written up in E-001 S4 (dispatch W24) from
  HANDOFF ledger items R3/R3a. Unblock condition: an operator decision on the
  storage budget, which the epic could not make for itself.
- 2026-08-23 — `parked` → **`planned`, re-scoped**. The operator made the
  decision the park was waiting on: deploy to `culi.to` under a scope that
  fits a real budget. Two of the three original options were foreclosed by
  measurement (Windows host: 25GB free of 476GB against a 360GB/yr
  projection); the third acquired a host when E-011 S1a brought `culi.to` live
  on 2026-08-18. The Why, Done-when and Stories above replace the original
  decision-shaped ones.
  **Process correction made in the same session:** this was briefly recorded
  as E-007 `withdrawn` + a new E-033. That was wrong — PROCESS.md amendment 7
  defines `withdrawn` as "was not an epic after all; work continues **as a
  card**," and requires a card reference. This work continues as an epic, at
  full epic size. There is no `superseded` state and inventing one for a
  case that re-scoping handles cleanly would be worse. E-033 was removed and
  its content folded back here, which also keeps every existing citation of
  E-007 (`CAMPAIGN_PROGRAM.md`, E-017, E-018) resolving.
