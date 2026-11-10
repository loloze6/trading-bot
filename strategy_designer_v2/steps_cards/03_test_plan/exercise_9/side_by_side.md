# Exercise 9: side by side

Prompt: `system_prompt_used.md`; the final helper (references in the system prompt, plan ids with the bar size). Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0548 USD)

Forecast: Uses the 14-bar Wilder RSI on daily closes (the standard setting). The raw reading is (50 - RSI) x 0.4. Each value is divided by the mean absolute value of the 60 readings before it and multiplied by 10, capped at +/-20. All positive values are then removed (clip at a maximum of 0), so the forecast is zero whenever RSI is at or below 50. It is negative (short) when RSI is above 50. A signed power with exponent 2 and pivot 10 is applied next. This keeps moderate readings small (a standardised -5 becomes -2.5). It makes extreme readings large (-15 becomes -22.5), and the combined forecast is clipped at -20. The short position therefore grows smoothly with how far RSI is above 50, and most of it sits at the high extremes. It never goes long.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Confirm: The test uses the 5-bar forward close-to-close return of the coin, before costs. Only bars where the forecast is -10 or lower (the high-RSI extremes) count, sampled at most once every 5 bars so overlapping returns are counted once. Their mean return minus the mean 5-bar return of all bars in the same window is the main measure. The idea is confirmed if this excess is negative, has a pooled t-stat of -2 or lower across all coins and windows, and is negative for at least 2 of the 3 coins. The supporting check is that the strategy's portfolio value, before costs, ends the windows above a portfolio that holds a short of the same average size in the coin.  
Reject: The idea is rejected if the pooled excess 5-bar return after forecasts of -10 or lower is positive with a t-stat of +2 or higher (continuation). It is also rejected if it is positive for at least 2 of the 3 coins.  
Inconclusive: A pooled t-stat between -2 and +2 is inconclusive. So is fewer than 30 non-overlapping extreme bars in total. So is a negative pooled excess that holds in only one coin.  
Deviation: "After RSI reaches a high extreme" is tested as "while RSI is above 50, sized by how far above". The short is held only while the reading stays elevated, and it shrinks as RSI falls back. A reversal that happens after RSI has dropped back below 50 is therefore not captured in the portfolio. It is still captured in the 5-bar forward-return measure. Moderate readings above 50 also carry a small short.  

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

### opus (0.0604 USD)

Forecast: RSI(14, Wilder) on daily closes, read as momentum. The raw component value is (50 − RSI) × 0.4. It is divided by its mean absolute value over the previous 60 bars and scaled to target 10 (cap ±20). The sign is then flipped, so the value is positive when RSI is above 50. Below 0 it is clipped to 0, which makes the forecast flat whenever RSI ≤ 50. Finally it is squared with sign kept (signed_power, exponent 2, pivot 10). The forecast is therefore 0 at RSI 50 and stays small near neutral readings. It grows with the square of RSI's distance above 50, so the largest long positions come at high extremes (RSI near or above 70). It is never negative.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Confirm: The test uses a 5-bar horizon, pooled over the 3 coins and 6 windows. Forward returns are taken from non-overlapping 5-bar blocks, so each return is counted once. Each block is classed by its starting bar. Extreme bars have recorded raw RSI value ≤ −8 (RSI ≥ 70). Neutral bars have raw value between −4 and +4 (RSI 40–60). The idea is confirmed if the mean forward 5-bar close-to-close return of extreme bars exceeds that of neutral bars with t ≥ 2, and the difference is positive in at least 2 of the 3 coins. Comparing against neutral bars of the same coin and period removes the market's own drift. Supporting check, before costs: the portfolio's total return beats buy-and-hold of the coin scaled by the strategy's average exposure, in at least 2 of 3 coins.  
Reject: The idea is rejected if the extreme-minus-neutral difference in mean forward 5-bar return is zero or negative pooled. It is also rejected if the difference is positive in fewer than 2 of 3 coins. A difference with t ≤ −2 additionally points to reversal rather than continuation.  
Inconclusive: A pooled difference that is positive but with t below 2, or that is confirmed pooled but positive in only 1 coin, neither confirms nor rejects the idea. The same holds if fewer than 20 non-overlapping extreme blocks exist across all coins and windows.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by the square of its distance from 50". Moderate readings above 50 therefore hold small long positions instead of none. The extreme-versus-neutral contrast is made in the evaluation, not in the position. Only the high-extreme (long) side is traded; low extremes stay flat.  

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
            "id": "rsi_mom",
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

### opus (0.0592 USD)

Forecast: The forecast is long-only and graded on the gap between the 50-day and 200-day simple moving averages of the close, the most common daily "golden cross" pair. - Raw value: (SMA50 − SMA200) / SMA200 × 100. - Scaling: the gap is divided by its own mean absolute value over the previous 200 bars and multiplied by 10, capped at 20. - Clip: the result is clipped at 0. - Positive: whenever the 50-day average is above the 200-day average, that is, in the state after an upward cross. It grows with how far the short average has pulled above the long one, up to 20 (200% long). - Zero: while the 50-day average is at or below the 200-day average. This is the state after a downward cross, which the brief says ends the trend. - Never negative.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Confirm: - Horizon: 10 bars, judged before costs. Within each window, sample every 10th bar so that forward returns do not overlap. - Main measure: the mean forward 10-bar BTC return on sampled bars with forecast > 0, minus the mean forward 10-bar return on all sampled bars of the same windows. This removes the coin's own drift, as against simply holding it. - Confirm if: that difference is at least +1.0% per 10 bars over at least 20 active samples, and it is positive in at least 4 of the windows that contain active bars. - Supporting check: the share of positive forward returns is higher on active bars than on all bars.  
Reject: The idea is rejected if the excess forward 10-bar return on active bars is 0 or negative over at least 20 active samples. It is also rejected if the Spearman correlation between forecast size and forward 10-bar return on active bars is below −0.1, which would mean moves after the cross reverse or exhaust.  
Inconclusive: The result is inconclusive in any of these cases: - The excess is between 0 and +1.0%. - The excess is positive in fewer than 4 of the windows that contain active bars. - There are fewer than 20 non-overlapping active samples. This is likely, because 50/200 crosses are rare in 6 windows of about 122 bars.  
Deviation: - "After a cross" becomes "while the short average is above the long one": the position is held for the whole up-state, not only the bars following the cross. - Size follows the gap, not freshness: the largest positions come when the gap is widest, typically well into a trend rather than just after the cross. The test therefore weights mature trends more than fresh crosses. - Downward crosses only end the trend: they set the position to flat and are not traded short.  

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
            "id": "sma_cross_gap",
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

### opus (0.0504 USD)

Forecast: While the 50-day simple moving average of the close is above the 200-day simple moving average (the stretch after an upward cross and before the next downward cross), hold a long position sized by the spread (SMA50 − SMA200) / SMA200 × 100. The spread is put on the scale of its own past by dividing it by its mean absolute value over the previous 200 bars and multiplying by 10, capped at 20, then clipped below at 0. The forecast is zero while SMA50 is at or below SMA200, which is the stretch between a downward cross and the next upward cross. It is positive and grows continuously with the gap between the averages: small just after a cross, larger as the averages separate. It is never negative.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Confirm: Horizon is 1 bar (next day's close-to-close return), pooled over all 6 windows, with each daily return counted once. The main measure is the mean next-day return on in-stretch bars (forecast > 0) minus the mean next-day return on out-of-stretch bars (forecast = 0). The idea is confirmed if this difference is positive with a Welch t-statistic ≥ 2. The supporting check is that the share of up days is higher in-stretch than out-of-stretch. The strategy's return per unit of exposure must also exceed buy-and-hold's mean daily return, before costs.  
Reject: The idea is rejected if the in-stretch minus out-of-stretch mean next-day return is ≤ 0, with at least 100 in-stretch bars and 30 out-of-stretch bars. It is rejected in its reversal form if that difference is negative with t ≤ −2, meaning the cross marks exhaustion.  
Inconclusive: The test is inconclusive in any of these cases: - the difference is positive but t < 2; - there are fewer than 100 in-stretch or fewer than 30 out-of-stretch bars across the 6 windows; - the windows contain fewer than 2 distinct upward-cross stretches, so the result rests on one trend episode.  
Deviation: The config holds a position sized by the gap between the averages, not a fixed full position from cross to cross. Gains are therefore weighted toward well-separated stretches, and days just after a cross carry little weight. The test is long-only, so the stretches after downward crosses are flat rather than tested short. "Random stretches of the same length" is replaced by a comparison with the out-of-stretch days and with buy-and-hold. The 50/200 periods are a convention, because the source does not give them.  

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

### opus (0.0785 USD)

Forecast: The forecast is active only on a daily bar that closes up on volume below its 20-bar average, where the average includes that day. A regime rule detects this with VolumeExpansionHedgeComponent (vol_period 20, raw value below 0). On every other bar the forecast is 0 (flat). On an active bar the forecast is short, sized by how sharp the day's rise was. The day's percent change (PriceEvolutionComponent, period 1) is divided by the mean absolute daily change of the 60 bars before it, times 10, capped at 20. It is then negated, passed through signed_power (exponent 2, pivot 10) and clipped at a maximum of 0. A rise of typical size gives about -10, i.e. 100% short. Half a typical rise gives -2.5. A rise of 1.4 times typical or more gives -20. The forecast is never positive.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Confirm: The horizon is 1 bar. The main measure is BTC's mean next-day return after the active bars, minus BTC's mean daily return over all bars of the same six windows. Each event counts once, because the returns do not overlap. The idea is confirmed if this excess return is negative with t ≤ -2, pooled over all windows, before costs. As a supporting check, events in the top half of |forecast| should show a more negative next-day return than events in the bottom half.  
Reject: The idea is rejected if the excess next-day return after active bars is ≥ 0. It is also rejected if the strongest-signal half shows a next-day return no lower than the weakest half, which would mean sharper thin-volume rises do not revert more.  
Inconclusive: An excess return that is negative but with -2 < t < 0 is inconclusive. So is a pooled sample of fewer than 60 active bars.  
Deviation: "Unusually low volume" becomes "volume below its 20-bar average", which covers more days than truly unusual ones. "Followed by a fall" is tested only over the next single day. The short position lasts one bar unless the next day is again a thin-volume up day. "Sharp" is not a cutoff: the short size grows with the day's rise, so small up days get small or untraded shorts. Only the low-volume half of the brief is tested. The high-volume continuation case is not part of this config.  

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
                "op": "negate"
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

### opus (0.0190 USD)

Untestable: The idea forecasts altcoin returns from bitcoin's earlier move, but the test runs on BTC/USDT alone and the config sees only one coin's bars, so it cannot read bitcoin's move while trading an altcoin, or an altcoin's response while trading bitcoin. Trading bitcoin's own momentum would drop the cross-coin lead-lag relation that the idea is about.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0385 USD)

Untestable: The idea compares RSI at the new price high with RSI at the previous price high. The catalogue has no way to find that earlier high or read the RSI value there: there is no swing-high detection, no rolling maximum of RSI, and no lagged value of a component. Any config could only use today's RSI level at a high in the price range. That drops the peak-to-peak comparison that defines a divergence and turns the test into the RSI-level question the brief excludes.  
