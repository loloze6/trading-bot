# Backtest of 074-01_agitated-stretch-below-rebounds_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/074-01_agitated-stretch-below-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.072113 | 0.351 |
| w2 | 17 | -0.015327 | -15.551 |
| w3 | 15 | 0.11661 | 7.619 |
| w4 | 2 | 0.291751 | 3.464 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.130852 | 6.841 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.003097 | -0.72 |
| w9 | 10 | -0.159459 | 8.731 |
| w10 | 5 | 0.089978 | 3.833 |
| w11 | 15 | 0.169076 | 20.383 |
| w12 | 13 | 0.115356 | 24.407 |
| w13 | 24 | 0.057789 | 10.204 |
| w14 | 14 | 0.017836 | -11.922 |
| w15 | 18 | -0.037453 | 8.048 |
| w16 | 8 | -0.021891 | -23.804 |
| w17 | 7 | 0.035097 | 15.76 |
| w18 | 26 | -0.000111 | -11.844 |
| w19 | 21 | 0.033556 | 5.677 |
| w20 | 15 | 0.151372 | 11.841 |
| w21 | 7 | 0.016136 | 6.485 |
| w22 | 14 | 0.179473 | 8.424 |
| w23 | 0 | None | 0.0 |
| w24 | 27 | 0.075764 | -20.18 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.090486 | 3.333 |
| w2 | 26 | -0.031824 | -19.731 |
| w3 | 15 | 0.130703 | 3.738 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.148995 | 1.549 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.00639 | 0.31 |
| w9 | 13 | 0.043451 | 13.307 |
| w10 | 8 | 0.117166 | 4.682 |
| w11 | 10 | -0.027462 | 17.035 |
| w12 | 10 | 0.135674 | 14.235 |
| w13 | 9 | 0.118204 | 1.277 |
| w14 | 23 | 0.034228 | -1.505 |
| w15 | 19 | -0.036905 | -0.638 |
| w16 | 9 | -0.044092 | -10.209 |
| w17 | 16 | 0.112413 | 9.459 |
| w18 | 24 | 0.056325 | 10.769 |
| w19 | 23 | 0.078485 | 14.478 |
| w20 | 28 | 0.039307 | 19.709 |
| w21 | 15 | -0.013369 | 3.004 |
| w22 | 32 | 0.117847 | -30.86 |
| w23 | 4 | 0.04305 | 2.107 |
| w24 | 20 | 0.146494 | -4.304 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 23 | 0.064691 | -2.188 |
| w3 | 9 | 0.115762 | 23.484 |
| w4 | 4 | 0.184014 | 7.502 |
| w5 | 14 | 0.053535 | 1.018 |
| w6 | 1 | 0.160846 | 11.639 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.034092 | 0.347 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.143248 | 3.982 |
| w11 | 23 | 0.036071 | 27.222 |
| w12 | 23 | -0.028073 | -7.795 |
| w13 | 11 | 0.043842 | 7.95 |
| w14 | 14 | 0.096975 | 4.18 |
| w15 | 17 | 0.170838 | 4.057 |
| w16 | 13 | -0.050785 | -12.869 |
| w17 | 20 | -0.027369 | 15.847 |
| w18 | 19 | 0.039213 | -11.938 |
| w19 | 19 | 0.057827 | 35.512 |
| w20 | 21 | 0.058496 | 11.351 |
| w21 | 14 | 0.04593 | 21.389 |
| w22 | 35 | 0.046228 | -6.211 |
| w23 | 7 | -0.003115 | 3.856 |
| w24 | 25 | 0.12752 | 4.565 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.058293 | -6.179 |
| w2 | 18 | -0.117791 | -28.122 |
| w3 | 8 | 0.039615 | 9.995 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.080727 | 9.88 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.042429 | -0.1 |
| w9 | 1 | -0.012138 | -2.957 |
| w10 | 2 | 0.081798 | 1.235 |
| w11 | 15 | 0.045368 | 25.465 |
| w12 | 13 | 0.089607 | 7.153 |
| w14 | 19 | 0.07037 | -1.435 |
| w15 | 14 | 0.116758 | 9.073 |
| w16 | 12 | -0.119444 | -21.515 |
| w17 | 11 | 0.044587 | 10.575 |
| w18 | 25 | 0.108026 | 0.863 |
| w19 | 23 | 0.222659 | 19.206 |
| w20 | 9 | 0.073709 | 3.085 |
| w21 | 7 | 0.025944 | 5.046 |
| w22 | 15 | 0.173808 | 16.575 |
| w23 | 12 | 0.242049 | 7.881 |
| w24 | 12 | 0.194776 | 34.08 |

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
| w1 | 5 | 0.1569 | 1.557 |
| w2 | 6 | -0.002584 | -19.072 |
| w3 | 0 | 0.045217 | 0.0 |
| w4 | 0 | -0.050443 | 0.0 |
| w5 | 13 | -0.0238 | -1.231 |
| w6 | 14 | 0.032802 | 8.408 |
| w8 | 3 | 0.042101 | -1.045 |
| w9 | 9 | 0.078729 | 7.382 |
| w10 | 5 | 0.026102 | 1.61 |
| w11 | 23 | 0.022584 | 44.299 |
| w12 | 3 | 0.016133 | -3.063 |
| w14 | 13 | 0.045888 | 15.993 |
| w15 | 11 | 0.020113 | 4.244 |
| w16 | 19 | -0.044027 | -15.365 |
| w17 | 17 | -0.061032 | -10.64 |
| w18 | 23 | 0.007245 | -10.758 |
| w19 | 15 | -0.011226 | -9.888 |
| w20 | 14 | 0.190999 | 111.668 |
| w21 | 20 | -0.108267 | -0.713 |
| w22 | 20 | 0.111787 | 5.957 |
| w23 | 5 | 0.185858 | 8.609 |
| w24 | 8 | 0.101056 | -0.646 |

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
| w1 | 8 | 0.04662 | -0.719 |
| w2 | 24 | 0.014962 | -12.393 |
| w3 | 7 | 0.177694 | 16.327 |
| w4 | 0 | 0.071138 | 0.0 |
| w5 | 9 | 0.135222 | 17.314 |
| w6 | 8 | 0.001473 | 3.613 |
| w7 | 9 | -0.079535 | -9.104 |
| w8 | 4 | 0.090328 | -1.081 |
| w9 | 14 | 0.143907 | 13.981 |
| w10 | 7 | 0.057822 | 1.834 |
| w11 | 20 | 0.051248 | 52.821 |
| w12 | 22 | 0.020707 | 15.302 |
| w13 | 21 | 0.077789 | -5.327 |
| w14 | 19 | 0.139072 | -11.888 |
| w15 | 18 | -0.102232 | -23.74 |
| w16 | 23 | -0.146879 | -7.844 |
| w17 | 28 | 0.172144 | 14.339 |
| w18 | 27 | 0.078048 | -7.313 |
| w19 | 33 | -0.024406 | -5.675 |
| w20 | 19 | -0.121866 | 32.217 |
| w21 | 15 | -0.011554 | 18.718 |
| w22 | 28 | 0.003979 | -2.606 |
| w23 | 9 | -0.114534 | -9.101 |
| w24 | 11 | -0.055943 | 5.475 |

