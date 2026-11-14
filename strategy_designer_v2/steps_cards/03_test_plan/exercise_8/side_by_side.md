# Exercise 8: side by side

Prompt: `system_prompt_used.md`. Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0555 USD)

Forecast: Use the 14-period Wilder RSI on daily bars, taken as (50 - RSI) through RSIPullbackComponent. Divide it by the mean absolute value of its previous 60 readings and multiply by 10 (standardise, capped at ±20). Apply signed_power with exponent 2 and pivot 10, so moderate readings shrink smoothly toward 0 and large ones grow. Then clip at a maximum of 0, so only the short side remains. The forecast is zero whenever RSI is at or below 50. It turns negative (short) when RSI is above 50, and the short grows roughly with the square of how far RSI sits above 50 relative to its own recent typical distance. A reading about as far from 50 as usual gives -10, which is 100% short. Readings near RSI 70 or higher reach the -20 cap, which is 200% short. The forecast is never positive.  
Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: The test uses a 5-bar horizon and pools 3 coins × 6 windows. Take the bars where the forecast is ≤ -10, keep only non-overlapping ones (at least 5 bars apart, giving at least 20 such observations), and measure the coin's mean forward 5-bar return after them. The idea is confirmed if that mean is negative and at least 1 percentage point below the mean of all non-overlapping 5-bar returns on the same windows (the hold-the-coin baseline), before costs. Supporting check: the same sign of difference holds in at least 2 of the 3 coins.  
Reject: The idea is rejected if the pooled mean forward 5-bar return after forecast ≤ -10 is at or above the unconditional 5-bar mean. It is also rejected if it is higher than the unconditional mean in at least 2 of the 3 coins, meaning price continues or behaves as usual after high RSI.  
Inconclusive: The result is inconclusive in three cases: the conditional mean is below the baseline by less than 1 percentage point; it is below the baseline by more but in fewer than 2 of 3 coins; or there are fewer than 20 non-overlapping observations with forecast ≤ -10.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, short sized by the square of its standardised distance from 50". The position closes as soon as RSI falls back to 50, not over a fixed set of following bars. "Extreme" is judged against RSI's own recent typical distance from 50 rather than a fixed level such as 70. The low-extreme (long) side of the brief is not tested.  

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
                "op": "signed_power",
                "params": {
                  "exponent": 2
                }
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

### opus (0.0618 USD)

Forecast: Use the 14-bar RSI on daily bars, through RSIPullbackComponent (period 14, long_only false). Its raw value is (50 − RSI) × 0.4. This value is standardised against its own past 60 values (target 10, cap 20, min_periods 20) and then negated, so it rises with RSI above 50. It is then clipped at 0, so the forecast is zero whenever RSI ≤ 50. Finally it goes through signed_power with exponent 2 and pivot 10. That step damps readings just above 50 towards zero and amplifies high readings. The forecast is never negative. It is near 0 for neutral readings and grows smoothly, roughly with the square of how far RSI sits above 50 relative to its usual distance. Strong overbought readings (RSI around 70–80+) reach the cap of +20, which is a 200% long position.  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: - Horizon: 5 bars, using the recorded RSI component value. Extreme bars have RSI ≥ 70 (raw ≤ −8); neutral bars have RSI 40–60 (|raw| ≤ 4). - Main measure: the mean 5-bar forward close-to-close return after extreme bars minus the mean after neutral bars. Returns are sampled non-overlapping, so each 5-bar block counts once, and pooled over the 3 coins and 6 windows, before costs. - Confirm if: the difference is positive with t ≥ 2, from at least 30 non-overlapping extreme observations, and is positive in at least 2 of the 3 coins. - Supporting check: the strategy's total return beats buy-and-hold scaled to the strategy's average exposure.  
Reject: Reject if the pooled difference (extreme minus neutral 5-bar forward return) is ≤ 0. If it is negative with t ≤ −2, that points to reversal instead. Also reject if it is negative in at least 2 of the 3 coins.  
Inconclusive: The result is inconclusive in these cases: - the difference is positive but t < 2; - there are fewer than 30 non-overlapping extreme observations; - the difference is positive in only one coin.  
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50", with the position growing with the squared distance above 50. A small position is held on mildly elevated readings, not only on extremes. - The position follows RSI down instead of being held for a fixed number of bars after the extreme. - Low extremes are flat by design.  

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
            "id": "rsi_up",
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

### opus (0.0512 USD)

Forecast: The 50-day vs 200-day simple moving average spread on daily closes: (SMA50 − SMA200) / SMA200 × 100. This is scaled against the mean absolute value of its own previous 200 values, so a typical spread gives about 10, capped at 20. It is then clipped at 0 because the idea is only about upward crosses. The forecast is positive while SMA50 is above SMA200, which is the state that begins at an upward cross. It grows continuously as the short average pulls further above the long one. It is zero while SMA50 is at or below SMA200, and never negative.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: The horizon is 20 bars. Take one sample at every 20th bar across the six windows and pool them, so returns do not overlap. Measure the close-to-close log return over the next 20 bars. The main measure is the mean of that return on sampled bars where the forecast is above 0, minus the mean over all sampled bars (the random-point and hold baseline), before costs. The idea is confirmed if this excess is above 0 with a t-statistic of at least 2. The supporting check is that the share of positive 20-bar returns on forecast-positive samples is also higher than on all samples.  
Reject: The idea is rejected if the excess mean 20-bar return on forecast-positive samples is zero or negative. A clearly negative excess, meaning returns reverse after up-crosses, is a rejection on the brief's own exhaustion clause.  
Inconclusive: A positive excess with a t-statistic below 2 neither confirms nor rejects the idea. The same applies if fewer than 8 of the sampled bars have a positive forecast across the six windows, because the forecast was rarely positive.  
Deviation: "After an upward cross" becomes "while SMA50 is above SMA200, sized by how far above it is". The position is small right at the cross and largest well after it, when the spread is widest. So the test measures persistence of the up state rather than what follows the cross event itself. Down-crosses from the brief are not traded, because the idea concerns only upward crosses.  

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

### opus (0.0470 USD)

Forecast: The 50-day and 200-day simple moving averages of the close, the most common pair on daily bars (golden and death cross). Take the spread (SMA50 - SMA200) / SMA200 in percent. Divide it by the mean absolute spread of the 200 bars before it and multiply by 10, capped at 20. Then clip it at 0. The forecast is positive while the 50-day average sits above the 200-day average, which is the stretch from an upward cross to the next downward cross. Its size grows with how far the short average has pulled above the long one. It is zero while the short average is below the long one, because the idea makes no claim about those stretches. It is never negative.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: Pool all six windows and use a 1-bar horizon, counting each daily return once. The mean next-bar BTC close-to-close return on bars with forecast > 0 must exceed the mean next-bar return over all tested bars by a t-statistic of at least 2.0, before costs. The supporting check is that the share of up bars among forecast > 0 bars is higher than the share of up bars over all tested bars.  
Reject: The mean next-bar return on forecast > 0 bars is at or below the all-bar mean, or the strategy's equity does no better than buy-and-hold scaled to the same average exposure. A t-statistic of -2.0 or lower would also show that moves after up-crosses tend to reverse.  
Inconclusive: The difference is positive but its t-statistic is below 2.0, or fewer than 100 tested bars have forecast > 0.  
Deviation: The idea treats the up-cross stretch as one on/off state. The config instead sizes the position by the width of the SMA50/SMA200 spread, so it tests "while the short average is above the long one, and more so the wider the gap". It does not test an equal bet from each cross. Periods 50/200 are a convention, because the brief gives none. Only the long side of the cross is tested.  

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

Forecast: Active only on a day whose volume is below its 20-day average volume. That condition is set by a regime veto: volume_filter (period 20) applied to a constant +10 gives 0 on low-volume days, and the veto fires when that value is below 5. On those days the forecast is short and sized by the day's rise: - the 1-day close-to-close return (PriceEvolutionComponent, period 1), divided by the mean absolute 1-day return of the previous 60 days (standardise, window 60, min_periods 20, target 10, cap 20); - then negated, then clipped to at most 0, so down days give 0; - then passed through signed_power (exponent 2, pivot 10), so small rises give a tiny short and sharp rises a large one. The result runs from 0 (flat or down day) to about -40, clipped at -20 by the engine. On normal or high-volume days the regime is null and the forecast is 0. It is never positive.  
Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Horizon is 1 bar (the position is set at the close of the thin-volume up day and held over the next day). Pool all active bars (forecast < 0) across the 6 windows; non-overlapping one-day returns count once. Regress the next day's coin return, minus that window's mean daily return, on the forecast. Confirm if the slope is positive (bigger shorts are followed by lower-than-average returns) with t ≥ 2. Supporting check: the forecast-weighted sum of demeaned next-day returns is favourable to the short in at least 4 of the 6 windows.  
Reject: Reject if the pooled slope is zero or negative: after thin-volume rises, the next day's demeaned return is no lower, or is higher, the larger the rise.  
Inconclusive: A positive slope with t between 0 and 2, or fewer than 60 active bars in total. Also a slope with t ≥ 2 that is favourable in only 3 or fewer windows.  
Deviation: - "Unusually low volume" becomes volume below its own 20-day average, a plain threshold rather than an extreme. - "Sharp move" becomes the size of a single day's rise relative to the past 60 days' moves, graded rather than thresholded. - "Followed by price falling back" is tested only over the one day after the move bar, because the position exists only while the condition holds. A slower reversion over several days is not captured. - The brief's contrast with high-volume moves (which should hold) is not tested: those days are flat.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "volgate",
        "class": "strategies.strategy_components.BuyAndHoldStrategy",
        "params": {}
      }
    ],
    "vetoes": [
      {
        "id": "volgate",
        "transforms": [
          {
            "op": "volume_filter",
            "params": {
              "period": 20
            }
          }
        ],
        "rules": [
          {
            "op": "lt",
            "value": 5
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
    "regimes": {
      "mean_reversion": {
        "components": [
          {
            "id": "thin_rise",
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

### opus (0.0146 USD)

Untestable: The idea needs bitcoin's past returns to forecast an altcoin's later returns, but the config sees only one coin at a time and cannot read another coin's prices. The test also runs only on BTC/USDT, so there is no altcoin whose lagged response could be measured.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0320 USD)

Untestable: The idea compares RSI at the current price high with RSI at the previous price high, which needs a memory of past swing highs. No catalogue component finds swing highs or records RSI at them; the closest composition, a Donchian range position combined with RSI level, drops that peak-to-peak comparison and becomes a plain range-fade. The brief's own test, divergent new highs against non-divergent new highs, cannot be built either, because the detector has no rule that can flag a divergence.  
