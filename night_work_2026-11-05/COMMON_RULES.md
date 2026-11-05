# Common rules for night work round 4 (operator request, 2026-11-05: "doc, cleaning, refacto, standardization and organisation, structure")

Repo /home/user/trading-bot. SR = strategy-research/, TB = trading-bot/, RP = SR/workflow/run_phase1_research.py,
RC = SR/workflow/run_campaign.py. Code is master as of 2026-10-28 plus night-work doc commits.

- Edit only the files your task names; never git add/commit/push (the lead commits after review).
- Never read any "## Inspector notes" section of guided_tour/ files; never open guided_tour/_post_tour/ (sealed from the operator).
  Do not edit anything under guided_tour/.
- Do not edit code (.py), configs (SR/config/*.yaml, TB/config/*), schemas, skills or prompt templates
  (SR/workflow_artifacts/) unless your task says so. The operator's PC holds uncommitted edits to the configs.
- Docs describe the COMMITTED code and its DEFAULTS (a flag's default where the code reads it, and the
  committed config). Do not rewrite docs to the operator's live flag state.
- Never write any date from SR/config/campaign_data_policy.yaml, any holdout date range, or a protocol window
  label; refer to the policy file. If you must look at text that may contain such dates, mask YYYY-MM-DD before
  printing. Never open TB/local_data/ or anything named holdout_sealed; exclude TB/local_data/ from every
  recursive search (grep --exclude-dir=local_data, find -path '*/local_data' -prune).
- No runs, backtests or pipeline scripts. A command's --help is fine only for tools whose --help is pure
  argparse (check the code first: no side effects before argument parsing); otherwise read the argparse code.
- Tests: venv at /tmp/claude-0/-home-user-trading-bot/701d5161-06df-5dc0-bab6-a240a8f6c04d/scratchpad/venv.
  Run SR tests from SR/ and TB tests from TB/ with `CI=true PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -m pytest -q <files>`.
  Run only the tests that read the files you changed (grep SR/tests, TB/tests for the file name and for quoted
  strings you changed).
- Facts with file:line. Only fix what is unambiguous; list everything else.
