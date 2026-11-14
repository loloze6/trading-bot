# Exercise 2: the twelve helper outputs, side by side

Revised system prompt (`helper_system_prompt.md`; changes in `prompt_diff_from_exercise_1.txt`). Same requests as exercise 1 (`../exercise_1/inputs/`). Two samples per cell. Cost is the list price reported by the call.

## Context 1: no theme

### sonnet, sample 1: 0.0097 USD, 1649 tokens in, 301 out (0 thinking), 5.9 s

```
---
---
After a sharp, high-volume drop in a coin's price, the price tends to recover part of the drop over the following bars, because much of that selling is forced or impatient rather than informed. Leveraged longs hit liquidation levels and sell at any price, and holders who panic sell into thin order books, so the price overshoots the level that its value would support. Liquidity providers and patient buyers are slower to step in, and they absorb the excess supply once the forced sellers are gone, which pulls the price back. The recovery should be larger when the drop came with unusually high volume and a close near the bar's low, since that points to a forced flush rather than slow selling. The theory is wrong if, after such drops, the price on average continues lower or shows no partial recovery beyond what ordinary price noise would give, or if high-volume drops recover no more than quiet drops of similar size.

short-name: forced-selling-flush-rebound
other-theories: none
```

### sonnet, sample 2: 0.0095 USD, 1652 tokens in, 279 out (0 thinking), 6.4 s

```
---
---
After a sharp, high-volume drop in a coin's price, the market tends to partly rebound over the following bars, because the drop is driven by forced and impatient sellers rather than by new information. Liquidated leveraged longs, stop-loss orders and panic sellers must trade at once whatever the price, so they push price past what buyers who are not in a hurry would pay. Liquidity providers and patient buyers are slow to step in, and they take the other side only once price has moved well away from where it was. Price then drifts back as that selling pressure runs out. If the drop instead carries on in the same direction, or if rebounds after such drops are no larger than after ordinary drops of similar size on normal volume, the theory is wrong. The reason is my own reasoning, not taken from a source.

short-name: volume-capitulation-rebound-reversal
other-theories: none
```

### opus, sample 1: 0.0198 USD, 1646 tokens in, 328 out (0 thinking), 8.3 s

```
---
---
When a coin falls sharply on unusually heavy volume, part of the selling comes from traders who must sell regardless of price: leveraged longs being liquidated, stop orders being triggered in a cascade, and holders capitulating under margin or loss limits. Because this forced flow is driven by position size and price thresholds rather than by new information about the coin's value, it can push the price below the level that discretionary buyers consider fair. Those discretionary buyers and market makers are slow to step in during the cascade, since they face the same uncertainty and widening spreads, so the overshoot is corrected only after the forced selling is exhausted. The theory is that such high-volume sharp declines tend to be followed by a partial rebound, while declines of similar size on ordinary volume, which more likely reflect information, show no such rebound. It would be shown wrong if price after high-volume sharp drops continues lower or drifts no differently than after equally large drops on normal volume.

short-name: forced-selling-overshoot-rebound
```

### opus, sample 2: 0.0192 USD, 1647 tokens in, 298 out (0 thinking), 7.8 s

```
---
---
When a coin's price falls sharply on unusually heavy volume, part of that selling is forced: leveraged longs on derivatives venues get liquidated, and the hedges and arbitrage links between futures and spot carry that selling into the spot market. Forced sellers trade on account balance, not on value, so they push the price past where willing holders would sell, and the move should partly reverse once the forced flow is exhausted. A drop of the same size on ordinary volume is more likely to reflect new information that holders act on by choice, and should reverse less or keep going. The theory is that a heavy-volume selloff is followed by a larger rebound than a light-volume selloff of the same size. It would be shown wrong if heavy-volume drops reverse no more than light-volume drops, or if they keep falling further, which would suggest the volume marks informed selling rather than forced selling.

short-name: forced-selling-volume-reversal
```

## Context 2: RSI theme on BTC, ETH, BNB

### sonnet, sample 1: 0.0147 USD, 1687 tokens in, 780 out (440 thinking), 10.5 s

```
---
instruments: BTC, ETH, BNB
---
Does the Relative Strength Index (RSI), a bounded summary of recent gains against recent losses, carry information about the direction of BTC, ETH and BNB price moves that the recent returns themselves do not already give? It could point toward reversal: after sharp one-sided moves, leveraged traders are forced out and impatient buyers or sellers push price past where liquidity can absorb it, and price then partly retraces. It could instead point toward continuation: information spreads slowly and traders herd, so a high reading marks a trend still being absorbed rather than an exhaustion. It could also carry nothing, because RSI is only a transform of past prices, is watched by many traders, and any edge would be competed away. The theory is wrong if price moves following extreme RSI readings do not differ from those following ordinary readings, or if the direction of any difference flips between coins and market regimes with no consistent pattern. The reasons here are mine; no source was given.

short-name: rsi-extremes-predict-direction
```

### sonnet, sample 2: 0.0103 USD, 1686 tokens in, 340 out (0 thinking), 7.0 s

```
---
instruments: BTC, ETH, BNB
---
Does the Relative Strength Index, a bounded momentum reading built from recent up-closes versus down-closes, carry information about the direction or size of the next price moves in BTC, ETH and BNB? It could, because stretched readings mark runs of one-sided buying or selling that may end in forced liquidations, exhausted flow and short-term mean reversion by liquidity providers, or may instead persist as trends when slower participants chase and leveraged traders are pushed to add to the move. It could also carry nothing, because the reading is only a transformation of past closes that traders widely see, so any edge may already be traded away, and its meaning may differ between the three coins and between calm and trending regimes. The theory would be shown wrong if stretched readings, high or low, are followed by price behaviour no different from that after ordinary readings, in all three coins and in both trending and ranging conditions. The reasoning here is mine, not from a source.

short-name: rsi-predicts-next-moves
other-theories: none
```

### opus, sample 1: 0.0264 USD, 1679 tokens in, 636 out (281 thinking), 12.5 s

```
---
instruments: BTC, ETH, BNB
---
Does the RSI, which measures how one-sided recent up and down closes have been, carry information about where BTC, ETH and BNB go next, and if so, does a stretched reading point to a reversal or a continuation? It could point to reversal: a run of one-sided closes is often driven by impatient traders or forced sellers and buyers, such as liquidated leveraged positions. Those who absorb that flow are paid by the price snapping back once the pressure is spent. It could point to continuation: news and flows reach participants slowly, and trend followers and herding traders keep buying strength and selling weakness, so a one-sided run marks demand that persists. It could also carry no information at all, because RSI is among the most watched indicators in crypto and any simple pattern in it may already be traded away. The idea that RSI predicts price behaviour would be shown wrong if price moves after stretched-high, stretched-low and neutral readings did not differ in direction or size beyond what chance alone produces in these three coins.

short-name: rsi-predicts-price-direction
```

### opus, sample 2: 0.0227 USD, 1685 tokens in, 450 out (92 thinking), 10.1 s

```
---
instruments: BTC, ETH, BNB
---
Does the RSI, a measure of how one-sided recent up and down moves have been, carry information about where BTC, ETH and BNB prices go next, and if so, does a stretched reading point to reversal or to continuation? It could point to reversal: when buying or selling has been lopsided, short-term traders and liquidity providers may be holding stretched positions, and as that one-sided flow tires and they unwind, price gives some of the move back. It could point to continuation: in crypto, strong moves often draw in late trend followers and force out traders on the wrong side through stop-outs and margin calls, so a high reading may mark a trend gathering strength rather than ending. It could also carry no information: RSI is built only from past closes, it is watched by so many participants on these large, liquid coins that any simple edge may already be traded away, and its readings may just restate recent returns. The theory is wrong if price behaviour after stretched or neutral RSI readings looks no different, in direction or size, from price behaviour at other times.

short-name: rsi-predicts-major-coins
```

## Context 3: TradingView listing page

### sonnet, sample 1: 0.0538 USD, 12033 tokens in, 436 out (0 thinking), 7.6 s

```
---
source: TradingView, "SMAcross-mvr" (SMAcross-mvrNew v2) by vmedaram1, a moving-average crossover strategy page
---
When a short moving average of prices crosses above a longer one, the coin tends to keep drifting in that direction over the following bars, and the same holds in reverse after a cross below. The source gives no reason; my reason is that large holders build or unwind positions in steps, and slower participants react to a move only after it has persisted, so a trend that has already started is extended. A cross of the short average over the long one is a delayed sign that such a persistent move is under way. The theory is wrong if, after such crosses, price direction over the following bars is no more likely to continue than to reverse, or if it tends to reverse, as it would in a market that mean-reverts around its longer average.

short-name: sma-cross-trend-persistence
other-theories: Price crossing the long average (rather than the two averages crossing) marks trend-continuation entries, a variant of the same idea | Exiting when price closes beyond the short average ends trends earlier than waiting for the opposite cross | Other scripts listed on the page (SPY mean-reversion with ML filter, RSI/SMA pullbacks, 3-bar ignite-pullback-confirm pattern, Ichimoku with Bollinger Bands)
```

### sonnet, sample 2: 0.0602 USD, 12036 tokens in, 1070 out (526 thinking), 13.3 s

```
---
source: TradingView, script "SMAcross-mvr" by vmedaram1 (Dec 30, 2025), shown with a list of related moving-average strategy scripts
---
When a short-horizon average of price moves from below to above a longer-horizon average, the market is more likely to keep drifting in that direction than to fall back. The same holds in reverse for a downward crossing. The source gives no reason beyond calling this classic trend-following, so the reason below is mine. Information and capital spread slowly, so some participants react late. Trend followers and momentum-chasing flows add to moves that are already under way, which makes the drift persist for a while. The theory is wrong if, across many coins, price movement after an upward crossing is no more positive than after a downward crossing or at random times. It is also wrong if the typical post-crossing move is reversed quickly, so that crossings mostly mark whipsaws around a flat or mean-reverting price.

short-name: moving-average-cross-trend-persistence
other-theories: Price in a long-term uptrend that briefly dips into oversold territory tends to rebound (Connors RSI and SMA) | Price stretched far below or above a long average reverts toward it (SMA offset, Z-score mean reversion) | Price crossing a long average continues as a pullback entry within the trend (entry mode B) | A trend filter from a very long average improves the reliability of shorter crossovers | A three-candle ignite, pullback and confirmation pattern predicts continuation | Aligned stacks of several averages followed by a snap-back toward a fast average signal a bounce | Overnight or session-specific holding carries gap risk that a session filter avoids
```

### opus, sample 1: 0.1229 USD, 12031 tokens in, 1265 out (583 thinking), 18.2 s

```
---
source: TradingView, "SMAcross-mvr" (SMAcross-mvrNew v2) by vmedaram1, Dec 30 2025, with the surrounding TradingView SMA strategy listing
---
When a short-term average of price crosses a longer-term average, or price itself crosses the longer-term average, the move tends to keep going in the direction of the cross for a while instead of fading. So the side of the long average that price sits on carries information about the coming drift. The source offers no reason beyond calling the crossing a sign of trend, so the reason here is mine. Traders take in news and shifts in demand slowly and unevenly, and many trend-following and momentum participants pile in only after a trend is visible. That late buying or selling extends moves that have already begun. The theory is wrong if price after such crossings drifts no more in the direction of the cross than at random times. It is also wrong if price tends to reverse back across the long average, which would mean a crossing marks exhaustion rather than continuation.

short-name: moving-average-cross-trend-persistence
other-theories: S&P 500 z-score mean reversion filtered by machine learning and trading session | fast/slow average cross taken only in the direction of a long-term trend filter | ignite-pullback-confirmation three-bar continuation pattern | Vortex indicator cross confirmed by a moving average | RSI oversold/overbought combined with an average trend filter | Ichimoku cloud combined with Bollinger Bands | Larry Connors pullback: RSI oversold below a fast average within an uptrend, reverting to the fast average | count of fast-above-slow averages as uptrend strength, buying oversold dips | Heikin-Ashi moving-average candles as an always-in trend signal | Awesome Oscillator with average alignment for trend entries | rate-of-change bands around reference averages | mean reversion when price is stretched far below or above a long average | Traders Dynamic Index built on MFI or RSI | snap-back bounce after averages fan out in a stretched trend | price crossing the 200-period average as a trend signal
```

### opus, sample 2: 0.1233 USD, 12030 tokens in, 1289 out (584 thinking), 27.6 s

```
---
source: TradingView, "SMAcross-mvr" (SMAcross-mvrNew v2) by vmedaram1, Dec 30, 2025, with the surrounding moving-average strategy listing
---
When a short-term average of price crosses a longer-term average, it marks the start of a trend, and price tends to keep moving in the direction of the cross more often than chance would allow. A variant of the idea is that price crossing back over the longer average marks a pullback ending and the trend resuming. The source gives no reason beyond calling the shaded zone between the averages a way to "recognise the trend." The reason here is mine. News and changes in demand are absorbed by market participants slowly and unevenly, and late buyers and sellers who chase recent moves keep pushing price the same way, so a shift in direction tends to persist for a while. The theory is wrong if price moves after such crosses are no more likely to continue in the crossing direction than at random times, or if they tend to reverse, so that crosses mostly mark exhaustion rather than the start of a trend.

short-name: moving-average-cross-trend-persistence
other-theories: Z-score mean reversion in the S&P 500 with a machine-learning filter, trading only within the session | moving-average cross taken only in the direction of a longer trend average | ignite-pullback-confirmation three-bar continuation pattern | Vortex indicator cross confirmed by a moving average | RSI oversold or overbought signals combined with a moving-average trend | Ichimoku cloud combined with Bollinger Bands | Larry Connors pullback: RSI oversold below a fast average within an uptrend reverts back to that average | trend strength scored by how many fast averages sit above slow ones | always-in-market trend following with Heikin-Ashi moving-average candles | Awesome Oscillator momentum with moving-average alignment | rate-of-change bands around moving averages | buying a stretch below a long moving average and selling a stretch above it | Traders Dynamic Index built on MFI or RSI | snap-back reversal after the moving averages fan out in a stretched trend | price crossing the 200-period average as a trend switch
```
