# Review of the helper prompt before exercise 1

Reviewed: prompts (a) and (b) in `../../01_brief.md`, draft 4. Question asked of each line: does the helper have what it needs to write a brief that meets the card's criteria, and nothing about the pipeline?

## What was missing or wrong
1. **The helper does not know what the theory is for.** Nothing says it will be tested on historical market data. A model left to guess writes theories about news, order flow, funding or sentiment that cannot be seen in prices. Fix: one sentence: the theory is researched on historical price and volume bars of coins traded spot. This is the domain of the evidence, not how the pipeline works. Assumption to confirm: the research reads bars only (open, high, low, close, volume). I have not checked what else the engine offers.
2. **No case for "no theme".** The prompt read "Write one trading theory about: {theme}". With no theme it breaks. Fix: the request is in the user message, and "a theory of your choice" is a valid request.
3. **A question theme had no rule.** The operator's RSI theme is a question. The prompt pushed the helper to a claim, which means the helper picks the answer. Fix: a question may stay a question; the helper then gives the reasons it could go either way.
4. **"If the source argues several, take the main one" is undefined.** A listing page holds twenty scripts and no main one. Fix: write the theory most of the source supports, and name the others after the file, one line each, so the operator sees what was left out.
5. **The reason's origin was not asked.** Scripts on a listing page rarely give a reason. A helper that adds one makes it look like the source's. Fix: say whether the reason comes from the source or from the helper.
6. **Results in the source were not handled in (a).** The source says "optimized for better total profit", "tested on BTCUSDT", "high win rates". Fix: the no-results rule is in the one prompt, for the source and for memory.
7. **Code and parameters.** The source holds Pine code and parameter values (10/50 SMA). Fix: read code only to understand the rule; the theory names no parameter value.
8. **Language.** The source is a French page with Chinese and Spanish entries. Fix: write in English.
9. **The output spec contradicted itself.** "Return one Markdown file and nothing else", then "after the file, write short-name:". Fix: the exact output is defined once, with two lines after the file.
10. **A theory that cannot show in crypto bars had no exit.** The first item on the source page is an S&P 500 session filter. Fix: if the theory cannot show in crypto price and volume bars, the helper says so in one line instead of writing a brief.
11. **Two prompts, one comparison too many.** The operator's test is three models by three contexts. Prompt (b) was my recommendation, so the criteria are in the one prompt; (a) is dropped from this exercise.
12. **Structure.** The instructions are moved to the system prompt and the request (theme or source) to the user message, so the same instructions serve all three contexts unchanged.

## What was kept
The role, the closed list of header keys, "fill a header line only if the request or the source states it", "say what would show it wrong", "say if you do not know a reason".

## The call
One call per test: no tools, no files, no web, no repository, a new empty working folder, no project or user settings, no commit attribution. One note cannot be removed in this cloud environment: an account note with the operator's email, added by the host. It says nothing of trading or the pipeline. Model effort is left at each model's default.
