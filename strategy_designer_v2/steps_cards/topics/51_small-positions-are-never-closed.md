# Topic 51: a position smaller than the rebalance band is never closed

Status: option A built on the working branch 2026-11-25, proof below; merging into master is the operator's go (it changes topic 19's decision)  
Where: engine (shared code: the risk layer's `min_allocation_change`); research: what a book holds after its bets end  
Opened: 2026-11-24, the designer, from topic 49's proof (a book that must be flat outside its market profile).

## Question
When a book's bets have all ended and it is asked to be flat, should it close a small remaining position, or keep it
until the next bet?

## Seen
- **The rule** (`03_test_plan/helper/reference/strategy_config_guide.md`, the risk layer; kept: topic 19): a rebalance
  is refused when both the signal's change (forecast / 10) and the sized change are below `min_allocation_change` (0.2). Closing a position is a
  rebalance, so a position under 0.2 stays open until a bet changes it.
- **Example** (topic 49's proof, idea 025-01 "in a falling market, a large one-day rise is given back over 5 days",
  ETH, fold C, window w14): its last bet ends; the book is asked to go flat from a short of 9 % of the capital; the
  engine refuses each day (`approved_rebalance` False) and the short stays open 9 days, outside the idea's situation and
  outside its market profile.
- **How much, on that book:** 553 of its 6,708 days in a position (8 %) are days with no forecast within the idea's
  horizon: leftovers. Median size 0.14 of the capital, against 0.45 on all its days in a position.

## Why it matters
A leftover is a position the idea did not ask for: it collects the market's own moves, outside the idea's situation
(topic 47, N3) and outside a named profile (topic 49). On a short book in a rising market it loses; on a long book it
collects the market's drift. It also makes a book look in position more often than its idea says.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. A move to flat is never refused by the band (the band still filters small changes between two non-zero positions) | a book is flat when its idea says so; one rule for every book | engine change (shared code, the operator's go, a rerun proof); every past record changes slightly (one more trade per leftover: its cost) |
| B. Keep the rule; measure leftovers in step 6's check (days and share of the book's gain) | no engine change | the books stay as they are; visibility only |
| C. No change | none | leftovers stay unseen |

Recommended: A, after B's measure on the paying books shows how much they matter: if leftovers carry a material part of
a paying book's gain or loss, the book is not what its idea says.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-25 | Option A built on the working branch, proven (above) | the operator ("go for 1l") | | |
| 2026-11-25 | Un-parked: option A to design and prove | the operator ("it would make sense to clean the small positions never closed ... keep solution simple") | night 7 (M8): a median 16 % of the profile specialists' days in a position are leftovers outside their profile; they also count in step 6's days in a position | B: measuring alone leaves the books unlike their ideas |
| 2026-11-24 | Parked | the operator ("park that") | the rule was already decided (topic 19: kept, so backtests and live follow the same rule); this adds one measure (a short book in falling markets: leftovers 8 % of its days in a position, median 0.14) | |

## The build (option A, 2026-11-25)
`trading-bot/risk/risk_manager.py`: `approve_allocation_change` takes the order's target; a move to flat (target exactly
0, a position to close) passes the `min_allocation_change` band whatever its size (`passed_on` "flat" with a sizing
block). `core/trading_bot.py` passes the target on both band calls. Every change between two non-zero allocations is
judged as before. Backtests and the live bot follow the same rule (topic 19's reason kept). Tests:
`tests/test_d176_sizing_block.py` (the rule, with and without a sizing block); `tests/test_d176_master_replay.py` now
checks the named difference against the master recordings (below); bot suite 1674 passed, cards 164.

## Proof (2026-11-25; 0 USD)
**The master recordings** (`strategy-research/tests/fixtures/d176`, two real configs over a seeded series): every row
byte-identical up to the first close of a remainder (run_084: 2019-09-21, forecast 0, a 10 % long the old rule kept);
from it on, every row where the approval differs is such a close or follows from one (the book entered the bar
differently). The recorder writes the end-of-run cash on every row (`balances.USDT.free`: one value in the whole
file), so those two columns differ from the first row and are left out of the comparison.

**Seven research books rerun on both engines** (step 4, the same plans and data; 4 of night 7's specialists and 3 of
the portfolio's 20; script `topics/51_review/compare.py`, table `topics/51_review/compare.csv`): 1,408 coin-windows;
763 identical; in every other one the first differing bar is a close of a remainder under the band (the old engine
did not trade it, this one closed it to flat), and every later difference follows from it; 0 unexplained.

| Book | Days in a position, before → after | Sharpe (daily), before → after | Days inside its profile |
|---|---|---|---|
| 038-01 falling agitated | 1,745 → 1,324 | 1.07 → 1.07 | 81 % → 99 % |
| 034-02 rising | 9,039 → 5,087 | 1.35 → 1.39 | 64 % → 83 % |
| 035-01.b1 calm | 20,891 → 17,331 | 1.19 → 1.11 | 80 % → 95 % |
| 045-01 rising | 1,894 → 1,894 | 1.09 → 1.09 (identical) | |
| 002-03 (portfolio) | 18,155 → 14,489 | 0.91 → 0.90 | |
| 011-01 (portfolio) | 6,809 → 4,287 | 0.77 → 0.78 | |
| 013-04 (portfolio) | 237 → 237 | 0.52 → 0.52 (identical) | |

What it changes elsewhere: every backtest from now on (a book's days in a position fall where it kept remainders; its
gain moves a little either way); records made before are not rerun; the live bot closes a remainder when its strategy
asks for flat (one more small order).

## Status and next
Parked. Note: the band is 2 forecast points of signal change, or 0.2 of the capital of sized change, whichever passes
(`trading-bot/risk/risk_manager.py`); only a leftover under both is never closed. Topic 19 holds the decision.

## Links
Topic 49 (`49_review/profile_book_check.py`, the proof that found it); topic 47 (N3: the book trades the idea's
situation); `common/forecast.md` (7: the holding period); `trading-bot/risk/risk_manager.py`.
