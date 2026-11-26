# Backtest of 068-02_falling-agitated-run-break-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/068-02_falling-agitated-run-break-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.127084 | 7.975 |
| w2 | 17 | 0.075907 | 20.366 |
| w3 | 15 | -0.050611 | -7.215 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.189 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.214699 | 11.803 |
| w9 | 8 | -0.037776 | -3.217 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.025499 | -1.224 |
| w13 | 13 | 0.076202 | 9.178 |
| w14 | 14 | 0.154066 | 28.153 |
| w15 | 0 | None | 0.0 |
| w16 | 14 | 0.117722 | 11.992 |
| w17 | 0 | None | 0.0 |
| w18 | 22 | 0.11506 | 19.305 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.012828 | -1.471 |
| w21 | 0 | None | 0.0 |
| w22 | 15 | 0.021541 | -0.703 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.002799 | 1.763 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.018015 | -2.343 |
| w2 | 20 | -0.003005 | 5.983 |
| w3 | 7 | -0.011108 | -0.987 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.125327 | 6.066 |
| w9 | 5 | 0.082267 | 7.395 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 26 | 0.108343 | 30.803 |
| w15 | 5 | 0.000707 | -1.138 |
| w16 | 13 | 0.106499 | 8.471 |
| w17 | 1 | -0.029217 | -1.607 |
| w18 | 8 | 0.004898 | -1.174 |
| w19 | 0 | None | 0.0 |
| w20 | 16 | 0.083665 | 13.497 |
| w21 | 6 | 0.040611 | 0.848 |
| w22 | 21 | 0.109106 | 31.614 |
| w23 | 2 | 0.024436 | -0.17 |
| w24 | 7 | -0.085653 | -7.072 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 20 | 0.073602 | 17.607 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 6 | -0.034131 | -3.765 |
| w6 | 1 | -0.135216 | -5.164 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.03348 | -1.372 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.035714 | -1.501 |
| w13 | 6 | -0.020912 | -1.473 |
| w14 | 15 | 0.119513 | 21.543 |
| w15 | 5 | 0.027643 | 1.169 |
| w16 | 12 | 0.157481 | 15.371 |
| w17 | 1 | -0.009055 | -1.209 |
| w18 | 12 | 0.037974 | 3.435 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.105443 | 15.844 |
| w21 | 0 | None | 0.0 |
| w22 | 14 | 0.076828 | 9.545 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 12 | -0.089047 | -11.295 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.026229 | -0.556 |
| w2 | 14 | -0.042351 | -8.931 |
| w3 | 3 | 0.013981 | -0.011 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.108858 | -6.891 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.05064 | 0.444 |
| w9 | 2 | 0.05278 | 2.672 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 17 | 0.139675 | 26.964 |
| w15 | 3 | 0.012229 | -0.109 |
| w16 | 14 | 0.115546 | 8.778 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | -0.01978 | -3.091 |
| w19 | 14 | -0.043703 | -10.433 |
| w20 | 3 | 0.020396 | -0.727 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.203791 | -20.566 |
| w24 | 4 | 0.046697 | 0.865 |

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
| w1 | 1 | 0.0449 | 1.753 |
| w2 | 1 | 0.082536 | 18.026 |
| w3 | 0 | 0.007787 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.013003 | -0.86 |
| w8 | 3 | -5.7e-05 | -0.061 |
| w9 | 4 | 0.095228 | 7.393 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | 0.006177 | -3.404 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.026218 | 1.628 |
| w15 | 4 | 0.024843 | 2.146 |
| w16 | 17 | 0.193902 | 26.372 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.042308 | 3.377 |
| w19 | 2 | 0.032699 | 0.819 |
| w20 | 5 | 0.091161 | 5.02 |
| w21 | 2 | 0.104554 | 10.174 |
| w22 | 10 | 0.061448 | 5.24 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.064118 | 7.192 |

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
| w2 | 20 | 0.284592 | 53.55 |
| w3 | 8 | -0.088415 | -9.489 |
| w4 | 4 | 0.054679 | 2.743 |
| w5 | 4 | -0.283471 | -22.859 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.18756 | 9.262 |
| w9 | 12 | 0.014853 | 2.405 |
| w10 | 1 | -0.015115 | -0.779 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | 0.133209 | 11.489 |
| w14 | 11 | 0.172894 | 26.362 |
| w15 | 3 | 0.046652 | 3.147 |
| w16 | 15 | -0.0566 | -16.511 |
| w17 | 4 | -0.028498 | -2.787 |
| w18 | 12 | 0.09578 | 10.313 |
| w19 | 14 | -0.05924 | -12.061 |
| w20 | 6 | -0.025076 | -6.346 |
| w21 | 2 | 0.001233 | -1.439 |
| w22 | 18 | -0.178944 | -26.509 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

