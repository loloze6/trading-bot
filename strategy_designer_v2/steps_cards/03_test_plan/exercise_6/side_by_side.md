# Exercise 6: side by side

Prompt: `system_prompt_used.md` (unchanged from exercise 5). Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0574 USD)

Forecast: Use the 14-bar Wilder RSI on daily closes, taken from RSIPullbackComponent (period 14), which outputs (50 − RSI) × 0.4. Standardise it against the mean absolute value of its own previous 60 readings (min_periods 20, target 10, cap 20). Clip it at a maximum of 0, so only the overbought side is kept: zero whenever RSI ≤ 50, negative when RSI > 50. Then apply signed_power with exponent 2 and pivot 10. This damps mild readings towards 0 (−5 becomes −2.5) and amplifies extreme ones (−15 becomes −22.5, and the combined forecast is clipped at −20). The forecast is therefore never positive. It is 0 when RSI is at or below 50, and it shorts the coin more and more strongly the further RSI sits above 50, measured against the coin's own recent RSI excursions. It runs on every bar, with no regime gate.  
Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: Horizon is 5 bars. Take the bars where the forecast is ≤ −10, keeping one entry per non-overlapping 5-bar block. Over all 3 coins and 6 windows, the coin's 5-bar forward close-to-close return after those bars is at least 1.0 percentage point below the coin's unconditional mean 5-bar return over the same windows (buy-and-hold). The t-statistic on the non-overlapping returns must be ≤ −2, and the difference must be negative in at least 2 of the 3 coins. Supporting check: the strategy's before-cost return, pooled across windows, is positive in at least 2 of the 3 coins.  
Reject: Pooled across coins and windows, the mean 5-bar forward return after forecast ≤ −10 bars is equal to or above the unconditional mean 5-bar return, or the difference is ≥ 0 in at least 2 of the 3 coins.  
Inconclusive: The pooled difference is negative but smaller than 1.0 percentage point, or the t-statistic is between −2 and 0. Also inconclusive: fewer than 30 non-overlapping qualifying blocks in the pooled sample.  
Deviation: The idea says "after the RSI reaches a high extreme". The config tests "while the RSI is above 50", with a short sized by how far above 50 it is. Mild readings take small damped shorts rather than none. The extreme is judged against the coin's last 60 RSI readings, not against a fixed level such as 70. The config holds the position only while the reading stays high; it does not hold it for a set number of bars after the extreme.  

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

### opus (0.0604 USD)

Forecast: Use the 14-bar Wilder RSI on daily closes, through RSIPullbackComponent (period 14, long_only false). Its raw value is (50 − RSI) × 0.4. Standardise it: the latest value times 10, divided by the mean absolute value of the 60 stored values before it (min_periods 20), capped at ±20. Negate it, so it is positive when RSI is above 50. Clip it at a minimum of 0, so it is zero whenever RSI is 50 or below. Then apply signed_power with exponent 2 and pivot 10: small readings are damped smoothly towards 0 and extreme readings are amplified. The forecast is long only and graded. It is zero at RSI ≤ 50 and grows with the square of how far RSI sits above 50, measured against the coin's own recent RSI swings. A typical high extreme (RSI around 65–70) takes it near or to the +20 cap. Readings near 55 give about +2. The forecast is never negative. There is no regime gate.  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: Horizon is 5 bars, using the forward 5-bar close-to-close return. - Extreme bars: forecast ≥ 10. - Neutral bars: RSI between 40 and 60, which is a raw rsi_strength value between −4 and +4. - Sampling: each side keeps only one bar per 5 bars (no overlapping returns), pooled over the 3 coins and 6 windows. - Main measure: extreme-bar mean forward return minus neutral-bar mean forward return. - Confirmation: that difference is above 0 with t ≥ 2, and it is positive for at least 2 of the 3 coins. - Supporting check: the strategy's before-cost return beats an exposure-matched hold, which is the bar-by-bar mean allocation times the coin's return over each window.  
Reject: The idea is rejected if the pooled difference (extreme minus neutral) is ≤ 0 with at least 30 non-overlapping extreme observations. A significantly negative difference (t ≤ −2) would point to reversal instead.  
Inconclusive: These results neither confirm nor reject: - a positive difference with t below 2; - a positive pooled difference carried by only one coin; - fewer than 30 non-overlapping extreme observations pooled.  
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50", sized by the squared distance above 50. - Mildly strong readings therefore hold small positions instead of none. - "Extreme" is judged against the coin's own last 60 bars of RSI swings, not a fixed 70 level. - Low extremes are left flat, because the idea concerns only high readings.  

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
            "id": "rsi_strength",
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

### opus (0.0495 USD)

Forecast: Take the percent spread between the 50-day and 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100. The brief gives no lengths, so I used the most common daily-bar convention, the 50/200 "golden cross". Standardise the spread against its own previous 200 values (window 200, min_periods 50), so a typical spread maps to about 10, capped at 20. Then clip it at 0 from below. The forecast is zero while SMA50 is at or below SMA200. It turns positive the moment SMA50 crosses above SMA200, starting from zero with no jump. It grows in proportion to how far SMA50 has pulled above SMA200, up to +20 (200% long). It never goes short, because the idea is only about the upward cross.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: The horizon is 20 bars. Sample one bar every 20 bars, so overlapping returns are counted once, and pool the samples across the 6 windows. The idea is confirmed if two things hold: - Main measure: on sampled bars with forecast > 0, the forecast-weighted mean forward 20-bar return of BTC beats the mean forward 20-bar return of all sampled bars (the buy-and-hold baseline) by at least 1.0 percentage point. This must hold in at least 4 of the 6 windows that have active bars. - Supporting check: the share of active samples with a positive forward 20-bar return is higher than the same share over all samples.  
Reject: The idea is rejected if the forecast-weighted forward 20-bar return on active bars is at or below the all-bars baseline in the pooled sample. It is also rejected if that return is negative, which would mean moves after upward crosses reverse.  
Inconclusive: The result is inconclusive in any of these cases: - The pooled excess is positive but below 1.0 percentage point. - The excess is positive pooled but holds in fewer than 4 of the windows with active bars. - Fewer than 10 non-overlapping active samples exist across all windows.  
Deviation: The idea says "after an upward cross". The config tests "while SMA50 is above SMA200, more strongly the wider the gap". The position starts near zero right at the cross and is largest later in an established uptrend, not just after the cross event.  

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

### opus (0.0486 USD)

Forecast: Long only, and only while the 50-day simple moving average of the close is above the 200-day simple moving average. That is the stretch that runs from an upward cross until the next downward cross. The raw value is (SMA50 − SMA200) / SMA200 × 100, using the averages as of each bar's close with the current close included. It is divided by the mean absolute value of its own previous 200 values and multiplied by 10, capped at 20. It is then clipped at 0. So the forecast is zero whenever SMA50 is at or below SMA200 and is never negative. Inside an up-stretch it is positive and grows smoothly with the gap between the two averages. It starts near 0 at the upward cross and returns to 0 at the downward cross.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: The test pools all six windows and uses non-overlapping 1-bar horizons. The main measure is the mean next-bar close-to-close return on bars where the forecast is above 0, minus the mean next-bar return over all bars, before costs. The idea is confirmed if this difference is positive with t ≥ 2 and rests on at least 100 in-stretch bars. The supporting check is the share of up bars: it must be higher inside the stretches than over all bars.  
Reject: The idea is rejected if the in-stretch mean next-bar return is at or below the all-bar mean. It is rejected more strongly if it is significantly below (t ≤ −2), because that would show that returns tend to reverse after upward crosses.  
Inconclusive: The test is inconclusive if the difference is positive but t < 2. It is also inconclusive if fewer than 100 bars fall inside up-stretches, or if all the in-stretch bars come from a single cross episode.  
Deviation: The idea treats every bar between the crosses alike. The config instead sizes the position by how far SMA50 sits above SMA200, so bars just after a cross get small positions. The confirm and reject measures use the stretch membership itself (forecast above 0), not the size of the position. The test covers only up-crosses on BTC with the conventional 50/200 settings, because the brief gives none. Cross-of-price-over-long-average variants and down-crosses are not tested.  

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

### opus (0.0744 USD)

Forecast: The forecast is active only on a day that closes higher than the day before on volume below its 20-day average volume (the average includes that day). This condition comes from the regime detector, using VolumeExpansionHedgeComponent(vol_period 20) as a measure only, and its raw value must be below 0. On every other day the forecast is 0. On an active day the forecast is short and sized by how sharp the rise was. Take that day's 1-bar percent change (PriceEvolutionComponent, period 1) and standardise it against the mean absolute 1-day change of the 60 days before it, so a typical daily move gives 10 and the cap is 20. Pass it through signed_power with exponent 2 and pivot 10: a move half the typical size gives 2.5, a typical move gives 10, and a move 1.5 times typical gives 22.5. Then negate it and clip it at a maximum of 0. The forecast therefore runs from about 0 for a tiny rise down to −20 (200% short) for a rise of about 1.4 times the typical daily move or more. Small rises are damped smoothly towards flat. The position lasts one bar unless the next day is again a low-volume up day.  
Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: The horizon is 1 bar, so the events do not overlap; there are roughly 150–250 of them over the 6 windows. Main measure: on bars with a non-zero position, the position-weighted mean of the next bar's close-to-close return, minus the coin's unconditional mean daily return over the same windows. The idea is confirmed if this excess, measured before costs, is positive with a t-statistic of at least 2. Supporting check: the excess is positive in at least 4 of the 6 windows.  
Reject: The idea is rejected if the position-weighted excess next-bar result is zero or negative. That means the day after a thin-volume rise is no weaker than an average day, or it is stronger.  
Inconclusive: The excess is positive but its t-statistic is below 2. Or the excess is positive with t ≥ 2 but positive in fewer than 4 of the 6 windows. Or fewer than 60 active bars traded across all windows.  
Deviation: The idea gives no horizon for "followed by falling back", so the config tests a fall on the next single day only. "Unusually low volume" becomes volume below its 20-day average, a binary regime gate whose level is not graded. "Sharp" is graded by the size of the 1-day rise relative to the last 60 days' typical daily move, through a smooth dead zone, and is not a threshold. A rise that builds over several days is not covered. The brief's comparison with high-volume moves is not part of this idea and is not tested.  

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
              },
              {
                "op": "clip",
                "params": {
                  "max": 0.0
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

### opus (0.0152 USD)

Untestable: The idea forecasts altcoin returns from bitcoin's earlier move, but the test runs only on BTC/USDT, and the config sees one coin at a time with no other coin's prices in the catalogue. So a forecast on an altcoin cannot read bitcoin's move, and a forecast on bitcoin cannot be judged against altcoin returns.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.1224 USD)

Forecast: The forecast is active only on bars where the close is at or very near its 20-day closing high, meaning the close sits in the top 2.5% of the range of the last 20 closes. On every other bar it is 0. On an active bar it is short, sized by how weak the 14-day Wilder RSI is. R is RSI strength (RSI − 50), divided by its own mean absolute value over the previous 60 bars, times 10, then held between 0 and 10. The forecast is (R − 10) / 2. It is 0 when RSI is at or above its usual strength, and it grows toward −5 (50% short) as RSI falls toward 50 while price is at the high. It is never positive.  
Config: 005-01_bearish-rsi-divergence-reversal_config.json  
Confirm: Pool all coins and windows. Take the new-high bars (recorded Donchian value ≥ 19) and keep one bar per cluster, with clusters at least 10 bars apart so overlapping returns count once. On these bars, the mean 10-bar forward close-to-close return after divergence bars (forecast < 0) is negative and at least 2 percentage points below the mean after non-divergence new-high bars (forecast = 0). This needs at least 20 divergence episodes and a one-sided permutation p < 0.05. Supporting check: across the divergence bars, the Spearman correlation between forecast and the 10-bar forward return is positive, so larger shorts are followed by weaker returns.  
Reject: With at least 20 divergence episodes, the 10-bar forward return after divergence new highs is not below the return after non-divergence new highs (difference ≥ 0). Or it is lower by less than 0.5 percentage points with permutation p > 0.3.  
Inconclusive: Fewer than 20 independent divergence episodes. Or a difference between −0.5 and −2 points, or below −2 points with p ≥ 0.05. Or results that point in opposite directions on different coins with no pooled significance.  
Deviation: "RSI makes a lower high than at the previous price high" becomes "RSI is weaker than its usual absolute deviation from 50 while the close is at its 20-day high". No comparison with RSI at the previous peak is made, because the catalogue has no rolling RSI maximum. "New high" means the close is in the top 2.5% of the 20-day close range, not a new swing high. The short is held only while price stays at the high. The retracement that follows is measured from the recorded price over 10 bars, not earned by the position. Only the bearish side is tested.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "don",
        "class": "strategies.strategy_components.DonchianBreakoutComponent",
        "params": {
          "period": 20,
          "scaling_factor": 20.0
        }
      }
    ],
    "vetoes": [],
    "rules": [
      {
        "regime": "trending",
        "any_of": [
          [
            {
              "id": "don",
              "op": "gte",
              "value": 19.0
            }
          ]
        ]
      }
    ],
    "default_regime": "unknown"
  },
  "strategies": {
    "min_allocation_change": 0.05,
    "regimes": {
      "trending": {
        "components": [
          {
            "id": "rsi_strength",
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
                  "min": 0.0,
                  "max": 10.0
                }
              }
            ]
          },
          {
            "id": "offset",
            "class": "strategies.strategy_components.BuyAndHoldStrategy",
            "params": {},
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
              }
            ]
          }
        ]
      },
      "mean_reversion": null,
      "chop": null,
      "unknown": null
    }
  }
}
```
