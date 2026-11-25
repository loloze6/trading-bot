---
backtest: 033-02_upside-break-continues-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8739 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3197 | above 0 | yes |
| Mean daily return, on days in a position | 0.000779 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.728 | above 0 | yes |
| Calmar | 0.7094 | above 0.75 | no |
| Trades per day | 0.03589 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.490 % |
| Yearly return | +8.0 % (over 7.94 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-02_upside-break-continues-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
