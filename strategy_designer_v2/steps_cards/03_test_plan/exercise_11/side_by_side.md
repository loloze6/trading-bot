# Exercise 11: side by side

Prompt: `system_prompt_used.md` (exercise 10 plus the turning-point line). Opus: the seven fixed ideas and the five other divergence ideas of step 2, exercise 3.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2722 USD)

Forecast: Use the 14-bar Wilder RSI on daily closes, through RSIPullbackComponent (period 14), whose raw value is (50 − RSI) × 0.4. Then apply these steps in order: 1. Standardise it against its own past 60 values (min_periods 20). An average deviation from 50 maps to about 10 forecast points, capped at ±20. 2. Clip at a maximum of 0, so only RSI above 50 counts and gives a short. RSI at or below 50 gives a forecast of exactly 0. 3. Apply signed_power with exponent 2 and pivot 10. Mild readings just above 50 then give near-zero shorts. Readings far above 50 give shorts that grow with the square of the standardised distance, up to the −20 cap (200% short). The forecast is never positive. It is zero when RSI ≤ 50 and grows more negative the higher RSI is pushed.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Confirm: Take the bars whose forecast is in the most negative 20% of all non-zero forecasts, pooled over 3 coins × 6 windows. Over the next 5 bars, their mean close-to-close return must be below the unconditional mean 5-bar return of all bars by a t-statistic of −2 or lower. Overlap is removed by counting each run of consecutive qualifying bars once, using its first bar. The same sign must hold in at least 2 of the 3 coins. Supporting check: the Spearman correlation between the forecast and the next 5-bar return, sampled every 5th bar, is positive.  
Reject: The 5-bar forward return after the most negative 20% of forecasts is at or above the unconditional mean 5-bar return, which would mean continuation or no effect. Or it is below that mean in fewer than 2 of the 3 coins.  
Inconclusive: The difference is negative but its t-statistic is between −2 and 0. Or the result is significant in the pooled sample but not in at least 2 coins. Or there are fewer than 30 non-overlapping extreme episodes in the pooled sample.  
Deviation: The idea says the reversal comes "after RSI reaches a high extreme". The config tests "while RSI is above 50, short in proportion to the squared standardised distance above 50". The position is held during the elevated reading and shrinks as RSI falls, rather than starting at the extreme and being held for a fixed number of bars afterwards. Moderate readings above 50 carry small shorts instead of none. "Extreme" is relative to each coin's last 60 RSI readings, not a fixed level such as 70.  

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

### opus (0.0620 USD)

Forecast: Take RSI(14), the Wilder RSI on daily closes. The component outputs (50 − RSI) × 0.4, and this is flipped so it reads (RSI − 50) × 0.4. That value is standardised: divided by the mean absolute value of its previous 60 values and multiplied by 10, capped at ±20. It is then passed through signed_power with exponent 2 and pivot 10, so moderate readings shrink smoothly toward 0 and extreme readings grow. Finally it is clipped at a minimum of 0. The forecast is therefore zero whenever RSI ≤ 50. It is positive (long) when RSI > 50, and grows with the square of how far RSI sits above 50 compared with its recent typical distance. The largest long positions come when RSI is at a high extreme (about 70 and up). It is never negative.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Confirm: Horizon 5 bars. The main measure, before costs, uses all 3 coins × 6 windows pooled, taking non-overlapping samples (at most one sample every 5 bars per coin). From the recorded RSI component value it compares two groups: the mean 5-bar forward close-to-close return after high-extreme bars (raw value ≤ −8, i.e. RSI ≥ 70) and the mean after neutral bars (raw value between −4 and +4, i.e. RSI 40–60). The idea is confirmed if the high-extreme mean exceeds the neutral mean by at least +1.0%, with t ≥ 2. This needs at least 30 non-overlapping extreme samples, and the difference must be positive on at least 2 of the 3 coins. The supporting check is that the strategy's return per unit of average exposure exceeds the coin's buy-and-hold daily return.  
Reject: The idea is rejected if the pooled difference (high-extreme minus neutral 5-bar forward return) is ≤ 0 with at least 30 non-overlapping extreme samples. A significantly negative difference (t ≤ −2) would further point to reversal rather than continuation.  
Inconclusive: The test is inconclusive in any of these cases: a positive difference below +1.0%; a difference with t < 2; fewer than 30 non-overlapping extreme samples; or a positive result on only one coin.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50". The position is sized by the squared distance of RSI above 50, relative to its last 60 bars, so a reading near 70 counts as extreme only relative to recent RSI behaviour. Low extremes are not traded.  

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
                "op": "signed_power",
                "params": {
                  "exponent": 2
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

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus (0.0571 USD)

Forecast: One graded, long-only trend reading on daily bars, using the classic 50/200 "golden cross" pair. The raw value is the spread between the two simple averages: (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own past 200 values (min_periods 50): the latest spread is divided by the mean absolute spread of the previous 200 bars and multiplied by 10, with a cap of ±20. It is then clipped at 0. The forecast is positive while SMA50 is above SMA200, which is the state that follows an upward cross. It grows as the short average pulls further above the long one. It is zero while SMA50 is at or below SMA200, so a downward cross closes the position.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Confirm: Horizon: 20 bars. Each window is cut into non-overlapping 20-bar blocks, so overlapping returns are counted once. For each block, record BTC's forward return from the forecast at the block's first bar, pooled over all 6 windows. The idea is confirmed if two things hold. First, the mean forward return of blocks that start with a forecast above 0 exceeds that of blocks that start flat by at least 2 percentage points, with a Welch t-stat of at least 2 and at least 8 blocks on each side. Second, as a supporting check, the share of positive long blocks is higher than the share of positive flat blocks.  
Reject: The idea is rejected if long blocks average no more than flat blocks (difference ≤ 0), or if long blocks are positive less often than flat blocks. The second case means that moves after an upward cross reverse and the cross marks exhaustion.  
Inconclusive: Either side has fewer than 8 blocks. Or the difference is positive but below 2 points, or has a t-stat below 2.  
Deviation: The idea says "after an upward cross". The config tests "while SMA50 is above SMA200", sized by how far apart the averages are. The largest positions therefore come well into an established trend, not at the cross itself. Only the long side is tested; the brief's downward cross is used only as the exit. Settings are the 50/200 convention, so with 122-bar windows there are few crosses and most evidence comes from states inherited from the warm-up.  

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

### opus (0.0529 USD)

Forecast: The 50-day simple moving average minus the 200-day simple moving average, as a percent of the 200-day average. Each bar's value is divided by the mean absolute value of the 200 values before it, times 10 and capped at ±20, then clipped at 0 below. The forecast is positive while the 50-day SMA is above the 200-day SMA, which is the stretch after an upward cross. It is zero while the 50-day SMA is below, which is the stretch after a downward cross. It grows continuously as the 50-day average pulls further above the 200-day average. It is never negative.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Confirm: Horizon is 1 bar (the next day's close-to-close BTC return), so no returns overlap. Pool all 6 windows. The idea is confirmed if two things hold. First, the mean next-bar return on bars with forecast > 0 exceeds the mean next-bar return on all bars by an amount with t-stat ≥ 2. Second, as the supporting check, the share of up days on forecast > 0 bars is higher than the share on all bars.  
Reject: The idea is rejected if the pooled mean next-bar return on forecast > 0 bars is at or below the mean over all bars. This applies when both the forecast > 0 bars and the forecast = 0 bars number at least 60. That result means that being in an up-cross stretch adds nothing over holding the coin, or that the stretch is followed by reversal.  
Inconclusive: The test is inconclusive in two cases. One is a positive difference with t-stat below 2. The other is fewer than 60 pooled bars in either state (forecast > 0 or forecast = 0), since crosses of the 50/200 averages are rare in 6 windows of about 122 days.  
Deviation: The idea is a binary state: in an up-cross stretch or not. The config tests it as a position that is sized by how far the 50-day SMA sits above the 200-day SMA. The criterion judges only the state (forecast > 0 versus all bars), not the size. The idea names no averages, so the conventional daily 50/200 SMA pair stands in for "short" and "long". Down-cross stretches are held flat, not short, because the idea speaks only of the upward stretch.  

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

### opus (0.0686 USD)

Forecast: On each daily close, first check the condition. The bar must close above the previous close, on volume below its 20-day average (the average includes the current bar). On any other bar the forecast is 0 (flat). On a qualifying bar the forecast is short, sized by how sharp the rise was. The rise is today's 1-bar percent change in the close, divided by the mean absolute 1-bar change of the previous 60 days and multiplied by 10. That gives about 10 for a typical daily move, capped at 20. Next it goes through signed_power with exponent 2 and pivot 10, so small rises give a very small short and sharp rises a large one: a 0.5x-typical rise gives 2.5, a typical rise gives 10, a 1.5x-typical rise gives 22.5. The sign is then flipped to short and the forecast is clipped to at most 0. The combined forecast is clipped to -20 overall. The position is held only for the bar after the qualifying close, unless the next bar qualifies again.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Confirm: The horizon is 1 bar (the next day). Pool all active bars across the 6 windows; each next-day return counts once, so none overlap. Before costs, the position-weighted mean next-day BTC return after active bars must be below the mean daily return over all bars of the same windows, with a t-statistic of 2 or more on at least 30 active bars. Supporting check: within the active bars, the strategy's next-day return grows with the size of the short (positive slope on |forecast|).  
Reject: Before costs, the position-weighted mean next-day return after active bars is equal to or above the all-bar mean daily return (t-statistic of 0 or more). Equivalently, the short's pooled return relative to the all-bar baseline is zero or negative.  
Inconclusive: Two cases neither confirm nor reject. The first is fewer than 30 active bars. The second is a shortfall below the all-bar mean that has the right sign but a t-statistic between 0 and 2.  
Deviation: Four parts of the idea change in the config. - "Sharp" is not a threshold. Every up bar on below-average volume is traded, and sharpness only sets the size through signed_power. - "Unusually low volume" becomes "below the 20-day average". - "Followed by falling back" is tested only over the single next day, because the short exists only while the qualifying bar's condition holds. - The move is a one-day close-to-close change, not a multi-day rise.  

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

### opus (0.0186 USD)

Untestable: The idea needs bitcoin's past returns to forecast an altcoin, but the config sees only one coin at a time and the only coin in this test is BTC/USDT. No altcoin price is available, and a config cannot read another coin's bars. So the lead-lag relation between bitcoin and smaller coins cannot be built or measured here.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0223 USD)

Untestable: The idea compares RSI at the current price high with RSI at the previous price high, and the config keeps no memory of past turning points, so it cannot recall the RSI value at the earlier high. A proxy such as "price near the top of its range while RSI is below its own average" would drop the high-to-high comparison that defines the divergence.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0224 USD)

Untestable: The idea compares RSI at today's new price low with RSI at the previous price low. The config has no memory of past turning points, so it cannot recall the earlier low or the RSI value there. No catalogue component measures price-RSI divergence, and approximations such as "close at the bottom of its range while RSI is not oversold" would drop the higher-low comparison the idea is about.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0252 USD)

Untestable: The idea compares the RSI high at today's new price high with the RSI high at the previous price high, so it needs the RSI value at an earlier turning point. The config keeps no memory of past turning points and has no component for an RSI rolling high or RSI range position. The closest substitute would rank RSI against its own history with `percentile`, but that cannot be combined with `standardise`, which must be the only history op. Dropping that comparison would remove the divergence the idea is about.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0225 USD)

Untestable: The idea compares RSI at today's new price low with RSI at the earlier price low, and the config has no memory of past turning points. The catalogue also has no component that places RSI within its own recent range, so a config would have to drop the higher-RSI-low comparison that the idea is about.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0236 USD)

Untestable: The idea needs RSI at today's new price high compared with RSI at the earlier price high (a lower RSI high), and the config keeps no memory of past turning points, so it cannot hold the RSI value from the earlier high. Substitutes such as "close at the top of its range while RSI is below 50" drop the high-to-high comparison that defines the divergence, so they would not test this idea.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.0215 USD)

Untestable: The idea needs RSI at the current new price low compared with RSI at the earlier price low, and the config keeps no memory of past turning points. It can see that price is at a new low (Donchian position) and what RSI reads now, but not whether RSI's low is higher than its value at the previous low, so the divergence condition the idea is about cannot be built.  
