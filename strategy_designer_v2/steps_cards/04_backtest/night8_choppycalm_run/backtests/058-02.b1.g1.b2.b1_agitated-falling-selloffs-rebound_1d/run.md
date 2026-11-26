# Backtest of 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d

- Plan: `../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.040042 | -3.726 |
| w2 | 25 | 0.053616 | -3.743 |
| w3 | 19 | 0.276445 | 18.595 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 5.213 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.048811 | 2.118 |
| w9 | 10 | -0.065604 | -7.947 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 4.104 |
| w13 | 23 | 0.045081 | 2.292 |
| w14 | 20 | 0.209818 | 19.815 |
| w15 | 5 | -0.078733 | -3.306 |
| w16 | 17 | 0.258858 | 21.047 |
| w17 | 0 | None | 0.0 |
| w18 | 37 | 0.158685 | 18.826 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.066616 | 1.739 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.187718 | 18.534 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | 0.075506 | 2.256 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.147198 | -12.99 |
| w2 | 38 | -0.020668 | -14.617 |
| w3 | 10 | 0.318134 | 22.54 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.145856 | 8.007 |
| w9 | 11 | 0.031513 | 0.685 |
| w10 | 2 | 0.127574 | 1.498 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 38 | 0.20643 | 24.639 |
| w15 | 6 | 0.03125 | 1.505 |
| w16 | 17 | 0.284809 | 20.647 |
| w17 | 1 | -0.006609 | 0.026 |
| w18 | 12 | 0.030928 | 3.967 |
| w19 | 1 | None | -0.057 |
| w20 | 25 | 0.07457 | -2.24 |
| w21 | 10 | 0.025534 | 3.142 |
| w22 | 39 | 0.056861 | -4.659 |
| w23 | 2 | 0.070086 | 0.016 |
| w24 | 11 | 0.135554 | 7.453 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 31 | 0.032955 | -2.421 |
| w3 | 1 | 0.393083 | 19.101 |
| w4 | 2 | 0.074257 | 3.057 |
| w5 | 8 | 0.00473 | -1.589 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | -0.027316 | 0.061 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.060961 | 3.191 |
| w13 | 7 | 0.096346 | 3.008 |
| w14 | 28 | 0.187858 | 14.851 |
| w15 | 11 | 0.126897 | 11.032 |
| w16 | 14 | 0.314123 | 25.212 |
| w17 | 3 | 0.051076 | 3.556 |
| w18 | 21 | 0.120101 | 7.891 |
| w19 | 1 | -0.042376 | -0.507 |
| w20 | 21 | 0.097935 | 3.342 |
| w21 | 1 | 0.047127 | 1.777 |
| w22 | 23 | 0.104441 | 7.933 |
| w23 | 3 | 0.092892 | 4.305 |
| w24 | 28 | -0.026343 | -6.935 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.095916 | -12.91 |
| w2 | 23 | 0.003948 | -5.024 |
| w3 | 2 | 0.137813 | 3.177 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.005505 | 0.37 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.078301 | 3.625 |
| w9 | 2 | 0.035349 | 0.556 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 28 | 0.139943 | 7.406 |
| w15 | 3 | 0.09407 | 4.248 |
| w16 | 18 | 0.26752 | 18.74 |
| w17 | 0 | None | 0.0 |
| w18 | 20 | 0.219866 | 24.043 |
| w19 | 20 | 0.28331 | 29.925 |
| w20 | 2 | 0.276842 | 6.192 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.018278 | -1.692 |
| w24 | 1 | 0.006569 | 0.017 |

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
| w1 | 4 | 0.143881 | 4.175 |
| w2 | 0 | -0.059944 | 0.0 |
| w3 | 0 | 0.035982 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 1.56 |
| w8 | 4 | 0.089253 | 2.69 |
| w9 | 6 | 0.080758 | 2.389 |
| w10 | 0 | None | 0.0 |
| w11 | 7 | 0.015707 | 4.161 |
| w12 | 0 | None | 0.0 |
| w14 | 8 | 0.033322 | 2.156 |
| w15 | 6 | 0.026651 | 1.176 |
| w16 | 21 | 0.249051 | 22.996 |
| w17 | 2 | -0.009703 | -0.983 |
| w18 | 14 | 0.030764 | 1.206 |
| w19 | 12 | -0.03754 | -7.036 |
| w20 | 5 | 0.041779 | 5.036 |
| w21 | 5 | -0.019682 | 2.688 |
| w22 | 21 | 0.102882 | 9.091 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.073468 | 2.984 |

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
| w1 | 1 | 0.021729 | 0.691 |
| w2 | 33 | 0.077373 | 1.642 |
| w3 | 9 | 0.252708 | 14.982 |
| w4 | 6 | -0.03587 | -1.175 |
| w5 | 9 | 0.095432 | 6.219 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -2.168 |
| w8 | 8 | 0.160613 | 4.35 |
| w9 | 24 | 0.063488 | 0.122 |
| w10 | 3 | -0.048188 | -0.658 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.085692 | 3.275 |
| w14 | 22 | 0.162365 | 11.52 |
| w15 | 10 | -0.052078 | -5.681 |
| w16 | 23 | 0.11617 | 14.652 |
| w17 | 8 | 0.212733 | 18.264 |
| w18 | 21 | 0.124298 | 11.13 |
| w19 | 30 | 0.099075 | 6.936 |
| w20 | 11 | 0.101981 | 11.673 |
| w21 | 5 | 0.00076 | 0.611 |
| w22 | 26 | -0.022883 | -8.067 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

