# Exercise 2: side by side

Prompt: `system_prompt_used.md`. Briefs: `inputs/`, run 001, 002, 003, 004, 005, then 001 again, each model on its own index.

## 001_rsi-extremes-predict-next-move

### opus (call 1: 4 ideas, 1 attempt(s), 0.0303 USD; call 6: 0 ideas, 1 attempt(s), 0.0292 USD, already-indexed: 001-01_rsi-high-extreme-reversal, 001-02_rsi-low-extreme-reversal, 001-03_rsi-high-extreme-continuation, 001-04_rsi-low-extreme-continuation)

**001-01_rsi-high-extreme-reversal**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the preceding rise.  
Consequence: Reversal: an overbought one-sided run reflects crowding and overshoot that unwinds once the pressure is spent.

**001-02_rsi-low-extreme-reversal**

Idea: After the relative strength index reaches a low extreme on BTC, ETH or BNB, price rises over the following bars, recovering part of the preceding fall.  
Consequence: Reversal: an oversold one-sided run reflects forced liquidations and panic selling that unwind once the pressure is spent.

**001-03_rsi-high-extreme-continuation**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: Continuation: a strong upward run reflects slowly spreading news, trend-following funds and leveraged chasing that push price further up.

**001-04_rsi-low-extreme-continuation**

Idea: After the relative strength index reaches a low extreme on BTC, ETH or BNB, price keeps falling over the following bars, more than it does after neutral readings.  
Consequence: Continuation: a strong downward run reflects slowly spreading news, trend-following selling and leveraged chasing that push price further down.

### sonnet (call 1: 4 ideas, 1 attempt(s), 0.0151 USD; call 6: 4 ideas, 1 attempt(s), 0.0218 USD, already-indexed: 001-01_overbought-rsi-then-pullback, 001-02_oversold-rsi-then-bounce, 001-03_overbought-rsi-then-continuation-up, 001-04_oversold-rsi-then-continuation-down)

**001-01_overbought-rsi-then-pullback**

Idea: After the relative strength index reaches a high extreme (overbought) following a one-sided run up, the coin's price over the following bars falls back, giving up part of the advance.  
Consequence: Reversal answer: crowding, liquidations and emotional overshoot at an upside extreme are followed by price giving back part of the move.

**001-02_oversold-rsi-then-bounce**

Idea: After the relative strength index reaches a low extreme (oversold) following a one-sided run down, the coin's price over the following bars rises back, recovering part of the decline.  
Consequence: Reversal answer: forced selling and panic overshoot at a downside extreme are followed by price recovering part of the move.

**001-03_overbought-rsi-then-continuation-up**

Idea: After the relative strength index reaches a high extreme (overbought), the coin's price over the following bars keeps rising, extending the run.  
Consequence: Continuation answer: slow news diffusion, trend-following inflows and leveraged chasing make strong upside readings precede further gains.

**001-04_oversold-rsi-then-continuation-down**

Idea: After the relative strength index reaches a low extreme (oversold), the coin's price over the following bars keeps falling, extending the decline.  
Consequence: Continuation answer: slow news diffusion, trend-following selling and leveraged chasing make weak downside readings precede further losses.

**001-05_overbought-rsi-underperforms-neutral**

Idea: After RSI reaches an overbought extreme, BTC, ETH or BNB returns over the following bars are lower than after neutral RSI readings.  
Consequence: Reversal answer: crowded one-sided runs give back part of the move, so extreme highs are followed by weaker returns than neutral readings.

**001-06_oversold-rsi-outperforms-neutral**

Idea: After RSI reaches an oversold extreme, BTC, ETH or BNB returns over the following bars are higher than after neutral RSI readings.  
Consequence: Reversal answer: overshooting sellers and forced liquidations are followed by a rebound, so extreme lows are followed by stronger returns than neutral readings.

**001-07_overbought-rsi-outperforms-neutral**

Idea: After RSI reaches an overbought extreme, BTC, ETH or BNB returns over the following bars are higher than after neutral RSI readings.  
Consequence: Continuation answer: slowly spreading news, trend-following funds and leveraged chasers push further, so extreme highs are followed by stronger returns than neutral readings.

**001-08_oversold-rsi-underperforms-neutral**

Idea: After RSI reaches an oversold extreme, BTC, ETH or BNB returns over the following bars are lower than after neutral RSI readings.  
Consequence: Continuation answer: persistent selling by trend followers and leveraged traders extends the drop, so extreme lows are followed by weaker returns than neutral readings.

## 002_moving-average-cross-trend-persistence

### opus (call 2: 6 ideas, 2 attempt(s), 0.0791 USD)

**002-01_sma-up-cross-continuation**

Idea: After the short moving average crosses above the long moving average, price keeps rising over the following bars, more often and further than after random points.  
Consequence: An upward cross of the averages starts an uptrend that persists, because late buyers extend the move.

**002-02_sma-down-cross-continuation**

Idea: After the short moving average crosses below the long moving average, price keeps falling over the following bars, more often and further than after random points.  
Consequence: A downward cross of the averages starts a downtrend that persists, because late sellers extend the move.

**002-03_price-up-cross-continuation**

Idea: After price closes above the long moving average, having been below it, price keeps rising over the following bars, more often and further than after random points.  
Consequence: Price crossing up through the long average starts an uptrend that persists, because late buyers extend the move.

**002-04_price-down-cross-continuation**

Idea: After price closes below the long moving average, having been above it, price keeps falling over the following bars, more often and further than after random points.  
Consequence: Price crossing down through the long average starts a downtrend that persists, because late sellers extend the move.

**002-05_golden-to-death-cross-gain**

Idea: From an upward cross of the averages to the next downward cross, price rises, by more than over random spans of the same length.  
Consequence: The uptrend begun by an upward cross lasts until the opposite cross ends it.

**002-06_death-to-golden-cross-loss**

Idea: From a downward cross of the averages to the next upward cross, price falls, by more than over random spans of the same length.  
Consequence: The downtrend begun by a downward cross lasts until the opposite cross ends it.

### sonnet (call 2: 6 ideas, 1 attempt(s), 0.0139 USD)

**002-01_golden-cross-uptrend-persists**

Idea: After the short moving average crosses above the long moving average, price keeps drifting upward over the following bars, more often than it does at arbitrary points.  
Consequence: An upward short-over-long average cross starts an uptrend that persists.

**002-02_death-cross-downtrend-persists**

Idea: After the short moving average crosses below the long moving average, price keeps drifting downward over the following bars, more often than it does at arbitrary points.  
Consequence: A downward short-under-long average cross starts a downtrend that persists.

**002-03_price-cross-above-long-average**

Idea: After price closes from below to above the long moving average, price keeps rising over the following bars, more often than it does at arbitrary points.  
Consequence: Price crossing up through the long average starts an uptrend that persists.

**002-04_price-cross-below-long-average**

Idea: After price closes from above to below the long moving average, price keeps falling over the following bars, more often than it does at arbitrary points.  
Consequence: Price crossing down through the long average starts a downtrend that persists.

**002-05_downward-cross-ends-uptrend**

Idea: After an uptrend that began with an upward cross, the short moving average crosses back below the long moving average, and price then falls over the following bars.  
Consequence: A downward cross marks the end of the preceding uptrend and price turns down.

**002-06_upward-cross-ends-downtrend**

Idea: After a downtrend that began with a downward cross, the short moving average crosses back above the long moving average, and price then rises over the following bars.  
Consequence: An upward cross marks the end of the preceding downtrend and price turns up.

## 003_thin-volume-moves-revert

### opus (call 3: 6 ideas, 1 attempt(s), 0.0369 USD)

**003-01_low-volume-rise-reverts**

Idea: After a sharp rise made on unusually low volume, price falls back over the following bars and gives back part of the rise.  
Consequence: Thin-volume moves carry little information, so returning liquidity providers lean against the stretched price and it drifts back.

**003-02_low-volume-fall-reverts**

Idea: After a sharp fall made on unusually low volume, price rises over the following bars and recovers part of the fall.  
Consequence: Thin-volume moves carry little information, so returning liquidity providers lean against the stretched price and it drifts back.

**003-03_high-volume-rise-continues**

Idea: After a sharp rise made on unusually high volume, price keeps rising over the following bars.  
Consequence: Heavy-volume moves reflect real news or broad repositioning, which slower traders, scheduled rebalancers and trend followers keep adding to.

**003-04_high-volume-fall-continues**

Idea: After a sharp fall made on unusually high volume, price keeps falling over the following bars.  
Consequence: Heavy-volume moves reflect real news or broad repositioning, which slower traders, scheduled rebalancers and trend followers keep adding to.

**003-05_rise-holding-differs-by-volume**

Idea: After sharp rises of similar size, the ones made on low volume give back a larger share of the rise than the ones made on high volume.  
Consequence: Later price behaviour after a sharp move differs by volume, with low-volume moves holding worse than high-volume ones.

**003-06_fall-holding-differs-by-volume**

Idea: After sharp falls of similar size, the ones made on low volume recover a larger share of the fall than the ones made on high volume.  
Consequence: Later price behaviour after a sharp move differs by volume, with low-volume moves holding worse than high-volume ones.

### sonnet (call 3: 6 ideas, 1 attempt(s), 0.0156 USD)

**003-01_low-volume-up-move-reverts**

Idea: After a sharp upward move on unusually low volume, price falls back over the following bars, giving back part of the move.  
Consequence: Low-volume moves are partly given back once liquidity providers return, so an upward thin-volume spike reverts downward.

**003-02_low-volume-down-move-reverts**

Idea: After a sharp downward move on unusually low volume, price rises back over the following bars, recovering part of the drop.  
Consequence: Low-volume moves are partly given back once liquidity providers return, so a downward thin-volume drop reverts upward.

**003-03_high-volume-up-move-continues**

Idea: After a sharp upward move on unusually high volume, price holds the gain or keeps rising over the following bars.  
Consequence: High-volume moves reflect broad participation and are absorbed slowly, so an upward heavy-volume move holds or continues.

**003-04_high-volume-down-move-continues**

Idea: After a sharp downward move on unusually high volume, price holds the loss or keeps falling over the following bars.  
Consequence: High-volume moves reflect broad participation and are absorbed slowly, so a downward heavy-volume move holds or continues.

**003-05_volume-splits-reversal-from-continuation**

Idea: Among sharp moves of similar size, those on unusually low volume are followed by a price change in the opposite direction of the move, while those on unusually high volume are followed by a price change in the same direction as the move.  
Consequence: Later price behaviour differs by volume: low-volume moves revert and high-volume moves persist.

**003-06_quiet-hours-moves-revert**

Idea: Sharp moves that occur during quiet periods such as weekends or overnight hours, when volume is thin, are followed by price moving back against the move.  
Consequence: Moves made while market makers are away carry little information and revert when liquidity returns.

## 004_bitcoin-leads-altcoins-lagged-response

### opus (call 4: 7 ideas, 2 attempt(s), 0.1102 USD)

**004-01_btc-rise-alts-follow-later**

Idea: After bitcoin makes a sharp rise, smaller and less traded coins keep rising over the following bars, drifting up toward the level the bitcoin move implies.  
Consequence: Altcoins take on part of a sharp bitcoin rise only later, through a delayed upward drift.

**004-02_btc-fall-alts-follow-later**

Idea: After bitcoin makes a sharp fall, smaller and less traded coins keep falling over the following bars, drifting down toward the level the bitcoin move implies.  
Consequence: Altcoins take on part of a sharp bitcoin fall only later, through a delayed downward drift.

**004-03_alt-shortfall-closes-after-rise**

Idea: When an altcoin rises less than bitcoin during a sharp bitcoin rise, it gains more than usual over the following bars, closing part of the gap to bitcoin's move.  
Consequence: Altcoin prices drift toward the level implied by a bitcoin rise, so an altcoin's shortfall gets closed afterwards.

**004-04_alt-shortfall-closes-after-fall**

Idea: When an altcoin falls less than bitcoin during a sharp bitcoin fall, it loses more than usual over the following bars, closing part of the gap to bitcoin's move.  
Consequence: Altcoin prices drift toward the level implied by a bitcoin fall, so an altcoin's shortfall gets closed afterwards.

**004-05_low-volume-alts-lag-more**

Idea: After a sharp bitcoin move, low-volume altcoins make a larger share of their bitcoin-direction move in the following bars than high-volume altcoins do.  
Consequence: The lag behind bitcoin is larger for coins with lower volume, whose thin books and fewer market makers reprice slowly.

**004-06_wide-range-alts-lag-more**

Idea: After a sharp bitcoin move, altcoins with wide bar ranges make a larger share of their bitcoin-direction move in the following bars than altcoins with narrow ranges.  
Consequence: The lag behind bitcoin is larger for coins with wider ranges, where spreads widen and arbitrage costs more.

**004-07_btc-leads-alts-more-strongly**

Idea: Bitcoin's moves are followed by same-direction altcoin moves in later bars more strongly than altcoin moves are followed by same-direction bitcoin moves.  
Consequence: Information reaches bitcoin first, so bitcoin leads small coins more than small coins lead bitcoin.

### sonnet (call 4: 0 ideas, 3 attempt(s), 0.0537 USD, NOTHING SAVED)

(no valid answer after three attempts: short-names of six words)

## 005_rsi-divergence-predicts-reversal

### opus (call 5: 6 ideas, 1 attempt(s), 0.0458 USD)

**005-01_bearish-divergence-reversal-down**

Idea: After price makes a new high on BTC, ETH or BNB while RSI makes a lower high than at the previous price high, price falls back over the following bars and gives back part of the rise.  
Consequence: Weaker momentum behind a new high means buyers are running out, so the high is followed by a reversal down.

**005-02_bullish-divergence-reversal-up**

Idea: After price makes a new low on BTC, ETH or BNB while RSI makes a higher low than at the previous price low, price rises over the following bars and recovers part of the fall.  
Consequence: Weaker momentum behind a new low means sellers are running out, so the low is followed by a reversal up.

**005-03_divergent-highs-underperform-confirmed**

Idea: On BTC, ETH or BNB, new price highs reached with a lower RSI high are followed by weaker returns than new price highs reached with a higher RSI high.  
Consequence: Fading momentum behind a new high carries information beyond the new high itself, pointing to exhaustion.

**005-04_divergent-lows-outperform-confirmed**

Idea: On BTC, ETH or BNB, new price lows reached with a higher RSI low are followed by stronger returns than new price lows reached with a lower RSI low.  
Consequence: Fading momentum behind a new low carries information beyond the new low itself, pointing to exhaustion of sellers.

**005-05_bearish-divergence-uptrend-continues**

Idea: After price makes a new high on BTC, ETH or BNB while RSI makes a lower high, price keeps rising over the following bars as the trend grinds on.  
Consequence: A divergence at a high reflects a slower, steadier climb in a strong uptrend, not exhaustion, so the rise continues.

**005-06_bullish-divergence-downtrend-continues**

Idea: After price makes a new low on BTC, ETH or BNB while RSI makes a higher low, price keeps falling over the following bars as the trend grinds on.  
Consequence: A divergence at a low reflects a slower, steadier decline in a strong downtrend, not exhaustion, so the fall continues.

### sonnet (call 5: 6 ideas, 2 attempt(s), 0.0361 USD)

**005-01_bearish-divergence-then-decline**

Idea: After price makes a new high while RSI fails to make a new high (bearish divergence), BTC, ETH or BNB price falls over the following bars.  
Consequence: Fading momentum behind a new price high shows buyers running out, so a top reverses downward.

**005-02_bullish-divergence-then-bounce**

Idea: After price makes a new low while RSI fails to make a new low (bullish divergence), BTC, ETH or BNB price rises over the following bars.  
Consequence: Fading momentum behind a new price low shows sellers running out, so a bottom reverses upward.

**005-03_divergent-highs-underperform-confirmed-highs**

Idea: After a new price high with bearish RSI divergence, BTC, ETH or BNB price falls by more over the following bars than after a new price high where RSI also makes a new high.  
Consequence: A new high with fading momentum carries information beyond the new high itself, so it is followed by weaker returns than a confirmed high.

**005-04_divergent-lows-outperform-confirmed-lows**

Idea: After a new price low with bullish RSI divergence, BTC, ETH or BNB price rises by more over the following bars than after a new price low where RSI also makes a new low.  
Consequence: A new low with fading selling momentum carries information beyond the new low itself, so it is followed by stronger returns than a confirmed low.

**005-05_bearish-divergence-then-continuation-up**

Idea: After price makes a new high while RSI fails to make a new high, BTC, ETH or BNB price keeps rising over the following bars, as the steady climb continues.  
Consequence: Divergence at a new high reflects a slower, steadier climb rather than exhaustion, so the uptrend continues.

**005-06_bullish-divergence-then-continuation-down**

Idea: After price makes a new low while RSI fails to make a new low, BTC, ETH or BNB price keeps falling over the following bars.  
Consequence: Divergence at a new low reflects a slower, steadier decline rather than exhaustion, so the downtrend continues.
