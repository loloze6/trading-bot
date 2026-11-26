# Backtest of 058-01_agitated-decline-rally-giveback_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01_agitated-decline-rally-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 19 | 0.035445 | 6.508 |
| w3 | 15 | 0.054948 | 4.247 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.009927 | -4.982 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.066054 | 3.018 |
| w9 | 7 | -0.248075 | -6.87 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 16 | -0.068763 | -0.299 |
| w14 | 12 | -0.027996 | 2.717 |
| w15 | 0 | 0.066112 | 0.0 |
| w16 | 20 | 0.042011 | -12.129 |
| w17 | 0 | None | 0.0 |
| w18 | 19 | 0.087141 | -9.399 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.024127 | -2.619 |
| w21 | 0 | None | 0.0 |
| w22 | 18 | 0.000772 | -3.632 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.040975 | 3.612 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.035058 | 9.298 |
| w2 | 20 | -0.055493 | 7.693 |
| w3 | 5 | 0.032579 | -0.037 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.035975 | 3.666 |
| w9 | 6 | 0.100317 | 1.665 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 26 | -0.13166 | -6.783 |
| w15 | 4 | -0.015725 | 0.065 |
| w16 | 15 | 0.064684 | -6.176 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | 0.022303 | -6.628 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | -0.08063 | -12.721 |
| w21 | 8 | -0.027002 | -8.889 |
| w22 | 17 | 0.167169 | 30.808 |
| w23 | 1 | 0.03334 | 0.239 |
| w24 | 9 | 0.040308 | 20.954 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 21 | 0.103314 | 1.174 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 8 | 0.071789 | 0.441 |
| w6 | 4 | -0.112222 | -8.974 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.006181 | 7.514 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.156228 | 2.097 |
| w13 | 8 | -0.055618 | -8.093 |
| w14 | 17 | -0.084768 | -6.092 |
| w15 | 5 | 0.066141 | 2.76 |
| w16 | 14 | 0.097121 | -1.923 |
| w17 | 6 | 0.045705 | -0.199 |
| w18 | 11 | 0.047159 | 2.938 |
| w19 | 0 | 0.047511 | 0.0 |
| w20 | 18 | -0.072591 | -12.514 |
| w21 | 2 | -0.047127 | 0.126 |
| w22 | 16 | -0.054819 | -3.005 |
| w23 | 1 | 0.075743 | -1.251 |
| w24 | 18 | 0.198293 | 2.477 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.104395 | -9.569 |
| w2 | 17 | -0.049383 | -15.047 |
| w3 | 2 | 0.014843 | 0.173 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | 0.062069 | -0.804 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.098122 | 4.515 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 14 | -0.034414 | 3.675 |
| w15 | 2 | -0.037017 | -2.196 |
| w16 | 20 | 0.032673 | -13.121 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.119092 | 3.952 |
| w19 | 17 | -0.050143 | -9.098 |
| w20 | 4 | -0.0055 | -5.696 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | -0.045808 | 1.028 |
| w24 | 6 | -0.105979 | -7.522 |

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
| w1 | 2 | 0.021195 | -0.023 |
| w2 | 0 | 0.096087 | 0.0 |
| w3 | 0 | -0.004026 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.036796 | -5.608 |
| w8 | 2 | -0.024052 | -0.213 |
| w9 | 7 | 0.010751 | 0.738 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.023746 | -10.828 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.001106 | -1.67 |
| w15 | 5 | 0.003177 | 1.39 |
| w16 | 22 | 0.138745 | -1.937 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | 0.072473 | 2.513 |
| w19 | 2 | -0.051279 | -1.566 |
| w20 | 7 | -0.104023 | -28.069 |
| w21 | 1 | 0.034997 | -0.444 |
| w22 | 10 | 0.055612 | -1.662 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.097959 | 12.767 |

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
| w1 | 0 | None | 0.0 |
| w2 | 15 | 0.063527 | 11.317 |
| w3 | 12 | -0.005883 | 2.393 |
| w4 | 7 | 0.092794 | 1.254 |
| w5 | 11 | -0.047748 | -4.531 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.029162 | 0.698 |
| w9 | 15 | 0.025878 | 15.432 |
| w10 | 2 | -0.01149 | 0.705 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.07729 | 1.56 |
| w14 | 12 | -0.037336 | -0.264 |
| w15 | 1 | 0.127271 | 1.295 |
| w16 | 26 | -0.050815 | -18.66 |
| w17 | 6 | -0.015971 | -5.069 |
| w18 | 6 | 0.032951 | 1.396 |
| w19 | 21 | -0.073978 | -18.407 |
| w20 | 10 | -0.150224 | -22.674 |
| w21 | 7 | -0.004662 | -9.961 |
| w22 | 22 | -0.050457 | 0.018 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

