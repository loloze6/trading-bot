# Backtest of 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h

- Plan: `../../../../03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.020184 | -4.848 |
| w2 | 11 | -0.000946 | 18.157 |
| w3 | 24 | -0.004246 | -10.24 |
| w4 | 14 | 0.057653 | 15.852 |
| w5 | 19 | -0.002421 | 6.864 |
| w6 | 14 | 0.03063 | 31.724 |
| w7 | 29 | -0.011566 | 6.428 |
| w8 | 15 | 0.036215 | 6.922 |
| w9 | 15 | 0.009193 | 20.751 |
| w10 | 30 | 0.0124 | 20.752 |
| w11 | 6 | -0.008304 | 4.082 |
| w12 | 27 | 0.018981 | -13.929 |
| w13 | 6 | 0.000507 | 0.371 |
| w14 | 20 | -0.029285 | 3.675 |
| w15 | 5 | -0.030752 | 19.197 |
| w16 | 16 | 0.004511 | -9.632 |
| w17 | 20 | -0.003769 | 3.115 |
| w18 | 10 | 0.021702 | 10.042 |
| w19 | 6 | 0.009953 | 12.267 |
| w20 | 11 | -0.037965 | 3.812 |
| w21 | 6 | -0.002887 | 6.701 |
| w22 | 5 | 0.015587 | 0.226 |
| w23 | 25 | 0.023836 | -3.278 |
| w24 | 9 | -0.017829 | -1.382 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.02229 | 2.776 |
| w2 | 9 | 0.033852 | 16.58 |
| w3 | 22 | -0.017366 | -0.257 |
| w4 | 24 | 0.050027 | 13.517 |
| w5 | 28 | 0.001266 | 4.59 |
| w6 | 13 | 0.020919 | 12.772 |
| w7 | 0 | -0.014103 | 0.0 |
| w8 | 16 | 0.040578 | 0.192 |
| w9 | 25 | 0.016619 | 28.988 |
| w10 | 25 | 0.032398 | 13.721 |
| w11 | 8 | 0.000856 | 2.243 |
| w12 | 27 | -0.001567 | -5.304 |
| w13 | 2 | 0.00686 | 4.088 |
| w14 | 0 | 0.006022 | 0.0 |
| w15 | 12 | -0.000377 | 16.458 |
| w16 | 13 | 0.021022 | -15.731 |
| w17 | 14 | -0.027625 | 2.836 |
| w18 | 12 | -0.020855 | 3.979 |
| w19 | 4 | 0.012077 | 0.246 |
| w20 | 2 | -0.001547 | 0.229 |
| w21 | 11 | 0.003009 | 12.84 |
| w22 | 0 | None | 0.0 |
| w23 | 18 | -0.00024 | 2.241 |
| w24 | 15 | 0.01111 | -2.548 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.026027 | 2.247 |
| w2 | 14 | 0.034349 | 10.893 |
| w3 | 18 | 0.008064 | -8.986 |
| w4 | 25 | -0.021636 | 0.489 |
| w5 | 16 | -0.004316 | 5.521 |
| w6 | 28 | 0.027304 | 2.661 |
| w7 | 0 | -0.014591 | 0.0 |
| w8 | 8 | -0.014176 | -10.161 |
| w9 | 23 | 0.022084 | 25.107 |
| w10 | 28 | 0.005911 | 27.524 |
| w11 | 4 | -0.005816 | -7.124 |
| w12 | 19 | 0.012831 | -12.429 |
| w13 | 0 | -0.006078 | 0.0 |
| w14 | 0 | -0.041746 | 0.0 |
| w15 | 10 | 0.005007 | -4.295 |
| w16 | 10 | 0.011583 | 1.601 |
| w17 | 14 | 0.000474 | -8.813 |
| w18 | 11 | -0.011721 | 9.422 |
| w19 | 10 | 0.003467 | 8.186 |
| w20 | 15 | -0.032804 | -1.822 |
| w21 | 18 | 0.001105 | 0.979 |
| w22 | 6 | 0.022019 | -0.836 |
| w23 | 27 | 0.046307 | -4.007 |
| w24 | 10 | 0.014855 | 1.695 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.009746 | 19.436 |
| w2 | 13 | -0.010699 | -1.245 |
| w3 | 22 | -0.002013 | 2.427 |
| w4 | 28 | 0.038297 | -1.535 |
| w5 | 24 | -0.02813 | -0.035 |
| w6 | 22 | -0.021711 | -11.186 |
| w7 | 0 | 0.001999 | 0.0 |
| w8 | 17 | -0.001336 | 5.288 |
| w9 | 22 | -0.010799 | 11.252 |
| w10 | 30 | 0.004566 | -1.261 |
| w11 | 2 | -0.000394 | -0.116 |
| w12 | 20 | 0.035151 | -20.822 |
| w14 | 0 | -0.007426 | 0.0 |
| w15 | 14 | -0.007656 | 7.716 |
| w16 | 7 | 0.01091 | -6.194 |
| w17 | 22 | -0.013566 | 15.727 |
| w18 | 10 | 0.025363 | 2.992 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | 0.058004 | 3.675 |
| w21 | 24 | 0.018499 | 23.288 |
| w22 | 16 | 0.029227 | 7.413 |
| w23 | 13 | 0.025625 | -8.571 |
| w24 | 12 | 0.005503 | -5.761 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 7757 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.035767 | 9.654 |
| w2 | 4 | 0.019651 | 24.127 |
| w3 | 0 | 0.006528 | 0.0 |
| w4 | 0 | 0.049818 | 0.0 |
| w5 | 7 | 0.002269 | 5.826 |
| w6 | 17 | 0.034395 | 4.902 |
| w8 | 13 | 0.000192 | 23.754 |
| w9 | 30 | 0.014455 | 30.881 |
| w10 | 24 | -0.001195 | 11.174 |
| w11 | 5 | 0.014625 | -22.639 |
| w12 | 19 | 0.021896 | -1.343 |
| w14 | 0 | -0.010827 | 0.0 |
| w15 | 19 | -0.00396 | 29.111 |
| w16 | 10 | 0.037295 | -1.207 |
| w17 | 13 | -0.009076 | 3.576 |
| w18 | 14 | -0.004671 | -2.483 |
| w19 | 16 | -0.031691 | -6.566 |
| w20 | 15 | -0.013158 | 23.589 |
| w21 | 18 | 0.000982 | 8.295 |
| w22 | 2 | -0.017055 | 1.497 |
| w23 | 24 | -0.009583 | -0.324 |
| w24 | 22 | -0.009303 | 2.354 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 8280 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 5455 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.002824 | 8.474 |
| w2 | 15 | 0.007549 | 24.315 |
| w3 | 27 | -0.015681 | -15.393 |
| w4 | 29 | -0.012732 | -8.301 |
| w5 | 27 | -0.002938 | -2.523 |
| w6 | 20 | 0.010914 | 4.43 |
| w7 | 0 | -0.005722 | 0.0 |
| w8 | 4 | 0.032827 | -1.209 |
| w9 | 10 | 0.00366 | 10.717 |
| w10 | 16 | 0.002343 | -4.613 |
| w11 | 6 | 0.047702 | 16.704 |
| w12 | 18 | -0.032061 | -27.402 |
| w14 | 0 | -0.010183 | 0.0 |
| w15 | 16 | 0.005894 | 26.721 |
| w16 | 4 | -0.016877 | 26.481 |
| w17 | 14 | 0.001998 | 17.68 |
| w18 | 9 | -0.015709 | 6.051 |
| w19 | 4 | 0.012485 | -3.561 |
| w20 | 12 | 0.012954 | 1.67 |
| w21 | 11 | 0.008837 | 5.801 |
| w22 | 8 | 0.065307 | -1.763 |
| w23 | 28 | 0.011044 | -10.531 |
| w24 | 8 | -0.019043 | -2.417 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 9318 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

