# Backtest of 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d

- Plan: `../../../../03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.012353 | -2.519 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | -0.029011 | -3.677 |
| w5 | 1 | -0.162412 | -2.224 |
| w6 | 1 | 0.09465 | 4.199 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.246201 | 0.0 |
| w11 | 2 | -0.098162 | 5.736 |
| w12 | 5 | -0.051374 | 1.292 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.050218 | 1.256 |
| w16 | 2 | 0.015015 | -1.512 |
| w17 | 2 | 0.135813 | 8.644 |
| w18 | 0 | -0.01825 | 0.0 |
| w19 | 2 | -0.062461 | -1.57 |
| w20 | 0 | None | 0.0 |
| w21 | 8 | -0.017123 | 7.947 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.0057 | -8.917 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.064651 | -1.17 |
| w3 | 0 | None | 0.0 |
| w4 | 5 | -0.236601 | 0.75 |
| w5 | 1 | -0.140053 | -3.706 |
| w6 | 6 | 0.034992 | 9.224 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.048924 | 1.399 |
| w11 | 4 | 0.012404 | 8.168 |
| w12 | 2 | -0.017362 | -0.543 |
| w13 | 0 | 0.108156 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.015363 | 4.963 |
| w16 | 0 | -0.030202 | 0.0 |
| w17 | 3 | 0.032432 | -0.295 |
| w18 | 1 | None | -0.011 |
| w19 | 0 | 0.030923 | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.060556 | 4.398 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.047733 | 0.833 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.213498 | 0.0 |
| w4 | 1 | -0.153511 | -2.325 |
| w5 | 2 | -0.023549 | -4.243 |
| w6 | 2 | -0.021735 | 4.392 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.087328 | 3.721 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.055408 | 0.0 |
| w11 | 2 | -0.022463 | 4.435 |
| w12 | 2 | 0.025557 | -0.462 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.030834 | 0.0 |
| w16 | 0 | 0.017161 | 0.0 |
| w17 | 2 | 0.11718 | 5.493 |
| w18 | 2 | -0.006443 | -3.546 |
| w19 | 1 | -0.119416 | -3.639 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.083468 | 12.208 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.004223 | -5.038 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.053789 | -0.314 |
| w2 | 2 | -0.060772 | -1.529 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.009326 | 2.507 |
| w5 | 0 | 0.01276 | 0.0 |
| w6 | 1 | -0.062688 | -2.959 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | -0.175698 | -0.858 |
| w11 | 1 | -0.240618 | -5.575 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.013573 | 0.229 |
| w16 | 2 | 0.037028 | -2.141 |
| w17 | 2 | -0.06271 | 2.222 |
| w18 | 2 | 0.057723 | 0.122 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.083081 | -0.008 |
| w21 | 2 | 0.333383 | 2.259 |
| w22 | 0 | -0.147047 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.038847 | 3.867 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.253137 | 2.81 |
| w5 | 2 | -0.153277 | -6.816 |
| w6 | 2 | 0.025984 | 7.231 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | -0.083755 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.0687 | -5.078 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.16656 | -0.696 |
| w16 | 0 | 0.066344 | 0.0 |
| w17 | 3 | -0.006141 | 59.732 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.118894 | -1.488 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.052015 | -2.834 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.020671 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.038609 | -3.84 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.0287 | -1.946 |
| w7 | 2 | -0.008086 | -8.996 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | -0.200836 | 2.162 |
| w11 | 2 | -0.122358 | 15.594 |
| w12 | 3 | -0.068093 | -9.236 |
| w13 | 1 | -0.10006 | -2.137 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.02846 | 1.558 |
| w16 | 2 | -0.02204 | -2.933 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.059319 | -7.102 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.290905 | -1.332 |
| w21 | 2 | 0.005643 | 3.318 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.002235 | 2.329 |

