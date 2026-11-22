---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, the larger today's one-day rise measured in usual daily moves, the larger the coin's fall over the next 5 days.
Consequence: A short against a bounce in a falling coin should be held for several days, where the giveback is many times the cost of a trade, rather than covered after one day.
Why:
- F3: In coins with a negative 90-day return, the bounce fade lasts beyond the single day the book held. The 3-day unusual move is −1.03 % after rises of 1–2 usual moves (t −3.09, n 477) and −1.87 % after 2–3 moves (t −2.75, n 129). The 5-day unusual move is −2.38 % after 2–3 moves (t −1.64, n 70) and −7.43 % after more than 3 moves (t −3.65, n 27). These are many times the 1-day sizes the test captured: −0.66 % and −1.28 % next day, against a cost of 0.22 % per trade.
- F4: The one-day fade is graded and is opposite in the two regimes. Among up days, the next-day unusual move slopes −0.25 % per usual move in falling coins (t −3.81, n 7482) and +0.20 % per usual move in rising coins (t 4.38, n 8337). The next-day mean after rises above 2 moves runs from −1.62 % (t −2.45) in the lowest 30-day-return quintile to +0.68 % in the highest.
- F6: The tested book earned nothing, −0.004 % a day on average, with window means scattered from −0.116 % to +0.088 % a day. Its 1-day total move per case of +0.19 % is below the 0.22 % cost of a trade.
