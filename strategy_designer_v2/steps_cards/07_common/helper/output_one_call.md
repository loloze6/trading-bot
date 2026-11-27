Ideas. From your findings, write the ideas your line asks for. {{IDEA_DEFINITION}}
[MARKET PROFILES]
{{MARKET_PROFILE}}

When your findings show the tested idea's effect lives in one market profile, the same idea in that profile is an idea
of its own: its text with the profile named, and its profile line.
Every idea rests on findings and names them. Write no idea that no finding supports. If your findings support none,
say so.

Your answer, when you give it, is exactly this and nothing else:

findings:
F1: <the finding, with its numbers>
F2: ...

Then, one block per idea, separated by a blank line:
idea: <the idea, in one or two sentences>
consequence: <what it means for a trader, in one sentence>
name: <three to five words>
from: <the findings it rests on, for example F1, F3>
side: <what the idea bets: long, short or both>
profile: <only when the idea names a market profile: its trend, its agitation or both, such as falling agitated, or
         choppy. Name one only when your findings show the effect lives there>
data: <only if your idea is about other data than the backtest's: instruments: ...; bar: ...; period: ...>

For the tested idea unchanged, on other data, a block of its own instead (the code copies the tested idea's text):
same-idea-on: instruments: <coins, from the data available>; bar: <bar size>; period: folds <A, B, C, D>
name: <three to five words>
from: <the findings it rests on>

Or, instead of the ideas:
no-ideas: <why, in one sentence>

To explore instead, answer with one Python code block holding `def explore(data):`, and nothing else.
