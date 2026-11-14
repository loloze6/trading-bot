# Exercise 3: side by side (the test plan in two calls)

Call 1 (opus, no reference documents) writes the plan in words: `split_helper/prompt_1_plan_in_words.md`. Call 2 turns it into a config, with the two references: `split_helper/prompt_2_config.md`, once with opus (`opus_opus/`) and once with sonnet on the same call-1 plan (`opus_sonnet/`). Raw answers: `*_call1.txt`, `*_call2.txt`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus_opus

Config: 001-01_rsi-high-extreme-reversal_config.json  
Forecast: Compute the 14-day relative strength index on each coin's daily closes, using Wilder's standard smoothing. When the index is at or below 70, the forecast is zero. When the index is above 70, the forecast is negative: −(RSI − 70) / 30. This is a short position that starts at zero right at 70, grows steadily as the reading climbs, and reaches a full short of −1 at an index of 100. The forecast is recomputed at every daily close. It shrinks back toward zero as the index falls, so the short is held only while the high extreme lasts. The forecast is never positive, because this idea makes no claim about low readings. The three coins are run separately with the same settings.  
Confirm: Pool all three coins and look at every bar where the forecast is nonzero. The average price change over the next 5 bars is lower than the coin's average 5-bar change over all bars. That gap is statistically significant: a t-statistic below −2, with standard errors that allow for overlapping 5-bar windows. It also gets more negative as the position gets larger: bars with the index above 80 show a larger shortfall than bars with the index between 70 and 80. Finally, the short positions earn a positive return before costs, measured against the coin's average drift over the same bars, and the gap points the same way on at least two of the three coins.  
Reject: Over the next 5 bars after nonzero-forecast bars, the pooled average change is equal to or above the coin's average 5-bar change. In that case the short positions lose money, or only break even, once the market's drift is removed. If the excess is clearly positive (t-statistic above +2), that is evidence of continuation, which is the opposite of the idea.  
Inconclusive: The pooled shortfall after extremes is negative but the t-statistic is between −2 and 0. Or the result rests on only one coin, with the other two showing no gap or the opposite sign. Or the shortfall is significant but does not grow with the index level.  
Deviation: The idea says price gives back part of the run after the index reaches an extreme. The forecast instead holds a short for every bar the index stays above 70, sized by how far above 70 it is, so it tests "the higher the reading, the weaker the next 5 days" rather than one entry at the moment the extreme is reached. It also tests the direction of the next move, not whether the retracement is a specific fraction of the prior run.  
Config differs: The plan's −(RSI − 70)/30 needs an offset of 70 RSI points. The engine can only add an offset with a constant component, which is not allowed. So the short begins at RSI 50, not 70. - Short starts at 50. The config takes the 14-day Wilder RSI as (50 − RSI) and puts it on the scale of its own past 60 values (standardise). It keeps only the short side (clip at 0), so it is never positive. It then damps small readings with a cubic soft dead zone (signed_power, exponent 3, pivot 20). - Rough sizes. With a typical |RSI − 50| of about 10–12, the forecast is about −2 or smaller in size (less than about 20% short) up to RSI ≈ 60. It is about −6 near RSI 65 and about −15 at RSI 70. It reaches the −20 cap (200% short) from roughly RSI 72 upward. - Opposite of the plan near 70. The plan's short is zero at 70 and reaches −1 (forecast −10) only at RSI 100. This config is already near full size at 70 and flat-capped above about 72. Its grading falls mostly in the 55–72 band, not across 70–100. - Scale drifts. The scale depends on each coin's recent RSI dispersion, not a fixed /30. - More nonzero bars. Bars with RSI between 50 and 70 also carry a small short. The confirm/reject test should still select its bars from the plan's own RSI > 70 rule. - Regime gate not used. Gating on RSI > 70 would make the position jump from 0 to about −18. Above that, the standardised value is saturated, which is effectively on/off.  

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
            "id": "rsi_overbought",
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
                  "exponent": 3,
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

### opus_sonnet

(no plan saved: call 2's config was not valid JSON; see the call-2 text)

## 001-03_rsi-high-extreme-continuation

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

### opus_opus

Config: 001-03_rsi-high-extreme-continuation_config.json  
Forecast: Compute the 14-day Wilder relative strength index on each coin's daily close. The forecast is zero whenever the index is at or below 70, the conventional overbought line. Above 70 the forecast is long and grows in a straight line with the excess: (index − 70) / 30. It reaches full size at an index of 100. The forecast never goes short, because the idea only concerns high extremes. Each coin is run separately with the same settings.  
Confirm: Use a horizon of 10 bars, with bars from all three coins pooled. Compare the 10-bar forward return of the price after bars where the forecast is above zero with the forward return after neutral bars (index between 40 and 60). The idea is confirmed if all four of the following hold: - The forecast-weighted mean of the 10-bar forward return after active bars is above the mean after neutral bars. - That difference is significant, with a t-statistic above 2 using standard errors corrected for the 10-bar overlap (Newey-West, 9 lags). - The same difference is positive in at least 2 of the 3 coins. - Within active bars, the forward return grows with forecast size. This means a positive rank correlation between forecast and 10-bar forward return, and the top third of forecasts beating the bottom third.  
Reject: The idea is rejected if, pooled, the forecast-weighted mean of the 10-bar forward return after active bars is at or below the mean after neutral bars. It is also rejected if it falls significantly below that mean, which would point to reversal, with a t-statistic below −2.  
Inconclusive: The result is inconclusive in any of these cases: - The pooled difference is positive but the t-statistic is between 0 and 2. - The difference is positive pooled but holds in only one coin. - Active bars beat neutral bars, but forward returns do not grow with forecast size.  
Deviation: The idea is a condition ("after the index reaches a high extreme"). The forecast instead sizes the position by how far the index sits above 70, so it also tests a dose-response that the idea does not state. The comparison benchmark is neutral readings (index 40–60) rather than simply holding the coin. Low extremes are left out of the test.  
Config differs: The regime gate matches the plan exactly. The detector reads (50 − RSI) × 0.4 below −8, which means a 14-day Wilder RSI strictly above 70, and every other bar is flat. Inside the gate the size differs from the plan, because no catalogue component or op can subtract the 70 offset. The stored value is 0.4 × (RSI − 50), floored at 8 on bars where RSI ≤ 70. `standardise` then scales it against the mean of its own last 60 stored values. As a result: (1) the forecast jumps from 0 to about 8–10 when RSI crosses 70, instead of starting at 0; (2) it grows linearly with (RSI − 50) rather than (RSI − 70)/30; (3) its scale drifts over time and per coin with the past mean; (4) it is capped at 20, which binds only near RSI ≈ 90–95 or above, instead of reaching full size at exactly 100. It never goes below zero, and within active bars it rises monotonically with RSI. So the set of active bars is the plan's, and the ordering used for the rank test is preserved, but the forecast-weighted mean weighs bars by (RSI − 50) with a floor rather than by the excess over 70.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "rsi_gate",
        "class": "strategies.strategy_components.RSIPullbackComponent",
        "params": {
          "period": 14,
          "scaling_factor": 0.4
        }
      }
    ],
    "rules": [
      {
        "regime": "trending",
        "any_of": [
          [
            {
              "id": "rsi_gate",
              "op": "lt",
              "value": -8.0
            }
          ]
        ]
      }
    ],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "trending": {
        "components": [
          {
            "id": "rsi_excess",
            "class": "strategies.strategy_components.RSIPullbackComponent",
            "params": {
              "period": 14,
              "scaling_factor": 0.4
            },
            "weight": 1.0,
            "history_transforms": [
              {
                "op": "negate"
              },
              {
                "op": "clip",
                "params": {
                  "min": 8.0
                }
              }
            ],
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20
                }
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

### opus_sonnet

Config: 001-03_rsi-high-extreme-continuation_config.json  
Forecast: Compute the 14-day Wilder relative strength index on each coin's daily close. The forecast is zero whenever the index is at or below 70, the conventional overbought line. Above 70 the forecast is long and grows in a straight line with the excess: (index − 70) / 30. It reaches full size at an index of 100. The forecast never goes short, because the idea only concerns high extremes. Each coin is run separately with the same settings.  
Confirm: Use a horizon of 10 bars, with bars from all three coins pooled. Compare the 10-bar forward return of the price after bars where the forecast is above zero with the forward return after neutral bars (index between 40 and 60). The idea is confirmed if all four of the following hold: - The forecast-weighted mean of the 10-bar forward return after active bars is above the mean after neutral bars. - That difference is significant, with a t-statistic above 2 using standard errors corrected for the 10-bar overlap (Newey-West, 9 lags). - The same difference is positive in at least 2 of the 3 coins. - Within active bars, the forward return grows with forecast size. This means a positive rank correlation between forecast and 10-bar forward return, and the top third of forecasts beating the bottom third.  
Reject: The idea is rejected if, pooled, the forecast-weighted mean of the 10-bar forward return after active bars is at or below the mean after neutral bars. It is also rejected if it falls significantly below that mean, which would point to reversal, with a t-statistic below −2.  
Inconclusive: The result is inconclusive in any of these cases: - The pooled difference is positive but the t-statistic is between 0 and 2. - The difference is positive pooled but holds in only one coin. - Active bars beat neutral bars, but forward returns do not grow with forecast size.  
Deviation: The idea is a condition ("after the index reaches a high extreme"). The forecast instead sizes the position by how far the index sits above 70, so it also tests a dose-response that the idea does not state. The comparison benchmark is neutral readings (index 40–60) rather than simply holding the coin. Low extremes are left out of the test.  
Config differs: The plan's forecast is (RSI − 70)/30 above 70 and exactly 0 at or below 70, reaching full size at RSI 100. The catalogue has no component that shifts RSI by 70. The config uses the Wilder RSI(14) component negated, so the raw value is proportional to RSI − 50. `standardise` rescales it by its own past mean absolute value, so the forecast is not a fixed (RSI − 70)/30. The forecast is clipped at 0, so it is long only. The zero point is therefore RSI 50, not 70. The cubic `signed_power` damps readings just above 50 smoothly, which only approximates the 70 cutoff. RSI between 50 and 70 gives a small positive forecast, where the plan gives 0. The forecast does not reach full size at RSI 100, because its scale depends on the recent history of |RSI − 50| rather than a fixed 30-point range. The forecast still grows continuously with the RSI excess. Each coin runs separately with the same settings. The forecast is graded and ungated.  

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
                  "exponent": 3
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

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus_opus

Config: 002-01_sma-upcross-upward-drift_config.json  
Forecast: Long only, from two simple moving averages of daily close, 50 days and 200 days (the conventional "golden cross" pair). Take the gap (SMA50 / SMA200 − 1). Divide it by the 200-day standard deviation of daily log returns × √50, which puts it in units of the coin's own volatility. The forecast is this normalized gap, capped at 2 and divided by 2, so it runs from 0 to 1 (0 to 100% of the portfolio in BTC). It is zero whenever SMA50 is at or below SMA200. It turns positive on the bar after an upward cross, grows as the short average pulls away from the long one, shrinks as they converge, and returns to zero at a downward cross, which the brief says ends the trend. It is never negative.  
Confirm: Use a horizon of 20 bars. Two results must both hold. First, across all bars, the 20-bar forward return of BTC rises with the size of the forecast: the rank correlation between forecast and the following 20-bar return is positive. Second, the bars where the forecast is positive show a higher mean 20-bar forward return, and a higher share of positive 20-bar forward returns, than all bars taken together, which stand in for random points. The difference in mean must have a block-bootstrap 90% interval above zero. Alongside this, before costs, the strategy's final value must exceed a benchmark that holds BTC every bar at the strategy's average exposure. The 20 bars after each fresh upward cross must show positive mean forward returns rather than declines.  
Reject: Any one of these rejects the idea at the 20-bar horizon. The mean 20-bar forward return on positive-forecast bars is at or below the unconditional mean. The share of rising 20-bar windows is no higher than unconditional. The rank correlation between forecast size and 20-bar forward return is zero or negative. The strategy fails to beat the matched-exposure buy-and-hold benchmark. Or the mean 20-bar forward return starting from fresh upward-cross bars is negative, meaning moves after crosses reverse and the cross marks exhaustion.  
Inconclusive: The direction favors the idea but the bootstrap interval includes zero. Or the measures disagree: for example, the mean is higher but the hit rate is not, or the strategy beats the benchmark but the rank correlation is flat. Or fewer than 6 upward crosses occur in the sample, so the post-cross check rests on too few events.  
Deviation: The idea is about the point of the cross. The forecast instead holds a position for the whole period the short average stays above the long one, sized by how far apart they are. It therefore tests persistence of the trend state as well as the start of the trend, and it gives the largest positions to mature trends rather than fresh crosses. Only the upward side is tested. The brief's downward crosses and its price-crossing-the-long-average variant are not tested. The 50/200 setting is a convention, not taken from the source script.  
Config differs: - Normalisation. The SMA50/SMA200 gap is divided by its own mean absolute value over the previous 200 bars. The plan divides by the 200-day standard deviation of daily log returns × √50, and the catalogue has no component or op for that. - The 0-to-1 mapping is the same shape: target 5 and cap 10 give a forecast of 0–10, so 0–100% of the portfolio. - Full exposure is reached at twice the gap's typical recent size, instead of at 2 volatility units. - Timing. The spread uses SMAs that include the current close, and the engine fills at that close. The position therefore starts on the cross bar's close, not on the bar after the cross. - Small moves. Changes in target allocation smaller than 5% are not traded. I set `min_allocation_change` to 0.05 instead of the default 0.2 to keep sizing close to the plan near crosses.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "min_allocation_change": 0.05,
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "sma_gap",
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
                  "min_periods": 50,
                  "target": 5,
                  "cap": 10
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

### opus_sonnet

Config: 002-01_sma-upcross-upward-drift_config.json  
Forecast: Long only, from two simple moving averages of daily close, 50 days and 200 days (the conventional "golden cross" pair). Take the gap (SMA50 / SMA200 − 1). Divide it by the 200-day standard deviation of daily log returns × √50, which puts it in units of the coin's own volatility. The forecast is this normalized gap, capped at 2 and divided by 2, so it runs from 0 to 1 (0 to 100% of the portfolio in BTC). It is zero whenever SMA50 is at or below SMA200. It turns positive on the bar after an upward cross, grows as the short average pulls away from the long one, shrinks as they converge, and returns to zero at a downward cross, which the brief says ends the trend. It is never negative.  
Confirm: Use a horizon of 20 bars. Two results must both hold. First, across all bars, the 20-bar forward return of BTC rises with the size of the forecast: the rank correlation between forecast and the following 20-bar return is positive. Second, the bars where the forecast is positive show a higher mean 20-bar forward return, and a higher share of positive 20-bar forward returns, than all bars taken together, which stand in for random points. The difference in mean must have a block-bootstrap 90% interval above zero. Alongside this, before costs, the strategy's final value must exceed a benchmark that holds BTC every bar at the strategy's average exposure. The 20 bars after each fresh upward cross must show positive mean forward returns rather than declines.  
Reject: Any one of these rejects the idea at the 20-bar horizon. The mean 20-bar forward return on positive-forecast bars is at or below the unconditional mean. The share of rising 20-bar windows is no higher than unconditional. The rank correlation between forecast size and 20-bar forward return is zero or negative. The strategy fails to beat the matched-exposure buy-and-hold benchmark. Or the mean 20-bar forward return starting from fresh upward-cross bars is negative, meaning moves after crosses reverse and the cross marks exhaustion.  
Inconclusive: The direction favors the idea but the bootstrap interval includes zero. Or the measures disagree: for example, the mean is higher but the hit rate is not, or the strategy beats the benchmark but the rank correlation is flat. Or fewer than 6 upward crosses occur in the sample, so the post-cross check rests on too few events.  
Deviation: The idea is about the point of the cross. The forecast instead holds a position for the whole period the short average stays above the long one, sized by how far apart they are. It therefore tests persistence of the trend state as well as the start of the trend, and it gives the largest positions to mature trends rather than fresh crosses. Only the upward side is tested. The brief's downward crosses and its price-crossing-the-long-average variant are not tested. The 50/200 setting is a convention, not taken from the source script.  
Config differs: The gap (SMA50/SMA200 − 1) is not divided by the 200-day return standard deviation × √50, because no catalogue component or transform does that. `standardise` instead divides it by the mean absolute value of its own previous 200 gaps and multiplies by 10. The cap is therefore a clip at forecast 10 (100% long) rather than at 2 volatility units, and the forecast is not in units of the coin's own return volatility. The forecast is still zero when SMA50 is at or below SMA200, never negative, and graded between 0 and 10. The SMA components here include the current bar's close, so the forecast turns positive on the bar of the upward cross rather than the bar after. The risk layer also ignores rebalances smaller than 0.2 in allocation, so very small forecasts near a cross do not move the position.  

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
            "id": "golden_gap",
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
                  "min": 0.0,
                  "max": 10.0
                }
              }
            ]
          }
        ],
        "weight_note": null
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

### opus_opus

Config: 002-05_sma-up-regime-positive-drift_config.json  
Forecast: Use the closing price of BTC/USDT on daily bars. Compute the 50-day simple moving average (short) and the 200-day simple moving average (long), the conventional pair for daily bars. The gap is (SMA50 − SMA200) / SMA200. When the gap is zero or negative, no upward cross is in force and the forecast is zero. When the gap is positive, the stretch since the last upward cross is still open, so the forecast is positive. Its size is the gap divided by a volatility scale, capped at 1. The scale is 10 × the standard deviation of daily close-to-close returns over the last 100 bars. So the position starts small just after the upward cross. It grows as the averages spread apart, relative to normal volatility. It shrinks back to zero as they converge into the downward cross. The forecast never goes below zero, because the idea is only about stretches that begin with an upward cross.  
Confirm: Use a horizon of 20 bars. The mean forward 20-bar return of BTC must be higher on bars with a positive forecast than on all bars (the unconditional, buy-and-hold average), by more than twice its standard error. The standard error must be computed with an overlap-adjusted (Newey-West, 20-lag) method. The share of positive 20-bar returns must also be higher on positive-forecast bars than on all bars. Finally, before costs, the strategy must beat a constant long position in BTC with the same average exposure. It must beat it both in total return and in return per unit of volatility. The edge must not come from a single cross-to-cross stretch. Removing the most profitable stretch must still leave the in-trend mean above the unconditional mean.  
Reject: The mean forward 20-bar return on positive-forecast bars is equal to or below the unconditional mean. Or the share of positive 20-bar returns on those bars is no higher than on all bars. Or returns fall as the forecast grows, so the largest positions are followed by reversals, which would mean the cross marks exhaustion. Or the strategy does no better than the same-exposure constant long position.  
Inconclusive: The in-trend 20-bar mean is higher than the unconditional mean but by less than two standard errors. Or the edge disappears once the single best stretch is removed. Or the hit rate and mean return point in opposite directions. With a 200-day average on daily data, BTC has only a handful of cross-to-cross stretches, so a positive but weak result cannot separate persistence from luck.  
Deviation: The idea treats the whole stretch between crosses as one uniform uptrend. The forecast instead scales the position with the volatility-adjusted gap between the averages. This also tests whether a wider gap means a stronger drift, and it gives little weight to the bars just after the cross and just before the exit. The 50/200 pair is chosen by convention, not by the source. The comparison is made bar by bar over a fixed 20-bar horizon, not stretch by stretch against random stretches of equal length. The price-crosses-long-average variant and the downward-cross side of the brief are not tested.  
Config differs: The config uses the same gap, (SMA50 − SMA200) / SMA200. It is zero when the gap is zero or negative and is capped at allocation 1 (forecast 10). The divisor is different. The plan divides the gap by 10 × the standard deviation of daily close-to-close returns over the last 100 bars. The config divides it by the mean absolute value of the gap over the previous 200 bars, as required by `standardise`, so there is no return-volatility scale. As a result, a gap at its own recent average size gives forecast 10 (allocation 1). The cap is therefore reached whenever the gap is above its recent average absolute size, which is much sooner than under the plan's 10σ scale. The catalogue cannot compute the plan's 100-bar return-volatility divisor inside a component. `vol_normalize` uses the 24-bar close standard deviation × close, which is in price-squared units, and `vol_target` is excluded by the guide.  

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
            "id": "sma_gap",
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
                  "min": 0.0,
                  "max": 10.0
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

### opus_sonnet

Config: 002-05_sma-up-regime-positive-drift_config.json  
Forecast: Use the closing price of BTC/USDT on daily bars. Compute the 50-day simple moving average (short) and the 200-day simple moving average (long), the conventional pair for daily bars. The gap is (SMA50 − SMA200) / SMA200. When the gap is zero or negative, no upward cross is in force and the forecast is zero. When the gap is positive, the stretch since the last upward cross is still open, so the forecast is positive. Its size is the gap divided by a volatility scale, capped at 1. The scale is 10 × the standard deviation of daily close-to-close returns over the last 100 bars. So the position starts small just after the upward cross. It grows as the averages spread apart, relative to normal volatility. It shrinks back to zero as they converge into the downward cross. The forecast never goes below zero, because the idea is only about stretches that begin with an upward cross.  
Confirm: Use a horizon of 20 bars. The mean forward 20-bar return of BTC must be higher on bars with a positive forecast than on all bars (the unconditional, buy-and-hold average), by more than twice its standard error. The standard error must be computed with an overlap-adjusted (Newey-West, 20-lag) method. The share of positive 20-bar returns must also be higher on positive-forecast bars than on all bars. Finally, before costs, the strategy must beat a constant long position in BTC with the same average exposure. It must beat it both in total return and in return per unit of volatility. The edge must not come from a single cross-to-cross stretch. Removing the most profitable stretch must still leave the in-trend mean above the unconditional mean.  
Reject: The mean forward 20-bar return on positive-forecast bars is equal to or below the unconditional mean. Or the share of positive 20-bar returns on those bars is no higher than on all bars. Or returns fall as the forecast grows, so the largest positions are followed by reversals, which would mean the cross marks exhaustion. Or the strategy does no better than the same-exposure constant long position.  
Inconclusive: The in-trend 20-bar mean is higher than the unconditional mean but by less than two standard errors. Or the edge disappears once the single best stretch is removed. Or the hit rate and mean return point in opposite directions. With a 200-day average on daily data, BTC has only a handful of cross-to-cross stretches, so a positive but weak result cannot separate persistence from luck.  
Deviation: The idea treats the whole stretch between crosses as one uniform uptrend. The forecast instead scales the position with the volatility-adjusted gap between the averages. This also tests whether a wider gap means a stronger drift, and it gives little weight to the bars just after the cross and just before the exit. The 50/200 pair is chosen by convention, not by the source. The comparison is made bar by bar over a fixed 20-bar horizon, not stretch by stretch against random stretches of equal length. The price-crosses-long-average variant and the downward-cross side of the brief are not tested.  
Config differs: The gap (SMA50 − SMA200)/SMA200 is computed as in the plan, and the forecast is zero when the gap is zero or negative and positive and graded when it is positive. The volatility scale and the cap differ. - Volatility scale: the plan divides by 10 × the std of daily close-to-close returns over 100 bars, which the catalogue cannot compute. The config divides by the 24-bar price std (`stddev_24`) × close through `vol_normalize`. It then standardises the result against its own past 200 values, with target 10 and cap 20. - Cap: the plan caps the scaled gap at 1. The config caps the forecast at +20 (allocation 2.0), and the zero floor comes from `clip` with `min` 0. The size therefore does not saturate where the plan's does. - Scale: the plan's size falls in 0 to 1. The config's average positive forecast is around 10, scaled against the gap's own history. - Direction: the shape matches the plan. The position starts small after the upward cross, grows as the averages spread, and shrinks to zero as they converge.  

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
            "id": "sma_gap",
            "class": "strategies.strategy_components.EMASpreadComponent",
            "params": {
              "fast_period": 50,
              "slow_period": 200,
              "average": "sma"
            },
            "weight": 1.0,
            "history_transforms": [
              {
                "op": "vol_normalize"
              }
            ],
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
        ],
        "trending": null,
        "mean_reversion": null,
        "chop": null
      }
    }
  }
}
```

## 003-01_low-volume-up-move-reverts

**The idea**

Idea: A sharp upward move made on unusually low volume is followed by price falling back, giving up part of the rise.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against the stretched price, so it drifts back.

### opus_opus

Config: 003-01_low-volume-up-move-reverts_config.json  
Forecast: Short only, never above zero, and zero unless the coin has just risen sharply on thin volume. - Move strength. Take the 3-bar log return. Divide it by the standard deviation of daily log returns over the previous 20 bars (not counting the current bar), multiplied by √3. Call this z. Move strength = min(max(z − 1, 0), 2). It is zero unless the 3-bar rise exceeds one normal 3-day swing, and it is capped once the rise passes three swings. - Thinness. Take the mean volume of the same 3 bars and divide it by the median daily volume of the 20 bars before them. Thinness = min(max(−ln(ratio), 0) / ln 2, 1). It is zero at normal or above-normal volume, grows as volume falls below normal, and is full at half the normal volume. - Forecast. Forecast = −(move strength / 2) × thinness, so it runs from 0 to −1 (−1 is a full short). - Behaviour. The short grows with both the size of the rise and how thin its volume was. It fades back to zero as the 3-bar window rolls past the move or as volume returns to normal. - Settings. The 3-bar window and the 20-bar baselines are conventional choices, not tuned.  
Confirm: Take every bar where the forecast is nonzero and keep only events at least 5 bars apart, at least 20 of them. After the third of those events with the largest |forecast|, BTC's mean 5-bar forward close-to-close return must be: - negative, - below BTC's unconditional mean 5-bar return over the whole sample, and - lower than after the smaller-|forecast| events. The gap to the unconditional mean must have a t-statistic of at least 2, before costs.  
Reject: After the top-third events, the mean 5-bar forward return is at or above BTC's unconditional mean 5-bar return. In other words, sharp rises on thin volume are not followed by any give-back relative to simply holding.  
Inconclusive: Any of these neither confirms nor rejects the idea: - the top-third mean is below the unconditional mean but the t-statistic is under 2; - it is negative but not lower than after the smaller events; - fewer than 20 separate events occur.  
Deviation: - Bar size. Daily bars cannot see the intraday, quiet-hour or weekend liquidity gaps the brief describes. The test therefore checks a coarser version: multi-day rises on below-normal daily volume. - "Sharp" and "unusually low". These are fixed as a 3-bar rise above one volatility unit and volume below its 20-day median. - Scope. Only the upward, low-volume half of the brief is tested. The contrast with high-volume moves is left to other ideas.  
Config differs: The plan grades thinness, but here it is an on/off gate. The catalogue has no graded volume component. The regime is active only when the current bar's volume is below its 20-bar mean. The plan instead uses the mean of the 3 bars against the median of the prior 20, and scales the short by −ln(ratio)/ln 2. As a result, the short does not grow as volume gets thinner, and it switches to flat when volume returns to its average instead of fading. Move strength is measured differently. The plan divides the 3-bar log return by the std of the prior 20 daily log returns ×√3. Here the 3-bar percent return is divided by the mean absolute value of the previous 60 3-bar returns. The `standardise` target of 3 and `signed_power` with exponent 2 approximate the plan's mapping, assuming roughly normal returns and full thinness: - z≈1 gives about −1.4 instead of 0; - z≈2 gives about −5.6 instead of −5; - z≈3 and above gives −10 (full short). The plan's hard dead zone, max(z−1, 0), becomes this smooth one, so small rises still carry a small short (it stays below the 2-point minimum rebalance). Rises below 0 give no position, so the config is short-only as the plan requires.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "vol_gate",
        "class": "strategies.strategy_components.BuyAndHoldStrategy",
        "params": {}
      }
    ],
    "vetoes": [
      {
        "id": "vol_gate",
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
            "id": "rise_3",
            "class": "strategies.strategy_components.PriceEvolutionComponent",
            "params": {
              "period": 3
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "standardise",
                "params": {
                  "window": 60,
                  "min_periods": 20,
                  "target": 3
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
                "op": "clip",
                "params": {
                  "max": 10.0
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

### opus_sonnet

Forecast: Short only, never above zero, and zero unless the coin has just risen sharply on thin volume. - Move strength. Take the 3-bar log return. Divide it by the standard deviation of daily log returns over the previous 20 bars (not counting the current bar), multiplied by √3. Call this z. Move strength = min(max(z − 1, 0), 2). It is zero unless the 3-bar rise exceeds one normal 3-day swing, and it is capped once the rise passes three swings. - Thinness. Take the mean volume of the same 3 bars and divide it by the median daily volume of the 20 bars before them. Thinness = min(max(−ln(ratio), 0) / ln 2, 1). It is zero at normal or above-normal volume, grows as volume falls below normal, and is full at half the normal volume. - Forecast. Forecast = −(move strength / 2) × thinness, so it runs from 0 to −1 (−1 is a full short). - Behaviour. The short grows with both the size of the rise and how thin its volume was. It fades back to zero as the 3-bar window rolls past the move or as volume returns to normal. - Settings. The 3-bar window and the 20-bar baselines are conventional choices, not tuned.  
Confirm: Take every bar where the forecast is nonzero and keep only events at least 5 bars apart, at least 20 of them. After the third of those events with the largest |forecast|, BTC's mean 5-bar forward close-to-close return must be: - negative, - below BTC's unconditional mean 5-bar return over the whole sample, and - lower than after the smaller-|forecast| events. The gap to the unconditional mean must have a t-statistic of at least 2, before costs.  
Reject: After the top-third events, the mean 5-bar forward return is at or above BTC's unconditional mean 5-bar return. In other words, sharp rises on thin volume are not followed by any give-back relative to simply holding.  
Inconclusive: Any of these neither confirms nor rejects the idea: - the top-third mean is below the unconditional mean but the t-statistic is under 2; - it is negative but not lower than after the smaller events; - fewer than 20 separate events occur.  
Deviation: - Bar size. Daily bars cannot see the intraday, quiet-hour or weekend liquidity gaps the brief describes. The test therefore checks a coarser version: multi-day rises on below-normal daily volume. - "Sharp" and "unusually low". These are fixed as a 3-bar rise above one volatility unit and volume below its 20-day median. - Scope. Only the upward, low-volume half of the brief is tested. The contrast with high-volume moves is left to other ideas.  
Untestable (call 2): The forecast depends on thinness, the 3-bar mean volume against the 20-bar median daily volume. No catalogue component outputs a graded volume measure; the only volume-reading class, `VolumeExpansionHedgeComponent`, is on/off, refused as a forecast source, and uses only the current up bar against a 24-bar mean. A price-only config would test "short after any sharp rise", which is a different idea. A gate built from the on/off volume class would replace the graded thinness with a switch and change the test.  

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus_opus

Untestable (call 1): The idea says altcoins drift up after a sharp bitcoin move, so the position must be held in an altcoin while the signal comes from bitcoin's bars. A forecast may use only the traded coin's own bars, and the test runs only on BTC/USDT, so neither the cross-coin signal nor the altcoin position can be built.  

### opus_sonnet

Untestable (call 1): The idea says altcoins drift up after a sharp bitcoin move, so the position must be held in an altcoin while the signal comes from bitcoin's bars. A forecast may use only the traded coin's own bars, and the test runs only on BTC/USDT, so neither the cross-coin signal nor the altcoin position can be built.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus_opus

Forecast: Use a 14-bar RSI (Wilder) on daily closes, computed separately for each coin. - At each bar's close, take the recent high H1, the highest close of the last 10 bars including today, and note its bar. - Take the prior high H0, the highest close from 60 bars ago to 11 bars ago, and note its bar. - A bearish divergence is active when H1 is above H0 and the RSI at H1's bar is below the RSI at H0's bar. - When the divergence is active, the forecast is minus min((RSI at H0 − RSI at H1) / 20, 1). The position is therefore short, and it grows with how far momentum has faded behind the new high. It reaches a full short at a 20-point RSI shortfall. - Otherwise the forecast is zero. This covers bars with no new high above H0, and new highs where RSI also makes a higher high. - The forecast is never positive, because the idea speaks only about new highs. - Since H1 is drawn from a rolling 10-bar window, the short stays on, recomputed each bar, for up to 10 bars after a divergent high. It then returns to zero unless a newer divergent high appears. - All settings are conventional (RSI 14, 20/60-bar swing windows, a 20-point RSI gap for full size) and are fixed in advance.  
Confirm: The horizon is 10 bars. Take every bar where the forecast is nonzero, pooled across BTC, ETH and BNB. Compute the coin's 10-bar forward log return after each one. As a control, compute the same return after every bar where H1 is above H0 but RSI did not make a lower high, meaning a new high without divergence. The idea is confirmed if all of the following hold: - The mean forward return after divergence bars is negative. - It is below the control mean, with a one-sided block-bootstrap p-value under 0.05 (resampling blocks of 10 bars). - The difference has the same sign in at least 2 of the 3 coins. - Before costs, the strategy's 10-bar returns on active bars beat simply holding the coin over the same bars.  
Reject: The idea is rejected if either of these holds: - The pooled mean 10-bar forward return after divergence bars is equal to or higher than after non-divergent new highs. This is the brief's own falsification line. - The strategy's returns on active bars are not better than holding the coin over the same bars.  
Inconclusive: Any of the following counts as inconclusive: - Divergence returns come out lower than the control but the bootstrap p-value is 0.05 or higher. - The effect appears in only one of the three coins. - Fewer than 30 independent divergence episodes are found, pooled. Overlapping bars from the same divergent high count as one episode.  
Deviation: - Highs are measured on closes, and the "previous high" is taken from fixed windows (60 to 11 bars back versus the last 10 bars) rather than from discretionary swing pivots. - The retracement "of part of the run" is tested as a negative 10-bar forward return compared with non-divergent new highs. It is not tested as a measured fraction of the prior advance. - The position size following the RSI shortfall is a modelling choice the idea does not state. - The mirror case (bullish divergence at new lows) from the brief is not tested, because this idea covers only highs.  
Untestable (call 2): The forecast needs the RSI value at the bar where the 10-bar closing high occurred, compared with the RSI at the bar of the earlier 60-to-11-bar closing high. No component or transform op can look up a past value at the bar of a rolling maximum, so neither the divergence condition nor the RSI shortfall that sizes the short can be computed. Any substitute, such as "close near its 60-bar high while RSI is below 70", would define different signal bars and a different control set, so the plan's divergence-versus-control criterion would no longer be tested.  

### opus_sonnet

Forecast: Use a 14-bar RSI (Wilder) on daily closes, computed separately for each coin. - At each bar's close, take the recent high H1, the highest close of the last 10 bars including today, and note its bar. - Take the prior high H0, the highest close from 60 bars ago to 11 bars ago, and note its bar. - A bearish divergence is active when H1 is above H0 and the RSI at H1's bar is below the RSI at H0's bar. - When the divergence is active, the forecast is minus min((RSI at H0 − RSI at H1) / 20, 1). The position is therefore short, and it grows with how far momentum has faded behind the new high. It reaches a full short at a 20-point RSI shortfall. - Otherwise the forecast is zero. This covers bars with no new high above H0, and new highs where RSI also makes a higher high. - The forecast is never positive, because the idea speaks only about new highs. - Since H1 is drawn from a rolling 10-bar window, the short stays on, recomputed each bar, for up to 10 bars after a divergent high. It then returns to zero unless a newer divergent high appears. - All settings are conventional (RSI 14, 20/60-bar swing windows, a 20-point RSI gap for full size) and are fixed in advance.  
Confirm: The horizon is 10 bars. Take every bar where the forecast is nonzero, pooled across BTC, ETH and BNB. Compute the coin's 10-bar forward log return after each one. As a control, compute the same return after every bar where H1 is above H0 but RSI did not make a lower high, meaning a new high without divergence. The idea is confirmed if all of the following hold: - The mean forward return after divergence bars is negative. - It is below the control mean, with a one-sided block-bootstrap p-value under 0.05 (resampling blocks of 10 bars). - The difference has the same sign in at least 2 of the 3 coins. - Before costs, the strategy's 10-bar returns on active bars beat simply holding the coin over the same bars.  
Reject: The idea is rejected if either of these holds: - The pooled mean 10-bar forward return after divergence bars is equal to or higher than after non-divergent new highs. This is the brief's own falsification line. - The strategy's returns on active bars are not better than holding the coin over the same bars.  
Inconclusive: Any of the following counts as inconclusive: - Divergence returns come out lower than the control but the bootstrap p-value is 0.05 or higher. - The effect appears in only one of the three coins. - Fewer than 30 independent divergence episodes are found, pooled. Overlapping bars from the same divergent high count as one episode.  
Deviation: - Highs are measured on closes, and the "previous high" is taken from fixed windows (60 to 11 bars back versus the last 10 bars) rather than from discretionary swing pivots. - The retracement "of part of the run" is tested as a negative 10-bar forward return compared with non-divergent new highs. It is not tested as a measured fraction of the prior advance. - The position size following the RSI shortfall is a modelling choice the idea does not state. - The mirror case (bullish divergence at new lows) from the brief is not tested, because this idea covers only highs.  
Untestable (call 2): The catalogue has no component that stores the RSI at a specific past price high, so it cannot compare the RSI at H1's bar with the RSI at H0's bar. It also has no way to compute the 10-bar versus 60-to-11-bar high comparison. Combining Donchian range position with the RSI level would only measure "price near its high and RSI low", which is not divergence. That blend also cannot be kept from going positive, because a clip can only be applied to each component, not to their sum.  
