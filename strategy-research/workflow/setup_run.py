import argparse
import contextlib
import shutil
import yaml
import sys
from pathlib import Path


# CUL-12: the emoji status prints below crash on a Windows cp1252 console
# (UnicodeEncodeError) the moment stdout is redirected/piped/logged — exactly an
# unattended campaign run. Degrade unencodable glyphs to '?' rather than raising.
# Guarded: pytest's captured stdout has no .reconfigure, and a stream may reject
# it (OSError) — never crash a context the raw prints already survived. getattr
# because typeshed types sys.stdout as TextIO, which does not declare reconfigure
# (present on the real TextIOWrapper since 3.7).
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")


ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "workflow_artifacts" / "templates" / "handoffs"


def _is_fresh_or_absent(state_path: Path) -> bool:
    """
    F8 (2026-07-04): True if no pipeline_state.yaml exists yet, or if it exists but
    represents an untouched scaffold (no stages completed, still waiting on
    hypothesis_generation). False means this run has already made real progress —
    overwriting it would be exactly what a run-ID collision looked like in practice
    (run_043's reframe computing "run_044" while an unrelated run_044 was already
    mid-pipeline, and vice versa the next time).
    """
    if not state_path.exists():
        return True
    try:
        existing = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return False  # unparseable — do not blindly overwrite
    return (
        not existing.get("completed_stages")
        and existing.get("pending_stage", "hypothesis_generation") == "hypothesis_generation"
    )


def create_pipeline_state(run_dir: Path, run_id: str):
    """Generates a fresh pipeline_state.yaml for the new run. And stores it in the run directory.

    F8 (2026-07-04): refuses to overwrite a run that already has real progress —
    see _is_fresh_or_absent(). This is a backstop independent of whether the caller's
    run-ID allocation is correct; even a correct allocator should never need this path,
    but a defect there must fail loudly here instead of silently destroying state.
    """
    state_path = run_dir / "pipeline_state.yaml"
    if not _is_fresh_or_absent(state_path):
        raise RuntimeError(
            f"REFUSING TO OVERWRITE: {state_path} already exists and represents a run "
            f"in progress or completed (non-empty completed_stages, or pending_stage != "
            f"'hypothesis_generation'). This is very likely a run-ID collision (F8) — "
            f"'{run_id}' was computed as a supposedly-free ID but is already in use. "
            f"Fix the caller's ID allocation; do not delete this file to work around it."
        )
    state = {
        "run_id": run_id,
        "status": "active",
        "current_stage": None,
        "pending_stage": "hypothesis_generation",
        "completed_stages": [],
        "artifacts": {},
        "governance": {
            "max_hypothesis_variants_per_cycle": 3,
            "max_refinements_after_validation": 2,
            "max_reruns_after_analysis": 1,
            "max_required_reads_per_stage": 3
        },
        "counters": {
            "refinements_used": 0,
            "reruns_used": 0
        },
        "flags": {
            "holdout_reserved": False,
            "validation_approved": False,
            "screening_passed": False,
            "walk_forward_passed": False
        },
        "last_summary": None
    }

        
    state_path = run_dir / "pipeline_state.yaml"
    with open(state_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)
    print(f"✅ Created: {state_path}")

def setup_run(run_id: str):
    run_dir = ROOT / "runs" / run_id
    artifacts_dir = run_dir / "artifacts"
    handoffs_dir = run_dir / "handoffs"

    # 1. Create directories for artifacts and handoff in the new run
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    handoffs_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directories for {run_id}")

    # 2. Generate initial pipeline state yaml 
    create_pipeline_state(run_dir, run_id)

    # 3. Take templates in template / handoff and copy them into the new run's handoff directory.
    if not TEMPLATES_DIR.exists():
        print(f"⚠️ Warning: Templates directory not found at {TEMPLATES_DIR}.")
        print("Please create it and add your master handoff files.")
    else:
        copied_count = 0
        for template_file in TEMPLATES_DIR.glob("*.yaml"):
            dest_file = handoffs_dir / template_file.name
            shutil.copy(template_file, dest_file)
            copied_count += 1
        print(f"✅ Copied {copied_count} handoff templates to {handoffs_dir}")

    # 4. Create an empty research_brief.yaml prompt if not existing yet in the artifacts directory.
    brief_path = artifacts_dir / "research_brief.yaml"
    if not brief_path.exists():
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write("# TODO: Paste your research brief configuration here.\n")
        print(f"📝 Created blank brief: {brief_path}")

    print(f"\n🚀 Setup complete! Fill out {brief_path} and execute your run.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new quant research run.")
    parser.add_argument("run_id", type=str, help="The ID for the new run (e.g., run_002)")
    args = parser.parse_args()
    
    setup_run(args.run_id)