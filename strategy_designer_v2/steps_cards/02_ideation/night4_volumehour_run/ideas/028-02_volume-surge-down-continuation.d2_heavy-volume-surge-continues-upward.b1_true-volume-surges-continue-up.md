---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next four hours. The larger that hour's volume relative to its 30-day average and its rise relative to its typical 30-day hourly move, the larger the further rise, counted only on hours where both are far above their usual levels.
Consequence: A true heavy-volume hourly surge up is a reason to hold a long for about four hours rather than fade it, since the move it carries can exceed the cost of the trade.
Why:
- F1: The test did not measure the idea's situation, which is why its result came out unclear (-0.03 % per case, t -1.38). Its forecast is standardised against its own last 500 values, so it was positive on 49 % of all hours and at its cap of 20 on 7.6 %. That gave 11,507 cases, and even the cases at the cap averaged only 1.8 typical hourly moves on 2.6 times the usual volume. Hours that truly rise more than 2 typical 30-day moves on more than 3 times the 30-day volume give only 1,201 cases on the 6-hour grid.
- F2: On those true heavy-volume rising hours the rise carries on. The unusual move over the next 4 hours is +0.19 % (t 2.64, 1,270 cases) and over the next 6 hours +0.17 % (t 2.06, 1,201 cases). Over the next 2 hours it is only +0.03 % (t 0.64).
- F3: The carry-on after heavy-volume rising hours shows in both coins over 6 hours: BTC +0.18 % (t 1.72, 618 cases) and ETH +0.16 % (t 1.24, 583 cases).
- F5: Inside the heavy-volume rising hours, the size of the surge grades the follow-through only weakly. Over 4 hours the top third by rise times volume ratio gets +0.30 % against +0.18 % for the bottom third, but the slope's t is only 0.84. Over 6 hours the two thirds get +0.22 % and +0.20 % (slope t 0.11).
- F7: The +0.19 % 4-hour move after true heavy-volume rising hours (F2) is about 1.7 times the 0.11 % cost of a trade. The test's diluted cases moved a total of only +0.01 %, which is 0.1 times that cost.
