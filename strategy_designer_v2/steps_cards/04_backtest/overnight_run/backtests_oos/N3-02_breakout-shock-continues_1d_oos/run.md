# Backtest of N3-02_breakout-shock-continues_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N3-02_breakout-shock-continues_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.099007 | 10.399 |
| w2 | 9 | -0.071278 | -30.086 |
| w3 | 2 | 0.033103 | -2.526 |
| w4 | 22 | -0.087737 | -17.141 |
| w5 | 3 | -0.167728 | -19.497 |
| w6 | 17 | 0.1606 | 90.73 |
| w7 | 9 | 0.039012 | -2.146 |
| w8 | 8 | -0.057014 | -12.949 |
| w9 | 16 | 0.187774 | 144.155 |
| w10 | 4 | -0.171211 | -48.091 |
| w11 | 15 | 0.144676 | 45.451 |
| w12 | 3 | -0.049834 | -10.349 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 8 | 0.016923 | -2.66 |
| w3 | 7 | -0.040734 | -14.404 |
| w4 | 16 | 0.035407 | 2.573 |
| w5 | 3 | 0.092872 | 4.056 |
| w6 | 26 | -0.012227 | 24.113 |
| w7 | 11 | 0.018371 | -5.537 |
| w8 | 5 | 0.084028 | 12.621 |
| w9 | 14 | 0.014939 | -3.874 |
| w10 | 3 | -0.026116 | -6.789 |
| w11 | 11 | 0.059313 | 13.035 |
| w12 | 3 | 0.060297 | 6.047 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=24. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.151167 | -39.16 |
| w2 | 3 | -0.150804 | -27.159 |
| w3 | 7 | 0.280154 | 133.141 |
| w4 | 12 | -0.072108 | -15.719 |
| w5 | 5 | -0.058908 | -13.901 |
| w6 | 11 | -0.174779 | -30.718 |
| w7 | 13 | 0.08586 | 18.852 |
| w8 | 5 | 0.073051 | 11.635 |
| w9 | 17 | 0.316116 | 331.078 |
| w10 | 2 | -0.049612 | -10.185 |
| w11 | 11 | 0.158179 | 52.964 |
| w12 | 3 | 0.0831 | 9.972 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.001939 | -8.933 |
| w2 | 12 | -0.03337 | -20.605 |
| w3 | 9 | -0.09862 | -30.525 |
| w4 | 16 | -0.080085 | -17.864 |
| w5 | 6 | -0.098363 | -20.036 |
| w6 | 18 | 0.036097 | 40.473 |
| w7 | 9 | -0.058642 | -15.702 |
| w8 | 8 | -0.02923 | -12.033 |
| w9 | 21 | -0.173753 | -51.971 |
| w10 | 4 | -0.021988 | -9.449 |
| w11 | 23 | 0.060517 | 34.093 |
| w12 | 1 | -0.046254 | -5.361 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.043977 | 2.036 |
| w2 | 5 | 0.042164 | 0.714 |
| w3 | 3 | -0.089434 | -29.875 |
| w4 | 11 | 0.09118 | 30.471 |
| w5 | 10 | 0.04876 | 6.006 |
| w6 | 24 | 0.203169 | 310.962 |
| w7 | 16 | 0.069122 | 20.457 |
| w8 | 10 | -0.007885 | -3.071 |
| w9 | 18 | 0.014494 | 6.891 |
| w10 | 5 | 0.155963 | 29.247 |
| w11 | 10 | 0.017721 | 5.51 |
| w12 | 7 | -0.009218 | -5.919 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.065565 | 6.233 |
| w2 | 7 | -0.148132 | -41.078 |
| w3 | 4 | -0.1129 | -9.7 |
| w4 | 13 | -0.166733 | -26.269 |
| w5 | 16 | -0.006271 | -3.676 |
| w6 | 25 | -0.045818 | -3.222 |
| w7 | 19 | 0.017031 | 0.396 |
| w8 | 19 | 0.091787 | 16.169 |
| w9 | 16 | 0.168588 | 41.44 |
| w10 | 4 | 0.004769 | -0.694 |
| w11 | 21 | -0.129867 | -14.508 |
| w12 | 1 | -0.071845 | -2.977 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.067872 | -14.677 |
| w2 | 8 | -0.009415 | -9.698 |
| w3 | 9 | -0.040273 | -10.728 |
| w4 | 16 | -0.101901 | -24.487 |
| w5 | 9 | -0.078182 | -18.152 |
| w6 | 15 | -0.115296 | -23.259 |
| w7 | 11 | 0.091806 | 36.386 |
| w8 | 7 | 0.039834 | 6.765 |
| w9 | 14 | -0.031622 | -1.099 |
| w10 | 1 | -0.062394 | -4.919 |
| w11 | 14 | -0.055704 | -14.907 |
| w12 | 2 | -0.143891 | -28.703 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.022852 | -10.032 |
| w2 | 10 | -0.094314 | -39.203 |
| w3 | 6 | 0.013378 | -6.205 |
| w4 | 12 | 0.088517 | 25.424 |
| w5 | 8 | -0.066704 | -18.466 |
| w6 | 17 | -0.063103 | -9.375 |
| w7 | 9 | 0.02734 | 0.976 |
| w8 | 13 | 0.031969 | 9.051 |
| w9 | 17 | 0.016195 | 22.458 |
| w10 | 3 | -0.002285 | -5.668 |
| w11 | 19 | 0.007968 | 11.942 |
| w12 | 1 | -0.043876 | -5.57 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.079373 | -17.813 |
| w2 | 4 | 0.072192 | 14.063 |
| w3 | 11 | -0.034936 | -15.004 |
| w4 | 26 | 0.012002 | 72.991 |
| w5 | 9 | -0.004215 | -2.833 |
| w6 | 28 | 0.049535 | 132.45 |
| w7 | 5 | -0.042171 | -17.387 |
| w8 | 10 | -0.052006 | -21.844 |
| w9 | 13 | 0.00366 | 2.309 |
| w10 | 5 | -0.107496 | -26.693 |
| w11 | 16 | 0.016017 | 0.601 |
| w12 | 0 | -0.088131 | 0.0 |

