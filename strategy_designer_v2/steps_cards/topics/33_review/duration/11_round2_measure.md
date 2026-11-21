# Round 2, measurement: where an hourly backtest's time goes (2026-11-20)

Topic 33, brief `10_round2_brief.md`. Measuring only: nothing in the repository was changed. Branch
`engine-speed-round2`, from `ccr-6624e33e-aakrpv` at `41f5085c6` (engine with the holding period).

**How.** One coin (BTC) on fold A (6 windows), the wrapper called exactly as step 4 calls it
(`backtest/run_protocol.py ... --legacy-verdict-retired --trades-file-in-out-dir`, Kraken venue keys), on this
container (Linux, 4 cores, the run machine's kind; venv from `trading-bot/requirements.txt`: pandas 2.3.3,
numpy 2.5.1). Times are real seconds, from light timers put around the engine's functions by a scratch driver (no repo
change), checked against cProfile and against a plain run (grind: 69 s plain, 65 s timed). 0 USD, no model call.

**Fixed inputs** (step 3, `hold_ideas_1h_run/plans/`):
| Short name | Plan | What it computes per bar |
|---|---|---|
| grind | `016-03 ... d1_grinding-rises-keep-rising_1h` | 1 component (top gains' share of a 72-bar rise), always on, hold 72 |
| deep | `016-06 ... d1_deep-decline-fresh-drop-rebound_1h` | 3 price-change components (the most used class in hourly plans: 66 of 88 configs), hold 72 |
| evening | `016-03 ... d2_volatile-evening-fall-rebound_1h` | a regime detector (hour of day, volatility ratio over 720 bars) and a volatility-scaled fall (720 bars), hold 24 |

## 1. One coin, one fold (6 windows), seconds
| Part | grind | deep | evening |
|---|---|---|---|
| Python start and the bot's imports (once per call) | 1.7 | 1.9 | 2.2 |
| Reading the coin's data (6 windows) | 1.6 | 1.5 | 1.6 |
| **The bar loop** (34,942 bars) | **52.6** | **49.0** | **423.8** |
| - the one-bar frame handed to the strategy (`get_data_history`: a pandas table of 1 row, built per bar) | 9.3 | 8.9 | 13.9 |
| - reading the row and building the candle (`process_next_tick`, `add_row`) | 4.1 | 4.0 | 6.6 |
| - the strategy's history table: built from its columns | 5.3 | 5.0 | 6.5 |
| - the same table: its `stddev_24` column computed and inserted, every bar | 13.0 | 12.4 | 17.2 |
| - the regime detector's components | 0.0 | 0.9 | **163.2** |
| - the strategy's components | 4.2 | 0.8 | **193.6** |
| - other strategy glue (taking the last row as a dict, ...) | 2.7 | 2.7 | 3.6 |
| - forecast and transforms (`generate_signals`) | 3.2 | 3.3 | 2.4 |
| - sizing | 1.0 | 1.2 | 1.2 |
| - holding period (`core/holding_period.py`) | 0.1 | 0.1 | 0.1 |
| - risk layer | 0.3 | 0.3 | 0.4 |
| - execution (311, 544 and 313 trades) | 0.1 | 0.2 | 0.2 |
| - the bar's record (`record_state`) | 1.6 | 1.7 | 3.4 |
| - logging calls (debug level, written nowhere) | 1.5 | 1.6 | 2.7 |
| - other per-bar glue (reading close and time from frames, formatting debug messages) | 5.7 | 5.5 | 8.5 |
| End of each window: metrics and files (6 windows) | 4.2 | 4.7 | 4.4 |
| End of the call: the wrapper's episode bootstrap | 4.0 | **16.1** | 0.3 |
| **Total** | **64.9** | **74.0** | **433.3** |

The evening runs shared the machine with one other backtest (4 cores, 2 busy), so its seconds may be a little high.

## 2. One coin, folds A to D (24 windows): deep
| Part | Seconds | Share |
|---|---|---|
| Bar loop (139,661 bars) | 190 | 62 % |
| **Episode bootstrap, at the end of the call** | **87** | **28 %** |
| End of each window (24) | 19 | 6 % |
| Data reading, start-up | 8 | 3 % |
| **Total** | **307** | |

## 3. What a whole idea costs (6 coins x folds A to D, 4 cores)
Step 4 runs one call per coin, 4 coins at once: 6 coins make **two waves**, the second using 2 of the 4 cores. So an
idea takes about 2 x one coin's time.
- deep: 2 x 307 s = about 10 min. Recorded on 2026-11-19 (`runs/D_LINE_1H_RUN.md`): 606 to 688 s. It matches.
- evening: one coin is about 4 x 433 s = 29 min (estimate: 4 folds); an idea about 58 min. Recorded: over 53 min.

## Findings
| # | Finding | Measured | Why |
|---|---|---|---|
| M1 | **Two volatility components recompute 720 standard deviations on every bar.** They are 82 % of the evening book's time | 357 s of 433; 42 million `np.std` calls for 6 windows | `VolatilityRatioToAverageComponent` and `VolatilityScaledReturnComponent` (with `vol_lookback` 720) take the mean of the last 720 rolling stds; each bar recomputes all 720, though 719 are the previous bar's. 7 of 88 hourly plans use `vol_lookback` 720 or 2400: these are the 30 to 60 min books. Two other components have the same loop (`VolatilityRankedFallComponent`, `RankWeightedScaledMoveComponent`); no hourly plan uses them yet |
| M2 | **The episode bootstrap at the end of each call is computed and thrown away.** | 87 s of 307 per coin (deep, 24 windows); 4 s (grind) to 16 s (deep) per 6 windows; grows with the active bars | `run_protocol.py` builds the "extended summary" for the prescreen cross-check. On step 4's path there is no prescreen file, so the cross-check is `null`; of the bootstrap only its **method label** is written (`episode_blocked_significance_by_symbol`), and the label is decided before the 2,001 resamples run (`episode_significance.compute_a851a_significance`). Its numbers are also unseeded: they would differ between two runs |
| M3 | **The coins run in two waves on 4 cores** | about a quarter of step 4's core time idle | 6 coins, one call each, 4 at a time: the last 2 coins run alone on 2 cores |
| M4 | **Per-bar pandas glue** is most of a light book's time: building small tables to read one value | grind: one-bar frame 9.3 s, `stddev_24` column 13.0 s, row reading 4.1 s, debug formatting and other glue about 7 s: about 34 s of 65 | The engine hands each bar around as a 1-row pandas table; the strategy's 1,541-row history table gets a 24-bar rolling std column inserted on every bar (read only at its last row, and only by `vol_normalize` transforms and older components) |
| M5 | **Half of the bars processed are warm-up** | 17,423 of 34,942 | each window first replays 2 x `required_bars` (2 x 1,441, driven by the 60-day sizing window) before its about 2,900 bars. Required by `common/backtest_record.md` (the strategy ready on every recorded bar): a research matter, not a speed one |
| M6 | Small items | | end-of-window outputs 4 to 5 s per 6 windows (6 to 7 %), of which the Excel exports step 4 deletes about 1 s; components themselves (grind 4.2 s, deep 0.8 s) are cheap |

## Prototypes (scratch only, to measure the gain before proposing; nothing in the repo)
| Prototype | Book | Before | After | Files (bars, trades, metrics, forecast distribution, manifest) |
|---|---|---|---|---|
| M1: each volatility component keeps the previous bar's 720 stds and computes only the new one when its closes are the previous bar's shifted by one bar (each std still `np.std` on the same values; the mean still `np.mean` of the same list, same order) | evening, BTC fold A | 433 s | **63 s (7x)** | 30 of 30 identical |
| M4 (two parts): the backtest rows read from arrays taken once per window; the history table built with its `stddev_24` column in one construction | grind, BTC fold A | 64.9 s | **55.0 s (-15 %)** | 30 of 30 identical; a second run in check mode compared every frame with today's on every bar: all equal |
| M4, third part: the one-bar frame from typed arrays instead of a list of dicts | micro-benchmark | 0.194 ms per bar | 0.078 ms | the same frame (values, types, column order); about -4 s per 6 windows |
| M2: not prototyped: the code path shows the numbers are never written | | | | to be proven by a rerun |

## What I do not know
- How the 6 coins differ in time on the run machine (I measured BTC; the fold-split gain in the plan assumes similar coins).
- The bootstrap's cost on the other plans over 24 windows (measured: deep 87 s; it depends on the active bars).
- Whether a deeper rewrite of the per-bar glue (no 1-row tables at all) is worth its risk: not measured.
