# Exercise 10: side by side

Prompt: `system_prompt_used.md`; the final helper (references in the system prompt, plan ids with the bar size). Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0521 USD)

Forecast: Take the 14-bar Wilder RSI on daily closes and form (50 − RSI). Standardise it: divide by the mean absolute value of its previous 60 daily readings and multiply by 10, capped at ±20. Clip at a maximum of 0, so only the overbought side (RSI above 50) trades. Then apply signed_power with exponent 2 and pivot 10. Readings near RSI 50 shrink smoothly towards 0, and high readings grow (standardised −15 becomes −22.5, and the combined forecast is clipped at −20). The forecast is never positive. It is zero whenever RSI is at or below 50 and negative (short) whenever RSI is above 50. It grows in size with the square of how far RSI sits above 50 compared with its recent typical distance, so the largest shorts sit at the highest RSI readings.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Confirm: The horizon is 5 bars. Take the bars where the forecast is −10 or lower (the strongest overbought readings), keeping only one per 5-bar block so that overlapping returns are counted once, and pool all coins and windows. Over those bars, the mean forward 5-bar close-to-close return, minus the mean forward 5-bar return over all bars of the same coin and window, is −1% or lower, from at least 30 such observations. The excess has the same sign in at least 2 of the 3 coins. Supporting check: the short-only strategy's pre-cost return, summed over all windows and coins, is positive.  
Reject: With at least 30 non-overlapping observations, the pooled excess forward 5-bar return after forecast ≤ −10 is 0 or higher. That means price after high RSI does as well as or better than average. An excess of +1% or more would point to continuation instead.  
Inconclusive: The pooled excess lies between −1% and 0. Or there are fewer than 30 non-overlapping strong-forecast observations. Or the excess is −1% or lower pooled, but the coins disagree in sign.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by the square of how far above". No fixed extreme threshold is used. Mildly overbought bars also carry small short positions, and the position stays on for as long as RSI stays high instead of over a fixed number of bars after the extreme. The oversold side of the brief is not tested.  

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
            "id": "rsi_overbought",
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

### opus (0.0520 USD)

Forecast: Compute the 14-bar Wilder RSI on daily closes. The raw component value is (50 − RSI) × 0.4. Standardise it against the mean absolute value of its previous 60 values (target 10, cap 20). Negate it, so the reading is positive when RSI is above 50. Clip it at 0, so the forecast is zero whenever RSI ≤ 50. Then apply signed_power with exponent 2 and pivot 10: a mild reading is damped smoothly towards 0 and a strong one is amplified. The result is a long-only forecast. It is zero at or below RSI 50 and grows continuously as RSI rises above its usual distance from 50. The largest positions come at the highest RSI extremes, and the combined forecast is capped at +20.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Confirm: Horizon is 5 bars. Take non-overlapping 5-bar blocks, sampling every 5th bar, so overlapping returns are counted once. Pool the three coins and six windows. The main measure is the coin's mean forward 5-bar return after "extreme" bars minus its mean after "neutral" bars: - "Extreme" bars are those whose forecast is in the top 20% of that coin's bars. - "Neutral" bars are those where the recorded raw indicator has |value| ≤ 4, which means RSI is between 40 and 60. The idea is confirmed if this difference is positive with a t-statistic ≥ 2 and is positive for at least 2 of the 3 coins. The supporting check is that the Spearman correlation between the forecast and the forward 5-bar return, on bars with forecast > 0, is positive. All of this is judged before costs.  
Reject: The idea is rejected if the pooled extreme-minus-neutral 5-bar forward return difference is zero or negative. This covers the reversal case, a significantly negative difference with t ≤ −2, as well as no difference at all.  
Inconclusive: The result is inconclusive if the difference is positive but its t-statistic is below 2. It is also inconclusive if the difference is significant pooled but positive in only one of the three coins.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above it is". There is no fixed 70 threshold. Instead, "extreme" is measured against the RSI's own distance from 50 over the previous 60 bars and emphasised by the squaring. The low-extreme (short) side of the brief is not traded.  

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
            "id": "rsi_momentum",
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

### opus (0.0482 USD)

Forecast: Take the gap between the 50-day and the 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100. Divide it by the mean absolute value of its previous 200 daily readings and multiply by 10, capping at 20. Then clip it at 0 from below. The forecast is positive while the 50-day average is above the 200-day average, and it grows as the 50-day average pulls further above. It is zero while the 50-day average is at or below the 200-day average, so a cross back down closes the position. It is never negative. The settings are the usual 50/200 daily "golden cross", because the brief gives none.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Confirm: The horizon is 20 bars. Use non-overlapping 20-bar forward close-to-close returns, taken every 20th bar and pooled across the 6 windows. On bars where the forecast is above 0, the mean forward return must beat the mean over all sample bars (the coin held throughout) by at least +1.5 percentage points. This excess must also be positive in at least 4 of the 6 windows. Supporting check: the share of positive forward returns on forecast-above-0 bars beats the share on all bars by at least 5 percentage points.  
Reject: The pooled excess 20-bar forward return on forecast-above-0 bars is 0 or below, or it is negative in at least 4 of the 6 windows. Either result means a short average above the long one is followed by no more rise than random points, or by reversal.  
Inconclusive: The pooled excess is between 0 and +1.5 percentage points. Or the excess is positive in only 3 of the 6 windows. Or fewer than 8 non-overlapping sample bars carry a forecast above 0.  
Deviation: "After the short average crosses above the long one" becomes "while the 50-day SMA is above the 200-day SMA, sized by how far above". The test therefore pools fresh crosses with long-established trends; it is not an event study of the bars just after a cross. The short-side half of the brief and the price-crosses-long-average variant are not tested.  

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

### opus (0.0490 USD)

Forecast: Take the 50-day simple moving average of the close minus the 200-day simple moving average, as a percent of the 200-day average (EMASpreadComponent, average "sma", fast 50, slow 200). Divide it by the mean absolute value of its own previous 200 values and multiply by 10, capped at ±20. Clip it at 0, so the idea is long only. The forecast is positive exactly while the 50-day average is above the 200-day average, which is the stretch from an upward cross to the next downward cross. It grows continuously as the gap between the averages widens. It is zero while the 50-day average is below the 200-day average. It starts at about 0 at the upward cross and returns to 0 at the downward cross, so the position never jumps.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Confirm: Use a horizon of 1 bar (next-day close-to-close return; daily returns do not overlap, so each counts once). Pool all 6 windows and compare two numbers: the mean next-day BTC return on bars where the forecast is above 0, and the mean next-day return on all bars. The idea is confirmed if the first exceeds the second with a t-statistic of at least 2.0, before costs. A supporting check must also hold: the share of up days on bars with a positive forecast must be above the share of up days on all bars.  
Reject: The idea is rejected if the mean next-day return on positive-forecast bars is at or below the mean on all bars. It is also rejected if the share of up days on those bars is at or below the share on all bars. Either result means the stretches after an upward cross gain no more often and no further than the coin's ordinary days.  
Inconclusive: Three results neither confirm nor reject the idea. The first is an excess return that is positive but has a t-statistic below 2.0. The second is a positive excess return whose hit-rate check does not agree with it. The third is fewer than 60 positive-forecast bars across the 6 windows, because the 50-day average sits below the 200-day average for most of the test, so too few cross stretches are observed.  
Deviation: The idea holds a full position over the whole stretch between the crosses. The config instead sizes the position by the width of the gap between the averages, so the position is small just after the cross and largest deep into the trend. The idea compares the stretch with random stretches of the same length; the config compares it with all bars, which is the same as buy-and-hold over the period. The 50/200 periods are the daily convention, not the source script's settings, which the source does not give. Downward-cross stretches are not traded, because the idea is stated about upward crosses only.  

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

### opus (0.0612 USD)

Forecast: The forecast is non-zero only on a day that closes above the previous close on volume below its 20-day average, where the average includes that day. The regime detector tests this with VolumeExpansionHedgeComponent(vol_period 20) < 0. On such a day the forecast is minus the size of that day's rise. The rise is PriceEvolutionComponent(period 1), the close-to-close percent change. It is standardised against the mean absolute 1-day change of the previous 60 days (target 10, cap 20). It then passes through signed_power with exponent 2 and pivot 10, so a small rise gives a small short and a sharp rise gives a much larger one, and the sign is negated. The forecast is therefore always zero or negative. A rise of the usual daily size gives -10 (a 100% short). Half that size gives -2.5. One and a half times the usual size gives -22.5, clipped to -20. On every other day the forecast is 0 (flat).  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Confirm: The horizon is 1 bar: the day after each active day. Pool all active days across the 6 windows; each next-day return is counted once, because the days do not overlap. Take the strategy's per-bar return (forecast/10 × next-day return), before costs, and subtract what buy-and-hold earns at the same exposure, |forecast|/10 × the window's mean daily return. The idea is confirmed if the mean of this excess is above 0 with a t-statistic ≥ 2 over at least 60 active days. Supporting check: the next-day return following the third of active days with the largest |forecast| is lower than the next-day return following the third with the smallest.  
Reject: The mean excess return is ≤ 0. Or the next-day return after thin-volume up days, weighted by forecast size, is at or above the window's mean daily return, with t ≤ 0. Either result shows that the thin-volume rises are not given back.  
Inconclusive: The mean excess is positive but t < 2. Or there are fewer than 60 active days in total. Or the main measure passes but the supporting check goes the wrong way: the sharpest thin rises revert less than the mildest.  
Deviation: "Unusually low volume" becomes "below its 20-day average", a lower bar than the idea's "unusually low". "Sharp" becomes a graded size of the 1-day rise, damped smoothly for small rises, not a threshold. "Followed by falling back" is tested over the next day only, because the position cannot be held after the up day. The brief's comparison with high-volume moves is not tested by this idea's config.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "thin_up",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 20,
          "scaling_factor": 20.0
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
            "id": "up_move",
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

### opus (0.0125 USD)

Untestable: The idea needs the bitcoin return as the signal and an altcoin's later return as the outcome, but the config sees one coin at a time and the test runs only on BTC/USDT. No altcoin is traded and no altcoin's bars are available, so the lagged response of altcoins to bitcoin cannot be computed or traded.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0296 USD)

Untestable: The idea compares RSI at the current price high with RSI at the previous price high. The catalogue has no swing-high detection and no way to read RSI's past peak: `RSIPullbackComponent` gives only the current RSI level, and a percentile of RSI against its own history would need a second history op beside `standardise`, which V15 refuses. Any graded stand-in, such as the Donchian range position minus the RSI level, would drop that two-peak comparison, so it would not test the idea.  
