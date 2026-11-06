---
research_goal: "On BTC and LTC daily bars, does a breakout from a volatility channel (a multiple of average range around a moving mean) with a trailing exit pay after cost, and which channel width and exit rule?"
venue: kraken
product: "BTC/USD, LTC/USD spot"
strategy_domain: daily_vol_channel
bar_size: 1d
already_tried:
  - "On ETH daily: Donchian breakout net of cost, compression-then-breakout, and trend rules with volatility gates failed. On BTC daily: low-volatility-regime momentum passed the judge and made money at full size but breached the 20% drawdown bar."
---
# Volatility channels on daily bars (night brief 17)
A channel is a mean plus a band in units of recent range. This brief asks what a close outside the band means for the following days, and whether a rule that enters on the break and exits on a trailing band or after a fixed horizon pays after 0.15% per round trip. Ideas should vary the band width, the mean, the exit and the horizon, and say why the break carries information. Both coins must pass.
