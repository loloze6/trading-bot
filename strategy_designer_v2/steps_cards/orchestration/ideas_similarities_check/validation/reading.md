# ideas_similarities_check: validation (2026-11-22)

**Inputs:** the 35 paying books rerun on today's engine (`runs/PAYING_RERUN_RUN.md`: 22 daily, 9 hourly, 4 four-hourly),
added to the register (`register/`), then every book compared with the 34 others and with holding (`--all`). No model
call.

| Card's "done when" | What happened |
|---|---|
| The tests pass | 9 of 9, on books whose answer is known (a copy, a copy one period apart both ways, the opposite, noise, under a year in common, periods outside the window) |
| Daily returns equal step 6's | on 3 records (two daily, one hourly): identical, largest difference 0.0 |
| The register holds every paying book on today's engine | 35 of 35 (the older plans as they are: no holding setting, operator 2026-11-21) |
| On night 3's books, the comparisons say what the hand checks said | the 7 ideas checked by hand (`runs/NIGHT3_RUN.md`: 2 resistance breakouts, 2 four-hour breakouts, 3 hourly rebounds) each have a nearest relative explaining 0.65 to 0.91 of them, with what is left at t below 2.5: "a profit we already have". Step 7 A/B's 1-day reversal, which should read differently, has a nearest relative explaining 0.21 |

**Met.**

**What the register shows (the 35 books, `register/COMPARISONS.md`):**
- 33 of 35 have a paying relative that explains 0.42 to 0.99 of them, almost all momentum variants; near copies exist
  ("strong rises keep rising" and "strong monthly rises continue": 0.99).
- Matches across bar sizes: hourly nearness to highs with the four-hour 30-day trend (0.86), the hourly weekly rise with
  the four-hour pullback inside a rising week (0.84).
- Two books stand apart, both daily reversals: "one-day reversal against the trend" (nearest relative 0.21) and
  "volatile reversal completes quickly" (0.12); holding explains 0.02 of them, against 0.3 to 0.6 for the momentum books.
- In every nearest pair the match is on the same period (no book leads another by one period).

**Size:** the register holds about 1.3 MB per hourly book (its hourly, 4-hour and daily returns), 11 MB for the 35. Stored
to 7 significant digits, dates as UTC seconds, holding at the book's own bar only: on all 1,190 pairs, the shares
explained change by at most 3e-8 against a full-precision store, no nearest relative and no reading of who leads changes.
