# Backtest of N4-03_breakouts-pay-in-uptrends_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N4-03_breakouts-pay-in-uptrends_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.09733 | -4.761 |
| w2 | 23 | 0.056625 | 20.249 |
| w3 | 6 | 0.091015 | 10.502 |
| w4 | 29 | -0.140339 | -24.79 |
| w5 | 13 | -0.158177 | -12.531 |
| w6 | 31 | 0.068428 | 14.852 |
| w7 | 20 | 0.096567 | 15.026 |
| w8 | 19 | 0.02569 | 5.934 |
| w9 | 26 | 0.217616 | 85.501 |
| w10 | 13 | -0.14364 | -39.959 |
| w11 | 24 | -0.155354 | -32.126 |
| w12 | 8 | -0.015371 | -5.881 |

- AVAXUSD: 10 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 11 | 0.007324 | 6.661 |
| w4 | 28 | -0.136988 | -21.697 |
| w5 | 7 | 0.006661 | 4.553 |
| w6 | 20 | 0.1891 | 49.126 |
| w7 | 25 | 0.006794 | -9.015 |
| w8 | 16 | -0.144641 | -26.483 |
| w9 | 37 | 0.122193 | 49.381 |
| w10 | 12 | -0.07095 | -9.59 |
| w11 | 32 | -0.174893 | -43.039 |
| w12 | 13 | 0.149621 | 19.814 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 131 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.088346 | 12.471 |
| w2 | 19 | -0.003073 | 2.882 |
| w3 | 17 | 0.090441 | 8.521 |
| w4 | 31 | -0.145589 | -22.168 |
| w5 | 17 | -0.118149 | -20.798 |
| w6 | 38 | -0.119397 | -19.123 |
| w7 | 24 | 0.132758 | 43.086 |
| w8 | 25 | -0.088842 | -15.68 |
| w9 | 37 | 0.157732 | 94.599 |
| w10 | 10 | -0.050263 | -10.848 |
| w11 | 27 | -0.161528 | -45.921 |
| w12 | 8 | 0.106684 | 7.98 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.050004 | -9.546 |
| w2 | 19 | -0.058168 | -11.259 |
| w3 | 21 | -0.122438 | -29.633 |
| w4 | 34 | -0.149975 | -30.146 |
| w5 | 14 | -0.063438 | -10.715 |
| w6 | 33 | -0.008464 | 19.173 |
| w7 | 27 | -0.037382 | -19.992 |
| w8 | 23 | 0.009738 | -4.236 |
| w9 | 38 | 0.033873 | 2.053 |
| w10 | 15 | -0.028648 | -10.323 |
| w11 | 37 | -0.031801 | -23.839 |
| w12 | 9 | 0.014952 | 3.893 |

- SOLUSD: 10 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 15 | 0.049731 | 22.042 |
| w4 | 27 | -0.045262 | -32.356 |
| w5 | 18 | -0.109582 | -15.358 |
| w6 | 36 | 0.141243 | 129.622 |
| w7 | 24 | 0.11885 | 47.473 |
| w8 | 28 | 0.002133 | -4.713 |
| w9 | 25 | 0.038057 | 18.244 |
| w10 | 19 | 0.022393 | -3.552 |
| w11 | 28 | -0.032609 | -11.365 |
| w12 | 11 | 0.090822 | 2.14 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 198 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
  File "/usr/local/lib/python3.13/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Invalid control character at: line 243 column 51 (char 8219)
```

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.102577 | -14.699 |
| w2 | 42 | -0.234501 | -63.091 |
| w3 | 25 | 0.166737 | 15.205 |
| w4 | 36 | -0.26567 | -32.018 |
| w5 | 39 | 0.010359 | 0.875 |
| w6 | 29 | -0.102312 | 0.604 |
| w7 | 25 | 0.054996 | 11.543 |
| w8 | 38 | 0.131246 | 17.305 |
| w9 | 38 | 0.08049 | 50.931 |
| w10 | 34 | -0.27266 | -35.393 |
| w11 | 40 | -0.063694 | 3.174 |
| w12 | 15 | 0.010209 | -1.332 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.063173 | -0.007 |
| w2 | 33 | -0.040226 | -17.581 |
| w3 | 24 | -0.01361 | -8.688 |
| w4 | 28 | -0.214454 | -43.28 |
| w5 | 22 | -0.001133 | -6.758 |
| w6 | 39 | -0.083998 | -15.187 |
| w7 | 20 | 0.1112 | 34.163 |
| w8 | 18 | -0.023041 | -4.813 |
| w9 | 48 | -0.01522 | -9.104 |
| w10 | 7 | -0.062114 | -0.338 |
| w11 | 29 | -0.064429 | -48.621 |
| w12 | 9 | -0.292658 | -36.753 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.111529 | -17.427 |
| w2 | 32 | 0.019439 | 5.348 |
| w3 | 15 | -0.028703 | -7.45 |
| w4 | 34 | -0.215639 | -32.366 |
| w5 | 15 | 0.011355 | -5.153 |
| w6 | 32 | -0.016352 | 10.44 |
| w7 | 23 | 0.018301 | 0.568 |
| w8 | 31 | 0.00418 | 0.832 |
| w9 | 37 | 0.026739 | 90.598 |
| w10 | 7 | -0.085037 | -15.565 |
| w11 | 41 | -0.138883 | -23.833 |
| w12 | 13 | 0.078769 | 14.011 |

- INJUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 16 | -0.024559 | -5.27 |
| w3 | 28 | -0.025031 | -29.332 |
| w4 | 38 | 0.073543 | 108.989 |
| w5 | 21 | 0.045937 | 6.883 |
| w6 | 38 | 0.162311 | 199.881 |
| w7 | 21 | -0.069106 | -25.539 |
| w8 | 22 | 0.014049 | 2.006 |
| w9 | 31 | -0.029064 | -12.814 |
| w10 | 7 | -0.040172 | -5.506 |
| w11 | 29 | -0.044709 | -26.143 |
| w12 | 7 | -0.035912 | -13.613 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 144 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

