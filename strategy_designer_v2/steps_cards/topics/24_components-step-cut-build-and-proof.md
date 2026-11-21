# Topic 24: Components step: a cut build undone; the proof backtest removed

Status: closed (2026-11-19)  
Where: research: components  
Opened: 2026-11-19 (clean-up 4; the night 1h)

## Question
How does the components step stay safe across restarts and engine changes?

## Seen
- 00:26: a restart cut a build; its class, catalogue row and spec stayed in the shared files (undone by hand).
- After the 1-day hole rule, every build failed its proof: the stored proof record dated from before the rule; 4 wishes
  were wrongly answered "cannot build".
- The proof backtest used `PriceEvolutionComponent` only, which no build touches: it showed only that the module loads
  and the engine runs, which the harness shows.
- Built: a note of the files as they were (`components/build_in_progress.json`), undone at the next start; the proof
  is the standard checks (the old defaults unchanged on real data) and the bot's suite. A build: 86 s (about 3 min
  before).

## Why it matters
A half-built component in shared code, or every build refused, stops the research.

## Options
| Option | Gain | Risk |
|---|---|---|
| A note on disk, undone at the next start | survives a restart | - |
| Restore from git at start | simple | loses earlier uncommitted builds |
| Proof: before and after the build | no stale record | still tests nothing a build touches |
| Proof: the checks and the suite only | tests what a build can break | - |

Recommended: the note; the checks and the suite.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | A build cut short is undone at the next start, from a note of the files | operator's go, on the design session's proposal | the undo lived only in the running process | restore from git |
| 2026-11-19 | The proof backtest removed | operator | it tested a backtest unrelated to the component created: it secured nothing | a before-and-after backtest |

## Status and next
Closed. Lives in `components/helper/build_component.py` and its card.

## Links
Commit 5f97b1d0.
