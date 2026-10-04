# E-068 3b: offline measurement of the claim-test review -- FAIL, parked (CUL-397)

The review call (`orchestrator.claim_test_review`) was to ship only if all 6 real calls met
expectations fixed before the first call (`measure_review.py` docstring): A must flag the units
(1h bars, "next 1 to 10 days", horizons 1-10 bars), B must not (the control, "next 1-4 hours",
horizons 1-4), C must flag run_070's tests as selecting on the close's level instead of the
claimed 1h move.

Result (`summary_run1.md`, raw answers and prompts in `raw/run1/`): A 2/2, B 2/2, **C 0/2** --
both answers judged "close in the top 10% of the trailing 100 bars" to match the statement
(which itself also says "after extreme-high closes (top 10%)"). Verdict **FAIL**; the review
code and flag were removed from the branch (items 1-4 of 3b stay).

- 6 calls, $0.2908 (`claude-haiku-4-5`, closed-book, the pipeline's own options); most of the
  cost is 5,000-11,000 output tokens per call for a ~15-line answer.
- The one allowed prompt revision was not run: it would have doubled the approved spend
  (about $0.30) for the same 6 calls.
- A and B never reached step 1b, so each got a stated synthetic forecast manifest
  (`inputs/A|B/block_manifest.yaml`). B's original card is not valid YAML as a whole; only its
  `hypothesis_id`, `timeframe` and `claim` block (all the review reads) were parsed
  (`work/B/artifacts/hypothesis_card.yaml`).
- `measure_review.py` imports the review's prompt builder and answer check from
  `workflow/run_phase1_research.py`; they exist only at commit `603aa23e` (the measured state).
  Check that commit out to re-run it.
