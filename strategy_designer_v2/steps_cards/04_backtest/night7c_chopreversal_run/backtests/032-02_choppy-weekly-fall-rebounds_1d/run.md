# Backtest of 032-02_choppy-weekly-fall-rebounds_1d

- Plan: `../../../../03_test_plan/night7c_chopreversal_run/plans/032-02_choppy-weekly-fall-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.089731 | -0.611 |
| w2 | 10 | -0.327265 | -25.715 |
| w3 | 11 | 0.087597 | 3.043 |
| w4 | 2 | 0.157648 | 1.225 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | 0.031442 | 6.288 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.032547 | 4.11 |
| w9 | 14 | -0.128732 | -10.373 |
| w10 | 12 | 0.138604 | 3.236 |
| w11 | 14 | 0.106023 | 19.91 |
| w12 | 11 | 0.111973 | 15.205 |
| w13 | 26 | -0.015643 | -5.0 |
| w14 | 2 | 0.207201 | 1.108 |
| w15 | 26 | -0.051129 | 8.155 |
| w16 | 8 | -0.318032 | -28.196 |
| w17 | 13 | 0.01323 | 20.047 |
| w18 | 22 | -0.116048 | -17.088 |
| w19 | 26 | 0.051769 | 15.011 |
| w20 | 26 | 0.117539 | 6.39 |
| w21 | 8 | 0.028435 | 13.695 |
| w22 | 13 | 0.191175 | 4.383 |
| w23 | 0 | 0.112478 | 0.0 |
| w24 | 27 | -0.072786 | -24.214 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.066516 | -1.107 |
| w2 | 22 | -0.07396 | -24.755 |
| w3 | 19 | 0.085146 | -0.095 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.079914 | 7.005 |
| w7 | 0 | None | 0.0 |
| w8 | 14 | 0.010822 | 2.182 |
| w9 | 7 | 0.002018 | 4.871 |
| w10 | 10 | 0.091481 | 7.248 |
| w11 | 18 | -0.042551 | 18.319 |
| w12 | 12 | 0.137412 | 8.719 |
| w13 | 16 | 0.02716 | 0.106 |
| w14 | 11 | 0.101889 | -1.071 |
| w15 | 14 | -0.037122 | 0.177 |
| w16 | 11 | -0.147801 | -8.86 |
| w17 | 20 | 0.131755 | 34.603 |
| w18 | 22 | -0.037895 | -0.511 |
| w19 | 24 | 0.058568 | 19.08 |
| w20 | 32 | -0.0006 | -4.087 |
| w21 | 18 | 0.034547 | 3.503 |
| w22 | 28 | 0.037984 | -24.612 |
| w23 | 7 | 0.153743 | 10.941 |
| w24 | 12 | -0.02133 | -10.76 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 18 | -0.227006 | -10.02 |
| w3 | 12 | 0.069922 | 18.307 |
| w4 | 8 | 0.151411 | 3.835 |
| w5 | 11 | 0.056404 | 1.979 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 18 | 0.006713 | 9.909 |
| w9 | 0 | None | 0.0 |
| w10 | 7 | 0.056631 | 8.246 |
| w11 | 26 | -0.059562 | 13.298 |
| w12 | 21 | 0.020069 | 4.51 |
| w13 | 10 | -0.08377 | -1.888 |
| w14 | 7 | 0.068074 | 3.152 |
| w15 | 20 | 0.033764 | 4.524 |
| w16 | 17 | -0.173289 | -14.595 |
| w17 | 18 | 0.022701 | 21.338 |
| w18 | 15 | -0.030023 | -9.59 |
| w19 | 22 | 0.053867 | 8.226 |
| w20 | 20 | 0.035713 | 1.435 |
| w21 | 22 | 0.123169 | 26.726 |
| w22 | 42 | 0.02779 | -0.816 |
| w23 | 13 | 0.000504 | 5.926 |
| w24 | 19 | 0.016078 | -9.417 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.123416 | -9.71 |
| w2 | 12 | -0.100608 | -23.71 |
| w3 | 10 | -0.026586 | -2.18 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 8 | 0.04469 | 6.017 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.083183 | 3.632 |
| w9 | 1 | -0.012138 | -4.852 |
| w10 | 3 | 0.141183 | 3.197 |
| w11 | 15 | -0.034498 | 9.899 |
| w12 | 11 | 0.126371 | 7.432 |
| w14 | 6 | 0.117191 | 5.183 |
| w15 | 19 | 0.060826 | 8.416 |
| w16 | 15 | -0.031544 | -21.205 |
| w17 | 16 | 0.082578 | 19.196 |
| w18 | 27 | 0.040685 | -11.163 |
| w19 | 31 | 0.101215 | 9.569 |
| w20 | 9 | 0.113765 | 13.963 |
| w21 | 13 | 0.098552 | 15.722 |
| w22 | 15 | 0.051041 | 15.595 |
| w23 | 11 | 0.041921 | -10.082 |
| w24 | 25 | 0.057638 | 31.26 |

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
| w1 | 2 | 0.149932 | 0.682 |
| w2 | 0 | -0.052845 | 0.0 |
| w3 | 0 | 1.9e-05 | 0.0 |
| w4 | 0 | -0.029506 | 0.0 |
| w5 | 11 | -0.000886 | 7.142 |
| w6 | 8 | 0.001943 | 0.618 |
| w8 | 5 | 0.068904 | -1.009 |
| w9 | 6 | -0.008055 | 6.4 |
| w10 | 1 | 0.029834 | 0.734 |
| w11 | 23 | -0.048688 | 37.298 |
| w12 | 5 | 0.035751 | -0.578 |
| w14 | 12 | 0.001676 | 10.183 |
| w15 | 15 | 0.01871 | 7.348 |
| w16 | 22 | -0.082156 | -13.951 |
| w17 | 13 | 0.030917 | -1.438 |
| w18 | 20 | 0.023858 | -8.549 |
| w19 | 30 | -0.041187 | -13.981 |
| w20 | 17 | 0.199332 | 55.743 |
| w21 | 17 | -0.080775 | -4.248 |
| w22 | 33 | 0.017792 | 3.811 |
| w23 | 7 | 0.163353 | 6.803 |
| w24 | 10 | -0.113718 | -1.177 |

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
| w1 | 4 | 0.029942 | -4.408 |
| w2 | 15 | -0.014474 | -11.206 |
| w3 | 4 | 0.050903 | 1.651 |
| w4 | 2 | 0.012094 | 0.763 |
| w5 | 6 | 0.004916 | 3.904 |
| w6 | 8 | -0.042693 | -1.862 |
| w7 | 10 | -0.048942 | -9.078 |
| w8 | 6 | 0.10108 | 4.817 |
| w9 | 18 | 0.074991 | -0.663 |
| w10 | 14 | 0.044101 | 5.374 |
| w11 | 27 | -0.060001 | 38.741 |
| w12 | 23 | 0.062686 | 41.342 |
| w13 | 20 | 0.002042 | -10.839 |
| w14 | 7 | 0.044568 | -11.034 |
| w15 | 20 | -0.02646 | -7.231 |
| w16 | 21 | -0.045232 | 7.596 |
| w17 | 25 | 0.218405 | 15.982 |
| w18 | 24 | 0.040353 | -3.715 |
| w19 | 30 | -0.002059 | -15.577 |
| w20 | 23 | -0.145073 | -5.311 |
| w21 | 17 | 0.053748 | 17.908 |
| w22 | 29 | 0.096922 | -12.818 |
| w23 | 9 | -0.081213 | -8.455 |
| w24 | 13 | -0.086915 | 3.031 |

