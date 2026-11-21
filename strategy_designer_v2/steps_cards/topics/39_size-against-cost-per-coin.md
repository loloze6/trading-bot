# Topic 39: the idea's size against the cost, coin by coin

Status: open (parked: small gain measured)  
Where: research: step 5 (`size.json`), step 7 (the size against the cost)  
Opened: 2026-11-21, the operator: "the standard move is different per coin... ratioing the size with the standard
deviation of the coin?"; then "only if we do not introduce extra complexity for almost no impact".

## Question
Should the idea's move per case be compared with the cost coin by coin, instead of pooled over the record's coins?

## Seen
- The strength is already per coin (the move divided by the coin's own usual move, `common/measures.md`). What is
  pooled: the move per case in % (mean over all coins' cases) and the cost (mean over the coins).
- Each coin's usual move and cost differ (1h record, new costs): over 1 day, BTC 3.6 % for 0.10 %, XMR 4.7 % for
  0.31 %. The strength an idea needs to cover the cost over 1 day: 0.024 to 0.029 on BTC, ETH, XRP; 0.040 to 0.045 on
  ZEC, LTC; 0.067 on XMR (real ideas: about 0.05, F10).
- Measured on the 123 confirmed ideas with a size (848 coin books, the costs their records paid; scratch script, not
  committed): 62 ideas have coins on both sides of their own cost. Whether a coin covers its own cost tells whether
  that coin's book earns (sum of its window returns > 0) 79.5 % of the time; the pooled reading, 77.1 %. The two
  disagree on 130 coin books; the coin's own reading is right on 75 of them. 8 ideas read "too small" pooled have at
  least one coin that covers its cost and earns.

## Why it matters
A small gain in reading accuracy (about 2 points). The per-coin reading matters only if an idea may be traded on part
of its coins, which is choosing coins on the data that judges the idea (topic 31).

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Per-coin lines in `size.json`, read by step 7 against each coin's cost | about 2 points of accuracy; step 7 can name the coins an idea pays on | more numbers in step 7's context for little change |
| B. Keep the pooled reading | simple | an idea that pays on BTC and ETH but not XMR reads as one mean |

Recommended: B now. Reopen with topic 31 (choosing on some folds, judging on others), when choosing an idea's coins
can be done without judging on the same data, or if the calibrated costs (topic 38) widen the gap between coins.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Parked | the session, on the operator's condition ("not extra complexity for almost no impact") | gain measured at about 2 points | A: built now, little change |

## Status and next
Parked. Reopen with topic 31, or when a run shows an idea lost for its pooled reading.

## Links
`common/idea_size.py`, `common/measures.md` ("The size of an idea"), `common/findings.md` (F10, F11), topics 31, 38.
