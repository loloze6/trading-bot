# Backtest of 043-01_falling-agitated-intraday-drop-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/043-01_falling-agitated-intraday-drop-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.038413 | -5.525 |
| w2 | 27 | 0.100216 | 2.9 |
| w3 | 21 | 0.19732 | 22.103 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 5.213 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.067286 | 3.175 |
| w9 | 11 | -0.066612 | -9.636 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 4.104 |
| w13 | 22 | 0.10692 | 13.512 |
| w14 | 20 | 0.183362 | 19.341 |
| w15 | 5 | -0.077045 | -3.76 |
| w16 | 18 | 0.263082 | 34.748 |
| w17 | 0 | None | 0.0 |
| w18 | 38 | 0.131946 | 16.37 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.131849 | 11.129 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.212968 | 30.872 |
| w23 | 0 | None | 0.0 |
| w24 | 21 | 0.026312 | -2.977 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.165286 | -18.586 |
| w2 | 36 | 0.013541 | -13.877 |
| w3 | 14 | 0.234194 | 23.65 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 14 | 0.169165 | 14.569 |
| w9 | 11 | 0.079269 | 5.719 |
| w10 | 2 | 0.122181 | 1.508 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 39 | 0.184796 | 22.04 |
| w15 | 7 | -0.028689 | -3.321 |
| w16 | 21 | 0.223492 | 31.52 |
| w17 | 1 | -0.006609 | 0.045 |
| w18 | 12 | 0.036089 | 4.697 |
| w19 | 1 | None | -0.057 |
| w20 | 25 | 0.093765 | -2.73 |
| w21 | 9 | 0.013472 | 2.675 |
| w22 | 39 | 0.079227 | -3.462 |
| w23 | 2 | 0.069674 | 0.019 |
| w24 | 12 | 0.158232 | 12.339 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 32 | 0.081403 | 3.952 |
| w3 | 1 | 0.393083 | 19.101 |
| w4 | 2 | 0.074314 | 3.132 |
| w5 | 8 | 0.002429 | -2.435 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.008838 | 3.271 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.08206 | 5.47 |
| w13 | 7 | 0.087076 | 5.897 |
| w14 | 27 | 0.173739 | 19.054 |
| w15 | 13 | 0.118323 | 12.812 |
| w16 | 17 | 0.298399 | 36.273 |
| w17 | 3 | 0.056051 | 4.891 |
| w18 | 21 | 0.135532 | 12.84 |
| w19 | 1 | -0.041373 | -1.279 |
| w20 | 20 | 0.083832 | 2.175 |
| w21 | 1 | 0.047127 | 2.348 |
| w22 | 23 | 0.120212 | 11.727 |
| w23 | 3 | 0.093379 | 4.83 |
| w24 | 27 | -0.014002 | -9.438 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.066103 | -13.261 |
| w2 | 24 | 0.02517 | -2.811 |
| w3 | 2 | 0.148825 | 8.022 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.009028 | -0.086 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | 0.091142 | 4.961 |
| w9 | 2 | 0.031957 | 0.524 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 27 | 0.135659 | 9.239 |
| w15 | 3 | 0.08959 | 4.682 |
| w16 | 16 | 0.283829 | 33.844 |
| w17 | 0 | None | 0.0 |
| w18 | 22 | 0.191026 | 22.082 |
| w19 | 26 | 0.244778 | 34.033 |
| w20 | 3 | 0.254774 | 11.298 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.006381 | -0.505 |
| w24 | 5 | 0.020394 | 1.418 |

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
| w1 | 4 | 0.118687 | 6.321 |
| w2 | 0 | -0.035549 | 0.0 |
| w3 | 0 | 0.029762 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 1.56 |
| w8 | 4 | 0.106853 | 4.589 |
| w9 | 6 | 0.096248 | 6.363 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.03237 | 6.657 |
| w12 | 0 | None | 0.0 |
| w14 | 10 | -0.017062 | -1.606 |
| w15 | 5 | 0.004511 | -0.035 |
| w16 | 24 | 0.258045 | 43.309 |
| w17 | 3 | 0.008762 | -1.05 |
| w18 | 14 | 0.033876 | 1.769 |
| w19 | 12 | -0.040933 | -9.101 |
| w20 | 5 | 0.038877 | 4.835 |
| w21 | 5 | -0.020419 | 3.162 |
| w22 | 23 | 0.106227 | 12.932 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.051003 | 0.836 |

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
| w1 | 1 | 0.021729 | 0.965 |
| w2 | 32 | 0.076425 | 1.438 |
| w3 | 12 | 0.169804 | 14.212 |
| w4 | 6 | -0.027789 | -1.872 |
| w5 | 9 | 0.067478 | 5.861 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -2.798 |
| w8 | 10 | 0.156152 | 5.111 |
| w9 | 25 | 0.116108 | 7.124 |
| w10 | 3 | -0.051291 | 2.943 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.090366 | 5.637 |
| w14 | 22 | 0.181117 | 18.33 |
| w15 | 13 | -0.049649 | -6.553 |
| w16 | 21 | 0.119702 | 21.221 |
| w17 | 8 | 0.218796 | 21.764 |
| w18 | 23 | 0.114032 | 12.001 |
| w19 | 33 | 0.043915 | -3.1 |
| w20 | 12 | 0.080401 | 10.428 |
| w21 | 6 | -0.006952 | 0.821 |
| w22 | 27 | -0.007366 | -7.617 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

