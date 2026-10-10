## Your lens: trade efficiency

How does this strategy turn a forecast into lots, and which lots do worse than the others: by
exit cause (flip, reduction, end of window), holding length, side, entry forecast, the move
before entry? The "why" here is usually mechanical: name the pipeline rule (the target
allocation is the forecast divided by 10; a rebalance happens on every allocation change at or
above the band; lots are closed last-in-first-out) and predict a second query it implies. Your
claims are strategy claims, measured on trades (CLAIM_TESTS_TRADE.md) and confirmed on the same
strategy run on a fold you have not seen (`vehicle: []`, kind `execution_behaviour`), or on a
variant that changes the rule (a config change). Exit fields describe what happened; a vehicle
may only act on what was known at entry.
