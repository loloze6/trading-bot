---
backtest: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4053 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1488 | above 0 | no |
| Mean daily return, on days in a position | 6.957e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2403 | above 0 | yes |
| Calmar | 0.1379 | above 0.75 | no |
| Trades per day | 0.01992 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.218 % |
| Yearly return | +1.6 % (over 7.94 years) |
| Days in a position | 67 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
