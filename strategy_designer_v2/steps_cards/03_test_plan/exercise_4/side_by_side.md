# Exercise 4: side by side

Prompt: `system_prompt_used.md` (exercise 2 plus changes A to E); script with change F and the data's windows. `opus/`: the seven ideas. `opus_rerun/`: three ideas rerun after one line was added to the data block (warm-up bars are loaded before each window).

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2781 USD)

Forecast: Use a 14-bar Wilder RSI (RSIPullbackComponent, period 14), whose raw value is (50 - RSI) x 0.4. It is negative when RSI is above 50. Each bar, divide it by the mean absolute raw value of the previous 60 bars and multiply by 10 (standardise, window 60, min_periods 20, cap +/-20). Then clip it at a maximum of 0, so only readings above 50 count. Then apply signed_power with exponent 2 and pivot 10. Moderate readings shrink smoothly toward 0, and high readings grow quickly; for example, a standardised -5 becomes -2.5 and -15 becomes -22.5. The combined forecast is then clipped at -20. - When RSI is at or below 50 the forecast is exactly 0, and the position is flat. - When RSI is above 50 the forecast is negative, a short. Its size grows with the square of how far RSI sits above 50, measured against the coin's own recent RSI deviations. The largest shorts come at the high extremes. - The forecast is never positive. It is ungated: it runs on every bar.  
Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: Horizon is 5 bars. Use the "large" bars, where the recorded forecast is -10 or lower, and sample them non-overlapping: after a sampled bar, skip the next 4 bars. Pool these across all 3 coins and 6 windows. For each sampled bar, take the coin's 5-bar forward return minus that window's average 5-bar return (so the coin's own drift is not credited). The idea is confirmed if the mean of these excess returns is negative with t ≤ -2, and (supporting check) the mean is negative in at least 2 of the 3 coins.  
Reject: The idea is rejected if, on the same non-overlapping large bars, the mean 5-bar excess forward return is zero or positive. A mean with t ≥ +2 is also rejected, and points to continuation rather than reversal.  
Inconclusive: Three cases: the mean is negative but with -2 < t < 0; the pooled t is ≤ -2 but fewer than 2 of the 3 coins are negative; or fewer than 20 non-overlapping large bars exist across all coins and windows.  
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50". The short is held and sized only while RSI stays high, so it shrinks as RSI falls back, and part of any retrace that comes after RSI normalises is not held. - "Extreme" is not a fixed level such as 70. It is a deviation that is large relative to the coin's last 60 bars, softened by the squared power. - Low-RSI extremes, the mirror case, are not tested.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "rsi_high",
            "class": "strategies.strategy_components.RSIPullbackComponent",
            "params": {
              "period": 14,
              "long_only": false
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "clip",
                "params": {
                  "max": 0.0
                }
              },
              {
                "op": "signed_power",
                "params": {
                  "exponent": 2,
                  "pivot": 10
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

## 001-03_rsi-high-extreme-continuation

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

### opus (0.2690 USD)

Forecast: Take the 14-bar Wilder RSI of the coin's daily closes through RSIPullbackComponent (period 14, not long-only), whose raw value is (50 − RSI) × 0.4. Standardise it: divide it by the mean absolute value of its 60 previous readings (at least 20), times 10, capped at ±20. Then: - Negate it, so it is positive when RSI is above 50. - Clip it at a minimum of 0, so it is zero whenever RSI is at or below 50. The idea concerns only high readings and upward continuation. - Apply signed_power with exponent 2 and pivot 10. This is a graded dead zone: RSI just above 50 gives a near-zero position, and RSI far above its usual distance from 50 gives a large one. Forecast = 10 × (s/10)², where s = max(0, standardised (RSI − 50) distance). Examples: s = 5 gives 2.5, s = 10 gives 10, s ≥ 14.1 gives the 20 cap. The position is always long or flat, with no regime gating.  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: The horizon is 5 bars. Split each coin-window's active period into non-overlapping 5-bar blocks, so each forward return is counted once. Take the blocks that start on a bar with forecast ≥ 10 (high RSI). Pooled over all 18 coin-windows, their mean 5-bar forward return must exceed the mean 5-bar forward return of all blocks in the same coin-windows (the hold baseline) by at least +1.0 percentage point, with at least 30 such high-RSI blocks. The supporting check requires this excess to be positive for at least 2 of the 3 coins.  
Reject: The pooled excess forward return after high-RSI blocks is ≤ 0 over at least 30 such blocks, meaning no continuation or a reversal. The same result holds if the excess is positive pooled but negative for 2 or more of the 3 coins.  
Inconclusive: Any of the following: - The pooled excess lies between 0 and +1.0 percentage point. - There are fewer than 30 high-RSI blocks after warm-up. About 36 bars of each 122-bar window are lost to warm-up.  
Deviation: The config differs from the idea as written in three ways: - Event versus state: "after RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above 50 it is relative to its own recent typical distance". There is no fixed 70 threshold; the extreme is defined against the past 60 readings. - Graded position: mildly high readings carry small positions instead of none. - Neutral baseline: the comparison with "neutral readings" is made against all blocks, which equals holding the coin, rather than against RSI-near-50 blocks only.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "rsi_high",
            "class": "strategies.strategy_components.RSIPullbackComponent",
            "params": {
              "period": 14,
              "long_only": false
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "negate"
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              },
              {
                "op": "signed_power",
                "params": {
                  "exponent": 2
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

### opus_rerun (0.2660 USD)

Forecast: Use the 14-bar Wilder RSI on each coin's daily closes, through RSIPullbackComponent (period 14). Its raw value is (50 − RSI) × 0.4. The forecast is built in five steps: 1. Divide the raw value by the mean absolute value of its previous 60 values, times 10, capped at ±20 (standardise, window 60, min_periods 20). 2. Flip the sign, so the value is positive when RSI is above 50. 3. Clip at 0, so the forecast is zero whenever RSI is at or below 50. 4. Apply signed_power (exponent 2, pivot 10). A reading of about average strength stays at 10, moderate readings are damped smoothly towards 0, and readings above the recent average are amplified. The forecast is therefore: - zero at neutral or low RSI; - long only, and never negative; - continuous, growing with the square of how far RSI sits above 50 relative to its recent scale. The largest positions come at the highest RSI readings, with a combined clip at +20 (200 percent long).  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: Use a 5-bar horizon and the recorded raw indicator. A high extreme is RSI ≥ 70 (raw ≤ −8); a neutral reading is RSI 40–60 (raw between −4 and +4). Count non-overlapping 5-bar windows only: one sample per 5-bar block, with at least 30 extreme samples pooled. The idea is confirmed if the pooled mean 5-bar forward close-to-close return after extreme bars exceeds the mean after neutral bars with t ≥ 2. The difference must also be positive on at least 2 of the 3 coins. Supporting check: the strategy's pre-cost return beats holding the coin scaled by the strategy's average exposure.  
Reject: The idea is rejected if the pooled difference (extreme minus neutral) in 5-bar forward returns is zero or negative, or is negative on at least 2 of the 3 coins. A difference at t ≤ −2 would further point to reversal rather than continuation.  
Inconclusive: The result is inconclusive in three cases: - the difference is positive but t < 2; - fewer than 30 non-overlapping extreme samples are available; - the pooled difference is positive but only 1 of the 3 coins agrees. The result is also inconclusive if the main measure confirms but the supporting check fails.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, with position size growing steeply with how high it is". This changes four things: - Moderately high readings also hold small positions. - The holding time follows how long RSI stays high, not a fixed number of bars after the extreme. - The extreme threshold of 70 is used only in the criterion, not in the config. - Behaviour after low extremes is not tested.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "rsi_high",
            "class": "strategies.strategy_components.RSIPullbackComponent",
            "params": {
              "period": 14,
              "long_only": false
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "negate"
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              },
              {
                "op": "signed_power",
                "params": {
                  "exponent": 2
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus (0.2657 USD)

Forecast: One graded component, the spread between a 10-bar and a 30-bar simple moving average of the close: (SMA10 − SMA30) / SMA30 × 100. Each bar, this spread is divided by the mean absolute spread of the 60 bars before it and multiplied by 10, then capped at ±20. Negative values are cut to 0, so the forecast is long-only. - It is positive while the short average is above the long one, that is, after an upward cross and until the next downward cross. - It is near 0 just after the cross and grows as the short average pulls further above the long one; a spread equal to its recent average gives +10 (100 % long). - It is exactly 0 while the short average is below the long one. - It is active on every bar, with no regime. - Settings: 10/30 rather than the 50/200 convention, because each window holds only about 122 daily bars. 10/30 becomes ready near bar 51, leaving about 70 tradable bars per window.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: Horizon 5 bars, before costs, pooled over the 6 windows. Use only the bars where the forecast is ready, and sample every 5th of them so that 5-bar returns do not overlap. - Main measure: the forecast-weighted mean of BTC's next 5-bar return (sum of f×r over sum of f) minus the plain mean next 5-bar return over all sampled bars. The second term is the random-point and buy-and-hold baseline. - The idea is confirmed if this excess is positive with t ≥ 2.0 (non-overlapping samples) and positive in at least 4 of the 6 windows. - Supporting check: the share of positive next 5-bar returns on bars with forecast > 0 exceeds the share on all sampled bars.  
Reject: The idea is rejected in either of two cases: - The excess is ≤ 0 pooled, or positive in at most 2 of the 6 windows. - The excess is negative with t ≤ −2.0, meaning moves after upward crosses tend to reverse.  
Inconclusive: The excess is positive but has t < 2.0. Or it is positive pooled while positive in only 3 of the 6 windows. Neither confirms nor rejects the idea.  
Deviation: The idea says "after an upward cross." The config tests "while the short average is above the long one," sized by how far above it is. As a result: - Fresh crosses get small positions and mature, extended trends get the largest ones. - The position ends at the downward cross rather than after a fixed number of bars. - The 10/30 periods replace a longer conventional pair because the windows are short. - Downward crosses (the brief's short side) are not tested.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "sma_cross",
            "class": "strategies.strategy_components.EMASpreadComponent",
            "params": {
              "fast_period": 10,
              "slow_period": 30,
              "average": "sma"
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

### opus_rerun (0.2588 USD)

Forecast: Ungated and long only. Compute the spread between the 20-day and the 50-day simple moving average of the close: (SMA20 − SMA50) / SMA50 × 100. Standardise it against its own past 60 daily values, with min_periods 20: the latest spread divided by the mean absolute spread of the 60 bars before it, times 10, capped at ±20. Then clip it at 0. - The forecast is positive while SMA20 is above SMA50. - It grows with how far the short average has pulled above the long one: about +10 for a typical gap, up to +20. - It is zero while SMA20 is at or below SMA50, so a downward cross closes the position. - It is never negative.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: The main measure uses a horizon of 10 bars. On every 10th bar of each window (non-overlapping), take BTC's forward 10-bar close-to-close return. Average it over the bars where the forecast is above 0, and subtract the average over all sampled bars of the same window. - The idea is confirmed if this excess is positive in at least 4 of the windows that have active bars (at least 3 such windows are needed), and the pooled excess has t ≥ 2. - Supporting check: the strategy's return minus (its average allocation × the buy-and-hold return of the window) is positive when pooled over the windows.  
Reject: The idea is rejected if the pooled excess forward 10-bar return on active bars is ≤ 0. It is rejected outright, as moves that reverse after the cross, if that excess is negative with t ≤ −2.  
Inconclusive: Any of these neither confirms nor rejects the idea: - the pooled excess is positive but t < 2; - the excess is positive in fewer than 4 of the active windows; - fewer than 3 windows have any bar with a forecast above 0.  
Deviation: The idea says "after an upward cross"; the config tests "while SMA20 is above SMA50", sized by the gap between them. So the largest positions come well after the cross, once the averages have spread apart, not at the cross itself. The 20/50 periods are a convention I chose, because the source gives no lengths.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "sma_cross_spread",
            "class": "strategies.strategy_components.EMASpreadComponent",
            "params": {
              "fast_period": 20,
              "slow_period": 50,
              "average": "sma"
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

## 002-05_sma-up-regime-positive-drift

**The idea**

Idea: Over the stretch from an upward cross of the short average over the long average until the next downward cross, price rises more often and further than over random stretches of the same length.  
Consequence: The uptrend begun by an upward cross lasts until the opposite cross ends it.

### opus (0.2584 USD)

Forecast: The idea needs one indicator, the spread between a 20-day and a 50-day simple moving average of the close: (SMA20 − SMA50) / SMA50 × 100. Each average includes the current close. The spread is put on its own scale: it is divided by the mean absolute value of its previous 60 values and multiplied by 10, capped at ±20. Negative values are then clipped to 0. - Positive: on every bar where SMA20 is above SMA50, which is exactly the stretch from an upward cross to the next downward cross. The forecast grows continuously with how far the short average sits above the long one. - Zero: whenever SMA20 is at or below SMA50, because the idea makes no claim about the stretches after a downward cross. - Never negative.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: The horizon is 1 bar. Each daily close-to-close return of BTC is counted once. - Main measure: the mean next-bar return on bars where the forecast is above 0, minus the mean next-bar return on all ready bars of the same window. This "in-stretch excess" must be positive in at least 4 of the 6 windows. Pooled across windows, it must be positive with a Welch t-statistic of 2 or more. - Supporting check: the share of up days inside the stretches must exceed the share of up days on all ready bars, pooled.  
Reject: The idea is rejected if the pooled in-stretch excess is 0 or negative, or if it is positive in 2 or fewer of the 6 windows. It is rejected outright, as a reversal, if the pooled excess is negative with a t-statistic of −2 or lower. That would mean upward crosses mark exhaustion rather than the start of a trend.  
Inconclusive: Any of these neither confirms nor rejects the idea: - the pooled excess is positive but its t-statistic is below 2; - it is positive in exactly 3 of the 6 windows; - the main measure confirms but the up-day share does not.  
Deviation: The position size grows with the gap between the two averages instead of being a fixed long through the whole stretch. This weights the test toward bars where the short average is far above the long one, and early bars after a cross carry little size. The test compares in-stretch bars with all bars of the same window, not with random stretches of matched length. The averages include the current close, and the brief's other variant (price crossing the long average) is not tested. Warmup takes about 71 of each window's ~122 bars if no earlier history is supplied, so only about 50 bars per window may be scored.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "sma_cross_spread",
            "class": "strategies.strategy_components.EMASpreadComponent",
            "params": {
              "fast_period": 20,
              "slow_period": 50,
              "average": "sma"
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

### opus_rerun (0.2626 USD)

Forecast: The forecast is long-only and comes from one indicator: the spread between the 50-day and the 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100. This is the conventional daily cross pair; the source gives no periods. The spread is standardised against the mean absolute value of its own previous 200 stored values (target 10, cap 20). It is then clipped at 0. The forecast is positive on every bar where the short average sits above the long one, which is the whole stretch from an upward cross to the next downward cross. It is zero on every bar where the short average is below the long one. Within a stretch, the position grows continuously with how far the short average sits above the long one. It starts near 0 just after the upward cross and is capped at 20 when the spread is twice its usual size.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: The horizon is 1 bar: the coin's close-to-close return on the day after each bar, so returns do not overlap. Pool the 6 windows. The idea is confirmed if two things hold: - Main measure: the mean next-day return on bars with forecast > 0 exceeds the mean next-day return over all bars of the same windows (the buy-and-hold baseline), with a Welch t-statistic ≥ 2. - Supporting check: the share of up days on forecast > 0 bars is at least 3 percentage points above the share over all bars. Both must hold, with at least 100 pooled bars with forecast > 0.  
Reject: The idea is rejected if the pooled mean next-day return on forecast > 0 bars is at or below the all-bar mean. It is also rejected if the up-day share on those bars is at or below the all-bar share, since that would mean stretches after upward crosses rise no more often or no further than random days. It is rejected outright if the in-stretch mean is below the all-bar mean with a t-statistic ≤ −2, since that shows reversal or exhaustion.  
Inconclusive: The test is inconclusive in three cases: - The in-stretch mean is above the all-bar mean but the t-statistic is between 0 and 2. - The main measure and the supporting up-day share disagree. - Fewer than 100 pooled bars have forecast > 0, for example because the 50/200 pair stays crossed down through most windows.  
Deviation: The idea treats every bar of the stretch from the upward cross to the downward cross equally. The config does not: it sizes the position by the distance between the averages. Exposure is therefore small right after the cross and largest deep into the trend. The main measure is unweighted per bar, so it still tests the stretch as written. The source's periods are unknown, so the conventional 50/200 SMA pair is assumed. The brief's variant of price crossing the long average is not tested. Downward stretches are not traded.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "sma_cross_spread",
            "class": "strategies.strategy_components.EMASpreadComponent",
            "params": {
              "fast_period": 50,
              "slow_period": 200,
              "average": "sma"
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 200,
                  "min_periods": 50
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0.0
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

## 003-01_low-volume-up-move-reverts

**The idea**

Idea: A sharp upward move made on unusually low volume is followed by price falling back, giving up part of the rise.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against the stretched price, so it drifts back.

### opus (0.2773 USD)

Forecast: The forecast is active only on a day whose close is above the previous close and whose volume is below 75% of its 24-day average volume, where the average includes that day. On those days the forecast is negative: a short whose size grows with how sharp the day's rise was. The raw value is the day's close-to-close return in percent (PriceEvolutionComponent, period 1). It is standardised against its own previous 60 daily values (min_periods 20), so a typical absolute day sits near 10. The sign is then flipped. A signed power with exponent 2 and pivot 10 follows, so small rises give almost no short and sharp rises give a large one: a rise twice the typical size reaches the cap of -20. On every other day the forecast is 0 (flat). It is never positive. The minimum rebalance size is set to 0 so that small shorts are opened and every short is closed the next day.  
Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Horizon is 1 bar: the day after each event day, an event day being one where the forecast is below 0. The main measure is pooled over all event days in the 6 windows. For each event day, compute the position times the next day's coin return in excess of that window's mean daily return, which strips out the coin's own drift (the holding benchmark). Each event counts once, since the 1-bar horizons do not overlap. The idea is confirmed if this excess P&L has a positive mean with t ≥ 2 over at least 30 events. The supporting check is that the events in the top half by |forecast| have a more negative mean excess next-day coin return than the bottom half.  
Reject: The idea is rejected if the pooled mean excess P&L per event is zero or negative, meaning the coin does not fall, relative to its drift, on the day after low-volume up days.  
Inconclusive: Any of these neither confirms nor rejects the idea: a positive mean with t below 2, fewer than 30 events in total, or a positive mean where the larger shorts do not do better than the smaller ones.  
Deviation: "Followed by falling back" is tested as the next day's return only, with a one-day short held while the condition is true. "Sharp move" becomes the size of a single day's close-to-close rise, graded, rather than a multi-day surge. "Unusually low volume" becomes volume below 75% of a 24-day average that includes the same day, a fixed threshold that switches the position on and off. The brief's contrast with high-volume moves is not tested here.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "lowvol_up",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 24,
          "scaling_factor": 20.0
        }
      }
    ],
    "vetoes": [
      {
        "id": "lowvol_up",
        "transforms": [
          {
            "op": "identity"
          }
        ],
        "rules": [
          {
            "op": "lt",
            "value": -5.0
          }
        ],
        "consecutive_bars": 1,
        "result": "mean_reversion"
      }
    ],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "min_allocation_change": 0.0,
    "regimes": {
      "mean_reversion": {
        "components": [
          {
            "id": "rise",
            "class": "strategies.strategy_components.PriceEvolutionComponent",
            "params": {
              "period": 1
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
              },
              {
                "op": "negate"
              },
              {
                "op": "signed_power",
                "params": {
                  "exponent": 2
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "chop": null,
      "unknown": null
    }
  }
}
```

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.2225 USD)

Untestable: The idea forecasts altcoin returns from bitcoin's earlier move, so it needs another coin's prices. The config sees only one symbol's bars, and the only coin in the test is BTC/USDT, so there is no altcoin to trade. On BTC alone the config could only test bitcoin following its own past moves (self-momentum), which is not the lead-lag idea.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.2561 USD)

Untestable: The idea compares RSI now with RSI at the previous price high, a lower high in RSI against the last peak. No catalogue component or transform can give a lagged or peak-tracked RSI value: rules see only the latest raw value, and `standardise` must be the only history op. Any composition, such as "price near the top of its Donchian range while RSI is lowish", measures how slowly the climb went, not a divergence from the prior peak. So it cannot separate divergent new highs from non-divergent ones, which is the comparison the brief's falsification needs.  
