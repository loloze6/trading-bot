---
backtest: 058-02_choppy-agitated-weekly-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4584 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.028 | above 0 | no |
| Mean daily return, on days in a position | -0.001207 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8438 | above 0 | no |
| Calmar | -0.1331 | above 0.75 | no |
| Trades per day | 0.0282 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.467 % |
| Yearly return | -4.4 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/058-02_choppy-agitated-weekly-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
