# Backtest of 002-03_price-cross-above-long-sma_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 20 | -0.189079 | 14.769 |
| w5 | 14 | -0.021614 | -6.444 |
| w6 | 13 | -0.03225 | 48.756 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.050942 | 1.617 |
| w9 | 3 | -0.018482 | -5.332 |
| w10 | 28 | -0.149427 | 6.88 |
| w11 | 25 | 0.030918 | 149.918 |
| w12 | 30 | -0.099463 | -31.483 |
| w13 | 11 | -0.082151 | -30.009 |
| w14 | 0 | None | 0.0 |
| w15 | 26 | 0.017044 | 109.02 |
| w16 | 10 | -0.106279 | -11.549 |
| w17 | 18 | 0.094842 | 327.947 |
| w18 | 2 | -0.150132 | -16.731 |
| w19 | 28 | 0.045516 | 57.193 |
| w20 | 6 | -0.014005 | 1.238 |
| w21 | 11 | -0.010936 | 47.888 |
| w22 | 17 | -0.045014 | -11.761 |
| w23 | 23 | -0.184042 | -5.47 |
| w24 | 14 | 0.021679 | -6.941 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.08041 | -5.715 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 26 | -0.210177 | -3.081 |
| w5 | 23 | -0.057999 | -14.374 |
| w6 | 15 | -0.049476 | 13.536 |
| w7 | 2 | -0.012111 | -5.946 |
| w8 | 5 | -0.091273 | -6.599 |
| w9 | 1 | -0.039856 | -2.09 |
| w10 | 25 | 0.003652 | 140.754 |
| w11 | 28 | -0.007374 | 468.157 |
| w12 | 19 | -0.201978 | -22.204 |
| w13 | 23 | -0.046031 | -20.321 |
| w14 | 0 | None | 0.0 |
| w15 | 31 | 0.012037 | -3.372 |
| w16 | 22 | -0.096052 | -36.05 |
| w17 | 38 | -0.311562 | -10.15 |
| w18 | 13 | -0.082752 | -15.86 |
| w19 | 24 | 0.005559 | 37.729 |
| w20 | 9 | 0.00655 | -6.387 |
| w21 | 17 | -0.128822 | -15.037 |
| w22 | 13 | -0.041109 | -15.032 |
| w23 | 15 | 0.005844 | 85.014 |
| w24 | 12 | -0.009178 | -22.524 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.089517 | -10.953 |
| w4 | 35 | -0.149992 | -12.797 |
| w5 | 14 | -0.165095 | -19.306 |
| w6 | 0 | -0.241789 | 0.0 |
| w7 | 0 | -0.017723 | 0.0 |
| w8 | 16 | -0.083054 | 11.519 |
| w9 | 0 | None | 0.0 |
| w10 | 19 | -0.068853 | -10.854 |
| w11 | 30 | -0.083193 | 96.351 |
| w12 | 19 | -0.150248 | -46.372 |
| w13 | 19 | -0.123211 | -45.772 |
| w14 | 0 | None | 0.0 |
| w15 | 30 | 0.104825 | 16.976 |
| w16 | 12 | -0.099487 | -20.531 |
| w17 | 33 | 0.06799 | 119.895 |
| w18 | 8 | -0.066883 | -32.279 |
| w19 | 26 | -0.027402 | -29.714 |
| w20 | 8 | -0.035355 | -7.369 |
| w21 | 21 | 0.009956 | 14.584 |
| w22 | 30 | -0.016099 | -33.308 |
| w23 | 22 | -0.128369 | -20.864 |
| w24 | 17 | -0.096419 | -41.826 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.076409 | -21.712 |
| w2 | 3 | -0.320316 | -7.017 |
| w3 | 1 | -0.05892 | -1.598 |
| w4 | 36 | -0.183935 | -25.775 |
| w5 | 16 | -0.056183 | -6.726 |
| w6 | 32 | -0.140985 | -10.03 |
| w7 | 0 | -0.013331 | 0.0 |
| w8 | 1 | -0.194054 | -3.118 |
| w9 | 0 | -0.157897 | 0.0 |
| w10 | 29 | -0.008503 | 31.709 |
| w11 | 34 | -0.107872 | 120.126 |
| w12 | 2 | -0.203143 | -5.417 |
| w14 | 0 | None | 0.0 |
| w15 | 42 | -0.105016 | -38.936 |
| w16 | 22 | -0.098311 | -27.267 |
| w17 | 46 | -0.261999 | 29.949 |
| w18 | 17 | -0.169471 | -68.033 |
| w19 | 10 | -0.278267 | -39.856 |
| w20 | 36 | -0.230054 | -19.605 |
| w21 | 32 | -0.091741 | -22.973 |
| w22 | 33 | -0.085753 | 25.32 |
| w23 | 15 | 0.070696 | 8.851 |
| w24 | 33 | -0.162475 | -12.147 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.184623 | -11.817 |
| w4 | 18 | -0.115104 | -21.704 |
| w5 | 34 | -0.129411 | -38.253 |
| w6 | 16 | -0.123237 | -9.937 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | 0.047024 | 26.885 |
| w11 | 40 | -0.042015 | 194.169 |
| w12 | 10 | -0.203686 | -29.032 |
| w14 | 2 | -0.199841 | -4.777 |
| w15 | 31 | -0.110303 | -47.019 |
| w16 | 7 | -0.077685 | -10.152 |
| w17 | 34 | 0.019055 | -65.671 |
| w18 | 20 | -0.162379 | -76.756 |
| w19 | 29 | -0.160543 | -44.748 |
| w20 | 21 | -0.172163 | -27.026 |
| w21 | 23 | 0.190042 | 647.58 |
| w22 | 11 | -0.015072 | -12.26 |
| w23 | 13 | -0.152555 | -18.775 |
| w24 | 10 | -0.026928 | -15.685 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.06219 | -23.933 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 12 | -0.224981 | -12.544 |
| w7 | 0 | -0.211954 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 36 | -0.080584 | 14.444 |
| w11 | 38 | -0.175733 | 210.781 |
| w12 | 26 | -0.138606 | -62.512 |
| w13 | 19 | -0.111792 | -58.365 |
| w14 | 0 | None | 0.0 |
| w15 | 23 | -0.021221 | -29.33 |
| w16 | 20 | -0.138644 | -31.861 |
| w17 | 38 | -0.370872 | -70.534 |
| w18 | 9 | -0.112437 | -77.209 |
| w19 | 21 | -0.0559 | -24.161 |
| w20 | 26 | -0.040916 | -0.516 |
| w21 | 43 | -0.051242 | 25.119 |
| w22 | 8 | -0.09899 | -28.905 |
| w23 | 17 | -0.214062 | -21.756 |
| w24 | 45 | 0.028525 | 2726.859 |

