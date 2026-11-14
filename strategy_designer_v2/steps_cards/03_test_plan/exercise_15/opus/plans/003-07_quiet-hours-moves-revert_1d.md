---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp move during quiet hours or a weekend, on low volume -> replaced: 1d bars cannot show quiet hours, and no component reads the weekday or graded relative volume.
- Comparison: the move's volume against the coin's usual volume, at its busier times -> replaced: intraday busy and quiet volume merge into one daily total.
- Outcome: the move partly reverses once busier hours and volume return -> replaced: the next daily bar mixes quiet and busy hours, so the reversal's timing cannot be seen.
- Verdict transfer: no: on daily bars the test would measure a different situation, so neither result would settle the idea.
Reason: The idea's situation and outcome turn on hours within the day (quiet hours, then busy hours returning). The 1d bars this test runs on do not carry that, and the config has no symbol, timeframe or intraday key to reach it. Even the weekend and low-volume parts would need a weekday reading and a graded relative-volume component, which the catalogue lacks.
