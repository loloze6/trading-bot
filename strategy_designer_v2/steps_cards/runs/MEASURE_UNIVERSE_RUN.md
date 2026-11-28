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

## Method
(filled in with the results)
