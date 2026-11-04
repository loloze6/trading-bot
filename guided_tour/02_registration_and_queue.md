# Stop 02: Registration and the queue

## Speech (verbatim)

**Stop 02 of 29: Registration and the queue.** Open on the side: `run_campaign.py`, `campaign_queue.yaml`, `record_schema.py`, `venue_tradability.yaml`.

(Correction to stop 01, also written under that stop: the operator's SMA brief first launched run_100; run_101 came from the same brief through a second queue line, explained below.)

**In one sentence.**
Registration puts a finished brief on the campaign's to-do list; the queue is that to-do list, and also the history of every brief the campaign has ever taken on.

**Why it exists.**
The campaign is meant to run without a person at every step. So it needs one place that says what to work on next and what is already done.
Without it, an idea could be launched twice, a run could start from a half-filled form, and nobody could trace which brief produced which run.
The checks at the door are cheap. They refuse a bad brief before any money is spent on AI calls or backtests.

**What comes in, what goes out.**
- In: a brief, written by the operator, by decide-next at the end of a run, or by the campaign review.
- Out: one new line in the queue: which brief, its priority, who wrote it, its state, and an empty list of runs.
- Next: the launcher (stop 04) picks a line and starts a run; decide-next (stop 24) reads the history to choose follow-ups.

**What happens here, step by step.**
1. The operator hands over the brief, a priority (a smaller number goes first) and a short note.
2. The registrar reads the top of the brief. It checks the six things every brief must say: the kind of idea, the idea itself, the coins, the bar size, the exchange and the product. It refuses a brief that still holds the template's blanks.
3. It checks that the coins and the bar size at the top match those in the test settings further down. So a run cannot backtest something other than what its brief claims.
4. It looks for an old pass/fail block from the retired verdict system. An empty one is refused. A filled one is accepted, with a note that nothing will read it.
5. It names the line after the brief's file name, and refuses a name already in the list.
6. It appends the line and saves the whole list. Before saving, every line is checked against a fixed vocabulary of states and labels. The file is replaced in one move, so a crash cannot leave it half written.

Registration does not wait for a running campaign: it takes no lock.
Whether the operator may legally trade that exchange and product is not checked here. That happens at launch.

A line then moves through states:
- ready: waiting to be picked;
- in progress: its runs are going;
- done: finished;
- paused: stopped on a problem, picked up only by a resume;
- blocked: waiting for a person, for example an approval;
- queued: set aside, never picked on its own;
- superseded: closed without running, or replaced; set by a person.

The launcher always continues a line already in progress. Otherwise it takes the ready line with the smallest priority number.

One brief can feed several lines. The operator's SMA brief became the line that ran run_100. The brief stayed "open" (it may yield more ideas). So after run_100, decide-next added a second line on the same brief, which ran run_101. After run_101, decide-next wrote a new brief; the operator picked it, and it ran run_102. After run_102, decide-next wrote the brief we read at stop 01. Its line now waits for the operator's approval.

**What it costs and how long it takes.**
No AI call and no backtest.
76 lines in the queue today: 38 done, 35 superseded, 2 waiting for approval, 1 blocked (`campaign_queue.yaml`, counted with a read-only script).
43 lines written by an agent, 32 approved by the operator, 1 delivered by the user (same count).

**What is switched off or not used here.**
- The older check that demanded a pass/fail block is not reached: verdict routing is retired.
- The coin and bar-size check runs only because config-direct authoring is on.
- The tradability table is not read at registration, only at launch.
- No code sets "superseded"; the code's messages tell a person to set it.
- Three origin labels (composition, campaign review, external) are on no line today.
- Five old lines carry verdict fields that newer lines do not have.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Command line | `run_campaign.py:5931-5975` | Builds the commands; `register` takes `--brief`, `--priority`, `--notes` (`:5953-5962`) |
| Folder guard | `run_campaign.py:5977-5981` | Refuses any command run outside `strategy-research/` |
| No lock for register | `run_campaign.py:5983-5984`, `:6014-6024` | `register` exits before the campaign lock is taken |
| Register entry point | `run_campaign.py:5615-5626` | With `decide_next` on (`campaign_config.yaml:649-650`), adds `brief_status: open` |
| Register function | `run_campaign.py:955-1026` | Parses, lints, refuses duplicates, builds and appends the entry, logs one line |
| Allowed extra keys | `run_campaign.py:948-949` | `origin`, `proposal_ref`, `card_ref`, `decision_ref`, `brief_status`, `parked_reason` |
| Allowed start states | `run_campaign.py:952` | `ready`, `queued`, `blocked_on_operator_approval` |
| Refusal handling | `run_campaign.py:980-988` | A malformed brief gives `REGISTER REFUSED` and exit code 1 |
| Entry fields | `run_campaign.py:1008-1020` | `id`, `brief_path`, `status`, `priority`, `source`, `relation`, `notes`, `run_ids`, then extras |
| Required keys and blanks | `run_campaign.py:669-733`; `tools/campaign_review_retired.py:29-30` | Six required keys; the `<FILL IN` sentinel (`:404`, `:422`) |
| Registration-only lint | `run_campaign.py:610-666` | Runs only under `config_direct_authoring` (`:638-639`); wraps malformed shapes (`:652-666`) |
| Promotion check, retired routing | `run_campaign.py:572-607` | No key: silent; empty or generic: refused; other: note |
| Promotion check, flag off | `run_campaign.py:547-569` | Requires a block; not reached with current flags |
| Coins and bar size agree | `run_campaign.py:454-544` | Compares `market_universe`/`timeframe` with the protocol; `USDT` stripped (`:440-451`) |
| Tradability table reader | `run_campaign.py:367-396` | Used at launch (`:787-792`), not at registration |
| Tradability table | `venue_tradability.yaml:15-42` | Kraken spot and perp tradable; margin unconfirmed; anything else not tradable |
| Queue path | `run_campaign.py:106` | `config/campaign_queue.yaml` |
| Load and save | `run_campaign.py:173-220` | Read; check every entry (`:178-188`), then atomic replace |
| Entry schema | `record_schema.py:215-250` | Kinds of value per field |
| Vocabularies | `record_schema.py:113-114`, `:123-133` | Statuses, relations, sources, brief statuses, origins |
| Picking a line | `run_campaign.py:223-235` | `in_progress` first, else lowest-priority `ready` |
| Where states are set | `run_campaign.py:4424`, `:4436` (in progress); `:4847`, `:4728` (done); `:333-349` (paused); `:148` (approval status) | Writers of each state |
| Superseded by hand | `run_campaign.py:2569`, `:2576`, `:4601`; `RUNBOOK.md:674-738` | Messages and runbook rows that tell a person to set it |
| Other registrars | `run_campaign.py:5541` (extra card, `queued`), `:5605-5606` (reframe); decide-next (stop 24) | Same function, other callers |
| Derived files after a save | `run_campaign.py:338-348` | Halt path rewrites summary, loop health, schedulability; registration does not |
| Queue file head | `campaign_queue.yaml:1-3` | `version`, `created_at`, `queue` |
| First entry | `campaign_queue.yaml:4-10` | `P4_ts_trend`, `blocked_on_daily_bar_ingest` |
| SMA brief, run_100 | `campaign_queue.yaml:1299-1310` | Operator line, `brief_status: open`, `outcome: refuted` |
| Same brief, run_101 | `campaign_queue.yaml:1311-1323` | R2 line `..._more_1`, `origin: brief` |
| run_102's line | `campaign_queue.yaml:1335-1351` | Operator pick of decide-next's brief; records the retry-analyst |
| Rejected candidate | `campaign_queue.yaml:1352-1363` | `trade_efficiency-run_102-1`, superseded |
| Waiting candidate | `campaign_queue.yaml:1364-1374` | `forecast_power-run_102-2`, `blocked_on_operator_approval` |

Remarks? Mark a remark "direct" for an answer before the next stop; say "next" to continue.

## Operator remarks (verbatim, with the guide's direct answers)

CHallenge here on It looks for an old pass/fail block from the retired verdict system. An empty one is refused. . If it is retired, why checking it. It seems adding complexity for nothing. 

Thanks, clear, so, in general this step is the workflow input backlog manager from my understaindg

Next

## Inspector notes

### (1) Design and mechanism

1. The operator's reading is right: this is the backlog manager, and it checks form, not substance. The six door checks (`RC:955-1026`) verify shape (required keys, blanks, universe/timeframe agreement, promotion block, id uniqueness, vocabulary). Nothing here asks whether the idea was already tested, whether the fold is one the idea was not seen on, or whether the venue is tradable; those live at decide-next (stop 24), 5a's anti-adjacency gate (stop 16) and launch (`RC:787-792`). For a hand-registered brief the first "already tried" check therefore comes after 1a and 1b have been paid for (stop 16's gate), not at the door. The speech's "the checks at the door are cheap" is true; the expensive mistake they could catch (a repeat idea) is not among them.
2. No run self-launches under the current switchboard. Agent entries are registered at priority 999 (`decide_next.py:132`) and, with `operator_approval` on (`campaign_config.yaml:939-940`), start as `blocked_on_operator_approval` (`RC:952`, `_approval_status :3431-3433`); only `--approve <id>` (`RC:6002-6004`) sets them `ready`. Today's queue has 0 `ready`, 0 `in_progress`, 2 `blocked_on_operator_approval` (counted by grep over `campaign_queue.yaml`). So "run autonomously and continuously" is, by the flag, "run one brief, stop, wait for a person"; and an operator brief at priority 1 always pre-empts every agent candidate (`_select_entry`, `RC:231-235`). This is the operator's chosen mode (D-071), recorded as a fact for the autonomy question raised at stop 00 note 1.4.
3. On the operator's challenge (the retired promotion check, `RC:572-607`): under the live flags its only effects are to refuse a key the template already says not to write (stop 01, template `:11`) and to log a note that the key is ignored. It exists because the flag-off branch (`RC:547-569`, `_check_generate_protocol_has_promotion`) still requires that key, and the launch drops it (`_without_retired_promotion`, `RC:760-774`). The check is the cost of keeping `verdict_routing_retired` a flag instead of the only path: three of the six door steps (steps 3 and 4 of the speech, and the branch choice at `RC:640-656`) are conditional on flags whose off-state no run uses. The simplification is upstream of this file (stop 28).
4. `register` takes no lock (`RC:5983-5984` exits before `:6019-6021`), while the running campaign holds its queue in memory and rewrites the whole file at every state change (`_save_queue`, `RC:191-214`, atomic replace of the full list). A `register` issued while `run_forever` is between two saves is overwritten at the runner's next save: the new entry is lost silently, no error. The docstring itself names the file "the clearest concurrent-writer-risk file in this repo" and defers the fix (`:194-197`, E-051 at `:6017-6018`). The speech presents the no-lock as a convenience; it is also the one unguarded write path into the campaign's to-do list.
5. The vocabulary check at save (`_validate_queue_provenance`, `RC:178-188`) validates all 76 entries on every write, with the verdict-token rule (`record_schema.py:139-141`) refusing a bare verdict word in any field but `outcome_reason`. That is a real anti-fooling guard (a hand-written `outcome: kill` cannot ride in). But `status` is a regex, not a closed list: `paused:.+` and `blocked_on_.+` accept any suffix (`record_schema.py:113-114`); the first entry's `blocked_on_daily_bar_ingest` (`campaign_queue.yaml:6`) is a hand-written status no code sets (grep in `RC`: no writer). The speech's "fixed vocabulary of states" is only half fixed.
6. One file is both the to-do list and the history: 76 entries, 73 terminal (38 done + 35 superseded), 1374 lines, rewritten whole at each save. Decide-next does read the history (owner status for the R2 rule, `decide_next.py:212`, `:959`), so the history is load-bearing and cannot simply be archived; but the per-run record also lives in `campaign_memory.yaml` (stop 22). Whether two histories are needed is a stop-22/24 question.
7. After `register`, the operator-facing derived files (`campaign_summary.md`, `loop_health.yaml`, `schedulability.yaml`) are not refreshed: `_regenerate_summary`/`_write_loop_health`/`_write_schedulability` are called on halts and state changes (`RC:338-348`, `:2461-2466`, `:2616-2621`, `:2756-2760`), not from `register_hypothesis`. The summary shows the new entry only after the next `process_once`. Minor.
8. `research_only` (computed at launch from `venue_tradability.yaml`, `RC:789-790`) is written into `research_brief.yaml`; what reads it back and what it blocks was not checked here (lead for stop 04). The table's own header (`venue_tradability.yaml:3-5`) and the code comment (`RC:357-361`) call it a "registration-rule mechanism", which it is not: it runs at materialisation.

### (2) Legacy or simplifiable (leads)

1. `_check_generate_protocol_has_promotion` (`RC:547-569`) and the flag-off half of `_lint_new_pipeline_registration` (`RC:640-656`): reachable only with `verdict_routing_retired` off. With the retired promotion check (`:572-607`) they are three functions serving a `promotion` key no live path reads. Checked: `_without_retired_promotion` drops the key at launch (`:760-774`); the template says not to write it. Not checked: tests pinning these functions.
2. `relation` (`RC:1014`, vocabulary `record_schema.py:123-126`): the docstring says its vocabulary "is the retired routing words" (`RC:971-972`); agent entries omit it; operator entries carry `new_registration` (30 by grep). The field carries one constant on the live path. Candidate for removal with the retired routing.
3. Legacy fields on old entries: `title` on 13 entries (`[obsolete] ...`, written once by code, `record_schema.py:230-233`), `verdict_status` on 5, `verdict_void_reason` on 1 (grep counts). The `QUEUE_ENTRY_SCHEMA` (`record_schema.py:215-254`) keeps `refinement_brief_path`, `refinement_brief_consumed_for`, `launch_failed_run_id`, `launch_exception_detail`, `launch_prior_status`: which of these any live entry carries was not counted beyond the three above.
4. `_REGISTER_EXTRA_KEYS` includes `parked_reason` (`RC:948-949`, schema note "unused until slice 6c", `record_schema.py:226`): whether any entry or writer uses it today is not checked.
5. `origin` values `composition`, `campaign_review`, `external` (`record_schema.py:133`): on no entry (grep: 25 `brief`, 19 `reader`). `campaign_review` has a writer (`RC:5606`); `composition` and `external` writers not checked.
6. The `queued` status (`RC:952`, `:5541`, extra cards): 0 entries today. Its reader/un-queue path not checked at this stop.
7. `BASELINE_PATH` (`RC:112`, `config/campaign_baseline_runs.yaml`) and `_LINEAGE_CONTINUATION_STAGES` / `_LEGACY_MINTING_ROUTERS` (`RC:122`, `:137`): legacy-routing constants kept for the halt that refuses a legacy continuation (`RC:125`, `:268-279`). Live only as refusals of a shape no run has produced since the flag went on; lead for stop 28.

### (3) Disagreements between the speech and the element

1. Step 6 "every line is checked against a fixed vocabulary of states and labels": statuses are a regex with free suffixes (`record_schema.py:113-114`), see note 1.5. Labels (`source`, `relation`, `origin`, `brief_status`) are closed sets (`:123-133`).
2. Step 2 "the six things every brief must say" and the reading-map row "Six required keys": correct (`campaign_review_retired.py:29-30`). The speech says the registrar "refuses a brief that still holds the template's blanks"; the same check also runs at launch and resume (`RC:705-718`), which the speech omits (stop 01 said it).
3. "Registration does not wait for a running campaign: it takes no lock" is stated as a fact only; the lost-write consequence (note 1.4) is not mentioned, and section 6 ("switched off or not used") does not list it. Not a wrong statement, an incomplete one.
4. "No code sets `superseded`" — confirmed (grep for an assignment in `RC` and `decide_next.py`: only messages and tuples, `RC:2569`, `:2576`, `:2630`, `:3447`, `decide_next.py:212`).
5. The figures (76 entries; 38 done, 35 superseded, 2 awaiting approval, 1 blocked; 43 agent, 32 operator, 1 user) match a grep count of `campaign_queue.yaml`. "Five old lines carry verdict fields" matches 5 `verdict_status` (one also `verdict_void_reason`).
6. Reading map "Entry schema `record_schema.py:215-250`": the schema continues past `:250` (to `:254` and beyond); the range is short, not wrong.
7. The states list in the speech omits the hand status `blocked_on_daily_bar_ingest` on the first entry (`:4-10`, which the reading map does name) and `queued` is listed although no entry carries it today; both are facts, fine.
8. Correction to stop 01 (run_100 from the operator's brief, run_101 from the R2 line `__more_1`, `campaign_queue.yaml:1299-1323`): confirmed by the queue. My stop-01 notes read the same brief file for both, so they stand; where they say "run_101's brief" read "the brief that ran run_100 and run_101".
9. Verified as stated: `RC:5931-5975`, `:5977-5981`, `:5983-5984`, `:6014-6024`, `:5615-5626`, `:955-1026`, `:948-952`, `:980-988`, `:1008-1020`, `:610-666`, `:638-639`, `:652-666`, `:572-607`, `:547-569`, `:454-544`, `:367-396`, `:787-792`, `:106`, `:173-220`, `:178-188`, `:223-235`, `:4424`, `:4436`, `:4728`, `:4847`, `:333-349`, `:148`, `:5541`, `:5605-5606`, `:338-348`; `venue_tradability.yaml:15-42`; `campaign_config.yaml:649-650`; queue `:1-3`, `:4-10`, `:1299-1310`, `:1311-1323`, `:1335-1351`, `:1352-1363`, `:1364-1374`.
