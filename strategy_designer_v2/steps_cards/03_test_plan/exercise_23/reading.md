# Exercises 23 and 24: "state each part in the idea's own words"

**Prompt change** (approved: "Good suggestion"). One line before the fidelity statuses: "State each part in the idea's own words, without dropping any of its conditions." The 13 fixed ideas, opus, two runs side by side. Cost 0.95 and 0.82 USD.

| | Exercise 23 | Exercise 24 |
|---|---|---|
| Outcomes | 6 plans, 2 untestable, 5 missing-components | 6 plans, 1 untestable, 6 missing-components |
| 003-07 (quiet hours) | untestable: "replaced" (right) | plan: "adapted" (wrong) |
| 005-06 (bullish divergence, downtrend continues) | plan: "adapted" (wrong) | missing-components (right) |
| Near-zero rejects | 0 | 0 |

**The line helps the reading, not the judgement.** Each situation line now names every condition of the idea ("in quiet hours or on weekends"), so a dropped part is visible. But the status is still wrong in one plan per run:
- 003-07 in exercise 24: quiet hours and weekends become "a low-volume day", called adapted.
- 005-06 in exercise 23: "RSI makes a higher low than at the prior price low" becomes "RSI compared with its own recent past", called adapted. The config cannot remember the prior low: that is a different quantity, replaced.

**The likely cause.** The card's list of allowed adaptations is closed: a threshold or on/off condition made graded, "after X" made "while X", a holding period dropped. The prompt says "such as", which leaves it open, and the model stretches it. The fix is to align the prompt with the card: those three, and anything else is replaced. Not yet made: the full-data run was writing its plans with this prompt.

**Status.** "Done when" not met.
