---
idea: 043-01_falling-agitated-intraday-drop-rebound
brief: 043_falling-agitated-intraday-selloff-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's drop from the day's open to its close, in percent, in a falling agitated market -> replaced: no catalogue component gives the signed open-to-close drop (BarBodySize is unsigned, OpenToLowDrop reads the low, PriceEvolution reads the prior close).
- Comparison: none (the larger the drop, the larger the rise) -> adapted: graded by the drop's size inside the profile.
- Outcome: the coin rises over the next day -> kept: a long position held for 1 bar.
- Verdict transfer: no: a close-to-close or unsigned body stand-in measures a different quantity, so neither a confirm nor a reject would carry to the open-to-close claim.
Reason: The idea's situation is the day's own open-to-close fall in percent, zero on days that close at or above their open. It is in the coin's own open and close columns. No component computes it, alone or combined. The weighted mean cannot multiply the unsigned body by a sign. No regime measure separates close-below-open days, and a close-to-close return is the very replacement the brief rules out.
