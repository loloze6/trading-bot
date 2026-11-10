# Exercise 15: side by side

Prompt: `system_prompt_used.md`. Opus, the 13 fixed ideas. The wish list is `opus/plans/COMPONENT_WISHLIST.md`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2730 USD)

Fidelity:  
- Situation: RSI at a high extreme -> adapted: the threshold becomes graded, so the short position grows with RSI above 50, and "after X" becomes "while X".  
- Comparison: after extreme readings vs after neutral readings -> adapted: the position is near zero at neutral RSI and largest at extremes, and outcomes are judged against all bars.  
- Outcome: price falls back over the following bars -> adapted: the holding period is dropped, so the short is held only while RSI stays high.  
- Verdict transfer: yes: a graded short sized by how high RSI sits tests directly whether high readings come before declines.  
Forecast: The forecast uses 14-bar Wilder RSI through RSIPullbackComponent, whose raw value is (50 - RSI) x 0.4. This is standardised against its own previous 60 values, so an average reading is 10. Then signed_power with exponent 2 and pivot 10 damps readings near neutral and amplifies extremes, without a cliff. Finally clip with max 0 keeps only the short side. The forecast is negative when RSI is above 50 and grows with the square of how far RSI sits above its usual distance from 50. It is zero whenever RSI is at or below 50. It never goes long.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's mean 5-bar forward close-to-close return after bars with forecast <= -10 (strong short), minus its mean 5-bar forward return over all bars of the same windows. Results are pooled across the three coins, keeping at most one case per 5 bars so that overlapping returns count once.  
- Supporting check: Mean 5-bar forward return after bars with forecast between -2 and 0 (neutral RSI). Strong-short bars should fall below this, and the extreme-vs-neutral gap should share the main measure's sign.  
- Confirm: The pooled difference is -1.0% or lower with t <= -2.0, and it is negative in at least 2 of the 3 coins.  
- Reject: The pooled difference is >= 0. A difference of +1.0% or more with t >= 2.0 would also point to continuation.  
- Inconclusive: A pooled difference between -1.0% and 0, or a t-stat between -2.0 and 0, or only 1 of 3 coins agreeing. Fewer than 30 non-overlapping strong-short cases pooled is inconclusive whatever the result.  

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

### opus (0.0635 USD)

Fidelity:  
- Situation: RSI at a high extreme -> adapted: "extreme" becomes graded; the long position grows smoothly with RSI above 50 and is amplified near the top.  
- Comparison: versus neutral RSI readings -> adapted: neutral readings near 50 give a position near zero, so extremes are judged against them by the size of the position.  
- Outcome: price keeps rising over the following bars -> adapted: "after the extreme" becomes "while RSI is high", and no holding period is set.  
- Verdict transfer: yes: RSI is measured as the idea states, and the long side is sized by how extreme it is, so both a confirmation and a rejection carry over to the idea.  
Forecast: Use RSI(14) on daily closes. The `RSIPullbackComponent` output, (50 − RSI) × sf, is first standardised against its own previous 60 values. It is then negated, so it becomes positive when RSI is above 50. It is clipped at 0, so the forecast is long-only on the high side. Finally `signed_power` with exponent 2 is applied. The result is near 0 when RSI is near 50 and zero when RSI is at or below 50. It grows quadratically as RSI rises, so the largest long positions come at the highest readings. It is never negative.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's mean 5-bar forward return after bars with RSI(14) ≥ 70 (the largest positions), minus its mean 5-bar forward return after bars with RSI between 40 and 60. Pool BTC, ETH and BNB over all windows. Use non-overlapping 5-bar returns only, so each period counts once. Comparing against neutral bars means the coin's own drift is not credited to the idea.  
- Supporting check: Compare the before-cost strategy return with holding the coin at the strategy's own average allocation over the same bars. The strategy must beat it, meaning the gains come from sizing up at high RSI and not from being long a rising market.  
- Confirm: The difference in the main measure is above 0 with a t-statistic of at least 2 on the non-overlapping returns. It is also positive for at least 2 of the 3 coins, and the supporting check is positive.  
- Reject: The difference in the main measure is 0 or below. Or it is negative for at least 2 of the 3 coins. Either result rejects continuation after high RSI.  
- Inconclusive: The difference is positive but its t-statistic is below 2, or the coins disagree in a way the confirm and reject rules do not cover. The test is also inconclusive with fewer than 30 non-overlapping extreme (RSI ≥ 70) cases or fewer than 30 neutral cases in the pool.  

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

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus (0.0531 USD)

Fidelity:  
- Situation: short SMA has crossed above long SMA -> adapted: "after the cross" becomes "while the 50-day SMA is above the 200-day SMA", graded by the percent spread between them.  
- Comparison: drift after random points -> kept: forward returns on active bars are compared with all bars and with holding the coin.  
- Outcome: price keeps rising over the following bars -> kept: forward return on the long side.  
- Verdict transfer: yes: the up-cross regime holding and its spread growing is the persistence the idea claims, measured long-only against random bars.  
Forecast: The indicator is the percent spread between the 50-day and 200-day simple moving averages. These are the conventional golden-cross settings on daily bars. The spread is standardised against its own past 200 values, so an average spread gives about 10, capped at 20. It is then clipped at 0. The forecast is positive while the 50-day SMA is above the 200-day SMA. It grows as the short average pulls further above the long one. It is zero when the short average is below the long one. It is never negative, because the idea concerns only up-crosses.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Criterion:  
- Horizon: 10 bars  
- Main measure: The coin's forward 10-bar return, taken on non-overlapping 10-bar blocks and pooled over the 6 windows. Blocks that start with forecast > 0 are compared with all blocks, which stand for random points or simply holding the coin. Before costs.  
- Supporting check: Regress the forward 10-bar return on the forecast at the block start, over the active blocks. A positive slope means returns grow with the size of the spread.  
- Confirm: The mean forward return of active blocks exceeds the all-block mean, with Welch t ≥ 2. The share of rising blocks among active blocks also exceeds the share among all blocks. The supporting slope is ≥ 0.  
- Reject: The active-block mean forward return is ≤ the all-block mean. Or the active blocks show reversal, with the difference negative and t ≤ -1.  
- Inconclusive: A positive difference with t between 0 and 2 neither confirms nor rejects. So do mixed signs between the mean and the hit rate. The test is also inconclusive if there are fewer than 20 non-overlapping active blocks, or fewer than 20 inactive blocks.  

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

### opus (0.0596 USD)

Fidelity:  
- Situation: the stretch from an upward 50/200 SMA cross until the next downward cross -> adapted: "after the up-cross, until the down-cross" becomes "while SMA50 > SMA200", graded by the size of the spread.  
- Comparison: random stretches of the same length -> kept: the in-trend bars are compared with all bars, which is the same as holding the coin.  
- Outcome: price rises more often and further during the stretch -> kept: the coin's next-bar returns on in-trend bars.  
- Verdict transfer: yes: the up-cross stretch is exactly the set of bars where the forecast is positive, so both a confirm and a reject carry over to the idea.  
Forecast: The forecast uses the spread between the 50-day SMA and the 200-day SMA, as a percent of the 200-day SMA (50/200 is the usual daily convention; the brief gives no settings). The spread is standardised against its own past 200 values, then clipped at 0. It is positive, and grows with the spread, from the bar of an upward cross until the next downward cross. It is zero while the 50-day SMA is below the 200-day SMA. It is long only, because the idea concerns only the stretches that start with an upward cross.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Criterion:  
- Horizon: 1 bar. Each bar's next-day return is counted once, so returns do not overlap.  
- Main measure: The coin's mean next-bar return on bars with forecast > 0, minus its mean next-bar return on all bars. The bars are pooled over the 6 windows, and the measure is taken before costs.  
- Supporting check: The share of up days on bars with forecast > 0, against the share of up days on all bars.  
- Confirm: The in-trend mean next-bar return exceeds the all-bar mean, with a t-statistic of at least 2.0. The in-trend share of up days is also higher than the all-bar share.  
- Reject: The in-trend mean return is at or below the all-bar mean. It is also a reject if in-trend returns are below out-of-trend returns with a t-statistic of -2.0 or lower, which would mean the moves reverse.  
- Inconclusive: A positive difference with a t-statistic between 0 and 2, or a main measure and supporting check that disagree, neither confirms nor rejects. The test needs at least 100 in-trend bars and at least 3 distinct upward-cross stretches; fewer than that is also inconclusive.  

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

### opus (0.0801 USD)

Fidelity:  
- Situation: sharp one-day rise on unusually low volume -> adapted: low volume is a veto (volume below its 20-bar mean), and the size of the rise is graded.  
- Comparison: volume against its usual level -> adapted: "unusually low" becomes "below its 20-bar average", the only volume threshold the detector offers.  
- Outcome: price falls back after the rise -> adapted: short while the low-volume up bar is current; the holding period is dropped.  
- Verdict transfer: yes: the test bets against exactly the low-volume up moves the idea names, sized by the move.  
Forecast: Two parts decide each bar. First, a veto checks whether the daily bar's volume is below its 20-bar mean. Only then is the regime mean_reversion; on every other bar the forecast is flat. Second, in that regime the forecast is the bar's 1-day percent move, scaled by its mean absolute size over the 60 prior bars (target 10, cap 20). It is then negated and clipped to at most 0. The result is a short whose size grows with how sharp the low-volume up move is. Down bars and flat bars give 0.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Criterion:  
- Horizon: 1 bar  
- Main measure: The close-to-close return on the bar after each bar with a non-zero forecast. Compare it with the coin's mean 1-bar return over all tested bars, the buy-and-hold baseline. Pool the cases across the 6 windows; each case counts once.  
- Supporting check: Over the same active bars, regress the next-bar return on the forecast. The slope should be positive (a bigger short comes before a bigger fall). Separately, the 3-bar forward return should also sit below the 3-bar baseline, with non-overlapping cases counted once.  
- Confirm: The mean next-bar return after active bars is below the baseline mean. The difference has a one-sided t-stat of 2 or more, and the forecast-weighted gain before costs is positive.  
- Reject: The mean next-bar return after active bars is at or above the baseline mean (difference ≥ 0), or the forecast-weighted gain is ≤ 0.  
- Inconclusive: A difference below the baseline with a t-stat between 0 and 2 is inconclusive. So is any result from fewer than 60 active bars across all windows.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "move",
        "class": "strategies.strategy_components.PriceEvolutionComponent",
        "params": {
          "period": 1
        }
      }
    ],
    "vetoes": [
      {
        "id": "move",
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
            "op": "between",
            "low": 0.0,
            "high": 0.0
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
            "id": "thin_up_move",
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

## 003-07_quiet-hours-moves-revert

**The idea**

Idea: Sharp price moves that happen during a coin's quiet hours or on weekends, when its volume is low, are partly reversed once the coin's busier hours and volume return.  
Consequence: Thin-liquidity moves happen when market makers have stepped away, and price drifts back when liquidity providers come back.

### opus (0.0398 USD)

Fidelity:  
- Situation: a sharp move during quiet hours or a weekend, on low volume -> replaced: 1d bars cannot show quiet hours, and no component reads the weekday or graded relative volume.  
- Comparison: the move's volume against the coin's usual volume, at its busier times -> replaced: intraday busy and quiet volume merge into one daily total.  
- Outcome: the move partly reverses once busier hours and volume return -> replaced: the next daily bar mixes quiet and busy hours, so the reversal's timing cannot be seen.  
- Verdict transfer: no: on daily bars the test would measure a different situation, so neither result would settle the idea.  
Reason: The idea's situation and outcome turn on hours within the day (quiet hours, then busy hours returning). The 1d bars this test runs on do not carry that, and the config has no symbol, timeframe or intraday key to reach it. Even the weekend and low-volume parts would need a weekday reading and a graded relative-volume component, which the catalogue lacks.  

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.0220 USD)

Fidelity:  
- Situation: a sharp bitcoin up move -> kept: BTC's own recent return can be measured from BTC bars.  
- Comparison: altcoin response against the earlier bitcoin move -> replaced: the altcoin bars are not in the BTC config, which sees only its own coin.  
- Outcome: altcoins drift up in the following bars -> replaced: only BTC's own next return can be traded on BTC/USDT.  
- Verdict transfer: no: a test on BTC alone only checks BTC momentum, which says nothing about altcoins catching up.  
Reason: The idea's outcome is the later return of other coins (altcoins) after a bitcoin move. A config sees only one coin's own bars and feeds and cannot read bitcoin while trading an altcoin, and the run is BTC/USDT only.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0398 USD)

Fidelity:  
- Situation: price makes a new high -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent), not a swing-high event.  
- Comparison: RSI's peak now is lower than RSI at the previous price high -> replaced: no component stores RSI at a prior price peak, only the current RSI level.  
- Outcome: price falls back and retraces part of the run-up -> adapted: a short forecast, graded by divergence size, held while the situation lasts; no fixed retracement target.  
- Verdict transfer: no: RSI level next to a range high is not RSI's peak against its own previous peak, so neither result would settle the divergence idea.  
Reason: The comparison needs RSI's value at the previous price swing high, set against RSI now while price exceeds that high. No catalogue component, alone or combined through weights, regimes or transforms, finds a prior price peak or recalls RSI there. Pairing RSI level with range position measures overbought-at-high, which the brief explicitly excludes.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0521 USD)

Fidelity:  
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent, flipped).  
- Comparison: RSI now vs RSI at the previous price low (higher low) -> replaced: the catalogue only gives the current RSI level, not its value at the prior swing low.  
- Outcome: price rebounds and recovers part of the decline -> adapted: long while the divergence holds, with no holding period.  
- Verdict transfer: no: without RSI at the prior low there is no divergence, only "price low while RSI is not low", which is a different signal.  
Reason: The divergence compares RSI at the current price low with RSI at the previous swing low, which can be computed from the coin's own closes. No catalogue component, alone or combined, finds the prior swing low or reads RSI there. Pairing Donchian position with the RSI level against 50 replaces that comparison instead of measuring it.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0455 USD)

Fidelity:  
- Situation: a new price high reached with RSI below its own prior high -> replaced: no component compares RSI with its own recent high.  
- Comparison: divergent new highs set against new highs where RSI also makes a new high -> kept: a rule on Donchian at its top selects new highs, and the RSI gap would separate the two groups.  
- Outcome: weaker (more downward) returns after divergent highs -> kept: the forecast's sign and size, set against the next bars' returns.  
- Verdict transfer: no: RSI level is the only stand-in, and it tests RSI extremes, which the brief rules out.  
Reason: The idea needs today's RSI measured against RSI's own peak over the same window where price sets its new high. No catalogue component computes this. RSIPullbackComponent gives only the RSI level, and `standardise` must be the only history op in a forecast pipeline, so no rolling-max or rank of RSI can be built from the existing ops.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0386 USD)

Fidelity:  
- Situation: a new price low reached with a higher RSI low -> replaced: the catalogue has nothing that compares the current RSI with its earlier lows.  
- Comparison: the same returns after new lows where RSI also makes a new low -> kept: the forecast record can split new-low bars by the size of the RSI divergence.  
- Outcome: price rises more after divergent lows (a reversal up) -> kept: forward returns from the forecast record.  
- Verdict transfer: no: no catalogue combination measures "RSI above its prior low while price is at its low". A sum of range position and RSI level is long on any low or any high RSI, not on the divergence.  
Reason: The idea needs RSI's own rolling minimum set against price's rolling minimum on the same bar. No catalogue component outputs RSI's rolling extreme, and the strategy forecast cannot multiply or condition one component on another. `DonchianBreakoutComponent` covers price's range position, and `RSIPullbackComponent` covers only RSI's current level, not its prior low.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0534 USD)

Fidelity:  
- Situation: price at a new high while RSI peaks below its earlier high -> replaced: no component compares RSI with its own earlier peak, so only RSI level or rank would be available.  
- Comparison: the RSI high against its prior high, and price above its prior high -> adapted: the price side is kept graded as the close's place in its range (Donchian), but the RSI side has no counterpart.  
- Outcome: price keeps rising to further highs (long) -> adapted: a long position held while the divergence lasts, judged on the return over a fixed horizon.  
- Verdict transfer: no: a test on RSI level instead of "RSI lower high" would judge weak-momentum highs, not divergences.  
Reason: The divergence needs RSI's current value compared with its own highest value over the same lookback in which price sets its high. No catalogue component does this. RSIPullbackComponent gives only the current RSI. Weighted sums, negation and percentile ranks over the detector's fixed history cannot rebuild a windowed RSI maximum. Everything needed is in the coin's own closes, and a regime rule or a graded component could hold the result.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.1026 USD)

Fidelity:  
- Situation: price at a new low while RSI makes a higher low -> replaced: the catalogue gives only RSI's level, not where RSI sits against its own earlier low.  
- Comparison: the earlier price low and the RSI value at it -> replaced: no component keeps the prior low or the RSI reading there.  
- Outcome: price keeps falling to further lows -> kept: a short position sized by the divergence, judged on the next bars' returns.  
- Verdict transfer: no: a test of RSI level against the price range is a different signal, so its verdict would not carry over to the higher-low divergence.  
Reason: The divergence compares RSI's current low with its own earlier low, at the bar of the earlier price low. No catalogue component computes that, alone or combined. Pairing `DonchianBreakoutComponent` with `RSIPullbackComponent` measures RSI's level, not a higher low, so it would replace the situation.  
