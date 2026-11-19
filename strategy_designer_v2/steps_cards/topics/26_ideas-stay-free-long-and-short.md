# Topic 26: Ideas stay free: no forced long and short

Status: closed (2026-11-19)  
Where: research: steps 2, 7  
Opened: 2026-11-19 (operator: why did recent ideas not reach a negative forecast?)

## Question
Should every idea be made to trade both sides, so that profitability does not hang on a rising market?

## Seen
- slow_1h_run: 17 of 18 configs trade one side, as their ideas claim (step 3 is faithful). Brief 016: 4 ideas bet on a
  rise, 4 on a fall; step 7's 10 ideas: 9 on a rise, 1 both ways.
- 153 backtests with a verdict (12 runs):

  | Side traded | Backtests | Confirmed | Confirmed and profitable | Not confirmed, profitable |
  |---|---|---|---|---|
  | long only | 83 | 43 | 7 | 4 |
  | short only | 19 | 2 | 0 | 0 |
  | both | 50 | 26 | 2 | 0 |

- Step 5 already removes the drift (its measures are excess or de-meaned returns); step 6 requires beating holding.
- Short-only ideas lose even when the market falls (-0.5 % against -30 %).

## Why it matters
Forcing symmetry could add the side that does not pay; leaving it free leaves books tied to rises.

## Options
| Option | Gain | Risk |
|---|---|---|
| Free ideas | keeps what pays; a one-sided claim is a sharper test | books need rises somewhere |
| Forced long and short | less dependence on the market's direction | attaches a weak short half to good long ideas (2 of 50 two-sided books pay) |

Recommended: free ideas; the market dependence observed after step 6 (topic 8).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Ideas stay free; no rule forcing both sides | operator | forcing a behaviour could work against discovering what pays; the market's influence is to be observed, not imposed | forced long and short |
| 2026-11-19 | The market-direction split is an observation of the stage after step 6, not part of step 6 | operator | step 6 is a profitability check, nothing informational | a line in step 6's check |

## Status and next
Closed. Its observation continues in topic 8; the short side in topic 9.

## Links
Commits 53b723d8, 23d10f34, 1cf1dcad.
