---
backtest: 066-02_falling-agitated-year-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1618 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.2282 | above 0 | no |
| Mean daily return, on days in a position | -0.0004273 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3772 | above 0 | no |
| Calmar | -0.3475 | above 0.75 | no |
| Trades per day | 0.06198 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.535 % |
| Yearly return | -2.1 % (over 0.87 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/066-02_falling-agitated-year-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
