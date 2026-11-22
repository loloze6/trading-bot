---
idea: 024-04_downrun-volume-fade-depth-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars whose loss is large against the coin's typical 4h move over 30 days -> adapted: the streak's loss in usual one-bar moves (180 bars), with "large" made a graded dead zone and "after" made "while the streak runs".
- Comparison: the larger the volume decline from the streak's first bar to its last, the larger the rise -> kept: the log of first-bar volume over last-bar volume, added as a graded term that only increases the long.
- Outcome: the coin rises over the next three days (18 bars) -> kept: each bet is held 18 bars and judged on the 18-bar return.
- Verdict transfer: yes: the forecast is long exactly while the stated streak exists, and grows with its loss and with its volume fade, so its results speak for the idea.
Forecast: The forecast is the equal-weight mean of two terms, and it is never short. - The first term is the current down-streak's summed loss divided by the mean absolute 4h return of the last 180 bars. It is standardised, then raised by signed_power with exponent 3, so short or shallow streaks give nearly 0 and only large losses give a sizable long. - The second term is the streak's volume fade, ln(volume of the first streak bar / volume of the last). It is standardised, clipped at 0 so rising volume adds nothing, then raised by signed_power with exponent 3. - Both terms are 0 on any bar that does not close down, so the forecast is 0 outside a streak. - The forecast is positive during a falling streak. It grows with the streak's loss in usual moves and with how much its volume has faded.
Config: 024-04_downrun-volume-fade-depth-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: A case is each long bet (a rise of the forecast of at least 2 points), read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal bar's close, minus the coin's normal 18-bar drift over all windows. The measure is the mean of these excess returns over all cases, with its ordinary t.
- Supporting check: Split the cases at the median of the raw volume_fade value (last_history_value). The mean excess return of the above-median cases minus that of the below-median cases must be above 0.
- Confirm: The idea is confirmed when the mean excess return is above 0 with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The idea is rejected when the mean excess return is below 0 with t <= -2 over at least 30 cases.
- Inconclusive: The result is inconclusive in either of these cases: - the t lies between -2 and 2; - the main measure confirms but the fade check fails. Fewer than 30 cases is inconclusive whatever the t.
