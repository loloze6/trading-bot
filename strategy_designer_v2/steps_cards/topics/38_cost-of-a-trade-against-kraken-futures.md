# Topic 38: the backtest's cost of a trade against real Kraken futures

Status: designing (values only; the logic stays)  
Where: engine settings (`trading-bot/config/cost_model.json`, shared config)  
Opened: 2026-11-20, the operator: "yes to ensure we have cost reflecting reality as close as we can (keeping same
logic, but different value). So far the bot would be taker. Let's park if we should do it maker."

## Question
Does the cost the backtest charges for a trade match what a taker order costs on Kraken futures, coin by coin?

## Seen
- The backtest charges, per trade (one way): a fee of 5 bps plus a slippage of 7.5 bps by default, 2.5 for BTC and
  4 for ETH (`cost_model.json`, `kraken.futures`; the file calls the default "conservative", not calibrated). So a buy
  plus a sell costs 15 bps on BTC, 18 on ETH and 25 on every other coin. The backtest's balance is 1,000 USD
  (`core/launcher.py`).
- The fee is right: Kraken futures charges a taker 0.05 % (5 bps) and a maker 0.02 % at the lowest tier.
- The slippage, measured on one snapshot of Kraken futures' public order books (2026-11-20, about 00:40 Paris, a quiet
  hour). It is the gap between the average fill price and the mid-price, for an order that crosses the book (taker),
  the mean of a buy and a sell, in bps:

| Coin | Backtest | Half the spread | Order of 10k USD | 100k USD |
|---|---|---|---|---|
| BTC | 2.5 | 0.1 | 0.1 | 0.9 |
| ETH | 4 | 0.3 | 0.5 | 1.7 |
| XRP | 7.5 | 1.1 | 3.0 | 4.5 |
| LTC | 7.5 | 1.2 | 6.4 | 11.7 |
| ZEC | 7.5 | 3.0 | 7.2 | 11.2 |
| XMR | 7.5 | 3.7 | 10.7 | 29.4 |
| SOL, DOGE, SUI, TRX | 7.5 | 0.2 to 1.8 | 1.1 to 5.1 | 3.6 to 17.4 |
| AVAX, LINK, UNI, TAO, ADA, ONDO, NEAR, AAVE | 7.5 | 0.8 to 4.9 | 5.1 to 8.9 | 11 to 19 |
| INJ | 7.5 | 4.7 | 18.2 | 34.6 |

  What it shows: on BTC and ETH, the backtest charges far more than the book does (2.5 against 0.1 to 1; 4 against
  0.3 to 2). On the other coins it is about right at 10k USD, and too low above that (XMR, INJ).
- Limits of this measure: one snapshot, at one quiet hour; spreads widen when the market moves, and a strategy's
  trades are often when it moves. The backtest's years start in 2016, when these contracts were thinner than today:
  today's spreads applied to those years are optimistic.

## Why it matters
The cost decides which ideas can pay (`common/findings.md`, F10 and F11). A cost too high on BTC and ETH rejects ideas
that would pay there; a cost too low on thin coins accepts books that would not.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Measure each coin's taker slippage at one stated order size, from Kraken futures' public order books sampled over several days and hours (a small sampler, a few days of snapshots), and write the median per coin into `cost_model.json` | values from the real venue, at the size the bot would trade; the logic unchanged | a few days before the values exist; the past years stay optimistic |
| B. Write today's snapshot into `cost_model.json` now | immediate | one quiet hour decides every later result |
| C. Keep today's values | no change | BTC and ETH overcharged, thin coins undercharged |

Recommended: A, with the order size set by the operator (the table shows the cost grows with it). Then the proof the
rules ask for: the same records rerun with the new values, compared file by file, the allowed differences named (the
costs and what they move: returns, Sharpe, step 6's checks), and the counts of verdicts and paying books that change.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-20 | The bot is a taker: the cost is the taker fee plus crossing the book | the operator | how the bot would trade today | maker: parked (below) |
| 2026-11-20 | Maker execution is parked | the operator | to decide later whether the bot should place limit orders | — |

## Status and next
Waiting on the operator: the order size to calibrate at, and the go for option A. Shared config: the values change
only with the proof and the operator's go. Parked: maker (fee 0.02 %, no spread crossed, but orders may not fill).

## Links
`trading-bot/config/cost_model.json`, `trading-bot/config/cost_model.py`, `common/measures.md` ("The cost of a trade"),
`common/findings.md` (F1, F10, F11).
