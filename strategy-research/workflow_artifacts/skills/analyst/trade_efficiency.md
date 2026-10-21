## Your lens: trade efficiency

How does this strategy turn a forecast into lots, and which lots do worse than the others: by
exit cause (flip, reduction, end of window), holding length, side, entry forecast, the move
before entry? The "why" here is usually mechanical: name the pipeline rule (the target
allocation is the forecast divided by 10; a rebalance happens on every allocation change at or
above the band; lots are closed last-in-first-out) and predict a second query it implies. Your
claims are strategy claims, measured on trades (CLAIM_TESTS_TRADE.md) and confirmed by the
child run of a variant that changes the rule (a config change, its vehicle) on a fold you
have not seen. The pipeline rule itself is not a vehicle; the vehicle changes the forecast the
rule acts on (for example a smoothing span that cuts sign flips). Exit fields describe what
happened; a vehicle may only act on what was known at entry.

Profit and cost are measurements of this run: cost share, fees and net are evidence,
never the claim. A cost claim names the cause of the weak gross edge (the edge lasts one
bar, the forecast changes sign on most bars, the forecast is large when the move is small,
the signal predicts only the next bar); its test tests that cause; its vehicle changes that
cause. Read `window_economics` first: it gives, per window and
coin, the trades, the turnover, the direction changes, the allocation, gross, fees, net and
cost drag, so the cause is named from a measurement. Read the cost in this order: first fees
as a percent of the account (per window and per year), then gross per lot against fees per
lot, then turnover; fees over the absolute gross is never the first figure. A gross result
near zero with small fees is a signal finding, and no cost claim follows from it.
