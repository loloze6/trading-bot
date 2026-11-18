---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's average daily volume over the last 5 days against its 30-day average, the more its price rises over the next 3 days relative to its usual 3-day return, and the more so the further the coin fell over its last day.
Consequence: A volume surge that comes with a down day is a stronger reason to lean long than a surge that comes with an up day.
Why:
- F5: The one losing state is a negative 30-day return combined with an up last day. It has a mean gain of -0.00134 and a mean next-day coin return of -0.0018 over 2337 active bars. The other three combinations of the two signs gain between 0.0017 and 0.0029.
- F6: The day before matters strongly. When the last day's return was in its lowest fifth (below -3%), the active book gains 0.00496 per bar and the coin's next-day return averages 0.0098 (1725 bars). In the highest fifth (above +3.3%) the gain is only 0.00007, and the next-day return is -0.0007.
- F7: On the 3-day grid, the excess return after a forecast > 0 rises with the last day's fall. It is 0.0226 (t 4.39, 443 cases) when the last day fell more than 2.2%, against -0.003 in the top two quarters of the last day's return.
