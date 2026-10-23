# Run viewer: design (D-180, operator tool, read-only, no pipeline change)

A local web page that reads the campaign's run folders and records and shows them in four
levels: campaign, run, step, variant-in-window. Stdlib `http.server`, pandas, yaml; uPlot
(MIT, vendored) for charts. Works offline.

## Hard rules (enforced in code and tests)

- Read-only. Every file is opened for reading; no write, rename, mkdir or lock anywhere.
  Test: an API sweep under a guard that fails on any write-mode `open`, `os.replace`,
  `os.mkdir`, `Path.write_*`.
- Reads only these paths, all under the strategy-research root (`--root`, default: the
  parent of `--runs`): `runs/run_NNN/**` (never `runs/*/handoffs/`), `config/campaign_queue.yaml`,
  `briefs/<name>.md`, `campaign_record/{campaign_state.yaml, campaign_memory.yaml,
  campaign_log.md, block_registry.yaml}`. Never `trading-bot/local_data/` (so never
  `holdout_sealed/`). The one other read is `config/campaign_data_policy.yaml`, once,
  by `sanitize.py` only (option A below). Test: the sweep records every path opened and
  asserts none is outside that list.
- No sealed-window date in any API response, page or log line (option A below).
- Ids from URLs are checked against what is on disk (run id `^run_\d+$` and present;
  variant in the run's `variants/index.yaml`; window label in that variant's
  `protocol_result.yaml`; step name in the fixed list), so no path is built from user text.
- Binds 127.0.0.1 unless `--host 0.0.0.0`; banner: "run viewer: read-only, local network
  only, no authentication".

## Data model

One loader per view returns one JSON document. Loaders never raise on a missing or
unparseable file: each source is reported as `{"path", "state": "present"|"absent"|"unreadable",
"reason"?}` and the field it would fill is `null` (corrected after review: the code has
always emitted "unreadable" with a "reason"). Parsed files are cached by
`(path, mtime_ns, size)`, so each request rescans the folders cheaply and a finished run
appears without a restart.

## URL scheme

| URL | Returns |
|---|---|
| `/` , `/static/*` | the page (hash routing: `#/`, `#/run/<id>`, `#/run/<id>/step/<name>`, `#/run/<id>/variant/<v>/window/<label>`) |
| `/api/runs` | view 1 |
| `/api/run/<id>` | view 2 |
| `/api/run/<id>/step/<name>` | view 3 |
| `/api/run/<id>/variant/<v>/window/<label>/bars` | view 4, one window |
| `/api/run/<id>/variant/<v>/equity` | view 4, chained equity across windows |

## Steps (view 2 order; the run_099 reading)

| name | title | sources (under the run folder unless stated) | headline numbers |
|---|---|---|---|
| launch | Launch | queue entry, brief, campaign_log LAUNCH-CARD/VENUE-CHECK lines, pipeline_state.yaml | entry id; fold; coins x timeframe |
| config | Step 1b: config | candidate_strategy_config.json, backtest_spec.yaml, deviations.yaml, block_manifest.yaml | hypothesis id; deviations status; rationale lines |
| variants | Step 2: variants | variant_patches.yaml, variants/index.yaml, variant_anti_adjacency_result.yaml | n variants; kinds; anti-adjacency outcomes |
| data_gate | Data gate | variants/<v>/data_availability_gate.yaml | windows validated / total per variant |
| protocol | Protocol execution | variants/<v>/protocol_result.yaml, forecast_size_probe.yaml | trades per variant; windows run |
| replay_gate | Replay gate | config_replay_gate.yaml | verdict; series with differences |
| profit_bars | Profit bars | profit_bars_evaluation.yaml | base bars passed / total; result per variant |
| grid | Criteria grid and residual IC | grid_evaluation.yaml, residual_ic.yaml, idea_status.yaml | idea_status; FAIL cells / cells |
| claims | Claim tests | claim_measurement.yaml, claim_result_digest.yaml, variants/<v>/claim_test.yaml, findings_summary.yaml | claim_status; tests measured |
| analyst | Analyst lenses | analyst/<lens>.yaml, analyst_queries/<lens>.yaml | outcome per lens; queries; cost |
| decide_next | Decide-next | decision_record.yaml, campaign_log DECIDE line | candidates; eligible; picked |
| record | Record | registry_summary.yaml, tried_ideas.yaml, campaign_state trial rows, campaign_memory entry, campaign_log DONE line | trial rows; blocks registered by this run |

Card status: `ok` (green), `fail` (red: a FAIL, refuted, refused, invalid verdict),
`warn` (amber: INCONCLUSIVE, partial coverage, a warning line), `absent` (grey: no source
file). Each step loader returns
`{name, title, status, headlines: [{label, value}], line, sources: [...]}` for the card and,
for view 3, adds `tables: [{title, columns, rows, links?}]`, `text: [{title, body}]` and
`raw: [{path, text}]` (raw file text, 300 KB cap, truncation noted; only files under the
run folder and the brief: the campaign-wide files stay in `sources` but are not embedded).

## Artifact shapes move (operator 2026-10-23)

- Target: the as-is shape (run_098, run_099 on master today) and the next runs. Old runs
  are not a goal.
- The loaders are written against `SHAPES_run_099.md` (every run_099 artifact, its
  top-level keys and their types, generated from the files). File:line hints and this
  doc's step table are hints; the listing wins.
- Every field: absent file -> "absent"; missing key or unexpected type ->
  "unreadable (<reason>)". Each step loader is wrapped, so one broken artifact greys one
  card, never the page. A folder with only `pipeline_state.yaml` still gets a view-1 row.
- Legacy runs (a core file absent or not in the as-is shape) carry `legacy_shape: true`
  in view 1 and open to whatever loads.
- The page reads only the loaders' JSON, never YAML; a future shape change is fixed in
  the loader. Every view-3 table is also given in a narrow form:
  `{by: variant|window, options, rows_by_option: {option: [[label, value], ...]}}`.

## Mobile first (operator 2026-10-23)

Phone width (360-430 px) is the base layout; wider screens widen it.
- One column on a phone: view 2's step cards stack in pipeline order, full width; on a
  desktop (>= 900 px) they flow into a grid. No horizontal page scroll anywhere; a wide
  table scrolls inside its own container with its first column sticky.
- Touch targets >= 44 px. The breadcrumb, and in view 4 the variant and window
  selectors, sit in a sticky top bar. The raw-YAML toggle is a button.
- View 3 tables on a phone: two columns (label, value) with a variant or window
  selector, from the narrow form above; the wide grid from 900 px.
- View 4: the chart fills the width; pinch-zoom and one-finger pan on the time axis;
  the values of the bar under the finger (date, close, forecast, position, equity) in a
  fixed strip above the chart, not a tooltip. Trade markers: entries and exits only,
  >= 10 px, coloured by the trade's net sign.
- 16 px base text; system font stack; `prefers-color-scheme` dark mode; no CDN, no web
  font, no network request other than this server.
- Acceptance: the reviewer opens every view at 390 px width in a browser and reports any
  overflow or horizontal page scroll; the MVP is not done while any view has one.

## Wireframes

```
VIEW 1  Campaign                                     breadcrumb: Campaign
+-----------------------------------------------------------------------------+
| Runs (newest first)                                                         |
| run | entry | fold | coins | tf | idea_status | outcome | base bars | $ | date | dur |
| run_099 child_run_098_long_only_fold_b  B  BTCUSD,LTCUSD 1d refuted  -  n/7  ...  |
| Queue: ready [..]   blocked [id, status, reason]                            |
| Blocks: block id | validated by run | status (last status record)           |
+-----------------------------------------------------------------------------+

VIEW 2  Run                                     breadcrumb: Campaign > run_099
+-----------------------------------------------------------------------------+
| PURPOSE (brief research_goal, first paragraph; full text behind a toggle)   |
| Pre-registered outcomes: A. ...  B. ...  C. ...   (outcome: not recorded)   |
| [Launch] [1b config] [2 variants] [Data gate] [Protocol] [Replay gate]      |
| [Profit bars] [Grid+residual IC] [Claims] [Analyst] [Decide-next] [Record]  |
|  each card: colour, 2-3 numbers, one line                                    |
+-----------------------------------------------------------------------------+

VIEW 3  Step                         breadcrumb: Campaign > run_099 > Profit bars
+-----------------------------------------------------------------------------+
| table(s) for the step, e.g. bar x variant: actual vs threshold, PASS/FAIL   |
| variant names and window labels link to view 4                              |
| [show raw YAML]                                                             |
+-----------------------------------------------------------------------------+

VIEW 4  Variant in window   breadcrumb: Campaign > run_099 > base > 2020-05
+-----------------------------------------------------------------------------+
| variant [base v]  window [2020-05 v]                                        |
| pane 1: close, trade markers (entry ^, exit v, coloured by net P&L sign)    |
| pane 2: forecast            pane 3: executed position (postRebalance alloc) |
| pane 4: window equity (portfolio_value)                                     |
| chained equity across the run's windows for this variant (gaps as breaks)   |
| trades table (entry, exit, side, net %, duration)                           |
+-----------------------------------------------------------------------------+
```

Phone (390 px), the base layout:

```
VIEW 1                 VIEW 2                 VIEW 3                 VIEW 4
[Campaign]  sticky     [Campaign > 099]       [.. > Profit bars]     [.. > base > 2020-05]
run_099  refuted       PURPOSE (3 lines,      variant [base v]       [base v] [2020-05 v]
 B  BTC,LTC 1d  n/7     [more] button)        sharpe_min  x > 0  PASS strip: date close
run_098  refuted       Outcomes [show]        dsr  x >= 0.5 FAIL      forecast pos equity
 ...  (table scrolls,  [Launch      ok ]      ...                    [ price + markers ]
  first col sticky)    [1b config   ok ]      [Raw YAML] button      [ forecast        ]
Queue / Blocks         [2 variants  ok ]                             [ position        ]
 (sections below)      ... one per row                               [ equity          ]
                                                                     chained equity
                                                                     trades (2 columns)
```

## Artifact shapes that differ from the brief's data map

- `profit_bars_evaluation.yaml`: each bar is `{name, threshold, actual, result, basis,
  comparator, note, detail}`; the value field is `actual`, not `value`.
- No artifact records which pre-registered outcome letter happened. The queue's free text
  sometimes names one, but on another entry (daily_breadth_fold_b's `brief_status_reason`
  names run_099's outcome C). The viewer shows "not recorded" rather than guess.
- `pipeline_state.yaml`'s `audit_log` holds only the stages that called a model (run_099:
  innovation_expansion and the two analyst lenses); cost is the sum of what is there.
- Window bars: `artifacts/variants/<v>/protocol_result.yaml` `results[i].run_id` is the
  results stamp; `runs/run_NNN/variants/<v>/results/<stamp>/bars.csv`. A variant gated out
  (run_098 `asset_ada`) has a config and a data gate but no protocol_result.

## Sealed-window dates: option A (operator 2026-10-23)

91 of 99 run folders carry an in-range date in some file other than `bars.csv`; no
run's `bars.csv` does. Not all of these are wall-clock stamps: in run_098 they are the
policy's holdout block copied into each variant's `protocol.json`, and run_098's and
run_099's own wall-clock stamps fall outside the range (corrected 2026-10-23 after the
fixture build; the first reading called them all provenance timestamps). Ruling: `sanitize.py`
reads the range once through `tools/holdout_policy.py` (the policy next to the tool, not
under `--root`), holds it only inside that module, and never logs, returns or prints it.
Every response, the raw file text, the request log and the banner pass through
`sanitize()`/`sanitize_text()`; an in-range date becomes "[sealed-window date]",
provenance timestamps included. Forms masked: YYYY-MM-DD (with any time), compact
YYYYMMDD and results stamps, YYYY-MM; after review also slash, dot and underscore
separators, day-first and month-first numeric dates, English month-name dates and
month-name years, YYYY/MM, MM/YYYY, quarter and half labels. Known limits, not masked:
epoch numbers, ISO week and ordinal dates, two-digit years (none of the forms the
review tried appeared in any real run's responses). Error pages of the stdlib server and
its traceback log are routed through the same filter. Policy unreadable -> the server does not start. Committed fixtures
were written through the same `sanitize_text()`. Tests: no in-range date in any response;
none in the server log over a full crawl of run_099; masking of dates built from the
policy at test time; the policy is the only read outside the allowed list.

## Rulings on labels (operator 2026-10-23)

- Cost is labelled "model cost (stages that called a model)".
- Outcome letter: "not recorded"; the gap is named in D-180, nothing is built for it.
- Analyst step: when `artifacts/analyst_rerun/` exists (run_098), view 3 adds a
  "re-run on a copy" section after the lens tables; otherwise it is ignored.
