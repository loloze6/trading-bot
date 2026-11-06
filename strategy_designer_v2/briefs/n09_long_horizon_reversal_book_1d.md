---
research_goal: "Can the long-horizon reversal seen on LTC and XMR (12-month return ranks against the next 60 days) be turned into a rule that pays after cost on daily bars?"
venue: kraken
product: "LTC/USD, XMR/USD, ZEC/USD spot"
strategy_domain: long_horizon_reversal
bar_size: 1d
already_tried:
  - "On LTC and XMR daily, fold C: the rank correlation between the 12-month log return and the next 60-day return is negative (-0.31 LTC, -0.12 XMR, 5 and 6 of 6 windows). It is a ranking, not a book: no profit rule has been tested."
---
# A book from the long-horizon reversal (night brief 09)
A negative rank correlation says extreme 12-month gains are followed by weak 60-day returns and extreme losses by strong ones. This brief asks for rules that trade it: enter after a drawdown of a given depth or a 12-month return below a threshold, exit after a horizon or a recovery; or the short side after a run-up. Measures should be net return after cost or hit rate, so the answer is about money. Fees 0.15% per round trip. All three coins must pass.
