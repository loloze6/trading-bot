# Backtest of 061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.098341 | -27.403 |
| w2 | 10 | -0.000894 | -33.595 |
| w3 | 9 | 0.014123 | -36.932 |
| w4 | 13 | 0.054489 | 32.893 |
| w5 | 17 | -0.114233 | -27.333 |
| w6 | 11 | -0.045349 | 31.49 |
| w7 | 16 | 0.069387 | 18.22 |
| w8 | 9 | -0.11992 | 47.646 |
| w9 | 16 | -0.047031 | 5.058 |
| w10 | 10 | 0.00111 | 10.636 |
| w11 | 4 | -0.031893 | -5.748 |
| w12 | 14 | -0.073791 | -27.555 |
| w13 | 4 | -0.116357 | 1.162 |
| w14 | 6 | 0.003976 | -10.691 |
| w15 | 1 | 0.140999 | 51.423 |
| w16 | 15 | -0.013855 | -0.254 |
| w17 | 12 | -0.04114 | 76.802 |
| w18 | 10 | 0.104624 | 19.322 |
| w19 | 5 | 0.192827 | 29.705 |
| w20 | 10 | 0.020611 | -3.549 |
| w21 | 15 | 0.213407 | 46.69 |
| w22 | 18 | -0.161479 | -29.201 |
| w23 | 25 | -0.020402 | 16.404 |
| w24 | 6 | 0.135171 | -1.509 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.019519 | 10.219 |
| w2 | 5 | -0.151302 | -33.424 |
| w3 | 10 | 0.02074 | -34.745 |
| w4 | 28 | 0.092167 | 36.077 |
| w5 | 20 | -0.163329 | -25.829 |
| w6 | 15 | -0.008347 | 37.534 |
| w7 | 14 | -0.075967 | -18.463 |
| w8 | 9 | -0.099732 | 11.337 |
| w9 | 15 | -0.026584 | -19.267 |
| w10 | 13 | 0.031468 | 89.211 |
| w11 | 8 | -0.011938 | 20.211 |
| w12 | 19 | -0.068425 | -4.011 |
| w13 | 8 | -0.133417 | -4.856 |
| w14 | 2 | -0.001163 | -14.645 |
| w15 | 17 | 0.049737 | 35.129 |
| w16 | 9 | 0.014647 | 72.573 |
| w17 | 10 | 0.085605 | 40.288 |
| w18 | 7 | -0.013506 | 20.785 |
| w19 | 11 | 0.064611 | 89.384 |
| w20 | 6 | -0.111732 | -7.104 |
| w21 | 6 | -0.06976 | -21.875 |
| w22 | 3 | 0.013415 | -18.225 |
| w23 | 15 | 0.084036 | 50.059 |
| w24 | 7 | 0.017304 | -16.496 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.05551 | -11.51 |
| w2 | 14 | -0.059716 | -31.816 |
| w3 | 14 | 0.07138 | -12.818 |
| w4 | 20 | 0.0279 | -13.219 |
| w5 | 8 | 0.06366 | -8.006 |
| w6 | 22 | -0.075183 | -17.004 |
| w7 | 14 | -0.067477 | -11.252 |
| w8 | 2 | -0.072765 | -3.435 |
| w9 | 17 | -0.014551 | -16.286 |
| w10 | 17 | -0.152014 | 17.881 |
| w11 | 4 | -0.012797 | 27.702 |
| w12 | 14 | 0.012459 | -15.514 |
| w13 | 7 | -0.16544 | -7.618 |
| w14 | 10 | -0.084452 | -34.518 |
| w15 | 6 | 0.024045 | 9.266 |
| w16 | 11 | -0.065084 | 20.044 |
| w17 | 6 | -0.008222 | -4.598 |
| w18 | 11 | 0.008183 | 18.457 |
| w19 | 9 | 0.125556 | 3.262 |
| w20 | 6 | -0.004796 | -14.05 |
| w21 | 8 | 0.04305 | 10.082 |
| w22 | 0 | None | 0.0 |
| w23 | 25 | 0.068096 | 11.384 |
| w24 | 8 | -0.184529 | -33.612 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.021846 | -7.024 |
| w2 | 11 | -0.004814 | -9.132 |
| w3 | 9 | -0.044901 | -18.659 |
| w4 | 17 | 0.060717 | 16.915 |
| w5 | 16 | 0.115016 | -14.191 |
| w6 | 17 | -0.013235 | 10.527 |
| w7 | 19 | -0.089007 | -17.578 |
| w8 | 14 | 0.033683 | 37.184 |
| w9 | 18 | -0.043118 | -16.108 |
| w10 | 19 | -0.058908 | 22.386 |
| w11 | 7 | -0.038905 | 35.225 |
| w12 | 18 | -0.052931 | -23.205 |
| w14 | 8 | 0.079483 | -22.979 |
| w15 | 14 | 0.184515 | 26.839 |
| w16 | 11 | -0.078121 | 18.472 |
| w17 | 9 | -0.134391 | 11.937 |
| w18 | 14 | 0.045327 | 13.346 |
| w19 | 2 | -0.017154 | -19.827 |
| w20 | 9 | -0.01138 | -3.317 |
| w21 | 13 | 0.185117 | 37.163 |
| w22 | 4 | 0.002515 | 14.928 |
| w23 | 11 | 0.05868 | -18.218 |
| w24 | 3 | 0.064194 | -9.389 |

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
| w1 | 11 | -0.015366 | 16.427 |
| w2 | 4 | -0.099703 | -24.341 |
| w3 | 0 | 0.003196 | 0.0 |
| w4 | 0 | -0.08783 | 0.0 |
| w5 | 0 | -0.024216 | 0.0 |
| w6 | 13 | 0.017933 | 22.653 |
| w8 | 14 | -0.216773 | -10.427 |
| w9 | 15 | -0.025864 | -12.816 |
| w10 | 6 | 0.040019 | 58.562 |
| w11 | 0 | None | 0.0 |
| w12 | 19 | 0.084353 | -8.041 |
| w14 | 9 | -0.037226 | 36.994 |
| w15 | 7 | 0.18682 | 0.992 |
| w16 | 6 | 0.105906 | -1.882 |
| w17 | 10 | 0.153993 | 221.767 |
| w18 | 9 | 0.068326 | 31.225 |
| w19 | 14 | -0.023552 | 7.053 |
| w20 | 10 | -0.157329 | 1.584 |
| w21 | 7 | 0.061084 | 84.292 |
| w22 | 1 | -0.031192 | -14.375 |
| w23 | 16 | 0.143406 | 32.063 |
| w24 | 10 | 0.005044 | -11.279 |

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
| w1 | 12 | 0.101319 | 21.421 |
| w2 | 8 | 0.035996 | 6.59 |
| w3 | 14 | -0.054623 | -54.189 |
| w4 | 21 | -0.104477 | -0.802 |
| w5 | 6 | -0.024907 | -29.754 |
| w6 | 20 | -0.215002 | -30.216 |
| w7 | 12 | 0.012825 | -29.872 |
| w8 | 21 | -0.084883 | 42.869 |
| w9 | 10 | -0.011207 | 11.282 |
| w10 | 17 | 0.004617 | 51.87 |
| w11 | 9 | 0.094102 | 27.524 |
| w12 | 11 | -0.015422 | -21.767 |
| w13 | 8 | 0.058092 | 1.02 |
| w14 | 10 | 0.034759 | -3.884 |
| w15 | 13 | -0.00062 | -17.344 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.003511 | -1.6 |
| w18 | 8 | -0.052179 | 17.986 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.091231 | -2.556 |
| w21 | 8 | 0.03424 | 21.157 |
| w22 | 1 | -0.047379 | -6.042 |
| w23 | 14 | 0.193123 | 6.664 |
| w24 | 3 | -0.05631 | 6.0 |

