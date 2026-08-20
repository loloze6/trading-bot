# E-023 — Enable live trading, targeting Kraken (parked until deployment is a real decision)

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-16

## Why

Raised directly by Jeremy (2026-08-15 Slack, alongside the risk-layer
reprioritization below): the live-execution path (`main.py run_bot` →
`core/launcher.py:run_bot` → live `DataManager`) currently only ever runs
against Binance, has never been run in anger, and is known to be buggy in
several places already logged separately in the Notion bug backlog:

- **P3** — live mode passes the performance tracker in as `test_mode`
  (mislabels every live run's recorded state).
- **P4** — live-mode state-recording crash.
- **P5** — no live warmup (the ~120-bar warmup gate the backtest path relies
  on is not exercised before a live run starts trading).

`CLAUDE.fork.md`'s hard rule #1 already forbids running `main.py run_bot` on
the fork at all ("known live-path bugs; keys may exist in env — backtests
only"), so these are not hypothetical. They're just currently three separate,
scattered bug cards rather than one tracked body of work — which makes them
easy to either forget or to nibble at piecemeal without ever actually closing
the path out.

**Deliberately parked, not queued.** Jeremy's call: the objective right now
is running the strategy-research workflow (generating and validating
strategies), not live infrastructure. Live trading needs its own explicit
joint decision before it's ever turned on (per `CLAUDE.fork.md`: "live
trading stays behind the risk layer and its own explicit joint decision").
Sinking time into a live-path refactor now — for a path that stays forbidden
regardless — would trade research throughput for readiness nobody's asked
for yet. This epic exists so the known gaps have one home and aren't lost,
not to schedule work on them.

**Relationship to the risk layer:** related but separate. The mandatory
account-level backstop (kill switch, daily loss limit, flatten-all — see
**E-024**) is about not blowing up an account once live; this epic is about
the live *execution* path itself being functionally broken (crashes,
mislabeled state, no warmup) independent of any risk controls. Both gate
real money; neither gates research.

**Real target venue is Kraken, not Binance.** The live path today only ever
talks to Binance, but none of the fork's recent work points there — the
Kraken ingest, Kraken price/funding feeds (PR #24), and the culi.to Ubuntu
deployment plan all target Kraken. Retitled 2026-08-16 to say so plainly:
this epic's actual deliverable is live trading working, on Kraken, not a
generic multi-venue abstraction and not Binance parity.

## Pointer

**2026-08-16 — P3/P4/P5 migrated in, Dorian confirmed ("go for it. Agree on
all three.", Slack 2026-08-16 01:57).** These three Notion cards are closed
(`Won't fix` — not resolved, relocated) with a pointer back to this epic;
their content is preserved verbatim above and in Notion's own history:
- P3 — https://app.notion.com/p/3a81d1fb05a281ad8718de4bc553c7a9
- P4 — https://app.notion.com/p/3a81d1fb05a28131a173f1aac745d777
- P5 — https://app.notion.com/p/3a81d1fb05a28149b694e151b48ae2b8

Notion mirror for this epic already exists (Dorian created it on sync,
2026-08-15 23:21): https://app.notion.com/p/3bd1d1fb05a281768d0feb96f894efad

## Done when

Not scoped yet — this epic starts `parked` specifically so it does not need
a Done-when until it's actually picked up. When it is, at minimum:
1. P3/P4/P5 (and any other live-path bugs surfaced by then) are reproduced
   with a real file:line root cause each, not just re-described.
2. The live path is parameterized across venues the way the backtest path
   already is (or an explicit decision is made to keep it Binance-only).
3. A real, supervised dry run (test_mode, no live orders) exercises the full
   candle→forecast→allocation→rebalance loop end to end without crashing.

## Stories

Not written yet — first story when this is unparked is a characterize-only
pass (file:line evidence for P3/P4/P5 + a fresh scan for anything else),
matching this repo's own "characterize before implement" convention, before
any fix is designed.

## Log

- 2026-08-15 — `new` → `parked`. Created directly from a Jeremy/Slack call
  consolidating three already-open Notion bug cards (P3, P4, P5) that all
  point at the same live-execution path, plus the Binance-only limitation.
  Parked immediately and on purpose: current priority is the strategy-
  research workflow, and `main.py run_bot` is already forbidden on this fork
  regardless of this epic's state, so there is no urgency pressure to offset
  against research throughput.
- 2026-08-16 — Retitled to name Kraken as the real target venue (matches
  where the fork's actual recent work points, not Binance). Dorian confirmed
  the P3/P4/P5-migration + risk-card-split proposal on Slack; P3/P4/P5
  closed in Notion (`Won't fix`, pointer to this epic) — see Pointer above.
  Risk-layer card split out separately as **E-024** (account-level backstop
  only; per-trade stops/sizing stay in the normal strategy-validation
  workflow, not an epic).
