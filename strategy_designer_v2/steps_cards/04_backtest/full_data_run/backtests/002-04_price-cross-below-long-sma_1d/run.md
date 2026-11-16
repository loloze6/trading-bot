# Backtest of 002-04_price-cross-below-long-sma_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.24828 | -16.032 |
| w2 | 21 | -0.098333 | 55.572 |
| w3 | 9 | -0.149124 | -0.687 |
| w4 | 3 | -0.066684 | -8.872 |
| w5 | 2 | -0.086924 | -1.523 |
| w6 | 5 | 0.005089 | -5.372 |
| w7 | 11 | -0.176882 | -9.352 |
| w8 | 11 | 0.065922 | -16.97 |
| w9 | 6 | -0.100323 | -4.083 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.157944 | -4.203 |
| w13 | 2 | -0.14682 | -3.412 |
| w14 | 24 | -0.038454 | 46.689 |
| w15 | 0 | None | 0.0 |
| w16 | 20 | -0.146863 | -23.507 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.202108 | -5.986 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.214973 | -6.065 |
| w21 | 6 | -0.054528 | -5.011 |
| w22 | 5 | -0.224159 | -3.688 |
| w23 | 0 | None | 0.0 |
| w24 | 19 | -0.019707 | 6.606 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.232511 | -6.981 |
| w2 | 18 | -0.055871 | 30.067 |
| w3 | 17 | -0.157095 | -6.763 |
| w4 | 2 | -0.097063 | -5.973 |
| w5 | 3 | -0.028606 | 0.189 |
| w6 | 12 | 0.022406 | -14.928 |
| w7 | 9 | -0.004368 | 21.717 |
| w8 | 4 | -0.001844 | -1.647 |
| w9 | 13 | -0.058871 | -1.344 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.079821 | -5.904 |
| w14 | 15 | -0.048219 | 41.636 |
| w15 | 1 | 0.02465 | 0.08 |
| w16 | 19 | -0.19743 | -35.794 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.077287 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.029367 | 1.033 |
| w21 | 14 | -0.037897 | -18.019 |
| w22 | 16 | -0.076756 | 13.38 |
| w23 | 13 | -0.182091 | -23.709 |
| w24 | 5 | -0.103453 | -1.02 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.169461 | 6.675 |
| w2 | 14 | -0.021124 | 33.449 |
| w3 | 7 | -0.028897 | -7.458 |
| w4 | 0 | -0.25146 | 0.0 |
| w5 | 10 | 0.022297 | 6.214 |
| w6 | 27 | -0.103733 | -27.196 |
| w7 | 8 | -0.064922 | 17.854 |
| w8 | 5 | -0.0276 | -11.007 |
| w9 | 8 | -0.07037 | 9.704 |
| w10 | 12 | -0.072868 | -10.969 |
| w11 | 0 | None | 0.0 |
| w12 | 16 | -0.088711 | -5.003 |
| w13 | 1 | -0.112517 | -1.845 |
| w14 | 11 | -0.169221 | 31.052 |
| w15 | 2 | 0.06469 | 0.835 |
| w16 | 15 | -0.205957 | -27.452 |
| w17 | 2 | -0.086076 | -1.384 |
| w18 | 4 | -0.1563 | -3.745 |
| w19 | 8 | -0.049379 | -6.441 |
| w20 | 35 | -0.109991 | -10.336 |
| w21 | 17 | 0.003696 | -18.795 |
| w22 | 7 | -0.065486 | -3.098 |
| w23 | 13 | -0.063851 | -9.755 |
| w24 | 28 | -0.09606 | -10.696 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.069237 | -19.337 |
| w2 | 33 | -0.1468 | -16.208 |
| w3 | 20 | -0.178801 | -14.46 |
| w4 | 6 | -0.198295 | -5.587 |
| w5 | 25 | -0.12241 | -18.372 |
| w6 | 20 | -0.065777 | -16.48 |
| w7 | 9 | -0.142204 | -2.346 |
| w8 | 5 | -0.038192 | -11.169 |
| w9 | 11 | -0.089365 | 8.925 |
| w10 | 0 | -0.281837 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.119126 | -11.409 |
| w14 | 14 | -0.113883 | 26.048 |
| w15 | 1 | 0.023371 | -0.142 |
| w16 | 18 | -0.195393 | -31.822 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.111258 | -3.958 |
| w19 | 46 | -0.210988 | -25.658 |
| w20 | 6 | -0.102271 | -13.225 |
| w21 | 11 | -0.158947 | -8.19 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.165506 | -5.342 |
| w24 | 1 | -0.067019 | -1.43 |

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
| w1 | 37 | -0.176212 | -9.159 |
| w2 | 14 | -0.001147 | 46.184 |
| w3 | 11 | -0.21896 | -20.835 |
| w4 | 13 | -0.224266 | -23.144 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.096389 | -5.475 |
| w8 | 19 | -0.34521 | -12.546 |
| w9 | 30 | -0.117673 | -1.046 |
| w10 | 12 | -0.033951 | -9.55 |
| w11 | 4 | -0.090047 | -7.618 |
| w12 | 12 | -0.105496 | -4.719 |
| w14 | 21 | -0.163559 | -26.564 |
| w15 | 23 | -0.04341 | -9.869 |
| w16 | 25 | -0.173913 | -34.164 |
| w17 | 3 | -0.025757 | -0.971 |
| w18 | 4 | -0.108898 | -4.592 |
| w19 | 23 | -0.093261 | -10.459 |
| w20 | 31 | -0.06742 | -19.657 |
| w21 | 9 | 0.044477 | -6.444 |
| w22 | 0 | -0.228857 | 0.0 |
| w23 | 1 | -0.055868 | -2.701 |
| w24 | 27 | -0.073701 | -1.599 |

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
| w1 | 30 | -0.117727 | -26.411 |
| w2 | 28 | -0.139989 | 11.512 |
| w3 | 12 | -0.164772 | 10.091 |
| w4 | 15 | -0.243506 | -8.104 |
| w5 | 26 | -0.208244 | 2.898 |
| w6 | 16 | -0.092321 | -19.136 |
| w7 | 17 | -0.122515 | 5.214 |
| w8 | 8 | -0.020467 | -13.547 |
| w9 | 13 | -0.166014 | 18.998 |
| w10 | 0 | -0.083271 | 0.0 |
| w11 | 3 | -0.034673 | -15.677 |
| w12 | 5 | -0.045734 | -4.994 |
| w13 | 12 | -0.097786 | -8.017 |
| w14 | 12 | -0.129951 | 37.617 |
| w15 | 6 | 0.057144 | 7.126 |
| w16 | 13 | -0.18081 | -25.161 |
| w17 | 4 | -0.234262 | -5.774 |
| w18 | 8 | -0.15093 | -9.449 |
| w19 | 27 | -0.106342 | -17.223 |
| w20 | 20 | -0.037794 | -21.753 |
| w21 | 3 | -0.033787 | -1.507 |
| w22 | 19 | -0.247881 | -10.482 |
| w23 | 18 | -0.221088 | -14.187 |
| w24 | 0 | None | 0.0 |

