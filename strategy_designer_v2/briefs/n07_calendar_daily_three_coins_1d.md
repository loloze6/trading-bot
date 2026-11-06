---
research_goal: "On daily bars of three coins, do calendar effects (turn of month, day of week, month of year, monthly expiry weeks) carry a return edge after cost?"
venue: kraken
product: "BTC/USD, ETH/USD, LTC/USD spot"
strategy_domain: daily_calendar
bar_size: 1d
already_tried:
  - "On BTC and ADA daily, fold A: a turn-of-month inflow claim (long from the last day of the month for 3 days) passed on ADA (+0.37%, 5 of 6 windows) and had the right sign on BTC but fell short of 0.2%. On hourly bars: weekend and US-open effects are volatility only."
---
# Calendar effects on daily bars (night brief 07)
The clock predicts volatility on hourly bars. On daily bars the question is direction: are there days of the month, days of the week, or weeks of the month where returns differ after cost? Ideas must name the calendar rule exactly (computable from the bar's date) and the horizon, and should say who the flow is (salaries, fund rebalancing, option expiries, weekend positioning). Fees 0.15% per round trip. All three coins must pass.
