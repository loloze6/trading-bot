# Backtest of 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d

- Plan: `../../../03_test_plan/plans/002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.06514 | -1.203 |
| w2 | 14 | -0.021938 | 79.298 |
| w3 | 10 | -0.025354 | 10.021 |
| w4 | 2 | -0.092573 | -10.711 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 6 | -0.121372 | -9.151 |
| w8 | 6 | -0.036048 | -28.348 |
| w9 | 0 | -0.04209 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.154454 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 15 | -0.02034 | 43.999 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | -0.07135 | -8.183 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | -0.038529 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.019605 | 2.677 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.159595 | -2.259 |
| w2 | 18 | -0.115531 | 16.723 |
| w3 | 12 | -0.057641 | 3.404 |
| w4 | 2 | -0.090002 | -2.383 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.134596 | -7.097 |
| w7 | 7 | 0.062651 | 23.408 |
| w8 | 6 | 0.007141 | -5.18 |
| w9 | 6 | 0.036408 | 6.022 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 15 | -0.050206 | 39.656 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | -0.107854 | -35.508 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | -0.020037 | -9.079 |
| w22 | 14 | -0.096125 | 9.386 |
| w23 | 17 | -0.002687 | -27.073 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.081367 | 4.145 |
| w2 | 11 | 0.00404 | 46.058 |
| w3 | 5 | -0.062947 | -19.955 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.01193 | 0.408 |
| w6 | 12 | -0.252274 | -22.734 |
| w7 | 5 | -0.044569 | 7.576 |
| w8 | 6 | -0.021955 | -18.014 |
| w9 | 6 | -0.017868 | 6.436 |
| w10 | 4 | 0.079813 | -3.159 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | 0.005224 | 2.09 |
| w13 | 0 | None | 0.0 |
| w14 | 15 | -0.05002 | 38.244 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | -0.146658 | -37.672 |
| w17 | 10 | -0.018903 | -11.052 |
| w18 | 0 | -0.100467 | 0.0 |
| w19 | 7 | 0.012965 | -2.891 |
| w20 | 1 | -0.123159 | -0.684 |
| w21 | 14 | 0.012792 | -29.563 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.069228 | -8.974 |
| w24 | 4 | 0.006738 | 2.859 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.177382 | -16.673 |
| w2 | 19 | -0.240769 | -25.329 |
| w3 | 17 | -0.022967 | -1.801 |
| w4 | 4 | -0.168158 | -1.596 |
| w5 | 6 | 0.056596 | 6.895 |
| w6 | 10 | -0.019688 | -9.369 |
| w7 | 5 | -0.08339 | 1.398 |
| w8 | 7 | -0.164194 | -21.985 |
| w9 | 7 | 0.036596 | 14.041 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.037877 | 7.483 |
| w13 | 0 | None | 0.0 |
| w14 | 15 | 0.080018 | 55.604 |
| w15 | 0 | None | 0.0 |
| w16 | 15 | -0.163816 | -43.438 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 24 | -0.122225 | -14.3 |
| w20 | 2 | -0.065363 | -21.208 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.042888 | 13.286 |
| w2 | 14 | -0.039948 | 51.668 |
| w3 | 12 | -0.20866 | -37.486 |
| w4 | 0 | -0.006871 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 3 | 0.029477 | 11.268 |
| w8 | 8 | 0.057889 | 5.634 |
| w9 | 12 | 0.007883 | 20.75 |
| w10 | 8 | 0.141226 | 1.306 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.035343 | -0.963 |
| w14 | 12 | -0.169801 | -25.182 |
| w15 | 4 | -0.16072 | -21.076 |
| w16 | 12 | -0.11622 | -38.861 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.090627 | -10.077 |
| w20 | 14 | -0.069817 | -22.494 |
| w21 | 7 | 0.106423 | -2.126 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | -0.080912 | 0.0 |
| w24 | 2 | 0.025469 | 2.664 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=275. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.333217 | -16.08 |
| w2 | 15 | -0.071824 | 11.487 |
| w3 | 12 | 0.007151 | 34.768 |
| w4 | 7 | -0.079193 | -3.455 |
| w5 | 6 | -0.010384 | 16.525 |
| w6 | 9 | -0.129795 | -26.154 |
| w7 | 11 | -0.045955 | 0.724 |
| w8 | 8 | -0.027216 | -13.772 |
| w9 | 11 | -0.007087 | 15.239 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.150401 | -3.564 |
| w13 | 0 | -0.141549 | 0.0 |
| w14 | 17 | 0.022068 | 51.543 |
| w15 | 1 | -0.080574 | -5.648 |
| w16 | 11 | -0.252643 | -57.704 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 9 | -0.127512 | -13.078 |
| w20 | 10 | -0.098741 | -28.643 |
| w21 | 1 | -0.030017 | -0.757 |
| w22 | 1 | -0.097085 | -1.722 |
| w23 | 10 | -0.123109 | -15.98 |
| w24 | 0 | None | 0.0 |

