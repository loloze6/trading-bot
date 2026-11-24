# Backtest of 031-02.b1.b2_flat-day-after-strong-rise_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b2_flat-day-after-strong-rise_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.081535 | 2.748 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.06286 | -3.535 |
| w2 | 2 | -0.045117 | -12.8 |
| w3 | 4 | -0.047946 | 21.347 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.234341 | 0.0 |
| w2 | 7 | -0.090591 | 23.24 |
| w3 | 4 | 0.227117 | 3.695 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.062338 | -13.902 |
| w3 | 0 | None | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.183142 | 0.367 |
| w2 | 5 | 0.282124 | 50.269 |
| w3 | 0 | None | 0.0 |

