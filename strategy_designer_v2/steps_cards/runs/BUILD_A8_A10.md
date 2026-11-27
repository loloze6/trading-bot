# Build A8, A10, A11: a run judged by what it adds; one holding bar; the return at a 20 % fall (2026-11-27)

Branch `build-a8-a10`, from `ccr-6624e33e-aakrpv`. The operator's go: "Go for next" (2026-11-27), next steps A8, A10, A11.

## Purpose (written before the build)
1. **A10:** the bar a portfolio must beat (holding its coins) is one number, whatever the order of its strategies.
2. **A11:** every version shows its yearly return at the risk the operator accepts (a worst fall of 20 %).
3. **A8:** a run or a batch is read by what it adds to the portfolio, with one command.

## Expected outcomes (written before the build)
| # | Outcome | How it is seen |
|---|---|---|
| 1 | Holding's Sharpe on v3 and v4 is the same in every order of the strategies | a test; v3 and v4 measured in three orders |
| 2 | v3 and v4 stay ready (the designer: v4 is above both 1.075 and 0.945) | measured again |
| 3 | The portfolio's own numbers do not move (Sharpe 1.914, yearly +21 %, worst fall 9.7 %) | measured again |
| 4 | v4's scale is about 2 and its yearly return at a 20 % fall roughly +40 % | measured |
| 5 | Nights 7 to 9 together: without them 87 candidates and 6 strategies, Sharpe 1.88 against 1.91, yearly +17 % against +21 % (the designer's check), or the difference explained | `addition.py` |
| 6 | Calling `addition.py` twice gives the same file | compared byte by byte |
| 7 | Both test suites pass | run |

## Files
| File | What changed |
|---|---|
| `orchestration/combine/card.md` | the three rules, written before the code: "Holding is one number" (A10), "The return at the risk the operator accepts" (A11), the section "What a run adds to the portfolio" (A8); output, calls, status |
| `runs/NIGHT_RULES.md` | morning step 3: the reading carries `addition.py`'s table; the count stays as information |
| `orchestration/combine/helper/update.py` | holding from the data files; `at_fall`; `select`; `measure_again` and `--measure-again`; the INDEX column |
| `orchestration/combine/helper/combine.py` | `per_coin` taken out of `portfolio` (same output) |
| `orchestration/combine/helper/addition.py` | new: A8's helper |
| `orchestration/combine/helper/test_update.py`, `test_addition.py` | 5 new tests and 2 new tests |
| `orchestration/combine/portfolios/INDEX.md` | the new column, v3's and v4's lines, the correction note |
| `orchestration/combine/portfolios/v3/`, `v4/` `measured_again.json` | new; `measures.json`, `portfolio.json`, `boxes.csv` untouched |
| `orchestration/combine/additions/` | `night7.md`, `night8.md`, `night9.md`, `nights7to9.md` |

Nothing in `trading-bot/`. `NEXT_STEPS.md` is not touched (the designer's).

### `update.py`'s measuring functions, for `build-a9` (every change named)
| Function | Name | What it returns | Change |
|---|---|---|---|
| `holding(weights, rows, records, data=None)` | kept | kept: the daily series | reads the data files; new optional `data` (the data folder; default `bx.DATA`); its values change (below) |
| `measure(weights, rows, records, data=None)` | kept | kept: `this version`, holding, `ready` | new optional `data`; `this version` gains `at_worst_fall_20pct` (`scale`, `yearly`); holding's dict gains `read_from`, `coin_days`, `coin_days_without_a_close_to_close` |
| `daily`, `related_on`, `cells`, `candidates`, `record_dir` | kept | kept | `related_on` reads each record once (same answers) |
| `build`, `update` | kept | kept | the selection moved into `select` (v3 and v4 selected again give the stored weights) |
| `index_line`, `HEADER` | kept | a line with **8** cells (was 7) | the new column before "Ready"; the final-test cell stays last |
| new | `coin_days`, `close_to_close`, `holding_coin_days`, `worst_fall`, `at_fall`, `select`, `measure_again`, `FALL`, `AT_FALL` | | |
| `combine.portfolio` | kept | kept | calls the new `combine.per_coin` |

## Proofs
### A10: one holding bar (v3 and v4 give the same figures: the same 11 strategies)
| | Before (`update.py` at `86c589c954`) | After |
|---|---|---|
| Holding's Sharpe, strategies in `portfolio.json`'s order | 0.945 | **1.058** |
| the reverse order | 1.075 | 1.058 |
| sorted by key | 1.075 | 1.058 |
| Holding's yearly, worst fall | +72.6 %, 91.2 % (or +54.0 %, 90.0 %) | +70.1 %, 91.7 % |
| The portfolio: Sharpe, yearly, worst fall | 1.914, +20.96 %, 9.7 % | the same |
| Ready | yes | yes |

- The fault reproduced: 1.075 or 0.945 by the order alone (the designer's two numbers; `update.py` built v4 in an order
  that gave 1.075, the stored order gives 0.945).
- **Why 1.058 and neither of the two.** Two causes, measured on v4's 55,782 coin-days:
  1. *Fewer days* (the fault named): in the stored order the first record holding 9 coins has fewer windows; holding
     lacked 10,500 coin-days (ATOM 725, BCH 724, DOT 724, GRT 724, FIL 605, CRV 605, ...).
  2. *Rounded closes* (found here): the chart files round a close to 6 decimals. For a coin priced far below 1 USD the
     return read from them is wrong (PEPE on 2026-08-30: the chart file goes from 0.000004 to 0.000003, a "fall" of 25 %; the data
     file goes from 0.000003657 to 0.000003411, a fall of 6.7 %). 3,838 coin-day returns differed by more than 0.000001 (DOGE 1,744, PEPE 962, TAO 304, ADA 294,
     BTC 240, ETH 158). On the old figure's own coin-days the data files give 1.058 where the chart closes gave 1.075
     (and 0.935 where they gave 0.945). The data files are the exact ones.
- 9 coin-days have no close-to-close in the data files (the previous day is missing): LTC 2016, five coins on one day
  of 2018, XRP 2022, BTC twice in 2024. Counted in `measures` (`coin_days_without_a_close_to_close`), not filled.
- The test: `test_holding_is_read_from_the_data_files_whatever_the_order_of_the_books` (a second record with one coin,
  400 days and other closes: the same series and the same measures in both orders).
- **Numbers of `portfolios/INDEX.md` that change:** in v3's and v4's lines, holding's Sharpe **1.075 becomes 1.058**;
  a new cell, "+47.9% (x 2.12)". Nothing else: version Sharpe 1.914, 129 and 131 candidates, 11 books, ready, final
  test not made. The note above the table says so. v3's and v4's `measures.json` still say 1.075 (as built); the new
  figures are in their `measured_again.json`.
- One figure differs in the last digit: worst fall 0.0970 in `measured_again.json`, 0.0969 in `measures.json`.
  `measure_again` uses the weights as stored, rounded to 4 decimals (0.1429 for 1/7); the build used 1/7.

### A11: the return at a worst fall of 20 %
| Version | Scale k | Yearly at that scale | As built |
|---|---|---|---|
| v3 | 2.12 | **+47.9 %** | +21.0 % a year, worst fall 9.7 % |
| v4 | 2.12 | **+47.9 %** | the same |

- Expected "about 2, roughly +40 %": the scale is as expected; the return is higher than twice 21 % because scaled
  returns compound (2.12 x 21 % is 44 %, compounding adds the rest). Before any cost of leverage.
- The method's assumption (the worst fall grows with k) checked on v4: 40 scales from 0.1 to 4, the fall rises at
  every step.
- Tests: ten days of +1 %, one of -5 %, ten of +1 % gives k = 4 exactly and the yearly return by hand; a target of
  10 % gives 2; a 50 % loss gives 0.4; a series that never falls gives none; a built version's scaled fall is 20 %,
  and `ready` is the Sharpe comparison alone.

### A8: what nights 7, 8 and 9 add (131 candidates with; all on the same 55,782 coin-days, 3,864 days)
| Batch | Candidates of it | Strategies: with, without | Sharpe: with, without | Yearly: with, without | Worst fall: with, without | At a 20 % fall: with, without | Entered, left |
|---|---|---|---|---|---|---|---|
| night 7 (with 7c) | 25 | 11, 9 | 1.91, 1.93 | +21.0 %, +19.6 % | 9.7 %, 8.3 % | +47.9 %, +53.5 % | 3, 1 |
| night 8 | 8 | 11, 11 | 1.91, 1.91 | +21.0 %, +20.8 % | 9.7 %, 9.7 % | +47.9 %, +47.6 % | 1, 1 |
| night 9 | 11 | 11, 10 | 1.91, 1.91 | +21.0 %, +20.4 % | 9.7 %, 9.5 % | +47.9 %, +47.6 % | 1, 0 |
| the three | 44 | 11, 6 | 1.91, 1.88 | +21.0 %, +16.9 % | 9.7 %, 8.3 % | +47.9 %, +46.5 % | 5, 0 |

- **The designer's check is reproduced:** without the three nights 87 candidates and 6 strategies, Sharpe 1.88 against
  1.91, yearly +17 % against +21 %. No difference to explain.
- What the table shows beyond it: at the same risk (a 20 % fall) the three nights add 1.4 points a year (+47.9 %
  against +46.5 %); the nights' strategies raise the yearly return and the fall together. Night 7 alone lowers the
  return at a 20 % fall (+47.9 % against +53.5 %). By year, the three nights help most in 2018 (+19.3 % against
  +1.5 %) and 2022 (+6.7 % against +2.0 %) and cost in 2024, 2025 and 2026 (2025: -1.7 % against +1.8 %).
- A "left" strategy is one the portfolio would hold without the batch (night 7's candidates displace one of night 8).
- **Twice, the same file:** `nights7to9.md` written, copied, written again by a second call: `cmp` says identical
  (sha256 `4dc4fe2f84...` both times).
- One call takes about a minute (131 records read).

### Tests
In a virtual environment with `trading-bot/requirements.txt` (pandas 2.3.3), on commit `897cb77612`:
- the cards' suite: **231 passed** (7 of them new); `topics/47_review/fold_rules_test.csv`, rewritten by it, restored;
- the bot's suite, from its folder: **1685 passed**, 16 skipped, 75 deselected.
v3 and v4 measured again in that environment give the same figures as above (first computed with pandas 3.0.5).

## The reading: which expected outcome happened
| # | Outcome | Happened |
|---|---|---|
| 1 | Holding the same in every order | yes: 1.058 in three orders, and a test |
| 2 | v3 and v4 stay ready | yes (1.914 against 1.058) |
| 3 | The portfolio's own numbers do not move | yes |
| 4 | Scale about 2, roughly +40 % | scale 2.12; +47.9 %, higher than the rough figure (compounding) |
| 5 | The designer's check reproduced | yes: 87 candidates, 6 strategies, 1.88 against 1.91, +16.9 % against +21.0 % |
| 6 | Twice, the same file | yes |
| 7 | Both suites pass | yes |

Not expected: the new holding figure is neither 1.075 nor 0.945, because the chart files' closes are rounded (above).

## Open (for the operator and the designer)
1. **The chart files round closes to 6 decimals** (`04_backtest/helper/chart_files.py`): wrong for coins priced far
   below 1 USD (PEPE, DOGE). Nothing in the rules reads those closes any more (holding was the reader); a chart drawn
   from them is still wrong for those coins. Not changed here (not asked): a topic for the operator.
2. **`final_test.py` (step 12) now reads holding from the data files too**, through `measure`: the same rule, on the
   final coins. Its tests pass; no final test has been made, so no record changes.
3. **`NEXT_STEPS.md`'s lines A8, A10 and A11** still say RUNNING: left to the designer (A10's line quotes 1.08 and 0.94;
   A11's "roughly +40 %" is +47.9 %).
4. **The night readings already written** (`NIGHT7_RUN.md` to `NIGHT9_RUN.md`) do not carry the table: the rule
   applies from the next reading; the three files are in `orchestration/combine/additions/` to quote.
5. **A8's table has no holding column** (not asked). Holding is step 11's bar for a version, not for a run.
6. The yearly figure of a calendar year not finished (2026: 241 days) is brought to a year, as step 6's formula does.
7. Not merged: branch `build-a8-a10` only.
