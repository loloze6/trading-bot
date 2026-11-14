# Exercise 1: side by side

Prompt: `system_prompt_used.md`. References: `../helper/reference/`. Ideas and briefs: `inputs/`. One call per idea and model.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2531 USD, 1 attempt)

Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: For each coin, take the bars with the largest short positions (forecast at -10 or lower, meaning RSI is well above its usual reading). Over the next 1 to 10 days, the before-cost close-to-close return after those bars is lower than the coin's average return over all bars. This should hold in at least two of BTC, ETH and BNB. Across bins of forecast size, the short's before-cost gain relative to holding the coin should grow as the position gets larger.  
Reject: In at least two of the three coins, returns after the largest short positions are equal to or higher than the coin's average return over all bars (no difference or continuation), or the gain relative to holding does not grow with position size.  
Deviation: The idea says "after RSI reaches a high extreme, price falls back over the following bars." The config tests something different: while RSI(14) is above 50, it holds a short sized by how far RSI is above 50. The signed_power step makes that short small near 50 and large at the extremes. The position shrinks as RSI falls, and nothing holds it for a fixed number of bars after the extreme reading. Only the high-RSI (reversal-down) side is tested; low-RSI readings give a flat position.  

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
            "id": "rsi_high_fade",
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

### sonnet (0.1271 USD, 1 attempt)

Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: On each coin, the daily returns after the most negative forecasts (the largest shorts, highest RSI) are clearly below the coin's average daily return over the whole period, and the short position's gross gain per bar rises as the position gets larger. It should also beat holding the coin, measured before costs.  
Reject: Returns after the largest shorts are equal to or above the coin's unconditional average, or the short's gross gain is flat or falls as position size grows. Then the high-RSI reading shows no reversal (continuation or nothing), and the short-only portfolio does no better than holding.  
Deviation: "Price falls over the following bars after an extreme" becomes "hold a short while RSI(14) is above 50, sized by how high it is against its own recent history and amplified toward extremes by squaring, fading as RSI falls back". It does not wait for a discrete extreme event or hold for a fixed number of bars, and it takes no long position when RSI is low, since the idea concerns only the high extreme.  

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
        ],
        "trending": null,
        "mean_reversion": null,
        "chop": null
      }
    }
  },
  "aux_feeds": []
}
```

## 001-03_rsi-high-extreme-continuation

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

### opus (0.2464 USD, 1 attempt)

Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: On each of BTC, ETH and BNB, before costs, the mean next-bar coin return on bars where the forecast is in its top decile (the highest RSI readings) is above the mean next-bar return on bars where the forecast is below 2 (RSI near or below 50). The strategy's gross return must also beat buy-and-hold scaled to the strategy's average allocation.  
Reject: On all three coins, the top-decile forecast bars are followed by next-bar returns equal to or below those after neutral bars, which would mean no effect or reversal. The strategy's gross return must also fail to beat exposure-matched buy-and-hold.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI(14) is above 50, a long position that grows with the square of how far RSI sits above 50, relative to its last 60 bars". The test holds the position bar by bar and lets it fade as RSI falls back, rather than measuring a fixed horizon after a threshold event. Low-RSI extremes are left out: the forecast is flat below RSI 50.  

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

### sonnet (0.1203 USD, 1 attempt)

Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: On each coin, the bars with the largest long positions (RSI far above 50, top decile of the forecast) are followed by next-1 to next-10-day returns that are clearly higher than the returns after bars with zero or small positions. The portfolio's gain per unit of position should also rise with position size, and the strategy should beat simply holding the coin before costs, on all three coins.  
Reject: Returns after the largest positions are no higher than after zero or small positions, or are lower (reversal), so gains do not grow with position size. The strategy is also no better than holding the coin before costs, or the result holds for only one of the three coins.  
Deviation: The config trades only the high side. Positions are long, growing with how far RSI(14) is above 50, and squared so the extremes get most of the weight. Flat when RSI is below 50. "Extreme" becomes a graded size rather than a threshold event, and the "neutral" comparison is the near-zero positions. Holding is continuous while RSI stays high, not just once after the extreme is reached.  

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

### opus (0.2428 USD, 1 attempt)

Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: The mean next-bar return of BTC on bars where the forecast is above 0 (SMA50 above SMA200) is higher than its mean return over all bars, before costs. The strategy's return per unit of average exposure also beats buy-and-hold over the same period. Within those long bars, next-bar returns rise with the size of the forecast, so that the top third of forecasts earns more than the bottom third.  
Reject: The mean next-bar return while the forecast is above 0 is no higher than the unconditional mean, or the return per unit of exposure does not beat buy-and-hold. It is also rejected if returns fall as the forecast grows, with the largest spreads followed by reversals, which would mean the cross marks exhaustion and not the start of a trend.  
Deviation: "After the short average crosses above the long one" becomes "while SMA50 is above SMA200, long in proportion to the percent gap between them". This changes the test in four ways. The position is small right at the cross and grows as the gap widens, so the test weights the established part of the trend more than the bars just after the cross. The idea gives no periods, so 50/200, the conventional daily golden cross, is assumed. Only the upward cross is tested: the forecast is clipped at 0, so there is no short side after a downward cross. Results are read on all bars above the cross, not on fixed windows after each cross event.  

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

### sonnet (0.1165 USD, 1 attempt)

Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: Forecast-weighted returns (forecast at bar close times the next bar's return) are positive, and cumulative gains rise with the size of the positive forecast: the top tercile of positive forecasts (strongest uptrend spread) is followed by higher mean next-bar and next-10-bar returns than the bottom tercile, and than the coin's unconditional average (buy-and-hold). Judged before costs.  
Reject: Mean returns after large positive forecasts are no higher than the coin's unconditional mean, or are lower (reversal), or the strategy's gross return does not beat holding the coin and shows no rise in gains with forecast size.  
Deviation: "After the cross" becomes "while the 50-day SMA is above the 200-day SMA, scaled by the size of the spread". The position is held at all times the spread is positive, not only after the cross event, and a negative spread gives a short position, which the idea (upside only) did not state. The test measures trend persistence across the whole spread, not just the bars right after the crossing. Price-crosses-average is not tested. The 50/200 periods come from convention and not from the brief.  

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
              }
            ]
          }
        ],
        "trending": null,
        "mean_reversion": null,
        "chop": null
      }
    }
  }
}
```

## 002-05_sma-up-regime-positive-drift

**The idea**

Idea: Over the stretch from an upward cross of the short average over the long average until the next downward cross, price rises more often and further than over random stretches of the same length.  
Consequence: The uptrend begun by an upward cross lasts until the opposite cross ends it.

### opus (0.2427 USD, 1 attempt)

Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: The test confirms the idea if, before costs, BTC's mean next-day return on bars with a positive forecast (the up-cross stretches) beats its mean next-day return over all bars. The strategy's return per unit of average exposure must also beat buy-and-hold, and next-day returns should not shrink as the forecast grows.  
Reject: The test rejects the idea if, on positive-forecast bars, the mean next-day return is no higher than the unconditional mean and the strategy's return per unit of exposure does not beat buy-and-hold. It also rejects the idea if returns fall as the spread widens, which would mean the cross marks exhaustion rather than a trend.  
Deviation: The idea's on/off state ("between an up-cross of SMA50 over SMA200 and the next down-cross") becomes "long in proportion to how far SMA50 sits above SMA200, flat when it is below". Days just after a cross get a small position and days deep in the stretch get a large one, so the test weights the middle and late part of each stretch, not the stretch evenly. The 50/200 periods are the conventional golden-cross choice, because the source gives no lengths. The comparison is against the unconditional mean and buy-and-hold, not against randomly placed stretches of equal length.  

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

### sonnet (0.1201 USD, 1 attempt)

Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: On bars with a positive forecast (SMA50 above SMA200), the mean next-bar BTC return is clearly higher than the mean over all bars, with a higher share of up bars. Bar gains also rise with the size of the forecast (top-tercile forecast bars gain more than bottom-tercile ones). Before costs, the portfolio's return per unit of exposure beats buy-and-hold.  
Reject: Next-bar returns on positive-forecast bars are no higher than the all-bar mean, or are lower, which would show reversal after crosses. Gains do not grow with forecast size, or the portfolio does not beat buy-and-hold per unit of exposure before costs.  
Deviation: The config uses the continuous, standardised SMA50−SMA200 spread on every bar, not the cross event and the stretch between crosses. The position therefore scales with the spread, is not constant between crosses, and tapers toward zero as the averages converge before a cross. The spread also turns negative after a downward cross, giving a short position. The idea as written only claims upward stretches rise, and treats a downward cross as the end of the trend. The test therefore also requires downward stretches to fall.  

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

### opus (0.2564 USD, 1 attempt)

Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Across the days that follow a short, BTC's average close-to-close return is below its average daily return over all days, so the shorts gain against holding the coin. Larger shorts, set by larger thin-volume up days, should be followed by larger declines.  
Reject: The day after a thin-volume up move, BTC's return is at or above its average daily return, so the short loses relative to holding. The same verdict applies if the shorts' P&L does not grow with position size, meaning bigger thin-volume rallies are not followed by bigger give-backs.  
Deviation: The short is opened at the close of the up day itself and held for one day only: it is closed whenever the next bar is not also a thin-volume up day. Any reversion that comes later is therefore not captured. "Unusually low volume" becomes volume below its 24-day average, with the current day included in that average. "Sharp" is graded, not a threshold: the day's return is scaled against the last 60 days and squared, with signed_power damping small moves. The brief's contrast with high-volume moves, which should hold or continue, is not tested here.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "thin_up",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 24,
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

### sonnet (0.1282 USD, 1 attempt)

Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Across the bars with a short position, the next-day BTC return is negative on average, and below the coin's unconditional average daily return. Gains before costs also grow with position size, so the biggest shorts (largest low-volume up-moves) earn the most.  
Reject: Next-day returns after the held shorts are zero or positive, or no lower than the coin's average daily return. The short's gross P&L is not positive, or it does not rise with position size. This would mean low-volume rises are not given back.  
Deviation: The config uses a regime of "up day with volume at least 20% below its 20-day average", which stands in for "unusually low volume". The size of the move is the one-day return, and the short grows with it. The position exists only on bars meeting that condition and goes flat on the next bar that does not, so "falls back afterwards" becomes mainly the next bar's return. Partial give-back over several days is not measured. The high-volume half of the brief (moves that hold or continue) is not tested here, because this single config trades only the low-volume leg.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "vx",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 20,
          "scaling_factor": 1.0
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
              "id": "vx",
              "op": "lte",
              "value": -0.2
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
            "id": "fade_move",
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

### opus (0.2218 USD, 1 attempt)

Untestable: The idea forecasts altcoin returns from bitcoin's earlier move, so it needs bitcoin's price as an input while trading a different, smaller coin. The config sees only one coin's bars, and the test runs on BTC/USDT alone, so neither the leading coin's move nor the lagging altcoin's response can be measured.  

### sonnet (0.1117 USD, 1 attempt)

Untestable: The idea is about altcoins responding to an earlier bitcoin move, which needs both bitcoin and altcoin prices. The config sees only one coin at a time (here BTC/USDT), has no altcoin series, and the catalogue has no cross-coin component. BTC's own past returns cannot show whether altcoins lag it.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.3035 USD, 1 attempt)

Config: 005-01_bearish-rsi-divergence-reversal_config.json  
Confirm: The idea is confirmed if, across the bars where price sits in the top quarter of its 20-day range, the size of the short predicts the fall that follows, on at least two of the three coins and before costs. Concretely, the mean 10-day forward return after bars with forecast ≤ -5 (new high with weak RSI) must be negative. It must also be lower than both the forward return after near-high bars with forecast above -2 (new high with strong RSI) and the coin's unconditional 10-day return, so that the strategy's equity on active bars rises while buy-and-hold over the same bars falls.  
Reject: The idea is rejected if forward returns after the strongest shorts are no lower than after near-high bars with strong RSI, or no lower than the coin's unconditional drift. That means pre-cost P&L on active bars is flat or negative, or does not grow with the size of the short.  
Deviation: The config never finds the previous price peak or compares RSI with its value there; the catalogue has no swing-point detection. "New high with RSI lower than at the prior high" becomes "while the close is in the top quarter of its 20-day closing range (a regime), short more the weaker 14-day RSI is relative to its own recent scale". The short is zero when RSI is at its cap of strength and about -13 when RSI is below 50. The short is held only while price stays near the high, so a retrace deeper than the top quarter of the range is not captured. Only bearish divergence at highs is tested: the brief's mirror case at lows is excluded, and the forecast is never positive.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "range_pos",
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
        "regime": "mean_reversion",
        "any_of": [
          [
            {
              "id": "range_pos",
              "op": "gte",
              "value": 10.0
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
            "id": "short_offset",
            "class": "strategies.strategy_components.BuyAndHoldStrategy",
            "params": {},
            "weight": 2.0,
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
          },
          {
            "id": "rsi_strength",
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

### sonnet (0.1346 USD, 1 attempt)

Config: 005-01_bearish-rsi-divergence-reversal_config.json  
Confirm: On bars where the forecast is negative (close in the top 5% of its 20-day range with RSI below 50), the largest short positions should be followed by 5 to 10 day returns clearly below that coin's unconditional average return. Short-side gains should also grow with position size across position-size buckets, and be positive before costs on BTC, ETH and BNB.  
Reject: Returns after the largest short positions are equal to or above the coin's unconditional average, or the short side loses money before costs, so that bars at new highs with weak RSI do no worse than other bars. Gains that do not grow with position size also reject it.  
Deviation: The config does not compare the RSI at the new high with the RSI at the previous price high. It tests "close in the top 5% of its 20-day range while RSI sits below 50, shorting more as RSI weakens". A new high is approximated by the range position, and divergence by absolute RSI weakness. The position is held only while the condition lasts and is flat otherwise, and it is short-only (only the bearish divergence is tested). The reversal is measured as forward returns and the position, not as a retracement of the run-up.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "range_pos",
        "class": "strategies.strategy_components.DonchianBreakoutComponent",
        "params": {
          "period": 20
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
              "id": "range_pos",
              "op": "gte",
              "value": 18
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
            "id": "rsi_weak",
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
                  "max": 0.0
                }
              }
            ]
          }
        ]
      },
      "unknown": null,
      "trending": null,
      "chop": null
    }
  }
}
```
