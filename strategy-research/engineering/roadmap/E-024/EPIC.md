# E-024 — Mandatory live-trading safety backstop (kill switch, daily loss limit, flatten-all)

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-16

## Why

Split out of the single Notion "Build real risk layer" card (`risk/risk_manager.py`,
52 lines today; "Prerequisite for ANY live run"), which bundled two
conceptually different things:

1. **Per-trade stops, position sizing, leverage caps.** These shape a
   strategy's own return profile — the engine already treats sizing as part
   of a strategy's edge (forecast → allocation, and vol-targeted sizing is
   already on the fork's own edge-playbook shortlist as a *strategy* idea,
   not an infra one). A universal stop imposed on every strategy by default
   could fight a strategy that's deliberately designed to ride a drawdown.
   **Not this epic's scope** — these belong in `strategy_config.json` /
   the normal validation-and-iteration workflow (`strategy-research/`),
   decided per strategy as its characteristics are established, not
   centrally dictated. No epic needed for this half; it's business as usual
   for strategy authoring.

2. **Account-level circuit breakers**: max-drawdown kill switch (flatten +
   halt), daily loss limit, manual flatten-all command, order-failure
   reconciliation. **This is this epic's actual scope.** These don't shape a
   strategy's returns — they exist to bound the damage from things a
   strategy's own backtest characterization *cannot* see: a bug in the live
   execution path (see **E-023**'s P3/P4/P5 — exactly this class of thing),
   an exchange outage, a corrupted feed, a forecast going haywire live. If
   whether the breaker exists were "decided per strategy," the one strategy
   that ships with an undiscovered bug — which is definitionally the one
   that never got flagged during validation — is the one that trades without
   a backstop. That inverts the point of having one. It's also close to
   free: a strategy behaving as backtested never trips it.

Decided jointly with Dorian (Slack, 2026-08-16): agreed as a mandatory,
strategy-blind baseline, separate from strategy-level risk parameters.

## Done when

Not scoped yet — parked on purpose, same reasoning as E-023: current
priority is the strategy-research workflow, and this only matters once a
live deployment is a real, jointly-made decision (`CLAUDE.fork.md`: "live
trading stays behind the risk layer and its own explicit joint decision").
When unparked, at minimum:
1. Max-drawdown kill switch: flattens all positions and halts trading past a
   pre-agreed drawdown threshold.
2. Daily loss limit: halts new entries (existing behavior TBD — flatten vs.
   hold) past a pre-agreed daily loss threshold.
3. Manual flatten-all command: operator can force-close everything on demand.
4. Order-failure reconciliation: a rejected/partial order doesn't leave the
   bot's internal state silently diverged from the exchange's actual
   position.
5. All four are strategy-blind — no strategy config can disable them.

## Stories

Not written yet — first story when unparked is a characterize-only pass over
`risk/risk_manager.py`'s current 52 lines (what, if anything, already exists)
before designing the four pieces above.

## Log

- 2026-08-16 — `new` → `parked`. Split out of the Notion "Build real risk
  layer" bug card (closed `Won't fix`, pointer here:
  https://app.notion.com/p/3a81d1fb05a281d696a6e1e7a21ed1db) after a
  Jeremy/Dorian Slack exchange on whether risk controls are a strategy
  characteristic or mandatory infra — resolved as both, split accordingly:
  this epic covers only the infra half (account-level backstop); per-trade
  sizing/stops stay in the normal strategy-validation workflow, no epic.
  Parked immediately: same rationale as E-023, no urgency to offset against
  the research-workflow priority, and `main.py run_bot` is already forbidden
  on this fork regardless.
