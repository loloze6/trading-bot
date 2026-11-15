# Backtest of 002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d

- Plan: `../../../03_test_plan/plans/002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d.md`
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
| w4 | 31 | -0.161437 | 13.074 |
| w5 | 9 | 0.050238 | 4.253 |
| w6 | 25 | 0.032175 | 57.487 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.007595 | 4.699 |
| w9 | 10 | -0.026639 | -4.033 |
| w10 | 35 | -0.038746 | 14.166 |
| w11 | 22 | -0.02578 | 32.437 |
| w12 | 18 | 0.035676 | 1.425 |
| w13 | 7 | -0.004349 | -0.714 |
| w14 | 0 | None | 0.0 |
| w15 | 24 | 0.051025 | 61.521 |
| w16 | 13 | -0.063748 | -6.288 |
| w17 | 25 | 0.154403 | 182.141 |
| w18 | 10 | -0.131967 | -11.705 |
| w19 | 19 | 0.048891 | 41.251 |
| w20 | 21 | -0.072637 | -8.269 |
| w21 | 22 | 0.009782 | 43.64 |
| w22 | 13 | -0.038184 | -5.782 |
| w23 | 26 | 0.009553 | 5.795 |
| w24 | 23 | -0.072119 | -17.749 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.05541 | -2.018 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 26 | -0.175005 | 1.739 |
| w5 | 20 | -0.195516 | -19.725 |
| w6 | 21 | -0.049429 | 11.615 |
| w7 | 5 | 0.070406 | 0.706 |
| w8 | 6 | -0.048889 | -1.722 |
| w9 | 3 | -0.016578 | -2.369 |
| w10 | 34 | 0.046574 | 71.223 |
| w11 | 28 | 0.002233 | 80.906 |
| w12 | 30 | -0.091158 | -13.404 |
| w13 | 16 | 0.005697 | 7.331 |
| w14 | 0 | None | 0.0 |
| w15 | 26 | 0.042281 | 15.27 |
| w16 | 19 | -0.019949 | 11.914 |
| w17 | 36 | -0.022663 | 20.625 |
| w18 | 14 | 0.025127 | 16.412 |
| w19 | 23 | 0.012603 | 18.06 |
| w20 | 9 | -0.006451 | -4.009 |
| w21 | 13 | -0.00215 | 11.048 |
| w22 | 4 | -0.151318 | -4.336 |
| w23 | 20 | -0.00403 | 42.065 |
| w24 | 8 | -0.117553 | -8.617 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.037062 | -2.738 |
| w4 | 35 | -0.075754 | -3.898 |
| w5 | 13 | -0.079179 | -11.54 |
| w6 | 3 | -0.236724 | -7.193 |
| w7 | 2 | 0.016491 | -0.54 |
| w8 | 17 | -0.090343 | 6.307 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | -0.026606 | 1.538 |
| w11 | 29 | -0.120744 | 6.929 |
| w12 | 19 | -0.145392 | -20.067 |
| w13 | 8 | -0.067286 | -7.832 |
| w14 | 0 | None | 0.0 |
| w15 | 28 | 0.058626 | 9.021 |
| w16 | 10 | -0.039425 | -1.613 |
| w17 | 29 | 0.018418 | 32.605 |
| w18 | 9 | -0.083725 | -9.986 |
| w19 | 29 | -0.036165 | 3.101 |
| w20 | 6 | -0.068022 | -3.037 |
| w21 | 12 | 0.033234 | 21.314 |
| w22 | 22 | -0.09062 | -14.89 |
| w23 | 22 | -0.02612 | 4.748 |
| w24 | 16 | -0.277824 | -31.697 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.087915 | -9.909 |
| w2 | 2 | -0.07601 | -2.019 |
| w3 | 4 | -0.030848 | -1.755 |
| w4 | 37 | -0.033425 | -4.552 |
| w5 | 12 | 0.029004 | 1.107 |
| w6 | 32 | -0.184687 | -17.002 |
| w7 | 2 | 0.029866 | 0.017 |
| w8 | 6 | -0.14617 | -9.698 |
| w9 | 1 | -0.15505 | -3.499 |
| w10 | 34 | -0.034011 | 22.755 |
| w11 | 31 | -0.038021 | 33.767 |
| w12 | 8 | -0.207603 | -7.958 |
| w14 | 0 | None | 0.0 |
| w15 | 34 | -0.121301 | -15.116 |
| w16 | 23 | -0.078502 | -5.912 |
| w17 | 34 | -0.007103 | 25.421 |
| w18 | 18 | -0.007056 | -6.838 |
| w19 | 6 | -0.154303 | -27.627 |
| w20 | 29 | -0.090549 | -7.499 |
| w21 | 35 | -0.014759 | 0.154 |
| w22 | 30 | 0.042215 | 20.588 |
| w23 | 16 | 0.085696 | 24.094 |
| w24 | 51 | -0.226712 | -7.855 |

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
| w3 | 8 | -0.101585 | -5.808 |
| w4 | 20 | -0.039072 | 0.974 |
| w5 | 10 | -0.074818 | -10.594 |
| w6 | 21 | -0.061707 | 1.481 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.127393 | 37.707 |
| w11 | 27 | -0.023889 | 57.29 |
| w12 | 17 | -0.162918 | -10.848 |
| w14 | 5 | -0.131818 | -6.885 |
| w15 | 19 | -0.076748 | -11.274 |
| w16 | 14 | -0.045333 | -4.196 |
| w17 | 24 | 0.188622 | 121.462 |
| w18 | 9 | -0.028347 | 3.412 |
| w19 | 22 | -0.090891 | -14.616 |
| w20 | 16 | -0.111114 | -12.531 |
| w21 | 18 | 0.279501 | 241.171 |
| w22 | 17 | -0.06394 | -8.513 |
| w23 | 23 | 0.00042 | 9.947 |
| w24 | 6 | -0.109849 | -7.311 |

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
| w1 | 12 | -0.007506 | -1.647 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.122873 | -11.477 |
| w7 | 1 | -0.211954 | -1.626 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 40 | -0.071489 | 16.623 |
| w11 | 34 | -0.158989 | 23.174 |
| w12 | 22 | -0.108958 | -15.366 |
| w13 | 16 | -0.133856 | -9.764 |
| w14 | 0 | None | 0.0 |
| w15 | 28 | 0.067864 | 5.28 |
| w16 | 17 | -0.036985 | 4.308 |
| w17 | 28 | -0.058525 | -9.645 |
| w18 | 13 | -0.149884 | -23.866 |
| w19 | 14 | 0.020828 | -0.716 |
| w20 | 19 | -0.03699 | 5.48 |
| w21 | 36 | -0.051505 | 14.152 |
| w22 | 2 | -0.17668 | -5.027 |
| w23 | 29 | -0.131735 | -11.866 |
| w24 | 29 | 0.153302 | 267.351 |

