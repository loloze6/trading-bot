# Coins: the universe, the categories, the final draw

(Shared definition, read by `data_use.md`. Written 2026-11-26, the operator's go on `data_use.md`'s design; the research
draw among drawable coins, 2026-11-27, next steps A12. Code: `common/coins.py`.)

## Business objective, one question
**Which coins may the research, the portfolio and the final test use, so that every kind of crypto is represented and
no person picks the coins?**

## The universe: three rules, applied in this order, once per final draw
1. **Kraken trades it against USD**, with its daily file in `trading-bot/local_data/` (39 coins on 2026-11-26).
2. **At least 3 years of daily data** at the draw (the coin's first day on or before the draw date minus 3 years).
3. **Liquid enough to trade:** its median daily traded value (close × volume) over the 12 months before the draw is
   at least **100,000 USD**. Why this number: the backtest's cost is estimated for a 10,000 USD order (topic 38); an
   order should stay under a tenth of a typical day's trading.

Left out on 2026-11-26 by rule 3: STORJ (14k USD a day), OCEAN (18k), YFI (23k), SNX (33k), COMP (57k), ETC (70k), XTZ
(82k). **32 coins remain.**

## The categories (one category per coin; the coin's main use, as public category lists such as CoinGecko's describe it; read once on 2026-11-26, fixed until the next draw)
| Category | Coins in the universe |
|---|---|
| Payments / store of value | BTC, LTC, XRP, XLM, BCH |
| Smart-contract platforms | ETH, ADA, ATOM, ALGO, TRX, DOT, SOL, AVAX, NEAR, SUI |
| Privacy | ZEC, XMR, DASH |
| Decentralised finance | CRV, UNI, AAVE, INJ, LDO, ONDO |
| Data / infrastructure | LINK, FIL, GRT |
| AI | FET, TAO |
| Meme | DOGE, SHIB, PEPE |

## The final draw
**Rule:** one coin per category, drawn at random among the category's coins with at least 4 years of data at the draw
(why 4, not the 5 first written: with 5, the AI category had no coin left once OCEAN fell to rule 3); Python's
`random.Random(seed)`, the categories in the order of the table, each category's eligible coins sorted by name, one
`choice` each.

**The draw of 2026-11-26** (seed 20261126):
| Category | Eligible | Drawn |
|---|---|---|
| Payments | BCH, BTC, LTC, XLM, XRP | **XLM** |
| Platforms | ADA, ALGO, ATOM, AVAX, DOT, ETH, NEAR, SOL, TRX | **SOL** |
| Privacy | DASH, XMR, ZEC | **DASH** |
| Finance | AAVE, CRV, INJ, LDO, UNI | **UNI** |
| Infrastructure | FIL, GRT, LINK | **LINK** |
| AI | FET | **FET** |
| Meme | DOGE, SHIB | **SHIB** |

**The final group: XLM, SOL, DASH, UNI, LINK, FET, SHIB.** Used by no step until the final test (`data_use.md`, step
12). Redrawn only after that test, with a new seed.

**The portfolio group: the other 25 coins:** BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC,
XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE.

## The research draw, at each run
8 coins among the **drawable** coins of the portfolio group (`data_use.md`, 1.3: a coin that can be tested on at least
half of the check half's windows, counted with the market-profile detector's warm-up): first one per category that has
a drawable coin, drawn at random within it (the categories in the table's order, coins sorted by name), then the rest
drawn among all the remaining drawable coins; `random.Random(<the run's name>)`; the 8 coins and the count they were
drawn from are written in the run's `data_use.json`. A run already started (its `data_use.json` exists) keeps its coins.

**Drawable on 2026-11-27 (19 of 25, 6 categories; check-half windows testable, of 14):**
| Category | Drawable | Not drawable |
|---|---|---|
| Payments | BTC 14, LTC 14, BCH 14, XRP 13 | |
| Platforms | ETH 14, ADA 14, ATOM 14, ALGO 13, TRX 12, DOT 11, AVAX 7 | NEAR 6, SUI 3 |
| Privacy | ZEC 14, XMR 14 | |
| Finance | CRV 11, AAVE 10, INJ 8 | LDO 6, ONDO 0 |
| Infrastructure | FIL 11, GRT 10 | |
| AI | | TAO 0 |
| Meme | DOGE 13 | PEPE 3 |

So a run draws 6 coins by category and 2 among the 13 left; DOGE is in every run (the only drawable meme coin) and no
run has an AI coin. The list is counted again at each run's start (a coin becomes drawable as its history grows).

## Data notes (the data session, `runs/DATA_COINS_RUN.md`)
XLM misses 177 days in a row (August 2017 to February 2018); DASH and ETC 1 day each; BCH's first day has a bad price
(left out by the 90-day rule of `data_use.md`); the 20 coins added on 2026-11-26 come from Kraken's rebuilt archive,
the 19 earlier ones from its earlier edition.
