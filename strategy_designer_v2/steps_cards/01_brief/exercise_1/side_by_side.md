# Exercise 1: the nine helper outputs, side by side

Same system prompt (`helper_system_prompt.md`) for all nine. One call each. Cost is the list price reported by the call.

## Context 1: no theme

### haiku: 0.0006 USD, 1624 tokens in, 258 out (0 thinking), 4.3 s

```
---
bar: (not stated)
---
Thin liquidity around a round-number price level can make a coin's price overshoot it briefly and then fall back. Stop-loss and breakout orders tend to cluster just beyond round numbers, so when price touches such a level, those orders are triggered together and push price through it. Once the resting orders are used up, the price has no further push and tends to revert toward the prior range. Market makers and arbitrage traders who supply liquidity near these levels are the ones paid for absorbing this flow, so they set the reversion. The theory would be wrong if overshoots past round-number levels are followed by continuation as often as by reversion, or if the reversion is no larger than for ordinary price moves of the same size.

short-name: round-number-overshoot-reversion
other-theories: none
```

### sonnet: 0.0092 USD, 1606 tokens in, 261 out (0 thinking), 5.6 s

```
---
---
After a sharp, high-volume drop in a coin's price, the following bars tend to give back part of the drop, because the selling that caused it was partly forced rather than informed. Liquidations on leveraged positions, margin calls and stop orders push sellers to trade at any price, so they take liquidity from a thin order book and move the price past what the coin is worth. Patient buyers who provide liquidity then absorb that supply and are paid for it through a partial price recovery. The theory would be wrong if, after drops of this kind, later bars show no tendency to recover, or if they continue lower as often and as far as after equally large drops on ordinary volume. The reason is mine, not from a source; I do not know how much of the selling in spot crypto is forced.

short-name: high-volume-drop-partial-rebound
```

### opus: 0.0197 USD, 1601 tokens in, 337 out (0 thinking), 9.3 s

```
---
---
When a coin has a sharp price move on unusually heavy volume, the move tends to keep going over the following bars rather than reverse, because the heavy volume shows that informed or large traders are acting on news, and such traders often spread their orders over time to limit their impact, so part of their demand or supply is still to come. Slower traders, who read the news late or wait for confirmation, add to the move as they arrive. A sharp move on thin volume should behave differently: with no sign of a large participant behind it, it more likely reflects a temporary imbalance in a shallow order book and tends to fade as liquidity providers step back in. The reason is my own reasoning, taken from general market microstructure, not from a source. The theory is wrong if moves on heavy volume continue no more than, or reverse as often as, moves of the same size on normal or light volume, or if large moves on heavy volume tend to reverse, as would happen if heavy volume mostly marks forced liquidations and capitulation rather than informed trading.

short-name: high-volume-moves-continue
```

## Context 2: RSI theme on BTC, ETH, BNB

### haiku: 0.0015 USD, 1663 tokens in, 1676 out (1310 thinking), 12.6 s

```
---
instruments: BTC, ETH, BNB
---
When RSI, a momentum gauge built from the ratio of recent average gains to recent average losses, reaches an extreme reading for BTC, ETH or BNB, the price has usually moved far and fast in one direction over a short stretch. That move is often driven by urgent market orders that consume the resting bids or asks, pushing price past the level where other participants are willing to trade. Passive liquidity providers and slower value buyers or sellers then tend to trade against the excess, so price partly retraces over the following bars. The reason is order-book depth: when the book is thin relative to urgent flow, prices overshoot and revert. This reasoning comes from market microstructure in general and has not been checked for these three coins. The theory is wrong if, relative to each coin's unconditional behaviour, bars after RSI extremes show continuation at least as often as reversal, or if any reversal disappears once volume is accounted for. Momentum persistence, where trend followers keep an extreme running, is the main rival and could also be what the data shows.

short-name: rsi-extremes-mean-reversion
```

### sonnet: 0.0105 USD, 1643 tokens in, 333 out (0 thinking), 6.4 s

```
---
instruments: BTC, ETH, BNB
---
After a coin's recent price moves have pushed the Relative Strength Index (a bounded measure of how much of recent price change was upward versus downward) to an extreme, the following price moves differ from what they would be at other times. The question is which way: extreme highs could be followed by pullbacks, because the rise drew in late buyers and profit-taking or liquidation of leveraged longs follows, and extreme lows could be followed by rebounds, because forced sellers are exhausted. Or extremes could be followed by continuation, because in trending crypto markets strong moves attract momentum buyers and sellers who are slow to react. I do not know which effect dominates, and it may differ by coin. The theory is wrong if future returns after extreme readings are no different from returns after non-extreme readings, in either direction, once volatility and the prevailing trend are accounted for, or if any difference is not shared by BTC, ETH and BNB.

short-name: rsi-extremes-predict-returns
```

### opus: 0.0231 USD, 1638 tokens in, 472 out (106 thinking), 13.3 s

```
---
instruments: BTC, ETH, BNB
---
Does the RSI, which measures how strongly recent gains have outweighed recent losses, predict whether BTC, ETH and BNB keep moving or turn back? It could predict reversal: a high reading can mark a crowd of late buyers who have run out of new money, and a low reading can mark forced or panicked sellers, such as liquidated leveraged traders, whose selling pushes price below what patient buyers will pay, so price snaps back once that pressure ends. It could instead predict continuation: a high reading can reflect news or capital flows that slow traders and funds absorb over days, so strength keeps going, and traders who sell "overbought" coins may just be supplying the trend-followers. Or it may predict nothing, because RSI is built only from past closes, is watched by almost everyone, and any easy edge would already be traded away. The theory is wrong in both directions if returns after extreme RSI readings, high or low, look the same as returns at other times, with no reliable lean toward reversal or toward continuation.

short-name: rsi-predicts-reversal-or-continuation
```

## Context 3: TradingView listing page

### haiku: 0.0047 USD, 12017 tokens in, 1937 out (1601 thinking), 13.8 s

```
---
source: TradingView, "SMAcross-mvrNew (v2)" Pine script by vmedaram1
---
When a fast simple average of recent prices (10 bars) crosses above a slow one (50 bars), price tends to keep moving in the same direction for some time, and a downward cross tends to be followed by further falls. The reason, which comes from my own general knowledge and not from the source (the source only calls the method a classic moving-average crossover): the fast average responds to new prices sooner than the slow one, so a cross means recent prices have moved decisively away from the older average. Slow-reacting participants, such as funds that rebalance on trend signals or traders who add to winning positions, take their positions over several bars, so the move carries on after the cross. A variant of the same idea uses the price itself crossing the slow average, without the fast average. The theory is wrong if price after crosses shows no more continuation than price after arbitrary bars, or if reversals after crosses are as common as continuations.

short-name: sma-crossover-trend-persistence
```

### sonnet: 0.0531 USD, 11990 tokens in, 384 out (0 thinking), 7.0 s

```
---
source: TradingView, "SMAcross-mvr" (vmedaram1), a moving-average crossover strategy page
---
When a short-term moving average of price crosses above a longer-term one, the coin tends to keep drifting in that direction over the following bars, and the reverse after a cross below. The reason comes from me, not the source: a lasting shift in the balance of buyers and sellers is absorbed slowly, because large holders split their orders over time, information spreads unevenly, and trend followers join late, so a move that has already turned the averages is more likely to continue than to reverse at once. The crossover is a delayed signal that fires after part of the move is done, so it works only if this slow absorption outlasts the lag of the averages. The theory is wrong if returns after crosses are no different from returns after random bars, or if they tend to reverse, as in choppy ranges where crosses are mostly noise and move back through the longer average.

short-name: sma-crossover-trend-persistence
other-theories: Price crossing the long average (pullback or trend-continuation entry) behaves differently from the two-average cross | A close beyond the short average works as an early exit that beats waiting for the opposite cross
```

### opus: 0.1144 USD, 11985 tokens in, 863 out (362 thinking), 15.6 s

```
---
side: long and short
source: TradingView, "SMAcross-mvr" (SMAcross-mvrNew v2) by vmedaram1, with the strategy listing page it was pasted from
---
When a short-run average of price crosses a longer-run average, or when price itself crosses the longer average, a new trend has started and will tend to continue in the direction of the cross long enough to be captured. The position then stays on that side until the opposite cross shows the trend has turned. The source gives no reason for this beyond calling the cross a sign of trend. The reason here is mine. In crypto, information and attention spread slowly across many small, retail-heavy participants. Late buyers chase rising prices and holders sell as losses grow, so moves that have started tend to feed themselves for a while rather than reverse at once. The theory is wrong if price changes after a cross are no more likely to follow the direction of the cross than changes at random times. It is also wrong if price tends to reverse soon after crosses, so that the whipsaw losses between crosses outweigh the trending stretches.

short-name: moving-average-crossover-trend-persistence
other-theories: Extreme short-run deviation from the mean (z-score) reverts within the trading session | Short-term oversold dips inside a longer uptrend snap back to the fast average | Price stretched far below a long average tends to recover toward it | An extended, fully ordered trend snaps back sharply when price crosses back through its fastest average | A strong impulse candle followed by a pullback and a confirmation candle signals continuation
```
