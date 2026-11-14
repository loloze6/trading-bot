# Exercise 1: side by side

Same prompt (`system_prompt_used.md`), same five briefs (`inputs/`), each model on its own index, briefs in order.

## 001_rsi-extremes-predict-next-move

### opus  (0.0338 USD, 1 attempt(s))

**001-01_rsi-high-extreme-next-move**

Idea: After the relative strength index reaches an extreme high reading on BTC, ETH or BNB, the next price move differs in direction from the move after neutral readings. Either price gives back part of the run (reversal) or keeps rising (continuation); the data will say which.  
Consequence: Extreme high readings carry information about the next move beyond what neutral readings show, as reversal or as continuation.

**001-02_rsi-low-extreme-next-move**

Idea: After the relative strength index reaches an extreme low reading on BTC, ETH or BNB, the next price move differs in direction from the move after neutral readings. Either price bounces back up (reversal) or keeps falling (continuation); the data will say which.  
Consequence: Extreme low readings carry information about the next move beyond what neutral readings show, as reversal or as continuation.

**001-03_rsi-extreme-next-move-size**

Idea: On BTC, ETH and BNB, price moves that follow extreme relative strength index readings differ in size from moves that follow neutral readings. They are either larger, as further pressure or a give-back unfolds, or smaller, as the pressure is spent.  
Consequence: The size of later moves after extreme readings differs from the size after neutral readings, so the index says something about what comes next.

### sonnet  (0.0179 USD, 1 attempt(s))

**001-01_high-extreme-direction-shift**

Idea: After the index reaches a high extreme following a one-sided rise, the next price move in BTC, ETH or BNB has a direction that differs from the move after neutral readings. Price either gives back part of the run or extends it, and the data will show which.  
Consequence: Overbought readings carry information about the direction of the next move, either reversal or continuation.

**001-02_low-extreme-direction-shift**

Idea: After the index reaches a low extreme following a one-sided fall, the next price move in BTC, ETH or BNB has a direction that differs from the move after neutral readings. Price either rebounds from the run or keeps falling in its direction, and the data will show which.  
Consequence: Oversold readings carry information about the direction of the next move, either reversal or continuation.

**001-03_extreme-readings-move-size-shift**

Idea: After extreme readings in either direction, the size of the next price move (the distance travelled over the following bars) is visibly different from the size after neutral readings. Crowding unwinds and trend-chasing both produce larger or smaller moves than a quiet, balanced market.  
Consequence: Extreme readings carry information about the size of the next move, not only its direction.

## 002_moving-average-cross-trend-persistence

### opus  (0.0398 USD, 1 attempt(s))

**002-01_ma-cross-up-continuation**

Idea: After the short moving average of price crosses above the long moving average, price rises over the following bars more often than it does after random points.  
Consequence: An upward cross of the averages starts an uptrend that persists, because late buyers keep extending the move.

**002-02_ma-cross-down-continuation**

Idea: After the short moving average of price crosses below the long moving average, price falls over the following bars more often than it does after random points.  
Consequence: A downward cross of the averages starts a downtrend that persists, because late sellers keep extending the move.

**002-03_price-cross-long-ma-up**

Idea: After price itself closes above the long moving average, having been below it, price rises over the following bars more often than it does after random points.  
Consequence: Price crossing up through the long average starts an uptrend that persists.

**002-04_price-cross-long-ma-down**

Idea: After price itself closes below the long moving average, having been above it, price falls over the following bars more often than it does after random points.  
Consequence: Price crossing down through the long average starts a downtrend that persists.

**002-05_ma-cross-move-size**

Idea: After a cross of the short moving average over the long one, the move that follows goes further in the direction of the cross than the moves after random points, or it tends to reverse instead.  
Consequence: The new trend after an averages cross extends further than chance, rather than marking exhaustion.

**002-06_price-cross-ma-move-size**

Idea: After price crosses the long moving average, the move that follows goes further in the direction of the cross than the moves after random points, or it tends to reverse instead.  
Consequence: The new trend after price crosses the long average extends further than chance, rather than marking exhaustion.

**002-07_cross-to-opposite-cross-drift**

Idea: From one cross of the averages to the next cross the other way, price ends up moved in the direction of the first cross more often than chance would give.  
Consequence: The trend begun by a cross persists until the opposite cross ends it.

### sonnet  (0.0424 USD, 3 attempt(s), NOTHING SAVED)

(no valid answer after three attempts: each short-name had six words)

## 003_thin-volume-moves-revert

### opus  (0.0430 USD, 1 attempt(s))

**003-01_low-volume-sharp-move-reverts**

Idea: After a sharp price move in a single bar that comes on unusually low volume, price over the following bars moves back against the move and gives back part of it.  
Consequence: Thin-volume moves carry little information, and returning liquidity providers lean against them, so price drifts back.

**003-02_high-volume-sharp-move-holds**

Idea: After a sharp price move in a single bar that comes on unusually high volume, price over the following bars stays near where the move ended or keeps going in the same direction.  
Consequence: Heavy-volume moves reflect real news or a broad change in positioning, absorbed slowly as later traders add in the same direction.

**003-03_move-follow-through-by-volume**

Idea: Among sharp moves of similar size, the later price change in the move's direction is larger after moves on high volume than after moves on low volume, which are followed by more give-back.  
Consequence: Later price behaviour after equal-size moves differs by volume, with high-volume moves holding better than low-volume ones.

**003-04_high-volume-move-delayed-drift**

Idea: After a sharp move on unusually high volume, the drift in the move's direction is spread over several later bars rather than ending on the next bar.  
Consequence: Heavy-volume moves are absorbed slowly, as slower traders, scheduled rebalancers and trend followers keep adding after the first burst.

**003-05_weekend-sharp-move-reverts**

Idea: Sharp moves that happen on weekend bars, when volume is thin, are partly given back on the following bars more than sharp moves of similar size on weekday bars.  
Consequence: Moves made while market makers are away, such as on weekends, revert once liquidity returns.

### sonnet  (0.0240 USD, 2 attempt(s))

**003-01_low-volume-move-partial-reversal**

Idea: After a sharp price move on unusually low volume, price afterward retraces part of that move back toward where it started.  
Consequence: Low-volume sharp moves carry little information and are partly given back once liquidity providers return.

**003-02_high-volume-move-holds-continues**

Idea: After a sharp price move on unusually high volume, price afterward holds the move or keeps going in the same direction.  
Consequence: High-volume sharp moves reflect real news or positioning change and are absorbed slowly, so they hold or continue.

**003-03_volume-separates-reversal-from-continuation**

Idea: Among sharp moves of similar size, those on unusually low volume are followed by price movement back against the move, while those on unusually high volume are followed by movement in the move's direction, so later drift differs in sign by volume.  
Consequence: Volume at the time of a move of given size separates later reversal from later follow-through.

**003-04_thin-hours-low-volume-reversal**

Idea: Sharp low-volume moves that happen in thin-liquidity periods such as quiet hours or weekends are retraced afterward more than sharp moves of similar size and low volume in busy periods.  
Consequence: Moves that come from market makers being temporarily absent are the ones that revert, as liquidity providers return.

## 004_bitcoin-leads-altcoins-lagged-response

### opus  (0.0359 USD, 1 attempt(s))

**004-01_btc-sharp-move-alt-follow**

Idea: After a sharp bitcoin move, smaller coins keep moving in the same direction over the following bars, beyond what their own earlier returns would predict.  
Consequence: Altcoins take on part of bitcoin's move only later, so their returns follow bitcoin's earlier returns.

**004-02_alt-lag-larger-low-volume**

Idea: After a sharp bitcoin move, the share of the move that altcoins take on later is larger for coins with lower volume than for heavily traded coins.  
Consequence: The lag is larger where market makers are fewer and arbitrage is costlier, i.e. on thinly traded coins.

**004-03_alt-lag-larger-wide-range**

Idea: After a sharp bitcoin move, the delayed follow-through is larger for coins with wider bar ranges than for coins with narrow ranges.  
Consequence: The lag is larger for coins with wider ranges, where quotes are wide and repricing is slow.

**004-04_btc-leads-alts-asymmetry**

Idea: Bitcoin's earlier returns line up with later altcoin returns more strongly than altcoins' earlier returns line up with later bitcoin returns.  
Consequence: Information reaches bitcoin first, so bitcoin leads small coins more often than they lead it.

**004-05_alt-gap-closes-toward-btc**

Idea: When an altcoin has lagged behind a sharp bitcoin move, it closes the gap toward the level the bitcoin move implies over the following bars, rather than the gap widening.  
Consequence: Altcoin prices drift toward the level implied by the bitcoin move.

### sonnet  (0.0473 USD, 3 attempt(s))

**004-01_btc-move-leads-altcoin-follow**

Idea: After a sharp bitcoin move over a short window, the returns of smaller coins over the following bars point in the same direction as that move, even after accounting for those coins' own past returns.  
Consequence: Bitcoin's earlier returns carry information about altcoins' later returns, which is the delayed pass-through of the move.

**004-02_thin-coins-lag-more**

Idea: After a sharp bitcoin move, the less traded coins (lower volume) take on more of the move in the following bars than the most traded coins do, so their catch-up is larger and slower.  
Consequence: The lag is larger for thinly traded coins because their market makers update quotes later and arbitrage is costlier.

**004-03_wide-range-coins-lag-more**

Idea: After a sharp bitcoin move, coins with wider bar ranges take on more of the move in the following bars than coins with narrow ranges.  
Consequence: The lag is larger for coins with wider ranges, which reflect wider spreads and slower repricing.

**004-04_btc-leads-more-than-follows**

Idea: Bitcoin's returns predict altcoins' later returns more strongly than altcoins' returns predict bitcoin's later returns; the lead runs from bitcoin to small coins more often than the reverse.  
Consequence: Information reaches the market through the most liquid coin first, so the lead-lag is asymmetric.

**004-05_altcoin-gap-to-btc-closes**

Idea: After a sharp bitcoin move, the gap between an altcoin's price and the level implied by bitcoin's move narrows over the following bars, as the altcoin moves toward that level.  
Consequence: Altcoin prices drift toward the level implied by the bitcoin move as quotes and arbitrage catch up.

**004-06_altcoin-response-delayed-after-btc**

Idea: After bitcoin moves sharply, altcoins show little immediate reaction in the same bar and a larger share of their response in the later bars.  
Consequence: Altcoins take on part of bitcoin's move only later, instead of right away.

## 005_rsi-divergence-predicts-reversal

### opus  (0.0434 USD, 1 attempt(s))

**005-01_bearish-divergence-next-move**

Idea: On BTC, ETH and BNB, after price makes a new high while RSI makes a lower high, the next move differs in direction from the move after new highs where RSI also makes a new high. It either turns down more often or keeps rising more often.  
Consequence: Fading buying momentum behind a new high carries information about the next move, toward reversal or toward continuation.

**005-02_bullish-divergence-next-move**

Idea: On BTC, ETH and BNB, after price makes a new low while RSI makes a higher low, the next move differs in direction from the move after new lows where RSI also makes a new low. It either bounces more often or keeps falling more often.  
Consequence: Fading selling momentum behind a new low carries information about the next move, toward reversal or toward continuation.

**005-03_divergence-next-move-size**

Idea: On BTC, ETH and BNB, the size of the price move after a new extreme with RSI divergence differs from the size of the move after a new extreme without divergence.  
Consequence: Exhaustion behind a new extreme changes how far price travels afterward, through a larger reversal or a steadier grind.

**005-04_divergence-trend-extension-rate**

Idea: On BTC, ETH and BNB, after a new extreme with RSI divergence, price goes on to set a further extreme in the same direction at a different rate than after a new extreme without divergence. It either stalls short of the extreme more often or extends past it more often.  
Consequence: Momentum running out of fuel shows as a trend that stops extending, while a slow steady grind shows as a trend that keeps extending.

### sonnet  (0.0167 USD, 1 attempt(s))

**005-01_bearish-divergence-direction-shift**

Idea: After price makes a new high while RSI fails to make a matching new high (bearish divergence), the following price moves differ in direction from the moves after new highs where RSI confirms, as reversal downward or as continuation upward. The data says which.  
Consequence: Fading momentum behind a new price high carries information about the next direction that confirmed highs do not.

**005-02_bullish-divergence-direction-shift**

Idea: After price makes a new low while RSI fails to make a matching new low (bullish divergence), the following price moves differ in direction from the moves after new lows where RSI confirms, as rebound upward or as continuation downward.  
Consequence: Fading selling momentum behind a new price low carries information about the next direction that confirmed lows do not.

**005-03_divergence-move-size-shift**

Idea: Price moves following divergences are of a different size than moves following new extremes without divergence, with larger swings if exhaustion releases a reversal or smaller drift if momentum simply cooled in a slow grind.  
Consequence: Divergence marks a different state of buyer and seller participation, which changes how far price moves next, not only its direction.

**005-04_divergence-in-strong-trend-contrast**

Idea: When a divergence appears during a strong, sustained trend, the following moves differ from those after a divergence in a sideways or weak trend, as reversal in one case and continued grinding in the other.  
Consequence: Whether cooling momentum means exhaustion or just a slower steady climb depends on the trend in which the divergence appears.

**005-05_repeated-divergence-outcome-shift**

Idea: Divergences that persist across repeated new price extremes, with RSI weakening further each time, are followed by a different outcome than a single divergence, as a stronger reversal or as continued trend.  
Consequence: Repeated fading momentum behind successive extremes shows more or less remaining fuel than a single fade, changing the odds of reversal.
