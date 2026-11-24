# Backtest of 031-01_near-yearly-low-keeps-falling_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-01_near-yearly-low-keeps-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.067307 | 14.552 |
| w2 | 26 | 0.032197 | 66.302 |
| w3 | 32 | -0.183213 | 4.143 |
| w4 | 6 | -0.086887 | -25.975 |
| w5 | 1 | -0.084755 | 0.076 |
| w6 | 2 | -0.046674 | -14.53 |
| w7 | 18 | -0.045912 | 1.609 |
| w8 | 11 | -0.033625 | -16.099 |
| w9 | 2 | -0.070206 | -1.126 |
| w10 | 12 | -0.10348 | -27.096 |
| w11 | 3 | -0.07816 | -13.258 |
| w12 | 10 | 0.089471 | 11.892 |
| w13 | 6 | -0.137397 | -8.161 |
| w14 | 17 | 0.029605 | 133.476 |
| w15 | 0 | -0.212299 | 0.0 |
| w16 | 9 | -0.094077 | -20.493 |
| w17 | 7 | 0.146801 | -31.974 |
| w18 | 6 | -0.267978 | -11.949 |
| w19 | 8 | -0.014299 | -21.251 |
| w20 | 6 | -0.129041 | -6.377 |
| w21 | 11 | -0.188985 | -44.657 |
| w22 | 17 | -0.008983 | -5.478 |
| w23 | 10 | -0.193979 | -14.469 |
| w24 | 23 | 0.056463 | 31.044 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | None | 18.45 |
| w2 | 23 | 0.112805 | 42.623 |
| w3 | 13 | -0.317908 | -8.034 |
| w4 | 4 | -0.189861 | -13.438 |
| w5 | 7 | -0.008117 | 4.302 |
| w6 | 15 | -0.057559 | -32.563 |
| w7 | 13 | None | 69.863 |
| w8 | 3 | -0.120326 | -3.857 |
| w9 | 7 | 0.01138 | 5.833 |
| w10 | 3 | 0.019368 | -15.612 |
| w11 | 1 | -0.08749 | -1.489 |
| w12 | 9 | 0.010437 | -0.499 |
| w13 | 12 | -0.042354 | -23.639 |
| w14 | 29 | 0.126413 | 66.235 |
| w15 | 0 | -0.139756 | 0.0 |
| w16 | 18 | -0.09893 | -47.944 |
| w17 | 1 | -0.024018 | -9.425 |
| w18 | 4 | -0.146007 | -15.68 |
| w19 | 8 | -0.088182 | -19.552 |
| w20 | 9 | -0.100748 | 1.442 |
| w21 | 26 | -0.192098 | -46.382 |
| w22 | 26 | -0.017953 | 55.363 |
| w23 | 3 | -0.151264 | -12.925 |
| w24 | 0 | -0.099877 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.053563 | 18.946 |
| w2 | 15 | 0.027659 | 48.562 |
| w3 | 4 | -0.165638 | -7.502 |
| w4 | 0 | -0.183355 | 0.0 |
| w5 | 13 | 0.003063 | 1.492 |
| w6 | 34 | -0.154594 | -35.98 |
| w7 | 8 | 0.150821 | 84.25 |
| w8 | 2 | -0.073253 | -6.788 |
| w9 | 8 | -0.022041 | 4.015 |
| w10 | 15 | -0.039657 | -25.48 |
| w11 | 1 | -0.142872 | -3.975 |
| w12 | 13 | 0.05302 | -0.18 |
| w13 | 6 | -0.08372 | -7.184 |
| w14 | 21 | 0.054997 | 42.702 |
| w15 | 0 | -0.074832 | 0.0 |
| w16 | 22 | -0.061361 | -39.587 |
| w17 | 7 | 0.045372 | -18.488 |
| w18 | 4 | -0.147812 | -7.13 |
| w19 | 25 | -0.046225 | -24.853 |
| w20 | 31 | -0.118947 | 1.788 |
| w21 | 24 | -0.023524 | -36.185 |
| w22 | 5 | -0.091885 | -1.859 |
| w23 | 1 | -0.106928 | -4.874 |
| w24 | 14 | -0.054072 | 9.911 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.007684 | -4.664 |
| w2 | 25 | -0.028972 | -5.904 |
| w3 | 6 | -0.341496 | -8.859 |
| w4 | 3 | -0.155173 | -4.64 |
| w5 | 21 | -0.084774 | -3.262 |
| w6 | 30 | -0.152526 | -36.163 |
| w7 | 10 | -0.010255 | 36.454 |
| w8 | 13 | -0.111305 | -15.07 |
| w9 | 9 | 0.017561 | 12.486 |
| w10 | 2 | -0.06394 | -5.594 |
| w11 | 3 | -0.121066 | -21.724 |
| w12 | 13 | -0.168199 | 6.751 |
| w14 | 22 | 0.017358 | 81.239 |
| w15 | 1 | -0.194608 | -0.615 |
| w16 | 20 | -0.056121 | -43.599 |
| w17 | 1 | -0.112417 | -7.694 |
| w18 | 12 | -0.189701 | -18.938 |
| w19 | 27 | -0.192049 | 4.502 |
| w20 | 6 | -0.19036 | -20.255 |
| w21 | 9 | -0.152246 | -13.58 |
| w22 | 3 | -0.118921 | -13.763 |
| w23 | 9 | -0.041172 | -8.109 |
| w24 | 9 | -0.18618 | -29.966 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.109561 | 15.09 |
| w2 | 28 | -0.039276 | 31.979 |
| w3 | 0 | -0.232981 | 0.0 |
| w4 | 0 | -0.144937 | 0.0 |
| w5 | 2 | -0.215929 | 1.089 |
| w6 | 7 | -0.108443 | -19.788 |
| w8 | 14 | -0.127697 | -8.16 |
| w9 | 34 | -0.065726 | 4.372 |
| w10 | 2 | -0.031348 | -8.614 |
| w11 | 5 | -0.128227 | -22.073 |
| w12 | 6 | -0.077521 | 2.652 |
| w14 | 22 | -0.050589 | -43.465 |
| w15 | 25 | -0.082565 | -31.54 |
| w16 | 13 | -0.242692 | -38.029 |
| w17 | 4 | 0.018866 | -9.689 |
| w18 | 6 | -0.185156 | -15.848 |
| w19 | 19 | -0.056905 | -3.229 |
| w20 | 19 | -0.003888 | -17.712 |
| w21 | 12 | 0.131975 | -36.272 |
| w22 | 0 | -0.165721 | 0.0 |
| w23 | 1 | -0.05301 | -0.035 |
| w24 | 11 | 0.035332 | 24.962 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.075007 | -21.399 |
| w2 | 31 | -0.033936 | 10.76 |
| w3 | 28 | -0.041241 | 24.329 |
| w4 | 13 | -0.103704 | -13.236 |
| w5 | 24 | -0.010166 | 5.922 |
| w6 | 26 | -0.135306 | -40.994 |
| w7 | 17 | -0.065747 | 5.123 |
| w8 | 15 | -0.04525 | -12.769 |
| w9 | 25 | -0.11847 | 29.026 |
| w10 | 0 | -0.082389 | 0.0 |
| w11 | 3 | -0.120129 | -20.492 |
| w12 | 15 | -0.116399 | -16.794 |
| w14 | 31 | -0.020664 | 37.494 |
| w15 | 7 | 0.032134 | -3.312 |
| w16 | 17 | -0.14563 | -64.546 |
| w17 | 1 | -0.149188 | -0.03 |
| w18 | 20 | -0.140981 | -19.144 |
| w19 | 23 | -0.028137 | -22.229 |
| w20 | 17 | -0.043192 | -48.919 |
| w21 | 2 | -0.06826 | -10.985 |
| w22 | 2 | -0.238205 | -1.162 |
| w23 | 16 | -0.016537 | -9.692 |
| w24 | 7 | -0.056665 | -52.68 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

