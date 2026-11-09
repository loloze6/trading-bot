# Exercise 7: side by side

Prompt: `system_prompt_used.md`. Opus, the same seven ideas.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2785 USD)

Forecast: Short only, and only on the high side of the RSI. Compute the 14-bar Wilder RSI on daily closes and take (50 − RSI). This is 0 at RSI 50 and negative when RSI is above 50. Divide it by the mean absolute value of the 60 readings before the current bar and multiply by 10, capped at ±20; this puts it on the forecast scale. Set every positive value (RSI below 50) to 0, so the forecast is zero whenever the index is not elevated. Then apply a graded dead zone, 20 × sign × (|v|/20)²: - a mildly elevated RSI gives a small short (−10 becomes −5); - the largest readings give the largest short (−20 stays −20, a 200% short). The forecast is never positive and grows in size continuously as RSI rises further above 50 relative to its recent range.  
Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: - Main measure, horizon 5 bars. Pool all 3 coins × 6 windows. Take bars where the forecast is ≤ −10, about the strongest RSI readings, sampled at most once per 5-bar block so overlapping returns count once. Their mean 5-bar forward close-to-close return, minus the mean 5-bar forward return of all bars in the same coin-window (the buy-and-hold drift), must be ≤ −1.0%, with a t-statistic ≤ −2. - Coin agreement. The excess must be negative in at least 2 of the 3 coins. - Supporting check. The strategy's summed before-cost return over the 18 coin-windows is positive.  
Reject: The pooled excess 5-bar forward return after forecast ≤ −10 bars is ≥ 0 (price does not fall more than usual after high RSI). If it is positive with t ≥ +2, this is evidence for continuation instead.  
Inconclusive: - The excess is negative but smaller than 1.0% in size, or its t-statistic lies between −2 and 0. - Fewer than 30 non-overlapping extreme samples exist. - The coins disagree in sign, with only 1 of 3 negative.  
Deviation: - Timing. "After RSI reaches a high extreme" becomes "while RSI is above 50". The short is held and sized continuously by how far RSI is above 50, with no fixed extreme threshold; the dead zone only damps the moderate readings. - Relative scale. "Extreme" is measured relative to the mean absolute RSI deviation of the previous 60 bars, not as a fixed level such as 70. - Low side. The low-extreme (oversold) side of the brief is not tested by this idea.  

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

## 001-03_rsi-high-extreme-continuation

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

### opus (0.2673 USD)

Forecast: Take the 14-bar Wilder RSI on daily closes and use how far it sits above 50 (RSI − 50) as the signal. This is RSIPullbackComponent(14), which outputs (50 − RSI) × 0.4, with its sign flipped. Standardise it against its own previous 60 values (min_periods 20). Then clip it at 0, so only RSI above 50 is held. Then apply signed_power with exponent 2 (pivot 10): readings near 50 are pushed towards 0 and high readings are amplified. The forecast is 0 whenever RSI ≤ 50 and never negative. Above 50 it is positive and grows with the square of the standardised distance, reaching the +20 cap (200% long) at strongly overbought readings such as RSI ≈ 70 or above. Low-RSI extremes are not part of this idea and give no position.  
Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: The horizon is 5 bars, measured before costs. Recover RSI from the recorded indicator value as 50 − value / 0.4, and sample every 5th bar so no 5-bar return is counted twice. Pool all coins and windows. The idea is confirmed if the mean 5-bar forward return of the coin after extreme bars (RSI ≥ 70, where the forecast is largest) exceeds the mean after neutral bars (RSI 40–60) by a positive amount with a t-statistic ≥ 2. This needs at least 30 non-overlapping extreme observations, and the difference must be positive in at least 2 of the 3 coins. Supporting check: the portfolio's return must exceed (average allocation × the coin's buy-and-hold return) over the same windows.  
Reject: The idea is rejected if the pooled difference (extreme minus neutral 5-bar forward return) is zero or negative. It is also rejected if the difference is negative in 2 or more of the 3 coins.  
Inconclusive: A positive pooled difference with a t-statistic below 2. Also inconclusive: fewer than 30 non-overlapping extreme observations, or a positive pooled difference carried by a single coin.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above". Moderate readings (RSI just above 50) also take small long positions, and the position is held for as long as RSI stays high rather than for a fixed number of bars after the extreme. Low-RSI extremes are left flat.  

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

### opus (0.2554 USD)

Forecast: The forecast is the percent spread between the 50-day and 200-day simple moving averages of the close: (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own last 200 daily values, so an average-sized spread is about 10 and the cap is 20. It is then clipped below at 0. The forecast is positive and grows with the spread while the 50-day average is above the 200-day average. It is 0 when the 50-day average is at or below the 200-day average. It is never negative, because the idea is only about upward crosses. The forecast starts from 0 at the moment of the cross and grows as the short average pulls away from the long one, so the position is built up gradually rather than switched on.  
Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: The test uses a horizon of 20 bars and samples every 20th bar, so the forward returns do not overlap (about 36 samples across the 6 windows). The forward return is demeaned by the mean 20-bar return of its own window, so the coin's own rise is not credited to the idea. The idea is confirmed if two things hold. First, the slope of the demeaned forward 20-bar log return on the forecast at the start of each sample is positive with t ≥ 2. Second, as a supporting check, the samples with forecast > 0 have a demeaned mean forward return above 0 in at least 4 of the windows that contain such samples.  
Reject: The idea is rejected if the slope is ≤ 0. It is also rejected if the samples with forecast > 0 show a demeaned mean forward return below 0 with t ≤ −1, which would mean moves after upward crosses fade or reverse relative to random points.  
Inconclusive: The test is inconclusive if the slope is positive with t below 2. It is also inconclusive if fewer than 10 non-overlapping samples have a forecast above 0, for example because the 50-day average stays below the 200-day average through most windows.  
Deviation: "After an upward cross" becomes "while the 50-day SMA is above the 200-day SMA, sized by how far apart they are." The forecast does not single out the bars just after the cross: it is small there and largest when the trend is well established. So it tests persistence of the whole above-the-long-average state, not the freshness of the cross. The cross of price itself over the long average and the downward cross from the brief are not tested.  

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

### opus (0.2628 USD)

Forecast: Long only, and only while the 50-day simple moving average of the close is above the 200-day simple moving average, which is the stretch between an upward cross and the next downward cross. The raw reading is the spread between the two averages, (SMA50 − SMA200) / SMA200 × 100, from EMASpreadComponent with average "sma", fast 50 and slow 200. This is the most common daily-bar convention, the golden/death cross. The spread is standardised against its own past 200 values (min_periods 50), giving an average absolute value of about 10 and a cap of 20. It is then clipped at 0. The forecast is therefore 0 whenever SMA50 ≤ SMA200, from the downward cross until the next upward cross. While SMA50 > SMA200 it is positive and grows smoothly with how far the short average sits above the long one. It starts near 0 right at the upward cross and returns to 0 at the downward cross, so the position never jumps. It is never negative.  
Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: Horizon: 1 bar. Each daily return is counted once, so no returns overlap. Main measure: over all 6 windows pooled, the mean next-1-bar close-to-close log return on bars where the forecast is > 0, minus the mean over all bars (buy-and-hold). The idea is confirmed if this difference is positive with a t-statistic ≥ 2, judged before costs. It also needs at least 60 bars with forecast > 0. Supporting check: the share of up days on forecast > 0 bars must also exceed the share on all bars.  
Reject: The idea is rejected if the difference in mean next-bar return between forecast > 0 bars and all bars is ≤ 0, given at least 60 forecast > 0 bars. It is also rejected if the forecast > 0 bars show a lower share of up days than all bars, which would point to reversal or exhaustion after the upward cross.  
Inconclusive: Any of these neither confirms nor rejects the idea: - the difference is positive but its t-statistic is below 2; - fewer than 60 bars have forecast > 0; - all forecast > 0 bars come from a single upward-cross stretch, which is likely with 50/200 on about 732 daily bars; - the main measure and the supporting check disagree in sign.  
Deviation: - While, not after: "over the stretch after an upward cross" becomes "while SMA50 is above SMA200". A stretch whose cross happened before a window starts is counted too. - Graded size: the position is sized by the gap between the averages instead of being a fixed long. Bars just after the cross, when the gap is small, therefore get little weight. - Long side only: the brief's symmetric short side, and its price-crosses-the-long-average variant, are not tested.  

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

### opus (0.2812 USD)

Forecast: The forecast is active only on a daily bar that closed above the previous close on volume below its 20-bar average, where the average includes the current bar. That condition is read by the regime detector: VolumeExpansionHedgeComponent(vol_period 20) is below 0. On those bars the forecast is short. It is built from that bar's one-day move, PriceEvolutionComponent(period 1), in four steps: 1. Standardise it against its own 60 previous daily values (min_periods 20). A move of typical size reads 10, a larger one more, capped at 20. 2. Apply signed_power with exponent 2 and pivot 10. Small up-moves are damped smoothly towards 0 and sharp ones are amplified. 3. Negate it. The forecast therefore runs from about 0 (a tiny up-move) to -20 (an up-move about 1.4 times the typical size or more), and grows in size with the sharpness of the rise. On every other bar (down bars, and up bars on average or higher volume) the forecast is 0, so the position is flat. Each short is held for the one bar after the event, unless the next bar is also a thin-volume up bar.  
Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Horizon is 1 bar (the next daily close-to-close return after each thin-volume up bar; these returns do not overlap). Pool the event bars across the 6 windows. Confirmation needs two results: - The main measure, the position-weighted next-bar return (forecast/10 × next return), is positive before costs with a t-statistic of at least 2 over at least 30 events. - The plain mean next-bar return after these events is below the mean next-bar return of all bars, the buy-and-hold benchmark. Supporting check: the third of events with the largest |forecast| shows a lower mean next-bar return than the smallest third.  
Reject: Reject if the position-weighted next-bar return is zero or negative. Also reject if the mean next-bar return after thin-volume up bars is at or above the unconditional mean next-bar return of all bars, meaning the thin-volume rise holds or continues at least as well as an average day.  
Inconclusive: Inconclusive in three cases: - The position-weighted return is positive but its t-statistic is below 2. - There are fewer than 30 events across all windows. - The pooled result is positive but the larger-forecast third does not revert more than the smaller third.  
Deviation: Four differences from the idea as written: - "Unusually low volume" becomes any volume below its 20-day average, with no stricter cut. - "A sharp upward move" becomes a single daily close-to-close rise, graded by its size relative to the last 60 days rather than gated on being sharp. - "Followed by price falling back" is tested only over the next one day. - The position jumps from flat to short when the volume condition opens the regime, because the condition is the idea itself.  

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

### opus (0.2212 USD)

Untestable: The idea needs two coins at once: bitcoin's past move as the signal and altcoin returns as the outcome, but the config sees one coin at a time and the test runs only on BTC/USDT, so no altcoin is traded. Bitcoin's own past move cannot stand in for the altcoins' lagged response the idea is about.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.2396 USD)

Untestable: The idea compares RSI at the current price high with RSI at the previous price high. No component in the catalogue remembers RSI at earlier price peaks or compares two peaks, and the config has no product or "and" in the forecast. The nearest thing is the close's place in its range (Donchian) combined with the current RSI level, which drops that peak-to-peak comparison and instead tests whether RSI levels or range extremes predict moves, which the brief explicitly excludes.  
