---
backtest: 058-02.b1.b2_choppy-range-position-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1147 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4395 | above 0 | no |
| Mean daily return, on days in a position | 0.0001492 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.08995 | above 0 | no |
| Calmar | 0.01319 | above 0.75 | no |
| Trades per day | 0.1542 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.903 % |
| Yearly return | +0.5 % (over 7.94 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2_choppy-range-position-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
