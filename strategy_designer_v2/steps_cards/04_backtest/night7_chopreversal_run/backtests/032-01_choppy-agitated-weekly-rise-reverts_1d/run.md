# Backtest of 032-01_choppy-agitated-weekly-rise-reverts_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/032-01_choppy-agitated-weekly-rise-reverts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.006775 | 7.776 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.220456 | 11.796 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.017245 | 0.697 |
| w10 | 3 | -0.032698 | -4.484 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.030415 | 0.0 |
| w13 | 5 | 0.00765 | -3.653 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.03771 | 0.0 |
| w16 | 5 | 0.038946 | -1.214 |
| w17 | 3 | 0.066379 | 0.016 |
| w18 | 4 | 0.243092 | 8.361 |
| w19 | 7 | -0.078479 | -19.923 |
| w20 | 23 | 0.035164 | -4.788 |
| w21 | 5 | 0.020647 | -11.508 |
| w22 | 3 | 0.042403 | 8.911 |
| w23 | 3 | 0.020393 | -2.926 |
| w24 | 5 | 0.000549 | 1.675 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | -0.02554 | -3.673 |
| w3 | 4 | -0.006734 | -1.134 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.031056 | -0.405 |
| w9 | 1 | -0.009327 | 3.788 |
| w10 | 2 | 0.060162 | -4.983 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.024651 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.009599 | 3.444 |
| w16 | 3 | 0.047191 | -0.889 |
| w17 | 3 | 0.044826 | 1.871 |
| w18 | 0 | 0.100917 | 0.0 |
| w19 | 7 | -0.025043 | -12.347 |
| w20 | 6 | -0.045062 | -9.754 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.033255 | 2.754 |
| w23 | 3 | -0.120412 | -12.878 |
| w24 | 3 | 0.036433 | 2.029 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.174658 | -26.198 |
| w4 | 8 | 0.033437 | -9.698 |
| w5 | 5 | -0.022649 | -0.855 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.081206 | -7.398 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.066603 | 3.146 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.076338 | 2.451 |
| w16 | 2 | 0.014689 | 0.897 |
| w17 | 2 | 0.002405 | -8.488 |
| w18 | 1 | 0.036018 | 0.448 |
| w19 | 7 | 0.072096 | 5.875 |
| w20 | 2 | 0.050257 | 1.142 |
| w21 | 7 | 0.040224 | 4.821 |
| w22 | 5 | -0.017866 | 3.641 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.021052 | 3.865 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.114947 | 3.967 |
| w2 | 7 | -0.008719 | -7.511 |
| w3 | 9 | -0.033533 | -8.388 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.049217 | -5.764 |
| w12 | 7 | -0.084957 | -6.571 |
| w14 | 3 | -0.049165 | 4.94 |
| w15 | 6 | -0.039995 | 2.673 |
| w16 | 2 | -0.120614 | -2.405 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | -0.040779 | -2.081 |
| w19 | 21 | 0.059601 | 7.73 |
| w20 | 11 | 0.056511 | -6.103 |
| w21 | 11 | 0.038143 | -11.452 |
| w22 | 6 | -0.010917 | -5.787 |
| w23 | 2 | 0.233219 | 13.073 |
| w24 | 1 | 0.052992 | 5.307 |

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
| w1 | 2 | 0.037921 | 3.214 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.330347 | 0.0 |
| w4 | 0 | -0.201979 | 0.0 |
| w5 | 4 | -0.000528 | 1.857 |
| w6 | 0 | 0.048668 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.029826 | 1.209 |
| w10 | 0 | None | 0.0 |
| w11 | 9 | -0.042143 | -17.121 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | -0.301119 | -14.446 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.01382 | -1.274 |
| w17 | 2 | -0.001681 | -1.098 |
| w18 | 1 | 0.103496 | 0.563 |
| w19 | 11 | 0.004487 | -1.461 |
| w20 | 6 | -0.285723 | -36.383 |
| w21 | 4 | 0.071176 | 1.945 |
| w22 | 11 | 0.030175 | 4.165 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.117374 | 11.277 |

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
| w1 | 6 | 0.04694 | -9.677 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.067511 | 21.815 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.264663 | 13.271 |
| w10 | 2 | 0.084245 | -5.646 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | -0.04049 | 0.83 |
| w13 | 2 | 0.008164 | 4.575 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.010774 | 5.247 |
| w16 | 5 | -0.157868 | -49.886 |
| w17 | 7 | 0.061456 | 3.356 |
| w18 | 4 | -0.039127 | 2.326 |
| w19 | 9 | -0.071746 | -17.331 |
| w20 | 6 | -0.15375 | -22.028 |
| w21 | 6 | 0.052882 | -5.426 |
| w22 | 6 | -0.010837 | 2.164 |
| w23 | 2 | 0.009735 | -3.997 |
| w24 | 2 | 0.005767 | -10.222 |

