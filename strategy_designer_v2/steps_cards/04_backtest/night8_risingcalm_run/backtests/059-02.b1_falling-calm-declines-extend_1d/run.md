# Backtest of 059-02.b1_falling-calm-declines-extend_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/059-02.b1_falling-calm-declines-extend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.052582 | -3.48 |
| w2 | 21 | 0.083934 | 32.762 |
| w3 | 25 | 0.073527 | -9.209 |
| w4 | 2 | 0.004406 | -0.702 |
| w5 | 11 | -0.089226 | -10.39 |
| w6 | 6 | 0.071732 | -2.658 |
| w7 | 21 | 0.008456 | 9.37 |
| w8 | 6 | 0.032906 | 0.121 |
| w9 | 32 | -0.220921 | -39.781 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -6.927 |
| w12 | 8 | -0.021291 | 0.166 |
| w13 | 15 | -0.002154 | -3.73 |
| w14 | 16 | 0.148535 | 39.502 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.080762 | -13.615 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.082146 | -6.64 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -9.502 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.195226 | 16.206 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.017786 | 5.712 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 20 | 0.114457 | 0.572 |
| w4 | 3 | -0.063113 | -1.176 |
| w5 | 7 | -0.059005 | -2.214 |
| w6 | 16 | 0.064755 | -2.022 |
| w7 | 41 | 0.044739 | 34.534 |
| w8 | 0 | None | 0.0 |
| w9 | 34 | -0.13169 | -21.168 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.024259 | 1.591 |
| w13 | 17 | 0.160506 | 26.059 |
| w14 | 9 | 0.158506 | 33.933 |
| w15 | 13 | 0.049742 | 4.816 |
| w16 | 6 | -0.096673 | -6.711 |
| w17 | 10 | -0.04705 | -8.237 |
| w18 | 2 | -0.011453 | -2.289 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.022337 | -8.135 |
| w22 | 11 | -0.057329 | 3.779 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.036798 | 8.507 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | 0.005545 | 14.386 |
| w2 | 8 | 0.106095 | 19.859 |
| w3 | 12 | -0.008669 | -1.312 |
| w4 | 5 | -0.127949 | -13.826 |
| w5 | 4 | -0.070681 | -0.197 |
| w6 | 15 | 0.063732 | 0.316 |
| w7 | 45 | 0.047174 | 50.062 |
| w8 | 0 | None | 0.0 |
| w9 | 55 | 0.015085 | 19.115 |
| w10 | 12 | -0.030533 | -1.513 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.006824 | -6.044 |
| w13 | 26 | 0.004865 | 0.281 |
| w14 | 26 | 0.117946 | 35.351 |
| w15 | 11 | 0.075225 | 3.505 |
| w16 | 14 | -0.086559 | -12.172 |
| w17 | 12 | -0.052342 | -13.025 |
| w18 | 14 | -0.050987 | -11.663 |
| w19 | 3 | -0.112482 | -17.903 |
| w20 | 19 | -0.024978 | 0.295 |
| w21 | 10 | -0.04454 | -6.192 |
| w22 | 3 | 0.124184 | 9.451 |
| w23 | 6 | -0.143798 | -6.533 |
| w24 | 17 | -0.050824 | -6.215 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.125122 | -13.209 |
| w2 | 9 | -0.120955 | -4.231 |
| w3 | 19 | -0.049054 | -2.782 |
| w4 | 12 | -0.330779 | -15.399 |
| w5 | 11 | -0.112313 | -7.226 |
| w6 | 11 | -0.078643 | -4.805 |
| w7 | 46 | -0.024631 | 22.852 |
| w8 | 3 | 0.039276 | 0.393 |
| w9 | 42 | -0.04321 | 13.155 |
| w10 | 4 | -0.16002 | -2.293 |
| w11 | 0 | None | 0.0 |
| w12 | 31 | 0.000102 | 0.1 |
| w14 | 11 | 0.183459 | 58.069 |
| w15 | 8 | 0.074132 | 7.859 |
| w16 | 4 | -0.152323 | -10.797 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | -0.075332 | -10.662 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.100971 | -7.852 |
| w21 | 6 | -0.059261 | -15.122 |
| w22 | 6 | -0.146581 | -14.733 |
| w23 | 15 | 0.067849 | 26.749 |
| w24 | 4 | 0.011739 | -1.821 |

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
| w1 | 26 | 0.082249 | 29.332 |
| w2 | 7 | -0.058705 | 18.436 |
| w3 | 0 | 0.027644 | 0.0 |
| w4 | 0 | -0.012536 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | 0.009685 | -1.086 |
| w8 | 29 | -0.162868 | -11.086 |
| w9 | 30 | 0.090852 | 21.999 |
| w10 | 11 | -0.081797 | -8.844 |
| w11 | 0 | None | 0.0 |
| w12 | 27 | -0.024781 | -1.082 |
| w14 | 19 | 0.046476 | -19.517 |
| w15 | 19 | 0.02352 | 5.232 |
| w16 | 4 | -0.071063 | -4.861 |
| w17 | 15 | -0.00304 | -2.814 |
| w18 | 13 | -0.022286 | -10.611 |
| w19 | 20 | -0.081639 | -12.478 |
| w20 | 24 | 0.041122 | 8.297 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.068396 | -0.631 |
| w23 | 3 | 0.027682 | -3.088 |
| w24 | 38 | -0.066549 | 28.766 |

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
| w1 | 29 | 0.009703 | -0.719 |
| w2 | 10 | -0.171091 | -9.557 |
| w3 | 37 | 0.089188 | 24.827 |
| w4 | 22 | -0.08083 | -12.832 |
| w5 | 26 | -0.028281 | 15.989 |
| w6 | 14 | 0.020185 | -2.579 |
| w7 | 47 | -0.066028 | -20.258 |
| w8 | 24 | -0.020256 | -6.39 |
| w9 | 27 | 0.067879 | 13.744 |
| w10 | 2 | -0.081071 | 1.295 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.030976 | -3.132 |
| w13 | 21 | 0.055745 | 13.492 |
| w14 | 27 | 0.061099 | 28.784 |
| w15 | 12 | 0.028585 | 8.643 |
| w16 | 0 | None | 0.0 |
| w17 | 23 | 0.040476 | -10.025 |
| w18 | 8 | -0.066511 | -9.417 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | -0.012472 | -8.088 |
| w21 | 8 | -0.036495 | -8.423 |
| w22 | 2 | -0.180561 | -2.386 |
| w23 | 15 | -0.016091 | -10.408 |
| w24 | 0 | None | 0.0 |

