# Backtest of 002-04_price-cross-below-long-sma_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.24828 | -31.795 |
| w2 | 49 | -0.098333 | 62.841 |
| w3 | 17 | -0.149124 | -9.52 |
| w4 | 2 | -0.066684 | -7.265 |
| w5 | 2 | -0.086924 | -1.414 |
| w6 | 5 | 0.005089 | -4.757 |
| w7 | 22 | -0.176882 | -12.611 |
| w8 | 13 | 0.065922 | -23.279 |
| w9 | 6 | -0.100323 | -4.333 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.157944 | -5.029 |
| w13 | 2 | -0.14682 | -7.857 |
| w14 | 35 | -0.038454 | 38.042 |
| w15 | 0 | None | 0.0 |
| w16 | 27 | -0.146863 | -69.461 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.202108 | -14.157 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.214973 | -7.845 |
| w21 | 6 | -0.054528 | -6.395 |
| w22 | 5 | -0.224159 | -5.459 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | -0.019707 | 5.621 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.232511 | -24.604 |
| w2 | 61 | -0.055871 | -12.052 |
| w3 | 20 | -0.157095 | -12.729 |
| w4 | 3 | -0.097063 | -6.054 |
| w5 | 4 | -0.028606 | -1.262 |
| w6 | 12 | 0.022406 | -12.813 |
| w7 | 22 | -0.004368 | 43.107 |
| w8 | 14 | -0.001844 | -16.774 |
| w9 | 24 | -0.058871 | -6.139 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.079821 | -16.117 |
| w14 | 43 | -0.048219 | 34.893 |
| w15 | 1 | 0.02465 | 0.174 |
| w16 | 22 | -0.19743 | -78.131 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.077287 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.029367 | 0.705 |
| w21 | 21 | -0.037897 | -27.66 |
| w22 | 32 | -0.076756 | -0.673 |
| w23 | 16 | -0.182091 | -48.774 |
| w24 | 8 | -0.103453 | -3.154 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 60 | -0.169461 | -13.355 |
| w2 | 47 | -0.021124 | 9.323 |
| w3 | 12 | -0.028897 | -16.384 |
| w4 | 0 | -0.25146 | 0.0 |
| w5 | 13 | 0.022297 | 11.08 |
| w6 | 39 | -0.103733 | -34.118 |
| w7 | 18 | -0.064922 | 41.367 |
| w8 | 10 | -0.0276 | -31.714 |
| w9 | 16 | -0.07037 | 15.891 |
| w10 | 12 | -0.072868 | -17.082 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | -0.088711 | -15.817 |
| w13 | 2 | -0.112517 | -5.233 |
| w14 | 35 | -0.169221 | 41.618 |
| w15 | 2 | 0.06469 | 2.24 |
| w16 | 24 | -0.205957 | -69.226 |
| w17 | 5 | -0.086076 | -10.256 |
| w18 | 7 | -0.1563 | -18.697 |
| w19 | 10 | -0.049379 | -8.711 |
| w20 | 44 | -0.109991 | -23.307 |
| w21 | 25 | 0.003696 | -25.786 |
| w22 | 7 | -0.065486 | -9.157 |
| w23 | 13 | -0.063851 | -17.862 |
| w24 | 36 | -0.09606 | -23.582 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 49 | -0.069237 | -62.072 |
| w2 | 60 | -0.1468 | -52.869 |
| w3 | 28 | -0.178801 | -26.532 |
| w4 | 6 | -0.198295 | -7.991 |
| w5 | 26 | -0.12241 | -18.436 |
| w6 | 19 | -0.065777 | -15.02 |
| w7 | 21 | -0.142204 | -7.099 |
| w8 | 14 | -0.038192 | -32.307 |
| w9 | 23 | -0.089365 | 21.411 |
| w10 | 0 | -0.281837 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 33 | -0.119126 | -32.014 |
| w14 | 37 | -0.113883 | 35.236 |
| w15 | 1 | 0.023371 | -0.367 |
| w16 | 28 | -0.195393 | -75.766 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.111258 | -9.317 |
| w19 | 64 | -0.210988 | -65.323 |
| w20 | 11 | -0.102271 | -19.94 |
| w21 | 11 | -0.158947 | -10.54 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.165506 | -7.022 |
| w24 | 1 | -0.067019 | -2.3 |

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
| w1 | 61 | -0.176212 | -36.201 |
| w2 | 46 | -0.001147 | 75.966 |
| w3 | 13 | -0.21896 | -35.979 |
| w4 | 17 | -0.224266 | -32.708 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.096389 | -5.085 |
| w8 | 22 | -0.34521 | -18.893 |
| w9 | 45 | -0.117673 | -6.746 |
| w10 | 11 | -0.033951 | -9.005 |
| w11 | 6 | -0.090047 | -39.008 |
| w12 | 13 | -0.105496 | -10.159 |
| w14 | 32 | -0.163559 | -70.857 |
| w15 | 26 | -0.04341 | -15.519 |
| w16 | 45 | -0.173913 | -73.672 |
| w17 | 3 | -0.025757 | -5.361 |
| w18 | 6 | -0.108898 | -14.626 |
| w19 | 22 | -0.093261 | -14.429 |
| w20 | 34 | -0.06742 | -31.697 |
| w21 | 9 | 0.044477 | -9.979 |
| w22 | 0 | -0.228857 | 0.0 |
| w23 | 1 | -0.055868 | -3.861 |
| w24 | 39 | -0.073701 | -4.313 |

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
| w1 | 44 | -0.117727 | -56.1 |
| w2 | 62 | -0.139989 | -17.026 |
| w3 | 29 | -0.164772 | 0.517 |
| w4 | 21 | -0.243506 | -22.387 |
| w5 | 37 | -0.208244 | -13.981 |
| w6 | 17 | -0.092321 | -20.523 |
| w7 | 45 | -0.122515 | -18.69 |
| w8 | 12 | -0.020467 | -8.087 |
| w9 | 35 | -0.166014 | 20.758 |
| w10 | 0 | -0.083271 | 0.0 |
| w11 | 3 | -0.034673 | -13.452 |
| w12 | 7 | -0.045734 | -9.659 |
| w13 | 17 | -0.097786 | -27.093 |
| w14 | 42 | -0.129951 | 65.395 |
| w15 | 9 | 0.057144 | 7.62 |
| w16 | 17 | -0.18081 | -59.013 |
| w17 | 4 | -0.234262 | -14.933 |
| w18 | 11 | -0.15093 | -29.85 |
| w19 | 38 | -0.106342 | -39.941 |
| w20 | 29 | -0.037794 | -39.029 |
| w21 | 3 | -0.033787 | -3.121 |
| w22 | 25 | -0.247881 | -29.308 |
| w23 | 20 | -0.221088 | -30.01 |
| w24 | 0 | None | 0.0 |

