# Exercise 13: side by side

Prompt: `system_prompt_used.md`. Opus, the 13 fixed ideas. The wish list is `opus/plans/COMPONENT_WISHLIST.md`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.2944 USD)

Fidelity:  
- Situation: the 14-bar RSI reaches a high extreme on BTC, ETH or BNB -> adapted: the "reaches an extreme" threshold becomes a graded short that grows as RSI rises above 50. The signed_power transform damps readings near 50 towards zero and amplifies readings far above it, so the position is concentrated at extremes without a cliff. "After the index reaches" becomes "while the index is high".  
- Comparison: behaviour after extreme readings against behaviour after neutral readings (from the brief) -> kept: the criterion compares forward returns after high-extreme bars with forward returns after neutral bars. Both groups are taken from the recorded RSI value. Neutral readings give a near-zero forecast.  
- Outcome: price falls over the following bars, giving back part of the run -> kept: the forward close-to-close return over 5 daily bars after the bar, expected negative relative to neutral bars.  
- Verdict transfer: yes: the test measures whether returns after high RSI readings are lower than after neutral ones, with the position growing with the extremity, which is exactly the claim. A confirm or reject transfers to the idea.  
Forecast: The forecast is built from RSIPullbackComponent with period 14, whose raw value is (50 − RSI) × 0.4. This value is negative when RSI is above 50. - It is standardised against its own previous 60 values, with min_periods 20, so an average reading is about 10 in size. - It is then passed through signed_power with exponent 2 and pivot 10. A standardised −5 becomes −2.5, −10 stays −10, and −15 becomes −22.5. Moderate readings are damped and extreme ones amplified, smoothly. - It is then clipped at a maximum of 0, so only the high-RSI side the idea speaks about takes positions. The forecast is zero whenever RSI is at or below 50. It is negative (short) when RSI is above 50, growing roughly with the square of the standardised distance above 50, and reaching the −20 cap (200% short) at the most extreme readings. It is never positive.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: - Extreme bars: bars whose forecast is −10 or lower (the largest short positions, roughly RSI well above its usual excursion). - Neutral bars: bars whose recorded raw RSI value is between −4 and +4 (RSI between 40 and 60). - Measure: the mean 5-bar forward return of the coin (close to close) after extreme bars, minus the same mean after neutral bars. - Counting: overlapping returns are counted once. Within a run of consecutive extreme bars, only the first bar and then every 5th bar are kept; neutral bars are sampled every 5th bar. - Drift: subtracting the neutral-bar return removes the coin's own drift, so buy-and-hold's rise is not credited. - Pooling: results are pooled across the 3 coins and 18 windows, and also reported per coin.  
- Supporting check: the 5-bar return of the strategy's portfolio on bars where the forecast is nonzero, minus the return of holding the coin over the same bars. Results are grouped into terciles of position size. If the idea holds, this excess should rise with the size of the short.  
- Confirm: All three of the following hold: - The pooled extreme-minus-neutral difference is −1.0 percentage point or lower. - The t-statistic on the non-overlapping cases is −2.0 or lower. - The difference has the same negative sign in at least 2 of the 3 coins.  
- Reject: Either of the following holds, with at least the minimum count of cases: - The pooled difference is 0 or higher (extreme readings are followed by returns no lower than neutral). - The difference is positive with a t-statistic of +2.0 or higher, which would indicate continuation, the opposite of the idea.  
- Inconclusive: - A negative difference that misses the confirm thresholds (smaller than 1.0 percentage point in size, or a t-statistic between −2.0 and 0). - Coins disagreeing in sign (fewer than 2 of 3 negative). - Fewer than 30 non-overlapping extreme cases pooled, or fewer than 30 non-overlapping neutral cases.  

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

### opus (0.0653 USD)

Fidelity:  
- Situation: the RSI reaches a high extreme on the coin -> adapted: the 14-bar RSI's distance above 50 is used as a graded measure. It is squared through `signed_power` so that high extremes get large positions and readings near 50 get nearly none. This replaces an on/off "extreme" threshold.  
- Comparison: behaviour after neutral RSI readings -> kept: in the criterion, forward returns after the largest positions (high-extreme RSI) are compared with forward returns after bars whose recorded RSI is neutral (40 to 60).  
- Outcome: price keeps rising over the following bars -> adapted: the long position is held for as long as RSI stays high and shrinks as RSI falls back. The outcome is read as the forward 5-bar return after each bar, so no fixed holding period is used in the config.  
- Verdict transfer: yes: the test asks whether upward moves after high-RSI bars are larger than after neutral bars, before costs and net of the coin's own drift, which is exactly the idea's claim.  
Forecast: The forecast starts from `RSIPullbackComponent` with period 14 (the convention), whose raw value is (50 − RSI) × 0.4. - It is standardised against its own previous 60 values (window 60, min_periods 20), which puts its average absolute value near 10. - It is then negated, so it is positive when RSI is above 50. - It is passed through `signed_power` with exponent 2 and pivot 10. Moderate readings shrink smoothly towards 0 (5 becomes 2.5) and strong readings grow (15 becomes 22.5). - Finally it is clipped at 0 from below. The forecast is 0 whenever RSI ≤ 50. It is positive and long when RSI is above 50. It grows roughly with the square of how far RSI sits above 50 relative to its recent typical distance. The final clip on the combined forecast caps it at +20 (200% long). It is never negative.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The forward 5-bar close-to-close return after "extreme" bars minus the forward 5-bar return after "neutral" bars. - Extreme bars are the top quintile of the forecast among bars where it is positive. - Neutral bars are those whose recorded RSI is between 40 and 60. RSI is recovered from the recorded raw value as 50 − raw / 0.4. - Results are pooled across BTC, ETH, BNB and all 6 windows. - Overlapping returns are counted once: within each coin and window, only the first qualifying bar of each non-overlapping 5-bar block is kept. - Because both groups are measured on the same coin and the same windows, the coin's own drift (the buy-and-hold return) cancels out of the difference.  
- Supporting check: The portfolio's daily return minus (that day's allocation × the coin's daily return under buy-and-hold) should not apply, as written; the check is instead the strategy's mean daily return per unit of allocation minus the coin's mean daily return. It must be positive for the idea to hold.  
- Confirm: Both conditions must hold: - The extreme-minus-neutral difference in mean forward 5-bar return is at least +1.0 percentage point, with a t-statistic of at least 2.0 on non-overlapping cases. - The difference is positive in at least 2 of the 3 coins.  
- Reject: Either of these rejects the idea: - The pooled difference is 0 or below, with a t-statistic of −1.0 or below. - The pooled difference is negative in at least 2 of the 3 coins, which would mean high RSI is followed by weaker moves (no continuation, or reversal).  
- Inconclusive: A positive difference below +1.0 percentage point, or a t-statistic between −1.0 and 2.0, or results where the coins disagree in direction, is inconclusive. A pooled count of fewer than 30 non-overlapping extreme cases or fewer than 30 non-overlapping neutral cases is also inconclusive, whatever the result.  

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
            "id": "rsi_strength",
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

### opus (0.0687 USD)

Fidelity:  
- Situation: the short moving average has just crossed above the long moving average -> adapted: "after the cross" becomes "while the 50-day SMA is above the 200-day SMA". The on/off cross becomes a graded measure: the percent spread of SMA50 over SMA200, kept only when positive.  
- Comparison: price after random points -> adapted: random points are represented by all bars of the same windows, which is what simply holding BTC earns. Returns while the spread is positive are judged against the unconditional return of holding the coin.  
- Outcome: price keeps rising over the following bars, more often and further than after random points -> kept: the forward 20-bar return of BTC, its sign (more often) and its size (further), measured after in-state bars.  
- Verdict transfer: yes: if bars with SMA50 above SMA200 are followed by more frequent and larger rises than all bars, the cross-started uptrend persists; if they are not, or if they reverse, the idea fails as the brief states.  
Forecast: One component, EMASpreadComponent with average "sma", fast 50 and slow 200 (the daily golden-cross convention). It computes (SMA50 − SMA200) / SMA200 × 100. - It is standardised against its own past 200 values (min_periods 50), so a typical spread gives about 10, which is a 100% long position, capped at 20. - It is then clipped at 0, so the forecast is long-only. - The forecast is zero while SMA50 is below SMA200 (before an upward cross, or after a downward cross ends the trend). - It is positive from the upward cross onward and grows continuously as the short average pulls further above the long one. - It never goes short, because the idea concerns only the upward cross.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: - Split each window into consecutive, non-overlapping 20-bar blocks, so overlapping returns are counted once. - Label a block "in-state" when the forecast is greater than 0 at its first bar. - For each in-state block, take BTC's close-to-close return over the block, before costs. - The measure is the mean of these in-state returns minus the mean 20-bar return over all blocks in all six windows (the buy-and-hold baseline, i.e. random points).  
- Supporting check: Compare two hit rates: the share of in-state blocks with a positive 20-bar return, and the share of all blocks with a positive 20-bar return. Also check the dose-response: in-state blocks with a forecast at or above the in-state median should show a mean forward return at least as high as the blocks below it.  
- Confirm: All three must hold: - The in-state mean 20-bar return exceeds the all-block mean by more than 0, with a one-sided t-statistic of at least 2.0 on the non-overlapping block returns. - The in-state hit rate exceeds the all-block hit rate. - The excess is positive in at least 4 of the windows that contain in-state blocks.  
- Reject: Either of these: - The in-state mean excess return is 0 or below and the in-state hit rate is no higher than the all-block rate. - The excess is negative with a t-statistic of −2.0 or lower, meaning moves reverse after crosses.  
- Inconclusive: - Any result in between, such as a positive excess with a t-statistic below 2.0, or a mean and a hit rate that disagree. - The test is also inconclusive if there are fewer than 12 non-overlapping in-state blocks, or fewer than 6 out-of-state blocks. - The six windows give about 36 blocks in total.  

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
            "id": "golden_spread",
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

### opus (0.0704 USD)

Fidelity:  
- Situation: the stretch between an upward cross of the short simple average over the long one and the next downward cross, which is the state "short SMA above long SMA" -> adapted: "after an up-cross, until the down-cross" becomes "while the 50-day SMA is above the 200-day SMA". The on/off state becomes graded by the size of the spread, and the forecast is 0 whenever the short average is below the long one.  
- Comparison: random stretches of the same length -> adapted: the forward returns from on-state bars are compared with the forward returns from all bars in the same windows, which is simply holding the coin. Random stretches are an unconditional sample of the coin's path, so this is the same baseline.  
- Outcome: price rises more often and further during the up-cross stretch -> kept: the forward BTC return and the share of up moves, measured from on-state bars.  
- Verdict transfer: yes: the long position exists exactly while the up-cross stretch lasts, so on-state returns that beat or fail to beat unconditional returns confirm or reject the idea directly.  
Forecast: One component, the percent spread between the 50-day and 200-day simple moving averages, computed as (SMA50 − SMA200) / SMA200. It is standardised against its own past 200 values (min_periods 50). That puts it on the forecast scale, with about 10 at an average-sized spread, capped at 20. It is then clipped at 0 from below. - The forecast is positive only while SMA50 is above SMA200, which is the stretch between an up-cross and the next down-cross. - It grows as the short average pulls further above the long one. - It is 0 from the down-cross until the next up-cross. - It is never negative. - The 50/200 pair is the most common daily convention, because the brief gives no lengths.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: The mean 20-bar forward BTC close-to-close return from bars where the forecast is above 0, minus the mean 20-bar forward return from all bars. Both are sampled on non-overlapping 20-bar blocks, so overlapping returns are counted once. Results are pooled over the 6 windows and judged before costs against holding the coin.  
- Supporting check: The share of on-state 20-bar blocks with a positive return, compared with the share of positive blocks among all blocks.  
- Confirm: All three must hold: - The on-state mean 20-bar return exceeds the all-blocks mean by at least 2 percentage points. - A Welch t-statistic of the on-state blocks against the off-state blocks is at least 2. - The on-state share of positive blocks is at least 10 points above the unconditional share.  
- Reject: Either of these: - The on-state mean 20-bar return is at or below the all-blocks mean. - The on-state mean 20-bar return is negative, meaning moves after up-crosses reverse.  
- Inconclusive: These cases neither confirm nor reject: - A positive excess below 2 points. - A t-statistic below 2. - A hit-rate gap below 10 points. - Fewer than 10 non-overlapping on-state blocks. - Fewer than 5 off-state blocks. - Fewer than 3 distinct up-cross stretches across the 6 windows.  

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

### opus (0.0960 USD)

Fidelity:  
- Situation: a sharp upward move made on unusually low volume -> adapted: the move is the latest daily bar's percent change, used as a graded size (larger rise, larger position, zero on down days). "Low volume" is a regime condition: the bar's volume is below its 20-bar mean. Volume is graded nowhere in the catalogue except through this on/off comparison, which is allowed only in the detector.  
- Comparison: volume judged against the coin's usual volume -> adapted: "unusually low" becomes "below its own 20-bar average volume" (the volume_filter convention), an on/off regime instead of a graded degree of thinness.  
- Outcome: price falls back after the rise, giving up part of it -> adapted: the short position is held only on the bar after the low-volume up day (holding period dropped). The fall-back is measured by that next bar's return, which should be below the coin's normal daily return.  
- Verdict transfer: yes: the test bets against exactly the low-volume rises, sized by how sharp they are, and is judged on whether price falls back right after them relative to holding; a confirmation or a rejection of that next-day drift speaks directly to the idea.  
Forecast: On every daily bar, the detector checks whether today's volume is below its 20-bar mean. It does this with a constant +10 passed through volume_filter(20), which reads 0 when volume is below its mean. When the result is below 5, the bar is forced into the `mean_reversion` regime. On every other bar the regime is `unknown`, which is flat (forecast 0). In the `mean_reversion` regime the forecast comes from the 1-bar price change (PriceEvolutionComponent, period 1). It is standardised against the mean absolute daily move of the 60 bars before it (target 10, cap 20), then negated and clipped at a maximum of 0. This makes it a short-only bet against the rise: - On a low-volume up day the forecast is negative and proportional to the size of the rise relative to recent daily moves. An average-sized rise gives about -10 (100% short). A rise twice the usual size or more gives -20. - On a low-volume down day it is 0. - On a normal or high-volume day it is 0. Its size grows continuously with how sharp the up move is.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Criterion:  
- Horizon: 1 bar  
- Main measure: For every bar with a negative forecast (a low-volume up day), take the next bar's return of BTC minus the mean daily return of BTC over the same window. That excess return is what the short earns relative to simply holding the coin. Average it weighted by |forecast|, pooled over the 6 windows. Each case covers one non-overlapping next bar. The t-statistic of the weighted mean is computed before costs.  
- Supporting check: Split the active bars into terciles by |forecast|. The mean next-bar excess return in the top tercile (sharpest low-volume rises) should be lower than in the bottom tercile.  
- Confirm: The |forecast|-weighted mean next-bar excess return after low-volume up days is negative with t ≤ -2.0, and the strategy's cumulative portfolio return, summed over the 6 windows before costs, is positive.  
- Reject: The weighted mean next-bar excess return is zero or positive, meaning price after low-volume rises does as well as or better than BTC's normal daily drift, or the top tercile follows through more than the bottom tercile.  
- Inconclusive: A negative weighted mean with t between -2.0 and 0 counts as inconclusive. Fewer than 60 active bars (low-volume up days) pooled across the 6 windows also makes the test inconclusive, whatever the sign.  

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
            "id": "upmove",
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

### opus (0.0445 USD)

Fidelity:  
- Situation: a sharp price move during the coin's quiet hours or on a weekend, when volume is low -> replaced: a 1d bar holds a whole day, so quiet hours cannot be seen. No component reads the day of the week. The nearest thing would be a daily move weighted by that day's volume against its average, and that is a different quantity. No graded component computes even that: the only volume readers are the on/off `VolumeExpansionHedgeComponent` and the dead-zone `volume_filter`.  
- Comparison: the move's volume against the coin's usual volume, and quiet hours or weekends against busy hours -> replaced: the hour-of-day contrast is not in daily bars at all. Only a day-against-day volume ratio could stand in for it.  
- Outcome: part of the move is given back once busy hours and normal volume return -> adapted: a return against the move's direction over the next day or days. The "once busy hours return" timing is inside the day and is lost.  
- Verdict transfer: no: a test on daily bars would measure whether low-volume days revert, not whether moves made in quiet hours or on weekends revert when liquidity comes back, so neither result would settle the idea.  
Reason: The idea's situation and its timing are intraday (quiet hours, then the return of busy hours). On 1d bars that information is not in the coin's own bars, and the config has no day-of-week or time-of-day input. Any daily-bar version would replace the situation with a generic low-volume-day move, which this task forbids.  

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.0262 USD)

Fidelity:  
- Situation: bitcoin makes a sharp up move over recent bars -> kept (the BTC/USDT bars hold bitcoin's own returns, e.g. `PriceEvolutionComponent`)  
- Comparison: altcoin returns judged against bitcoin's earlier move, with the altcoin's own past returns accounted for -> replaced: no config can hold an altcoin's returns next to bitcoin's, because a component sees only its own symbol's bars  
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only price the test can trade and score is BTC/USDT itself, so the outcome would become bitcoin's own continuation, a different claim  
- Verdict transfer: no: a test on BTC/USDT alone would only measure bitcoin's own momentum after a sharp up move, which says nothing about whether altcoins lag bitcoin.  
Reason: The idea links one coin's move (bitcoin) to the later returns of other coins (altcoins). The config sees only one symbol's bars and feeds, and the guide says other coins' prices cannot be expressed. The test runs only on BTC/USDT, so the altcoin outcome cannot be measured or traded.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0476 USD)

Fidelity:  
- Situation: price closes at a new high above its previous swing high -> kept (`DonchianBreakoutComponent` reads where the close sits in its recent range, and it is +sf at a new high)  
- Comparison: the RSI at the new high against the RSI at the previous price high, where a lower RSI means a bearish divergence -> replaced: no component records the RSI value at the bar of the previous price high. The only RSI reading available is `RSIPullbackComponent`, which is the current RSI against the fixed level 50. That is a different quantity from RSI against its own value at the prior high.  
- Outcome: price falls and gives back part of the run-up to the high -> adapted: a graded short whose size follows the size of the divergence, held while the divergence is present instead of for a fixed retracement period  
- Verdict transfer: no: a config built from "price near its range top while RSI is below 50" tests whether RSI weakness at a high matters, not whether RSI makes a lower high than at the previous price high. Its result would neither confirm nor reject the divergence idea.  
Reason: The divergence needs the RSI value on the bar of the previous price swing high, to compare with the RSI at the current new high. No catalogue component records a past pivot's RSI, and no transform or composition can fetch a value from a specific earlier bar chosen by price. All the data is in the coin's own closes, and a graded component could carry it, but the indicator does not exist.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0531 USD)

Fidelity:  
- Situation: price closes at a new low (below the previous swing low) while RSI(14) at this low is higher than RSI was at that previous price low -> replaced: no catalogue component, alone or combined, compares RSI at the current low with RSI at the earlier price low. The closest build would add a price-range position (DonchianBreakoutComponent, negated) to a contrarian RSI level (RSIPullbackComponent). That measures "price near its low and RSI low", which is the RSI-extreme question the brief explicitly excludes, not a divergence.  
- Comparison: RSI at the current price low against RSI at the previous price low (a higher low), and, per the brief, moves after divergent new lows against moves after non-divergent new lows -> replaced: the weighted mean of standardised components is additive and has no memory of a past bar's RSI. A `percentile` of RSI ranks it against all past RSI values, not against the RSI reading at the prior price low. Score_product can multiply two current readings but cannot look up the earlier one.  
- Outcome: price rebounds after the divergent low and recovers part of the decline into it (upward) -> adapted: the holding period and the "part of the decline" target are dropped. The outcome becomes the coin's forward return over a fixed horizon while the forecast is long, judged against holding the coin.  
- Verdict transfer: no: without a measure of RSI at the previous price low, any buildable forecast tests whether oversold new lows rebound, not whether fading momentum behind a new low does. A confirmation or rejection would therefore say nothing about divergence.  
Reason: The idea needs the RSI value at the previous price low, compared with the RSI value at the current new low. Both come from the coin's own closes, and a graded forecast could carry the result (zero when there is no new low, growing with the RSI higher-low margin, long only). No catalogue component records RSI at a past swing low. No composition of current-bar readings (Donchian position, RSI level, percentile ranks) can express that comparison.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0477 USD)

Fidelity:  
- Situation: the close makes a new high over its recent window while RSI stays below its own high over the same window (a bearish divergence), as opposed to a new price high where RSI also makes a new high -> replaced: no catalogue component, alone or combined, measures where RSI sits relative to its own recent high. `RSIPullbackComponent` gives only the RSI level, which is a different quantity from "RSI below its prior high".  
- Comparison: returns after diverging new highs against returns after confirming new highs -> kept: the forecast would be graded by how far RSI falls short of its high while price is at its high, and the criterion would compare what follows the larger positions with what follows the near-zero ones.  
- Outcome: weaker (lower) returns after a diverging new high than after a confirming one -> kept: a short-leaning forecast scaled by the size of the divergence, judged on forward returns against holding the coin.  
- Verdict transfer: no: built from the RSI level instead of RSI against its own high, the test would measure "high price with middling RSI", not divergence, so neither a pass nor a fail would settle the idea.  
Reason: The divergence needs RSI's position within its own recent range (or its distance below its own rolling high), set against the close's position within its range. The catalogue has the price side (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`), but nothing ranks or ranges RSI against its own past. That cannot be built with transforms either: `percentile` cannot sit next to the required `standardise` (rule V15), and a history op in `history_transforms` sees one value. Everything needed is in each coin's own closes, and a graded difference of two range positions fits the config's logic, so only the component is missing.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0541 USD)

Fidelity:  
- Situation: a new price low (the close is the lowest close of the recent window) where RSI makes a higher low than at the previous price low -> replaced: the new price low can be built (the raw `DonchianBreakoutComponent` value at -sf, as a regime rule). But the catalogue only gives the current RSI level (`RSIPullbackComponent`, 50 - RSI). No component compares today's RSI with its value at the previous price low, or with its own recent minimum. Using the RSI level instead would measure a different quantity.  
- Comparison: new price lows where RSI also makes a new low (confirming momentum) -> replaced: this needs the same missing RSI-against-its-prior-low reading. The sign or size of a working divergence component would separate the two kinds of low. With only the RSI level, "confirming" would just mean "low RSI", which is a different quantity.  
- Outcome: stronger (upward) returns after the divergent lows than after the confirming lows -> adapted: "after the low" becomes "while the close sits at its new low". A graded long position grows with how far RSI sits above its own prior low. The holding period is dropped.  
- Verdict transfer: no: a test built on the RSI level would test "oversold at a new low", which the brief rules out as a different question. Its result would therefore neither confirm nor reject the divergence idea.  
Reason: The divergence compares RSI now with RSI at the previous price low (or with its own rolling minimum), and no catalogue component or composition computes it. `RSIPullbackComponent` gives only the current RSI level, and no transform can take a rolling minimum of another component's output inside the window. Everything needed is in the coin's own closes, and a graded RSI-divergence component could be held in a regime gated on the new price low, so the gap is a missing component, not a limit of the config.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0483 USD)

Fidelity:  
- Situation: price closes at a new high over a recent window while RSI stays below its own prior high in that window (bearish divergence) -> replaced: the catalogue can measure where the close sits in its range (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`, 50 - RSI), but nothing measures RSI against its own recent peak. Using the RSI level instead of the RSI's prior high would be a different quantity.  
- Comparison: the RSI's current value against its previous high made while price was lower, and, from the brief, price moves after a divergence against price moves after new highs without one -> replaced: no component holds RSI's prior peak. `percentile` on RSI cannot follow `standardise` (V15), and a veto percentile ranks RSI over its whole stored history, not against the last swing high.  
- Outcome: price keeps rising to further highs after the divergence (long, continuation) -> kept: a positive forecast while the divergence is present, judged on the forward close-to-close return.  
- Verdict transfer: no: built from the RSI level instead of RSI-versus-its-own-prior-high, the test would measure "new price high with a moderate RSI", which is not the divergence the idea names.  
Reason: The divergence needs RSI compared with its own recent maximum (a lower RSI high while price makes a higher high). No catalogue component, alone or combined through weights, negation, centring or regimes, computes RSI's position relative to its own recent range or peak. The data is all in the coin's own closes, and a graded divergence score would fit the config's logic.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.0530 USD)

Fidelity:  
- Situation: price makes a new low (close at the bottom of its recent range) while RSI makes a higher low (RSI now above the low it made at the earlier price low) -> replaced: the catalogue can see the price side (DonchianBreakoutComponent, where the close sits in its range) and the RSI level against 50 (RSIPullbackComponent). Nothing computes where RSI sits against its own earlier low. A weighted sum of price range position and RSI level measures "price low while RSI is not far below 50", which is a different quantity from an RSI higher low.  
- Comparison: new price lows with an RSI higher low, against new price lows without one (the brief's test of whether divergence adds anything) -> adapted: graded, so a position that grows as the price low gets deeper while RSI holds further above its own recent low. This is only possible once the divergence itself can be measured.  
- Outcome: price keeps falling to further lows after the divergence (short, continuation) -> kept: a short position, judged on the coin's next returns against holding the coin.  
- Verdict transfer: no: without a measure of RSI against its own earlier low, a test built from price range position and RSI level would judge "oversold-looking lows" and not RSI divergence, so neither its confirmation nor its rejection would carry over to the idea.  
Reason: The divergence needs RSI to be compared with its own earlier low over the same window in which price makes its new low. Every input is in the coin's own closes, and a graded "price range position minus RSI range position" fits the config's weighted-mean logic. However, no catalogue component outputs RSI's position within its own recent range. Linear combinations of DonchianBreakoutComponent (price range position) and RSIPullbackComponent (RSI level against 50) cannot reconstruct RSI's distance from its prior low.  
