# Topic 15: The GitHub security warning

Status: closed 2026-11-26 (the pin raised)  
Where: operator  
Opened: 2026-11-17

## Question
Is the vulnerability GitHub reports on the default branch a real risk for this repository?

## Seen
- GitHub reports 1 critical vulnerability on the default branch (Dependabot alert 1). Its package, given by the operator
  (2026-11-26): `claude-agent-sdk`, pinned at 0.2.82 in `strategy-research/config/requirements-mac.txt` (the only pin in
  the repository; the current workflow does not import it). The advisory (GHSA-h4mw-j7qp-8mwm, osv.dev): argument
  injection via the `resume` option allows arbitrary command execution; fixed in 0.2.121.

## Why it matters
A critical dependency could matter once the bot runs on a server.

## Options
| Option | Gain | Risk |
|---|---|---|
| Read the alert on GitHub and update the dependency | removes the risk | a dependency update needs the bot's suite |

Recommended: read it before the bot is hosted (topic 11).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-17 | Parked | operator | not urgent while nothing runs on a server | - |
| 2026-11-26 | Pin raised to 0.2.180 (no known advisory, released 2026-11-09; declares mcp>=1.23,<3, so the mcp 1.30.0 pin stands) | operator ("go"), designer | the fix is in 0.2.121; the latest release at least two weeks old | 0.2.189 (released the day before: too recent) |

## Status and next
Closed. The campaign's code no longer runs (last runnable state c534774), so the raise is not run-tested; the
alert closes when the change reaches the default branch (master).

## Links
Topic 11.
