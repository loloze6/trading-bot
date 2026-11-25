# Backtest of 046-01_calm-scaled-rise-second-day-continues_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/046-01_calm-scaled-rise-second-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.118428 | -17.441 |
| w2 | 19 | 0.071141 | 0.604 |
| w3 | 29 | 0.034237 | -0.2 |
| w4 | 36 | 0.024505 | 27.831 |
| w5 | 43 | 0.057879 | -0.144 |
| w6 | 22 | -0.016012 | 7.558 |
| w7 | 52 | 0.094668 | 6.32 |
| w8 | 35 | 0.003873 | 5.066 |
| w9 | 30 | 0.033217 | -3.877 |
| w10 | 38 | 0.127921 | 27.532 |
| w11 | 11 | -0.039793 | -0.777 |
| w12 | 36 | -0.258582 | -30.737 |
| w13 | 18 | -0.046051 | -5.38 |
| w14 | 31 | 0.000847 | -11.589 |
| w15 | 6 | 0.195137 | 40.798 |
| w16 | 27 | 0.000585 | 2.568 |
| w17 | 35 | -0.077748 | 14.74 |
| w18 | 16 | 0.119191 | 18.666 |
| w19 | 9 | 0.274574 | 35.442 |
| w20 | 14 | 0.068266 | 7.693 |
| w21 | 31 | -0.042232 | 7.446 |
| w22 | 24 | -0.064752 | -9.783 |
| w23 | 53 | -0.004871 | -2.27 |
| w24 | 24 | 0.03437 | -2.928 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.021733 | -9.648 |
| w2 | 3 | -0.026688 | -3.691 |
| w3 | 24 | -0.01363 | -4.817 |
| w4 | 56 | 0.045211 | 23.133 |
| w5 | 45 | 0.025584 | -3.294 |
| w6 | 37 | 0.052663 | 23.819 |
| w7 | 46 | 0.092186 | -3.393 |
| w8 | 28 | 0.055948 | 7.731 |
| w9 | 38 | 0.106745 | 11.114 |
| w10 | 37 | 0.221359 | 71.693 |
| w11 | 18 | -0.018979 | 8.372 |
| w12 | 41 | -0.070888 | -10.544 |
| w13 | 24 | 0.075543 | 11.014 |
| w14 | 11 | -0.040206 | -7.608 |
| w15 | 34 | 0.024436 | 7.482 |
| w16 | 22 | 0.109422 | 39.973 |
| w17 | 26 | 0.024347 | 13.288 |
| w18 | 22 | 0.117527 | 24.456 |
| w19 | 17 | 0.179315 | 39.84 |
| w20 | 7 | 0.071246 | 3.893 |
| w21 | 17 | -0.00177 | 3.506 |
| w22 | 8 | -0.135216 | -12.298 |
| w23 | 33 | -0.073551 | 8.352 |
| w24 | 26 | -0.043795 | -9.404 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.029429 | -16.236 |
| w2 | 22 | 0.029508 | -1.465 |
| w3 | 34 | 0.012987 | 5.488 |
| w4 | 42 | -0.025474 | -7.174 |
| w5 | 26 | 0.045971 | 4.249 |
| w6 | 52 | -0.188171 | -26.21 |
| w7 | 43 | 0.079947 | -5.538 |
| w8 | 11 | -0.010784 | 1.575 |
| w9 | 46 | 0.134628 | 7.169 |
| w10 | 49 | 0.084217 | 23.257 |
| w11 | 7 | 0.010925 | 3.372 |
| w12 | 38 | -0.056531 | -11.072 |
| w13 | 26 | -0.013473 | -3.164 |
| w14 | 22 | 0.047508 | -1.311 |
| w15 | 18 | -0.161373 | -16.424 |
| w16 | 32 | 0.042198 | 16.919 |
| w17 | 17 | -0.047649 | -2.104 |
| w18 | 23 | 0.134143 | 26.896 |
| w19 | 16 | 0.067531 | 11.24 |
| w20 | 22 | -0.137665 | -22.49 |
| w21 | 18 | -0.061311 | -4.404 |
| w22 | 3 | -0.138756 | -5.054 |
| w23 | 40 | -0.037271 | -3.397 |
| w24 | 26 | -0.094257 | -16.281 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.070579 | 6.572 |
| w2 | 22 | 0.041627 | 0.732 |
| w3 | 43 | 0.011197 | -2.275 |
| w4 | 53 | -0.048554 | -16.999 |
| w5 | 59 | 0.15358 | 3.993 |
| w6 | 49 | 0.105078 | 10.161 |
| w7 | 45 | 0.088779 | -0.037 |
| w8 | 43 | 0.028062 | 8.079 |
| w9 | 46 | 0.005802 | -14.738 |
| w10 | 56 | 0.040595 | 20.173 |
| w11 | 16 | 0.14027 | 29.549 |
| w12 | 39 | -0.20865 | -32.58 |
| w14 | 28 | -0.086956 | -22.782 |
| w15 | 28 | 0.057333 | 7.926 |
| w16 | 22 | 0.151558 | 44.437 |
| w17 | 32 | 0.041721 | 8.942 |
| w18 | 21 | 0.099175 | 24.689 |
| w19 | 1 | -0.144092 | -16.574 |
| w20 | 18 | 0.021249 | 5.551 |
| w21 | 23 | 0.057534 | 8.935 |
| w22 | 25 | 0.035467 | 6.036 |
| w23 | 28 | 0.098453 | 7.744 |
| w24 | 9 | -0.184028 | -15.051 |

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
| w1 | 42 | -0.013533 | -8.097 |
| w2 | 4 | 0.143494 | 0.344 |
| w3 | 0 | -0.045758 | 0.0 |
| w4 | 0 | 0.133291 | 0.0 |
| w5 | 12 | 0.017932 | -6.372 |
| w6 | 35 | 0.070845 | 17.671 |
| w8 | 38 | -0.011129 | -6.331 |
| w9 | 31 | -0.012626 | -9.27 |
| w10 | 46 | 0.170399 | 45.274 |
| w11 | 0 | None | 0.0 |
| w12 | 50 | -0.087002 | -19.827 |
| w14 | 28 | 0.026066 | 5.184 |
| w15 | 31 | -0.060523 | -8.113 |
| w16 | 12 | -0.024324 | -1.247 |
| w17 | 23 | 0.086454 | 42.478 |
| w18 | 28 | 0.145231 | 30.737 |
| w19 | 24 | 0.02088 | -1.641 |
| w20 | 22 | -0.066472 | -12.204 |
| w21 | 17 | -0.003698 | 22.652 |
| w22 | 4 | -0.093731 | -5.085 |
| w23 | 43 | 0.075856 | 18.965 |
| w24 | 35 | -0.154634 | -23.456 |

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
| w1 | 36 | -0.036978 | -5.644 |
| w2 | 23 | 0.092828 | 5.915 |
| w3 | 38 | -0.143416 | -25.056 |
| w4 | 48 | 0.053398 | 1.619 |
| w5 | 34 | -0.100443 | -18.116 |
| w6 | 57 | 0.062264 | 12.431 |
| w7 | 39 | 0.080405 | 3.361 |
| w8 | 39 | -0.026929 | -7.426 |
| w9 | 27 | 0.078606 | 2.872 |
| w10 | 34 | -0.023261 | 7.214 |
| w11 | 18 | -0.010944 | 6.4 |
| w12 | 28 | 0.039063 | 2.085 |
| w13 | 20 | -0.003421 | -4.256 |
| w14 | 30 | -0.014666 | -16.438 |
| w15 | 28 | 0.039841 | 2.139 |
| w16 | 0 | None | 0.0 |
| w17 | 24 | -0.002843 | -2.865 |
| w18 | 25 | 0.111917 | 22.726 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | -0.055006 | -4.409 |
| w21 | 11 | -0.041659 | -2.596 |
| w22 | 3 | 0.01998 | 0.233 |
| w23 | 35 | -0.152883 | -24.056 |
| w24 | 10 | -0.066046 | -0.4 |

