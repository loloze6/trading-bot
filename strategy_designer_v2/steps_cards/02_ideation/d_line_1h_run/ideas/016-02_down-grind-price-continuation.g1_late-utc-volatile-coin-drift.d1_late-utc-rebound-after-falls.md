---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours from 21:00 to 23:00 UTC, and the higher its hourly volatility over the past 7 days, the larger that rise, the more so the further the coin fell over the past 24 hours.
Consequence: A trader would hold the late-UTC slot mainly on volatile days after a sharp 24-hour fall, where the expected rise is large enough to clear a round-trip fee, and skip the ordinary days whose drift is smaller than the cost.
Why:
- F1: Fees, not the forecast, sink the book: summed over all coins and windows, the position's gains before costs come to 7.77 while fees come to 18.24, about 0.00044 against 0.00104 per coin-day. That leaves a mean daily book return of -0.000596 (sd 0.0067), which is where the failing Sharpe of -2.1 comes from.
- F2: The slot effect itself is real but too small for its cost. The return from the 21:00 to the 23:00 close averages 0.101 % (t 9.07, 16,256 independent days), and every coin is positive with t between 3.1 and 4.7. Yet the fee per unit of turnover is 0.075 % to 0.125 %, so a daily in-and-out round trip costs 0.15 % to 0.25 % of the position, more than the 0.10 % it earns.
- F4: The slot gain is concentrated in the most volatile week. In the top quintile of raw 7-day hourly volatility (mean 1.70 % per hour) the 2-hour slot return is 0.250 %, against 0.04 % to 0.10 % in the four lower quintiles. The book's sizing by standardised volatility spreads its position much more evenly: mean position 0.33 in the lowest forecast quintile against 0.65 in the highest.
- F5: The slot gain is largest after a fall. When the coin's 24-hour return into 21:00 is in its lowest quintile (mean -5.95 %), the slot return is 0.229 %, against 0.071 % to 0.074 % in the middle quintiles. The lowest quintile of the 7-day return (mean -15.3 %) also gives 0.132 %, against 0.076 % in the middle.
