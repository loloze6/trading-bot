# Backtest of N1-09_below-falling-long-average_1d

- Plan: `../../../../03_test_plan/overnight_run/plans_newcomp/N1-09_below-falling-long-average_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.113834 | -19.466 |
| w2 | 45 | -0.032177 | 114.409 |
| w3 | 23 | 0.00207 | 1.79 |
| w4 | 3 | -0.041148 | -9.615 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | -0.100567 | -14.613 |
| w8 | 19 | -0.073871 | -54.288 |
| w9 | 0 | -0.040235 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.206315 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 31 | -0.036407 | 19.428 |
| w15 | 0 | None | 0.0 |
| w16 | 15 | -0.04531 | -35.095 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | -0.077966 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.017375 | 0.269 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.184867 | 0.0 |
| w2 | 51 | -0.140103 | -36.461 |
| w3 | 37 | -0.021741 | -12.916 |
| w4 | 0 | -0.056821 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.159043 | 0.0 |
| w7 | 17 | 0.057552 | 50.633 |
| w8 | 26 | 0.036793 | -40.212 |
| w9 | 12 | 0.019141 | 5.912 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 57 | 0.05968 | 35.627 |
| w15 | 0 | None | 0.0 |
| w16 | 17 | -0.084487 | -68.58 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 6.9e-05 | -6.151 |
| w22 | 29 | -0.102575 | -12.755 |
| w23 | 22 | -0.035581 | -61.949 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.046249 | -2.464 |
| w2 | 58 | -0.009763 | 19.895 |
| w3 | 19 | -0.069326 | -49.503 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.026228 | 0.491 |
| w6 | 18 | -0.176977 | -24.205 |
| w7 | 8 | -0.035486 | 9.97 |
| w8 | 11 | -0.001781 | -42.437 |
| w9 | 7 | -0.031516 | -0.947 |
| w10 | 2 | 0.02995 | 0.127 |
| w11 | 0 | None | 0.0 |
| w12 | 12 | 0.02962 | 8.372 |
| w13 | 0 | None | 0.0 |
| w14 | 58 | -0.024801 | 47.15 |
| w15 | 0 | None | 0.0 |
| w16 | 29 | -0.148321 | -79.665 |
| w17 | 13 | -0.015877 | -26.11 |
| w18 | 0 | -0.081623 | 0.0 |
| w19 | 9 | 0.00996 | -6.387 |
| w20 | 0 | -0.053925 | 0.0 |
| w21 | 15 | 0.013662 | -35.205 |
| w22 | 0 | None | 0.0 |
| w23 | 8 | -0.067174 | -11.665 |
| w24 | 8 | 0.021755 | 10.054 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.189046 | -76.016 |
| w2 | 47 | -0.211927 | -75.683 |
| w3 | 26 | -0.030252 | -23.403 |
| w4 | 0 | -0.161171 | 0.0 |
| w5 | 8 | 0.032588 | 3.868 |
| w6 | 8 | -0.012142 | -9.167 |
| w7 | 13 | -0.069182 | -13.04 |
| w8 | 14 | -0.118406 | -40.728 |
| w9 | 13 | 0.047258 | 22.599 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | 0.091061 | 30.655 |
| w13 | 0 | None | 0.0 |
| w14 | 53 | 0.067924 | 123.97 |
| w15 | 0 | None | 0.0 |
| w16 | 34 | -0.173904 | -90.035 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 29 | -0.096821 | -39.027 |
| w20 | 6 | -0.06528 | -32.261 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.04239 | 29.289 |
| w2 | 44 | -0.04242 | 82.446 |
| w3 | 22 | -0.208924 | -75.537 |
| w4 | 0 | -0.004471 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 12 | 0.06629 | 40.145 |
| w8 | 11 | 0.006967 | 2.332 |
| w9 | 20 | 0.000972 | 15.115 |
| w10 | 11 | 0.091809 | -0.419 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.00207 | -3.669 |
| w14 | 22 | -0.241178 | -91.922 |
| w15 | 3 | -0.156227 | -46.057 |
| w16 | 28 | -0.145733 | -76.71 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | -0.061175 | -8.646 |
| w20 | 21 | -0.050139 | -34.251 |
| w21 | 12 | 0.096747 | -4.264 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | -0.093149 | 0.0 |
| w24 | 1 | 0.010282 | 0.078 |

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
| w1 | 3 | -0.347832 | -29.95 |
| w2 | 53 | -0.040233 | 4.161 |
| w3 | 40 | -0.046937 | 20.324 |
| w4 | 11 | -0.108005 | -17.295 |
| w5 | 13 | 0.011935 | 23.613 |
| w6 | 12 | -0.102842 | -29.963 |
| w7 | 36 | -0.043847 | -28.246 |
| w8 | 23 | -0.007096 | -16.987 |
| w9 | 22 | -0.010751 | 19.582 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.156529 | 0.0 |
| w13 | 0 | -0.073713 | 0.0 |
| w14 | 61 | 0.096554 | 176.53 |
| w15 | 1 | -0.087404 | -6.992 |
| w16 | 14 | -0.24646 | -86.145 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | -0.163451 | -36.497 |
| w20 | 19 | -0.077866 | -49.581 |
| w21 | 0 | -0.059848 | 0.0 |
| w22 | 0 | -0.09562 | 0.0 |
| w23 | 12 | -0.128255 | -43.081 |
| w24 | 0 | None | 0.0 |

