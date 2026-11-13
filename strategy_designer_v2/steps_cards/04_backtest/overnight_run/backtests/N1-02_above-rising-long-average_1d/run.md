# Backtest of N1-02_above-rising-long-average_1d

- Plan: `../../../../03_test_plan/overnight_run/plans_newcomp/N1-02_above-rising-long-average_1d.md`
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
| w4 | 16 | -0.194469 | 4.661 |
| w5 | 14 | -0.021614 | -6.444 |
| w6 | 13 | -0.03225 | 48.756 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.018482 | -5.332 |
| w10 | 25 | -0.170076 | -2.045 |
| w11 | 25 | 0.030918 | 149.918 |
| w12 | 23 | -0.14135 | -40.292 |
| w13 | 11 | -0.082151 | -30.009 |
| w14 | 0 | None | 0.0 |
| w15 | 20 | -0.065424 | 47.875 |
| w16 | 0 | None | 0.0 |
| w17 | 18 | 0.094842 | 327.947 |
| w18 | 2 | -0.150132 | -16.731 |
| w19 | 28 | 0.045516 | 57.193 |
| w20 | 6 | -0.014005 | 1.238 |
| w21 | 6 | 0.006869 | 51.054 |
| w22 | 17 | -0.045014 | -11.761 |
| w23 | 23 | -0.184042 | -5.47 |
| w24 | 14 | 0.021679 | -6.941 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.077647 | -5.715 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 16 | -0.171959 | -5.858 |
| w5 | 23 | -0.057999 | -14.374 |
| w6 | 6 | -0.015396 | 19.007 |
| w7 | 2 | -0.012111 | -5.946 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.039856 | -2.09 |
| w10 | 25 | 0.003652 | 140.754 |
| w11 | 28 | -0.007374 | 468.157 |
| w12 | 19 | -0.201978 | -22.204 |
| w13 | 23 | -0.046031 | -20.321 |
| w14 | 0 | None | 0.0 |
| w15 | 25 | -0.080323 | -34.191 |
| w16 | 10 | -0.177761 | -59.703 |
| w17 | 38 | -0.311562 | -10.15 |
| w18 | 13 | -0.082752 | -15.86 |
| w19 | 24 | 0.005559 | 37.729 |
| w20 | 9 | 0.00655 | -6.387 |
| w21 | 11 | -0.085196 | -8.887 |
| w22 | 5 | -0.077539 | -8.002 |
| w23 | 9 | -0.042079 | 19.955 |
| w24 | 12 | -0.009178 | -22.524 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.100183 | -10.273 |
| w4 | 35 | -0.149992 | -12.797 |
| w5 | 14 | -0.165095 | -19.306 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.017723 | 0.0 |
| w8 | 12 | -0.046723 | 5.807 |
| w9 | 0 | None | 0.0 |
| w10 | 13 | -0.010882 | 2.018 |
| w11 | 30 | -0.083193 | 96.351 |
| w12 | 1 | -0.1759 | -8.908 |
| w13 | 19 | -0.123211 | -45.772 |
| w14 | 0 | None | 0.0 |
| w15 | 30 | 0.104825 | 16.976 |
| w16 | 0 | None | 0.0 |
| w17 | 29 | 0.134279 | 235.902 |
| w18 | 8 | -0.066883 | -32.279 |
| w19 | 18 | -0.067537 | -36.601 |
| w20 | 8 | -0.035355 | -7.369 |
| w21 | 12 | -0.004774 | 2.312 |
| w22 | 30 | -0.016099 | -33.308 |
| w23 | 17 | -0.110662 | -18.166 |
| w24 | 10 | -0.103134 | -34.51 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 32 | -0.182545 | -28.707 |
| w5 | 15 | -0.049036 | -6.041 |
| w6 | 24 | -0.172126 | -16.715 |
| w7 | 0 | -0.013331 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | -0.157897 | 0.0 |
| w10 | 29 | -0.008503 | 31.709 |
| w11 | 34 | -0.107872 | 120.126 |
| w12 | 1 | -0.159232 | -3.603 |
| w14 | 0 | None | 0.0 |
| w15 | 27 | -0.100476 | -38.107 |
| w16 | 6 | -0.121676 | -20.635 |
| w17 | 46 | -0.261999 | 29.949 |
| w18 | 17 | -0.169471 | -68.033 |
| w19 | 3 | -0.135014 | -11.708 |
| w20 | 14 | -0.153606 | -12.478 |
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
| w3 | 0 | None | 0.0 |
| w4 | 18 | -0.115104 | -21.704 |
| w5 | 22 | -0.113429 | -46.42 |
| w6 | 16 | -0.123237 | -9.937 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | 0.047024 | 26.885 |
| w11 | 40 | -0.042015 | 194.169 |
| w12 | 6 | -0.111407 | -19.228 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | -0.11399 | -33.421 |
| w16 | 0 | None | 0.0 |
| w17 | 29 | 0.021455 | -64.909 |
| w18 | 20 | -0.162379 | -76.756 |
| w19 | 17 | -0.241999 | -47.331 |
| w20 | 11 | -0.119397 | -11.65 |
| w21 | 14 | 0.178998 | 531.975 |
| w22 | 11 | -0.015072 | -12.26 |
| w23 | 12 | -0.173491 | -20.97 |
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
| w1 | 12 | -0.104233 | -32.461 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.211954 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 36 | -0.080584 | 14.444 |
| w11 | 38 | -0.175733 | 210.781 |
| w12 | 3 | -0.086367 | -8.661 |
| w13 | 19 | -0.111792 | -58.365 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.118771 | -45.943 |
| w16 | 1 | -0.030024 | 0.099 |
| w17 | 38 | -0.370872 | -70.534 |
| w18 | 9 | -0.112437 | -77.209 |
| w19 | 14 | -0.105082 | -31.049 |
| w20 | 13 | -0.048577 | -7.44 |
| w21 | 37 | -0.053885 | 13.565 |
| w22 | 8 | -0.09899 | -28.905 |
| w23 | 7 | -0.126825 | -10.67 |
| w24 | 45 | 0.028525 | 2726.859 |

