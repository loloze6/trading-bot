# Backtest of N2-04_slow-and-fast-momentum_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N2-04_slow-and-fast-momentum_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.007862 | -7.093 |
| w2 | 6 | -0.024472 | -7.639 |
| w3 | 5 | -0.018883 | -5.709 |
| w4 | 26 | -0.099721 | -3.946 |
| w5 | 1 | -0.015508 | -0.388 |
| w6 | 17 | 0.122052 | 185.988 |
| w7 | 18 | -0.05022 | -21.143 |
| w8 | 3 | -0.129674 | -7.777 |
| w9 | 17 | 0.258182 | 446.67 |
| w10 | 8 | -0.179749 | -40.213 |
| w11 | 27 | -0.110005 | -27.819 |
| w12 | 7 | -0.055551 | -6.939 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 9 | -0.026016 | -16.807 |
| w3 | 1 | -0.1288 | -7.782 |
| w4 | 22 | 0.004687 | 20.864 |
| w5 | 0 | None | 0.0 |
| w6 | 24 | 0.182439 | 581.885 |
| w7 | 18 | 0.008585 | -11.769 |
| w8 | 3 | -0.014549 | -2.284 |
| w9 | 25 | -0.001174 | 25.832 |
| w10 | 2 | -0.050796 | -4.673 |
| w11 | 33 | -0.081397 | -24.797 |
| w12 | 18 | 0.080062 | 0.784 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.028427 | -11.097 |
| w2 | 7 | -0.021405 | -14.071 |
| w3 | 19 | 0.031412 | -25.113 |
| w4 | 10 | -0.067103 | -9.074 |
| w5 | 9 | -0.034251 | -8.416 |
| w6 | 29 | 0.014047 | 22.529 |
| w7 | 21 | 0.096948 | 50.426 |
| w8 | 4 | -0.062304 | -4.571 |
| w9 | 22 | 0.208603 | 598.182 |
| w10 | 2 | -0.095884 | -2.731 |
| w11 | 30 | -0.129832 | -41.629 |
| w12 | 13 | 0.014697 | -11.334 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.018516 | -1.605 |
| w2 | 15 | -0.065791 | -26.44 |
| w3 | 21 | -0.09444 | -31.948 |
| w4 | 33 | -0.214588 | -35.618 |
| w5 | 13 | -0.053621 | -16.155 |
| w6 | 26 | -0.013092 | 67.077 |
| w7 | 19 | -0.039381 | -17.521 |
| w8 | 3 | -0.058893 | -5.646 |
| w9 | 24 | 0.092336 | 129.294 |
| w10 | 5 | 0.078056 | 5.852 |
| w11 | 37 | -0.043844 | 0.392 |
| w12 | 5 | -0.142259 | -10.785 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.058762 | 2.151 |
| w2 | 5 | -0.032667 | -13.808 |
| w3 | 4 | -0.06474 | -14.47 |
| w4 | 21 | -0.031912 | 8.468 |
| w5 | 11 | 0.006934 | -2.726 |
| w6 | 30 | 0.085023 | 494.921 |
| w7 | 35 | 0.066571 | 23.165 |
| w8 | 17 | -0.129316 | -29.103 |
| w9 | 19 | 0.073854 | 67.001 |
| w10 | 7 | -0.141287 | -27.007 |
| w11 | 28 | -0.100747 | -14.277 |
| w12 | 13 | 0.066829 | 9.645 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.003352 | -2.102 |
| w2 | 33 | -0.037827 | -34.075 |
| w3 | 3 | -0.065971 | -1.622 |
| w4 | 33 | -0.042858 | -1.628 |
| w5 | 34 | -0.046541 | -3.715 |
| w6 | 36 | -0.129773 | 9.802 |
| w7 | 23 | 0.070667 | 21.095 |
| w8 | 29 | -0.018896 | 11.618 |
| w9 | 33 | 0.058686 | 10.352 |
| w10 | 18 | -0.090131 | -12.83 |
| w11 | 37 | -0.095678 | 23.54 |
| w12 | 5 | -0.130773 | -2.982 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.039105 | -0.228 |
| w2 | 16 | 0.00886 | -2.57 |
| w3 | 9 | -0.101643 | -19.157 |
| w4 | 29 | -0.065064 | -18.392 |
| w5 | 20 | -0.069871 | -24.817 |
| w6 | 22 | -0.040843 | 16.439 |
| w7 | 24 | 0.072523 | 30.92 |
| w8 | 7 | -0.14352 | -19.962 |
| w9 | 39 | -0.013718 | 64.027 |
| w10 | 4 | -0.061279 | -6.185 |
| w11 | 52 | -0.0991 | -11.404 |
| w12 | 2 | -0.066871 | -1.844 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.06769 | 0.686 |
| w2 | 8 | -0.055301 | -23.779 |
| w3 | 9 | -0.117424 | -17.907 |
| w4 | 21 | 0.011126 | 8.349 |
| w5 | 14 | -0.019964 | -10.015 |
| w6 | 30 | -0.131685 | -3.878 |
| w7 | 19 | -0.075573 | -37.83 |
| w8 | 25 | 0.057842 | 44.786 |
| w9 | 45 | -0.030727 | 87.356 |
| w10 | 2 | -0.016558 | -2.649 |
| w11 | 37 | -0.095082 | 6.585 |
| w12 | 2 | -0.121056 | -4.956 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.011872 | -12.004 |
| w2 | 9 | -0.049252 | -22.067 |
| w3 | 28 | -0.102766 | -47.416 |
| w4 | 37 | -0.021528 | 257.212 |
| w5 | 18 | -0.01663 | -7.31 |
| w6 | 22 | 0.140759 | 742.777 |
| w7 | 20 | -0.153291 | -40.414 |
| w8 | 9 | -0.083353 | -15.735 |
| w9 | 28 | -0.020209 | -11.634 |
| w10 | 0 | None | 0.0 |
| w11 | 36 | -0.093166 | -25.467 |
| w12 | 3 | 0.045173 | -0.857 |

