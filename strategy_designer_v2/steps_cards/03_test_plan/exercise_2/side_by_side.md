# Exercise 2: side by side

Prompt: `system_prompt_used.md` (exercise 1 plus one horizon, an inconclusive line, no constant inside a regime). References: `../helper/reference/`. Ideas and briefs: `inputs/`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2534 USD, 1 attempt)

Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: The horizon is 5 bars. Take the bars whose forecast is in the most negative decile (the highest RSI readings). On at least 2 of the 3 coins, the coin's 5-bar forward return after those bars is below its unconditional mean 5-bar return, with a t-stat at or below -2. The gap is also wider than the one after bars with a forecast of zero or near zero (RSI at or below 50), measured before costs. As a cross-check, the strategy's 5-bar forward return per unit of short position grows with the size of the short position.  
Reject: On at least 2 of the 3 coins, the 5-bar forward return after the most negative forecast decile is at or above the coin's unconditional mean 5-bar return. That would mean no reversal, or continuation, after high RSI.  
Inconclusive: The three coins disagree in direction (for example one coin reverts while the others do not), or the excess forward return after the top decile has the expected sign but |t| < 2 on two or more coins.  
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, a short whose size grows with the square of RSI's standardised distance above 50". Moderate readings above 50 also hold small, damped shorts, and there is no fixed extreme threshold or hold period. Only the high-extreme (reversal-down) side of the brief is tested. Low readings stay flat.  

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

### sonnet (0.1287 USD, 1 attempt)

Config: 001-01_rsi-high-extreme-reversal_config.json  
Confirm: At a 5-bar horizon, on each of BTC, ETH and BNB, the mean forward 5-bar return after the largest short positions (top decile of |forecast|) is negative and below that coin's mean 5-bar return over all bars. The short-only portfolio, before costs, also gains on those bars, with gains growing from the smaller to the larger positions.  
Reject: On at least two of the three coins, the mean 5-bar forward return after the largest short positions is at or above the coin's all-bar mean, which is no reversal or continuation. Alternatively, the short positions lose money before costs, with losses growing with position size.  
Inconclusive: Results that differ by coin (one confirms, another rejects, the third is flat). Fewer than about 20 largest-position bars on a coin. A negative forward return that is not below the coin's all-bar mean (market drift only). A sign that appears at other horizons but not at 5 bars.  
Deviation: The config tests only the high side (RSI above 50, short), with no long on low RSI. "After the index reaches an extreme" becomes "while RSI is elevated, short in proportion to the squared standardised distance above 50". The position is held while the reading stays high, not triggered once on an event, and the size is relative to each coin's own recent RSI deviations rather than a fixed RSI level such as 70.  

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

### opus (0.2551 USD, 1 attempt)

Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: The horizon is 5 bars (5 days). Take the bars whose forecast is in that coin's top decile, which are the highest RSI readings. On at least 2 of the 3 coins, and with no coin showing the opposite, the mean 5-bar forward return after those bars must exceed both of these by more than one standard error: the mean 5-bar forward return after neutral bars (forecast above 0 but below the median of the positive forecasts), and the coin's unconditional mean 5-bar return. The strategy's return before costs must also beat buy-and-hold scaled to the strategy's average exposure.  
Reject: On at least 2 of the 3 coins, the mean 5-bar forward return after top-decile forecast bars is at or below the neutral-bar mean and the unconditional mean. A clear reversal, where the top-decile return falls below the neutral-bar return by more than one standard error, rejects the idea and points to the reversal reading.  
Inconclusive: The coins split in sign, or the top-decile minus neutral difference stays within one standard error on two or more coins.  
Deviation: "After RSI reaches a high extreme" is tested as a position held while RSI is above 50, growing with the square of RSI's distance above 50, so extremes dominate. There is no fixed threshold such as 70 and no explicit post-event window. The position is flat whenever RSI is below 50, so low extremes are not tested.  

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

### sonnet (0.1258 USD, 1 attempt)

Config: 001-03_rsi-high-extreme-continuation_config.json  
Confirm: On the daily record for each of BTC, ETH and BNB, the mean 5-bar forward return after the bars with the largest long forecasts (top decile of the forecast, i.e. high RSI) is clearly above the mean 5-bar forward return after bars with small positive forecasts (neutral RSI). Mean 5-bar gains also rise with the size of the position across forecast buckets. The before-cost portfolio return per unit of average exposure beats buy-and-hold of the same coin, in all three coins or in a clear majority.  
Reject: The mean 5-bar forward return after top-decile forecasts is at or below that after neutral bars, or is negative, so that gains do not rise with position size. Alternatively the before-cost portfolio does not beat buy-and-hold per unit of exposure, in most of the coins.  
Inconclusive: Top-decile bars beat neutral bars in only one or two coins, or by a margin within sampling noise (the top decile has few, heavily overlapping 5-bar windows). The idea is also inconclusive if the portfolio beats buy-and-hold only because it is flat in falling markets while the high-RSI forward returns show no difference.  
Deviation: "Reaches a high extreme" becomes "while RSI (14) is above 50, the position grows with the square of the RSI excess", i.e. a level and not an event, with no reference to the first touch of an extreme. The forecast is zero when RSI is at or below 50, so that there is no short side. Because the position is also nonzero at mild readings, "neutral" is read as small positive forecasts.  

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
            "id": "rsi_continuation",
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
        ],
        "trending": null,
        "mean_reversion": null,
        "chop": null
      }
    },
    "aux_feeds": []
  }
}
```

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus (0.2539 USD, 1 attempt)

Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: Horizon is 20 bars. Look at bars where the forecast is above 0, that is, where SMA50 is above SMA200. On those bars, the mean 20-bar forward return of BTC and the share of positive 20-bar forward returns must both exceed the same figures over all bars (random points). The gap in mean return must be at least 2 standard errors, counted on non-overlapping 20-bar blocks. Before costs, the portfolio must also beat exposure-matched holding, that is, the average allocation times buy-and-hold, over the same 20-bar blocks.  
Reject: The theory is rejected if any of these holds: - The 20-bar forward return on bars with a positive forecast is at or below the all-bar mean. - Its hit rate is no higher than the all-bar hit rate. - The 20-bar forward return after the first bars of each positive episode (the fresh upward crosses) is below the all-bar mean, meaning moves reverse after the cross. - The portfolio trails exposure-matched holding before costs.  
Inconclusive: These results neither confirm nor reject the idea: - Positive-forecast bars beat random points, but by less than 2 standard errors. - Mean and hit rate disagree. - The excess comes from only one or two of the roughly ten 50/200 upward crosses in the BTC daily history, too few episodes to separate trend persistence from a few large bull runs.  
Deviation: The idea says "after the short average crosses above the long one, for the following bars". The config tests something different: "while SMA50 is above SMA200, long in proportion to the gap between them". Three things change: - The position is largest well into a mature trend, not right after the cross. - The position stays on for the whole time the averages stay crossed, not for a fixed number of bars. - The short side of the brief (the downward cross) is left out, because the idea names only the upward cross.  

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

### sonnet (0.1177 USD, 1 attempt)

Config: 002-01_sma-upcross-upward-drift_config.json  
Confirm: Over a 20-bar (20-day) horizon, the forecast at each bar's close times the next 20-bar BTC return is positive, and the gain grows with position size: bars in the top tercile of forecast (long) earn a higher mean 20-bar forward return than bars in the bottom tercile (short), and the strategy's pre-cost return beats buy-and-hold BTC, or its excess over a 0.5-beta-adjusted hold is positive.  
Reject: Mean 20-bar forward return after bars with the largest positive forecasts is no higher than the unconditional mean 20-bar BTC return, or the forecast-times-forward-return relation is zero or negative (moves reverse after the cross). Pre-cost portfolio return does not beat buy-and-hold on a beta-adjusted basis.  
Inconclusive: The forecast-return relation is positive but the sample of independent 20-day windows is too small to separate from zero, or the strategy beats buy-and-hold only through the long-side drift while the short side loses (the edge is just market beta).  
Deviation: The idea is about the event of an upward cross (short SMA over long SMA). The config instead holds a position proportional to the spread of the 50-bar SMA over the 200-bar SMA on every bar, so it is long while the short average is above the long one (growing with the gap, not only just after the cross) and short when below. It tests persistence of the cross regime, not the return right after the crossing event, and it also takes shorts after downward crosses.  

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

### opus (0.2482 USD, 1 attempt)

Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: Use a 1-bar horizon (next-day close-to-close return), before costs. The idea is confirmed if, on bars where the forecast is above 0 (SMA50 above SMA200, the stretch from an upward cross to the next downward cross), BTC's mean next-day return and share of up days both exceed BTC's unconditional values. That excess must be significant against random stretches of the same lengths: p < 0.05 in a block-bootstrap or circular-shift test of the in-stretch bars. A corollary is that the portfolio's return per unit of average exposure beats buy-and-hold.  
Reject: The idea is rejected if the mean next-day return and up-day share on in-stretch bars are equal to or below BTC's unconditional values. It is also rejected if the in-stretch mean return is significantly negative relative to random stretches, which would point to crosses marking exhaustion.  
Inconclusive: The result is inconclusive if in-stretch returns exceed the unconditional ones but not significantly (p ≥ 0.05). It is also inconclusive if there are too few complete up-cross stretches (fewer than about 5 over the period) to separate the result from one or two dominant bull runs.  
Deviation: The on/off "between an up-cross and the next down-cross" state becomes a graded long position equal to the standardised SMA50−SMA200 spread. The position is still nonzero exactly during the stretch, but it scales with the gap between the averages instead of being constant, so returns are tested as exposure-weighted. The test is long-only (down-cross stretches are flat), uses the conventional 50/200 periods because the source gives none, and leaves out the "price crosses the long average" variant from the brief.  

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

### sonnet (0.1178 USD, 1 attempt)

Config: 002-05_sma-up-regime-positive-drift_config.json  
Confirm: Over a 20-bar horizon, forecast-weighted returns (forecast at bar t times the BTC return from t to t+20) are positive, and the portfolio's gain exceeds buy-and-hold of BTC (before costs). Gains should also grow with the size of the position: the bars in the top tercile of positive forecast should be followed by higher mean 20-bar returns than the lower tercile, and the bars with the most negative forecasts by lower returns than the bars with small forecasts.  
Reject: Over the 20-bar horizon, forecast-weighted returns are zero or negative, or the portfolio does not beat buy-and-hold BTC (before costs). Rejection is also supported if returns after large positive forecasts are lower than after small ones (reversal after crosses).  
Inconclusive: The portfolio beats buy-and-hold but forecast-weighted 20-bar returns do not grow with position size, or the gain comes from a few large episodes; or the portfolio's return is positive but within buy-and-hold's error range (the long-only market drift explains it).  
Deviation: The idea is an event-based stretch (from an upward cross to the next downward cross, long only). The config instead holds a graded position proportional to the standardised SMA50-SMA200 spread on every bar. It is signed (short when the short average is below the long), and its size varies with the spread, not a fixed level across the stretch. It tests "the sign and size of the spread predict the following 20-bar return", not returns measured from each cross to the next.  

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
            "id": "sma_spread",
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
                  "window": 250,
                  "min_periods": 62
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

### opus (0.2684 USD, 1 attempt)

Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: The horizon is 1 bar. Take the bars where the config is short, that is, up days with volume below the 20-day average. On those bars, BTC's next-day return must average below its unconditional mean next-day return (t ≤ -2). The short's next-day gain, before costs, must also grow with position size: the top size tercile earns more per bar than the bottom tercile.  
Reject: Over the same 1-bar horizon, the mean next-day return after short bars is at or above BTC's unconditional mean next-day return. Rejection also holds if the next-day gain does not grow with position size, or shrinks with it.  
Inconclusive: The mean next-day return after short bars is below the unconditional mean, but not significantly (-2 < t < 0). Also inconclusive: it is significant, but the size terciles show no ordering. Also inconclusive: fewer than 30 bars carry a position large enough to trade (|forecast| ≥ 2).  
Deviation: "Unusually low volume" becomes "the day's volume is below its 20-day average (including today)", which is a milder condition than "unusual". "Followed by falling back" becomes a short held for one day only, sized by that day's rise. Any give-back that comes after the first day is not captured. The brief's contrast with high-volume moves is not part of this test.  

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

### sonnet (0.1321 USD, 1 attempt)

Config: 003-01_low-volume-up-move-reverts_config.json  
Confirm: Over the next 5 bars, the bars with a nonzero (short) forecast are followed by a BTC return below its unconditional average 5-bar return, so the short position gains net of the coin's own drift. The gain also grows with the size of the short (larger |forecast| followed by a larger fall).  
Reject: The 5-bar return after the active bars is equal to or above BTC's unconditional average 5-bar return, so the short does no better than holding. The gain also does not grow with |forecast|, or the larger moves rise further.  
Inconclusive: Fewer than about 30 active bars over the sample, or a 5-bar shortfall versus holding that is too small to tell apart from the spread of 5-bar returns across active bars, or a gain that appears only in the smallest positions and not in the largest.  
Deviation: The config tests only the upward-move, low-volume half of the theory. It does not compare against high-volume moves, which the brief says should hold or continue, so the volume-dependence claim is not tested. "Sharp" is the single-day move, graded by its size, with small moves damped. "Unusually low volume" is a day's volume at or below 75% of its 20-day mean (the engine's on/off low-volume-up-bar component is used only as a regime measure, not as the forecast). The position exists only on the bar the condition holds and goes flat on the next bar that does not meet it, so it is not held for the 5-bar evaluation horizon. The 5-bar result is read from the recorded forecast rather than from a held position.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "lowvol_up",
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
              "id": "lowvol_up",
              "op": "lte",
              "value": -5.0
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
      "unknown": null,
      "trending": null,
      "chop": null
    }
  }
}
```

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.2207 USD, 1 attempt)

Untestable: The idea needs bitcoin's past returns as the signal and an altcoin's later returns as the outcome, but the config sees one coin at a time, and the test runs only on BTC/USDT with no altcoin and no cross-coin input. A lead-lag between bitcoin and altcoins therefore cannot be computed or traded here.  

### sonnet (0.1117 USD, 1 attempt)

Untestable: The idea is that altcoins drift up after a bitcoin up move, which needs altcoin returns alongside bitcoin's. The test runs on BTC/USDT only, and the config sees one coin's bars and nothing from any other symbol, so no altcoin price or return is available to measure the drift.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.2699 USD, 1 attempt)

Config: 005-01_bearish-rsi-divergence-reversal_config.json  
Confirm: The test uses a 10-bar horizon, on BTC, ETH and BNB pooled, before costs. Take the bars where the close is the highest close of the last 20 bars. On the ones where the forecast is negative, the next 10-bar return is lower than on the ones where the forecast is zero or positive. The gap must be significant at the 5% level. Also, the coin's 10-bar return minus its unconditional mean 10-bar return (the buy-and-hold drift) falls as the forecast becomes more negative, and is negative in the most-negative forecast decile.  
Reject: At 20-bar highs, the 10-bar forward returns after a negative forecast (divergence) are no lower than those after a non-negative forecast (no divergence). Or the most-negative forecast decile is followed by drift-adjusted 10-bar returns at or above zero.  
Inconclusive: The difference has the predicted sign but is not significant, or it holds on only one of the three coins. Also inconclusive if fewer than about 30 non-overlapping 20-bar-high bars with a negative forecast exist per coin.  
Deviation: The test does not detect the discrete pattern "new price high with an RSI peak lower than at the previous price high". Instead it uses a continuous spread on every bar: where the close sits in its 20-bar range, minus the RSI(14) level, both standardised. A short position grows when price is high in its range but RSI is weak. The spread is symmetric, so it also goes long on the bullish counterpart (price low in its range, RSI not low). It is also mildly long when a new high comes with very strong RSI, which is a part the idea does not claim. The confirm and reject criteria therefore look only at bars at 20-bar highs.  

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
            "id": "price_pos",
            "class": "strategies.strategy_components.DonchianBreakoutComponent",
            "params": {
              "period": 20
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
          },
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

### sonnet (0.1327 USD, 1 attempt)

Config: 005-01_bearish-rsi-divergence-reversal_config.json  
Confirm: Over a 10-bar horizon, before costs, the forecast correlates negatively with the next 10-bar return on each coin. The most negative forecasts (top decile of |forecast|, price at the top of its 20-bar range with weak RSI) are followed by a clearly lower 10-bar return than the bars with price at the top of its range but ordinary RSI. The portfolio also gains more than holding each coin over the same bars.  
Reject: The 10-bar returns after the most negative forecasts are no lower than after price-at-range-top bars without weak RSI, or the forecast's correlation with the next 10-bar return is zero or positive. Alternatively, the portfolio does not beat buy-and-hold before costs, or its gains do not grow with the size of |forecast|.  
Inconclusive: The sign is right on only one or two of the three coins, or the effect is too small to separate from the spread across coins. The top-decile |forecast| bars are too few or too clustered in one episode to judge. The portfolio beats holding only because of the long-side (bullish-divergence) bars.  
Deviation: The config does not detect a divergence event against the previous price high. It reads the state: price near the top of its 20-bar range while RSI(14) is weak relative to its recent level. This is a graded sum of two standardised parts, with no product or swing-high comparison. The position therefore also shrinks, rather than vanishing, when price is high and RSI is also high. The config is symmetric: price near the 20-bar low with strong RSI (a bullish divergence) goes long, which the idea does not state. The reversal is tested as a short while the state holds, not as the retracement of the run-up to the high.  

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
            "id": "price_pos",
            "class": "strategies.strategy_components.DonchianBreakoutComponent",
            "params": {
              "period": 20
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
          },
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
