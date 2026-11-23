---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: At the 16:00 UTC settlement, a coin's 24-hour return continues over the next 8 hours. The larger the 24-hour rise against the coin's usual 24-hour move, the larger the further rise.
Consequence: A trader holds with the day's trend through the US afternoon, sized by its strength, rather than fading it.
Why:
- F3: At the 16:00 close the 24-hour move continues over the next 8 hours, and mostly at the extreme. The top quintile of the scaled 24-hour return (z24 +1.90) is followed by +33.8 bp (strength +0.119); the middle quintiles give −1.9 to −0.2 bp; the bottom quintile gives +8.4 bp (about 3,170 cases each). The 24-hour continuation product is positive at closes 15–18 (t 1.6, 3.25, 2.14, 2.36). It is positive in all 6 coins (t 0.7 to 1.9) and in 7 of 8 years.
- F4: During the Asian and European night the 24-hour move reverses instead. The 24-hour continuation product over 8 hours is negative at every close from 00:00 to 09:00 UTC, with t −2.1 to −5.0 (about 15,700 cases each hour). This is the opposite sign to the 15–18 UTC afternoon in F3.
- F7: Volume concentrates around the afternoon UTC hours, as the brief expects. The median volume against its 720-bar median is 1.49–1.53 at closes 15–17 and 1.14 at 01:00, against 0.67–0.83 at closes 04–12.
