# Backtest of 039-02_agitated-range-fall-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/039-02_agitated-range-fall-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.059658 | -8.513 |
| w2 | 24 | 0.082746 | 0.253 |
| w3 | 22 | 0.205576 | 22.462 |
| w4 | 11 | 0.117683 | 13.549 |
| w5 | 0 | None | 0.0 |
| w6 | 24 | 0.217774 | 52.482 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | -0.003747 | -0.055 |
| w9 | 16 | -0.029277 | -6.708 |
| w10 | 14 | -0.005096 | 8.02 |
| w11 | 35 | 0.099142 | 34.533 |
| w12 | 13 | 0.059374 | 6.48 |
| w13 | 38 | 0.026754 | 1.052 |
| w14 | 21 | 0.215809 | 21.724 |
| w15 | 39 | -0.079307 | -3.236 |
| w16 | 20 | 0.244123 | 26.484 |
| w17 | 19 | -0.00492 | 9.335 |
| w18 | 42 | 0.158801 | 27.576 |
| w19 | 40 | 0.041405 | 15.73 |
| w20 | 38 | 0.080821 | 6.712 |
| w21 | 17 | 0.072613 | 18.656 |
| w22 | 24 | 0.210716 | 30.575 |
| w23 | 1 | -0.0534 | -1.792 |
| w24 | 35 | 0.009317 | -10.812 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.153712 | -16.502 |
| w2 | 47 | 0.047676 | -10.485 |
| w3 | 23 | 0.277484 | 32.572 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 18 | 0.126895 | 25.055 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | 0.190677 | 17.151 |
| w9 | 13 | 0.032241 | 0.642 |
| w10 | 16 | 0.058686 | 10.524 |
| w11 | 34 | 0.09419 | 43.295 |
| w12 | 8 | 0.054426 | 4.584 |
| w13 | 22 | -0.110891 | -18.094 |
| w14 | 35 | 0.183558 | 21.019 |
| w15 | 20 | 0.064431 | 9.037 |
| w16 | 29 | -0.00391 | -11.689 |
| w17 | 22 | -0.014649 | -1.861 |
| w18 | 35 | 0.054649 | 16.134 |
| w19 | 35 | -0.109567 | -14.418 |
| w20 | 44 | 0.140688 | 12.458 |
| w21 | 32 | 0.031607 | 11.039 |
| w22 | 45 | 0.115319 | 3.927 |
| w23 | 19 | 0.099986 | 32.771 |
| w24 | 23 | 0.013645 | -6.6 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 29 | 0.059891 | 1.201 |
| w3 | 19 | 0.119537 | 18.052 |
| w4 | 10 | 0.118428 | 9.879 |
| w5 | 22 | 0.030839 | -1.246 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 42 | 0.06964 | 27.837 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.029117 | 2.965 |
| w11 | 39 | -0.090578 | -5.186 |
| w12 | 21 | -0.052894 | -11.773 |
| w13 | 27 | -0.088479 | -6.098 |
| w14 | 27 | 0.176029 | 16.312 |
| w15 | 29 | 0.152743 | 21.645 |
| w16 | 24 | 0.070662 | -4.016 |
| w17 | 26 | 0.08943 | 25.116 |
| w18 | 34 | 0.135815 | 19.256 |
| w19 | 31 | 0.134332 | 31.733 |
| w20 | 21 | 0.089412 | 3.182 |
| w21 | 34 | -0.025966 | -2.278 |
| w22 | 45 | -0.020764 | -7.805 |
| w23 | 12 | 0.066995 | 7.533 |
| w24 | 28 | -0.033561 | -9.522 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.018941 | -10.62 |
| w2 | 30 | 0.005557 | -6.84 |
| w3 | 9 | 0.105307 | 7.438 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.021266 | 0.424 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | 0.098056 | 4.994 |
| w9 | 2 | 0.035153 | 0.554 |
| w10 | 5 | 0.112121 | 9.999 |
| w11 | 36 | 0.035346 | 27.909 |
| w12 | 9 | -0.009918 | -5.689 |
| w14 | 28 | 0.128694 | 7.291 |
| w15 | 31 | 0.015081 | 0.739 |
| w16 | 32 | 0.059074 | -0.83 |
| w17 | 21 | 0.010149 | 0.641 |
| w18 | 34 | 0.205426 | 38.494 |
| w19 | 49 | 0.239522 | 42.476 |
| w20 | 25 | 0.147307 | 24.693 |
| w21 | 22 | 0.109369 | 18.915 |
| w22 | 22 | 0.044593 | 8.649 |
| w23 | 25 | -0.176656 | -28.921 |
| w24 | 35 | -0.078857 | -7.191 |

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
| w1 | 6 | 0.097306 | 4.185 |
| w2 | 0 | -0.033868 | 0.0 |
| w3 | 0 | 0.119808 | 0.0 |
| w4 | 0 | 0.093516 | 0.0 |
| w5 | 25 | -0.05616 | -2.907 |
| w6 | 14 | -0.004381 | 2.997 |
| w8 | 4 | 0.107141 | 4.612 |
| w9 | 12 | 0.089165 | 6.923 |
| w10 | 7 | 0.063635 | 7.175 |
| w11 | 44 | -0.00247 | 31.14 |
| w12 | 3 | -0.01954 | -1.089 |
| w14 | 19 | 0.058521 | 3.891 |
| w15 | 18 | 0.066215 | 6.219 |
| w16 | 38 | 0.040631 | -4.326 |
| w17 | 32 | 0.058655 | 17.074 |
| w18 | 27 | 0.13755 | 12.476 |
| w19 | 34 | -0.006206 | -6.753 |
| w20 | 26 | -0.030835 | -2.99 |
| w21 | 34 | -0.037175 | 22.944 |
| w22 | 44 | 0.025667 | -1.047 |
| w23 | 11 | 0.078366 | 8.489 |
| w24 | 15 | -0.005314 | -6.332 |

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
| w1 | 15 | 0.129214 | 13.034 |
| w2 | 32 | 0.073489 | 1.538 |
| w3 | 10 | 0.189275 | 15.272 |
| w4 | 6 | -0.029767 | -1.864 |
| w5 | 16 | 0.087745 | 7.589 |
| w6 | 10 | 0.107467 | 9.04 |
| w7 | 7 | -0.044746 | -5.756 |
| w8 | 9 | 0.168196 | 5.519 |
| w9 | 22 | 0.089274 | 2.73 |
| w10 | 18 | -0.092681 | -9.21 |
| w11 | 35 | -0.018765 | 19.002 |
| w12 | 27 | -0.010827 | -3.74 |
| w13 | 30 | 0.043955 | 4.169 |
| w14 | 22 | 0.147003 | 10.764 |
| w15 | 29 | 0.037036 | -2.092 |
| w16 | 44 | 0.0133 | 16.266 |
| w17 | 27 | 0.012403 | -6.662 |
| w18 | 37 | 0.209462 | 39.401 |
| w19 | 58 | 0.040724 | -7.431 |
| w20 | 42 | -0.089603 | -9.769 |
| w21 | 40 | -0.047114 | 3.714 |
| w22 | 42 | -0.093028 | -22.989 |
| w23 | 11 | -0.070938 | -8.079 |
| w24 | 38 | -0.093564 | 6.134 |

