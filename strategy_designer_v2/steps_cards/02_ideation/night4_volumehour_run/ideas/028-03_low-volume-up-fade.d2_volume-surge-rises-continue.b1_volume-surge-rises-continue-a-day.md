---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The higher that hour's volume against its 30-day average, the larger the further rise.
Consequence: A sharp hourly rise on a volume surge is a reason to hold a long for a day rather than six hours, and never to fade it, while a sharp rise on ordinary volume gives no edge.
Why:
- F1: The tested forecast does not single out real surges, so its 8827 cases are mostly ordinary hours: bars with the smallest long forecast (0 to 1, n = 18630) show a 6-hour unusual move of −3.22 bp (t −2.27), and bars with the strongest forecast (10 to 20, n = 6165) show +0.11 bp (t 0.03), which is why the main measure sits at +0.36 bp with t 0.14.
- F2: Hours that actually match the idea's situation do continue, and the volume surge is what separates them: up hours of at least 3 thirty-day standard deviations on at least 1.5 times the 30-day mean volume are followed by a 24-hour unusual move of +61.56 bp (t 3.41, 829 independent cases, strength 0.147), while the same rises on ordinary volume give +6.47 bp (t 0.13, 65 cases, strength 0.002).
- F3: The continuation shows over a day rather than over the plan's six hours: up hours of at least 2.5 standard deviations on at least 3 times the mean volume give +21.74 bp at 6 hours (t 2.30, n 964, strength 0.109), +24.94 bp at 12 hours (t 1.90) and +59.57 bp at 24 hours (t 3.27, n 792, strength 0.142); for rises of at least 3 standard deviations the figures are +20.15 bp (t 1.82) at 6 hours and +72.58 bp (t 3.47, strength 0.178) at 24 hours.
- F4: The move is graded by volume, as the idea says: among up hours of at least 2.5 standard deviations, the Spearman correlation of the log volume ratio with the 24-hour unusual move is 0.063 (p 0.022, n 1318), and the volume quartiles from lowest to highest give −4.77, +27.70, +65.42 and +69.59 bp. The size of the rise itself grades the move less: its correlation is 0.040 (p 0.15).
- F6: At 24 hours the unusual move of surging rises, about 0.60 % to 0.73 % per case (F2, F3), is 5 to 7 times the 0.11 % cost of a trade. At the plan's six hours it is 0.20 % to 0.22 %, about 2 times the cost. As tested, the move was 0.0 times the cost.
