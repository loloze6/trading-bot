# Round 2: how the warm-up is set today, and whether it is too long (2026-11-20)

Asked by the operator (2026-11-20, relayed by the designer session): confirm how the warm-up is set, with numbers;
propose a change only if it is far too long. Measuring only: nothing in the repository changed.

## How it is set today: static, 2 x required_bars
- `core/launcher.py` (`warmup_prefetch`): before each window the engine feeds **2 x `strategy.required_bars`** bars,
  silently (no trade).
- `required_bars` (`strategies/main_strategy.py`) = the largest of: the regime detector's components' periods, the
  strategy's components' periods, 24 (the `stddev_24` column), and, when the plan sizes by volatility, the sizing
  window + 1.
- The strategy is ready once its history table holds `required_bars` rows and each component's history holds what
  its transforms ask for (a `standardise` op's `min_periods` + 1).

| Hourly plans (step 3, 88 configs) | Count |
|---|---|
| `required_bars` set by the 60-day sizing window (1,440 + 1 = 1,441): warm-up 2,882 bars, 120 days | **73** |
| set by the components | 15 (35 to 8,880 bars) |

The components' own need (their periods plus their history minimum) is 44 bars at least, 114 at the median, 9,001 at
most. On the three fixed inputs:
| Plan | Regime components | Strategy components | History minimum | Sizing | required_bars | Warm-up fed |
|---|---|---|---|---|---|---|
| grind | - | 93 | 21 | 1,440 | 1,441 | 2,882 |
| deep | 73 | 93 | 21 | 1,440 | 1,441 | 2,882 |
| evening | 960 | 145 | 121 | 1,440 | 1,441 | 2,882 |

## Is it too long? About 1.8 x what is held, not "far too long"
- Ready after about 1,441 bars; the history table keeps 1,541 (`required_bars` + 100). So about **1,300 of the 2,882
  bars** (about 54 days of hourly bars) are fed after the strategy already holds everything it keeps.
- They cost time: warm-up is half the bars processed (17,423 of 34,942 on fold A).

**Test** (scratch only): grind and evening, BTC fold A, warm-up of 1,600 bars instead of 2,882 (the engine fetches
from the start of the day, so a few more).
| | grind | evening |
|---|---|---|
| `bars.csv`, `trades.json`, `forecast_distribution.csv`, 6 windows | identical | identical |
| `metrics.json` | 5 of 6 identical; 1 differs: a 1-hour data hole that only the longer warm-up saw is counted in `data_quality` | the same |
| `manifest.json` | the data block differs (first bar, bar count, data hash), as expected | the same |

## What I propose (not built; the operator's go needed)
**A dynamic warm-up**: feed what the strategy holds rather than twice what it needs: the bars to be ready plus its
longest kept history (the history table, `required_bars` + 100, and each component's history). It would save about
1,300 bars per window: **about -20 % of an hourly backtest** (estimate), on top of A to D.

What it would change in the research:
- the manifest's data block and the data-quality count of every window (a gap seen during the warm-up);
- **possibly results:** a gap of the middle tier during the warm-up blocks new entries for `required_bars` bars after
  it, so a shorter warm-up can open trades the longer one blocked. And any state that grows with the whole history
  (for example, regime counters) could differ. Identical on these two plans and this fold; not shown in general.
- So it is a research change: a rule for "what the strategy holds" first (`common/backtest_record.md`), then a proof
  on every kind of plan.

Recommendation: **not now**. Do A to D first (identical files). Take the dynamic warm-up as its own decision
afterwards, if hourly backtests are still too slow.
