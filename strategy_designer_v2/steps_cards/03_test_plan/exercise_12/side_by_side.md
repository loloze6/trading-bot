# Exercise 12: side by side

Prompt: `system_prompt_used.md` (exercise 10 plus the turning-point line). Opus: the seven fixed ideas and the five other divergence ideas of step 2, exercise 3.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0433 USD)

Forecast: Take the 14-bar Wilder RSI on daily closes and measure how far it sits above 50 as (50 − RSI). Put that on the scale of its own past values: divide by the mean absolute value of the previous 60 readings and multiply by 10, capped at ±20. Then apply a smooth dead zone, 10 × sign × (|v|/10)², so ordinary readings shrink toward 0 and high extremes are amplified. Finally cap the result at 0 from above. The forecast is therefore never positive. It is zero whenever RSI is at or below 50. It is negative (short) while RSI is above 50, and the short grows with the square of how far RSI is above 50: a reading twice as stretched as usual gives a short four times as large, up to the −20 combined cap.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Confirm: Pool all three coins and all six windows. Take the bars where the short position is in the largest decile, and count the coin's 5-bar forward return only once per non-overlapping 5-bar block. The mean of those returns must be below the mean 5-bar forward return over all bars, by a margin with t ≤ −2. Supporting check: the same sign holds on at least 2 of the 3 coins.  
Reject: Under the same measure, the mean 5-bar forward return after the largest-decile shorts is at or above the all-bar mean (t ≥ 0). That would mean high RSI extremes are followed by no retracement, or by continuation.  
Inconclusive: The difference is negative but with −2 < t < 0. Also inconclusive: it reaches t ≤ −2 pooled but holds on only one coin.  
Deviation: The idea says the reversal comes after RSI reaches an extreme. The config tests something different: it holds a short while RSI is above 50, sized by how stretched the reading is, and the short shrinks as RSI falls back toward 50 rather than lasting a fixed number of bars. Moderate high readings also carry small shorts, damped by the squared dead zone rather than excluded.  

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

### opus (0.0529 USD)

Forecast: The forecast is the 14-bar Wilder RSI turned into a momentum reading, long only, with extremes emphasised. Start with RSI − 50, which is RSIPullbackComponent at period 14, negated. Divide it by the mean absolute value of its own previous 60 daily values and multiply by 10, capped at ±20. Clip it at 0, so it is zero whenever RSI ≤ 50; the brief does not limit the side, but this idea is only about high readings. Then apply signed_power with exponent 2 and pivot 10, so the position grows with the square of the standardised strength. Near-neutral readings just above 50 give almost no position, typical readings give about 10, and high extremes (RSI near 70 or above) give a large long, up to the +20 cap.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Confirm: Pool all three coins and all windows. Compare the coin's 5-bar forward close-to-close return after high-extreme bars (recorded RSI ≥ 70, raw component value ≤ −8) with the same return after neutral bars (RSI 40–60). Count only non-overlapping 5-bar blocks, so each block enters once. The idea is confirmed if the extreme mean exceeds the neutral mean by at least 1.0 percentage point, with t ≥ 2, from at least 30 non-overlapping extreme observations. Supporting check: the difference is positive in at least 2 of the 3 coins. All of this is before costs; comparing with neutral bars removes the market's own drift.  
Reject: The idea is rejected if the pooled difference (extreme minus neutral 5-bar forward return) is zero or negative, with at least 30 non-overlapping extreme observations. A difference at t ≤ −2 would point to reversal rather than continuation.  
Inconclusive: The test is inconclusive if the difference is positive but below 1.0 percentage point or has t < 2. It is also inconclusive if fewer than 30 non-overlapping extreme observations exist, or if the pooled result is positive but only 1 of the 3 coins agrees.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, with a long sized by the squared distance". The config therefore holds small longs at moderate readings and its largest longs while RSI stays extreme, not for a set number of bars after the extreme. Low extremes are not traded. The extreme is also measured relative to the RSI's previous 60 daily values, not against a fixed level of 70.  

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

### opus (0.0498 USD)

Forecast: The 50-bar simple moving average of the daily close minus the 200-bar simple moving average, as a percent of the 200-bar SMA: (SMA50 − SMA200) / SMA200 × 100, from EMASpreadComponent with average "sma". This spread is standardised against its own past 200 values (window 200, min_periods 50), so its average absolute size is about 10, capped at 20. It is then clipped at 0 below. The forecast is positive and grows with the spread while the short average is above the long one. It is zero while the short average is at or below the long one. It is never negative, because this idea is only about the upward cross. The position is forecast / 10 of equity, long only, and it scales continuously with how far the short average has pulled above the long one.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Confirm: The test pools all 6 windows and uses a horizon of 20 bars. It splits the record into non-overlapping 20-bar blocks, each starting at a block-start bar, so overlapping returns are counted once. The main measure is the mean forward 20-bar BTC return after block-starts where the forecast is > 0, minus the mean forward 20-bar return after all block-starts (random points, which is the buy-and-hold baseline). The idea is confirmed if this excess is at least +1.5 percentage points with a t-statistic of at least 2, and if the supporting check also holds: the share of positive 20-bar returns after in-position starts beats the unconditional share by at least 5 points.  
Reject: The idea is rejected if the excess forward 20-bar return after in-position block-starts is zero or negative versus all block-starts. It is also rejected if the in-position hit rate is no higher than the unconditional one. A significantly negative excess (t ≤ −2) additionally means the cross marks exhaustion, not persistence.  
Inconclusive: The result is inconclusive if the excess is positive but below +1.5 points, or if its t-statistic is below 2. It is also inconclusive if the forecast is > 0 on fewer than 8 or more than 28 of the roughly 36 non-overlapping block-starts, which leaves too few in-position or out-of-position blocks to compare.  
Deviation: "After the short SMA crosses above the long SMA" becomes "while the short SMA is above the long SMA, sized by how far above". This means the test credits the whole time the averages stay crossed, not only the bars just after the cross event. Because of that sizing, positions are smallest right at the cross and largest well into the trend. The settings 50/200 SMA come from the daily-bar golden-cross convention, since the brief gives none. Downward crosses are not tested.  

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

### opus (0.0459 USD)

Forecast: Uses the 50-day and 200-day simple moving averages of the daily close, the conventional daily "golden cross / death cross" pair. The raw value is the spread (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own last 200 values, so a spread of typical size gives about +10 (100% long) and the forecast is capped at +20. Negative values are clipped to 0. The forecast is therefore positive, and grows with how far SMA50 sits above SMA200, on every bar from an upward cross until the next downward cross. It is exactly 0 (flat) from a downward cross until the next upward cross. It is never short.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Confirm: The horizon is 1 bar (next-day close-to-close return; each bar is counted once, with no overlap), pooled over the 6 windows, before costs. Two results together confirm the idea. First, the mean next-day return of BTC on bars with forecast > 0 exceeds the mean next-day return on all bars (buy-and-hold) by a t-statistic ≥ 2. Second, the supporting check holds: the share of up days on forecast > 0 bars beats the share on all bars, and is ≥ 52%.  
Reject: The idea is rejected if the mean next-day return on forecast > 0 bars is at or below the all-bar mean. It is also rejected if the share of up days on forecast > 0 bars is no higher than on all bars. Either result means the up-cross stretches do no better than random stretches, or they reverse.  
Inconclusive: Three results neither confirm nor reject. The excess mean return is positive but its t-statistic is below 2. The two measures disagree in sign. Fewer than 100 bars across all 6 windows carry forecast > 0, or fewer than 100 bars carry forecast = 0, too few for a fair comparison.  
Deviation: The holding is not a fixed position from cross to cross. Its size grows with the width of the SMA50 − SMA200 gap: it is small just after a cross and larger as the gap widens. The criterion still judges the whole stretch where the forecast is positive. Only the long (upward-cross) stretch is tested. The brief's alternative trigger, "price crosses the long average", is not tested.  

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

### opus (0.0665 USD)

Forecast: The forecast is active only on a "thin up-move" bar. That is a daily bar that closes above the previous close on volume below its own 20-bar average, with the average including the current bar. On every other bar the forecast is 0 (flat). On an active bar the forecast is short and graded by the size of the day's rise. Take the one-bar percent return, PriceEvolutionComponent with period 1, divide it by the mean absolute one-day return of the previous 60 bars and multiply by 10 (capped at 20). Then negate it and clip it at 0 so it never goes long. A normal-sized up day on thin volume gives about -10 (100% short). A rise twice the usual size gives -20. A tiny rise gives close to 0. The position is held for that one bar and closed at the next close unless the next bar is again a thin up-move.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Confirm: Horizon is 1 bar (the next day), so each event counts once. Pool all active bars across the 6 windows, expecting about 150 or more events. Confirmation requires two things: - The position-weighted mean next-day return of the strategy, minus what holding the coin earned on those same days, is positive with a t-statistic of at least 2. - Supporting check: events with positions at or above the median size show a larger next-day give-back than the smaller ones.  
Reject: Rejection is either of two results, before costs: - The next-day return after thin up-moves, weighted by position, is at or above BTC's average next-day return over all bars, so there is no give-back. - The strategy's pooled return on active bars is zero or negative.  
Inconclusive: The excess return has the right sign but a t-statistic below 2. Or there are fewer than 30 active bars in total. Or the main measure confirms while larger positions show no larger give-back.  
Deviation: "Unusually low volume" becomes "volume below its 20-bar average", an on/off condition, not a graded measure of how thin the volume is. "Sharp" is graded by position size, not imposed as a threshold. "Followed by falling back" is tested only over the next day, because the position must close once the condition ends. The volume half of the brief, that heavy-volume moves hold, is not tested here.  

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
    "vetoes": [
      {
        "id": "thin_up",
        "transforms": [
          {
            "op": "identity"
          }
        ],
        "rules": [
          {
            "op": "lt",
            "value": 0.0
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
  },
  "aux_feeds": []
}
```

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.0142 USD)

Untestable: The idea needs bitcoin's past return as the signal and an altcoin's later return as the outcome, but the config sees only one coin's bars at a time and the test runs only on BTC/USDT. No config can read bitcoin's move while trading an altcoin, and a BTC-only run contains no altcoin whose catching-up could be measured.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0164 USD)

Untestable: The idea compares RSI at the new price high with RSI at the previous price high. That needs the config to remember where the earlier swing high was and what RSI read there, and the config has no memory of past turning points. Every catalogue component reads only its current window, so the "lower high in RSI than at the previous high" comparison, which is the idea itself, cannot be built. A proxy such as "close near the top of its range while RSI is low" would drop that comparison.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0158 USD)

Untestable: The idea compares RSI at the current price low with RSI at the previous price low, so it needs to remember an earlier turning point and the RSI value there, and the config cannot store either. The closest graded proxy, a close near the bottom of its range while RSI is not deeply oversold, drops the higher-low comparison that the idea is about.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0160 USD)

Untestable: The idea compares RSI at a new price high with RSI at the earlier price high, which is a comparison against a past turning point. The config has no memory of past turning points. The catalogue also has no component that measures where RSI sits relative to its own recent high, so the divergence itself cannot be built from it.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0181 USD)

Untestable: The idea compares the RSI at today's new price low with the RSI at the previous price low (a higher RSI low against a lower one), and the config keeps no memory of past turning points, so it cannot know the RSI value at the earlier low. The catalogue also has no RSI-range or RSI-low component. A weighted sum of where the close sits in its range and the RSI level would drop that low-to-low comparison, which is what the idea is about.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0157 USD)

Untestable: The idea requires checking that RSI at today's new price high is lower than RSI was at the previous price high. The config has no memory of past turning points, so it cannot look up RSI's value at an earlier high. Substitutes such as "price near the top of its range while RSI is moderate" drop the very comparison the divergence is defined by.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.0186 USD)

Untestable: A bullish divergence compares RSI at the current price low with RSI at the earlier price low it undercuts. The config keeps no memory of past turning points or of the indicator values at them, so it cannot tell whether RSI's low is higher than before. No catalogue component gives RSI's position within its own past range either. Any config built from these components would drop the RSI-versus-earlier-low comparison that is the idea, and would test only "price near its range low", which is a different idea.  
