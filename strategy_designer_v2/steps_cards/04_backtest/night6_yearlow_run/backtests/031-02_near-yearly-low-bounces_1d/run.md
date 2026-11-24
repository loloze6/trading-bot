# Backtest of 031-02_near-yearly-low-bounces_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-02_near-yearly-low-bounces_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.067307 | -25.907 |
| w2 | 22 | -0.032197 | -52.063 |
| w3 | 21 | 0.183213 | -14.899 |
| w4 | 5 | 0.086887 | 31.306 |
| w5 | 1 | 0.084755 | -0.097 |
| w6 | 1 | 0.046674 | 14.607 |
| w7 | 5 | 0.045912 | -18.289 |
| w8 | 11 | 0.033625 | 16.962 |
| w9 | 2 | 0.070206 | 1.046 |
| w10 | 9 | 0.10348 | 26.768 |
| w11 | 1 | 0.07816 | 11.424 |
| w12 | 7 | -0.089471 | -10.942 |
| w13 | 6 | 0.137397 | 5.799 |
| w14 | 18 | -0.029605 | -67.965 |
| w15 | 0 | 0.212299 | 0.0 |
| w16 | 6 | 0.094077 | 10.66 |
| w17 | 6 | -0.146801 | 42.546 |
| w18 | 5 | 0.267978 | 11.57 |
| w19 | 4 | 0.014299 | 18.705 |
| w20 | 4 | 0.129041 | 3.213 |
| w21 | 6 | 0.188985 | 66.944 |
| w22 | 10 | 0.008983 | -6.654 |
| w23 | 7 | 0.193979 | 13.104 |
| w24 | 8 | -0.056463 | -32.559 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | None | -31.413 |
| w2 | 18 | -0.112805 | -48.475 |
| w3 | 13 | 0.317908 | 4.299 |
| w4 | 4 | 0.189861 | 15.174 |
| w5 | 5 | 0.008117 | -6.136 |
| w6 | 9 | 0.057559 | 42.835 |
| w7 | 3 | None | -49.285 |
| w8 | 3 | 0.120326 | 3.833 |
| w9 | 4 | -0.01138 | -8.331 |
| w10 | 3 | -0.019368 | 18.721 |
| w11 | 1 | 0.08749 | 1.478 |
| w12 | 7 | -0.010437 | -3.212 |
| w13 | 8 | 0.042354 | 15.501 |
| w14 | 22 | -0.126413 | -51.85 |
| w15 | 0 | 0.139756 | 0.0 |
| w16 | 14 | 0.09893 | 54.241 |
| w17 | 1 | 0.024018 | 9.409 |
| w18 | 3 | 0.146007 | 16.312 |
| w19 | 7 | 0.088182 | 22.604 |
| w20 | 8 | 0.100748 | -7.628 |
| w21 | 20 | 0.192098 | 60.332 |
| w22 | 19 | 0.017953 | -45.314 |
| w23 | 3 | 0.151264 | 14.378 |
| w24 | 0 | 0.099877 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.053563 | -28.089 |
| w2 | 11 | -0.027659 | -49.273 |
| w3 | 3 | 0.165638 | 5.22 |
| w4 | 0 | 0.183355 | 0.0 |
| w5 | 12 | -0.003063 | -2.231 |
| w6 | 13 | 0.154594 | 29.546 |
| w7 | 3 | -0.150821 | -50.89 |
| w8 | 2 | 0.073253 | 6.876 |
| w9 | 6 | 0.022041 | -5.504 |
| w10 | 15 | 0.039657 | 30.718 |
| w11 | 1 | 0.142872 | 3.956 |
| w12 | 11 | -0.05302 | -11.938 |
| w13 | 6 | 0.08372 | 6.831 |
| w14 | 13 | -0.054997 | -49.577 |
| w15 | 0 | 0.074832 | 0.0 |
| w16 | 17 | 0.061361 | 26.776 |
| w17 | 7 | -0.045372 | 19.577 |
| w18 | 4 | 0.147812 | 6.617 |
| w19 | 22 | 0.046225 | 23.449 |
| w20 | 28 | 0.118947 | -10.625 |
| w21 | 18 | 0.023524 | 38.104 |
| w22 | 5 | 0.091885 | 1.405 |
| w23 | 1 | 0.106928 | 4.822 |
| w24 | 12 | 0.054072 | -14.795 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.007684 | -11.372 |
| w2 | 18 | 0.028972 | -10.557 |
| w3 | 6 | 0.341496 | 8.236 |
| w4 | 3 | 0.155173 | 4.263 |
| w5 | 18 | 0.084774 | -4.65 |
| w6 | 17 | 0.152526 | 40.425 |
| w7 | 4 | 0.010255 | -35.609 |
| w8 | 13 | 0.111305 | 15.484 |
| w9 | 8 | -0.017561 | -13.055 |
| w10 | 2 | 0.06394 | 5.622 |
| w11 | 2 | 0.121066 | 20.8 |
| w12 | 5 | 0.168199 | -21.15 |
| w14 | 14 | -0.017358 | -61.064 |
| w15 | 1 | 0.194608 | 0.582 |
| w16 | 15 | 0.056121 | 36.945 |
| w17 | 1 | 0.112417 | 7.651 |
| w18 | 12 | 0.189701 | 16.322 |
| w19 | 26 | 0.192049 | -23.781 |
| w20 | 6 | 0.19036 | 23.738 |
| w21 | 6 | 0.152246 | 12.63 |
| w22 | 4 | 0.118921 | 19.33 |
| w23 | 7 | 0.041172 | 5.644 |
| w24 | 8 | 0.18618 | 32.994 |

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
| w1 | 6 | 0.109561 | -25.988 |
| w2 | 23 | 0.039276 | -39.483 |
| w3 | 0 | 0.232981 | 0.0 |
| w4 | 0 | 0.144937 | 0.0 |
| w5 | 2 | 0.215929 | -1.109 |
| w6 | 5 | 0.108443 | 19.524 |
| w8 | 12 | 0.127697 | 0.437 |
| w9 | 27 | 0.065726 | -14.237 |
| w10 | 1 | 0.031348 | 6.789 |
| w11 | 4 | 0.128227 | 22.645 |
| w12 | 6 | 0.077521 | -4.51 |
| w14 | 18 | 0.050589 | 41.294 |
| w15 | 16 | 0.082565 | 13.154 |
| w16 | 8 | 0.242692 | 44.063 |
| w17 | 4 | -0.018866 | 16.66 |
| w18 | 6 | 0.185156 | 16.811 |
| w19 | 15 | 0.056905 | -2.981 |
| w20 | 13 | 0.003888 | 5.291 |
| w21 | 8 | -0.131975 | 39.011 |
| w22 | 0 | 0.165721 | 0.0 |
| w23 | 1 | 0.05301 | 0.017 |
| w24 | 7 | -0.035332 | -23.881 |

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
| w1 | 18 | 0.075007 | 11.285 |
| w2 | 26 | 0.033936 | -13.27 |
| w3 | 24 | 0.041241 | -32.144 |
| w4 | 11 | 0.103704 | 11.359 |
| w5 | 22 | 0.010166 | -20.78 |
| w6 | 19 | 0.135306 | 48.206 |
| w7 | 11 | 0.065747 | -28.448 |
| w8 | 14 | 0.04525 | 12.669 |
| w9 | 25 | 0.11847 | -32.181 |
| w10 | 0 | 0.082389 | 0.0 |
| w11 | 3 | 0.120129 | 22.955 |
| w12 | 15 | 0.116399 | 12.884 |
| w14 | 26 | 0.020664 | -42.855 |
| w15 | 5 | -0.032134 | -7.147 |
| w16 | 9 | 0.14563 | 124.216 |
| w17 | 1 | 0.149188 | 0.012 |
| w18 | 18 | 0.140981 | 14.244 |
| w19 | 15 | 0.028137 | 16.213 |
| w20 | 12 | 0.043192 | 59.186 |
| w21 | 2 | 0.06826 | 17.165 |
| w22 | 2 | 0.238205 | 1.023 |
| w23 | 18 | 0.016537 | 6.652 |
| w24 | 7 | 0.056665 | 95.807 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

