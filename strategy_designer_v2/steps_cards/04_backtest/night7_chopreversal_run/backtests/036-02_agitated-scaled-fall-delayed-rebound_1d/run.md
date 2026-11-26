# Backtest of 036-02_agitated-scaled-fall-delayed-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/036-02_agitated-scaled-fall-delayed-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.010538 | -2.121 |
| w2 | 33 | -0.141604 | -11.363 |
| w3 | 24 | 0.172718 | 9.653 |
| w4 | 11 | 0.060715 | 1.969 |
| w5 | 0 | None | 0.0 |
| w6 | 32 | -0.085863 | 15.533 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | -0.038495 | 0.153 |
| w9 | 15 | -0.031256 | 1.389 |
| w10 | 21 | -0.009551 | 6.934 |
| w11 | 47 | 0.022533 | 22.287 |
| w12 | 20 | 0.165827 | 11.44 |
| w13 | 46 | -0.036241 | -10.409 |
| w14 | 22 | -0.145813 | -23.15 |
| w15 | 55 | 0.05535 | 21.482 |
| w16 | 22 | -0.142812 | -1.307 |
| w17 | 25 | 0.052311 | 18.913 |
| w18 | 47 | -0.122946 | -20.62 |
| w19 | 47 | -0.066701 | -13.972 |
| w20 | 40 | -0.023102 | -13.949 |
| w21 | 17 | 0.079653 | 6.501 |
| w22 | 27 | -0.019277 | 10.954 |
| w23 | 3 | 0.104591 | 1.675 |
| w24 | 38 | 0.120014 | 3.707 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.055702 | -10.38 |
| w2 | 53 | -0.010592 | 4.105 |
| w3 | 29 | 0.120463 | -0.002 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 26 | -0.117278 | 3.155 |
| w7 | 0 | None | 0.0 |
| w8 | 22 | -0.029655 | -9.31 |
| w9 | 15 | -0.049492 | 9.558 |
| w10 | 24 | -0.140145 | 2.754 |
| w11 | 40 | -0.0275 | 41.764 |
| w12 | 11 | 0.209645 | 14.927 |
| w13 | 28 | -0.034326 | -10.272 |
| w14 | 47 | 0.009609 | -10.72 |
| w15 | 23 | -0.04854 | -1.563 |
| w16 | 37 | -0.065231 | 11.679 |
| w17 | 31 | -0.098849 | -13.538 |
| w18 | 36 | -0.079581 | -10.127 |
| w19 | 42 | 0.006101 | -3.738 |
| w20 | 48 | -0.118609 | -25.988 |
| w21 | 36 | 0.075993 | 7.894 |
| w22 | 54 | 0.000241 | -22.121 |
| w23 | 25 | -0.039558 | 7.664 |
| w24 | 22 | 0.211574 | 13.414 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 30 | -0.096868 | -13.478 |
| w3 | 18 | 0.243943 | 14.676 |
| w4 | 11 | 0.186845 | 15.639 |
| w5 | 25 | 0.191353 | 19.719 |
| w6 | 3 | 0.146408 | 8.241 |
| w7 | 0 | None | 0.0 |
| w8 | 52 | -0.063916 | 8.116 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | -0.026663 | 7.07 |
| w11 | 57 | 0.028599 | 31.492 |
| w12 | 27 | 0.106407 | 6.058 |
| w13 | 23 | -0.005731 | -10.87 |
| w14 | 31 | -0.122637 | -12.956 |
| w15 | 32 | 0.125988 | 11.271 |
| w16 | 31 | -0.142189 | -8.295 |
| w17 | 38 | 0.073182 | 12.651 |
| w18 | 37 | -0.120882 | -12.265 |
| w19 | 42 | -0.019065 | -5.126 |
| w20 | 34 | -0.114436 | -22.356 |
| w21 | 38 | 0.115194 | 28.591 |
| w22 | 50 | 0.079872 | 18.304 |
| w23 | 13 | 0.032305 | 10.197 |
| w24 | 32 | 0.186908 | 12.504 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.13831 | -17.406 |
| w2 | 33 | -0.302827 | -31.91 |
| w3 | 11 | 0.035607 | 4.731 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 14 | 0.082559 | 8.318 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | 0.02068 | -3.084 |
| w9 | 3 | -0.029485 | -4.314 |
| w10 | 6 | -0.145787 | 0.049 |
| w11 | 42 | 0.022336 | 15.924 |
| w12 | 15 | 0.181785 | 8.031 |
| w14 | 31 | -0.079814 | -13.954 |
| w15 | 28 | 0.043839 | 2.596 |
| w16 | 38 | -0.095781 | -3.062 |
| w17 | 35 | 0.025483 | 6.134 |
| w18 | 35 | -0.189075 | -20.282 |
| w19 | 58 | 0.028617 | -31.169 |
| w20 | 34 | 0.057155 | 14.052 |
| w21 | 19 | 0.06496 | 10.208 |
| w22 | 32 | 0.013249 | 0.477 |
| w23 | 33 | 0.061525 | 16.037 |
| w24 | 34 | 0.244235 | 46.227 |

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
| w1 | 8 | 0.027269 | 1.157 |
| w2 | 4 | -0.107662 | -18.185 |
| w3 | 0 | 0.21201 | 0.0 |
| w4 | 0 | -0.266171 | 0.0 |
| w5 | 20 | -0.018203 | -2.135 |
| w6 | 20 | -0.016471 | 3.904 |
| w8 | 5 | 0.005894 | -4.706 |
| w9 | 14 | 0.022079 | 0.661 |
| w10 | 7 | -0.134892 | -3.378 |
| w11 | 53 | 0.099017 | 120.248 |
| w12 | 4 | -0.001402 | -4.568 |
| w14 | 18 | -0.049546 | -6.876 |
| w15 | 21 | 0.002616 | 5.133 |
| w16 | 46 | -0.049381 | 10.806 |
| w17 | 41 | 0.002889 | -6.371 |
| w18 | 30 | 0.024292 | -2.284 |
| w19 | 35 | 0.092882 | 1.95 |
| w20 | 24 | 0.105645 | 20.187 |
| w21 | 31 | -0.048811 | 22.392 |
| w22 | 46 | -0.000109 | 8.735 |
| w23 | 10 | 0.162234 | 8.325 |
| w24 | 15 | 0.083713 | 7.674 |

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
| w1 | 11 | 0.02802 | 0.737 |
| w2 | 42 | -0.253954 | -26.887 |
| w3 | 11 | 0.247844 | 17.997 |
| w4 | 7 | -0.004454 | -1.765 |
| w5 | 17 | 0.15687 | 17.019 |
| w6 | 13 | -0.1018 | -15.32 |
| w7 | 8 | -0.086252 | -8.754 |
| w8 | 9 | -0.034714 | -5.17 |
| w9 | 27 | 0.053039 | -0.255 |
| w10 | 26 | -0.073124 | -5.335 |
| w11 | 42 | -0.105259 | 13.933 |
| w12 | 39 | 0.194599 | 20.831 |
| w13 | 28 | 0.023668 | -8.042 |
| w14 | 20 | -0.151216 | -16.931 |
| w15 | 31 | -0.031615 | -16.424 |
| w16 | 49 | -0.020531 | 14.303 |
| w17 | 29 | -0.024324 | -11.551 |
| w18 | 42 | -0.170269 | -14.313 |
| w19 | 61 | 0.064744 | -4.507 |
| w20 | 41 | 0.065884 | 6.134 |
| w21 | 43 | 0.101283 | 15.902 |
| w22 | 56 | 0.086297 | -5.527 |
| w23 | 16 | 0.022916 | 1.823 |
| w24 | 50 | 0.125522 | 51.429 |

