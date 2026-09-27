"""
E-060 composition: the names shared by tools/composition.py,
tools/decide_next.py, workflow/run_campaign.py and
workflow/run_phase1_research.py -- ONE definition each (code review fix 10).
No imports, so any of them can import it without weight.
"""
# The code-written composition manifest (next to the variant configs, and
# copied into a composition run's artifacts/).
MANIFEST_FILENAME = "composition_manifest.yaml"
# Queue `origin` of an R1 composition entry (tools/record_schema.py lists it).
ORIGIN_COMPOSITION = "composition"
# Where R1 writes each composition's variant configs + manifest.
COMPOSITIONS_DIR = "campaign_record/compositions"
# The composition record (entries + failure rows), read by
# tools/composite_cache.py and decide-next's R1.
COMPOSITIONS_FILE = "campaign_record/compositions.yaml"
