# Backtest of N1-01_trend-with-rising-month_1d

- Plan: `../../../../03_test_plan/overnight_run/plans/N1-01_trend-with-rising-month_1d.md`
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
| w4 | 31 | -0.161437 | 12.358 |
| w5 | 8 | 0.050238 | 4.922 |
| w6 | 23 | 0.032175 | 57.24 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.007595 | 7.444 |
| w9 | 10 | -0.026639 | -7.021 |
| w10 | 33 | -0.038746 | 7.84 |
| w11 | 26 | -0.02578 | 58.36 |
| w12 | 17 | 0.035676 | 3.653 |
| w13 | 7 | -0.004349 | -2.843 |
| w14 | 0 | None | 0.0 |
| w15 | 33 | 0.051025 | 78.727 |
| w16 | 13 | -0.063748 | -9.864 |
| w17 | 29 | 0.154403 | 300.592 |
| w18 | 10 | -0.131967 | -20.678 |
| w19 | 21 | 0.048891 | 40.461 |
| w20 | 21 | -0.072637 | -9.62 |
| w21 | 27 | 0.009782 | 46.041 |
| w22 | 13 | -0.038184 | -6.725 |
| w23 | 25 | 0.009553 | 8.785 |
| w24 | 17 | -0.072119 | -14.091 |

- ETHUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.05541 | -4.003 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 26 | -0.175005 | 1.46 |
| w5 | 20 | -0.195516 | -22.465 |
| w6 | 24 | -0.049429 | 7.564 |
| w7 | 5 | 0.070406 | 1.504 |
| w8 | 5 | -0.048889 | -5.103 |
| w9 | 3 | -0.016578 | -3.873 |
| w10 | 35 | 0.046574 | 102.01 |
| w11 | 33 | 0.002233 | 270.013 |
| w12 | 30 | -0.091158 | -24.998 |
| w13 | 17 | 0.005697 | 11.517 |
| w14 | 0 | None | 0.0 |
| w15 | 30 | 0.042281 | 12.794 |
| w16 | 21 | -0.019949 | 15.829 |
| w17 | 46 | -0.022663 | 26.114 |
| w18 | 18 | 0.025127 | 18.626 |
| w19 | 25 | 0.012603 | 17.893 |
| w20 | 9 | -0.006451 | -5.064 |
| w21 | 15 | -0.00215 | 14.484 |
| w22 | 4 | -0.151318 | -7.648 |
| w24 | 8 | -0.117553 | -15.955 |

- w23 not run: the engine stopped.

```
  File "/usr/local/lib/python3.13/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Invalid control character at: line 253 column 22 (char 8218)
```

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | -0.037062 | -3.877 |
| w4 | 36 | -0.075754 | -4.218 |
| w5 | 14 | -0.079179 | -23.46 |
| w6 | 3 | -0.236724 | -8.155 |
| w7 | 2 | 0.016491 | -1.495 |
| w8 | 17 | -0.090343 | 17.465 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | -0.026606 | -1.983 |
| w11 | 34 | -0.120744 | -15.261 |
| w12 | 22 | -0.145392 | -48.52 |
| w13 | 8 | -0.067286 | -24.442 |
| w14 | 0 | None | 0.0 |
| w15 | 29 | 0.058626 | 14.182 |
| w16 | 9 | -0.039425 | -5.79 |
| w17 | 36 | 0.018418 | 63.319 |
| w18 | 12 | -0.083725 | -35.827 |
| w19 | 31 | -0.036165 | -24.182 |
| w20 | 6 | -0.068022 | -6.605 |
| w21 | 16 | 0.033234 | 20.375 |
| w22 | 24 | -0.09062 | -38.798 |
| w23 | 24 | -0.02612 | 1.135 |
| w24 | 16 | -0.277824 | -50.074 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.087915 | -26.105 |
| w2 | 2 | -0.07601 | -6.248 |
| w3 | 4 | -0.030848 | -2.891 |
| w4 | 34 | -0.033425 | -8.02 |
| w5 | 12 | 0.02876 | 1.085 |
| w6 | 32 | -0.184687 | -17.412 |
| w7 | 2 | 0.029866 | 0.06 |
| w8 | 6 | -0.14617 | -18.697 |
| w9 | 1 | -0.15505 | -6.553 |
| w10 | 34 | -0.034011 | 11.334 |
| w11 | 37 | -0.038021 | 51.288 |
| w12 | 8 | -0.207603 | -14.988 |
| w14 | 0 | None | 0.0 |
| w15 | 36 | -0.121301 | -41.952 |
| w16 | 25 | -0.078502 | -18.948 |
| w17 | 40 | -0.007103 | 47.631 |
| w18 | 18 | -0.007056 | -18.275 |
| w19 | 6 | -0.154303 | -35.915 |
| w20 | 29 | -0.090549 | -10.066 |
| w21 | 35 | -0.014759 | -7.833 |
| w22 | 30 | 0.042215 | 29.525 |
| w23 | 15 | 0.085696 | 21.824 |
| w24 | 53 | -0.226712 | -22.149 |

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
| w3 | 8 | -0.101585 | -13.425 |
| w4 | 23 | -0.039072 | 1.344 |
| w5 | 13 | -0.074818 | -37.74 |
| w6 | 22 | -0.061707 | -5.975 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.127393 | 49.889 |
| w11 | 37 | -0.023889 | 115.098 |
| w12 | 17 | -0.162918 | -25.716 |
| w14 | 5 | -0.131818 | -26.377 |
| w15 | 22 | -0.076748 | -32.757 |
| w16 | 14 | -0.045333 | -9.475 |
| w17 | 29 | 0.190999 | 159.484 |
| w18 | 14 | -0.028347 | -23.586 |
| w19 | 22 | -0.090891 | -30.613 |
| w20 | 16 | -0.111114 | -23.856 |
| w21 | 23 | 0.279501 | 730.122 |
| w22 | 17 | -0.06394 | -25.093 |
| w23 | 20 | 0.00042 | 6.887 |
| w24 | 6 | -0.109849 | -12.578 |

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
| w1 | 13 | -0.007506 | -8.792 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.122873 | -13.809 |
| w7 | 1 | -0.211954 | -5.293 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 39 | -0.071489 | 4.077 |
| w11 | 44 | -0.158989 | 21.056 |
| w12 | 25 | -0.108958 | -50.161 |
| w13 | 16 | -0.133856 | -42.424 |
| w14 | 0 | None | 0.0 |
| w15 | 29 | 0.067864 | 3.567 |
| w16 | 17 | -0.036985 | 7.705 |
| w17 | 28 | -0.058525 | -30.249 |
| w18 | 13 | -0.149884 | -62.38 |
| w19 | 15 | 0.020828 | -3.497 |
| w20 | 22 | -0.03699 | 7.485 |
| w21 | 39 | -0.051505 | 4.965 |
| w22 | 2 | -0.17668 | -17.81 |
| w23 | 31 | -0.131735 | -26.373 |
| w24 | 41 | 0.153302 | 3629.8 |

