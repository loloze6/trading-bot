---
backtest: 032-02.b2.g1.d1.d1_close-location-wide-days-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3162 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.238 | above 0 | no |
| Mean daily return, on days in a position | 0.0004512 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1967 | above 0 | yes |
| Calmar | 0.1247 | above 0.75 | no |
| Trades per day | 0.3525 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.535 % |
| Yearly return | +5.1 % (over 7.94 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d1.d1_close-location-wide-days-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
