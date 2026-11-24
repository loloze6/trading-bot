# Backtest of 034-01_agitated-low-close-rebounds_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/034-01_agitated-low-close-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.048936 | -0.9 |
| w2 | 45 | -0.032347 | -2.533 |
| w3 | 40 | 0.203118 | 11.664 |
| w4 | 22 | -0.093058 | -3.609 |
| w5 | 0 | None | 0.0 |
| w6 | 40 | 0.199986 | 4.355 |
| w7 | 0 | None | 0.0 |
| w8 | 25 | 0.069559 | 0.375 |
| w9 | 20 | -0.014621 | 1.461 |
| w10 | 28 | 0.052083 | 2.828 |
| w11 | 69 | -0.000637 | 0.221 |
| w12 | 26 | -0.004666 | -0.059 |
| w13 | 61 | 0.0627 | 1.799 |
| w14 | 32 | 0.251535 | 7.354 |
| w15 | 77 | 0.000636 | 0.364 |
| w16 | 43 | 0.261036 | 15.956 |
| w17 | 43 | -0.02964 | -3.135 |
| w18 | 57 | 0.042954 | -0.091 |
| w19 | 75 | 0.105972 | 4.904 |
| w20 | 59 | 0.142067 | 8.242 |
| w21 | 31 | 0.117127 | 1.606 |
| w22 | 39 | 0.245123 | 10.167 |
| w23 | 2 | -0.101163 | -0.815 |
| w24 | 44 | 0.009072 | -2.399 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.065848 | -2.24 |
| w2 | 69 | -0.065466 | -6.332 |
| w3 | 38 | 0.225346 | 10.435 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 34 | 0.134474 | 5.893 |
| w7 | 0 | None | 0.0 |
| w8 | 22 | 0.062781 | 0.109 |
| w9 | 20 | 0.11636 | 3.288 |
| w10 | 29 | 0.171735 | 5.142 |
| w11 | 67 | 0.023053 | -0.851 |
| w12 | 15 | -0.02972 | -1.291 |
| w13 | 42 | -0.007253 | -1.134 |
| w14 | 57 | 0.105983 | 2.572 |
| w15 | 39 | 0.089639 | 6.038 |
| w16 | 55 | 0.100343 | -1.695 |
| w17 | 51 | 0.095328 | 4.123 |
| w18 | 56 | -0.006475 | 0.189 |
| w19 | 66 | -0.021464 | -4.135 |
| w20 | 66 | 0.126891 | 5.821 |
| w21 | 49 | 0.027842 | -0.622 |
| w22 | 63 | 0.192061 | 9.49 |
| w23 | 35 | 0.105617 | 2.134 |
| w24 | 29 | -0.052626 | -4.543 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 54 | 0.065497 | 3.77 |
| w3 | 31 | 0.058688 | 1.432 |
| w4 | 18 | -0.056693 | -2.111 |
| w5 | 46 | 0.057702 | 1.06 |
| w6 | 2 | 0.022324 | -0.166 |
| w7 | 0 | None | 0.0 |
| w8 | 60 | 0.12645 | 3.273 |
| w9 | 0 | None | 0.0 |
| w10 | 15 | 0.082563 | 1.915 |
| w11 | 83 | 0.009041 | -1.881 |
| w12 | 27 | -0.022129 | -1.733 |
| w13 | 42 | 0.035532 | 0.762 |
| w14 | 33 | 0.057237 | -4.998 |
| w15 | 47 | 0.014086 | -3.573 |
| w16 | 43 | 0.158634 | 6.166 |
| w17 | 52 | 0.007999 | -1.595 |
| w18 | 57 | 0.059958 | 4.228 |
| w19 | 55 | 0.248364 | 15.188 |
| w20 | 52 | 0.061505 | 2.272 |
| w21 | 58 | 0.070785 | 1.163 |
| w22 | 75 | 0.008583 | -2.731 |
| w23 | 18 | 0.041636 | 0.473 |
| w24 | 33 | -0.117881 | -4.458 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.028319 | -5.119 |
| w2 | 49 | 0.069839 | 2.485 |
| w3 | 22 | 0.045658 | 0.158 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 18 | -0.030193 | -1.931 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | 0.103818 | 0.72 |
| w9 | 2 | 0.020057 | -0.465 |
| w10 | 11 | 0.195364 | 5.468 |
| w11 | 72 | 0.078099 | 3.787 |
| w12 | 21 | -0.024682 | -0.197 |
| w14 | 39 | 0.146416 | 1.496 |
| w15 | 48 | 0.152232 | 6.679 |
| w16 | 49 | 0.131272 | 6.778 |
| w17 | 41 | 0.099874 | 2.443 |
| w18 | 65 | 0.191116 | 12.667 |
| w19 | 72 | 0.144037 | 16.303 |
| w20 | 51 | 0.155781 | 4.653 |
| w21 | 37 | 0.142533 | 6.302 |
| w22 | 55 | 0.047697 | 0.116 |
| w23 | 40 | -0.126143 | -7.499 |
| w24 | 54 | -0.089127 | -5.355 |

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
| w1 | 8 | 0.07806 | -0.248 |
| w2 | 0 | 0.046918 | 0.0 |
| w3 | 0 | 0.066751 | 0.0 |
| w4 | 0 | 0.158965 | 0.0 |
| w5 | 30 | -0.037954 | -1.804 |
| w6 | 20 | -0.015773 | -2.156 |
| w8 | 7 | 0.042628 | 0.211 |
| w9 | 16 | 0.121724 | 3.349 |
| w10 | 14 | -0.017982 | -0.935 |
| w11 | 79 | -0.010432 | -5.605 |
| w12 | 2 | 0.015271 | -1.114 |
| w14 | 27 | -0.061949 | -1.872 |
| w15 | 29 | 0.096348 | 2.289 |
| w16 | 67 | 0.130461 | 7.945 |
| w17 | 52 | 0.029762 | 11.875 |
| w18 | 45 | 0.14488 | 5.576 |
| w19 | 49 | 0.047708 | 5.636 |
| w20 | 37 | -0.129164 | -7.083 |
| w21 | 56 | -0.181648 | -12.839 |
| w22 | 71 | 0.023422 | -1.239 |
| w23 | 16 | 0.035167 | 0.957 |
| w24 | 18 | -0.061206 | -0.879 |

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
| w1 | 26 | 0.211559 | 7.857 |
| w2 | 41 | 0.06454 | 2.47 |
| w3 | 20 | 0.023261 | 0.661 |
| w4 | 9 | 0.04767 | 0.985 |
| w5 | 32 | 0.086543 | 2.743 |
| w6 | 14 | 0.020691 | 0.084 |
| w7 | 10 | -0.062768 | -1.915 |
| w8 | 13 | 0.229 | 2.35 |
| w9 | 32 | 0.018924 | -0.457 |
| w10 | 30 | -0.015033 | -0.174 |
| w11 | 64 | 0.01998 | -0.071 |
| w12 | 48 | -0.014555 | -2.765 |
| w13 | 46 | 0.082513 | 5.423 |
| w14 | 35 | 0.165917 | 5.569 |
| w15 | 41 | 0.079977 | 1.895 |
| w16 | 87 | -0.011559 | -2.287 |
| w17 | 59 | 0.06631 | 1.693 |
| w18 | 54 | 0.187794 | 13.872 |
| w19 | 81 | -0.019779 | -6.966 |
| w20 | 55 | -0.152829 | -11.171 |
| w21 | 64 | -0.067051 | -5.457 |
| w22 | 76 | -0.103399 | -5.834 |
| w23 | 19 | -0.092664 | -2.396 |
| w24 | 68 | -0.193705 | -18.564 |

