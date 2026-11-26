# Backtest of 032-02_choppy-downside-break-rebounds_1d

- Plan: `../../../../03_test_plan/night7_rangefail_run/plans/032-02_choppy-downside-break-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.048752 | -0.533 |
| w2 | 3 | 0.04303 | -1.47 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.068838 | -1.914 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.10763 | 0.44 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.009543 | -0.845 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.030682 | 1.253 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.030317 | -5.341 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.079872 | 0.367 |
| w21 | 0 | -0.002471 | 0.0 |
| w22 | 1 | -0.204021 | -1.35 |
| w23 | 0 | 0.001538 | 0.0 |
| w24 | 3 | 0.111053 | 0.874 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.183904 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.052874 | -2.589 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.097107 | 0.0 |
| w8 | 0 | -0.03611 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.076739 | -0.753 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.020574 | 0.054 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.069361 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.122795 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.05535 | 0.0 |
| w2 | 0 | 0.008964 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.217179 | 2.024 |
| w5 | 3 | -0.148548 | -1.351 |
| w6 | 0 | 0.148163 | 0.0 |
| w7 | 0 | 0.148299 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.062497 | -1.508 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.039301 | 14.974 |
| w18 | 2 | 0.169854 | -0.967 |
| w19 | 2 | 0.035557 | 1.031 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.023023 | 0.0 |
| w23 | 2 | 0.036808 | 2.493 |
| w24 | 0 | 0.01209 | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | -0.18394 | -2.268 |
| w3 | 0 | -0.002797 | 0.0 |
| w4 | 2 | 0.04467 | 1.643 |
| w5 | 6 | 0.206196 | -1.767 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.163937 | -0.578 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.030187 | -8.862 |
| w15 | 0 | 0.049498 | 0.0 |
| w16 | 1 | -0.026241 | -5.468 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.136203 | -2.798 |
| w20 | 0 | 0.01435 | 0.0 |
| w21 | 4 | -0.051962 | -0.612 |
| w22 | 0 | 0.165377 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.053661 | 0.788 |
| w3 | 0 | 0.346715 | 0.0 |
| w4 | 0 | 0.019295 | 0.0 |
| w5 | 2 | -0.005544 | 0.067 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.191893 | 0.0 |
| w8 | 1 | -0.098827 | -1.1 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | 0.059944 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.017986 | 1.039 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.090517 | -1.442 |
| w16 | 2 | 0.042137 | 2.096 |
| w17 | 2 | 0.323625 | -0.734 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | -0.307497 | 0.0 |
| w20 | 2 | 0.090563 | 1.9 |
| w21 | 0 | 0.017992 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.033845 | 3.25 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.036754 | -0.008 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.052642 | 0.0 |
| w4 | 1 | -0.069104 | -2.325 |
| w5 | 4 | 0.010666 | -4.712 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.055302 | -1.736 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.049074 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.032118 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.147843 | -3.377 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.274456 | 0.34 |
| w19 | 2 | 0.220953 | 0.177 |
| w20 | 1 | -0.099977 | -0.666 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

