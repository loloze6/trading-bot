# Backtest of 058-01_agitated-rise-stretch-giveback_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/058-01_agitated-rise-stretch-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.102582 | -7.272 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.032018 | 6.542 |
| w4 | 12 | -0.02055 | -12.518 |
| w5 | 0 | None | 0.0 |
| w6 | 23 | 0.063317 | -17.337 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.023802 | -3.646 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | 0.287325 | 7.801 |
| w11 | 38 | -0.062115 | -33.637 |
| w12 | 5 | -0.206793 | -28.465 |
| w13 | 2 | 0.103035 | 2.354 |
| w14 | 0 | None | 0.0 |
| w15 | 35 | 0.043746 | -20.181 |
| w16 | 0 | None | 0.0 |
| w17 | 18 | -0.064785 | -27.547 |
| w18 | 3 | 0.075945 | 1.179 |
| w19 | 22 | 0.054444 | -15.572 |
| w20 | 0 | None | 0.0 |
| w21 | 13 | 0.017736 | -11.158 |
| w22 | 2 | -0.006045 | -0.539 |
| w23 | 1 | 0.063978 | -0.206 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | -0.015401 | 0.343 |
| w3 | 3 | 0.030247 | 0.816 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 23 | 0.188155 | 14.318 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.032204 | 0.691 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | 0.114192 | 3.34 |
| w11 | 37 | -0.015505 | -42.271 |
| w12 | 7 | 0.018935 | -3.642 |
| w13 | 11 | -0.070723 | -14.033 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | 0.045974 | 6.077 |
| w16 | 7 | 0.046606 | 4.446 |
| w17 | 19 | 0.124152 | 9.657 |
| w18 | 8 | -0.062533 | -15.507 |
| w19 | 13 | 0.141184 | 45.8 |
| w20 | 6 | 0.017142 | -0.513 |
| w21 | 25 | -0.03139 | -21.027 |
| w22 | 5 | 0.013781 | 3.888 |
| w23 | 9 | 0.073337 | -5.99 |
| w24 | 3 | 0.040328 | 2.437 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 8 | -0.028976 | -12.151 |
| w4 | 0 | None | 0.0 |
| w5 | 6 | 0.112692 | 12.31 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 26 | 0.04641 | -17.709 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | 0.094396 | 5.733 |
| w11 | 30 | 0.018358 | -20.009 |
| w12 | 2 | -0.017368 | -0.679 |
| w13 | 0 | 0.137285 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.062985 | -14.942 |
| w16 | 2 | -0.034363 | -0.275 |
| w17 | 24 | -0.033668 | -28.84 |
| w18 | 7 | -0.016053 | -3.542 |
| w19 | 14 | 0.005624 | -17.902 |
| w20 | 0 | None | 0.0 |
| w21 | 25 | -0.04077 | -32.6 |
| w22 | 19 | 0.131879 | 9.935 |
| w23 | 1 | 0.061502 | 2.328 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.030382 | -3.285 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.084011 | 2.843 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.161265 | 1.956 |
| w11 | 26 | 0.043382 | -25.746 |
| w12 | 2 | 0.008103 | -1.979 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | 0.115779 | 13.882 |
| w16 | 4 | 0.036097 | -0.788 |
| w17 | 24 | 0.152092 | 5.996 |
| w18 | 7 | 0.068846 | 5.485 |
| w19 | 0 | 0.095511 | 0.0 |
| w20 | 14 | -0.048084 | -9.518 |
| w21 | 9 | 0.099412 | 9.08 |
| w22 | 23 | 0.05373 | -9.069 |
| w23 | 6 | 0.005086 | -2.612 |
| w24 | 38 | 0.123184 | -4.506 |

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
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.036429 | 0.0 |
| w4 | 0 | 0.121012 | 0.0 |
| w5 | 5 | 0.061472 | 5.257 |
| w6 | 9 | 0.112787 | 13.823 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.082461 | 0.827 |
| w10 | 5 | -0.017079 | -4.604 |
| w11 | 20 | -0.047407 | -35.697 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.066474 | 3.497 |
| w15 | 11 | 0.009581 | 0.04 |
| w16 | 7 | -0.007088 | -2.141 |
| w17 | 7 | -0.08921 | -19.957 |
| w18 | 2 | 0.197812 | 4.377 |
| w19 | 3 | 0.183036 | 1.45 |
| w20 | 14 | 0.034094 | -1.031 |
| w21 | 15 | -0.345018 | -74.965 |
| w22 | 13 | 0.141653 | 9.85 |
| w23 | 2 | 0.12645 | 2.054 |
| w24 | 0 | None | 0.0 |

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
| w1 | 9 | -0.032629 | -2.887 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.269174 | 10.268 |
| w7 | 0 | 0.115252 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.184864 | 15.86 |
| w11 | 31 | -0.05157 | -43.737 |
| w12 | 7 | 0.01562 | 1.47 |
| w13 | 8 | 0.108864 | 5.953 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 7e-06 | -14.068 |
| w16 | 17 | -0.080521 | -27.034 |
| w17 | 10 | 0.126973 | 12.97 |
| w18 | 9 | 0.035587 | 2.615 |
| w19 | 5 | 0.024086 | 0.206 |
| w20 | 18 | -0.081386 | -21.921 |
| w21 | 23 | 0.011394 | -23.274 |
| w22 | 1 | 0.029721 | -0.303 |
| w23 | 11 | -0.047638 | -6.377 |
| w24 | 34 | -0.172411 | -77.662 |

