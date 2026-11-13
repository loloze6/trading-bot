# Backtest of N3-04_dip-in-uptrend_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N3-04_dip-in-uptrend_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.026818 | -5.823 |
| w2 | 2 | -0.027464 | -5.46 |
| w3 | 3 | 0.095061 | 6.636 |
| w4 | 11 | 0.013018 | 3.489 |
| w5 | 1 | 0.000644 | -0.125 |
| w6 | 21 | 0.127234 | 46.865 |
| w7 | 9 | 0.082696 | 8.046 |
| w8 | 1 | -0.128358 | -2.756 |
| w9 | 8 | 0.009612 | 12.669 |
| w10 | 5 | -0.045415 | -11.843 |
| w11 | 24 | -0.038752 | -12.152 |
| w12 | 2 | -0.030691 | -5.677 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 4 | -0.058405 | -11.555 |
| w3 | 0 | None | 0.0 |
| w4 | 12 | 0.011916 | 5.443 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.004173 | 12.932 |
| w7 | 13 | 0.180199 | 38.228 |
| w8 | 0 | -0.071904 | 0.0 |
| w9 | 26 | -0.114457 | -25.87 |
| w10 | 1 | -0.152855 | -12.197 |
| w11 | 20 | -0.096544 | -23.158 |
| w12 | 9 | -0.035965 | -11.466 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.031562 | 0.465 |
| w2 | 2 | -0.007624 | -12.306 |
| w3 | 18 | -0.0146 | -15.231 |
| w4 | 2 | 0.047385 | 0.665 |
| w5 | 9 | -0.024699 | -5.393 |
| w6 | 17 | 0.103276 | 26.55 |
| w7 | 13 | -0.031728 | -25.461 |
| w8 | 1 | -0.096527 | -1.115 |
| w9 | 20 | -0.037156 | 4.642 |
| w10 | 3 | -0.016157 | -4.809 |
| w11 | 19 | -0.068741 | -18.451 |
| w12 | 4 | -0.073383 | -9.998 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.040254 | -2.408 |
| w2 | 5 | -0.064551 | -12.822 |
| w3 | 7 | -3.8e-05 | -4.364 |
| w4 | 21 | -0.07198 | -13.433 |
| w5 | 13 | -0.049833 | -11.007 |
| w6 | 23 | -0.014997 | 8.416 |
| w7 | 15 | -0.118028 | -19.289 |
| w8 | 1 | -0.062027 | -0.713 |
| w9 | 21 | -0.018615 | 0.009 |
| w10 | 4 | 0.073559 | 8.309 |
| w11 | 20 | 0.081866 | 30.925 |
| w12 | 2 | -0.014748 | -2.02 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.089233 | -11.528 |
| w2 | 5 | -0.056707 | -7.372 |
| w3 | 0 | -0.040565 | 0.0 |
| w4 | 15 | 0.024031 | 12.3 |
| w5 | 11 | 0.052018 | 4.727 |
| w6 | 24 | 0.044434 | 46.59 |
| w7 | 17 | 0.042565 | 5.522 |
| w8 | 10 | -0.067333 | -10.822 |
| w9 | 17 | 0.089825 | 18.604 |
| w10 | 3 | -0.12564 | -10.421 |
| w11 | 23 | -0.075574 | -18.891 |
| w12 | 9 | -0.063355 | -11.323 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.10818 | -12.132 |
| w2 | 15 | 0.343948 | 94.305 |
| w3 | 3 | -0.189763 | -4.105 |
| w4 | 17 | 0.088811 | 13.294 |
| w5 | 22 | 0.015429 | -0.874 |
| w6 | 26 | -0.055859 | -5.402 |
| w7 | 16 | -0.007105 | -2.594 |
| w8 | 21 | -0.058165 | -6.324 |
| w9 | 34 | -0.069733 | -25.575 |
| w10 | 8 | 0.075194 | 6.586 |
| w11 | 29 | -0.034549 | -0.637 |
| w12 | 4 | 0.103503 | 3.137 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.074041 | 3.746 |
| w2 | 16 | 0.11961 | 25.27 |
| w3 | 4 | 0.032398 | 1.795 |
| w4 | 10 | -0.04415 | -12.059 |
| w5 | 11 | -0.074715 | -16.606 |
| w6 | 19 | 0.228862 | 64.036 |
| w7 | 19 | -0.067191 | -27.017 |
| w8 | 0 | -0.048287 | 0.0 |
| w9 | 26 | -0.004169 | 11.131 |
| w10 | 3 | -0.070626 | -6.965 |
| w11 | 28 | -0.22164 | -60.505 |
| w12 | 3 | -0.025258 | -1.802 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.087794 | 11.48 |
| w2 | 6 | 0.164021 | 9.472 |
| w3 | 1 | 0.069058 | 2.099 |
| w4 | 11 | 0.047667 | 8.915 |
| w5 | 10 | -0.019918 | -7.569 |
| w6 | 27 | -0.122813 | -16.65 |
| w7 | 11 | 0.18663 | 42.014 |
| w8 | 14 | -0.172409 | -32.501 |
| w9 | 38 | 0.056267 | 54.71 |
| w10 | 2 | -0.176624 | -28.96 |
| w11 | 28 | -0.077809 | -14.878 |
| w12 | 2 | -0.016908 | -9.872 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.018334 | -0.387 |
| w2 | 9 | -0.015374 | -13.409 |
| w3 | 7 | 0.05708 | 9.429 |
| w4 | 27 | 0.0307 | 65.371 |
| w5 | 8 | 0.065442 | 11.719 |
| w6 | 19 | 0.000776 | 27.042 |
| w7 | 13 | 0.018429 | -6.317 |
| w8 | 4 | -0.160668 | -32.473 |
| w9 | 19 | 0.097661 | 31.957 |
| w10 | 0 | None | 0.0 |
| w11 | 19 | -0.169541 | -47.055 |
| w12 | 1 | -0.050518 | -2.042 |

