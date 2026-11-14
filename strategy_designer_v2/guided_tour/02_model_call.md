# Stop 02 of 12: The model call

## Speech (verbatim)

Stop 02 of 12: The model call. Open on the side: `strategy_designer_v2/steps/ask.py` (whole, 58 lines); `strategy-research/workflow/run_phase1_research.py`, `_stage_agent_options` (v1, read for comparison, not copied); `strategy_designer_v2/run.py`, `prompt_of` and the `MODELS` line; `strategy_designer_v2/runs/real_01_daily_breadth_fold_a/003/model_calls.yaml`.

### 1. In one sentence
The model call is v2's single doorway to a language model: one prompt out, one answer back, kept as a file, its cost written down.

### 2. Why it exists
Two steps are the model's: the ideas (stop 03) and the analyst (stop 08); both go through this doorway. Its first line: "Closed book, like v1": the model sees only what is pasted into its prompt and can open nothing itself, no data or file the pipeline did not give it.

### 3. What comes in, what goes out
In: a prompt (text), the name of the file the answer must go to, the model's name, and the cost log of the run. Out: the answer file, one new row in the cost log (time, model, answer file, cost in USD), and yes or no: is the answer file there now.

The prompt itself is assembled before, in `run.py`: each file to send (the step's instructions, the claim format, the brief) is pasted in full under a "# FILE <name>" line, anything extra is added (for the ideas, the claims already tried); it ends with "Answer with the YAML file only, nothing else." YAML is a plain-text format of named fields. Both calls use the same model, named once in `run.py`.

### 4. What happens here, step by step
1. If the answer file already exists, nothing is called; the answer is taken as given. This is how a stopped run picks up where it left off.
2. If the model's software kit is not installed on this machine, the prompt is written next to the answer file as "<answer>.prompt.md", a line says "ANSWER NEEDED", and the step reports no. The runner then stops; whoever answers writes the answer file, and the next start of the run takes it from step 1.
3. Otherwise one call is made, with three settings: no tools at all; no settings files loaded (so no project instructions and no machine permissions); and a working folder that is a new, empty temporary folder for each call. The text of the answer is collected, and the cost the kit reports.
4. Code fences (the ``` marks) around the answer are removed.
5. The answer is checked for one thing only: does it read as YAML. If not, the model is asked once more with the same prompt, the parser's complaint, and an instruction to quote values that start with a symbol. The two costs are added. A second failure stops the run with an error.
6. The answer is written to its file, and the cost row is appended to the log.

There is no time limit and no turn limit on the call. Whether the YAML holds the right fields is not checked here; the runner checks claims later (stop 09).

Compared with v1's options function: v2 passes v1's "no tools" and "no settings files" settings and a neutral working folder. v1 also passed a setting that keeps out every MCP server (outside tool connections) and an environment switch that keeps the CLI's automatic memory off; `ask.py` passes neither. v1 used one fixed working folder; v2 makes a new one per call.

Live: every ideas call and every analyst call goes through it.

### 5. What it costs
Run 003, `model_calls.yaml`: three calls, ideas 0.19 USD, analyst round 1 0.31 USD, round 2 0.12 USD, 0.63 USD in all. A re-ask, if one happened, is inside the row's figure; the log does not show it separately.

### 6. How it stands against the two rules
It reads no bars and no files of market data: it moves text. It makes no forecast and holds nothing on-off about one; its only either-or branches are "kit installed or not" and "answer parses or not".

### Reading map
| Part | File and section | One line |
|---|---|---|
| What it is | `steps/ask.py`, docstring | Closed book; with the kit one call, without it the prompt is left for someone to answer |
| Resume | `steps/ask.py`, `ask`, first check | An existing answer file is never asked again |
| No kit | `steps/ask.py`, `ask`, `HAVE_SDK` branch | Writes `<answer>.prompt.md`, prints "ANSWER NEEDED" |
| The three settings | `steps/ask.py`, `_call` | No tools, no settings files, a new empty folder per call |
| One re-ask | `steps/ask.py`, `ask`, the YAML check | Parse error sent back once; second failure stops the run |
| Cost log | `steps/ask.py`, `ask`, last lines; `runs/.../003/model_calls.yaml` | Time, model, answer file, USD per call |
| How the prompt is built | `run.py`, `prompt_of`; `MODELS` | Files pasted under "# FILE" lines; one model for both calls |
| v1's version | `strategy-research/workflow/run_phase1_research.py`, `_stage_agent_options` | Five closed-book settings, one fixed folder |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Next

(Sent together with Rectification 1; the full message is recorded verbatim in `00_rectifications.md`.)

## Inspector notes

1. The two rules (`V2/steps/ask.py`, whole): clean. It moves text, reads no bars, computes no verdict, holds no forecast. The closed book is the guard that keeps the model from becoming a second reader of bars, so its completeness matters for rule 1; see 2.
2. The closed book has a gap v1 had closed (`ask.py` `_call`, line 23; `strategy-research/workflow/run_phase1_research.py` `_stage_agent_options` docstring): v1 passes `strict_mcp_config=True` because, in its own words, "MCP tools are not built-in tools, so tools=[] alone does not remove them", and four of five retained transcripts showed MCP tools offered to a closed-book agent. `ask.py` passes `tools=[]` and `setting_sources=[]` only. On the operator's PC, where the SDK runs, any MCP server in the user's own configuration is offered to the ideas and analyst models. An MCP tool that reads files or the web would make the model a reader outside the engine, against rule 1 and against "closed book, like v1" in the docstring. One keyword argument closes it; v1's `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` is the second, cheaper to carry than to argue about (the per-call temp cwd has no git root, so the memory risk is small, but the setting costs one line).
3. Per-call temp folders (`ask.py` line 23, `tempfile.mkdtemp(prefix="sdv2_")`): v1 chose one fixed folder on purpose: the CLI files a transcript folder per cwd under `~/.claude/projects/`, so a new folder per call scatters one transcript folder per call; `mkdtemp` also leaves one temp directory per call, never removed. Run autonomously and continuously, that is two folders per model call, forever. A fixed neutral folder, as v1, removes both. Nothing in v2 depends on the cwd.
4. Scar 6 is not here either (`V2/README.md` "The scars" 6: "the analyst is capped"; `ask.py` whole; `run.py` `MODELS`, `--rounds`): no cost cap, no token cap, no `max_turns`, no timeout. The only bound on spend is `--rounds` (default 2) and the number of claims the model returns. Run 003 cost 0.63 USD, so today it does not matter; continuous running has no stop on a model that answers long or a loop that re-asks. v1 left `max_turns` unset for a stated reason (one turn by construction with no tools), which holds here too; a cost cap per run or per day does not exist anywhere in v2 (checked `run.py`, `ask.py`, `backtest.py`, `judge.py`, `summarise.py`).
5. The second parse failure is a crash, not a refusal (`ask.py` line 53: `yaml.safe_load(body)` with a comment "stops the run loudly"; `run.py` lines 125 and 152 test only the boolean). The exception leaves `run.py` with no `REFUSED` marker and no `DONE`; the next start resumes at the same call, which is right, but the record of the run shows nothing of why it stopped. The night's own lesson (STEPBACK "Wakeup 01:28") was "refused with a reason", and `run.py` applies it to malformed claims; the model call does not.
6. The cost log is read-modify-write (`ask.py` lines 55 to 57): `log.read_text` then `log.write_text`, not atomic (scar 4), and `cost` can be `None` when the SDK reports none, logged as `null` and then counted as 0 by anyone summing. One process at a time makes the first harmless today; a queue of briefs would not.
7. Redundant or stale around the call: `V2/steps/ideas/check_claims.py` requires `when, then, compared_to, measure, pass_if` under `claim`, the shape before try 09; the live shape is `code, horizon_bars, min_effect` (`run.py` `valid`, line 38). Nothing calls it (grep over `V2/*.py` and `V2/steps/`: only `tries/try_01/READING.md` names it). A file nothing reads that checks a format nothing writes; for stop 03. The instruction "Answer with the YAML file only, nothing else" is said twice: `run.py` `prompt_of` line 25 appends it, `steps/ideas/PROMPT.md` line 6 also says it; harmless, one would do.
8. Speech against element: the 58 lines, the four inputs, the resume rule, the no-SDK path, the three settings, the one re-ask, the missing two v1 settings, the per-call folder and the costs all match the file. Two small points: "named once in `run.py`" is one value under two keys (`MODELS`, line 11); and the speech says a re-ask "is inside the row's figure", true, and the row also has no mark that a re-ask happened, so the parse-failure rate of the prompts cannot be read from the log at all.

Running view after stop 02: the doorway is small and right in shape; its closed book is one keyword short of v1's; the two scars that have no code (atomic writes, a cap) are now confirmed absent at the model call as well. `check_claims.py` is the first dead file.
