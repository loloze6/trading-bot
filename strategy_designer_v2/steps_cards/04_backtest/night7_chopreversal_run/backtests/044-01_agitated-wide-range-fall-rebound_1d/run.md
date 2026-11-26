# Backtest of 044-01_agitated-wide-range-fall-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/044-01_agitated-wide-range-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.065935 | -7.323 |
| w2 | 24 | 0.087892 | 0.926 |
| w3 | 18 | 0.240103 | 20.057 |
| w4 | 10 | 0.112709 | 12.123 |
| w5 | 0 | None | 0.0 |
| w6 | 23 | 0.227838 | 51.648 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.013491 | 1.626 |
| w9 | 13 | -0.008043 | -4.139 |
| w10 | 15 | 0.030081 | 7.94 |
| w11 | 33 | 0.069702 | 23.066 |
| w12 | 12 | 0.063424 | 6.122 |
| w13 | 35 | -0.003659 | -2.713 |
| w14 | 14 | 0.211366 | 19.06 |
| w15 | 38 | -0.099155 | -7.879 |
| w16 | 15 | 0.224674 | 15.621 |
| w17 | 18 | 0.017204 | 10.99 |
| w18 | 37 | 0.206057 | 31.229 |
| w19 | 33 | 0.069341 | 19.429 |
| w20 | 43 | 0.057397 | 1.926 |
| w21 | 18 | 0.08228 | 15.91 |
| w22 | 22 | 0.216515 | 27.074 |
| w23 | 2 | -0.013981 | -0.146 |
| w24 | 31 | 0.006948 | -10.173 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.13694 | -12.925 |
| w2 | 46 | 0.068137 | -4.742 |
| w3 | 20 | 0.304896 | 29.64 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 20 | 0.148382 | 24.577 |
| w7 | 0 | None | 0.0 |
| w8 | 15 | 0.139831 | 10.062 |
| w9 | 10 | 0.060252 | 3.97 |
| w10 | 18 | 0.060887 | 9.62 |
| w11 | 33 | 0.069474 | 29.663 |
| w12 | 8 | 0.067005 | 4.854 |
| w13 | 16 | -0.135387 | -18.7 |
| w14 | 34 | 0.221278 | 26.894 |
| w15 | 20 | 0.038727 | 4.784 |
| w16 | 27 | -0.04816 | -17.329 |
| w17 | 20 | 0.028813 | 4.207 |
| w18 | 32 | 0.137819 | 27.395 |
| w19 | 30 | -0.098705 | -18.442 |
| w20 | 39 | 0.121887 | 6.291 |
| w21 | 34 | 0.021753 | 8.047 |
| w22 | 41 | 0.080467 | -1.391 |
| w23 | 18 | 0.098081 | 24.387 |
| w24 | 19 | 0.02726 | -4.648 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 28 | 0.078532 | 3.179 |
| w3 | 16 | 0.162592 | 17.072 |
| w4 | 9 | 0.131678 | 9.006 |
| w5 | 21 | 0.029054 | -0.771 |
| w6 | 1 | 0.066606 | 2.101 |
| w7 | 0 | None | 0.0 |
| w8 | 39 | 0.036818 | 17.053 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | 0.014401 | 0.569 |
| w11 | 38 | -0.14288 | -15.015 |
| w12 | 21 | -0.02921 | -7.204 |
| w13 | 20 | -0.058185 | -3.246 |
| w14 | 26 | 0.191287 | 18.28 |
| w15 | 26 | 0.163173 | 17.172 |
| w16 | 20 | -0.003149 | -11.812 |
| w17 | 25 | 0.072895 | 16.159 |
| w18 | 27 | 0.203449 | 22.656 |
| w19 | 29 | 0.154559 | 33.248 |
| w20 | 21 | 0.108334 | 4.416 |
| w21 | 34 | -0.044334 | -4.155 |
| w22 | 43 | -0.064454 | -12.363 |
| w23 | 10 | 0.137179 | 12.975 |
| w24 | 18 | -0.042536 | -6.205 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.0437 | -11.641 |
| w2 | 25 | -0.031739 | -11.067 |
| w3 | 9 | 0.134437 | 7.316 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.048655 | 2.594 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.050413 | 1.56 |
| w9 | 2 | 0.032825 | 0.531 |
| w10 | 5 | 0.077282 | 5.397 |
| w11 | 34 | 0.034014 | 22.321 |
| w12 | 10 | -0.000556 | -4.395 |
| w14 | 27 | 0.142634 | 7.591 |
| w15 | 25 | 0.010784 | 0.456 |
| w16 | 30 | 0.01572 | -6.067 |
| w17 | 19 | -0.025932 | -4.74 |
| w18 | 30 | 0.219722 | 35.513 |
| w19 | 40 | 0.232883 | 43.434 |
| w20 | 26 | 0.170828 | 23.278 |
| w21 | 15 | 0.10368 | 14.905 |
| w22 | 24 | 0.047743 | 7.255 |
| w23 | 25 | -0.173407 | -25.716 |
| w24 | 31 | -0.053935 | -2.241 |

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
| w1 | 7 | 0.133528 | 3.189 |
| w2 | 0 | -0.05352 | 0.0 |
| w3 | 0 | 0.157707 | 0.0 |
| w4 | 0 | 0.074562 | 0.0 |
| w5 | 20 | -0.016541 | 1.617 |
| w6 | 13 | 0.07579 | 8.872 |
| w8 | 4 | 0.070879 | 1.925 |
| w9 | 12 | 0.039587 | 0.989 |
| w10 | 7 | 0.097356 | 11.324 |
| w11 | 43 | 0.026058 | 28.424 |
| w12 | 4 | -0.009191 | -0.815 |
| w14 | 14 | 0.128929 | 12.759 |
| w15 | 17 | 0.061426 | 4.998 |
| w16 | 36 | -0.010671 | -11.507 |
| w17 | 27 | 0.05033 | 15.562 |
| w18 | 26 | 0.193039 | 17.115 |
| w19 | 31 | -0.007 | -3.706 |
| w20 | 20 | -0.034414 | -3.432 |
| w21 | 29 | -0.011728 | 23.103 |
| w22 | 43 | 0.017355 | -2.379 |
| w23 | 9 | 0.08762 | 8.125 |
| w24 | 10 | 0.029548 | -0.83 |

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
| w1 | 13 | 0.128981 | 11.496 |
| w2 | 32 | 0.13338 | 9.966 |
| w3 | 7 | 0.274677 | 13.271 |
| w4 | 6 | -0.037612 | -1.906 |
| w5 | 15 | 0.081532 | 5.26 |
| w6 | 8 | 0.101757 | 9.192 |
| w7 | 7 | -0.029014 | -4.037 |
| w8 | 5 | 0.142473 | 3.273 |
| w9 | 18 | 0.156875 | 12.327 |
| w10 | 19 | -0.089913 | -3.293 |
| w11 | 36 | -0.032214 | 11.599 |
| w12 | 25 | -0.004183 | -1.716 |
| w13 | 28 | 0.094345 | 8.81 |
| w14 | 23 | 0.158743 | 11.99 |
| w15 | 25 | 0.027548 | -3.206 |
| w16 | 41 | -0.040325 | 0.513 |
| w17 | 25 | 0.012829 | -5.836 |
| w18 | 35 | 0.270678 | 43.445 |
| w19 | 53 | 0.09152 | 2.758 |
| w20 | 40 | -0.045143 | -2.473 |
| w21 | 41 | -0.038096 | 3.59 |
| w22 | 39 | -0.070947 | -18.886 |
| w23 | 11 | -0.075649 | -7.398 |
| w24 | 37 | -0.067428 | 8.099 |

