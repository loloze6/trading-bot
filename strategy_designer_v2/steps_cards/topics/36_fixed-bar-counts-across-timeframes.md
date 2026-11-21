# Topic 36: settings counted in bars, carried from daily to finer timeframes

Status: open  
Where: research: step 3 (`03_test_plan/helper/reference/strategy_config_guide.md`, its prompt), the engine's defaults
(shared code) if any is changed  
Opened: 2026-11-20, the operator: "maybe the position's volatility comes from the length of the sizing's standard
deviation, not adapted from 1d to finer; extend the reflection to every fixed setting that enters the position."

## Question
Which fixed settings that shape a position are counted in bars, and so mean a different span of time on hourly bars
than on daily bars? Should each be stated in time, so an idea is sized and scaled the same way on any timeframe?

## Seen
2026-11-20, from the night's configs and bar files.

| Setting | Counted in | Daily bars | Hourly bars | Adapted today? |
|---|---|---|---|---|
| Sizing volatility window (`sizing.window`) | bars, chosen in time | 60 bars = 60 days | 1,440 bars = 60 days | yes |
| `sizing.periods_per_year` | bars per year | 365 | 8,760 | yes |
| `standardise` window: the forecast scaled against its own past (guide: "the larger of 60 and the component's longest lookback, at most 500") | bars | 60 to 500 days | **60 to 500 hours = 2.5 to 21 days** | no |
| `standardise` minimum history `min_periods` (guide: "a quarter of the window, 20 to 120") | bars | 20 to 120 days | **20 hours to 5 days** | no |
| Component lookbacks ("the return over 72 bars") | bars | from the idea's text | from the idea's text, usually in hours | per idea |
| Regime detector windows (guide's example: VarianceRatio k 5, window 100) | bars | 100 days | 100 hours, about 4 days | not checked |
| Smallest trade (`min_allocation_change`, 0.2) | units of position | 1 chance a day | 24 chances a day | not a span of time; its effect grows with the number of bars |

The sizing is not the cause. On three hourly books (grinding-rises, settlement-move, volatile-regime reversal), 0.0 to
0.2 % of the target position's movement happens on bars where the forecast did not change. The forecast itself
changes on 10 % to 89 % of hourly bars. Night configs: the volatile-regime reversal standardises over 500 bars (about
21 days), grinding-rises over 72 bars (3 days).

## Why it matters
`standardise` sets the forecast's scale by comparing it with its own recent past. On hourly bars that past is a few
days, so the scale resets with each few days of market, and the forecast, the position and the trades move more than
the same idea would on daily bars. One rule should mean the same span of time on every timeframe.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Keep the rules in bars | nothing to change | an hourly idea's forecast is scaled on 2.5 to 21 days, a daily one on months to a year |
| B. State the `standardise` rule in time (the same span as on daily bars: e.g. 60 to 500 days, converted to bars by the timeframe), in step 3's guide | one rule for every timeframe; no shared code changed | long windows on hourly bars (up to 12,000 bars) need that much history before the strategy is ready; to check against the data and the windows |
| C. B, and review each other bar-counted setting in the list (regime windows, `min_periods`, the smallest trade's effect) | complete | more to test |

Recommended: B first, tested by rerunning a few hourly books with the window in time and comparing them file by file
with the same books today. Then C, setting by setting, only where a run shows an effect.

**2026-11-20, pilot book 1 (grinding-rises) and a replay.** The pilot's real backtest (window 1,440 bars, 60 days):
the forecast changes on 6.4 % of bars instead of 9.9 %, but Sharpe 0.877 (0.875 at 72 bars), Calmar 0.634 (0.645). A
replay from the recorded raw values (`36_review/book_sim.py`): the forecast is exact on every bar, and the whole book
is within 0.06 of Sharpe and 10 % of units of the record. Scanning the window from 3 days to 1 year gives Sharpe 0.88 to
0.95 and Calmar 0.60 to 0.67: flat. For this book the window is not the lever. Its forecast is 0 on 84 % of bars, and
73 % of its gain is the market's. The replay is exact only for a component computed on every bar: a regime-gated one
(volatile evening-fall, deep-decline) is not recorded on its inactive bars, so its history cannot be rebuilt from the
record (55 % of active bars match).

**2026-11-20, the pilot, 4 books (`runs/HOLD2_AND_PILOT_RUN.md`).** With the window at 60 days: Sharpe +0.00 to +0.07,
Calmar −0.01 to +0.06, 0 of 4 pass step 6; within what the corrected holding rule alone explains. The forecast changes
less often only on grinding-rises (9.9 → 6.4 % of bars); on the others its changes come from the components themselves
(31 to 45 % of bars) or it is almost always 0 (99 %). The window is not the lever.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
Pilot read (2026-11-20): the window is not the lever. Open for the operator: state the window in time anyway (one
rule for every timeframe), or leave it. Next, if wanted: the other bar-counted settings (C), only where a run shows an
effect.

## Links
Topic 34 (the book's diagnosis), topic 30 (why hourly ideas rarely pay), `common/forecast.md`,
`03_test_plan/helper/reference/strategy_config_guide.md` (standardise, vol_target, sizing).
