# 7.b exercise 4: with the time rule (2026-11-15)

**Change since exercise 3** (operator, 2026-11-15): every idea states its time in real time (its horizon, the past
period of its situation), and step 3 converts it to bars (`../../common/idea_definition.md`).

**Two runs on the three inputs** (`run_1/`, `run_2/`, 1.89 USD). Every idea states its horizon in days ("over the
next 10 days", "over the next 20 days"). 002-01: the same idea three times out of five (inside the golden cross, the
higher the 20-day return, the more it rises over the next 10 days). 002-04: both runs repeat the idea already tested
(the 200-day average falling; inconclusive at 10 bars), not taken again.

**Two ideas through steps 3 to 6:**

| Idea | Step 3's horizon | Step 5 | Step 6 |
|---|---|---|---|
| 002-01 run 2 b1: inside the golden cross, the higher the 20-day return, the larger the return over the next 10 days | 10 bars (exercise 3's version: 20 bars, t 1.13) | inconclusive, t 1.69 | not profitable: Sharpe 0.85, Calmar 0.72 (original book 0.49, 0.20) |
| 002-03 run 2 b2: above the 200-day average, only while the 20-day return is positive, over the next 20 days | 20 bars | inconclusive, t 1.65 | not profitable: Sharpe 0.87, Calmar 0.74 (original book 0.68, 0.39) |

**Reading.** The time rule works: step 3 takes each idea's own horizon. 7.b's ideas are sharper and their books
better, but no idea reaches a clear answer: 7.b's own numbers came from its best cut (t 3.26 in the data, 1.69 in the
test), and each condition it adds leaves fewer cases. Not validated.
