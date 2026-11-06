---
research_goal: "Does momentum in a low-volatility regime, which passed the profit bar on BTC daily bars with a volatility target, hold on three other coins' daily bars?"
venue: kraken
product: "ETH/USD, LTC/USD, XRP/USD spot"
strategy_domain: low_vol_momentum_generalisation
bar_size: 1d
already_tried:
  - "On BTC daily, fold C: a 20-day momentum rule taken only when 20-day volatility is in the lower half of its trailing year passed the judge and the engine at a 20% volatility target (median window Sharpe 2.1, worst drawdown 10.5%); at full size it breached the 20% drawdown bar."
---
# Low-volatility momentum on other coins (night brief 25)
The mechanism: trends are cleaner when volatility is low against its own history. This brief asks whether that holds on three other coins' daily bars, with freedom on the momentum horizon, the volatility window and the regime threshold. Ideas should also test the opposite regime as a control. Fees 0.15% per round trip. All three coins must pass.
