# Exercise 5: side by side

Prompt: `system_prompt_used.md` (exercise 4 plus one line on settings). Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2765 USD)

Forecast: Use the 14-bar Wilder RSI on the daily close. Take 50 minus RSI, so the value is negative when RSI is above 50. Divide it by the mean absolute value of its own previous 60 readings and multiply by 10, capped at ±20 (standardise). Keep only the negative side, which covers readings above 50, so the forecast is zero whenever RSI is at or below 50. Then apply signed_power (exponent 2, pivot 10) so the short grows with the square of the reading's strength: a mild reading of -5 becomes -2.5, an average one of -10 stays -10, and an extreme one of -14 or beyond reaches the -20 cap. The forecast is never positive. It is zero when RSI ≤ 50 and grows more negative, smoothly, the further RSI sits above 50 relative to its recent typical distance from 50, so the largest shorts occur at the highest RSI extremes.  
Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: Horizon is 5 bars. Take the bars where the forecast sits at the -20 cap and keep only those at least 5 bars apart, so each 5-bar window is counted once. The coin's 5-bar forward close-to-close return after those bars must be lower than its average 5-bar return over all bars of the same windows, which is the buy-and-hold drift. Pooled over BTC, ETH and BNB and all 6 windows, with at least 30 such observations, this excess must be negative with t ≤ -2, and it must be negative for at least 2 of the 3 coins. Supporting check: the mean excess after forecasts between -2 and -10 is less negative than after -20, so the retracement grows with the reading.  
Reject: With at least 30 independent observations, the pooled excess 5-bar return after -20 forecasts is ≥ 0, meaning price keeps rising or matches its drift after high RSI extremes. The same holds if it is negative for fewer than 2 of the 3 coins with pooled t > -1.  
Inconclusive: Any of the following: the pooled excess is negative with t between -2 and -1; fewer than 30 independent observations at -20; or the pooled t ≤ -2 but only one coin shows a negative excess.  
Deviation: Four differences from the idea. (1) "After the RSI reaches a high extreme" becomes "while RSI is above 50", with the short sized by how far above. (2) "Extreme" is measured against RSI's own recent 60-bar typical distance from 50, not a fixed level such as 70, and it is judged at the -20 cap. (3) Mild above-50 readings carry small short positions instead of none. (4) Low (oversold) extremes are not tested.  

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

## 001-03_rsi-high-extreme-continuation

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

### opus (0.2630 USD)

Forecast: Take the 14-bar Wilder RSI of the close on daily bars and measure how far it sits above 50 (RSI − 50). Put that distance on the scale of its own recent past by dividing by the mean absolute RSI deviation over the previous 60 bars, times 10, capped at ±20. Keep only the upper side: the forecast is zero whenever RSI is at or below 50. Then square it with a pivot of 20 (20 × (x/20)²), so the forecast stays graded but is damped hard near neutral and grows quickly toward strong readings. A typical deviation of 10 gives a forecast of 5; the cap of 20 (200% long) is reached at about twice the typical deviation, roughly RSI ≥ 70. The forecast is positive and grows with how extreme the high RSI is, near zero for neutral readings, and never negative.  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: The horizon is 5 bars. Pool all 3 coins × 6 windows. Count only non-overlapping samples: a bar enters only if no earlier sampled bar of the same group lies within 5 bars. Confirmation requires both of the following: - The mean 5-bar forward close-to-close return after bars with forecast ≥ 10 (strong high-RSI readings) exceeds the mean 5-bar forward return after bars with forecast < 2 (neutral or low readings). The difference must be positive with a t-statistic ≥ 2 and positive in at least 2 of the 3 coins. - Supporting check: the strategy's total return before costs exceeds its average exposure times the coin's buy-and-hold return over the same windows.  
Reject: The pooled difference (high-forecast minus neutral 5-bar forward return, non-overlapping) is zero or negative. Alternatively, it is negative in at least 2 of the 3 coins with the strategy failing to beat exposure-matched buy-and-hold.  
Inconclusive: A positive pooled difference with a t-statistic below 2. Also inconclusive: a positive pooled difference with only 1 of 3 coins positive, or fewer than 30 non-overlapping high-forecast samples in total.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above". The position grows smoothly toward extremes rather than firing at a fixed threshold such as 70. Readings below 50 (low extremes) are not tested and are held flat.  

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
              "period": 14
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
                  "exponent": 2,
                  "pivot": 20
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

### opus (0.2629 USD)

Forecast: Use one indicator, the spread between the 50-day and 200-day simple moving averages of the close: (SMA50 − SMA200) / SMA200 × 100. These are the conventional daily golden-cross settings, since neither the brief nor the source gives periods. The spread is standardised against its own previous 200 values (current spread × 10 / mean absolute spread of the past 200 bars, capped at ±20). It is then clipped at 0 from below. - When it is positive: whenever SMA50 is above SMA200, that is, after an upward cross that has not yet been undone. It grows continuously as SMA50 pulls further above SMA200. An average-sized spread gives +10, or 100% long. - When it is zero: whenever SMA50 is at or below SMA200, or before warm-up is complete. - When it is negative: never. The idea concerns only the upward cross.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: Use a horizon of 20 bars. In each window, sample bars 0, 20, 40, 60, 80 and 100, so the 20-bar forward returns do not overlap. That gives about 36 samples across the 6 windows. The idea is confirmed if two things hold, judged before costs: - Main measure: on samples where the forecast is above 0, the mean 20-bar forward log return of BTC exceeds the mean over all samples (that is, simply holding the coin) by a positive amount, with a t-statistic of at least 2. - Supporting check: the share of positive forward returns on those samples is higher than the share over all samples.  
Reject: The idea is rejected if either of these holds: - The excess mean forward return on samples with a positive forecast is zero or negative, with at least 8 such samples. - That excess is negative with a t-statistic of −2 or below, which would show reversal after crosses.  
Inconclusive: The result is inconclusive in any of these cases: - Fewer than 8 samples have a positive forecast. - The excess is positive but its t-statistic is below 2. - The excess comes entirely from a single window. - The excess is positive but the supporting hit-rate check fails.  
Deviation: The idea says "after an upward cross"; the config tests "while SMA50 is above SMA200". The position is sized by how far apart the averages are, not by how recent the cross is. So the position is smallest right after the cross and largest later in the trend. The periods 50/200 are a convention, not taken from the source.  

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

## 002-05_sma-up-regime-positive-drift

**The idea**

Idea: Over the stretch from an upward cross of the short average over the long average until the next downward cross, price rises more often and further than over random stretches of the same length.  
Consequence: The uptrend begun by an upward cross lasts until the opposite cross ends it.

### opus (0.2577 USD)

Forecast: Take the 50-day simple moving average and the 200-day simple moving average of the daily close, with the current close included in both. The raw signal is their percent spread, (SMA50 − SMA200) / SMA200 × 100. It is positive from an upward cross until the next downward cross, and negative otherwise. The spread is divided by the mean absolute value of its own previous 200 values and multiplied by 10, capped at 20. That makes it about 10 on a typical stretch and larger when the short average is further above the long one. It is then clipped at 0. The forecast is therefore positive and grows with the spread for the whole stretch from an up-cross to the next down-cross. It is exactly 0 while SMA50 is below SMA200 and never negative. The position is long, sized by how far the short average sits above the long one, and flat outside the up-cross stretches.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: The horizon is 1 bar: the next day's close-to-close BTC log return, so each return is counted once. Pool all six windows. The main measure is the mean next-day return on bars where the forecast is > 0 minus the mean next-day return on all bars, which is the buy-and-hold baseline. The idea is confirmed if this difference is > 0 with a t-statistic ≥ 2.0 and there are at least 60 in-stretch bars. The supporting check is that the share of up days inside the stretches exceeds the share over all bars.  
Reject: The idea is rejected if the pooled difference is ≤ 0, or if it is negative with a t-statistic ≤ −2.0, which would mean the stretches after up-crosses underperform or reverse. It is also rejected if the in-stretch up-day share is no higher than the all-bar share.  
Inconclusive: These results neither confirm nor reject the idea: a positive difference with a t-statistic between 0 and 2.0, or fewer than 60 in-stretch bars across the six windows. With 50/200 averages on 122-bar windows, some windows may contain no up-cross stretch at all.  
Deviation: The idea is about the stretch between crosses, which is a binary state. The config instead sizes the long position by the size of the SMA50–SMA200 spread rather than holding a constant position throughout the stretch. The main measure still judges the stretch as a whole, so the sizing affects the portfolio's value but not the criterion. The down-cross stretches are left flat rather than shorted, because the idea as stated concerns only the up-cross stretches.  

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

### opus (0.2724 USD)

Forecast: Only on a day whose close is above the previous close and whose volume is below its 20-day average volume (the average includes that day), the forecast is a short position sized by that day's percent rise. The rise is close-to-close over 1 bar. It is divided by the mean absolute 1-day move of the 60 bars before it and multiplied by 10. The result is passed through a signed power with exponent 2 and pivot 10, so small rises give a near-zero short and sharp rises give a large short. It is then negated, giving a forecast between 0 and −20 (an average-sized rise gives about −10, half an average rise about −2.5, 1.4 times an average rise about −20). On every other day (down days, flat days, up days on volume at or above the 20-day average) the forecast is 0. The forecast is never positive.  
Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Horizon 1 bar. Take the bars where the forecast is non-zero, pooled over the 6 windows; each event is one non-overlapping next-day return. On those bars, the mean next-day close-to-close return minus the mean next-day return of all window bars must be negative with a t-statistic at or below −2.0, on at least 50 events. Supporting check: the third of events with the largest |forecast| must have a more negative mean excess next-day return than the smallest third.  
Reject: Over the same pooled events, the mean excess next-day return is zero or positive, so low-volume up days are followed by price holding or rising at least as much as an ordinary day.  
Inconclusive: An excess mean that is negative but has a t-statistic between −2.0 and 0, or fewer than 50 qualifying events. Also a negative excess mean whose size does not grow with |forecast| (the supporting check fails).  
Deviation: "Unusually low volume" becomes "volume below its 20-day average" (about half of up days qualify), and "sharp" is a graded damping (signed power) rather than a threshold. "Followed by price falling back" is tested only over the single next day, because the short exists only while the qualifying day is the latest bar. The position is not sized by how thin the volume is, because the only volume component is on/off and can only serve as the regime condition. The high-volume half of the brief is not tested here.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "thin_up",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 20
        }
      }
    ],
    "vetoes": [],
    "rules": [
      {
        "regime": "mean_reversion",
        "any_of": [
          [
            {
              "id": "thin_up",
              "op": "lt",
              "value": 0.0
            }
          ]
        ]
      }
    ],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "mean_reversion": {
        "components": [
          {
            "id": "day_move",
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
                "op": "signed_power",
                "params": {
                  "exponent": 2
                }
              },
              {
                "op": "negate"
              }
            ]
          }
        ]
      },
      "trending": null,
      "unknown": null,
      "chop": null
    }
  }
}
```

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.2212 USD)

Untestable: The idea forecasts altcoin returns from bitcoin's earlier move, but the test runs only on BTC/USDT, and each config sees only one coin's bars, so it cannot trade an altcoin on a bitcoin signal. No catalogue component reads another coin's prices: the guide names "another coin's prices" as a genuine gap.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.2446 USD)

Untestable: The idea needs RSI at the previous price high, compared with RSI at the current new high. No catalogue component finds swing highs or stores an indicator's value at an earlier peak, and `standardise` only compares against the average of past values, not the last peak. The nearest proxies do not measure divergence. A "price at the top of its range" regime with a graded RSI component can only size by RSI's absolute level, and an offset to centre it would put a constant inside a regime, which is not allowed. An ungated "range position minus RSI" spread measures range versus short-term momentum on every bar, which is a different idea.  
