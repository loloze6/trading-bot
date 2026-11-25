# Backtest of 040-01_falling-calm-scaled-fall-continuation_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/040-01_falling-calm-scaled-fall-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.039742 | 3.453 |
| w2 | 8 | 0.149915 | 36.436 |
| w3 | 22 | 0.145402 | -4.991 |
| w4 | 0 | 0.006236 | 0.0 |
| w5 | 8 | -0.035026 | -14.983 |
| w6 | 13 | 0.034286 | -3.472 |
| w7 | 24 | -0.06922 | 1.844 |
| w8 | 7 | 0.033185 | 0.172 |
| w9 | 41 | -0.297865 | -45.398 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.034784 | 4.877 |
| w12 | 10 | -0.049411 | -5.452 |
| w13 | 9 | 0.063003 | 4.876 |
| w14 | 12 | 0.022333 | 11.987 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.031463 | -6.498 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.04871 | 3.072 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -4.229 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.223899 | 10.314 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.209376 | 29.186 |
| w2 | 2 | -0.088467 | 12.316 |
| w3 | 19 | 0.14496 | -3.058 |
| w4 | 0 | -0.02418 | 0.0 |
| w5 | 8 | -0.127622 | -8.856 |
| w6 | 14 | 0.055722 | 0.864 |
| w7 | 34 | 0.041411 | 29.443 |
| w8 | 0 | None | 0.0 |
| w9 | 37 | -0.102518 | -14.392 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.037393 | 2.916 |
| w13 | 17 | 0.127292 | 20.318 |
| w14 | 9 | 0.136757 | 27.395 |
| w15 | 16 | -0.001225 | 3.343 |
| w16 | 6 | -0.075205 | -14.131 |
| w17 | 9 | -0.029683 | -4.161 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.075383 | 4.162 |
| w22 | 9 | -0.042054 | 2.618 |
| w23 | 0 | None | 0.0 |
| w24 | 24 | 0.07099 | 3.735 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.128538 | 27.647 |
| w2 | 7 | 0.026454 | 6.723 |
| w3 | 15 | -0.030558 | -3.238 |
| w4 | 4 | -0.127949 | -18.913 |
| w5 | 2 | 0.009015 | 0.017 |
| w6 | 21 | 0.021746 | -3.52 |
| w7 | 61 | -0.007709 | 16.189 |
| w8 | 0 | None | 0.0 |
| w9 | 57 | 0.015899 | 10.749 |
| w10 | 10 | -0.017313 | -3.61 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.003233 | 0.129 |
| w13 | 19 | 0.059911 | 10.293 |
| w14 | 22 | 0.056589 | 26.03 |
| w15 | 10 | 0.040254 | 2.849 |
| w16 | 9 | -0.077076 | -12.042 |
| w17 | 12 | 0.013154 | -3.028 |
| w18 | 12 | -0.008735 | -6.139 |
| w19 | 4 | -0.108554 | -6.987 |
| w20 | 22 | -0.014204 | 0.077 |
| w21 | 4 | -0.03801 | -3.936 |
| w22 | 2 | -0.042579 | -1.046 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | -0.019025 | -2.259 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.093905 | 2.342 |
| w2 | 8 | -0.10618 | -3.877 |
| w3 | 17 | 0.000802 | -1.395 |
| w4 | 12 | -0.265611 | -24.16 |
| w5 | 13 | -0.08715 | -12.254 |
| w6 | 11 | -0.087356 | -8.694 |
| w7 | 59 | -0.085969 | -5.965 |
| w8 | 4 | 0.02688 | 0.022 |
| w9 | 46 | -0.02627 | 10.965 |
| w10 | 4 | -0.144974 | -3.466 |
| w11 | 0 | None | 0.0 |
| w12 | 19 | -0.05052 | -8.957 |
| w14 | 13 | 0.036698 | 13.757 |
| w15 | 8 | 0.081274 | 2.604 |
| w16 | 4 | -0.091931 | -11.368 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | -0.056708 | -10.117 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.171288 | -10.25 |
| w21 | 3 | -0.012664 | -4.826 |
| w22 | 4 | -0.057225 | -5.523 |
| w23 | 13 | 0.048099 | 10.722 |
| w24 | 2 | 0.002382 | 0.129 |

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
| w1 | 24 | 0.134551 | 25.825 |
| w2 | 7 | -0.084914 | 15.021 |
| w3 | 0 | 0.041747 | 0.0 |
| w4 | 0 | -0.052014 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 12 | 0.075021 | 2.031 |
| w8 | 26 | -0.216184 | -9.074 |
| w9 | 35 | 0.097786 | 22.261 |
| w10 | 9 | -0.010048 | -0.476 |
| w11 | 0 | None | 0.0 |
| w12 | 17 | -0.019169 | -2.007 |
| w14 | 21 | 0.005438 | -13.054 |
| w15 | 20 | -0.045061 | -6.528 |
| w16 | 4 | -0.01641 | -4.2 |
| w17 | 11 | -0.002717 | -0.674 |
| w18 | 13 | -0.022173 | -8.006 |
| w19 | 14 | -0.037703 | -10.666 |
| w20 | 20 | 0.034802 | 9.966 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.010109 | -4.509 |
| w24 | 42 | -0.006259 | 18.178 |

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
| w1 | 24 | 0.123657 | 10.96 |
| w2 | 10 | -0.100674 | -12.666 |
| w3 | 40 | 0.111699 | 11.714 |
| w4 | 12 | -0.089835 | -3.614 |
| w5 | 18 | 0.031572 | 6.002 |
| w6 | 17 | 0.015799 | -1.567 |
| w7 | 40 | -0.120655 | -15.323 |
| w8 | 26 | -0.136615 | -11.967 |
| w9 | 28 | 0.107338 | 19.274 |
| w10 | 2 | -0.081071 | -1.691 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.012561 | -2.527 |
| w13 | 20 | 0.074532 | 19.96 |
| w14 | 24 | 0.06276 | 24.189 |
| w15 | 11 | -0.009307 | 0.331 |
| w16 | 0 | None | 0.0 |
| w17 | 21 | -0.02775 | -16.157 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.112826 | 1.127 |
| w21 | 7 | 0.024605 | -4.533 |
| w22 | 2 | -0.180561 | -3.962 |
| w23 | 17 | -0.043244 | -9.328 |
| w24 | 0 | None | 0.0 |

