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
| w4 | 19 | -0.189079 | 10.188 |
| w5 | 16 | -0.021614 | -5.597 |
| w6 | 12 | -0.03225 | 46.518 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.050942 | 0.704 |
| w9 | 3 | -0.018482 | -3.562 |
| w10 | 29 | -0.149427 | 12.492 |
| w11 | 16 | 0.030918 | 63.611 |
| w12 | 28 | -0.099463 | -19.96 |
| w13 | 9 | -0.082151 | -8.736 |
| w14 | 0 | None | 0.0 |
| w15 | 18 | 0.017044 | 83.673 |
| w16 | 10 | -0.106279 | -7.659 |
| w17 | 14 | 0.094842 | 194.565 |
| w18 | 3 | -0.150132 | -7.159 |
| w19 | 23 | 0.045516 | 56.199 |
| w20 | 9 | -0.014005 | -1.223 |
| w21 | 10 | -0.010936 | 48.997 |
| w22 | 17 | -0.045014 | -10.67 |
| w23 | 28 | -0.184042 | -7.032 |
| w24 | 17 | 0.021679 | -6.988 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.08041 | -2.974 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 26 | -0.210177 | -2.802 |
| w5 | 25 | -0.057999 | -11.887 |
| w6 | 16 | -0.049476 | 10.317 |
| w7 | 2 | -0.012111 | -2.064 |
| w8 | 5 | -0.091273 | -2.621 |
| w9 | 1 | -0.039856 | -1.307 |
| w10 | 23 | 0.003652 | 87.279 |
| w11 | 13 | -0.007374 | 122.61 |
| w12 | 18 | -0.201978 | -11.428 |
| w13 | 16 | -0.046031 | 0.699 |
| w14 | 0 | None | 0.0 |
| w15 | 23 | 0.012037 | 10.505 |
| w16 | 18 | -0.096052 | -12.067 |
| w17 | 32 | -0.311562 | 5.077 |
| w18 | 13 | -0.082752 | -2.44 |
| w19 | 22 | 0.005559 | 29.873 |
| w20 | 9 | 0.00655 | -4.764 |
| w21 | 17 | -0.128822 | -6.598 |
| w22 | 15 | -0.041109 | -8.927 |
| w23 | 9 | 0.005844 | 56.243 |
| w24 | 12 | -0.009178 | -12.424 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | -0.089517 | -4.37 |
| w4 | 34 | -0.149992 | -7.937 |
| w5 | 14 | -0.165095 | -7.792 |
| w6 | 0 | -0.241789 | 0.0 |
| w7 | 0 | -0.017723 | 0.0 |
| w8 | 13 | -0.083054 | 6.462 |
| w9 | 0 | None | 0.0 |
| w10 | 19 | -0.068853 | -4.717 |
| w11 | 22 | -0.083193 | 38.232 |
| w12 | 19 | -0.150248 | -19.895 |
| w13 | 14 | -0.123211 | -8.336 |
| w14 | 0 | None | 0.0 |
| w15 | 25 | 0.104825 | 14.605 |
| w16 | 12 | -0.099487 | -8.454 |
| w17 | 22 | 0.06799 | 64.254 |
| w18 | 5 | -0.066883 | -8.171 |
| w19 | 22 | -0.027402 | -1.956 |
| w20 | 8 | -0.035355 | -3.96 |
| w21 | 15 | 0.009956 | 24.157 |
| w22 | 28 | -0.016099 | -8.866 |
| w23 | 22 | -0.128369 | -11.334 |
| w24 | 17 | -0.096419 | -24.822 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.076409 | -7.779 |
| w2 | 3 | -0.320316 | -3.806 |
| w3 | 1 | -0.05892 | -0.973 |
| w4 | 37 | -0.183935 | -23.91 |
| w5 | 18 | -0.056183 | -6.37 |
| w6 | 35 | -0.140985 | -4.315 |
| w7 | 0 | -0.013331 | 0.0 |
| w8 | 1 | -0.194054 | -1.542 |
| w9 | 0 | -0.157897 | 0.0 |
| w10 | 26 | -0.008503 | 37.607 |
| w11 | 26 | -0.107872 | 56.965 |
| w12 | 2 | -0.203143 | -2.893 |
| w14 | 0 | None | 0.0 |
| w15 | 37 | -0.105016 | -10.714 |
| w16 | 22 | -0.098311 | -11.484 |
| w17 | 34 | -0.261999 | 17.539 |
| w18 | 17 | -0.169471 | -29.666 |
| w19 | 10 | -0.278267 | -34.414 |
| w20 | 35 | -0.230054 | -15.398 |
| w21 | 33 | -0.091741 | -13.491 |
| w22 | 35 | -0.085753 | 20.902 |
| w23 | 14 | 0.070696 | 16.445 |
| w24 | 37 | -0.162475 | -4.802 |

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
| w3 | 4 | -0.184623 | -4.928 |
| w4 | 15 | -0.115104 | -10.19 |
| w5 | 30 | -0.129411 | 22.686 |
| w6 | 16 | -0.123237 | -4.102 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.047024 | 21.444 |
| w11 | 30 | -0.042015 | 71.946 |
| w12 | 9 | -0.203686 | -9.113 |
| w14 | 2 | -0.199841 | -1.289 |
| w15 | 32 | -0.110303 | -17.567 |
| w16 | 7 | -0.077685 | -4.859 |
| w17 | 27 | 0.019055 | 51.107 |
| w18 | 19 | -0.162379 | -15.755 |
| w19 | 29 | -0.160543 | -25.11 |
| w20 | 21 | -0.172163 | -15.152 |
| w21 | 18 | 0.190042 | 226.771 |
| w22 | 9 | -0.015072 | -2.778 |
| w23 | 13 | -0.152555 | -8.305 |
| w24 | 10 | -0.026928 | -11.185 |

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
| w1 | 21 | -0.06219 | -7.554 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | -0.224981 | -9.26 |
| w7 | 0 | -0.211954 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 32 | -0.080584 | 22.3 |
| w11 | 18 | -0.175733 | 65.206 |
| w12 | 22 | -0.138606 | -19.556 |
| w13 | 15 | -0.111792 | -13.1 |
| w14 | 0 | None | 0.0 |
| w15 | 24 | -0.021221 | -10.826 |
| w16 | 21 | -0.138644 | -10.376 |
| w17 | 39 | -0.370872 | -33.443 |
| w18 | 7 | -0.112437 | -25.767 |
| w19 | 24 | -0.0559 | -10.834 |
| w20 | 22 | -0.040916 | 3.6 |
| w21 | 35 | -0.051242 | 35.095 |
| w22 | 8 | -0.09899 | -8.643 |
| w23 | 17 | -0.214062 | -10.088 |
| w24 | 17 | 0.028525 | 322.246 |

