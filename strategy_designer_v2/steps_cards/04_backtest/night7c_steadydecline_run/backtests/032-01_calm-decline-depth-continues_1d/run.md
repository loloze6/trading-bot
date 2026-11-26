# Backtest of 032-01_calm-decline-depth-continues_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-01_calm-decline-depth-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.135572 | -6.294 |
| w2 | 10 | -0.115215 | -6.661 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.039548 | -3.836 |
| w5 | 13 | -0.06946 | -9.418 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | -0.061859 | -1.299 |
| w10 | 2 | -0.035933 | -3.387 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.036866 | -7.812 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.031931 | -5.509 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | -0.255631 | -14.888 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.134546 | 22.268 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 11 | -0.014748 | 4.998 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | -0.075174 | 2.143 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.061155 | -0.686 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | -0.041807 | -8.73 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 16 | 0.034347 | 16.434 |
| w23 | 4 | -0.129407 | -9.816 |
| w24 | 21 | 0.057208 | 7.79 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.016123 | -0.881 |
| w4 | 4 | -0.065304 | -5.269 |
| w5 | 10 | -0.21759 | -16.116 |
| w6 | 2 | -0.148256 | -3.073 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | -0.102163 | -1.962 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.013651 | -0.457 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.078647 | 6.806 |
| w16 | 7 | 0.069077 | 5.291 |
| w17 | 5 | -0.013092 | -9.124 |
| w18 | 2 | 0.086261 | -1.401 |
| w19 | 8 | 0.012507 | 1.483 |
| w20 | 2 | -0.005542 | -0.307 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | -0.020108 | -1.106 |
| w23 | 4 | -0.076962 | -9.011 |
| w24 | 5 | 0.014506 | 11.599 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.037844 | 3.726 |
| w2 | 19 | -0.021597 | 5.345 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | 0.070447 | -0.485 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.00267 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | -0.016032 | 3.713 |
| w13 | 3 | -0.036529 | -2.279 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.12171 | -3.1 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | 0.04856 | 0.03 |
| w19 | 3 | -0.042697 | 7.988 |
| w20 | 21 | -0.098362 | -8.798 |
| w21 | 13 | -0.033894 | -13.124 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.049957 | 7.323 |
| w24 | 2 | -0.01682 | -6.972 |

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.199742 | 0.0 |
| w4 | 0 | -4e-06 | 0.0 |
| w5 | 12 | 0.010581 | -16.426 |
| w6 | 4 | -0.055749 | -1.229 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.019186 | 2.114 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.007407 | 1.027 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.007348 | -0.667 |
| w18 | 0 | None | 0.0 |
| w19 | 17 | 0.062364 | 20.902 |
| w20 | 9 | 0.03611 | -0.517 |
| w21 | 14 | 0.044353 | -2.917 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.034843 | 0.482 |
| w24 | 4 | -0.059261 | -1.722 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=360. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=360. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.070832 | 4.094 |
| w2 | 5 | 0.001907 | 9.173 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.176589 | -2.275 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.180428 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.073386 | 9.626 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.081895 | -7.928 |
| w18 | 5 | -0.077902 | -3.958 |
| w19 | 1 | 0.073193 | 4.008 |
| w20 | 9 | -0.141921 | -17.7 |
| w21 | 0 | None | 0.0 |
| w22 | 18 | -0.156103 | -7.624 |
| w23 | 6 | 0.062127 | -3.881 |
| w24 | 0 | None | 0.0 |

