# Backtest of 054-03.b1_rising-market-reclaimed-low-continuation_1d

- Plan: `../../../../03_test_plan/pilot_panic_run/plans/054-03.b1_rising-market-reclaimed-low-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | -0.047564 | -16.998 |
| w5 | 5 | 0.012081 | 2.855 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.03187 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.037472 | -0.325 |
| w13 | 2 | 0.02052 | 2.301 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.02479 | 2.92 |
| w17 | 1 | 0.108101 | -0.497 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | -0.118377 | -2.227 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.014151 | -0.441 |
| w22 | 0 | -0.07714 | 0.0 |
| w23 | 0 | 0.073495 | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.15055 | 3.165 |
| w2 | 2 | 0.066441 | -0.872 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.034588 | -0.2 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.038381 | -0.562 |
| w8 | 0 | 0.003207 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.196467 | 8.014 |
| w12 | 2 | -0.03911 | 6.124 |
| w13 | 4 | 0.039661 | -4.458 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.417755 | 18.265 |
| w17 | 0 | 0.286393 | 0.0 |
| w18 | 3 | -0.318985 | -6.1 |
| w19 | 4 | 0.006496 | -20.023 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.145488 | -5.389 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.089756 | 2.946 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | 0.002132 | 6.269 |
| w13 | 6 | -0.134165 | -2.091 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.087182 | 5.214 |
| w16 | 0 | -0.035779 | 0.0 |
| w17 | 0 | 0.051682 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.059313 | -6.906 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.046923 | 0.221 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | 0.098493 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | 0.038512 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.066821 | -4.019 |
| w12 | 2 | 0.022882 | 2.985 |
| w13 | 1 | 0.050385 | 12.553 |
| w14 | 0 | -0.030948 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.057276 | 2.725 |
| w17 | 5 | 0.046737 | -14.555 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.062264 | -3.718 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.006796 | 0.0 |
| w24 | 0 | -0.023418 | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.017093 | -0.496 |
| w5 | 1 | 0.13801 | 2.708 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.013634 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.100328 | -1.729 |
| w13 | 2 | -0.036844 | -5.241 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.060476 | -1.549 |
| w17 | 4 | 0.225041 | 9.642 |
| w18 | 2 | 0.155274 | -3.047 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.105673 | 3.963 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.114626 | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.022107 | 1.45 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.023065 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.067455 | 2.371 |
| w13 | 1 | 0.054576 | 16.827 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.04732 | 0.0 |
| w16 | 1 | 0.470256 | 6.987 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.074315 | 1.693 |
| w24 | 2 | -0.04775 | -2.719 |

