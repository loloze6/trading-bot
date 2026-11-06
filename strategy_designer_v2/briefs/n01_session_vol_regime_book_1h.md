---
research_goal: "Is there a return rule that pays inside the high-volatility sessions already validated as filters (the US open hour, bars with a volume surprise) and stays flat through the weekend compression?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: session_conditional_intraday
bar_size: 1h
already_tried:
  - "Validated filters, not to re-test: weekend volatility is 0.64 to 0.78 of weekday; the hours 13 to 14 UTC on weekdays carry 1.3 to 1.5x volatility; a bar with volume 3x its trailing median carries 1.6 to 1.9x volatility. Failed: continuation from the US open hour over 6 bars; weekend hourly reversion; Monday reversal of the weekend move; asian session drift."
---
# Session-conditional intraday rules (night brief 01)
Three volatility filters hold on BTC, ETH and SOL. None of them says which way price goes. This brief asks for return rules that use the filters as the gate: trade only when the gate is open, flat otherwise, so the book pays fees only in hours where something happens. Ideas may combine a gate with any direction rule computable from bars: momentum, reversal, range break, volume sign. Each idea must say why the gate improves the rule, and be measured against the same rule without the gate where possible. Fees are 0.15% per round trip; an intraday rule that trades daily must clear that with margin. Both symbols must pass.
