# Measure the universe: every coin Kraken trades against USD (2026-11-28, branch `measure-universe`)

## Purpose and expected outcomes (written before measuring)
**Purpose:** one table of every coin Kraken trades against USD, so the operator can decide the universe's rule on facts
(next steps A13). Today the universe is "the coins we have a file for": 39, of which 20 were asked for by the designer.
No coin is added to `trading-bot/local_data/`, no rule changes, nothing in `trading-bot/` changes. No model call.

**Expected (before the numbers):**
| Question | What I expect |
|---|---|
| Pairs Kraken lists against USD | several hundred (the API's `AssetPairs`), of which a minority are fiat, stablecoin or wrapped/staked |
| Pass "liquid at 100,000 USD a day, median over 12 months" | a clear minority of the pairs (most of the list is small tokens) |
| Pass "3 years of history" | roughly a third of the pairs (Kraken listed many coins from 2024 on) |
| Pass "testable on at least 7 of the 14 check-half windows at 790 days" | few: the 790-day warm-up needs a first day in or before about 2021 |
| Coins that pass everything and that we do not have | some, but fewer than 20; most of the older liquid coins are already among the 39 |
| Usable window before 2022 | only the oldest (2017-2020 listings) |
| Perpetual future on Kraken | most liquid large coins yes, small ones no |

The reading below says which of these happened.

## What was done
Public endpoints only, no key; a pause of 1.2 s between Kraken calls (7 s for CoinGecko), a wait and retry on a rate limit
(CoinGecko answered 429 twice on the first pages and was retried; Kraken never). No host was blocked. Nothing added to
`trading-bot/local_data/`, nothing changed in `trading-bot/`. Scripts: `runs/measure_universe/` (`fetch_kraken.py`,
`refine_first_day.py`, `fetch_categories.py`, `build_table.py`); the raw answers are not committed (records stay small).
Table: `common/universe_measure_2026-11-28.csv`, 664 rows, one per USD pair. Data read on 2026-11-28; the last complete
day is 2026-11-27.

| Item | How it was measured | Precision |
|---|---|---|
| Pairs | `AssetPairs`, every pair whose `wsname` ends in `/USD`: 664 (628 online, 34 `cancel_only`, 2 `post_only`; all kept, the status is a column). Kraken's `XBT` is BTC and `XDG` is DOGE | exact |
| Class (listed apart, not dropped) | `fiat`: AUD, EUR, GBP (3). `stablecoin`, `wrapped_or_staked`, `tokenized_commodity`: the coin is in CoinGecko's category `stablecoins` (33), `wrapped-tokens` or `liquid-staking-tokens` (0), `tokenized-gold` (2: PAXG, XAUT). `unclassified`: the symbol is not among CoinGecko's top 2,500 coins by market cap (102, many are small or new tokens; some may be stablecoins or wrapped tokens). `coin`: the rest (524). Stablecoins are not split USD or other: `price_last` is in the table. "Wrapped or staked" came out empty: WBTC, TBTC, METH, CMETH, JITOSOL, MSOL and LSETH are `unclassified` (not among CoinGecko's top 2,500 by symbol), so none is flagged; so far as the table goes they are counted as coins | CoinGecko's lists, symbol matched to the best-ranked coin |
| First trading day | the public `Trades` call, count 1, from the pair's first weekly OHLC candle: the day of the pair's first trade on Kraken. (First tried: the daily OHLC from the first week; Kraken returns only the last 720 days whatever `since` says, so it gave 2024-12-08 for every old coin; found by checking against our files, then replaced.) Checked on the 39 files we have: **38 of 39 first days equal our files'**; TAO's is 6 days earlier (2024-06-25 on Kraken, our file starts 2024-07-01) | 1 day |
| Traded value a day | close x volume of Kraken's daily OHLC candles (last 720 days), the median and the mean over the last 365 days and the last 90 days up to 2026-11-27; a day with no candle counts as 0 (Kraken writes no row for a day without a trade); a pair younger than the period is measured from its first day (`days_12m`, `days_3m` say how many days). Median trades a day: the candles' trade counts, the same way | exact on Kraken's candles |
| Spread | `Ticker`, (ask - bid) / mid, in %, one snapshot at read time | one instant: it moves |
| Perpetual | Kraken Futures `instruments` and `tickers`: a perpetual (`tag` = perpetual) quoted in USD whose base is the coin. Columns: its symbol, tradeable, opening date, 24 h volume in USD (`volumeQuote`), the median daily value of the last 90 days (close x volume of its daily candles; the volume is in coin units, checked: BTC 24 h volume x price equals `volumeQuote`), Kraken's own category | exact |
| Windows | the repository's own rules on the first day alone (holes ignored): a window of `research_2016.json` is used when it starts after the coin's first 90 days, and (for 395 or 790) when the coin's first day is on or before the first day the wrapper loads (`coins.warmup_start`). 32 windows, of which 14 from 2022 on (the check half) and 18 before | checked below |
| Category | the 39 coins we have, and coins.md's 32: coins.md's category. The others: CoinGecko's category lists, read through `coins/markets?category=`: payments = `payment-solutions`; platforms = `smart-contract-platform` or `layer-1`; privacy = `privacy-coins`; finance = `decentralized-finance-defi`; infrastructure = `infrastructure`, `oracle`, `storage` or `depin`; AI = `artificial-intelligence`; meme = `meme-token`. In exactly one: that category. In several: `ambiguous` (the matches are in `cg_our7_matches`; no guess). In none: `unknown`, with the other CoinGecko categories read in `cg_other_categories` (gaming, metaverse, NFT, exchange-based tokens, layer-2, interoperability, bitcoin layer-2). Not among CoinGecko's top 2,500: `unknown` | CoinGecko lists; the 7-way mapping is mine and is stated here |

**Checks of the table.** First days: 38 of 39 equal our files. Windows at 790 days, against `coins.md`'s table of 2026-11-27
(25 portfolio coins): 24 equal; XRP gives 14 here against 13 there, because the table counts from the first day only and
`coins.md`'s count also applies the hole rule (XRP's file has a hole). The 7 coins in `coins.md` not in the portfolio
(final group) are in the table too. All 39 files' coins are in the 664.

## Reading (counts; the operator decides the rule)
Below, "pairs" = the 664; "coins" = the 626 that are `coin` or `unclassified` (fiat, stablecoins and tokenized gold, 38 in
all, are listed apart and left out of the rule counts; 10 of them would pass the liquidity rule alone: AUD, EUR, GBP,
USDT, USDC, USDG, EURC, ZCHF, PAXG, XAUT). The 102 `unclassified` are kept in, not dropped; 2 of them pass
liquidity (KOR, LIGHTER).

**How many pairs in all: 664** (592 of the 626 coins are online).

**Each candidate rule alone (626 coins; in brackets all 664 pairs):**
| Rule | Pass |
|---|---|
| liquid: median daily value over 12 months at least 100,000 USD | **101** (111) |
| 3 years of history (first day on or before 2023-11-28) | **176** (184) |
| testable on at least 7 of the 14 check-half windows, 790-day warm-up | **98** (105) |
| the same, 395-day warm-up | **170** (177) |

**Together:**
| Rules | Pass |
|---|---|
| liquid + 3 years | **45** |
| liquid + 790 days (7 of 14) | **29** |
| liquid + 395 days (7 of 14) | **40** |
| liquid + 3 years + 790 days | **29** |
| liquid + 3 years + 395 days | **40** |
| 790 days alone but not liquid | 69 |

(All the coins that pass any of these are online. The 790-day rule includes the 3-year one in practice: 7 windows of the check half
need a first day around 2021 at the latest.)

**Of the 29 that pass at 790 days with liquidity: 25 are among the 39 we have and 4 are not: AKT, BAT, LUNA, MANA.**
**Of the 40 that pass at 395 days: 28 we have, 12 we do not: AKT, APT, ARB, BAT, CVX, FLR, ICP, JASMY, LUNA, MANA, QNT, XCN.**
Our 39 that do not pass at 790 days: COMP, ETC, FET, LDO, NEAR, OCEAN, ONDO, PEPE, SNX, STORJ, SUI, TAO, XTZ, YFI (14);
at 395 days: COMP, ETC, OCEAN, ONDO, PEPE, SNX, STORJ, SUI, TAO, XTZ, YFI (11).

**With a usable window before 2022** (windows of the explore half; the coin's first day plus 90 days and the warm-up before it):
among the 4 not-have passers at 790 days: **0**; among the 12 at 395 days: **1** (BAT; first day 2019-08-22).

**With a Kraken perpetual in USD:** 143 of the 664 pairs have one (all tradeable). Among the 626 coins: 137; among the 101
liquid coins: 73. Of the 40 passers at 395 days: 36 have one; of the 12 we do
not have: 8 (APT, ARB, BAT, CVX, ICP, JASMY, MANA, QNT); of the 4 at 790 days: 2 (BAT, MANA). AKT, LUNA, FLR, XCN have none. 52 other USD perpetuals exist for stocks, indices, metals and oil
(AAPLx, SPYx, XAU, WTIOIL...) with no spot pair here.

**By category** (626 coins; the 7, then what fits none):
| Category | All coins | Liquid | Passers at 395 days (40) | Of them, not in our 39 (12) |
|---|---|---|---|---|
| payments | 8 |  5 | 5 | 0 |
| platforms | 98 |  29 | 13 | 4 (APT, ARB, FLR, XCN) |
| privacy | 3 |  3 | 3 | 0 |
| finance | 106 |  20 | 6 | 1 (CVX) |
| infrastructure | 36 |  5 | 5 | 2 (JASMY, QNT) |
| AI | 37 |  5 | 1 | 0 |
| meme | 51 |  11 | 2 | 0 |
| ambiguous (in several of the 7 by CoinGecko) | 105 | 14 | 2 | 2 (AKT, ICP) |
| unknown (none of the 7, or not in CoinGecko's top 2,500) | 182 | 9 | 3 | 3 (BAT, LUNA, MANA) |

At 790 days: payments 5, platforms 8, finance 4, privacy 3, infrastructure 3, meme 2, ambiguous 1, unknown 3, AI 0;
the 4 not in our 39 are AKT (ambiguous), BAT, LUNA, MANA (unknown).

**Kinds of coins that fit none of the 7** (CoinGecko's other categories among the 626 coins; a coin may be in several,
and some are also in one of the 7): exchange-based tokens 47, NFT 39, gaming 36, layer-2 42, metaverse 14, bitcoin layer-2
5, interoperability 3. Among the 101 liquid coins: exchange tokens 8, layer-2 6 (ARB, MEGA, OP, POL, STRK, TON), NFT 3,
metaverse 2, gaming 1. Of the 182 `unknown`, 152 are not listed in any category read (102 of them because they are not
among CoinGecko's top 2,500). The 9 liquid `unknown`: BAT, BILL, KOR, LIGHTER, LUNA, MANA (gaming, metaverse, NFT), RIVER, SHX, WLFI.
The 14 liquid `ambiguous`: AI, AKT, EIGEN, GWEI, HYPE, ICP, KTA, PEARL, PYTH, RENDER, SEI, STRK, TON, ZBCN.

## Which of the expected outcomes happened
| Expected | Happened |
|---|---|
| several hundred pairs | 664, yes |
| liquid: a clear minority | 101 of 626 coins (16 %), yes |
| 3 years: roughly a third | 176 of 626 (28 %), close |
| 790 days: few | 98 coins, 29 of them liquid, yes |
| passers we do not have: some, fewer than 20 | 4 (790 days) or 12 (395 days), yes |
| a window before 2022: only the oldest | 0 (790) or 1 (395): BAT; yes |
| perpetual: large coins yes, small no | 73 of the 101 liquid coins have one; the liquid coins without one are mostly new (AERO, TON, SKY, XDC...) |

## What this does not say
- Spread is one snapshot; the traded values are Kraken's, in USD, close x volume (not VWAP); a day without a candle counts as 0.
- `first_day` is the first trade on Kraken, not the coin's age elsewhere; our own files for 38 of the 39 agree to the day.
- Window counts use the first day only: a hole in a file (XRP, XLM) lowers the real count (`coins.md`).
- The 102 `unclassified` and the `unknown` categories are a limit of CoinGecko's top-2,500 list, not a finding about the coins.
- Kraken's perpetual list is read today; its history of listings is not.
