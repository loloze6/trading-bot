# Backtest of 060-01.d1_wide-day-high-close-next-day-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.d1_wide-day-high-close-next-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.002333 | 0.06 |
| w2 | 15 | 0.023753 | 6.236 |
| w3 | 5 | 0.03132 | 3.088 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.058489 | -2.794 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.066107 | 0.446 |
| w9 | 6 | -0.12896 | -5.692 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.092316 | -0.814 |
| w13 | 13 | 0.074769 | 5.454 |
| w14 | 11 | 0.014148 | 1.757 |
| w15 | 1 | 0.057941 | 0.453 |
| w16 | 3 | 0.092629 | 4.325 |
| w17 | 0 | None | 0.0 |
| w18 | 14 | -0.072964 | -6.133 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.03003 | 0.926 |
| w21 | 0 | None | 0.0 |
| w22 | 8 | 0.04123 | 1.539 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.022359 | 3.28 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.006965 | 0.007 |
| w2 | 17 | -0.062944 | -5.66 |
| w3 | 3 | -0.065816 | -1.966 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.01235 | 0.03 |
| w9 | 2 | -0.09848 | -3.175 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 19 | 0.045466 | 9.97 |
| w15 | 2 | -0.103206 | -1.213 |
| w16 | 3 | 0.047054 | 2.064 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.060035 | -1.201 |
| w19 | 1 | None | -0.014 |
| w20 | 11 | 0.034217 | 1.933 |
| w21 | 3 | 0.062848 | 1.757 |
| w22 | 22 | 0.239365 | 35.105 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | -0.125245 | -8.12 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 13 | -0.025561 | 1.574 |
| w3 | 1 | -0.393083 | -4.923 |
| w4 | 1 | -0.072958 | -0.483 |
| w5 | 6 | 0.007291 | 0.389 |
| w6 | 4 | -0.066728 | -3.76 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.085195 | 2.314 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.071156 | -1.205 |
| w13 | 1 | -0.055164 | -1.579 |
| w14 | 15 | -0.059438 | -5.123 |
| w15 | 4 | -0.059077 | -1.458 |
| w16 | 5 | 0.074223 | 3.246 |
| w17 | 2 | 0.026025 | 0.207 |
| w18 | 2 | -0.311092 | -6.662 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.024364 | 1.73 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | 0.084913 | 5.572 |
| w23 | 2 | -0.019343 | -1.136 |
| w24 | 8 | -0.064261 | -2.913 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.041527 | 2.088 |
| w2 | 9 | -0.006425 | -2.255 |
| w3 | 1 | -0.010231 | -0.291 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.008724 | -0.588 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.003795 | -0.059 |
| w9 | 2 | -0.020876 | -0.3 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 8 | 0.047526 | 4.474 |
| w15 | 0 | -0.094553 | 0.0 |
| w16 | 3 | 0.004422 | -0.41 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.22444 | -6.644 |
| w19 | 14 | -0.063978 | -2.081 |
| w20 | 1 | -0.298286 | -1.313 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.227224 | -16.141 |
| w24 | 2 | -0.008338 | -1.34 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.045757 | 9.339 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.012488 | -0.604 |
| w8 | 1 | -0.012442 | -0.062 |
| w9 | 3 | 0.039979 | 2.097 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.08658 | -9.024 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.035502 | 1.879 |
| w15 | 3 | -0.085669 | -2.692 |
| w16 | 6 | 0.110802 | 8.284 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | 0.103423 | 4.159 |
| w19 | 6 | -0.093968 | -4.733 |
| w20 | 2 | 0.008854 | -0.488 |
| w21 | 3 | 0.006075 | -2.034 |
| w22 | 5 | 0.090595 | 3.731 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.052188 | -3.489 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 13 | -0.002305 | 0.141 |
| w3 | 3 | -0.097927 | -4.926 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | -0.091404 | -4.543 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.063448 | 0.382 |
| w8 | 1 | -0.076746 | -0.499 |
| w9 | 7 | -0.051206 | -3.048 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 7 | -0.070767 | -4.597 |
| w15 | 4 | 0.055087 | 1.469 |
| w16 | 10 | 0.088623 | 4.8 |
| w17 | 6 | -0.066579 | -3.315 |
| w18 | 4 | -0.230256 | -7.588 |
| w19 | 10 | -0.166698 | -13.198 |
| w20 | 4 | -0.170906 | -16.52 |
| w21 | 2 | -0.024288 | -3.938 |
| w22 | 14 | -0.063042 | -7.481 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

