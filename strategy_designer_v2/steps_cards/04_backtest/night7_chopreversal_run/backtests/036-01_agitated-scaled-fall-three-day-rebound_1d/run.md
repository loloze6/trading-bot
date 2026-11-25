# Backtest of 036-01_agitated-scaled-fall-three-day-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/036-01_agitated-scaled-fall-three-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.048595 | -9.215 |
| w2 | 31 | 0.079647 | -16.883 |
| w3 | 30 | 0.23135 | 6.887 |
| w4 | 11 | 0.102907 | 6.431 |
| w5 | 0 | None | 0.0 |
| w6 | 25 | 0.258567 | 42.21 |
| w7 | 0 | None | 0.0 |
| w8 | 19 | 0.036591 | 3.373 |
| w9 | 19 | -0.037815 | 12.509 |
| w10 | 24 | 0.025357 | 8.022 |
| w11 | 48 | 0.051572 | 25.823 |
| w12 | 19 | 0.050703 | 10.799 |
| w13 | 43 | 0.008034 | -14.794 |
| w14 | 17 | 0.198737 | -20.712 |
| w15 | 51 | -0.081183 | 8.882 |
| w16 | 22 | 0.239967 | 22.837 |
| w17 | 27 | 0.031109 | 16.276 |
| w18 | 49 | 0.206714 | -13.04 |
| w19 | 50 | 0.145741 | 12.392 |
| w20 | 50 | 0.061095 | 0.551 |
| w21 | 30 | 0.034714 | 15.677 |
| w22 | 25 | 0.193686 | 15.15 |
| w23 | 4 | -0.036945 | 1.027 |
| w24 | 37 | 0.004491 | -12.684 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.143697 | -19.399 |
| w2 | 53 | 0.041701 | -7.781 |
| w3 | 27 | 0.302491 | 8.116 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 22 | 0.155592 | 25.715 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | 0.160164 | -3.103 |
| w9 | 18 | 0.046687 | 13.645 |
| w10 | 19 | 0.064306 | 11.512 |
| w11 | 46 | 0.048575 | 64.624 |
| w12 | 13 | 0.05903 | 12.214 |
| w13 | 26 | -0.085487 | -19.539 |
| w14 | 49 | 0.192156 | -0.4 |
| w15 | 26 | 0.021719 | -6.963 |
| w16 | 41 | 0.015077 | 4.757 |
| w17 | 29 | -0.01011 | -19.774 |
| w18 | 41 | 0.0943 | -6.389 |
| w19 | 44 | -0.064469 | -15.842 |
| w20 | 60 | 0.120516 | -2.089 |
| w21 | 44 | -0.017425 | 10.234 |
| w22 | 53 | 0.086447 | -31.573 |
| w23 | 21 | 0.134469 | 31.068 |
| w24 | 22 | 0.041599 | 3.674 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 36 | 0.073297 | -10.089 |
| w3 | 21 | 0.168445 | 10.032 |
| w4 | 12 | 0.136672 | 23.361 |
| w5 | 26 | 0.029664 | 28.733 |
| w6 | 1 | 0.066606 | 9.245 |
| w7 | 0 | None | 0.0 |
| w8 | 49 | 0.034598 | 16.028 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.031978 | 7.908 |
| w11 | 57 | -0.096063 | 24.054 |
| w12 | 30 | -0.047931 | 1.929 |
| w13 | 27 | -0.0364 | -6.719 |
| w14 | 31 | 0.173478 | -10.039 |
| w15 | 36 | 0.156034 | 24.643 |
| w16 | 30 | 0.042123 | -7.67 |
| w17 | 42 | 0.008299 | 3.017 |
| w18 | 36 | 0.16919 | -7.845 |
| w19 | 45 | 0.128138 | 6.542 |
| w20 | 29 | 0.120196 | -8.24 |
| w21 | 43 | -0.058465 | 7.392 |
| w22 | 58 | -0.065478 | 3.187 |
| w23 | 14 | 0.066255 | 8.608 |
| w24 | 30 | -0.04347 | -2.217 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.062591 | -16.349 |
| w2 | 34 | 0.010277 | -25.786 |
| w3 | 12 | 0.110852 | 6.673 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | 0.050742 | 10.853 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.07722 | 1.987 |
| w9 | 3 | 0.035025 | -4.07 |
| w10 | 7 | 0.08523 | 4.283 |
| w11 | 48 | 0.033446 | 38.819 |
| w12 | 15 | -0.025489 | -1.93 |
| w14 | 35 | 0.140684 | -13.608 |
| w15 | 32 | 0.002095 | -0.333 |
| w16 | 43 | 0.051019 | 3.659 |
| w17 | 29 | -0.029766 | 10.445 |
| w18 | 41 | 0.246584 | -19.347 |
| w19 | 62 | 0.230312 | -6.467 |
| w20 | 37 | 0.152899 | 26.526 |
| w21 | 26 | 0.094377 | 19.425 |
| w22 | 33 | 0.062121 | 3.058 |
| w23 | 29 | -0.177898 | -5.915 |
| w24 | 38 | -0.102379 | 24.793 |

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
| w1 | 7 | 0.104497 | 3.101 |
| w2 | 0 | -0.022929 | 0.0 |
| w3 | 0 | 0.151615 | 0.0 |
| w4 | 0 | 0.09025 | 0.0 |
| w5 | 24 | -0.022014 | 2.698 |
| w6 | 22 | 0.05814 | 4.513 |
| w8 | 6 | 0.079045 | -1.519 |
| w9 | 14 | 0.079425 | 11.297 |
| w10 | 9 | 0.042422 | -2.227 |
| w11 | 55 | 0.022774 | 161.656 |
| w12 | 3 | -0.032217 | -5.858 |
| w14 | 22 | 0.112904 | 7.499 |
| w15 | 22 | 0.040631 | -4.506 |
| w16 | 48 | 0.001988 | -3.099 |
| w17 | 44 | 0.031939 | -2.427 |
| w18 | 32 | 0.145618 | -2.81 |
| w19 | 44 | -0.015059 | -6.091 |
| w20 | 22 | -0.015569 | 17.692 |
| w21 | 33 | -0.035684 | 27.026 |
| w22 | 49 | 0.04657 | 8.719 |
| w23 | 9 | 0.093409 | 11.496 |
| w24 | 14 | 0.014596 | 2.823 |

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
| w1 | 18 | 0.130071 | 23.774 |
| w2 | 39 | 0.125257 | -15.532 |
| w3 | 15 | 0.254718 | 21.479 |
| w4 | 7 | -0.033653 | 1.588 |
| w5 | 20 | 0.107659 | 31.706 |
| w6 | 12 | 0.100761 | -10.157 |
| w7 | 11 | -0.009249 | -7.996 |
| w8 | 10 | 0.162026 | 0.026 |
| w9 | 26 | 0.116901 | 4.599 |
| w10 | 23 | -0.033836 | -3.812 |
| w11 | 48 | 0.004738 | 36.427 |
| w12 | 34 | -0.00243 | 29.255 |
| w13 | 31 | 0.084438 | -8.683 |
| w14 | 20 | 0.153565 | -19.998 |
| w15 | 40 | 0.039567 | -20.595 |
| w16 | 59 | -0.03971 | 7.11 |
| w17 | 34 | 0.006943 | -11.57 |
| w18 | 41 | 0.249744 | -3.404 |
| w19 | 62 | 0.069981 | 2.076 |
| w20 | 38 | -0.079762 | 4.492 |
| w21 | 48 | -0.027763 | 36.685 |
| w22 | 56 | -0.088241 | -24.11 |
| w23 | 14 | -0.054315 | 5.133 |
| w24 | 46 | -0.085451 | 35.741 |

