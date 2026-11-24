# Topic 51: a position smaller than the rebalance band is never closed

Status: open (found 2026-11-24; for the operator)  
Where: engine (shared code: the risk layer's `min_allocation_change`); research: what a book holds after its bets end  
Opened: 2026-11-24, the designer, from topic 49's proof (a book that must be flat outside its market profile).

## Question
When a book's bets have all ended and it is asked to be flat, should it close a small remaining position, or keep it
until the next bet?

## Seen
- **The rule** (`03_test_plan/helper/reference/strategy_config_guide.md`, the risk layer): a rebalance whose size is below
  `min_allocation_change` (0.2 of the capital by default, 2 forecast points) is refused. Closing a position is a
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

## Status and next
Found; the operator's decision. First step if wanted: B's measure on the register's paying books (computing only).

## Links
Topic 49 (`49_review/profile_book_check.py`, the proof that found it); topic 47 (N3: the book trades the idea's
situation); `common/forecast.md` (7: the holding period); `trading-bot/risk/risk_manager.py`.
