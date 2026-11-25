# Backtest of 040-02_agitated-fall-vs-swing-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/040-02_agitated-fall-vs-swing-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.048595 | -6.331 |
| w2 | 26 | 0.079647 | -0.93 |
| w3 | 22 | 0.23135 | 17.042 |
| w4 | 9 | 0.102907 | 6.126 |
| w5 | 0 | None | 0.0 |
| w6 | 20 | 0.258567 | 40.29 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | 0.036591 | 2.607 |
| w9 | 15 | -0.037815 | -5.849 |
| w10 | 16 | 0.025357 | 7.807 |
| w11 | 35 | 0.051572 | 13.274 |
| w12 | 13 | 0.050703 | 3.241 |
| w13 | 38 | 0.008034 | -0.89 |
| w14 | 21 | 0.198737 | 20.149 |
| w15 | 42 | -0.081183 | -3.654 |
| w16 | 17 | 0.239967 | 18.512 |
| w17 | 19 | 0.031109 | 10.446 |
| w18 | 41 | 0.206714 | 28.965 |
| w19 | 38 | 0.145741 | 26.192 |
| w20 | 40 | 0.061095 | 1.392 |
| w21 | 18 | 0.034714 | 6.707 |
| w22 | 25 | 0.193686 | 18.837 |
| w23 | 2 | -0.036945 | -0.459 |
| w24 | 33 | 0.004491 | -8.726 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.143697 | -11.693 |
| w2 | 47 | 0.041701 | -8.178 |
| w3 | 23 | 0.302491 | 28.31 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 20 | 0.155592 | 18.438 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.160164 | 9.445 |
| w9 | 12 | 0.046687 | 1.68 |
| w10 | 14 | 0.064306 | 8.009 |
| w11 | 33 | 0.048575 | 20.096 |
| w12 | 9 | 0.05903 | 3.976 |
| w13 | 24 | -0.085487 | -10.131 |
| w14 | 39 | 0.192156 | 22.275 |
| w15 | 20 | 0.021719 | 2.037 |
| w16 | 32 | 0.015077 | -7.501 |
| w17 | 21 | -0.01011 | -2.184 |
| w18 | 34 | 0.0943 | 18.368 |
| w19 | 33 | -0.064469 | -9.36 |
| w20 | 39 | 0.120516 | 4.612 |
| w21 | 35 | -0.017425 | 2.041 |
| w22 | 47 | 0.086447 | -1.701 |
| w23 | 17 | 0.134469 | 20.161 |
| w24 | 19 | 0.041599 | -2.158 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 29 | 0.073297 | 2.498 |
| w3 | 17 | 0.168445 | 17.776 |
| w4 | 9 | 0.136672 | 7.885 |
| w5 | 22 | 0.029664 | -0.684 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 40 | 0.034598 | 12.567 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | 0.031978 | 2.579 |
| w11 | 42 | -0.096063 | -6.72 |
| w12 | 22 | -0.047931 | -8.323 |
| w13 | 23 | -0.0364 | -0.538 |
| w14 | 28 | 0.173478 | 14.017 |
| w15 | 26 | 0.156034 | 15.219 |
| w16 | 22 | 0.042123 | -6.92 |
| w17 | 25 | 0.008299 | 3.202 |
| w18 | 32 | 0.16919 | 17.782 |
| w19 | 33 | 0.128138 | 22.571 |
| w20 | 24 | 0.120196 | 6.151 |
| w21 | 34 | -0.058465 | -5.613 |
| w22 | 46 | -0.065478 | -11.289 |
| w23 | 11 | 0.066255 | 5.477 |
| w24 | 29 | -0.04347 | -7.752 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.062591 | -10.374 |
| w2 | 28 | 0.010277 | -5.307 |
| w3 | 9 | 0.110852 | 5.512 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | 0.050742 | 2.553 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.07722 | 3.227 |
| w9 | 2 | 0.035025 | 0.552 |
| w10 | 5 | 0.08523 | 5.086 |
| w11 | 34 | 0.033446 | 19.916 |
| w12 | 11 | -0.025489 | -5.312 |
| w14 | 29 | 0.140684 | 8.655 |
| w15 | 29 | 0.002095 | -0.685 |
| w16 | 33 | 0.051019 | -1.742 |
| w17 | 22 | -0.029766 | -4.004 |
| w18 | 31 | 0.246584 | 32.221 |
| w19 | 47 | 0.230312 | 41.011 |
| w20 | 26 | 0.152899 | 17.207 |
| w21 | 16 | 0.094377 | 10.676 |
| w22 | 24 | 0.062121 | 8.544 |
| w23 | 26 | -0.177898 | -20.054 |
| w24 | 32 | -0.102379 | -8.996 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.104497 | 1.912 |
| w2 | 0 | -0.022929 | 0.0 |
| w3 | 0 | 0.151615 | 0.0 |
| w4 | 0 | 0.09025 | 0.0 |
| w5 | 20 | -0.022014 | 1.187 |
| w6 | 15 | 0.05814 | 8.551 |
| w8 | 4 | 0.079045 | 2.293 |
| w9 | 12 | 0.079425 | 3.564 |
| w10 | 7 | 0.042422 | 3.203 |
| w11 | 40 | 0.022774 | 23.179 |
| w12 | 2 | -0.032217 | -1.602 |
| w14 | 15 | 0.112904 | 8.313 |
| w15 | 21 | 0.040631 | 2.22 |
| w16 | 40 | 0.001988 | -9.686 |
| w17 | 29 | 0.031939 | 8.277 |
| w18 | 24 | 0.145618 | 10.442 |
| w19 | 35 | -0.015059 | -5.288 |
| w20 | 20 | -0.015569 | -0.405 |
| w21 | 31 | -0.035684 | 15.918 |
| w22 | 45 | 0.04657 | 1.375 |
| w23 | 9 | 0.093409 | 6.263 |
| w24 | 12 | 0.014596 | -2.954 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.130071 | 6.886 |
| w2 | 36 | 0.125257 | 6.784 |
| w3 | 9 | 0.254718 | 14.074 |
| w4 | 6 | -0.033653 | -1.173 |
| w5 | 15 | 0.107659 | 7.613 |
| w6 | 10 | 0.100761 | 6.695 |
| w7 | 7 | -0.009249 | -1.521 |
| w8 | 8 | 0.162026 | 3.887 |
| w9 | 22 | 0.116901 | 6.679 |
| w10 | 20 | -0.033836 | 4.106 |
| w11 | 36 | 0.004738 | 15.903 |
| w12 | 27 | -0.00243 | -1.227 |
| w13 | 27 | 0.084438 | 5.626 |
| w14 | 22 | 0.153565 | 10.841 |
| w15 | 29 | 0.039567 | -1.161 |
| w16 | 43 | -0.03971 | 1.816 |
| w17 | 26 | 0.006943 | -6.516 |
| w18 | 34 | 0.249744 | 31.177 |
| w19 | 52 | 0.069981 | -1.609 |
| w20 | 39 | -0.079762 | -7.238 |
| w21 | 38 | -0.027763 | 2.684 |
| w22 | 44 | -0.088241 | -19.031 |
| w23 | 13 | -0.054315 | -4.25 |
| w24 | 38 | -0.085451 | 4.731 |

