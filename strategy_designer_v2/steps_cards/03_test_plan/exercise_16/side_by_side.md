# Exercise 16: side by side

Prompt: `system_prompt_used.md`. Opus, the 13 fixed ideas. The wish list is `opus/plans/COMPONENT_WISHLIST.md`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0601 USD)

Fidelity:  
- Situation: RSI at a high extreme -> adapted: graded RSI excess above 50 ("after" becomes "while"), with extremes amplified and no fixed 70 cut.  
- Comparison: behaviour after high readings vs after neutral readings -> kept: forward returns after the largest shorts are compared with forward returns on flat (neutral) bars.  
- Outcome: price falls back, giving back part of the run -> kept: the short gains when the next 5 bars' return is negative.  
- Verdict transfer: yes: the short-only RSI forecast bets exactly that high readings come before falls, sized by how extreme the reading is.  
Forecast: The forecast uses one indicator, RSIPullbackComponent with period 14 (the daily convention). Its raw value is (50 - RSI) x 0.4. - Scaling. standardise (window 60, min_periods 20) puts the raw value on the scale of its own past 60 values, about 10 on average. - Short side only. clip with max 0 keeps only the short side, so the forecast is zero whenever RSI is 50 or below. - Extremes weigh more. signed_power with exponent 2 and pivot 10 shrinks mild readings smoothly toward 0 and enlarges extreme ones. RSI near 55 gives a tiny short. RSI near 70 or higher gives a short of 10 to 20. - Sign and size. The forecast is never positive. It grows more negative, and the position larger, as RSI climbs further above 50.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's mean 5-bar forward return after bars with forecast ≤ -10 (the largest shorts, RSI roughly 70 or above), minus its mean 5-bar forward return after flat bars (forecast 0). This is pooled over coins and windows, using non-overlapping 5-bar returns only (a new case starts at least 5 bars after the previous one).  
- Supporting check: The same difference has the reversal sign (negative) in at least 2 of the 3 coins.  
- Confirm: The difference is negative with a t-stat ≤ -2 on non-overlapping cases, and the supporting check holds.  
- Reject: The difference is ≥ 0, or its t-stat is above -1 (high readings are followed by flat or continuing prices, not by a fall).  
- Inconclusive: A t-stat between -2 and -1, or a confirming t-stat where the coins disagree. The result is also inconclusive with fewer than 30 non-overlapping extreme cases in total, or fewer than 30 flat-bar cases.  

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

### opus (0.0517 USD)

Fidelity:  
- Situation: RSI at a high extreme -> adapted: RSI(14) above 50 becomes a graded long, and `signed_power` makes extremes count most; the hard threshold is dropped.  
- Comparison: forward moves after neutral readings -> kept: RSI near 50 gives a forecast near 0, and the criterion contrasts the high-forecast bars with those near-zero bars.  
- Outcome: price keeps rising over the following bars -> adapted: "after X" becomes "while X", and the long is held only while RSI stays high.  
- Verdict transfer: yes: higher forward returns after the largest RSI-driven longs than after neutral bars confirm the idea, and none or lower rejects it.  
Forecast: Take the 14-bar Wilder RSI, read as 50 minus RSI. Standardise it over its past 60 values, then negate it so that RSI above 50 is positive. Clip it at 0, so it is long only, since the idea is only about high extremes. Then apply `signed_power` with exponent 2 and pivot 10. The forecast is 0 when RSI is at or below 50 and small when RSI is just above 50. It grows quadratically as RSI moves further above 50 relative to its usual deviation, reaching 10 at a typical-size deviation and capping at 20 for extremes.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's mean forward 5-bar return after high-extreme bars (forecast ≥ 10), minus its mean forward 5-bar return after neutral bars (forecast < 2.5, RSI near 50). It is pooled over all coins and windows, with overlapping cases thinned to one per 5 bars per coin, before costs.  
- Supporting check: The strategy's portfolio return minus holding the coin at the strategy's average exposure, per coin, before costs.  
- Confirm: The extreme-minus-neutral difference is at least +1.0% per 5 bars with t ≥ 2 on non-overlapping cases. It must be positive for at least 2 of the 3 coins, and the supporting excess over exposure-matched holding must be positive.  
- Reject: The difference is ≤ 0 pooled, or negative for at least 2 of the 3 coins; a significantly negative value (reversal) also rejects this idea.  
- Inconclusive: A positive difference below +1.0%, or t < 2, or a coin split that meets neither rule. Fewer than 30 non-overlapping high-extreme cases or 30 neutral cases pooled is also inconclusive.  

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
            "id": "rsi_cont",
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

Fidelity:  
- Situation: short SMA has crossed above the long SMA -> adapted: "after the cross" becomes "while SMA50 is above SMA200", graded by the gap between them.  
- Comparison: random points -> kept: in-position bars are compared with all bars, which amounts to holding the coin.  
- Outcome: price keeps rising over the following bars -> kept: the forward return of BTC over the horizon, long side.  
- Verdict transfer: yes: "after a cross" made "while crossed" is an allowed adaptation, and persistence must show as better forward returns while the short average stays above the long one.  
Forecast: Uses the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA (EMASpreadComponent with average "sma"). This spread is standardised against its own past 200 values and clipped at 0. The forecast is positive, and grows with the spread, while SMA50 is above SMA200. It is zero while SMA50 is below SMA200. It is never short, because the idea is only about the upward cross.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: Take the BTC 20-bar forward return at bars where the forecast is above 0, minus the mean 20-bar forward return over all bars of the same windows. Sample at non-overlapping 20-bar steps and pool the 6 windows.  
- Supporting check: Across the in-position samples, the rank correlation between forecast size and the 20-bar forward return is above 0.  
- Confirm: The excess forward return is above 0 with a t-stat of at least 2. The share of positive 20-bar returns while in position is also above the all-bar share. The excess is positive in at least 4 of the windows that hold positions.  
- Reject: The excess forward return is at or below 0 with a t-stat of -1 or lower (moves fade or reverse after crosses). Or the excess is not above 0 in a majority of the windows that hold positions.  
- Inconclusive: Any result between these two counts as inconclusive. So does a run with fewer than 10 non-overlapping in-position 20-bar samples, or fewer than 3 windows with any position.  

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

### opus (0.0533 USD)

Fidelity:  
- Situation: short SMA above long SMA, from the up cross until the down cross -> adapted: the on/off "above" state is made graded by the SMA spread, kept long only and zero below the cross.  
- Comparison: random stretches of the same length -> kept: compared with forward returns from all bars, which is the same as holding the coin.  
- Outcome: price rises more often and further until the down cross -> kept: forward returns while the spread is positive, and how the portfolio grows.  
- Verdict transfer: yes: the position is open on exactly the bars between the up cross and the down cross, so only its size differs from the idea.  
Forecast: The forecast uses one spread, (SMA50 - SMA200) / SMA200, which is the standard 50/200 cross on daily bars. It is standardised against its own past 200 values and clipped at 0. It is positive while SMA50 is above SMA200 and grows with the gap between the two averages. It is zero from the down cross until the next up cross, and it is never negative.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: Take the coin's forward 20-bar return, sampled every 20 bars so that overlapping returns count once. Compare the mean on bars with forecast > 0 against the mean on all bars, pooled over the 6 windows and judged before costs.  
- Supporting check: The share of positive forward 20-bar returns on bars with forecast > 0, compared with the same share on all bars.  
- Confirm: The in-situation mean beats the all-bar mean, with a t-stat of at least 2 over the non-overlapping samples. The positive share is also at least 5 points higher. The difference has the same sign in at least 4 of the windows that have in-situation bars.  
- Reject: The in-situation mean is at or below the all-bar mean. A t-stat of -2 or lower means reversal or exhaustion, and that also rejects.  
- Inconclusive: The idea is neither confirmed nor rejected if the difference is positive with a t-stat between 0 and 2, or if the two measures disagree. The minimum is 15 non-overlapping in-situation samples and at least 2 separate up-cross stretches; with fewer, the result is inconclusive.  

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

## 003-01_low-volume-up-move-reverts

**The idea**

Idea: A sharp upward move made on unusually low volume is followed by price falling back, giving up part of the rise.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against the stretched price, so it drifts back.

### opus (0.0760 USD)

Fidelity:  
- Situation: a sharp up move on unusually low volume -> adapted: low volume becomes a regime veto (bar volume below its 20-bar mean), and the size of the move is graded.  
- Comparison: none in the idea (the brief's contrast with high-volume moves belongs to a sibling idea) -> kept  
- Outcome: price falls back after the move, so it goes down -> adapted: "after the move" becomes a short held over the next bar, sized by the move.  
- Verdict transfer: yes: the short earns before costs only if low-volume up bars are followed by falls, and it loses if they hold.  
Forecast: The forecast is zero unless the bar's volume is below its 20-bar mean. Volume is the idea's condition, so it is set in the regime detector. The detector uses a constant +10, passed through `volume_filter(20)`. A low-volume bar reads below 5, which selects `mean_reversion`. Every other bar falls back to the null `unknown` regime, so the position is flat. On a selected bar, the component is the 1-bar percent move (`PriceEvolutionComponent`, period 1). It is first standardised over its last 60 values (min 20). It is then clipped at 0, so only up moves count, and damped with `signed_power` (exponent 2, pivot 10) so small moves give little and sharp moves give a lot. Last, it is negated. The result is a short of 0 to 20, growing with the square of how large the up move was against recent moves. It is zero on down bars and on bars with normal or high volume, and never long.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Criterion:  
- Horizon: 1 bar  
- Main measure: Take every bar with a non-zero forecast. Measure BTC's close-to-close return over the next bar, minus BTC's mean 1-bar return over all bars of the same window. Weight each by |forecast|, pool across the 6 windows, and give the t-statistic of that weighted mean.  
- Supporting check: Split active bars into terciles of |forecast|. Compare the mean next-bar excess return of the top tercile with the bottom tercile; the top should be the more negative.  
- Confirm: The weighted mean excess return is negative with t ≤ -2, and the top tercile's mean is below the bottom tercile's. That means the short beats holding the coin, before costs.  
- Reject: The weighted mean excess return is ≥ 0, or the top tercile's mean is ≥ 0 and above the bottom tercile's.  
- Inconclusive: A negative mean with -2 < t < 0, or a negative mean whose terciles are not ordered. The test needs at least 60 active bars pooled across windows, and at least 20 in the top tercile; with fewer, it is inconclusive.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "const",
        "class": "strategies.strategy_components.BuyAndHoldStrategy",
        "params": {}
      }
    ],
    "vetoes": [
      {
        "id": "const",
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
            "value": 5.0
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
              },
              {
                "op": "negate"
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

## 003-07_quiet-hours-moves-revert

**The idea**

Idea: Sharp price moves that happen during a coin's quiet hours or on weekends, when its volume is low, are partly reversed once the coin's busier hours and volume return.  
Consequence: Thin-liquidity moves happen when market makers have stepped away, and price drifts back when liquidity providers come back.

### opus (0.0333 USD)

Fidelity:  
- Situation: sharp move in quiet hours or on a weekend, on low volume -> replaced: daily bars hide the hour of a move, and no component reads the weekday, so only a daily low-volume move could stand in for it.  
- Comparison: thin quiet-period liquidity against the busier hours that follow -> replaced: intraday quiet and busy sessions cannot be told apart on 1d bars.  
- Outcome: price partly reverses once busy hours and volume return -> replaced: only a reversal over the next daily bars could be measured, not one tied to the return of busy hours.  
- Verdict transfer: no: a daily low-volume reversal test says nothing about moves made in quiet hours or on weekends, so its result would not carry to this idea.  
Reason: The idea's situation is a move in a coin's quiet intraday hours or on a weekend, reversed when busy hours return. On 1d bars the hour of a move is not in the data, and the config has no component or rule that reads the calendar to pick out weekends. Testing it would mean replacing the timing with plain low daily volume, which is a different idea.  

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.0177 USD)

Fidelity:  
- Situation: bitcoin makes a sharp up move -> kept  
- Comparison: altcoin's later move against bitcoin's earlier move -> replaced: the config sees only one coin's bars, so no second coin is available to compare  
- Outcome: smaller altcoins keep rising over the following bars -> replaced: the test runs on BTC/USDT only, and a config cannot read another coin's prices  
- Verdict transfer: no: a forecast on BTC's own bars only tests BTC's own momentum, not whether altcoins lag bitcoin.  
Reason: The situation is measured on bitcoin and the outcome on other coins, so the idea needs two coins' prices at once. The config sees only one symbol's own bars and feeds, which the guide lists as something it cannot express ("another coin's prices"), and the run covers BTC/USDT alone.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0351 USD)

Fidelity:  
- Situation: price closes at a new recent high -> kept: DonchianBreakoutComponent gives +sf when the close is the highest of its window.  
- Comparison: RSI now is below RSI at the previous price high -> replaced: no component stores RSI at a past price pivot, and RSI rank against its own history is a different quantity.  
- Outcome: price falls and retraces part of the run-up -> adapted: a negative forecast sized by divergence strength, judged over a fixed horizon.  
- Verdict transfer: no: without RSI measured at the previous price high, the test would judge "high price with weak RSI", not divergence.  
Reason: The idea compares today's RSI with RSI at the previous price high. That needs a pivot-anchored memory, which is computable from one coin's closes, but no catalogue component computes it. I tried a weighted sum of DonchianBreakout and negated RSIPullback, and a score_product regime of Donchian times RSI percentile. Both measure RSI against its average or its own history, not against its value at the prior high, so they replace the comparison.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0345 USD)

Fidelity:  
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (Donchian position, negated).  
- Comparison: RSI at this low is higher than RSI at the previous price low -> replaced: no component recalls RSI at the previous swing low, so only the current RSI level is available.  
- Outcome: price rebounds and recovers part of the decline -> kept: long position, gains when price rises over the next bars.  
- Verdict transfer: no: without the RSI value at the previous low, the test would check "price low, RSI not oversold", which is not a divergence.  
Reason: The divergence needs the RSI value at the previous price low. That can be computed from the coin's own closes, and a graded value would fit the config's logic. No catalogue component, alone or combined, computes it. `RSIPullbackComponent` gives only the current RSI level, and `DonchianBreakoutComponent` gives only where price sits in its range. Neither gives RSI's own swing lows or the RSI value at the bar of a previous price low.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0448 USD)

Fidelity:  
- Situation: a new price high whose RSI is below its prior RSI high -> adapted: the new close high becomes a regime rule, and the divergence becomes a graded RSI shortfall; no catalogue component computes that shortfall.  
- Comparison: divergent new highs against confirming new highs (RSI also at a new high) -> kept: the shortfall's sign and size separate the two cases.  
- Outcome: weaker returns after divergent highs, towards a reversal down -> adapted: the forecast is graded short with the shortfall, so the hold lasts only while the situation does.  
- Verdict transfer: no: without a component that compares RSI with its own recent high, the divergence cannot be measured, so no config can carry the verdict.  
Reason: The bars hold everything the idea needs (closes give both the price high and RSI). The config's logic could hold it: a regime on `DonchianBreakoutComponent` at +sf for the new close high, plus a graded component inside it. But no component measures RSI against its own maximum over the lookback. `RSIPullbackComponent` gives only the RSI level. `percentile` cannot be used: it ranks against the whole stored history, not the divergence window, and as a second history op next to `standardise` V15 refuses it.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0376 USD)

Fidelity:  
- Situation: close makes a new N-bar low -> adapted: graded by the close's position in its range (DonchianBreakoutComponent, negated).  
- Comparison: RSI at that low is higher than at the prior low, versus RSI also at a new low -> replaced: no component places RSI against its own recent low, only against the fixed 50 (RSIPullbackComponent).  
- Outcome: price rises more after divergent lows than after confirming lows -> kept: forward returns follow a long forecast, judged against holding the coin.  
- Verdict transfer: no: measuring RSI against 50 instead of against its own prior low tests RSI level, not divergence, so neither a confirm nor a reject would carry over to the idea.  
Reason: The divergence needs RSI measured against its own recent extremes, so that "price at its range low while RSI sits above its range low" can be scored. The config could hold this as a weighted difference (price range position minus RSI range position), but no catalogue component computes where RSI sits in its own recent range. RSIPullbackComponent only compares RSI with 50, which is the RSI-extremes question the brief excludes.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0328 USD)

Fidelity:  
- Situation: price at a new high while RSI makes a lower high -> replaced: no component measures RSI against its own earlier peak, so the lower RSI high cannot be kept.  
- Comparison: current RSI peak against RSI at the prior price high -> replaced: no catalogue component or combination gives RSI's prior peak.  
- Outcome: price keeps rising to further highs -> kept: a graded long position judged on the forward return.  
- Verdict transfer: no: a stand-in such as "price at range top with RSI below 50" is a different situation, so its result would not confirm or reject the divergence idea.  
Reason: The divergence needs price at a new high together with RSI below its own earlier peak. Both come from one coin's closes, and the config could hold them as a regime plus a graded component. No catalogue component gives RSI's prior peak or RSI's position in its own range. Combining `DonchianBreakoutComponent` with `RSIPullbackComponent`, in a weighted sum or a score_product, only compares RSI with 50, not with its earlier high.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.0379 USD)

Fidelity:  
- Situation: price at a new low while RSI makes a higher low -> replaced: no catalogue component measures RSI's current low against its earlier low.  
- Comparison: RSI's current low against its prior low, within the same window as the price low -> replaced: RSI is only available as a level (50 - RSI), never as a position against its own recent extremes.  
- Outcome: price keeps falling to further lows -> kept: a negative, short forecast whose gain is measured over the following bars.  
- Verdict transfer: no: a test of "price near its low and RSI not oversold" is a different situation from "RSI makes a higher low".  
Reason: The divergence compares where price sits in its recent range with where RSI sits in its own recent range. The catalogue gives the price side (`DonchianBreakoutComponent`) but only a raw RSI level (`RSIPullbackComponent`), and no weighted sum of those reproduces "RSI above its own recent minimum". With an RSI range-position component, the forecast would be the standardised Donchian minus the standardised RSI position, clipped at max 0 to keep only the bullish-divergence case. That is a graded short that grows as price sits lower in its range while RSI sits higher in its own.  
