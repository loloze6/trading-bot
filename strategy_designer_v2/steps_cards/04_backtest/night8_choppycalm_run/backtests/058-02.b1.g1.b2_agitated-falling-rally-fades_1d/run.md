# Backtest of 058-02.b1.g1.b2_agitated-falling-rally-fades_1d

- Plan: `../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b2_agitated-falling-rally-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.108114 | 0.0 |
| w2 | 24 | 0.009399 | 7.74 |
| w3 | 15 | 0.018987 | 1.953 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.050041 | -5.147 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.136325 | 3.036 |
| w9 | 9 | -0.166415 | -7.024 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.005793 | -0.229 |
| w13 | 23 | 0.005237 | 0.234 |
| w14 | 18 | 0.148115 | 18.821 |
| w15 | 0 | None | 0.0 |
| w16 | 21 | 0.048592 | 1.952 |
| w17 | 0 | None | 0.0 |
| w18 | 26 | 0.073698 | 7.307 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.065715 | 3.525 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.055253 | 3.454 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.046709 | -2.249 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.008023 | 1.014 |
| w2 | 26 | -0.032119 | 1.12 |
| w3 | 6 | 0.008912 | 0.948 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.066502 | 1.509 |
| w9 | 5 | 0.070644 | 3.446 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 33 | 9e-06 | 4.141 |
| w15 | 7 | 0.048444 | 1.704 |
| w16 | 19 | 0.077386 | 2.645 |
| w17 | 1 | 1.8e-05 | -0.113 |
| w18 | 17 | -0.020836 | -3.257 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.104198 | 11.354 |
| w21 | 14 | -0.000584 | -3.105 |
| w22 | 29 | 0.24633 | 36.369 |
| w23 | 3 | 0.02106 | -0.127 |
| w24 | 10 | -0.050659 | -2.956 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 30 | 0.181417 | 25.245 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 8 | 0.016306 | 1.221 |
| w6 | 4 | -0.112784 | -7.118 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.004875 | -2.558 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.020713 | -0.189 |
| w13 | 9 | -0.033215 | -1.215 |
| w14 | 19 | -0.037883 | -4.802 |
| w15 | 8 | 0.070109 | 4.163 |
| w16 | 16 | 0.113925 | 6.5 |
| w17 | 4 | 0.013335 | -0.37 |
| w18 | 12 | -0.011032 | -1.16 |
| w19 | 0 | None | 0.0 |
| w20 | 26 | 0.054295 | 6.285 |
| w21 | 0 | None | 0.0 |
| w22 | 19 | 0.052219 | 3.014 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 19 | -0.021544 | -2.078 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.023868 | -2.586 |
| w2 | 22 | -0.110814 | -11.379 |
| w3 | 2 | 0.001268 | -0.17 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | -0.101782 | -8.699 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.137328 | 3.505 |
| w9 | 1 | 0.089178 | 0.435 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 18 | 0.068921 | 6.972 |
| w15 | 3 | -0.012684 | -0.618 |
| w16 | 23 | 0.062113 | 1.369 |
| w17 | 0 | None | 0.0 |
| w18 | 15 | 0.000472 | -0.542 |
| w19 | 18 | -0.047119 | -7.213 |
| w20 | 3 | 0.030868 | 0.003 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.22805 | -19.879 |
| w24 | 6 | -0.043956 | -4.532 |

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
| w1 | 2 | 0.089711 | 3.68 |
| w2 | 1 | 0.107404 | 10.259 |
| w3 | 0 | 0.01118 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.043982 | -3.31 |
| w8 | 2 | 0.024763 | 0.533 |
| w9 | 6 | 0.054861 | 4.282 |
| w10 | 0 | None | 0.0 |
| w11 | 11 | -0.236119 | -28.317 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.050507 | 2.294 |
| w15 | 5 | 0.009891 | 0.551 |
| w16 | 17 | 0.191157 | 18.038 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.070078 | 3.853 |
| w19 | 2 | 0.023666 | 0.067 |
| w20 | 9 | -0.009215 | -4.522 |
| w21 | 2 | 0.117647 | 6.082 |
| w22 | 17 | 0.07851 | 4.924 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.00771 | 0.415 |

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
| w2 | 23 | 0.098641 | 9.195 |
| w3 | 15 | -0.145542 | -9.975 |
| w4 | 6 | 0.109742 | 4.163 |
| w5 | 11 | -0.1664 | -9.111 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.132543 | 2.187 |
| w9 | 16 | 0.042827 | 4.99 |
| w10 | 1 | -0.015115 | -0.331 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.121002 | 5.217 |
| w14 | 14 | 0.033067 | 2.254 |
| w15 | 4 | 0.118045 | 2.289 |
| w16 | 27 | 0.006779 | -9.72 |
| w17 | 7 | -0.052407 | -3.424 |
| w18 | 17 | 0.02029 | 1.337 |
| w19 | 24 | -0.082002 | -11.625 |
| w20 | 8 | -0.051099 | -7.36 |
| w21 | 6 | -0.009105 | -4.292 |
| w22 | 32 | -0.010728 | -1.078 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

