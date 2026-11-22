# Backtest of 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h

- Plan: `../../../../03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.075801 | 1.719 |
| w3 | 2 | 0.013609 | -2.786 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.043086 | -0.874 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.008067 | 2.147 |
| w9 | 2 | 0.005782 | -0.548 |
| w10 | 2 | -0.020178 | -0.225 |
| w11 | 4 | 0.016745 | 12.733 |
| w12 | 6 | 0.112103 | 5.529 |
| w13 | 0 | None | 0.0 |
| w14 | 6 | -0.045138 | -4.399 |
| w15 | 6 | 0.041742 | 6.797 |
| w16 | 1 | -0.024718 | -2.525 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.152326 | 3.326 |
| w20 | 2 | 0.134344 | 2.89 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.030179 | 0.91 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.004134 | -3.758 |
| w3 | 2 | -0.075588 | -1.817 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.023304 | 0.062 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.016234 | 3.465 |
| w9 | 2 | 0.013841 | 0.86 |
| w10 | 2 | 0.038843 | 1.141 |
| w11 | 9 | -0.0048 | 8.184 |
| w12 | 2 | 0.004592 | 5.969 |
| w13 | 0 | 0.065645 | 0.0 |
| w14 | 3 | -0.024979 | -3.52 |
| w15 | 4 | -0.025901 | -2.847 |
| w16 | 2 | 0.154763 | 8.605 |
| w17 | 2 | 0.082867 | 4.545 |
| w18 | 2 | 0.108447 | 3.455 |
| w19 | 2 | 0.15808 | 3.685 |
| w20 | 2 | 0.085795 | 1.173 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.103972 | -4.764 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.000266 | 2.359 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.050817 | -2.165 |
| w3 | 2 | -0.049542 | 4.261 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.012688 | 0.102 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.065422 | 7.102 |
| w9 | 1 | -0.161139 | -1.172 |
| w10 | 2 | 0.022467 | 1.099 |
| w11 | 2 | 0.019395 | 0.124 |
| w12 | 2 | -0.005976 | -6.267 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | 0.042431 | -0.174 |
| w15 | 2 | -0.036529 | -3.818 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.09276 | 2.874 |
| w20 | 4 | 0.13682 | 4.375 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.038304 | 0.307 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.114332 | -1.329 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.004276 | 0.922 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.02663 | 1.22 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.025881 | 1.454 |
| w11 | 6 | 0.096555 | 17.597 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | -0.10947 | -9.312 |
| w15 | 4 | -0.054872 | 0.628 |
| w16 | 4 | 0.016101 | -2.144 |
| w17 | 2 | 0.018564 | 7.483 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.077834 | 0.808 |
| w20 | 2 | 0.029955 | 1.853 |
| w21 | 2 | -0.044679 | 1.417 |
| w22 | 4 | 0.006423 | 1.33 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.082076 | 1.262 |
| w4 | 2 | 0.055307 | 1.726 |
| w5 | 4 | 0.024115 | -3.224 |
| w6 | 2 | 0.038811 | -0.564 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.022953 | 1.385 |
| w9 | 4 | 0.065304 | -0.334 |
| w10 | 2 | 0.062869 | 0.489 |
| w11 | 4 | 0.007483 | 18.7 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | -0.003324 | -3.192 |
| w15 | 7 | -0.052657 | 5.274 |
| w16 | 2 | 0.134315 | 6.967 |
| w17 | 2 | -0.013046 | -6.982 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.067707 | 1.745 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.013749 | 0.599 |
| w22 | 2 | 0.171425 | 0.105 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.008673 | 2.511 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.100508 | -1.313 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.006162 | 2.264 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.02149 | 1.36 |
| w9 | 2 | 0.110215 | -2.067 |
| w10 | 2 | 0.007711 | 2.288 |
| w11 | 6 | 0.126419 | 6.726 |
| w12 | 2 | 0.087249 | 12.039 |
| w13 | 2 | 0.004375 | -0.006 |
| w14 | 2 | 0.023238 | -8.071 |
| w15 | 2 | 0.004499 | 3.922 |
| w16 | 6 | -0.00887 | 1.327 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.048542 | -3.709 |
| w19 | 4 | 0.09557 | -1.174 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.082081 | 1.496 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

