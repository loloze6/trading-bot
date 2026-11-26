---
backtest: 058-02.b2_calm-range-position-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2078 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3618 | above 0 | no |
| Mean daily return, on days in a position | 0.000298 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01782 | above 0 | yes |
| Calmar | 0.062 | above 0.75 | no |
| Trades per day | 0.1063 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.673 % |
| Yearly return | +1.9 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b2_calm-range-position-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
