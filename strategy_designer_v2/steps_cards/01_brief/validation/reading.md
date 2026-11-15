# Exercise 8: "not researchable"

**Prompt change.** When a request can only be met by a theory about how two or more coins move together (one leading another, a spread, a relation), the helper writes no brief, and no other theory in its place. It answers one line: `not-researchable: <why>`. The script prints it and saves nothing. Four requests on exercise 7's test index. Opus. Cost: 0.12 USD.

| # | Request | Result | Right? |
|---|---|---|---|
| 1 | "whether bitcoin's moves lead the moves of smaller coins" | not researchable: "a relation between two or more coins, and each coin can only be tested on its own bars" | yes |
| 2 | "whether the ETH/BTC ratio returns to its average" | a brief: 009, the ETH/BTC pair's own price, `instruments: ETH/BTC` | yes: the ETH/BTC pair trades as one instrument, with its own bars. Whether the engine has its data is not step 1's question |
| 3 | the RSI theme on BTC, ETH and BNB | a brief: 010, RSI around its midpoint, on each coin | yes: several coins, each tested on its own |
| 4 | no theme | a brief: 011, weekend moves reverse on weekdays (one coin) | yes |

**Point 2 is the line the rule draws.** A relation between two coins' separate prices is not researchable. A pair that trades as one instrument is. The model drew that line itself.
