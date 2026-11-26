# Backtest of 061-01.g1.g2_agitated-big-day-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.g2_agitated-big-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.041171 | -9.829 |
| w2 | 32 | -0.077065 | 11.119 |
| w3 | 24 | -0.194089 | -18.363 |
| w4 | 10 | 0.056993 | 38.472 |
| w5 | 0 | None | 0.0 |
| w6 | 37 | -0.175757 | -21.295 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | -0.09897 | -13.661 |
| w9 | 20 | 0.119538 | -17.69 |
| w10 | 18 | -0.069497 | -0.509 |
| w11 | 54 | 0.004455 | 5.755 |
| w12 | 29 | 0.064746 | -13.377 |
| w13 | 32 | -0.051301 | -14.526 |
| w14 | 19 | -0.244106 | 9.007 |
| w15 | 41 | -0.007915 | 2.98 |
| w16 | 27 | -0.196883 | 17.479 |
| w17 | 33 | -0.004615 | 37.212 |
| w18 | 38 | -0.201341 | 23.95 |
| w19 | 39 | -0.158986 | 25.774 |
| w20 | 41 | -0.096179 | -24.6 |
| w21 | 28 | -0.058164 | -6.154 |
| w22 | 33 | -0.222448 | -30.713 |
| w23 | 3 | 0.046013 | 1.764 |
| w24 | 37 | 0.010909 | -9.849 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.078136 | -22.03 |
| w2 | 58 | -0.024178 | 17.851 |
| w3 | 26 | -0.283587 | -2.193 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 26 | -0.187237 | -18.057 |
| w7 | 0 | None | 0.0 |
| w8 | 23 | -0.170992 | 2.67 |
| w9 | 13 | -0.097064 | 0.774 |
| w10 | 22 | -0.113696 | -13.655 |
| w11 | 40 | 0.02768 | -16.106 |
| w12 | 19 | 0.014839 | -14.896 |
| w13 | 35 | 0.039434 | 42.183 |
| w14 | 44 | -0.126999 | 10.507 |
| w15 | 20 | -0.056698 | -11.72 |
| w16 | 33 | -0.127889 | -35.739 |
| w17 | 28 | -0.024351 | -31.512 |
| w18 | 37 | -0.183151 | -24.718 |
| w19 | 43 | -0.021728 | -34.206 |
| w20 | 59 | -0.11833 | -34.596 |
| w21 | 38 | 0.019539 | 19.478 |
| w22 | 53 | -0.173818 | 6.473 |
| w23 | 22 | -0.10521 | -0.757 |
| w24 | 33 | 0.017028 | -33.413 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 36 | -0.175654 | -1.199 |
| w3 | 21 | -0.074461 | -12.97 |
| w4 | 10 | -0.030938 | 9.335 |
| w5 | 30 | 0.012862 | -11.768 |
| w6 | 5 | 0.041344 | -14.504 |
| w7 | 0 | None | 0.0 |
| w8 | 43 | -0.075102 | 11.499 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | -0.011102 | -19.623 |
| w11 | 42 | 0.065405 | 25.002 |
| w12 | 28 | 0.044396 | 2.051 |
| w13 | 25 | -0.064738 | -24.242 |
| w14 | 22 | -0.092637 | -11.569 |
| w15 | 30 | -0.053168 | -15.974 |
| w16 | 26 | -0.103651 | 14.62 |
| w17 | 33 | 0.037443 | -8.959 |
| w18 | 31 | -0.211028 | -14.745 |
| w19 | 43 | -0.203351 | -32.136 |
| w20 | 37 | -0.128336 | -23.788 |
| w21 | 34 | -0.037902 | 24.967 |
| w22 | 58 | 0.06106 | -24.575 |
| w23 | 13 | -0.087338 | 2.229 |
| w24 | 28 | 0.046814 | -21.843 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.013151 | -5.573 |
| w2 | 34 | -0.086376 | -9.049 |
| w3 | 19 | -0.069788 | -5.62 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 19 | 0.057884 | -21.95 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | -0.143853 | -6.332 |
| w9 | 3 | -0.045801 | 4.428 |
| w10 | 7 | -0.177472 | -5.029 |
| w11 | 50 | -0.057185 | -41.563 |
| w12 | 14 | 0.047752 | -1.228 |
| w14 | 24 | -0.118386 | 1.841 |
| w15 | 19 | -0.128443 | -26.421 |
| w16 | 39 | -0.08755 | 22.45 |
| w17 | 25 | -0.087718 | -8.896 |
| w18 | 28 | -0.253272 | -23.252 |
| w19 | 57 | -0.180428 | -31.027 |
| w20 | 34 | -0.137128 | 0.804 |
| w21 | 30 | -0.271236 | 2.204 |
| w22 | 45 | -0.025701 | 9.35 |
| w23 | 31 | 0.140145 | -24.536 |
| w24 | 50 | 0.03059 | -11.952 |

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
| w1 | 5 | -0.127314 | -8.397 |
| w2 | 11 | -0.046281 | -14.235 |
| w3 | 0 | -0.093801 | 0.0 |
| w4 | 0 | -0.162997 | 0.0 |
| w5 | 28 | -0.049631 | -14.828 |
| w6 | 35 | -0.087511 | 4.999 |
| w8 | 7 | -0.073091 | 1.509 |
| w9 | 15 | -0.111873 | -10.271 |
| w10 | 5 | -0.078868 | 9.875 |
| w11 | 45 | 0.069956 | 20.239 |
| w12 | 2 | 0.045691 | 0.109 |
| w14 | 19 | 0.045058 | 8.796 |
| w15 | 19 | -0.036462 | -4.67 |
| w16 | 43 | -0.121869 | 65.51 |
| w17 | 38 | -0.041185 | 24.397 |
| w18 | 37 | -0.202198 | -5.058 |
| w19 | 35 | -0.05536 | -8.538 |
| w20 | 28 | 0.150795 | -11.828 |
| w21 | 32 | 0.248398 | 129.414 |
| w22 | 52 | -0.024079 | 12.691 |
| w23 | 10 | -0.048937 | -10.717 |
| w24 | 19 | 0.006474 | -3.035 |

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
| w1 | 21 | -0.064844 | -35.487 |
| w2 | 34 | -0.149393 | 0.382 |
| w3 | 18 | -0.047909 | -20.117 |
| w4 | 6 | -0.069517 | -0.768 |
| w5 | 24 | -0.037588 | -13.634 |
| w6 | 10 | -0.050988 | 12.882 |
| w7 | 10 | -0.013559 | 12.12 |
| w8 | 7 | -0.200781 | -3.282 |
| w9 | 25 | -0.138397 | -25.743 |
| w10 | 19 | -0.055542 | -16.295 |
| w11 | 41 | 0.001797 | 58.865 |
| w12 | 37 | 0.107141 | -8.918 |
| w13 | 29 | -0.072086 | 0.035 |
| w14 | 14 | -0.129716 | 1.466 |
| w15 | 33 | -0.064024 | 7.027 |
| w16 | 56 | 0.044222 | 122.358 |
| w17 | 34 | -0.026803 | -24.829 |
| w18 | 29 | -0.292346 | 27.883 |
| w19 | 53 | 0.007368 | 8.215 |
| w20 | 38 | 0.114081 | -28.478 |
| w21 | 47 | 0.008947 | 7.496 |
| w22 | 37 | 0.049514 | 7.956 |
| w23 | 21 | 0.099693 | 5.984 |
| w24 | 52 | 0.106213 | 152.859 |

