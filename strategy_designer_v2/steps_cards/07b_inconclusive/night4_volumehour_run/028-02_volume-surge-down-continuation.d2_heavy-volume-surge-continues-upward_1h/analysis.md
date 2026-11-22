---
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
idea tested: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4058 USD
---
## Findings
- **F1:** The test did not measure the idea's situation, which is why its result came out unclear (-0.03 % per case, t -1.38). Its forecast is standardised against its own last 500 values, so it was positive on 49 % of all hours and at its cap of 20 on 7.6 %. That gave 11,507 cases, and even the cases at the cap averaged only 1.8 typical hourly moves on 2.6 times the usual volume. Hours that truly rise more than 2 typical 30-day moves on more than 3 times the 30-day volume give only 1,201 cases on the 6-hour grid.
- **F2:** On those true heavy-volume rising hours the rise carries on. The unusual move over the next 4 hours is +0.19 % (t 2.64, 1,270 cases) and over the next 6 hours +0.17 % (t 2.06, 1,201 cases). Over the next 2 hours it is only +0.03 % (t 0.64).
- **F3:** The carry-on after heavy-volume rising hours shows in both coins over 6 hours: BTC +0.18 % (t 1.72, 618 cases) and ETH +0.16 % (t 1.24, 583 cases).
- **F4:** Large rising hours on thin volume (below 1.5 times the 30-day average) do the opposite and fade, as the brief says. Their unusual move is -0.12 % over 2 hours (t -2.16, 677 cases), -0.15 % over 4 hours (t -2.08) and -0.15 % over 6 hours (t -1.65). The fade is strongest in BTC (-0.23 % over 6 hours, t -2.05).
- **F5:** Inside the heavy-volume rising hours, the size of the surge grades the follow-through only weakly. Over 4 hours the top third by rise times volume ratio gets +0.30 % against +0.18 % for the bottom third, but the slope's t is only 0.84. Over 6 hours the two thirds get +0.22 % and +0.20 % (slope t 0.11).
- **F6:** Heavy-volume falling hours are followed by a 2-hour rebound of +0.16 % (t 2.50, 1,494 cases), not by continuation. The rebound is unstable by year: +0.46 % in 2018 and +0.64 % in 2021, but -0.35 % in 2022 (t -2.16) and -0.12 % in 2025.
- **F7:** The +0.19 % 4-hour move after true heavy-volume rising hours (F2) is about 1.7 times the 0.11 % cost of a trade. The test's diluted cases moved a total of only +0.01 %, which is 0.1 times that cost.

## Ideas
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up` (from F1, F2, F3, F5, F7): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next four hours. The larger that hour's volume relative to its 30-day average and its rise relative to its typical 30-day hourly move, the larger the further rise, counted only on hours where both are far above their usual levels.
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back` (from F4): After an hour in which the coin rises far more than its typical hourly move over the past 30 days on volume at or below its 30-day average, the price falls back over the next four hours, and the larger that hour's rise relative to its typical 30-day hourly move, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
