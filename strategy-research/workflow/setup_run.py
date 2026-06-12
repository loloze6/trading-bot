import argparse
import shutil
import yaml
from pathlib import Path


ROOT = Path(".")
TEMPLATES_DIR = ROOT / "templates" / "handoffs"

def create_pipeline_state(run_dir: Path, run_id: str):
    """Generates a fresh pipeline_state.yaml for the new run. And stores it in the run directory."""
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