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
import sys
import shutil
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from google import genai
from google.genai import types

ROOT = Path(".")
CAMPAIGN_STATE_PATH = ROOT / "campaign_state.yaml"

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
    "protocol_execution": {
        "handoff": "backtest_spec_to_protocol_execution.yaml",
        "default_next": "verdict_interpreter",
    },
    "verdict_interpreter": {
        "handoff": "protocol_to_verdict_interpreter.yaml",
        "default_next": "dynamic_routing",
    },
    "campaign_review": {
        "handoff": "campaign_review.yaml",
        "default_next": "dynamic_routing",
    },
}

# ---------------------------------------------------------------------------
# Campaign state (B3) — cross-run memory spanning all runs of one research question
# ---------------------------------------------------------------------------

def load_campaign_state() -> dict:
    """Load campaign_state.yaml, creating a blank one if absent."""
    if not CAMPAIGN_STATE_PATH.exists():
        return {
            "campaign_id":               "default",
            "research_question":         "",
            "runs":                      [],
            "altitude_history":          [],
            "recent_parameter_dimensions": [],
            "failed_families":           [],
            "instruments_tried":         [],
            "components_built":          [],
            "timeframes_tried":          ["1h"],
            "diagnostics_log":           [],
            "status":                    "active",
        }
    return load_yaml(CAMPAIGN_STATE_PATH)

def _save_campaign_state(state: dict):
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_yaml(CAMPAIGN_STATE_PATH, state)

def update_campaign_state_after_run(run_id: str, altitude: str, dimension: str,
                                     family: str, outcome: str, diagnostics: dict):
    """Append one run's outcome to campaign history and update derived fields."""
    state = load_campaign_state()
    state.setdefault("runs", [])
    if run_id not in state["runs"]:
        state["runs"].append(run_id)

    state.setdefault("altitude_history", [])
    state["altitude_history"].append({
        "run": run_id, "altitude": altitude,
        "dimension": dimension, "family": family, "outcome": outcome,
    })

    if altitude == "parameter" and dimension:
        dims = state.setdefault("recent_parameter_dimensions", [])
        if dimension not in dims:
            dims.append(dimension)

    state.setdefault("diagnostics_log", [])
    state["diagnostics_log"].append({"run": run_id, **diagnostics})

    _save_campaign_state(state)

def record_pivot(family: str):
    """Record a failed hypothesis family and reset parameter-dimension counter."""
    state = load_campaign_state()
    state.setdefault("failed_families", [])
    if family:
        state["failed_families"].append(family)
    state["recent_parameter_dimensions"] = []   # reset for new hypothesis
    _save_campaign_state(state)

def record_escalation(target: str, detail: str, protocol_path: str = None):
    """Record a search-space escalation."""
    state = load_campaign_state()
    if target == "instrument":
        state.setdefault("instruments_tried", [])
        if detail and detail not in state["instruments_tried"]:
            state["instruments_tried"].append(detail)
    elif target == "timeframe":
        state.setdefault("timeframes_tried", [])
        if detail and detail not in state["timeframes_tried"]:
            state["timeframes_tried"].append(detail)
    elif target == "new_component":
        state.setdefault("components_built", [])
        if detail and detail not in state["components_built"]:
            state["components_built"].append(detail)
    if protocol_path:
        state["last_escalation"] = {"target": target, "detail": detail, "protocol_path": protocol_path}
    _save_campaign_state(state)


def _mark_campaign_status(status: str):
    """Set the top-level status field in campaign_state."""
    state = load_campaign_state()
    state["status"] = status
    _save_campaign_state(state)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _quote_yaml_line(line: str) -> str:
    """Quote the value portion of a single YAML line that is causing a parse error."""
    import re
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    # List item scalar
    if stripped.startswith("- "):
        value = stripped[2:]
        if value and not value[0] in ('"', "'", "|", ">", "{", "["):
            q = value.replace('"', "'")
            return " " * indent + '- "' + q + '"'
    # Mapping value
    m = re.match(r'^(\s*)([\w _\-./]+):\s+(.+)$', line)
    if m:
        pre, key, value = m.groups()
        if value and not value[0] in ('"', "'", "|", ">", "{", "[", "~"):
            q = value.replace('"', "'")
            return pre + key + ': "' + q + '"'
    return line


def _repair_yaml(content: str, source: str = "") -> str:
    """
    Iteratively repair LLM-generated YAML by using the parser's own error marks
    to find the exact failing line, quoting its value, and retrying.
    Handles both list-item colons and inline string colons.
    Logs each repair so silent fixes are auditable.
    """
    attempt = content
    for _ in range(30):
        try:
            list(yaml.safe_load_all(attempt))
            return attempt  # parsed successfully
        except yaml.YAMLError as e:
            mark = getattr(e, "problem_mark", None) or getattr(e, "context_mark", None)
            if mark is None:
                break
            line_idx = mark.line
            lines = attempt.split("\n")
            if line_idx >= len(lines):
                break
            original = lines[line_idx]
            fixed_line = _quote_yaml_line(original)
            if fixed_line == original:
                break  # no change possible — give up
            tag = f" [{source}]" if source else ""
            print(f"[YAML-REPAIR]{tag} line {line_idx + 1} quoted"
                  f"\n    was: {original[:120]}"
                  f"\n    now: {fixed_line[:120]}")
            lines[line_idx] = fixed_line
            attempt = "\n".join(lines)
    return attempt


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # First pass: standard parse (handles well-formed YAML)
    try:
        docs = list(yaml.safe_load_all(content))
        return docs[0] if docs else None
    except yaml.YAMLError:
        pass
    # Second pass: iterative repair (handles LLM colon/multi-doc errors)
    repaired = _repair_yaml(content, source=Path(path).name)
    docs = list(yaml.safe_load_all(repaired))
    return docs[0] if docs else None

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
    for p in paths:
        p = Path(p)
        if p.suffix in ('.yaml', '.yml'):
            try:
                yaml.safe_load(p.read_text(encoding='utf-8'))
            except yaml.YAMLError as e:
                raise ValueError(f"YAML parse error in {p.name}: {e}")

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
        "verdict_interpreter": "verdict-interpreter",
        "campaign_review": "campaign-review",
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

    YAML FORMATTING RULES (violations will crash the pipeline):
    - Any string value containing a colon (:) MUST be wrapped in double quotes.
    - Example bad:  description: Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs
    - Example good: description: "Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs"
    - When in doubt, quote the entire value.

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
        "verdict_interpreter": "verdict-interpreter",
        "campaign_review": "campaign-review",
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

    YAML FORMATTING RULES (violations will crash the pipeline):
    - Any string value containing a colon (:) MUST be wrapped in double quotes.
    - Example bad:  description: Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs
    - Example good: description: "Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs"
    - When in doubt, quote the entire value.
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

async def run_tool_worker(stage_name: str, run_id: str):
    """Executes a deterministic tool stage. No LLM call. No token cost."""
    RUN_DIR = ROOT / "runs" / run_id
    ARTIFACTS = RUN_DIR / "artifacts"
    TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"

    if stage_name == "protocol_execution":
        config_path     = ARTIFACTS / "candidate_strategy_config.json"
        # Protocol selection: replication_diagnostic → baseline_v1.json;
        # forced_diagnostic → protocol named in run_context.yaml; else → campaign escalation path.
        run_ctx_path = ARTIFACTS / "run_context.yaml"
        run_ctx = (load_yaml(run_ctx_path) or {}) if run_ctx_path.exists() else {}
        run_type = run_ctx.get("run_type", "")
        if run_type == "replication_diagnostic":
            print("🔁 replication_diagnostic run — ignoring last_escalation, using baseline_v1.json")
            protocol_path = ROOT / "protocols" / "baseline_v1.json"
        elif run_type == "forced_diagnostic":
            proto_name = run_ctx.get("protocol", "baseline_v1.json")
            protocol_path = ROOT / "protocols" / proto_name
            print(f"🔬 forced_diagnostic run — using protocol: {proto_name}")
        else:
            campaign = load_campaign_state()
            last_escalation = campaign.get("last_escalation") or {}
            protocol_path_str = last_escalation.get("protocol_path")
            protocol_path = Path(protocol_path_str) if protocol_path_str else ROOT / "protocols" / "baseline_v1.json"
        validation_path = ARTIFACTS / "validation_protocol.yaml"

        cmd = [
            str(TBOT_PYTHON), str(ROOT / "tools" / "run_protocol.py"),
            str(config_path), str(protocol_path),
            "--validation-protocol", str(validation_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            raise RuntimeError(f"run_protocol.py failed:\n{result.stderr}")

        summaries = sorted(
            (ROOT / "results" / "protocols").glob("*/protocol_summary.json"),
            key=lambda p: p.stat().st_mtime,
        )
        if not summaries:
            raise FileNotFoundError("protocol_summary.json not found after protocol run")
        latest = summaries[-1]

        with open(latest, encoding="utf-8") as f:
            summary = json.load(f)
        save_yaml(ARTIFACTS / "protocol_result.yaml", summary)
        hv = (summary.get("hypothesis_verdict") or {}).get("verdict", "unknown")
        print(f"✅ Protocol complete. Hypothesis verdict: {hv}")

        # Verify Phase A diagnostics are present
        result_data = load_yaml(ARTIFACTS / "protocol_result.yaml")
        hv_block = result_data.get("hypothesis_verdict") or {}
        diagnostics = hv_block.get("diagnostics") or {}
        missing = [f for f in ["median_gross_pnl", "median_forecast_return_corr",
                                "median_cost_drag_pct"] if diagnostics.get(f) is None]
        if missing:
            print(f"⚠️ WARNING: diagnostics block missing fields: {missing}")
            print("   Phase A metrics unavailable — verdict_interpreter will have reduced signal.")
            print("   Check run_artifact.py build_core and ensure trading-bot venv has scipy.")
        else:
            print(f"✅ Diagnostics verified: corr={diagnostics['median_forecast_return_corr']:.3f}, "
                  f"cost_drag={diagnostics['median_cost_drag_pct']:.1f}%, "
                  f"gross_pnl={diagnostics['median_gross_pnl']:.2f}")
    else:
        raise ValueError(f"No tool implementation for stage: {stage_name}")


async def async_invoke_agent(stage_name: str, run_id: str):
    tool_stages = {"protocol_execution"}
    if stage_name in tool_stages:
        await run_tool_worker(stage_name, run_id)
        return

    RUN_DIR = ROOT / "runs" / run_id
    HANDOFFS = RUN_DIR / "handoffs"
    config = STAGE_CONFIGS[stage_name]
    handoff_path = HANDOFFS / config["handoff"]

    # 1. Load the live handoff file
    handoff = load_yaml(handoff_path)

    # Select engine from handoff file, default to Claude if not specified
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

def _create_remaining_handoffs(run_id: str, run_dir: Path):
    """Write protocol_execution and verdict_interpreter handoffs for runs missing them."""
    handoffs = run_dir / "handoffs"
    pe_path = handoffs / "backtest_spec_to_protocol_execution.yaml"
    vi_path = handoffs / "protocol_to_verdict_interpreter.yaml"

    if not pe_path.exists():
        save_yaml(pe_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "backtest_specification", "to_stage": "protocol_execution",
            "assigned_engine": "tool",
            "objective": "Run the full walk-forward protocol against the emitted config, "
                         "evaluated against this hypothesis's specific validation criteria.",
            "required_inputs": [
                {"path": "artifacts/candidate_strategy_config.json",
                 "reason": "the config to backtest"},
                {"path": "artifacts/validation_protocol.yaml",
                 "reason": "hypothesis-specific success criteria for verdict evaluation"},
            ],
            "deliverables": ["protocol_result.yaml"],
        })

    if not vi_path.exists():
        save_yaml(vi_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "protocol_execution", "to_stage": "verdict_interpreter",
            "assigned_engine": "claude",
            "objective": "Interpret backtest findings against hypothesis-specific criteria. "
                         "Choose the correct altitude (refine/pivot/escalate/kill/promote) "
                         "based on diagnostics and campaign history. Produce the matching artifact.",
            "required_inputs": [
                {"path": "artifacts/protocol_result.yaml",
                 "reason": "backtest findings, hypothesis verdict, and diagnostics block"},
                {"path": "artifacts/validation_protocol.yaml",
                 "reason": "original success criteria and failure modes to interpret against"},
                {"path": "artifacts/backtest_spec.yaml",
                 "reason": "maps config choices to hypothesis claims for failure attribution"},
                {"path": "artifacts/research_brief.yaml",
                 "reason": "original research question and constraints"},
            ],
            "optional_inputs": [
                {"path": "../../campaign_state.yaml",
                 "reason": "cross-run altitude history; drives circuit-breaker altitude decisions"},
            ],
            "deliverables": ["verdict_interpretation.yaml"],
            "constraints": [
                "Change at most one hypothesis dimension in proposed_brief.yaml (refine case).",
                "Do not recommend components absent from STRATEGY_CONFIG_REFERENCE.md.",
                "Accept protocol_result.yaml numbers as truth — do not re-evaluate.",
                "Populate altitude_justification with the specific diagnostic value used.",
                "Do not emit both proposed_brief.yaml AND escalation_request.yaml.",
            ],
            "stop_conditions": [
                "All evaluable approve criteria pass → status: promote, emit research_decision.yaml.",
                "Two or more reject criteria confirmed → status: kill, emit research_decision.yaml.",
            ],
        })


def _scaffold_next_run(next_run_id: str):
    """Scaffold next run directory only — no brief copy."""
    subprocess.run([sys.executable, str(ROOT / "workflow" / "setup_run.py"), next_run_id])


def setup_next_run(current_run_path: Path, next_run_id: str):
    """Scaffold next run and copy proposed_brief as its research_brief. Refine path only."""
    _scaffold_next_run(next_run_id)
    proposed  = current_run_path / "artifacts" / "proposed_brief.yaml"
    next_brief = ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml"
    shutil.copy(proposed, next_brief)
    print(f"✅ {next_run_id} scaffolded with proposed brief from {current_run_path.name}")


def _next_run_id(run_id: str) -> str:
    """Increment the numeric suffix: run_013 → run_014."""
    parts = run_id.rsplit("_", 1)
    return f"{parts[0]}_{int(parts[1]) + 1:03d}" if len(parts) == 2 and parts[1].isdigit() else f"{run_id}_next"


def _next_instrument_from_universe(campaign: dict) -> dict:
    """
    Given current campaign state, return the next instrument to try from coin_universe.yaml.
    Returns: {symbol, category, timeframe} or None if all tried.
    """
    import yaml
    universe_path = ROOT / "coin_universe.yaml"
    if not universe_path.exists():
        return None

    universe = yaml.safe_load(universe_path.read_text(encoding="utf-8"))
    tried = set(campaign.get("instruments_tried", []))
    raw_tf = campaign.get("timeframes_tried", ["1h"])[-1]
    # Guard: timeframes_tried may contain prose strings if a corruption occurred.
    # Extract the first clean timeframe identifier; default to "1h" if none found.
    import re as _re
    _tf_match = _re.search(r'\b(1m|5m|15m|30m|1h|2h|4h|6h|12h|1d|3d|1w)\b', raw_tf)
    current_tf = _tf_match.group(1) if _tf_match else "1h"

    # Walk escalation_order by priority
    for step in sorted(universe["escalation_order"]["sequence"],
                       key=lambda x: x["priority"]):
        cat_name = step["category"]
        cat = universe["categories"].get(cat_name, {})
        for coin in cat.get("coins", []):
            symbol = coin["symbol"]
            if symbol not in tried:
                return {
                    "symbol": symbol,
                    "category": cat_name,
                    "timeframe": current_tf,
                    "strategy_affinity": cat.get("strategy_affinity", []),
                    "data_cached": coin.get("data_cached", False),
                }
    return None   # all instruments exhausted


def _next_timeframe_from_universe(campaign: dict):
    """Return the next timeframe to try, or None if all tried."""
    import yaml
    universe = yaml.safe_load((ROOT / "coin_universe.yaml").read_text(encoding="utf-8"))
    tried = set(campaign.get("timeframes_tried", ["1h"]))
    for step in universe["timeframe_escalation"]["sequence"]:
        if step["timeframe"] not in tried:
            return step["timeframe"]
    return None


def _create_escalation_protocol(symbol: str, timeframe: str) -> Path:
    """
    Create a new protocol file for the escalated instrument.
    Does NOT modify baseline_v1.json -- creates a new file in protocols/.
    Returns the path to the new protocol file.
    """
    import json
    baseline_path = ROOT / "protocols" / "baseline_v1.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    escalation = dict(baseline)
    escalation["symbols"] = [symbol]
    escalation["timeframe"] = timeframe
    escalation["_escalation_note"] = (
        f"Auto-generated for instrument escalation to {symbol}. "
        f"Derived from baseline_v1.json. Do not edit manually."
    )
    proto_name = f"escalation_{symbol.lower()}_{timeframe}.json"
    proto_path = ROOT / "protocols" / proto_name
    proto_path.write_text(json.dumps(escalation, indent=2), encoding="utf-8")
    print(f"✅ Created escalation protocol: {proto_path.name}")
    return proto_path


def _create_timeframe_protocol(timeframe: str) -> Path:
    """Create a new protocol file for a timeframe escalation."""
    import json
    baseline_path = ROOT / "protocols" / "baseline_v1.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    escalation = dict(baseline)
    escalation["timeframe"] = timeframe
    escalation["_escalation_note"] = (
        f"Auto-generated for timeframe escalation to {timeframe}. "
        f"Derived from baseline_v1.json."
    )
    proto_name = f"escalation_tf_{timeframe.replace('/', '_')}.json"
    proto_path = ROOT / "protocols" / proto_name
    proto_path.write_text(json.dumps(escalation, indent=2), encoding="utf-8")
    return proto_path


def _route_refine(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    proposed = path / "artifacts" / "proposed_brief.yaml"
    if not proposed.exists():
        print("\n⏸️ REFINE verdict but no proposed_brief.yaml found. Human review needed.")
        return "human_pause"
    state = load_yaml(path / "pipeline_state.yaml")
    used  = state.get("counters", {}).get("refinements_used", 0)
    max_r = state.get("governance", {}).get("max_refinements_after_validation", 2)
    if used >= max_r:
        print(f"\n🛑 Refinement budget exhausted ({used}/{max_r}). Killing hypothesis.")
        return "completed_rejected"
    next_id = _next_run_id(run_id)
    print(f"\n🔄 REFINE (altitude 1): setting up {next_id} with proposed brief.")
    setup_next_run(path, next_id)
    # Copy findings_carryover.yaml (enables directional memory / parameter_bracket)
    carryover_src = path / "artifacts" / "findings_carryover.yaml"
    if carryover_src.exists():
        carryover_dst = ROOT / "runs" / next_id / "artifacts" / "findings_carryover.yaml"
        import shutil as _shutil
        _shutil.copy(carryover_src, carryover_dst)
        print(f"  findings_carryover.yaml copied to {next_id}")
    # Record in campaign state
    dim = interp.get("proposed_change_dimension", "")
    fam = interp.get("hypothesis_family", "")
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "parameter", dim, fam, "no_improvement", diag)
    return "completed_refined"


def _route_pivot(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    family = interp.get("hypothesis_family", "")
    next_id = _next_run_id(run_id)
    print(f"\n🔀 PIVOT (altitude 2): hypothesis family '{family}' exhausted. "
          f"Setting up {next_id} for fresh hypothesis generation.")
    # Scaffold directory only — no proposed_brief to copy. The next run's brief
    # is produced by hypothesis_generation using findings_carryover.yaml as input.
    subprocess.run([sys.executable, str(ROOT / "workflow" / "setup_run.py"), next_id])
    # Copy findings_carryover.yaml if the LLM produced it
    carryover_src = path / "artifacts" / "findings_carryover.yaml"
    if carryover_src.exists():
        carryover_dst = ROOT / "runs" / next_id / "artifacts" / "findings_carryover.yaml"
        import shutil as _shutil
        _shutil.copy(carryover_src, carryover_dst)
        print(f"  findings_carryover.yaml copied to {next_id}")
    record_pivot(family)
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "hypothesis", "", family, "pivot", diag)
    return "completed_refined"


def _route_escalate(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    esc_path = path / "artifacts" / "escalation_request.yaml"
    # When the circuit breaker forces escalate (overriding an LLM pivot verdict),
    # no escalation_request.yaml is produced. Default to instrument escalation —
    # that is the canonical meaning of "hypothesis family exhausted".
    if not esc_path.exists():
        print("\n📊 ESCALATE (circuit-breaker forced) → defaulting to instrument escalation.")
        target = "instrument"
    else:
        escalation = load_yaml(esc_path)
        target = escalation.get("target", "instrument")

    campaign = load_campaign_state()

    if target == "instrument":
        next_inst = _next_instrument_from_universe(campaign)
        if next_inst is None:
            # All instruments exhausted. Do NOT return "campaign_review" (loop risk if we
            # arrived here FROM campaign_review). Mark the campaign space_empty and terminate.
            print("⚠️ All instruments in coin_universe.yaml tried. Marking campaign space_empty.")
            _mark_campaign_status("space_empty")
            return "completed_rejected"
        print(f"\n📊 ESCALATE → {next_inst['symbol']} ({next_inst['category']}, {next_inst['timeframe']})")
        if not next_inst["data_cached"]:
            print(f"   ⚠️ Data not cached for {next_inst['symbol']} — will fetch on first run.")
        proto_path = _create_escalation_protocol(next_inst["symbol"], next_inst["timeframe"])
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        # Carry the current methodology brief into the next run (not proposed_brief.yaml).
        src_brief = path / "artifacts" / "research_brief.yaml"
        if src_brief.exists():
            shutil.copy(src_brief, ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml")
        # Write run_context.yaml so hypothesis_generation knows the escalation target.
        # research_brief.yaml carries the hypothesis methodology; run_context overrides asset.
        next_run_ctx = ROOT / "runs" / next_run_id / "artifacts" / "run_context.yaml"
        save_yaml(next_run_ctx, {
            "escalation_type": "instrument",
            "target_symbol": next_inst["symbol"],
            "target_timeframe": next_inst["timeframe"],
            "escalation_reason": "hypothesis_family_exhausted",
            "source_run": run_id,
            "note": (
                "This run is an instrument escalation. research_brief.yaml carries the "
                "hypothesis methodology from the previous run. Override the asset target to "
                f"{next_inst['symbol']} — do NOT use the asset listed in research_brief.yaml. "
                f"All stages must target {next_inst['symbol']} at {next_inst['timeframe']} timeframe."
            ),
        })
        record_escalation("instrument", next_inst["symbol"], protocol_path=str(proto_path))
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "instrument", "", "escalate", diag)
        return "completed_escalated"

    elif target == "timeframe":
        next_tf = _next_timeframe_from_universe(campaign)
        if next_tf is None:
            print("⚠️ All timeframes tried. Marking campaign space_empty.")
            _mark_campaign_status("space_empty")
            return "completed_rejected"
        print(f"\n⏱ ESCALATE → timeframe {next_tf}")
        proto_path = _create_timeframe_protocol(next_tf)
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        # Carry the current methodology brief into the next run (not proposed_brief.yaml).
        src_brief = path / "artifacts" / "research_brief.yaml"
        if src_brief.exists():
            shutil.copy(src_brief, ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml")
        record_escalation("timeframe", next_tf, protocol_path=str(proto_path))
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "timeframe", "", "escalate", diag)
        return "completed_escalated"

    elif target == "new_component":
        print("\n⏸️ ESCALATE → new component required. Pausing for human authoring.")
        update_state(path=path, status="paused_for_human")
        return "human_pause"

    else:
        raise ValueError(f"_route_escalate: unknown escalation target '{target}'")


def _route_kill(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    print("\n🛑 KILL: space exhausted or question answered negatively.")
    decision = {
        "campaign_id": campaign.get("campaign_id", "default"),
        "terminal_run": run_id,
        "decision": "kill",
        "rationale": interp.get("primary_failure_mode", "no rationale provided"),
        "altitude_justification": interp.get("altitude_justification", ""),
        "runs_attempted": campaign.get("runs", []),
        "families_tried": campaign.get("failed_families", []),
        "instruments_tried": campaign.get("instruments_tried", []),
        "components_built": campaign.get("components_built", []),
        "utc": datetime.now(timezone.utc).isoformat(),
    }
    save_yaml(ROOT / "campaign_decision.yaml", decision)
    print(f"  → Campaign decision written to campaign_decision.yaml")
    state = load_campaign_state()
    state["status"] = "space_empty"
    _save_campaign_state(state)
    return "completed_rejected"


def _extract_diagnostics(path: Path) -> dict:
    """Pull diagnostics from protocol_result.yaml for campaign logging."""
    try:
        pr = load_yaml(path / "artifacts" / "protocol_result.yaml")
        diag = (pr.get("hypothesis_verdict") or {}).get("diagnostics", {})
        return {
            "forecast_return_corr":      diag.get("median_forecast_return_corr"),
            "cost_drag_pct":             diag.get("median_cost_drag_pct"),
            "win_rate_vs_sharpe":        diag.get("win_rate_vs_sharpe"),
            "avg_trade_duration_bars":   diag.get("median_avg_trade_duration_bars"),
        }
    except Exception:
        return {}


def _auto_generate_findings_carryover(path: Path, interp: dict):
    """
    Constructs findings_carryover.yaml from verdict_interpretation.yaml when the LLM
    omitted it. Called after verdict_interpreter completes, before _verify_verdict_outputs.
    Safe to call unconditionally — skips if the file already exists.
    """
    carryover_path = path / "artifacts" / "findings_carryover.yaml"
    if carryover_path.exists():
        return

    status = (interp.get("status") or "").strip().lower()
    if status not in ("refine", "pivot", "escalate"):
        return

    altitude_just = interp.get("altitude_justification", "")

    # First sentence of altitude_justification → diagnostic_rule_applied
    first_sentence = altitude_just.split(". ")[0].strip() if altitude_just else "Rule unknown: no altitude_justification provided"

    def _extract_float(pattern: str, text: str):
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).lstrip("+"))
            except ValueError:
                return None
        return None

    corr      = _extract_float(r'(?:forecast_return_corr|corr)=([+-]?[\d.]+)', altitude_just)
    cost_drag = _extract_float(r'cost_drag(?:_pct)?=([+-]?[\d.]+)', altitude_just)
    gross_pnl = _extract_float(r'gross_pnl=([+-]?[\d.]+)', altitude_just)

    what_failed = [
        c.get("criterion", str(c))
        for c in (interp.get("criteria_summary") or [])
        if str(c.get("result", "")).upper() == "FAIL"
    ]
    if not what_failed:
        what_failed = ["No explicit FAIL criteria found — see altitude_justification"]

    dim    = interp.get("proposed_change_dimension", "")
    family = interp.get("hypothesis_family", "")
    if status == "refine":
        what_not_to_try = [
            f"Do not change {dim} further without addressing the root cause cited in altitude_justification"
            if dim else "Do not repeat the same parameter dimension"
        ]
    elif status == "pivot":
        what_not_to_try = [
            f"Do not retry {family} hypothesis family — parameter space exhausted"
            if family else "Do not retry this hypothesis family"
        ]
    else:  # escalate
        what_not_to_try = [
            f"Do not apply {family} signal further on current instrument — regime/signal failure confirmed"
            if family else "Do not apply this signal on the current instrument"
        ]

    save_yaml(carryover_path, {
        "hypothesis_id":           interp.get("hypothesis_id", "unknown"),
        "what_failed":             what_failed,
        "diagnostic_rule_applied": first_sentence,
        "diagnostic_snapshot": {
            "forecast_return_corr": corr,
            "cost_drag_pct":        cost_drag,
            "gross_pnl":            gross_pnl,
        },
        "what_not_to_try": what_not_to_try,
        "next_altitude":   status,
    })
    print("⚙️ Auto-generated findings_carryover.yaml from verdict artifacts.")


def _verify_verdict_outputs(run_dir: Path) -> list:
    """
    Check that verdict_interpreter produced the right artifacts for its declared status.
    Always reads verdict_interpretation.yaml fresh — never uses caller-modified status.
    Returns a list of violation strings. Empty list = all checks pass.
    """
    violations = []
    ARTIFACTS = run_dir / "artifacts"
    interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml")

    # Derive status from the artifact itself, not from any caller-supplied value.
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()

    # Universal checks (all statuses)
    if not interp.get("altitude_justification"):
        violations.append("verdict_interpretation.yaml missing altitude_justification")
    if not status:
        violations.append("verdict_interpretation.yaml missing status field")

    if status == "pivot":
        # pivot does NOT produce proposed_brief.yaml — the next run's brief is
        # generated fresh by hypothesis_generation using findings_carryover as input.
        # findings_carryover must exist and contain diagnostic_rule_applied
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("pivot: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append(
                    "pivot: findings_carryover.yaml missing diagnostic_rule_applied field"
                )
            if not carryover.get("what_not_to_try"):
                violations.append(
                    "pivot: findings_carryover.yaml missing what_not_to_try field"
                )

    if status == "refine":
        proposed_path = ARTIFACTS / "proposed_brief.yaml"
        if not proposed_path.exists():
            violations.append("refine: proposed_brief.yaml not produced")
        else:
            dim = interp.get("proposed_change_dimension", "")
            campaign = load_campaign_state()
            recent   = campaign.get("recent_parameter_dimensions", [])
            if dim and dim in recent:
                violations.append(
                    f"refine: proposed_change_dimension '{dim}' was already tried "
                    f"(in recent_parameter_dimensions: {recent}). Should have pivoted."
                )
            if not interp.get("proposed_change_dimension"):
                violations.append(
                    "refine: verdict_interpretation.yaml missing proposed_change_dimension"
                )

        # findings_carryover must exist for refine (cross-run directional memory)
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("refine: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append(
                    "refine: findings_carryover.yaml missing diagnostic_rule_applied field"
                )
            if not carryover.get("what_not_to_try"):
                violations.append(
                    "refine: findings_carryover.yaml missing what_not_to_try field"
                )

    if status == "escalate":
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("escalate: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append("escalate: findings_carryover.yaml missing diagnostic_rule_applied field")
            if not carryover.get("what_not_to_try"):
                violations.append("escalate: findings_carryover.yaml missing what_not_to_try field")
        escalation_path = ARTIFACTS / "escalation_request.yaml"
        if not escalation_path.exists():
            violations.append("escalate: escalation_request.yaml not produced")

    return violations


def _should_trigger_campaign_review(campaign: dict) -> bool:
    """
    Trigger campaign review when:
    - 2+ distinct hypothesis families have failed, OR
    - run count hits a multiple of review_every_n_runs (e.g. every 6 runs)
    Note: called AFTER the current run is recorded in campaign_state, so counts are current.
    """
    failed = campaign.get("failed_families", [])
    runs   = campaign.get("runs", [])
    review_n = campaign.get("review_every_n_runs", 6)
    families_trigger = len(set(failed)) >= 2   # distinct families, not total entries
    budget_trigger   = len(runs) > 0 and len(runs) % review_n == 0
    return families_trigger or budget_trigger


def determine_post_verdict_route(path: Path, run_id: str):
    interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
    # `status` is the new altitude-aware field; fall back to `protocol_verdict` for old runs
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()
    campaign = load_campaign_state()

    # --- CIRCUIT BREAKER: enforce altitude climbing regardless of LLM choice ---
    if status == "refine":
        dim         = interp.get("proposed_change_dimension", "")
        recent_dims = campaign.get("recent_parameter_dimensions", [])
        if dim in recent_dims or len(recent_dims) >= 2:
            reason = (f"tried dimension '{dim}' before" if dim in recent_dims
                      else f"2 parameter dimensions already tried ({recent_dims})")
            print(f"⚠️  CIRCUIT BREAKER: parameter altitude exhausted ({reason}). Forcing pivot.")
            status = "pivot"

    if status == "pivot":
        family         = interp.get("hypothesis_family", "")
        failed_families = campaign.get("failed_families", [])
        if failed_families.count(family) >= 2:
            print(f"⚠️  CIRCUIT BREAKER: hypothesis family '{family}' exhausted "
                  f"(appeared {failed_families.count(family)}x in failed_families). Forcing escalate.")
            status = "escalate"
    # --- end circuit breaker ---

    if status == "promote":
        update_state(path=path, flags={"walk_forward_passed": True})
        print("\n🎯 PROMOTE: hypothesis passes all evaluable criteria. Proceed to holdout.")
        return "completed_promoted"

    if status == "kill":
        return _route_kill(path, run_id, interp, campaign)

    # Auto-generate findings_carryover if missing (catches both normal and resume paths)
    _auto_generate_findings_carryover(path, interp)

    # Verify verdict outputs before scaffolding the next run (not applied to terminal routes)
    violations = _verify_verdict_outputs(path)
    if violations:
        print(f"\n⚠️ VERDICT VERIFICATION FAILED ({len(violations)} issue(s)):")
        for v in violations:
            print(f"   - {v}")
        report_path = path / "artifacts" / "verdict_verification_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(violations))
        update_state(path=path, status="paused_for_human")
        print("Pipeline paused. Fix the violations above, then resume.")
        return "human_pause"

    if _should_trigger_campaign_review(load_campaign_state()):
        print(f"\n🔭 CAMPAIGN REVIEW TRIGGERED — stepping back to assess campaign direction.")
        # Ensure the run-specific handoff file exists (it's only in templates by default)
        cr_handoff = path / "handoffs" / "campaign_review.yaml"
        if not cr_handoff.exists():
            template = ROOT / "templates" / "handoffs" / "campaign_review.yaml"
            cr_data = load_yaml(template)
            cr_data["run_id"] = run_id
            save_yaml(cr_handoff, cr_data)
        return "campaign_review"

    if status == "refine":
        return _route_refine(path, run_id, interp, campaign)

    if status == "pivot":
        return _route_pivot(path, run_id, interp, campaign)

    if status == "escalate":
        return _route_escalate(path, run_id, interp, campaign)

    raise ValueError(f"Unknown verdict status: '{status}'")


def determine_post_campaign_review_route(path: Path, run_id: str) -> str:
    review = load_yaml(path / "artifacts" / "campaign_review.yaml")
    rec = review.get("recommendation", "").strip().lower()

    if rec == "continue":
        # If campaign_review supplied next_research_question, honour it —
        # it overrides the verdict_interpreter's proposed_brief.yaml.
        nrq = review.get("next_research_question")
        if nrq and isinstance(nrq, dict) and len(nrq) > 0:
            import yaml as _yaml_nrq
            if isinstance(nrq, str):
                nrq = _yaml_nrq.safe_load(nrq)
            next_run_id = _next_run_id(run_id)
            _scaffold_next_run(next_run_id)
            save_yaml(ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml", nrq)
            update_campaign_state_after_run(
                run_id=run_id, altitude="campaign", dimension="research_question",
                family="", outcome="reframed", diagnostics=_extract_diagnostics(path),
            )
            print(f"\n🔄 CAMPAIGN REVIEW (continue+reframe): next_research_question -> {next_run_id}")
            return "completed_reframed"

        # No next_research_question — true continue, defer to verdict_interpreter.
        print("\n🔭 CAMPAIGN REVIEW: continue current direction.")
        interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
        status = interp.get("status", "refine").strip().lower()
        campaign = load_campaign_state()
        # Apply circuit-breaker overrides exactly as determine_post_verdict_route would,
        # then route — but do NOT call _should_trigger_campaign_review again.
        if status == "refine":
            dim         = interp.get("proposed_change_dimension", "")
            recent_dims = campaign.get("recent_parameter_dimensions", [])
            if dim in recent_dims or len(recent_dims) >= 2:
                reason = (f"tried dimension '{dim}' before" if dim in recent_dims
                          else f"2 parameter dimensions already tried ({recent_dims})")
                print(f"⚠️  CIRCUIT BREAKER: parameter altitude exhausted ({reason}). Forcing pivot.")
                status = "pivot"
        if status == "pivot":
            family          = interp.get("hypothesis_family", "")
            failed_families = campaign.get("failed_families", [])
            if failed_families.count(family) >= 2:
                print(f"⚠️  CIRCUIT BREAKER: hypothesis family '{family}' exhausted "
                      f"(appeared {failed_families.count(family)}x in failed_families). Forcing escalate.")
                status = "escalate"
        if status == "refine":
            return _route_refine(path, run_id, interp, campaign)
        if status == "pivot":
            return _route_pivot(path, run_id, interp, campaign)
        if status == "escalate":
            return _route_escalate(path, run_id, interp, campaign)
        if status == "promote":
            return "completed_promoted"
        if status == "kill":
            return _route_kill(path, run_id, interp, campaign)
        raise ValueError(f"continue: unknown verdict status {status}")

    if rec == "reframe":
        # Write the new research question as the next run's brief
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        nrq = review.get("next_research_question", {})
        if nrq:
            import yaml as _yaml
            if isinstance(nrq, str):
                nrq = _yaml.safe_load(nrq)
            save_yaml(ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml", nrq)
        update_campaign_state_after_run(
            run_id=run_id,
            altitude="campaign",
            dimension="research_question",
            family="",
            outcome="reframed",
            diagnostics=_extract_diagnostics(path),
        )
        print(f"\n🔄 REFRAME: new research question for {next_run_id}")
        return "completed_reframed"

    if rec in ("escalate_instrument", "escalate_component"):
        # Route through the escalate helper directly (escalate is NOT a stage name).
        # Build a minimal interp dict carrying the escalation target so _route_escalate
        # knows whether to escalate instrument or component.
        interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
        target = "instrument" if rec == "escalate_instrument" else "new_component"
        # Ensure escalation_request.yaml exists with the right target for _route_escalate
        esc_path = path / "artifacts" / "escalation_request.yaml"
        if not esc_path.exists():
            save_yaml(esc_path, {"target": target,
                                 "reason": review.get("recommendation_rationale", "")})
        return _route_escalate(path, run_id, interp, load_campaign_state())

    if rec == "terminate":
        return _route_kill(path, run_id, review, load_campaign_state())

    raise ValueError(f"Unknown campaign_review recommendation: {rec}")


def determine_post_spec_route(path: Path):
    KNOWN_STATUSES = {"spec_ready", "component_gap"}
    decision = load_yaml(path / "artifacts" / "decision.yaml")
    status = decision.get("status", "").strip().lower()
    if status == "spec_ready":
        return "protocol_execution"
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
        run_loop(run_id)
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
         
        TERMINAL_PREFIXES = ("completed", "rejected", "human_pause", "failed_validation")
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

            # Skip agent invocation if artifact already exists and is valid YAML
            # (avoids re-running LLM when manually recovering from a parse error)
            _skip_agent = False
            if current_stage == "campaign_review":
                _cr_path = RUN_DIR / "artifacts" / "campaign_review.yaml"
                if _cr_path.exists():
                    try:
                        import yaml as _yaml_check
                        _yaml_check.safe_load(_cr_path.read_text(encoding="utf-8"))
                        _skip_agent = True
                        print(f"⏭️  campaign_review.yaml already valid — skipping LLM re-run.")
                    except Exception:
                        pass  # invalid YAML — re-run the agent

            if current_stage == "verdict_interpreter":
                _vi_path = RUN_DIR / "artifacts" / "verdict_interpretation.yaml"
                if _vi_path.exists():
                    try:
                        import yaml as _yaml_check
                        _yaml_check.safe_load(_vi_path.read_text(encoding="utf-8"))
                        _skip_agent = True
                        print(f"⏭️  verdict_interpretation.yaml already valid — skipping LLM re-run.")
                    except Exception:
                        pass  # invalid YAML — re-run the agent

            # Invoke the Agent
            if not _skip_agent:
                asyncio.run(async_invoke_agent(current_stage, run_id))

            
            # # 4. Validate output artifacts were created
            # ensure_files(config["required_outputs"])

            # 4. Validate output artifacts were created
            expected_outputs = [RUN_DIR / "artifacts" / x for x in handoff_data.get("deliverables", [])]
            ensure_files(expected_outputs)

            # 4b. For campaign_review: validate YAML is parseable (LLM often emits colons in list items)
            if current_stage == "campaign_review" and not _skip_agent:
                import yaml as _yaml_val
                _cr_out = RUN_DIR / "artifacts" / "campaign_review.yaml"
                try:
                    _yaml_val.safe_load(_cr_out.read_text(encoding="utf-8"))
                except Exception as _ye:
                    raise ValueError(
                        f"YAML parse error in campaign_review.yaml: {_ye}\n"
                        f"Fix the file manually and re-run to resume."
                    )

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
                if next_stage == "protocol_execution":
                    spec = load_yaml(ARTIFACTS / "backtest_spec.yaml")
                    config_obj = spec.get("config")
                    candidate_path = ARTIFACTS / "candidate_strategy_config.json"
                    with open(candidate_path, "w", encoding="utf-8") as f:
                        json.dump(config_obj, f, indent=2)
                    validator  = Path("..") / "trading-bot" / "tools" / "validate_config.py"
                    TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"
                    result = subprocess.run(
                        [str(TBOT_PYTHON), str(validator), str(candidate_path)],
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
                        print("✅ config schema-valid; advancing to protocol_execution")
                        # Create handoff files for the remaining pipeline stages
                        _create_remaining_handoffs(run_id, RUN_DIR)
                elif next_stage == "human_pause":
                    break

            elif current_stage == "verdict_interpreter":
                _interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml")
                _auto_generate_findings_carryover(RUN_DIR, _interp)
                next_stage = determine_post_verdict_route(RUN_DIR, run_id)

            elif current_stage == "campaign_review":
                next_stage = determine_post_campaign_review_route(RUN_DIR, run_id)

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