# Stop 01 of 12: The brief

## Speech (verbatim)

Stop 01 of 12: The brief. Open on the side: `strategy_designer_v2/briefs/real_01_daily_breadth_fold_a.md` (yours), `strategy_designer_v2/briefs/n04_btc_daily_vol_timing_1d.md` (one night brief), `strategy_designer_v2/README.md` ("The path", step 1), `strategy_designer_v2/run.py` (`read_brief`, and `main` where the brief is passed on).

Note on a name: the itinerary speaks of "the four-line head rule in README". The README has no section by that name; the rule sits in "The path", step 1: "research goal, venue, product, strategy domain. The rest optional." Your brief's own body says "The pipeline reads the four lines above".

### 1. In one sentence
The brief is a short text file in which the operator says what to look for, on which exchange, which coins, which kind of strategy and which bar size; it is the only thing the operator writes for a run.

### 2. Why it exists
The operator decides, the pipeline discovers: the brief is where the deciding happens. The README's path makes the brief the operator's step and everything after it the pipeline's, and says the operator approves only new briefs and the holdout.

### 3. What comes in, what goes out
In: the operator's words. Out: a file with a head (a block of named lines between two `---` marks) and a free-text body. The runner parses the head and uses two of its lines: the coins and the bar size. The whole file, head and body, goes word for word to the two model calls.

### 4. What happens here, step by step
Your brief's head has six lines: research goal, venue (kraken), product (BTC/USD and ADA/USD spot, with Kraken perp fees applied to spot prices), strategy domain (daily breadth), bar size (1d), and an `already_tried` line (lane 1, a slow moving-average trend, closed). Its body is your v1 brief, verbatim, with two v2 notes: a claim is measured on BTC and on ADA and must pass on both; your "branch 3" is the engine's profit bar.

What code reads, in `run.py`: the runner cuts the head out and reads it. From the product line it picks every "XXX/USD" pair and turns it into a symbol: BTCUSD and ADAUSD here; with none found it uses BTCUSD. From the bar-size line it takes the bar size; with none it uses 1h. Nothing else in the head is read by code: not the goal, the venue, the domain, the fees nor `already_tried`. Those, and the body, reach only the models, which read the whole file as a trader would. The fold is not taken from the brief either: it is a knob of the runner, A by default; the "fold_a" in the file name is a name. The fee sentence is for the model; the engine applies its own cost (stop 05). The body names v1 files (the criterion menu, the profitability bars, the coin universe); no v2 code reads them. Separately from the brief's own `already_tried`, the runner adds the claims already tried under this brief's file name from the records (stop 03).

The night brief n04 has the same head shape, BTC only, daily, and one paragraph; it states its fee itself, 0.15% per round trip. The folder holds 45 briefs: three made-up ones from the first tries, forty night briefs written by the night's delegate (`night_2026-11-06/README.md`), yours, and a variant of yours on LTC that the night made because ADA has no history before folds B and C.

Live: the brief is read on every run.

### 5. What it costs
Nothing of its own: it is a text file.

### 6. How it stands against the two rules
The brief reads no bars and computes nothing; code takes two lines from it. Nothing in it is on-off. Your body's line "say in each idea why its inputs cannot leak" is the no-lookahead scar, passed to the model as text.

### Reading map
| Part | File and section | One line |
|---|---|---|
| Your brief | `briefs/real_01_daily_breadth_fold_a.md` | Six-line head; your v1 text verbatim below |
| A night brief | `briefs/n04_btc_daily_vol_timing_1d.md` | Same head shape, one paragraph, BTC only |
| What a brief must hold | `README.md`, "The path", step 1 | Goal, venue, product, domain; the rest optional |
| What code reads | `run.py`, `read_brief` | The head, the coins from the product line, the bar size |
| Where the brief goes | `run.py`, `main` (the ideas call and the analyst call) | The whole file to both model calls |
| Fold | `run.py`, `main` (`--fold`, default A) | A runner knob, not a brief line |
| Who wrote the night briefs | `night_2026-11-06/README.md`, first paragraph | "briefs by the delegate" |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Remarks: Readme should be regularly clean up over the engineering iterations. 
> Wondering of the brief is only having relevant info around ideas. It should not encapsulate enginerring or workflow details. We had before a guideline in v1 to allow a good brief tonbe created. A brief should be structured: only information relevant and correponding to each field. Suggesting to udnerstand why it is not the case (if it is), how to avoid, what to improve. Check also guided tour on v1 around that for further remarks. Also extra information not used by workflow should be cleaned !

## Inspector notes

1. The two rules (`V2/briefs/*.md`; `V2/run.py` `read_brief`, lines 16 to 20): clean. The brief is text; `read_brief` reads the head and nothing else; no bars, no verdict, no switch. One brief asks for what the rules forbid: `n04` body asks for rules that "size by volatility state" and "switch between momentum and reversal by volatility regime"; v2 has no sizing a claim can set (the sizing is the engine's, fixed in `backtest.py`) and a regime that flips the sign is a switch dressed as a strength. The brief is not a rule-breaker, but no file tells a brief writer what a v2 claim can and cannot carry; see 5.
2. What code reads against what the pages say (`V2/README.md` "The path" step 1; the brief's own line 12 "The pipeline reads the four lines above"; `run.py` lines 19 to 20): three different statements. The README names four lines (goal, venue, product, domain); the brief says the pipeline reads four; the code reads two, `product` (regex `[A-Z]{3,5}/USD`, default `BTCUSD`) and `bar_size` (default `1h`), of which `bar_size` is not among the README's four. `venue` is read by nothing: `backtest.py` line 59 passes `exchange="kraken"` as a constant, so a brief with another venue would run on Kraken bars without a word. The disagreement is between the README, the brief and the code, and the speech states it correctly.
3. Three fee statements for one book (`briefs/real_01...` head and body: "Kraken perp costs"; `steps/ideas/PROMPT.md` line 12 and `CLAIM_FORMAT.md` line 44: "0.15% per round trip"; `steps/engine/backtest.py` line 14: `FEE_PER_LEG = 0.0005`, 5 bps per leg, 0.10% per round trip plus the engine's own slippage; `briefs/fake_01` body: "about 0.2%"; `n04` body: "0.15%"). The model is asked to clear one cost and the engine charges another; the brief's fee sentence is a fourth, read by no code. Which number is the engine's to settle at stop 05; the brief should not carry a fee at all, since nothing reads it.
4. The fold is not in the brief (`run.py` line 111, `--fold`, default A; `records/claims_tried.yaml` keyed by `brief.name` in `remember`, line 79). The README says the operator writes briefs and approves the holdout; the fold, which fixes what months the idea is judged on (scar 3, "fixed before the backtest"), is a command-line knob with a default and is recorded only in `record.yaml`. The file name `..._fold_a` is a name, as the speech says, and `real_01b` says "folds B and C" in its body while the runner has to be told. Autonomously and continuously, a brief that does not name its fold cannot be queued without a hand on the knob. One line in the head, read by `read_brief`, would close it.
5. Why the brief is "a mess" (the operator's remark): checked `V2/steps/ideas/` (`PROMPT.md`, `CLAIM_FORMAT.md`, `check_claims.py`), `V2/README.md`, `V2/briefs/`: v2 has no brief format file and no brief check; the one specification is the README's one line. The real brief was made by pasting the v1 brief verbatim under a v2 head (its line 12 says so). Its body therefore carries v1 engineering that nothing in v2 reads or can act on: `criteria_from`, `config/criterion_menu.yaml`, `config/profitability_bars.yaml`, `config/coin_universe.yaml`, "Step 1a", "design variant (a config change)", "blocks ... registered and composed later", "D-128", the drawdown-cap fact. The ideas model reads all of it (`PROMPT.md` line 24: "read the brief as a trader would, including the prose"; run 003 `claims.yaml` line 126 shows it acted on the SMA line), and `PROMPT.md` line 15 says "Data: only what the brief makes available", so the brief's text is scope, and dead v1 words in it are scope too. v1's guideline (`strategy-research/workflow_artifacts/templates/research_brief_new_pipeline.md`, with the registration refusal of `<FILL IN>`) was not pulled into v2, which is v2's rule; but nothing replaced it. The operator's v1 remark at stop 01 of the v1 tour asked for exactly this (purpose of the prose, plain words, a maximum length); it is open in v2 as well.
6. Simplifiable: (a) two "already tried" lists: the head's `already_tried` (hand-written, read by the model via the whole file, `PROMPT.md` line 21) and the record's list keyed by brief file name, appended by `run.py` lines 123 to 124. The second is automatic; the first exists for v1 history and had to be copied by hand into `real_01b` (STEPBACK, "02:40"). One mechanism would do if the record could be seeded. (b) The v2 note on line 12 of the real brief ("the brief's branch 3 is the profit bar of the engine") is a translation of v1 words that the body should not need. (c) 45 brief files, 40 of them void night briefs beside the live ones, same folder; `run.py` makes `runs/<brief stem>/`, so a stray re-run of a night brief would write live records. Nothing reads the folder as a whole, so the cost is only confusion; to weigh at stop 11.
7. Small code points in `read_brief` (`run.py` lines 16 to 20): `text.split("---")[1]` takes the first block, fine; an empty head gives `fm = None` and `fm.get` raises, so a brief with `---\n---` crashes rather than refuses; a product written `BTC-USD` or `BTCUSD` silently becomes `BTCUSD` by the default, not by a match. No refusal path for a malformed head, where the night's lesson (STEPBACK "Wakeup 01:28") was "refused with a reason, never a crash".
8. Speech against element: the speech's account of what code reads, the defaults, the fold as a knob, the fee going only to the model and the 45 briefs matches the files. One addition the speech does not make: the head has six lines and the brief claims four are read; the README names four, and they are not the same four the code uses (2 above). No disagreement of substance.

Running view after stop 01: the brief is the one thing the operator writes, and it has no format, no check and no fold line; the real brief carries v1 prose as v2 scope; the fee is said three ways. The two rules stand.
