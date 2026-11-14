---
research_goal: "On hourly bars of three coins, does the move of one trading session (Asia, Europe, US, defined by UTC hours) reverse or continue in the next session, after cost?"
venue: kraken
product: "BTC/USD, ETH/USD, LTC/USD spot"
strategy_domain: session_reversal
bar_size: 1h
already_tried:
  - "On ETH hourly, fold B: a fade of stretches during Asia hours passed the judge (+0.5%, 5 of 6 windows) but not the engine (Sharpe 0.33, drawdown 25%); weekend stretch continuation likewise. On BTC, ETH, SOL hourly: Asia-session drift and US-open continuation failed."
---
# Session to session on hourly bars (night brief 26)
The day has three sessions and the flows differ. This brief asks whether the return of one session (its open to close, by UTC hours) predicts the next session's return, by sign or by size, on three coins. Ideas must name the sessions' UTC hours and the horizon. Fees 0.15% per round trip. All three coins must pass.
