# Topic 53: which coins, grouped how, weighted how

Status: parked (the operator, 2026-11-25)  
Where: research: common (data, the profile map), steps 2, 3, 5, 6, the step 7 lines; the portfolio layer (topic 44)  
Opened: 2026-11-25, the operator, from 1q ("how do you manage the fact that a backtest can vary by coin?"): "the coins
were selected without rationale; we test at equal weight and the verdict is global; the analysts do not differentiate.
Possible improvements: coin categories by characteristics, and a reallocation by regime to keep the portfolio's
standard deviation stable."

## Question
Which coins should an idea be tested on, should coins be grouped by what they are, and how should capital be spread
across coins and strategies so that the portfolio's risk stays stable?

## Seen (2026-11-25)
- **The coins were chosen by data, not by a rationale** (`common/data_available.md`): the 6 default coins (BTC, ETH, LTC,
  XMR, XRP, ZEC) are those with Kraken data in all four folds; 13 more were added as their data exists (some in folds A
  and D only, four in fold D only). No characteristic (size, liquidity, swing, link to BTC) chose them.
- **Equal weight, one verdict:** a book's return is the mean of its coins' daily returns (step 6); step 5 pools every
  coin's cases into one verdict. A book earning on 2 coins of 6 counts as earning.
- **The analysts do not differentiate by coin:** line 7.e reads "one coin" as a possible source of a gain; no line
  proposes an idea for a kind of coin.
- **The profile map does not show coins** (1q): of the 109 paying books, 68 run on the 6 default coins, 30 on 19, 11 on
  1 to 18; "falling agitated: 12 strategies" mixes books tested on different coin sets.
- **A coin's own profile** differs from the six coins' average on 37 to 54 % of days (`common/market_profile.md`):
  coins are not one market.
- **Risk is not stable:** P4's 20 books at equal capital had a worst fall of 11.1 % on 2016-17 and 4.8 % on 2026
  (`runs/PORTFOLIO_UNSEEN_RUN.md`). A volatility target inside one book did not lift the typical book (topic 47, 1d-5);
  across books it was not tried.

## Why it matters
Without it, a strategy's verdict hides on which coins it works, the search cannot aim at a kind of coin, and the
portfolio's risk follows the market's swings.

## Options (to weigh when it is opened)
| Option | Gain | Risk |
|---|---|---|
| A. The profile map shows each book's coins (the designer's suggestion, 1q) | lines 7.e and 7.g see a profile covered on some coins only; a few lines of code | visibility only |
| B. Coin categories by characteristics, defined in `common/` (for example size and liquidity, usual swing, link to BTC, age), measured on past data only; an idea may name a category as it names a profile; step 6 reports the gain by category (informative) | ideas aimed at kinds of coin; a reason for each coin set | categories fitted on the same data the ideas are tested on; fewer cases per category |
| C. Weights across coins by risk (each coin the same share of the book's risk, not the same capital) | a book is not carried by its most volatile coins | changes every book's measures; needs a proof as for any engine or step 6 change |
| D. The portfolio's exposure scaled by regime to keep its standard deviation stable; and the money moved each day to the strategies that hold a position that day (parked from the combination step, 2026-11-25) (a volatility target at the portfolio level, with the profile map's regimes) | the risk the operator holds stays the same in calm and agitated markets | belongs to the portfolio layer (topic 44, P5, P10); a target chosen after seeing results fits noise |

Recommended order when opened: A first (cheap, visibility); then B's definition and its informative measure, before
any rule; D with the portfolio layer (P10, P5).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-25 | Parked, with the designer's suggestions | the operator | a broader topic than 1q's map | |

## Status and next
Parked.

## Links
`common/data_available.md`; `common/market_profile.md` (the profile map); topic 44 (the portfolio layer, P10); topic 47
(1d-5); topic 50 (1q); `runs/PORTFOLIO_UNSEEN_RUN.md`.
