# Exercise 3: side by side

Prompt: `system_prompt_used.md` (same as exercise 2). Code: refuses only major deviations. Briefs: `inputs/`, run 001, 002, 003, 004, 005, then 001 again, each model on its own index.

## 001_rsi-extremes-predict-next-move

### opus (call 1: 4 ideas, 1 attempt(s), 0.0182 USD; call 6: 0 ideas, 1 attempt(s), 0.0306 USD, already-indexed: 001-01_rsi-high-extreme-reversal, 001-02_rsi-low-extreme-rebound, 001-03_rsi-high-extreme-continuation, 001-04_rsi-low-extreme-continuation)

**001-01_rsi-high-extreme-reversal**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the run that pushed the index up.  
Consequence: The index predicts reversal: crowded buying pressure that pushed the reading high gets spent and price retraces.

**001-02_rsi-low-extreme-rebound**

Idea: After the relative strength index reaches a low extreme on BTC, ETH or BNB, price rebounds over the following bars, recovering part of the decline that pushed the index down.  
Consequence: The index predicts reversal: forced selling and liquidations that pushed the reading low get spent and price recovers.

**001-03_rsi-high-extreme-continuation**

Idea: After the relative strength index reaches a high extreme on BTC, ETH or BNB, price keeps rising over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged chasing extend upward runs.

**001-04_rsi-low-extreme-continuation**

Idea: After the relative strength index reaches a low extreme on BTC, ETH or BNB, price keeps falling over the following bars, more than it does after neutral readings.  
Consequence: The index predicts continuation: slow-spreading news, trend-following funds and leveraged traders extend downward runs.

### sonnet (call 1: 5 ideas, 1 attempt(s), 0.0106 USD; call 6: 5 ideas, 1 attempt(s), 0.0210 USD, already-indexed: 001-01_overbought-extreme-then-pullback, 001-02_oversold-extreme-then-rebound, 001-03_overbought-extreme-then-continuation, 001-04_oversold-extreme-then-continuation, 001-05_extreme-readings-larger-subsequent-moves)

**001-01_overbought-extreme-then-pullback**

Idea: After the relative strength index reaches a high extreme, the next period's return for BTC, ETH or BNB is negative, as part of the run is given back.  
Consequence: Reversal answer: an overbought extreme reflects crowding and overshoot, so price falls back afterwards.

**001-02_oversold-extreme-then-rebound**

Idea: After the relative strength index reaches a low extreme, the next period's return for BTC, ETH or BNB is positive, as part of the drop is recovered.  
Consequence: Reversal answer: an oversold extreme reflects forced liquidations and panic overshoot, so price rebounds afterwards.

**001-03_overbought-extreme-then-continuation**

Idea: After the relative strength index reaches a high extreme, the next period's return for BTC, ETH or BNB is positive, as the upward move continues.  
Consequence: Continuation answer: strong readings reflect slowly spreading news, trend-following buying and leveraged chasing that keep pushing price up.

**001-04_oversold-extreme-then-continuation**

Idea: After the relative strength index reaches a low extreme, the next period's return for BTC, ETH or BNB is negative, as the downward move continues.  
Consequence: Continuation answer: weak readings reflect slowly spreading news, trend-following selling and leveraged traders adding to the fall, so price keeps dropping.

**001-05_extreme-readings-larger-subsequent-moves**

Idea: Price moves following extreme relative strength index readings are larger in absolute size than moves following neutral readings for BTC, ETH or BNB, in whichever direction they go.  
Consequence: Either predictive answer: extreme readings mark states of crowding or trend pressure, so later moves differ in size from those after neutral readings.

**001-06_high-extreme-continues-upward-drift**

Idea: After the index reaches a high extreme on BTC, ETH or BNB, the return over the following bars is positive because trend-following funds and leveraged chasers keep adding exposure beyond the extreme reading.  
Consequence: Strong readings come before further moves in the same direction (continuation), seen after high extremes.

**001-07_low-extreme-continues-downward-drift**

Idea: After the index reaches a low extreme on BTC, ETH or BNB, the return over the following bars is negative because slowly spreading bad news, trend-following selling and forced leveraged exits keep pushing price lower.  
Consequence: Strong readings come before further moves in the same direction (continuation), seen after low extremes.

**001-08_high-extreme-crowding-unwind-decline**

Idea: After the index reaches a high extreme, price falls over the following bars as crowding and emotional overshooting unwind and part of the run is given back.  
Consequence: Extreme readings predict reversal, seen after high extremes.

**001-09_low-extreme-liquidation-spent-rebound**

Idea: After the index reaches a low extreme, price rises over the following bars as forced liquidations and panic selling are spent and part of the drop is recovered.  
Consequence: Extreme readings predict reversal, seen after low extremes.

**001-10_extreme-readings-bigger-following-moves**

Idea: The size of price moves over the bars following an extreme index reading, high or low, is larger than the size of moves following a neutral reading.  
Consequence: Behaviour after extreme readings differs from behaviour after neutral readings in size, so the index carries information about how far price moves next.

## 002_moving-average-cross-trend-persistence

### opus (call 2: 6 ideas, 1 attempt(s), 0.0329 USD)

**002-01_sma-upcross-upward-drift**

Idea: After a short moving average of price crosses above a long moving average, price keeps rising over the following bars more often and further than after random points.  
Consequence: An upward cross of the short average over the long average starts an uptrend that persists because late buyers extend the move.

**002-02_sma-downcross-downward-drift**

Idea: After a short moving average of price crosses below a long moving average, price keeps falling over the following bars more often and further than after random points.  
Consequence: A downward cross of the short average under the long average starts a downtrend that persists because late sellers extend the move.

**002-03_price-upcross-long-sma-drift**

Idea: After price closes above its long moving average, having been below it, price keeps rising over the following bars more often and further than after random points.  
Consequence: Price crossing up through the long average starts an uptrend that persists because late buyers extend the move.

**002-04_price-downcross-long-sma-drift**

Idea: After price closes below its long moving average, having been above it, price keeps falling over the following bars more often and further than after random points.  
Consequence: Price crossing down through the long average starts a downtrend that persists because late sellers extend the move.

**002-05_sma-up-regime-positive-drift**

Idea: Over the stretch from an upward cross of the short average over the long average until the next downward cross, price rises more often and further than over random stretches of the same length.  
Consequence: The uptrend begun by an upward cross lasts until the opposite cross ends it.

**002-06_sma-down-regime-negative-drift**

Idea: Over the stretch from a downward cross of the short average under the long average until the next upward cross, price falls more often and further than over random stretches of the same length.  
Consequence: The downtrend begun by a downward cross lasts until the opposite cross ends it.

### sonnet (call 2: 7 ideas, 1 attempt(s), 0.0151 USD)

**002-01_short-above-long-cross-uptrend**

Idea: After the short moving average crosses above the long moving average, price keeps rising over the following bars more often than it falls, so the market drifts upward.  
Consequence: An upward cross of short over long average starts an uptrend that persists.

**002-02_short-below-long-cross-downtrend**

Idea: After the short moving average crosses below the long moving average, price keeps falling over the following bars more often than it rises, so the market drifts downward.  
Consequence: A downward cross of short under long average starts a downtrend that persists.

**002-03_price-above-long-average-uptrend**

Idea: After price closes from below to above the long moving average, price keeps rising over the following bars more often than it falls.  
Consequence: Price crossing up through the long average starts an uptrend that persists.

**002-04_price-below-long-average-downtrend**

Idea: After price closes from above to below the long moving average, price keeps falling over the following bars more often than it rises.  
Consequence: Price crossing down through the long average starts a downtrend that persists.

**002-05_opposite-cross-ends-uptrend**

Idea: After an upward trend that began with an upward cross, a later downward cross of the short average under the long average is followed by price falling, so the uptrend ends and the move turns down.  
Consequence: A cross the other way marks the end of the prior uptrend.

**002-06_opposite-cross-ends-downtrend**

Idea: After a downtrend that began with a downward cross, a later upward cross of the short average over the long average is followed by price rising, so the downtrend ends and the move turns up.  
Consequence: A cross the other way marks the end of the prior downtrend.

**002-07_cross-direction-extended-move-size**

Idea: After a moving average cross, the price move in the direction of the cross extends further than after arbitrary bars, so the cross is followed by a larger net move in its direction.  
Consequence: Drift after a cross is larger in the cross direction than chance would give, because late participants extend the move.

## 003_thin-volume-moves-revert

### opus (call 3: 6 ideas, 1 attempt(s), 0.0354 USD)

**003-01_low-volume-up-move-reverts**

Idea: A sharp upward move made on unusually low volume is followed by price falling back, giving up part of the rise.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against the stretched price, so it drifts back.

**003-02_low-volume-down-move-reverts**

Idea: A sharp downward move made on unusually low volume is followed by price rebounding, recovering part of the drop.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against the stretched price, so it drifts back.

**003-03_high-volume-up-move-continues**

Idea: A sharp upward move made on unusually high volume is followed by price rising further in the same direction.  
Consequence: Heavy-volume moves reflect real news or broad repositioning, which slower traders, scheduled rebalancers and trend followers keep adding to.

**003-04_high-volume-down-move-continues**

Idea: A sharp downward move made on unusually high volume is followed by price falling further in the same direction.  
Consequence: Heavy-volume moves reflect real news or broad repositioning, which slower traders, scheduled rebalancers and trend followers keep adding to.

**003-05_up-move-retrace-by-volume**

Idea: Among sharp upward moves of similar size, those made on low volume give back a larger share of the rise afterwards than those made on high volume.  
Consequence: Later price behaviour after a move of a given size differs by its volume: thin moves revert more, heavy moves hold more.

**003-06_down-move-retrace-by-volume**

Idea: Among sharp downward moves of similar size, those made on low volume give back a larger share of the drop afterwards than those made on high volume.  
Consequence: Later price behaviour after a move of a given size differs by its volume: thin moves revert more, heavy moves hold more.

### sonnet (call 3: 5 ideas, 1 attempt(s), 0.0145 USD)

**003-01_low-volume-up-move-reverts**

Idea: After a sharp upward move on unusually low volume, price falls back over the following bars, giving up part of the rise.  
Consequence: Low-volume sharp moves are partly given back as liquidity providers lean against the stretched price (upward case).

**003-02_low-volume-down-move-reverts**

Idea: After a sharp downward move on unusually low volume, price rises back over the following bars, recovering part of the drop.  
Consequence: Low-volume sharp moves are partly given back as liquidity providers lean against the stretched price (downward case).

**003-03_high-volume-up-move-continues**

Idea: After a sharp upward move on unusually high volume, price keeps rising over the following bars, holding the gain and extending it.  
Consequence: High-volume sharp moves reflect real news or positioning change and are absorbed slowly, so they carry on (upward case).

**003-04_high-volume-down-move-continues**

Idea: After a sharp downward move on unusually high volume, price keeps falling over the following bars, holding the loss and extending it.  
Consequence: High-volume sharp moves reflect real news or positioning change and are absorbed slowly, so they carry on (downward case).

**003-05_volume-splits-follow-through-direction**

Idea: Among sharp moves of similar size, the move in its own direction that follows is larger after high-volume moves than after low-volume moves.  
Consequence: Volume at the time of the move separates later behaviour: high-volume moves hold or extend while low-volume moves revert.

## 004_bitcoin-leads-altcoins-lagged-response

### opus (call 4: 7 ideas, 1 attempt(s), 0.0472 USD)

**004-01_btc-up-move-alts-follow**

Idea: After bitcoin makes a sharp up move, smaller altcoins keep rising over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin up move only later, so they drift up after it.

**004-02_btc-down-move-alts-follow**

Idea: After bitcoin makes a sharp down move, smaller altcoins keep falling over the following bars, as if catching up to the bitcoin move.  
Consequence: Altcoins take on part of a bitcoin down move only later, so they drift down after it.

**004-03_alt-shortfall-btc-rally-closes**

Idea: When an altcoin rises less than bitcoin's sharp up move implies in the same bar, it then rises over the following bars and closes part of that shortfall.  
Consequence: Altcoin prices drift toward the level a bitcoin up move implies, so the gap left behind on the move closes later.

**004-04_alt-shortfall-btc-drop-closes**

Idea: When an altcoin falls less than bitcoin's sharp down move implies in the same bar, it then falls over the following bars and closes part of that gap.  
Consequence: Altcoin prices drift toward the level a bitcoin down move implies, so the gap left behind on the move closes later.

**004-05_btc-lead-larger-low-volume**

Idea: After a sharp bitcoin move, low-volume altcoins show a larger follow-through in the direction of the bitcoin move over the following bars than high-volume altcoins.  
Consequence: The lag is larger for coins with lower volume, because their market makers reprice more slowly.

**004-06_btc-lead-larger-wide-range**

Idea: After a sharp bitcoin move, altcoins with wide bar ranges show a larger follow-through in the direction of the bitcoin move over the following bars than altcoins with narrow ranges.  
Consequence: The lag is larger for coins with wider ranges, where spreads widen and arbitrage is costlier.

**004-07_btc-leads-alts-not-reverse**

Idea: Bitcoin's returns move later altcoin returns in the same direction more strongly than altcoin returns move later bitcoin returns.  
Consequence: Information reaches bitcoin first, so bitcoin leads small coins more than small coins lead bitcoin.

### sonnet (call 4: 7 ideas, 1 attempt(s), 0.0195 USD)

**004-01_btc-up-move-alts-follow-up**

Idea: After a sharp upward move in bitcoin, smaller altcoins post positive returns over the following bars, as they take on part of the move with a delay.  
Consequence: Altcoins follow bitcoin's sharp upward moves with a delayed move in the same direction.

**004-02_btc-down-move-alts-follow-down**

Idea: After a sharp downward move in bitcoin, smaller altcoins post negative returns over the following bars, as they take on part of the move with a delay.  
Consequence: Altcoins follow bitcoin's sharp downward moves with a delayed move in the same direction.

**004-03_btc-lagged-return-predicts-alt-return**

Idea: Bitcoin's return in one bar is positively related to an altcoin's return in the next bars, beyond what the altcoin's own past returns would suggest.  
Consequence: Bitcoin's past returns carry information about altcoins' later returns, so altcoins lag bitcoin.

**004-04_lag-larger-in-low-volume-coins**

Idea: After a sharp bitcoin move, the delayed follow-through in altcoins is larger for coins with lower trading volume than for coins with higher trading volume.  
Consequence: The lag is larger for less traded coins.

**004-05_lag-larger-in-wide-range-coins**

Idea: After a sharp bitcoin move, the delayed follow-through in altcoins is larger for coins with wider bar ranges than for coins with narrower bar ranges.  
Consequence: The lag is larger for coins with wider ranges.

**004-06_lead-runs-from-btc-to-alts**

Idea: Bitcoin's return in a bar is more strongly related to the later returns of an altcoin than that altcoin's return is related to bitcoin's later returns.  
Consequence: The lead-lag runs from large coins to small coins, not the other way.

**004-07_unmoved-alt-catches-up-more**

Idea: When an altcoin has not yet moved after a sharp bitcoin move, its later move in bitcoin's direction is larger than when it already moved with bitcoin in the same bar.  
Consequence: Altcoins that lag the most right after the bitcoin move have the most catching up left to do.

## 005_rsi-divergence-predicts-reversal

### opus (call 5: 6 ideas, 1 attempt(s), 0.0471 USD)

**005-01_bearish-rsi-divergence-reversal**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high than at the previous price high, price then falls back and retraces part of the run up to that high.  
Consequence: Fading momentum behind a new high means buyers are running out, so the advance reverses.

**005-02_bullish-rsi-divergence-rebound**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low than at the previous price low, price then rebounds and recovers part of the decline into that low.  
Consequence: Fading momentum behind a new low means sellers are running out, so the decline reverses.

**005-03_divergent-high-weaker-than-confirmed**

Idea: On BTC, ETH and BNB, returns after new price highs with a lower RSI high are weaker than returns after new price highs where RSI also makes a new high.  
Consequence: A new high reached on weaker momentum carries more exhaustion than one reached on confirming momentum.

**005-04_divergent-low-stronger-than-confirmed**

Idea: On BTC, ETH and BNB, returns after new price lows with a higher RSI low are stronger than returns after new price lows where RSI also makes a new low.  
Consequence: A new low reached on weaker downside momentum carries more seller exhaustion than one reached on confirming momentum.

**005-05_bearish-divergence-uptrend-continues**

Idea: On BTC, ETH and BNB, when price makes a new high while RSI makes a lower high, price then keeps rising to further highs.  
Consequence: The divergence reflects a slower, steadier climb with slow money still entering, so the uptrend continues.

**005-06_bullish-divergence-downtrend-continues**

Idea: On BTC, ETH and BNB, when price makes a new low while RSI makes a higher low, price then keeps falling to further lows.  
Consequence: The divergence reflects a slower, steadier decline with sellers still arriving, so the downtrend continues.

### sonnet (call 5: 7 ideas, 1 attempt(s), 0.0203 USD)

**005-01_bearish-divergence-then-decline**

Idea: When price makes a new high while RSI fails to make a new high (bearish divergence), the following return is negative, as the push is running out of buyers and holders take profit.  
Consequence: A bearish divergence at a new price high warns of a downward reversal.

**005-02_bullish-divergence-then-rebound**

Idea: When price makes a new low while RSI fails to make a new low (bullish divergence), the following return is positive, as sellers are running out and little supply remains.  
Consequence: A bullish divergence at a new price low warns of an upward reversal.

**005-03_divergent-high-weaker-than-confirmed-high**

Idea: After a new price high with a bearish divergence, the following return is lower than after a new price high where RSI also makes a new high.  
Consequence: Fading momentum behind a new high carries information beyond the new high itself, favouring reversal.

**005-04_divergent-low-stronger-than-confirmed-low**

Idea: After a new price low with a bullish divergence, the following return is higher than after a new price low where RSI also makes a new low.  
Consequence: Fading momentum behind a new low carries information beyond the new low itself, favouring reversal.

**005-05_bearish-divergence-then-continuation-up**

Idea: When price makes a new high while RSI fails to make a new high, the following return is positive, as the slower, steadier climb continues while slow money keeps entering.  
Consequence: A bearish divergence at a new high is followed by continuation upward in strong trends.

**005-06_bullish-divergence-then-continuation-down**

Idea: When price makes a new low while RSI fails to make a new low, the following return is negative, as the slower, steadier decline continues.  
Consequence: A bullish divergence at a new low is followed by continuation downward.

**005-07_divergence-high-downside-skew**

Idea: Following a bearish divergence at a new price high, the largest price move over the next bars is larger in the downward direction than the upward direction, as holders taking profit meet little demand.  
Consequence: A divergence at a new high leads to a sharper downward reversal, seen in move asymmetry.
