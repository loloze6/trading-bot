# Backtest of 058-02.g1_choppy-agitated-dip-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/058-02.g1_choppy-agitated-dip-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.003551 | -1.337 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.032472 | 4.066 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 6 | -0.050891 | -0.615 |
| w10 | 4 | 0.056953 | -4.478 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.014888 | -5.745 |
| w13 | 4 | 0.059828 | 7.256 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.024536 | -4.078 |
| w16 | 2 | 0.351216 | 38.501 |
| w17 | 11 | -0.059538 | -8.83 |
| w18 | 6 | -0.036684 | 0.955 |
| w19 | 9 | -0.047728 | -12.873 |
| w20 | 51 | -0.03262 | 10.715 |
| w21 | 12 | -0.043 | -10.709 |
| w22 | 2 | 0.108883 | 9.083 |
| w23 | 5 | -0.05693 | -8.392 |
| w24 | 18 | -0.009134 | 9.505 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | -0.09464 | -3.687 |
| w3 | 11 | 0.109808 | 5.344 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.00786 | 2.124 |
| w9 | 6 | 0.003841 | 1.686 |
| w10 | 6 | 0.067028 | -1.549 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.083578 | -10.61 |
| w13 | 0 | 0.024651 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.032121 | 6.701 |
| w16 | 2 | 0.135025 | 5.926 |
| w17 | 5 | -0.171165 | -8.064 |
| w18 | 7 | 0.057898 | 7.227 |
| w19 | 9 | -0.019656 | -3.576 |
| w20 | 17 | -0.042339 | -2.982 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | -0.071197 | 4.185 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.087679 | -1.034 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | 0.020838 | 2.358 |
| w4 | 10 | -0.21191 | -16.018 |
| w5 | 17 | -0.140612 | -27.641 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.006295 | -4.868 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | 0.024397 | -5.342 |
| w13 | 2 | -0.021693 | 0.594 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.101702 | -0.656 |
| w16 | 1 | 0.410454 | 19.944 |
| w17 | 8 | 0.025602 | -3.825 |
| w18 | 5 | 0.16562 | 0.154 |
| w19 | 18 | 0.019462 | -8.177 |
| w20 | 5 | 0.038275 | -0.13 |
| w21 | 8 | 0.026549 | -8.661 |
| w22 | 13 | 0.116209 | 8.153 |
| w23 | 4 | -0.034127 | -3.919 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.012182 | -4.393 |
| w2 | 6 | 0.131693 | 19.865 |
| w3 | 13 | -0.014451 | -5.685 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.159889 | -12.034 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.061708 | -11.493 |
| w12 | 4 | -0.18962 | -8.652 |
| w14 | 2 | -0.043374 | -0.019 |
| w15 | 17 | 0.030485 | 3.672 |
| w16 | 1 | 0.338337 | 28.545 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | -0.103038 | -4.992 |
| w19 | 34 | 0.052752 | 8.732 |
| w20 | 13 | -0.135879 | -20.866 |
| w21 | 15 | -0.071662 | -19.361 |
| w22 | 16 | -0.058878 | -8.417 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.085932 | -10.642 |

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
| w1 | 4 | -0.022959 | -2.137 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.306119 | 0.0 |
| w4 | 0 | -0.152249 | 0.0 |
| w5 | 14 | -0.021115 | -13.53 |
| w6 | 7 | 0.007739 | -0.429 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.109677 | -7.622 |
| w10 | 0 | None | 0.0 |
| w11 | 10 | 0.069655 | -4.546 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | -0.083829 | -3.85 |
| w15 | 6 | -0.049081 | 6.269 |
| w16 | 10 | 0.209201 | 11.562 |
| w17 | 8 | -0.114528 | -7.269 |
| w18 | 2 | 0.116531 | 2.324 |
| w19 | 17 | -0.136918 | -7.815 |
| w20 | 7 | -0.096104 | -21.752 |
| w21 | 7 | 0.04982 | 2.446 |
| w22 | 13 | -0.06406 | -11.502 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.076395 | 5.414 |

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
| w1 | 6 | -0.164544 | -8.534 |
| w2 | 2 | -0.043081 | 0.003 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 10 | -0.058022 | 1.066 |
| w6 | 3 | 0.046328 | -4.9 |
| w7 | 2 | 0.021554 | 1.609 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.084245 | 0.256 |
| w11 | 8 | -0.066421 | -10.667 |
| w12 | 7 | 0.002351 | -1.171 |
| w13 | 6 | -0.23091 | -16.016 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.027121 | -2.451 |
| w16 | 1 | None | -0.03 |
| w17 | 25 | 0.034732 | 0.305 |
| w18 | 6 | -0.101139 | -4.621 |
| w19 | 10 | -0.098941 | -4.58 |
| w20 | 10 | 0.066164 | 7.199 |
| w21 | 9 | 0.067379 | -4.477 |
| w22 | 11 | -0.000393 | 6.234 |
| w23 | 5 | -0.041319 | -5.835 |
| w24 | 2 | -0.002679 | -0.745 |

