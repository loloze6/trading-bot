---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close sits just below prices where the coin turned up several times in the past 90 days -> adapted: "just below" and "several times" become graded. The measure counts the 90-day swing lows clustered at the nearest level above the close, weighted by how close the price sits under that level.
- Comparison: the more such turning-up lows just above the close, the larger the fall -> kept: the forecast's size grows with the count of lows at the level.
- Outcome: the price falls over the next 10 days, only while the coin has not already lost a large share of its value over the past 90 days -> kept: 10-bar short holding, with the no-collapse condition set as a regime on the 90-bar return (a 50 % loss, by convention).
- Verdict transfer: yes: the config shorts in proportion to the clustered support just above the close, only while the coin has not collapsed, so its 10-day outcome confirms or rejects the idea directly.
Forecast: The forecast uses SwingHighClusterCountComponent with these settings: pivot "low", level "above", form "proximity", period 90, side 2, band 2 %, power 1. - What it measures: it finds the lowest 90-day swing low at or above the close. It counts the swing lows within 2 % of that level, and multiplies the count by 1/(1+D), where D is the close's percent distance below the level. - Scaling and sign: the value is standardised over 90 bars, damped by signed_power with exponent 2, so a single distant low gives almost nothing and several lows just overhead give a lot. It is then negated, so the forecast is short only. - When it is zero: the forecast is 0 when no swing low lies above the close. - When it is active: it is active only while the 90-bar return is at or above -50 %. On a deeper collapse the regime is null and the book is flat. - Size: the short grows with the number of lows at the level and with how near the close is to it.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Cases are the grid bars (positions 0, 10, 20, … of each window) where the forecast is below 0. For each case, take the coin's 10-bar return minus the coin's mean 10-bar return over all windows, with the sign flipped to the short side, and multiply it by |forecast|. The measure is the t of the mean of these values across all coins and windows.
- Supporting check: Among the cases, the third with the largest |forecast| must show a larger mean unusual fall than the third with the smallest (difference above 0).
- Confirm: The main t is 2 or more over at least 30 cases, and the supporting check passes.
- Reject: The main t is -2 or less over at least 30 cases.
- Inconclusive: The main t lies between -2 and 2, or t is at least 2 but the supporting check fails, or there are fewer than 30 cases.
