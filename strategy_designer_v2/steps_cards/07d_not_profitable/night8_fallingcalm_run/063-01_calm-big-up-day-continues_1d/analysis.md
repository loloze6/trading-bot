---
line: 7.d confirmed, not profitable
backtest: 063-01_calm-big-up-day-continues_1d
idea tested: 063-01_calm-big-up-day-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3671 USD
---
## Findings
- **F1:** The check failed on Calmar, 0.309 against 0.75: a yearly return of +16.2 % against a deepest fall of about 47 % (−46.9 % on folds B and C, reached in w14 and w15). The long-only book gives back its gains in windows where the coins fall: w14 book −33 % (coins −52 %), w7 −22 % (coins −54 %), w9 −11 % (coins −31 %).
- **F2:** The losses sit on bars held while the coin's 20-day return was below −10 %. Those 1,027 held bars lost a mean −0.21 % per bar, against +0.41 % and +0.42 % on the 862 and 1,249 held bars with a 20-day return of 0 to +10 % and above +10 %. In the worst windows w13 to w15, the 322 held bars in a 20-day fall lost −0.52 % per bar, and those losses came from LTC (−58 % summed) and ZEC (−43 %).
- **F3:** The continuation lives only when the coin's recent path already points up. In calm grid cases with a rise above 1 usual swing, the 5-day excess return was +4.7 % (t 2.34, 37 cases) and +9.0 % (t 1.99, 20 cases) when the 20-day return was above +10 %. It was +0.1 % (14 cases) and −4.3 % (11 cases) when the 20-day return was below 0.
- **F4:** The 10-day return shows the same split for any calm up day. Calm up days with a 10-day return above +5 % were followed by a 5-day excess return of +3.6 % (t 3.80, 151 cases), and those with 0 to +5 % by +1.9 % (t 1.44, 72 cases). Up days with a negative 10-day return were followed by −0.7 % (t −0.64, 84 cases) and −1.1 % (t −0.95, 57 cases).
- **F5:** The recent rise is not an effect of its own. Calm days without a rise (one-day move ≤ 0) but with a 20-day return of 0 to +10 % or above +10 % were followed by a 5-day excess return of −1.0 % (96 cases) and −0.6 % (104 cases). With an up day above 1 swing it was +3.9 % to +9.0 %, so the condition adds nothing without the idea's signal.
- **F6:** Keeping the book's per-bar gains only on bars with a positive 20-day return changes the failing measure on folds B and C. The deepest fall goes from −47.0 % to −20.5 %, the yearly return from +30.5 % to +39.7 %, Calmar from 0.65 to 1.93 and Sharpe from 0.90 to 1.38 (a rebuild from bar values, not the engine's book).
- **F7:** The effect is graded inside the calm market, so its information lies in the large days. Calm 5-day excess returns rise with the swing-scaled day: −3.6 % below −2 swings, +0.7 % at 0 to 0.5, +2.4 % (t 1.98, 76 cases) at 1 to 2, and +6.8 % (t 2.08, 28 cases) above 2. Trades entered at forecasts of 16.7 to 20 netted +5.2 % against +1.0 % at 10 to 16.7. The size measure's +0.01 % per case is diluted by the many small up days.
- **F8:** On a 60-day trend, the calm big-day continuation is absent in falling markets. The excess return was +0.4 % (20 cases) when the 60-day return was below −10 %, against +5.1 % (t 1.87, 36 cases) in rising and +8.2 % (t 2.47, 18 cases) in choppy markets. The 60-day return was available on 64 % of calm cases.

## Ideas
- `063-01.d1_calm-big-up-day-uptrend` (from F1, F2, F3, F4, F5, F6): In a calm market, the larger a coin's one-day rise against its usual daily swing (the standard deviation of its daily returns over the past 30 days), the larger its rise over the next 5 days, only while its 10-day return is positive, and the more so the larger that 10-day return.
- `063-01.d2_rising-calm-big-day` (from F1, F2, F7, F8): In a rising, calm market, the larger a coin's one-day rise against its usual daily swing (the standard deviation of its daily returns over the past 30 days), the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
