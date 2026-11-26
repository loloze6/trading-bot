# Coins: the universe, the categories, the final draw

(Shared definition, read by `data_use.md`. Written 2026-11-26, the operator's go on `data_use.md`'s design. Not yet
read by any step: the research still runs on its 6 coins until `data_use.md` is built.)

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
8 coins from the portfolio group: first one per category, drawn at random within it (the categories in the table's
order, coins sorted by name), then an 8th drawn among the rest; `random.Random(<the run's name>)`; the 8 coins written in
the run's header. Every category has at least one coin in the portfolio group (AI: TAO).

## Data notes (the data session, `runs/DATA_COINS_RUN.md`)
XLM misses 177 days in a row (August 2017 to February 2018); DASH and ETC 1 day each; BCH's first day has a bad price
(left out by the 90-day rule of `data_use.md`); the 20 coins added on 2026-11-26 come from Kraken's rebuilt archive,
the 19 earlier ones from its earlier edition.
