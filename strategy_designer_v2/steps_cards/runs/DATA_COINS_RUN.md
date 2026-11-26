# Data coins: the daily Kraken files of 20 more coins (2026-11-26, branch `data-coins`)

## Purpose and expected outcome
(As set by the designer's brief, 2026-11-26, before the run; this file was written after it.)

**Purpose:** give a coin card enough coins to group them by category (operator's go, 2026-11-26): the daily (1d)
Kraken USD history of BCH, XLM, DASH, ETC, XTZ, ATOM, ALGO, DOT, COMP, CRV, SNX, YFI, LDO, STORJ, FIL, GRT, OCEAN,
FET, SHIB and PEPE, made the same way as the 19 present files (Kraken's archive, then Kraken's public OHLC API).

**Expected:** 20 files `kraken_<COIN>USD_1d.csv` in the present files' 12 columns, each from the pair's first day on
Kraken to yesterday, with its coverage in `coverage.yaml`; the 19 present files unchanged; some odd coins (OCEAN,
merged into ASI in 2024, might have stopped).

## Result: 20 of 20 written

| Step | What was done | Result |
|---|---|---|
| Archive | Kraken's full OHLCVT archive (5 parts, 9,546,553,626 bytes, dated 2026-11-11): only the zip's directory and the 20 `<PAIR>USD_1440.csv` members were read, by byte ranges (curl, HTTP 206) over the parts read as one file; about 2 MB compressed, nothing else downloaded | 12,352 members listed; all 20 coins present under their usual names; each member's CRC32 checked on extraction (the parts' SHA256 sums need whole parts, so they were not checked) |
| Ingest | `tools/ingest_kraken_archive.py --resolution 1440 --assets <20 coins> --archive-dir <the extracted members>` | 20/20 ingested; archive's last day **2026-09-30** for every coin |
| Latest days | `tools/extend_kraken_daily.py --coins <20 coins>` (Kraken public OHLC API) | 56 days added to each (2026-10-01 to 2026-11-25); on the 664 days both sources have, prices equal for all 20 coins |
| Coverage | `coverage.yaml`: 2 entries per new file (archive: first day to 2026-09-30; API: 2026-10-01 to 2026-11-25) | 40 entries added; no existing line changed or removed |
| The 19 present files | sha256 before and after | **19/19 identical** |
| Not touched | `trading-bot/config/campaign_data_policy.yaml` (read by the ingest's own holdout guard, not changed); `local_data/holdout_sealed/` (not opened) | |
| Bot tests | `cd trading-bot && pytest -q` | 1677 passed, 16 skipped |

Size: 5.1 MB for the 20 files.

## Per coin
Missing day = a calendar day between the first and the last day with no row (Kraken writes no row for a day without a
trade). The last two columns flag rows worth a look, not errors: a day whose high is above 3x its close or whose low is
below a third of it (a wild print), and closes that moved more than 50% from the day before (first 3 dates shown).

| coin | first day | last day | days | missing days | holes | largest hole | zero-volume days | high > 3x close or low < close/3 | close-to-close moves > 50% |
|---|---|---|---|---|---|---|---|---|---|
| BCH | 2017-08-01 | 2026-11-25 | 3404 | 0 | 0 | none | 0 | 1 2017-08-01 | 6 2017-08-18 2018-12-20 2020-03-12 |
| XLM | 2017-01-17 | 2026-11-25 | 3419 | 181 | 4 | 177 (2017-08-23 to 2018-02-15) | 0 | 0  | 10 2017-04-02 2017-05-05 2017-05-06 |
| DASH | 2017-04-12 | 2026-11-25 | 3514 | 1 | 1 | 1 (2018-01-12) | 0 | 0  | 3 2020-03-12 2021-02-13 2021-05-19 |
| ETC | 2016-07-27 | 2026-11-25 | 3773 | 1 | 1 | 1 (2018-01-12) | 0 | 1 2018-01-13 | 2 2017-05-24 2020-03-12 |
| XTZ | 2018-10-16 | 2026-11-25 | 2963 | 0 | 0 | none | 0 | 1 2018-10-16 | 2 2020-03-12 2021-05-19 |
| ATOM | 2019-04-22 | 2026-11-25 | 2775 | 0 | 0 | none | 0 | 0  | 2 2020-03-12 2021-05-19 |
| ALGO | 2020-01-22 | 2026-11-25 | 2500 | 0 | 0 | none | 0 | 0  | 2 2020-03-12 2021-09-08 |
| DOT | 2020-08-18 | 2026-11-25 | 2291 | 0 | 0 | none | 0 | 2 2020-08-18 2021-02-22 | 1 2021-05-19 |
| COMP | 2020-07-15 | 2026-11-25 | 2325 | 0 | 0 | none | 0 | 0  | 0  |
| CRV | 2020-09-17 | 2026-11-25 | 2261 | 0 | 0 | none | 0 | 0  | 3 2020-10-27 2021-01-17 2021-05-19 |
| SNX | 2020-09-17 | 2026-11-25 | 2261 | 0 | 0 | none | 0 | 0  | 3 2021-05-19 2022-06-20 2025-10-12 |
| YFI | 2020-10-15 | 2026-11-25 | 2233 | 0 | 0 | none | 0 | 0  | 1 2021-05-19 |
| LDO | 2022-05-05 | 2026-11-25 | 1666 | 0 | 0 | none | 0 | 1 2025-10-10 | 0  |
| STORJ | 2020-07-15 | 2026-11-25 | 2325 | 0 | 0 | none | 0 | 1 2020-08-13 | 7 2021-03-23 2021-03-27 2021-05-19 |
| FIL | 2020-10-15 | 2026-11-25 | 2233 | 0 | 0 | none | 0 | 1 2025-10-10 | 4 2020-10-25 2021-02-09 2021-05-19 |
| GRT | 2020-12-18 | 2026-11-25 | 2169 | 0 | 0 | none | 0 | 0  | 7 2020-12-19 2020-12-20 2020-12-21 |
| OCEAN | 2021-03-03 | 2026-11-25 | 2094 | 0 | 0 | none | 0 | 1 2022-06-17 | 0  |
| FET | 2022-05-06 | 2026-11-25 | 1665 | 0 | 0 | none | 0 | 1 2022-05-06 | 2 2022-05-12 2025-11-07 |
| SHIB | 2021-11-30 | 2026-11-25 | 1822 | 0 | 0 | none | 0 | 0  | 1 2024-03-04 |
| PEPE | 2023-05-16 | 2026-11-25 | 1290 | 0 | 0 | none | 0 | 0  | 0  |

## What is odd
| What | Detail |
|---|---|
| **OCEAN did not stop** | Kraken kept the pair `OCEANUSD` after the 2024 merger into ASI: rows every day to 2026-11-25, no rename, no hole. But it is thin since: median daily USD volume 273k in 2024, 39k in 2025, 16k in 2026 (e.g. 2026-11-24: 6.5k USD, 125 trades). A card should treat its late years as a near-dead market. |
| FET | Under its own name throughout (Kraken did not rename it ASI). Tiny volume in 2022 (median 7k USD a day), deep from 2024. |
| XLM hole | 177 days without a row, 2017-08-23 to 2018-02-15, plus 3 short holes in Jan-Feb 2017. |
| DASH, ETC | 1 missing day each, the same day: 2018-01-12. |
| First-day prints | BCH 2017-08-01 opens at 600,000 (a fat-finger print on its listing day; close 350); XTZ, DOT, FET also flag on their first day. |
| Later wild lows | LDO and FIL on 2025-10-10 (the market-wide crash day), STORJ 2020-08-13, OCEAN 2022-06-17, ETC 2018-01-13, DOT 2021-02-22. Left as Kraken printed them. |
| End day | The new files end 2026-11-25; the 19 present files end 2026-11-17 (not extended here, by the brief). |
| Coverage start | The tools record the archive's first day as `start` (e.g. BCH '2017-08-01'); the 19 present files have `start: null` (recorded by hand from the file, 2026-11-18). Both mean the same thing for days with data; a backtest asking for days before a new coin's first row stops with "not fetched" instead of reading nothing. |
| **The archive edition changed** | A check, read only: the new archive's BTC daily file against our present `kraken_BTCUSD_1d.csv`, on their 4,730 common days. Prices differ on 8 days (in highs, e.g. 2013-11-07: 3484.09 in the new archive, 348.41 in ours; also 2013-11-10, 2013-11-12, 2017-12-17, 2019-07-14, 2020-07-04, 2020-07-07, 2020-07-21) and volume on 1,083 days (at most 4.5%). So Kraken rebuilt its archive; the 20 new coins come from this new edition, the 19 present files from the earlier one. Not acted on (the 19 stay unchanged). |

## Tools changed (shared code, on `data-coins` only)
| File | Change | Default behaviour |
|---|---|---|
| `trading-bot/tools/ingest_kraken_archive.py` | `--assets` (which coins) and `--archive-dir` (where the archive's files are) | unchanged: the 20-pair breadth set, `local_data/Kraken_batch/master_q4/` |
| `trading-bot/tools/extend_kraken_daily.py` | `--coins` (only these coins' files): without it the tool would also have extended the 19 present files | unchanged: every cached daily file |

Proof the default path is unchanged: `extend_kraken_daily.py --dry-run` with no `--coins` went through all 39 daily
files (the 19 would get 8 days each, 2026-11-18 to 2026-11-25; the 20 nothing) and every file in `local_data/` and
`coverage.yaml` kept its checksum. The ingest's default path could not be rerun here (no `master_q4/` in this container).

## Why this can't leak
Files only: no backtest, card or idea reads these 20 files yet. Each row is one finished UTC day (today's still-forming
bar is dropped by the API tool), and the engine hands each bar's decision the rows up to that bar. Every day written
(to 2026-11-25) is before the sealed holdout, which the ingest's guard checked against the policy file; no file under
`local_data/holdout_sealed/` was opened.
