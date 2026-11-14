# Exercise 14: side by side

Prompt: `system_prompt_used.md`. Opus, the 13 fixed ideas. The wish list is `opus/plans/COMPONENT_WISHLIST.md`.

## 001-01_rsi-high-extreme-reversal

**The idea**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

### opus (0.0691 USD)

Fidelity:  
- Situation: the RSI reaches a high extreme (a strongly one-sided run of gains) -> adapted: the "extreme" threshold becomes a graded reading. The forecast uses 50 - RSI(14), keeps only the overbought side, and passes it through a smooth dead zone (signed_power, exponent 2). The position therefore stays small at mildly high RSI and grows steeply as RSI nears its extremes. "After the RSI reaches" becomes "while the RSI is high".  
- Comparison: behaviour after extreme readings versus after neutral readings (from the brief) -> kept: neutral readings give a forecast near 0, so the criterion compares what follows the largest short positions with what follows near-zero forecasts.  
- Outcome: price falls over the following bars, giving back part of the run -> adapted: there is no holding period. The short is held only while RSI stays high, and the fall is measured as the forward 5-bar return after each bar.  
- Verdict transfer: yes: the forecast is short in proportion to how overbought the RSI is and flat when RSI is neutral or low, so the comparison and the forward return measure exactly whether high RSI extremes are followed by falls.  
Forecast: The forecast uses RSIPullbackComponent with period 14, the Wilder convention. Its raw value is (50 - RSI) x 0.4: negative when RSI is above 50, positive below. - It is standardised over the 60 previous values (min_periods 20), which puts it on the forecast scale, about 10 for an average distance of RSI from 50. - It is clipped at a maximum of 0, so only the overbought side remains and the forecast is never positive. - signed_power with exponent 2 and pivot 10 damps moderate readings towards 0 and amplifies large ones. A standardised -5 becomes -2.5, -10 stays -10, and -20 becomes -40. The combined forecast is clipped at -20. - The forecast is 0 whenever RSI is at or below 50. It grows more negative, continuously and faster than linearly, as RSI rises towards an extreme. A bigger short is taken the more overbought the coin is. - There is no regime condition: the detector is ungated.  
Config: 001-01_rsi-high-extreme-reversal_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's forward 5-bar close-to-close return is measured after two groups of bars, pooled over the 3 coins and 6 windows: - extreme bars: bars whose forecast is at most -10, that is, RSI clearly overbought; - neutral bars: bars whose forecast is 0, that is, RSI at or below 50 (none of the idea's situation). The measure is the mean forward return after extreme bars minus the mean after neutral bars. Taking the difference removes the market's own drift, the same way it would against simply holding the coin. Returns are taken on non-overlapping 5-bar blocks, so that overlapping returns are counted once: within a run of qualifying bars, only every 5th bar counts. The result is judged before costs.  
- Supporting check: The sign of the main difference is computed per coin. It must be negative for at least 2 of the 3 coins, so that one coin does not carry the result.  
- Confirm: Both of the following hold: - The pooled difference (extreme minus neutral) is negative, with a t-statistic of -2.0 or lower on the non-overlapping blocks. - It is negative for at least 2 of the 3 coins. That is, price falls more, or rises less, in the 5 bars after high RSI extremes than after neutral readings.  
- Reject: Either of the following holds: - The pooled difference is zero or positive, which means continuation or no effect after high extremes. - The pooled difference is negative with a t-statistic above -1.0, and the difference is negative for at most 1 of the 3 coins.  
- Inconclusive: Any other result is inconclusive. This includes: - a negative difference with a t-statistic between -2.0 and -1.0; - a t-statistic of -2.0 or lower with only 1 coin agreeing; - fewer than 30 non-overlapping extreme-bar blocks pooled across the coins, or fewer than 30 neutral blocks.  

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

### opus (0.0599 USD)

Fidelity:  
- Situation: the RSI reaches a high extreme -> adapted: graded rather than a threshold. The position grows with how far the 14-bar RSI sits above 50. A squared dead zone keeps readings just above 50 small and lets extreme readings carry the largest positions. "After the RSI reaches an extreme" becomes "while the RSI is high".  
- Comparison: the move after neutral readings -> kept: neutral readings (RSI near 50) give a forecast near zero. The test compares what follows the largest positions with what follows near-zero ones, and also with the coin's average move over all bars.  
- Outcome: the price keeps rising over the following bars -> adapted: no holding period is set. The return is read over the next 5 bars while the position follows the RSI, and only the upward side is traded.  
- Verdict transfer: yes: the forecast is the RSI's high-side strength, so a forward return that rises after large forecasts relative to neutral bars and to holding is exactly the idea's claim, and its absence rejects it.  
Forecast: Use the 14-bar RSI on daily bars as RSIPullbackComponent, whose raw value is (50 − RSI) × 0.4. Standardise it against its own 60 previous values (target 10, cap 20), then negate it so it is positive when the RSI is above 50. Clip it at 0 to make it long-only, since the idea is about high extremes only. Finally apply signed_power with exponent 2 and pivot 10. The forecast is 0 when the RSI is 50 or below and small just above 50. Around the RSI's typical distance from 50 it is about +10, a 100% long position. At extreme readings it rises steeply and is capped at +20 (200% long). It is never negative.  
Config: 001-03_rsi-high-extreme-continuation_1d_config.json  
Criterion:  
- Horizon: 5 bars  
- Main measure: The coin's 5-bar forward return after "extreme" bars minus its 5-bar forward return over all bars, which is the return of simply holding the coin. Extreme bars are those with forecast ≥ 10. The comparison is made per coin and then pooled across the 3 coins and 6 windows. Only non-overlapping 5-bar blocks are counted: within a run of consecutive extreme bars, a case is taken only every 5th bar.  
- Supporting check: Compare the forward return after extreme bars with the forward return after neutral bars, those with forecast between 0 and 2. The idea needs extreme > neutral as well as extreme > holding.  
- Confirm: The pooled excess 5-bar forward return after extreme bars is > 0 with a t-statistic ≥ 2.0 on the non-overlapping cases. The excess is also positive in at least 2 of the 3 coins, and the supporting check shows extreme > neutral when pooled.  
- Reject: The pooled excess 5-bar forward return after extreme bars is ≤ 0 and is ≤ 0 in at least 2 of the 3 coins. A significantly negative pooled excess (t ≤ −2) also rejects; it would point to reversal instead of continuation.  
- Inconclusive: The pooled excess is positive but t < 2.0, or the coins disagree (only 1 of 3 positive while the pooled excess is positive), or extreme ≤ neutral despite a positive excess over holding. At least 40 non-overlapping extreme cases are needed pooled, with at least 10 per coin. Below that the result is inconclusive whatever its sign.  

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

## 002-01_sma-upcross-upward-drift

**The idea**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

### opus (0.0543 USD)

Fidelity:  
- Situation: a short moving average of price has just crossed above a long moving average -> adapted: "after the cross" becomes "while the short SMA stays above the long SMA". This is the state that begins at the upward cross and ends at the cross back, which the brief says ends the trend. The on/off cross event becomes graded by the percent spread between the two SMAs. Settings are the daily-bar convention, SMA 50 over SMA 200.  
- Comparison: price after random points -> kept: forward returns from active bars are compared with forward returns from all bars of the same windows, which is the same as simply holding the coin.  
- Outcome: price keeps rising over the following bars, more often and further -> kept: the up-share and the mean of forward returns after active bars, long side only.  
- Verdict transfer: yes: the forecast is non-zero exactly over the bars that follow an upward cross until the trend ends, so the direction and size of later returns on those bars, compared with all bars, confirm or reject the idea as stated.  
Forecast: The percent spread of the 50-bar SMA over the 200-bar SMA of the close is computed as (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own past 200 values, with window 200 and min_periods 50, so that an average spread reads about 10. It is capped at 20, then clipped at 0 from below. The forecast is zero while the short average is below the long one, which is before an upward cross or after a downward one. It is positive from the moment the 50-SMA crosses above the 200-SMA. It grows smoothly as the short average pulls further above the long one, to at most +20, which is a 200% long position. It is never negative.  
Config: 002-01_sma-upcross-upward-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: Take the BTC close-to-close return over the next 20 bars, starting at bars where the forecast is above 0. Use non-overlapping blocks: after a case is counted, the next one starts no earlier than 20 bars later. Compare these returns with 20-bar returns from non-overlapping blocks across all bars of the same six windows, which is buy-and-hold from random points. Two numbers are measured: the excess in mean 20-bar return, and the excess in the share of blocks that end up. Both are measured before costs.  
- Supporting check: Over all active bars, the Spearman rank correlation between the forecast size and the following 20-bar return, counted on non-overlapping blocks. It should be positive if a larger spread means a more established trend.  
- Confirm: Both of the following hold: - The mean 20-bar return after active bars exceeds the all-bars mean by at least +2 percentage points, with a one-sided t-statistic of at least 1.5 on non-overlapping blocks. - The up-share after active bars exceeds the all-bars up-share by at least 10 percentage points.  
- Reject: Any one of the following: - The excess mean 20-bar return is at or below 0. - The up-share after active bars is at or below the all-bars up-share. - The mean 20-bar return after active bars is negative in absolute terms, meaning moves after upward crosses reverse.  
- Inconclusive: These results neither confirm nor reject: - The excess mean is positive but below +2 points. - The t-statistic is below 1.5. - The up-share edge is between 0 and 10 points. Any result is also inconclusive if fewer than 10 non-overlapping active 20-bar blocks exist across the six windows, which is likely if the 50/200 state is rarely on.  

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

### opus (0.0730 USD)

Fidelity:  
- Situation: the stretch from an upward cross of the short SMA over the long SMA until the next downward cross, that is, the short average above the long one -> adapted: "after the up-cross, until the down-cross" becomes "while the short SMA is above the long SMA". The on/off state is made graded by the size of the spread (SMA50 − SMA200) / SMA200. The spread is 0 at the cross and grows as the averages separate. Short-average-below stretches give zero, because the idea speaks only of up-cross stretches.  
- Comparison: random stretches of the same length -> adapted: the coin's own return over all tested bars of the same windows, measured in equal-length non-overlapping blocks. This is the expected return and hit rate of a random stretch of that length.  
- Outcome: price rises more often and further over the stretch (upward) -> kept: forward coin returns while the stretch is active, measured as a hit rate and as an average size.  
- Verdict transfer: yes: the main measure uses every bar where the short SMA is above the long SMA, whatever the spread size, so a confirm or reject on it is a confirm or reject of the idea as stated. The spread grading is only checked separately.  
Forecast: One indicator, the SMA-pair spread (SMA50 − SMA200) / SMA200 in percent. This is the most common daily-bar convention, the "golden cross", and the brief gives no lengths. The spread is standardised against its own previous 200 values (min 50), so a typical spread maps to about 10, and the result is capped at 20. It is then clipped at 0 below. The forecast is positive while SMA50 is above SMA200, so from the up-cross until the down-cross. It grows smoothly from 0 at the cross as the short average pulls further above the long one. It is exactly 0 while SMA50 is at or below SMA200, so the position is flat outside the idea's stretches. It never goes short.  
Config: 002-05_sma-up-regime-positive-drift_1d_config.json  
Criterion:  
- Horizon: 20 bars  
- Main measure: The coin's 20-bar forward close-to-close return over non-overlapping 20-bar blocks. - The blocks start on bars where the forecast is > 0 and are taken consecutively within each window, so overlapping returns are counted once. - These are compared with the same non-overlapping 20-bar blocks taken over all bars of the six windows, which is the buy-and-hold random-stretch baseline. - The two quantities reported are the difference in mean block return and the difference in share of positive blocks. Both are before costs.  
- Supporting check: Is the spread size itself informative? Within in-stretch bars, compare the mean next-bar coin return when the forecast is above its in-stretch median with the mean when it is below. This is reported, but it does not decide the verdict.  
- Confirm: Both of the following hold, with at least the minimum counts below: - The in-stretch blocks' mean 20-bar return exceeds the all-bars blocks' mean by at least 3 percentage points, with a one-sided t ≥ 2.0 (Welch) on the block returns. - The in-stretch share of positive blocks exceeds the all-bars share by at least 10 percentage points.  
- Reject: Either of the following, with at least the minimum counts below: - The in-stretch mean 20-bar return is at or below the all-bars mean. - The in-stretch share of positive blocks is at or below the all-bars share. A negative excess with t ≤ −2.0 additionally shows reversal after up-crosses, the brief's second failure case.  
- Inconclusive: - A positive excess smaller than 3 points, or with t < 2.0, or with only one of the two differences meeting its bar. - Too few cases: fewer than 10 non-overlapping in-stretch 20-bar blocks, or fewer than 3 distinct up-cross-to-down-cross stretches (or stretches already active at a window's start) across the six windows. - Fewer than 25 all-bars blocks.  

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

### opus (0.0832 USD)

Fidelity:  
- Situation: a sharp upward move made on unusually low volume -> adapted: the volume part becomes an on/off regime condition. A veto fires on a daily up bar whose volume is below its 20-bar average, read from `VolumeExpansionHedgeComponent` in the detector, where on/off components are allowed. The sharpness part is graded: the size of that bar's rise (`PriceEvolutionComponent`, period 1), with a graded dead zone (`signed_power` 2) so small rises carry almost no position.  
- Comparison: none in this idea. "Part of the rise" sets only the direction, and the brief's high-volume contrast belongs to a sibling idea -> kept  
- Outcome: price falls back after the thin-volume rise (down) -> adapted: "after X" becomes "while X". The short is held only on the signal bar's close and judged on the next bar's return, so the multi-bar holding period is dropped.  
- Verdict transfer: yes: if the drift-adjusted next-bar return after low-volume up bars is reliably negative, the idea is confirmed at its shortest horizon; if it is zero or positive, nothing falls back and the idea is rejected.  
Forecast: On every daily bar the detector reads the volume-hedge value for the last 20 bars. - When the bar closed up on volume below its 20-bar average, a veto selects `mean_reversion`. On every other bar the regime is `unknown`, which is flat. - In `mean_reversion` the forecast is the bar's one-day percent change, standardised against its last 60 values (a typical absolute daily move gives 10, capped at 20). - That value goes through `signed_power` with exponent 2 and pivot 10. A small rise is damped towards 0, and a large one is amplified (15 becomes 22.5, final clip at 20). - It is then negated. Because the bar is an up bar, the forecast is always zero or negative: a short that grows with the size of the thin-volume rise. - It is zero on all bars outside the situation.  
Config: 003-01_low-volume-up-move-reverts_1d_config.json  
Criterion:  
- Horizon: 1 bar  
- Main measure: Pool all six windows. On every signal bar (forecast below 0), take the coin's next-bar close-to-close return. Measure its mean minus the mean next-bar return over all bars of the same windows. This is the drift-adjusted reversion, the edge over simply holding the coin, before costs. Each case is one non-overlapping 1-bar return, with a t-statistic on the signal-bar returns' excess.  
- Supporting check: Split the signal bars into halves by the absolute size of the forecast. The larger-forecast half (sharper thin-volume rises) should show a more negative drift-adjusted next-bar return than the smaller half.  
- Confirm: The drift-adjusted mean next-bar return on signal bars is negative with t ≤ -2.0. The strategy's cumulative return before costs is positive. The larger-forecast half is at least as negative as the smaller half.  
- Reject: The drift-adjusted mean next-bar return on signal bars is zero or positive, which means thin-volume rises do not fall back relative to the coin's normal drift. Or the larger-forecast half is clearly less negative than the smaller half, with the overall t above -1.0.  
- Inconclusive: The drift-adjusted mean is negative but with t between -2.0 and -1.0, or the supporting check contradicts the main measure. The result is also inconclusive if fewer than 60 signal bars occur across the six windows, whatever the result.  

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [
      {
        "id": "thinvol",
        "class": "strategies.strategy_components.VolumeExpansionHedgeComponent",
        "params": {
          "vol_period": 20,
          "scaling_factor": 20.0
        }
      }
    ],
    "vetoes": [
      {
        "id": "thinvol",
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
            "id": "rise",
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

### opus (0.0425 USD)

Fidelity:  
- Situation: a sharp price move made during the coin's quiet hours or on a weekend, while its volume is low -> replaced: on 1d bars the quiet hours sit inside a single bar and cannot be seen. A weekend day can only be told apart through the timestamp's day of week, and no component reads that. The most a config could hold is "a sharp daily move on a day whose volume is below its average", which is a different quantity.  
- Comparison: low volume during those hours, judged against the coin's normal (busier) volume -> adapted: volume below its N-bar average can be set as a regime condition (a veto with volume_filter), but only per day, not per hour.  
- Outcome: the move is partly reversed once the busier hours and normal volume return -> replaced: the return of the busy hours, and any reversal it brings, usually happens within the same day, so it falls inside the same daily bar. A daily config could only measure whether the next days move against the previous day's move.  
- Verdict transfer: no: the idea's move and its reversal both happen within the day. A daily test of low-volume days could confirm or reject something without bearing on quiet-hour or weekend moves, and an intraday reversal would never appear in it.  
Reason: The idea's situation (quiet hours) and its outcome (reversal when the busy hours return) both happen within a single 1d bar, so the data this test runs on does not contain them. The weekend part would also need the day of the week, which no part of the config can read.  

## 004-01_btc-up-move-alts-follow

**The idea**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

### opus (0.0196 USD)

Fidelity:  
- Situation: bitcoin has just made a sharp up move -> replaced: the config runs on one coin's own bars, and a component sees only its own symbol. A bitcoin move would have to come from bitcoin's bars while the position is held in an altcoin, and no component can read another coin's prices. The run's only coin is BTC/USDT, so bitcoin's move could be measured only as BTC's own past return.  
- Comparison: the altcoin's response to the bitcoin move, beyond the altcoin's own past returns -> replaced: this needs the altcoin's and bitcoin's returns side by side, two coins in one forecast, which the config cannot express.  
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only price traded is BTC/USDT, so the test would measure bitcoin following its own move (time-series momentum), not altcoins catching up.  
- Verdict transfer: no: a test of BTC following its own up moves says nothing about whether altcoins lag bitcoin, so neither a confirmation nor a rejection would carry over to the idea.  
Reason: The idea links two coins: the signal is bitcoin's move and the traded price is a smaller altcoin. The config sees only one symbol's own bars and feeds, and has no key for another coin's prices. The run also contains only BTC/USDT, so there is no altcoin to observe drifting.  

## 005-01_bearish-rsi-divergence-reversal

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

### opus (0.0422 USD)

Fidelity:  
- Situation: price makes a new high while RSI makes a lower high than it did at the previous price high -> replaced: no catalogue component, alone or combined, compares the RSI at the current price high with the RSI at the previous price high. `DonchianBreakoutComponent` shows that price is at the top of its range. `RSIPullbackComponent` gives only the current RSI level (50 - RSI). Taking one minus the other measures "price high while RSI is low", which is not the same as "RSI below its value at the prior peak". Ranking RSI against its own recent history would need `percentile` as a second history op beside `standardise`, which V15 refuses.  
- Comparison: the RSI at the previous price high, and, from the brief, new highs that come without a divergence -> replaced: no component stores or retrieves the RSI value at an earlier swing high.  
- Outcome: price falls after the divergent high and gives back part of the run-up (short side) -> adapted: the forecast is held while the divergence reading is present, and is judged on forward returns against holding the coin, with no fixed holding period.  
- Verdict transfer: no: built from the catalogue, the test would measure price range position against RSI level, not divergence between peaks, so its result would not confirm or reject the idea.  
Reason: The idea needs the RSI at the current price high compared with the RSI at the previous swing high. That value comes from the coin's own closes and could feed a graded forecast, but no catalogue component computes or remembers the RSI at a prior peak. The nearest compositions (Donchian position minus RSI level) measure a different quantity, and RSI ranked within its own window is blocked by the single-history-op rule.  

## 005-02_bullish-rsi-divergence-rebound

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

### opus (0.0482 USD)

Fidelity:  
- Situation: price closes at a new low below its previous swing low, while RSI(14) at this low is higher than RSI was at that previous low (bullish divergence) -> adapted: the new-low part can be read graded with `DonchianBreakoutComponent` (close at the bottom of its range), held "while" rather than "at" the low. The RSI-higher-low part cannot be built (see comparison).  
- Comparison: RSI at the current price low judged against RSI at the previous price low -> replaced: the catalogue can only give the current RSI level (`RSIPullbackComponent`) or that level against RSI's own past distribution. Neither reads RSI on the bar of the previous price low, so this part would have to be swapped for "price low while RSI is not oversold", which is a different quantity.  
- Outcome: price rebounds afterwards and recovers part of the decline into the low (long, up) -> kept: a long forecast while the divergence is present, with forward returns judged against holding the coin.  
- Verdict transfer: no: with the comparison replaced, a test of "low price, non-extreme RSI" could confirm or reject without saying anything about RSI making a higher low than at the previous price low.  
Reason: A bullish divergence needs RSI's value on the bar of the previous swing low in price, compared with RSI now. Both come from the coin's own closes and a per-bar forecast could hold the result. But no catalogue component, alone or combined through weights, negation, offsets or history ops, finds the previous price low and reads RSI there. The only compositions available, such as Donchian position combined with RSI level, or RSI against its own history, measure something else.  

## 005-03_divergent-high-weaker-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

### opus (0.0440 USD)

Fidelity:  
- Situation: the close makes a new price high (above its recent highs) -> adapted: graded as where the close sits in its recent range (`DonchianBreakoutComponent`, near +sf at a new high), or as a regime rule on that value reaching its top. "After a new high" becomes "while at or near a new high".  
- Comparison: whether the RSI at the new price high is below or above RSI's own earlier high (divergence against confirmation) -> replaced: the catalogue gives only the current RSI level (`RSIPullbackComponent`, 50 - RSI). No component and no allowed transform chain compares RSI with its own rolling maximum. `standardise` must be the only history op, and `percentile` in `history_transforms` sees a single value. Using the RSI level would answer the brief's excluded question (RSI extremes), not divergence.  
- Outcome: forward returns after divergent new highs are weaker than after confirmed new highs (a fade, short or less long) -> kept: a forecast that grows short with the size of the divergence at a new high, judged on its forward returns against holding the coin.  
- Verdict transfer: no. Without the RSI-against-its-own-high comparison, the test would measure RSI level at new highs, not divergence, so neither a confirm nor a reject would carry over to the idea.  
Reason: Everything the idea needs comes from one coin's own closes, and the config's logic could hold it: a regime or graded weight on "price at its range top" times a graded RSI shortfall. No catalogue component measures where the current RSI sits relative to its own recent high, and no composition of the existing components or ops can build that from RSI's history.  

## 005-04_divergent-low-stronger-than-confirmed

**The idea**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

### opus (0.0427 USD)

Fidelity:  
- Situation: the close makes a new low over a recent window, while RSI stays above the low it made at the earlier price low (a higher RSI low) -> replaced: no catalogue component, alone or combined, measures RSI against its own earlier low. `DonchianBreakoutComponent` can mark the new price low (a regime rule on its raw value at -sf). But `RSIPullbackComponent` only gives the RSI level (50 - RSI), and an RSI level at a new low is not the same as RSI being above its earlier low.  
- Comparison: new price lows where RSI also makes a new low (confirming momentum) -> replaced: this needs the same RSI-against-its-own-earlier-low measure, so it cannot be separated from divergent lows with the existing components.  
- Outcome: price rises more after divergent new lows than after confirming new lows -> adapted: "after the low" becomes "while the new-low regime is active", with the long position graded by the divergence strength and no holding period.  
- Verdict transfer: no: using the RSI level at a new low in place of RSI against its prior low tests whether oversold lows bounce, which the brief explicitly says is not its question, so neither a confirmation nor a rejection would carry over to the divergence idea.  
Reason: The idea needs RSI compared with its own value at the previous price low, which comes from one coin's closes and fits the config's logic. That logic would be a regime on "close at its window low" (Donchian raw at -sf) plus a graded long component sized by how far RSI sits above its window low. No catalogue component gives RSI's position within its own recent range, and no composition of the existing components (RSI level, price range position, the transforms) produces it.  

## 005-05_bearish-divergence-uptrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

### opus (0.0402 USD)

Fidelity:  
- Situation: price closes at a new high (the highest close of its recent window) -> adapted: the threshold "new high" becomes a regime rule on `DonchianBreakoutComponent` (period 20, the usual 20-day high; raw value `gte` 20 means the close is the highest close of the window). The condition is the idea itself, so a regime fits it.  
- Comparison: RSI at this new price high is lower than RSI was at the earlier price high (a lower RSI high) -> replaced: no component or combination in the catalogue measures RSI against its own earlier peak. `RSIPullbackComponent` gives only the RSI level against 50. `standardise` divides by a past mean and does not subtract a past maximum. The rule and veto operators compare a value with a fixed constant, not with an earlier value of RSI.  
- Outcome: price keeps rising to further highs over the following bars (long, continuation) -> kept: a long position that is larger when the divergence is larger, judged on later returns against holding the coin.  
- Verdict transfer: no: standing in for "RSI below its earlier high" with "RSI below 50" or with plain RSI weakness tests a different quantity, so neither a confirmation nor a rejection would carry over to the divergence idea.  
Reason: Every input to the divergence comes from one coin's closes, and the config could hold it: a regime for "close at a new high" plus a graded long component for "how far RSI sits below its earlier high". But no catalogue component computes RSI relative to its own recent peak, and no composition of the existing components or ops (weights, negate, standardise, clip, regime rules against constants) can produce a rolling maximum of RSI.  

## 005-06_bullish-divergence-downtrend-continues

**The idea**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### opus (0.0453 USD)

Fidelity:  
- Situation: price makes a new low while RSI makes a higher low (a bullish price-RSI divergence) -> replaced: the catalogue has the RSI level (`RSIPullbackComponent`, 50 - RSI) and the close's place in its range (`DonchianBreakoutComponent`), but nothing compares the current RSI low with RSI's earlier low. Any combination of the two would measure "price low while RSI is below or above 50", not the divergence.  
- Comparison: the new price low is judged against the earlier price low, and the RSI low against the earlier RSI low -> replaced: the price half can be kept with Donchian's range position on closes. The RSI half has no counterpart, since no component places RSI within its own recent range or against its own prior trough.  
- Outcome: price keeps falling to further lows after the divergence -> kept: this is a short position whose size grows with the divergence's strength, judged on the next bars' returns.  
- Verdict transfer: no: a test built on RSI's level or price's range position alone would confirm or reject a statement about oversold lows, not about a higher RSI low under a lower price low.  
Reason: The divergence uses only the coin's own closes, and the config could hold it as one graded short signal. No catalogue component, alone or combined, measures RSI against its own earlier low, so the "higher RSI low" half of the situation cannot be built. RSI level, the Donchian range position and RSI pullback measure different things.  
