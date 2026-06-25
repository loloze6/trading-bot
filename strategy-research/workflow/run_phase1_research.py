"""
=============================================================================
PHASE 1 ORCHESTRATOR: HYPOTHESIS & VALIDATION STATE MACHINE
=============================================================================
This script runs a file-driven, autonomous state machine that generates and 
ruthlessly validates quantitative trading hypotheses BEFORE any backtest code 
is written.

THE AGENTS (DIVISION OF LABOR):
1. Hypothesis Design    : Invents the core thesis (The Concept).
2. Innovation Expansion : Designs specific, testable variants (The Blueprints).
3. Quant Validation     : The Gatekeeper. Finds lookahead bias, overfitting, 
                          or missing data. (Outputs: Approve, Refine, or Reject).
4. Refinement Planner   : Translates "Refine" rejections into concrete action 
                          plans to fix the strategy or flag missing data.

THE ROUTING LOGIC:
- ✅ Path A (Approval)  : Validation -> [Approve] -> Moves to Phase 2 (Code).
- 🔄 Path B (Logic Fix) : Validation -> [Refine] -> Refinement Planner -> 
                          Loops back to Innovation Expansion to redraw the 
                          variants using the new plan.
- ⏸️ Path C (Data Block): Validation -> [Refine] -> Refinement Planner detects 
                          missing data -> Pipeline PAUSES for human audit.

THE HUMAN-IN-THE-LOOP (HITL) RESUME:
If paused for a data audit, the human downloads the data, writes 
`human_resolution.yaml`, and runs this script with `--resume`. 
Crucially, the pipeline resumes back to QUANT VALIDATION (not Phase 2), 
forcing the agent to officially review the human's data before approving.

SAFETY GUARDRAILS:
Controlled by `pipeline_state.yaml`. If the `refinements_used` counter hits
`max_refinements_after_validation`, the loop terminates to prevent infinite 
AI hallucination cycles.
=============================================================================
"""


from pathlib import Path
import yaml
from datetime import datetime, timezone
import argparse
import os
import re
import asyncio
import tempfile
import time
import subprocess
import json
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from google import genai
from google.genai import types

ROOT = Path(".")

# Dynamic Stage Configurations
STAGE_CONFIGS = {
    "hypothesis_generation": {
        "handoff": "research_brief_to_hypothesis.yaml",
        # "required_outputs": [ARTIFACTS / "hypothesis_card.yaml"],
        "default_next": "innovation_expansion",
    },
    "innovation_expansion": {
        "handoff": "hypothesis_to_innovation_expansion.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "expanded_hypothesis_card.yaml",
        #     ARTIFACTS / "innovation_notes.yaml",
        # ],
        "default_next": "validation",
    },
    "validation": {
        "handoff": "innovation_expansion_to_validation.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "validation_protocol.yaml",
        #     ARTIFACTS / "validation_decision.yaml",
        # ],
        "default_next": "dynamic_routing", # Validation decides the next step
    },
    "refinement_planner": {
        "handoff": "validation_to_refinement.yaml",
        # "required_outputs": [ARTIFACTS / "refinement_notes.yaml"],
        "default_next": "innovation_expansion", # Route back to innovation after planning
    },
    "backtest_specification": {
        "handoff": "validation_to_backtest_specification.yaml",
        "default_next": "dynamic_routing",
    },
}

def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def update_state(path: Path, **kwargs):
    state = load_yaml(path / "pipeline_state.yaml")
    for key, value in kwargs.items():
        if isinstance(value, dict) and key in state and isinstance(state[key], dict):
            state[key].update(value) # Merge nested dicts (like counters)
        else:
            state[key] = value

    if "audit_log" not in state:
        state["audit_log"] = {}

    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_yaml(path / "pipeline_state.yaml", state)

def ensure_files(paths):
    missing = [str(p) for p in paths if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"Missing files: {missing}")

def estimate_tokens(text: str) -> int:
    """Provides a rough token estimation (1 token ≈ 4 chars)."""
    return len(str(text)) // 4

def check_context_limits(stage_name: str, full_prompt: str, max_window: int = 100000):
    """Monitors the payload size and warns/halts if nearing limits."""
    estimated_tokens = estimate_tokens(full_prompt)
    print(f"📊 [METRICS] {stage_name} Payload: ~{estimated_tokens:,} tokens")
    
    if estimated_tokens > max_window * 0.8:
        print("⚠️ WARNING: Context window is at 80% capacity. Risk of model degradation.")
    if estimated_tokens > max_window:
        raise ValueError(f"CRITICAL: Context window exceeded ({estimated_tokens:,} > {max_window:,}). Pipeline halted.")
        
    return estimated_tokens

async def run_claude_worker(stage_name: str, handoff: str, path: Path):
    
    print(f"\n🧠 [AGENT INVOKED] Waking up specialist for: {stage_name}")
    
    
    # 2. Map the stage to the correct SKILL definition
    skill_map = {
        "hypothesis_generation": "hypothesis-design",
        "innovation_expansion": "innovation-expansion",
        "validation": "quant-validation",
        "refinement_planner": "refinement-planner",
        "backtest_specification": "backtest-engineering",
    }

    skill_file_name = skill_map.get(stage_name)
    if not skill_file_name:
        raise ValueError(f"No SKILL file mapped for stage: {stage_name}")
        
    skill_path = Path(".") / "skills" / skill_file_name / "SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 3. Gather Context
    context_blocks = []
    inputs_to_read = handoff.get("required_inputs", []) + handoff.get("optional_inputs", [])
    
    for req in inputs_to_read:
        filepath = path / req["path"]
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            context_blocks.append(f"--- CONTENT OF {req['path']} ---\n{content}\n")
        elif req in handoff.get("required_inputs", []):
            raise FileNotFoundError(f"Agent strictly requires {filepath}, but it is missing.")

    # 4. Construct the strict prompt (Combining Persona + Instructions)
    full_prompt = f"""
    PERSONA AND RULES:
    {system_prompt}
    
    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}
    
    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}
    
    INSTRUCTIONS FOR OUTPUT:
    Fulfill the objective defined in the handoff. You must generate the exact deliverables requested.
    Output ONLY valid YAML blocks for your deliverables. Do not output conversational filler.
    
    You MUST use this exact format for each deliverable so my script can parse it:
    
    ```yaml
    # filename.yaml
    <your yaml content here>
    ```
    """

    # --- PRE-FLIGHT SAFETY RADAR ---
    start_time = time.time()
    check_context_limits(stage_name, full_prompt, max_window=150000)

    # 5. Invoke the Agent and Stream the Response (with strict tool constraints to enforce handoff rules)
    print("⏳ Waiting for Claude CLI response...")
    agent_output = ""
    exact_usage = {}
    total_cost = 0.0
    
    # We pass an empty allowed_tools list to prevent it from wandering off 
    # and strictly enforce our handoff file constraints.
    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(model= "claude-haiku-4-5",allowed_tools=[])
    ):
        # Accumulate text content from assistant messages
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    agent_output += block.text
        # --- Optional: NATIVE COST TRACKING ---
        if hasattr(message, "total_cost_usd"):
            exact_usage = getattr(message, "usage", {})
            total_cost = getattr(message, "total_cost_usd", 0.0)

    # --- OPTIONAL METRICS POST-FLIGHT CALCULATION ---
    execution_time = round(time.time() - start_time, 2)

    input_tokens = exact_usage.get("input_tokens", 0)
    output_tokens = exact_usage.get("output_tokens", 0)
    cache_read = exact_usage.get("cache_read_input_tokens", 0)
    cache_creation = exact_usage.get("cache_creation_input_tokens", 0)
    total_tokens = input_tokens + output_tokens + cache_read + cache_creation

    print(f"⏱️ Finished in {execution_time}s")
    print(f"💰 Cost Estimate: ${total_cost:.4f} | Tokens: {total_tokens:,} (Cache Read: {cache_read:,})")
    
    # 4. Save to the central audit ledger
    attempt_num = handoff.get('injected_context', {}).get('refinement_attempt', '0')
    log_entry = {
        f"{stage_name}_attempt_{attempt_num}": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "claude-agent-sdk",
            "execution_time_seconds": execution_time,
            "cost_usd": total_cost,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "cache_read": cache_read,
                "cache_creation": cache_creation,
                "total": total_tokens
            }
        }
    }
    update_state(path=path, audit_log=log_entry)


    # 6. Parse and Save the Deliverables
    pattern = r"```yaml\s*#\s*([a-zA-Z0-9_.]+\.yaml)\s*(.*?)```"
    matches = re.findall(pattern, agent_output, re.DOTALL)
    
    if not matches:
        print("⚠️ Warning: Could not parse standard YAML blocks. Saving raw output for debug.")
        debug_path = path / "artifacts" / f"debug_{stage_name}_raw_output.txt"
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(agent_output)
        return

    saved_files = []
    for filename, yaml_content in matches:
        dest_path = path / "artifacts" / filename.strip()
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(yaml_content.strip())
        saved_files.append(filename.strip())
        
    print(f"✅ [AGENT COMPLETE] Successfully wrote deliverables: {', '.join(saved_files)}")



# Initialize the Native Client
# It automatically picks up the GEMINI_API_KEY environment variable
client = genai.Client()

async def run_gemini_worker(stage_name: str, handoff: dict, run_dir: Path):
    print(f"\n✨ [GEMINI INVOKED] Waking up Native Gemini API for: {stage_name}")
    
    # 2. Map the stage to the correct SKILL definition
    skill_map = {
        "hypothesis_generation": "hypothesis-design",
        "innovation_expansion": "innovation-expansion",
        "validation": "quant-validation",
        "refinement_planner": "refinement-planner",
        "backtest_specification": "backtest-engineering",
    }

    skill_file_name = skill_map.get(stage_name)
    if not skill_file_name:
        raise ValueError(f"No SKILL file mapped for Gemini stage: {stage_name}")
        
    # --- FIX 3: Point to the 'skills' directory ---
    skill_path = Path(".") / "skills" / skill_file_name / "SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 2. Gather Context
    context_blocks = []
    inputs_to_read = handoff.get("required_inputs", []) + handoff.get("optional_inputs", [])
    
    for req in inputs_to_read:
        filepath = run_dir / req["path"]
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            context_blocks.append(f"--- CONTENT OF {req['path']} ---\n{content}\n")

    full_prompt = f"""
    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}
    
    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}
    """

    # --- PRE-FLIGHT SAFETY RADAR ---
    start_time = time.time()
    # Gemini has a massive context window, but we still protect our budget
    estimated_prompt_tokens = check_context_limits(stage_name, full_prompt, max_window=200000)

    print("⏳ Waiting for Gemini API response...")
    
    # --- FIX 1 & 2: Use the async '.aio' client and correct model name ---
    response = await client.aio.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2, # Keep the quant bot logical and deterministic
            max_output_tokens=4000, # <-- LAYER 3 HARD LIMIT
            safety_settings=[
                {
                    "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
            ]
        ),
        
    )
    
    agent_output = response.text

    # --- METRICS POST-FLIGHT CALCULATION ---
    execution_time = round(time.time() - start_time, 2)
    
    # Extract perfect Native Token tracking from the response object
    exact_input_tokens = response.usage_metadata.prompt_token_count
    exact_output_tokens = response.usage_metadata.candidates_token_count
    total_tokens = exact_input_tokens + exact_output_tokens

    print(f"⏱️ Finished in {execution_time}s | Output: {exact_output_tokens:,} tokens")

    # 4. Save to the central audit ledger
    attempt_num = handoff.get('injected_context', {}).get('refinement_attempt', '0')
    log_entry = {
        f"{stage_name}_attempt_{attempt_num}": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "gemini-native-api",
            "execution_time_seconds": execution_time,
            "tokens": {
                "input": exact_input_tokens,
                "output": exact_output_tokens,
                "total": total_tokens
            }
        }
    }
    update_state(path=run_dir, audit_log=log_entry)

    # 5. Simple Stage-Based Saving
    blocks = re.sub(r'^[a-zA-Z0-9_\-.]+\.yaml\s*\n', '', agent_output.strip())
    yaml_blocks = re.findall(r"```yaml\s*(.*?)\s*```", blocks, re.DOTALL)
    
    if yaml_blocks:
        # Define exactly what files each stage is supposed to emit in order
        stage_outputs = {
            "hypothesis_generation": ["hypothesis_card.yaml"],
            "innovation_expansion": ["expanded_hypothesis_card.yaml", "innovation_notes.yaml"],
            "validation": ["validation_protocol.yaml", "validation_decision.yaml"],
            "refinement_planner": ["refinement_notes.yaml"]
        }
        
        expected_files = stage_outputs.get(stage_name, [f"{stage_name}_output.yaml"])
        saved_files = []
        
        # Match each extracted block to its expected filename
        for i, block_content in enumerate(yaml_blocks):
            if i < len(expected_files):
                filename = expected_files[i]
            else:
                filename = f"{stage_name}_extra_{i}.yaml"
                
            dest_path = run_dir / "artifacts" / filename
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(block_content.strip())
            saved_files.append(filename)
            
        print(f"✅ [WORKER COMPLETE] Successfully wrote deliverables: {', '.join(saved_files)}")
    else:
        print(f"⚠️ Warning: No yaml blocks found in output. Saving raw debug file.")
        debug_path = run_dir / "artifacts" / f"debug_{stage_name}_raw_output.txt"
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(agent_output)

async def async_invoke_agent(stage_name: str, run_id: str):

    RUN_DIR = ROOT / "runs" / run_id
    HANDOFFS = RUN_DIR / "handoffs"
    config = STAGE_CONFIGS[stage_name]
    handoff_path = HANDOFFS / config["handoff"]    
    
    # 1. Load the live handoff file
    
    handoff = load_yaml(handoff_path)

    # Select enginefrom handoff file, default to Claude if not specified

    engine = handoff.get("assigned_engine", "claude")
    
    if engine == "claude":
        # Fires the Claude Agent SDK worker
        return await run_claude_worker(stage_name, handoff, RUN_DIR)
    elif engine == "gemini":
        # Fires the Gemini API worker
        return await run_gemini_worker(stage_name, handoff, RUN_DIR)

def determine_post_refinement_route(path: Path):
    """Checks if refinement requires a human pause or loops back to innovation."""
    refinement_path = path / "artifacts" / "refinement_notes.yaml"
    refinement = load_yaml(refinement_path)
    
    # Check the flag from the Refinement Planner
    implementation_allowed = refinement.get("decision", {}).get("implementation_allowed", True)
    
    if not implementation_allowed:
        print("\n⏸️ PIPELINE PAUSED: Human Intervention Required.")
        print("Please review artifacts/refinement_notes.yaml.")
        print("When complete, create artifacts/human_resolution.yaml and run with --resume.")
        update_state(path=path, status="paused_for_human")
        return "human_pause" # Halts the while loop
    
    return "innovation_expansion" # Otherwise, loop back for another try

def determine_post_validation_route(path: Path):
    """Once validation is complete, read the decision from validation_decision artifact and route accordingly:
    - If "approve": proceed to Phase 2 development of backtest 
    - If "refine": route to refinement planner (unless max refinements reached, then reject)
    - If "reject": mark as completed and rejected
    """
    decision_path = path / "artifacts" / "validation_decision.yaml"
    decision = load_yaml(decision_path)
    status = decision.get("status").strip().lower()
    
    state = load_yaml(path / "pipeline_state.yaml")
    refinements_used = state.get("counters", {}).get("refinements_used", 0)
    max_refinements = state.get("governance", {}).get("max_refinements_after_validation", 2)

    if status in ("approve", "conditional_approve"):
        if status == "conditional_approve":
            conditions = decision.get("conditions", [])
            print(f"\n⚠️  CONDITIONAL APPROVAL — conditions to respect in backtest config:")
            for c in conditions:
                print(f"   - {c}")
        update_state(path=path, flags={"validation_approved": True})
        return "backtest_specification"
    
    elif status == "refine":
        if refinements_used >= max_refinements:
            print(f"🛑 Refinement limit reached ({max_refinements}). Rejecting hypothesis.")
            return "completed_rejected"
        return "refinement_planner"
    
    elif status == "reject":
        return "completed_rejected"
    
    else:
        raise ValueError(f"Unknown validation status: {status}")

def determine_post_spec_route(path: Path):
    KNOWN_STATUSES = {"spec_ready", "component_gap"}
    decision = load_yaml(path / "artifacts" / "decision.yaml")
    status = decision.get("status", "").strip().lower()
    if status == "spec_ready":
        return "ready_for_protocol"     # terminal this iteration; protocol run manually
    if status == "component_gap":
        update_state(path=path, status="paused_for_human")
        print("\n⏸️ COMPONENT GAP: hypothesis needs an engine piece that does not exist. "
              "See artifacts/decision.yaml; extend the engine per STRATEGY_EXTENDING.md, then resume.")
        return "human_pause"
    if status not in KNOWN_STATUSES:
        update_state(path=path, status="paused_for_human")
        print(f"\n⏸️ UNEXPECTED STATUS '{status}' from backtest_specification — "
              f"SKILL.md may need a new status case, or this run had bad inputs. "
              f"Rationale: {decision.get('rationale', '<none>')}")
        return "human_pause"

def resume_pipeline(run_id: str):
    RUN_DIR = ROOT / "runs" / run_id
    state = load_yaml(RUN_DIR / "pipeline_state.yaml")
    if state.get("status") != "paused_for_human":
        print("Pipeline is not paused. Nothing to resume.")
        return

    resolution_path = RUN_DIR / "artifacts" / "human_resolution.yaml"
    ensure_files([resolution_path])
    
    resolution = load_yaml(resolution_path)
    if resolution.get("status") == "resolved_proceed":
        print("✅ Human resolution verified. Resuming pipeline...")
        # Inject the human's paths directly into the state so the next agent can see them
        update_state(
            path=RUN_DIR, 
            status="active",
            current_stage="human_resolution",
            pending_stage="backtest_specification", # Move to Phase 2
            injected_human_context=resolution.get("injected_context")
        )
        run_loop()
    else:
        print("❌ Human marked issue as unresolvable. Ending run.")
        update_state(path=RUN_DIR, status="rejected", pending_stage="completed_rejected")

def run_loop(run_id: str):
    """Main loop to run through the stages of Phase 1 with dynamic routing and state management.
    1- Load State from current run folder
    2- From the config (top of this file), determine the current pending stage its handoff file, required outputs, and default next stage
    3- Verify required handoff files exist before invoking the agent
    4- Run the Agent
    5- Validate required output artifacts were created
    6- Handle Dynamic Routing & Counters based on agent outputs and current state
        6.1 For validation, route to refinement if "refine", completed_rejected if "reject", or next phase if "approve"
        6.2 For refinement planner, increment a refinement counter and route back to innovation expansion
    7 -Mark completed and stage next phase
    
    """
    RUN_DIR = ROOT / "runs" / run_id
    ARTIFACTS = RUN_DIR / "artifacts"
    HANDOFFS = RUN_DIR / "handoffs"
    STATE_FILE = RUN_DIR / "pipeline_state.yaml" # Updated to your new state file
    state = load_yaml(STATE_FILE)
    
    while True:
        current_stage = state.get("pending_stage")
         
        TERMINAL_PREFIXES = ("completed", "rejected", "ready_for_protocol", "human_pause", "failed_validation")
        if not current_stage or current_stage.startswith(TERMINAL_PREFIXES):
            print(f"🏁 Pipeline finished. Final state: {current_stage}")
            break

        # --- Optional: TOKEN CIRCUIT BREAKER ---
        budget = 300000
        # budget = state.get("governance", {}).get("max_total_tokens_per_run", 80000)
        audit = state.get("audit_log", {})
        
        total_tokens_used = 0
        for entry in audit.values():
            # Support both the SDK's exact dict and our manual estimator's flat integer
            if isinstance(entry.get("tokens"), dict):
                total_tokens_used += entry["tokens"].get("total", 0)
            else:
                total_tokens_used += entry.get("total_estimated_tokens", 0)
        
        if total_tokens_used > budget:
            print(f"🛑 RUN TERMINATED: Token budget exceeded ({total_tokens_used:,} > {budget:,}).")
            update_state(path=RUN_DIR, status="rejected_budget_exceeded")
            break
        # ----------------------------------

        print(f"\n⚙️ Starting stage: {current_stage}")
        config = STAGE_CONFIGS[current_stage]
        #Each stage has Handodff YAML (inputs) / required output and default next stage
        handoff_path = HANDOFFS / config["handoff"]
        


        # 1. Verify required inputs exist before invoking the agent
        handoff_data = load_yaml(handoff_path)
        required_input_paths = [RUN_DIR / x["path"] for x in handoff_data.get("required_inputs", [])]
        ensure_files(required_input_paths)

        # 2. Update state to running
        update_state(path=RUN_DIR, current_stage=current_stage, status="running")

        try:
            # 3. Inject dynamic state directly into the run's existing handoff file
            handoff_data["run_id"] = state.get("run_id", run_id)
            
            # Create or overwrite the injected_context block with the latest dynamic info from the state (like counters or human context)
            handoff_data["injected_context"] = {
                "refinement_attempt": str(state.get("counters", {}).get("refinements_used", 0)),
                "human_data_paths_injected": "true" if state.get("injected_human_context") else "false"
            }
            if state.get("injected_human_context"): # If there is human context in the state, merge it into the injected_context for the agent to consume
                handoff_data["injected_context"].update(state.get("injected_human_context"))

            # Save it right back over the existing file
            save_yaml(handoff_path, handoff_data)

            # Invoke the Agent
            asyncio.run(async_invoke_agent(current_stage, run_id))

            
            # # 4. Validate output artifacts were created
            # ensure_files(config["required_outputs"])

            # 4. Validate output artifacts were created
            expected_outputs = [RUN_DIR / "artifacts" / x for x in handoff_data.get("deliverables", [])]
            ensure_files(expected_outputs)

            # 5. Handle Dynamic Routing & Counters
            next_stage = config["default_next"]
            
            if current_stage == "validation":
                next_stage = determine_post_validation_route(RUN_DIR) # Used to trigger state of refinement until (Artifact State is validated OR max refinement reached OR rejected)
                
            elif current_stage == "refinement_planner":
                # Increment the refinement counter
                current_count = state.get("counters", {}).get("refinements_used", 0)
                update_state(path=RUN_DIR, counters={"refinements_used": current_count + 1})

                # Ask the new function where to go next
                next_stage = determine_post_refinement_route(RUN_DIR) #Checks if refinement requires a human pause or loops back to innovation.

                if next_stage == "human_pause":
                    break # Break the while loop to stop the script cleanly

            elif current_stage == "backtest_specification":
                next_stage = determine_post_spec_route(RUN_DIR)
                if next_stage == "ready_for_protocol":
                    spec = load_yaml(ARTIFACTS / "backtest_spec.yaml")
                    config_obj = spec.get("config")
                    candidate_path = ARTIFACTS / "candidate_strategy_config.json"
                    with open(candidate_path, "w", encoding="utf-8") as f:
                        json.dump(config_obj, f, indent=2)
                    validator = Path("..") / "trading-bot" / "tools" / "validate_config.py"
                    result = subprocess.run(
                        ["python", str(validator), str(candidate_path)],
                        capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        report = result.stdout + result.stderr
                        report_path = ARTIFACTS / "spec_validation_report.txt"
                        with open(report_path, "w", encoding="utf-8") as f:
                            f.write(report)
                        print("❌ Config schema violations found:")
                        print(report)
                        update_state(path=RUN_DIR, status="failed_validation")
                        next_stage = "failed_validation"
                    else:
                        print("✅ config schema-valid; run the protocol manually:")
                        print(f"  python tools/run_protocol.py runs/{run_id}/artifacts/candidate_strategy_config.json protocols/baseline_v1.json")
                elif next_stage == "human_pause":
                    break

            # 6. Mark completed and stage next phase
            completed = state.get("completed_stages", [])
            completed.append(current_stage)
            
            update_state(path=RUN_DIR, 
                status="active" if next_stage != "completed_rejected" else "rejected",
                completed_stages=completed,
                current_stage=current_stage,
                pending_stage=next_stage
            )
            
            # Reload state for the next while loop iteration
            state = load_yaml(STATE_FILE)

        except Exception as e:
            print(f"❌ Error in stage {current_stage}: {e}")
            update_state(path=RUN_DIR, status="failed", last_error=str(e))
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume from human pause")
    parser.add_argument("run_id", type=str, help="The ID for the new run (e.g., run_002)")
    args = parser.parse_args()

    if args.resume:
        resume_pipeline(args.run_id)
    else:
        run_loop(args.run_id)