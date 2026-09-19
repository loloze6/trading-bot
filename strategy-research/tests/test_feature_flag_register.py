"""
E-041 S2: the register ratchet.

WHY THIS EXISTS
---------------
E-041 found eight off-by-default feature flags where nothing in the process
ever decided when to turn one on -- "an abandoned feature with a test suite."
S1 (characterize) and S3 (act on the eight decisions) are done: 5 flags are
on, 3 are off with a named blocking epic each. What remained was S2, "the
register" -- one file naming every flag's owner and switch-on criterion,
"mechanically checked against the code so it cannot drift" (E-041's own
Risks section explicitly names E-037's ratchet tests, e.g.
test_user_guide_field_tables.py, as the model to follow).

This file is that ratchet, same shape as E-037's: green today, fails only on
NEW drift -- in either direction:
  1. A flag exists in the real code (an `orchestrator.*.enabled` key in
     config/campaign_config.yaml) with no matching entry in
     config/feature_flag_register.yaml -- a new flag landed without an owner
     or criterion being recorded.
  2. A register entry's `config_key` no longer resolves to a real flag --
     a stale entry describing something that was renamed or removed.
  3. A register entry's declared `state` ("on"/"off_incomplete") disagrees
     with the flag's real current value -- the register drifted from the
     code, silently, in either direction.

The two `engine_param` flags (bar_equity, model_funding) aren't YAML keys,
so they can't be discovered the same way; they get their own two functions
below, name-pinned (there are only ever two of them, unlike the open-ended
orchestrator set), checking the same "does the register's claimed state
match the real code" question via the engine's own default and the one
caller that matters (tools/run_protocol.py).

This supersedes tests/test_campaign_config_e041_flags.py (deleted in the
same change): that file's own docstring called itself "deliberately a small,
flat file rather than E-041 S2's planned register+test... until it exists,"
and it covered only the orchestrator flags, never bar_equity/model_funding.
Its per-flag knowledge (why each was switched on or held back) is preserved
verbatim in the register's `criterion` fields, not lost.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

_STRATEGY_RESEARCH_ROOT = Path(__file__).resolve().parent.parent
_CAMPAIGN_CONFIG_PATH = _STRATEGY_RESEARCH_ROOT / "config" / "campaign_config.yaml"
_REGISTER_PATH = _STRATEGY_RESEARCH_ROOT / "config" / "feature_flag_register.yaml"
_RUN_PROTOCOL_PATH = _STRATEGY_RESEARCH_ROOT / "tools" / "run_protocol.py"


def _load_register() -> list[dict]:
    with open(_REGISTER_PATH, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    flags = doc.get("flags")
    assert isinstance(flags, list) and flags, (
        f"{_REGISTER_PATH} has no `flags` list -- register is empty or malformed."
    )
    return flags


def _load_orchestrator_flags() -> dict:
    with open(_CAMPAIGN_CONFIG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return cfg.get("orchestrator") or {}


def _register_by_config_key(register: list[dict]) -> dict:
    return {
        entry["config_key"]: entry
        for entry in register
        if entry.get("kind") == "orchestrator_config"
    }


def _real_orchestrator_keys(orchestrator: dict) -> set:
    return {
        f"orchestrator.{name}.enabled"
        for name, block in orchestrator.items()
        if isinstance(block, dict) and "enabled" in block
    }


def _missing_register_entries(orchestrator: dict, register: list[dict]) -> set:
    """Real flags with no register entry -- pure, so it can be exercised
    against synthetic data to prove it isn't vacuous (see
    test_missing_and_stale_detection_is_not_vacuous below)."""
    registered_keys = set(_register_by_config_key(register).keys())
    return _real_orchestrator_keys(orchestrator) - registered_keys


def _stale_register_entries(orchestrator: dict, register: list[dict]) -> set:
    """Register entries with no matching real flag -- the inverse check."""
    registered_keys = set(_register_by_config_key(register).keys())
    return registered_keys - _real_orchestrator_keys(orchestrator)


def _state_mismatches(orchestrator: dict, register: list[dict]) -> list[str]:
    by_key = _register_by_config_key(register)
    mismatches = []
    for name, block in orchestrator.items():
        if not isinstance(block, dict) or "enabled" not in block:
            continue
        config_key = f"orchestrator.{name}.enabled"
        entry = by_key.get(config_key)
        if entry is None:
            continue  # reported by _missing_register_entries instead
        real_value = bool(block["enabled"])
        declared_on = entry.get("state") == "on"
        if real_value != declared_on:
            mismatches.append(
                f"{name}: register says state={entry.get('state')!r} but "
                f"campaign_config.yaml has enabled={real_value!r}"
            )
    return mismatches


def test_every_real_orchestrator_flag_has_a_register_entry() -> None:
    """A new `orchestrator.<name>.enabled` key with no register entry is
    exactly the drift this ratchet exists to catch -- a flag landing without
    an owner or a switch-on criterion ever being recorded."""
    missing = _missing_register_entries(_load_orchestrator_flags(), _load_register())
    assert not missing, (
        f"New orchestrator flag(s) with no entry in {_REGISTER_PATH.name}: "
        f"{sorted(missing)}. Add an entry naming its owner and switch-on "
        f"criterion (or the epic it's blocked on) before this flag ships."
    )


def test_no_stale_register_entries_for_removed_flags() -> None:
    """A register entry naming a config_key that no longer exists is a stale
    entry -- the flag it described was renamed or removed and nobody updated
    the register. Shrinking the register is enforced exactly like growing it
    (same ratchet principle as test_user_guide_field_tables.py's
    KNOWN_PHANTOM check)."""
    stale = _stale_register_entries(_load_orchestrator_flags(), _load_register())
    assert not stale, (
        f"{_REGISTER_PATH.name} names orchestrator flag(s) that no longer "
        f"exist in campaign_config.yaml: {sorted(stale)}. Remove or correct "
        f"these entries -- a stale register entry hides real drift."
    )


def test_orchestrator_register_states_match_real_config_values() -> None:
    """The register's declared on/off_incomplete state for every orchestrator
    flag must match campaign_config.yaml's real `enabled:` value -- this is
    what test_campaign_config_e041_flags.py's six hand-written functions each
    checked individually; here it's one data-driven check covering all of
    them, plus any future flag automatically."""
    mismatches = _state_mismatches(_load_orchestrator_flags(), _load_register())
    assert not mismatches, (
        "Register/config drift on orchestrator flag(s):\n  " + "\n  ".join(mismatches) +
        "\nEither the flag was flipped without updating the register, or the "
        "register was edited without checking the real value."
    )


def test_missing_and_stale_detection_is_not_vacuous() -> None:
    """Proves the three pure checks above actually catch drift, using
    synthetic data -- not just that they pass on today's already-correct
    register (same discipline as the near-miss scoreboard firewall's own
    'inject a violation and confirm the scanner catches it' test)."""
    orchestrator = {"a_new_flag": {"enabled": True}}
    empty_register: list[dict] = []
    assert _missing_register_entries(orchestrator, empty_register) == {
        "orchestrator.a_new_flag.enabled"
    }

    stale_register = [
        {"kind": "orchestrator_config", "config_key": "orchestrator.a_removed_flag.enabled",
         "state": "on"}
    ]
    assert _stale_register_entries({}, stale_register) == {
        "orchestrator.a_removed_flag.enabled"
    }

    drifted_register = [
        {"kind": "orchestrator_config", "config_key": "orchestrator.a_new_flag.enabled",
         "state": "off_incomplete"}
    ]
    mismatches = _state_mismatches(orchestrator, drifted_register)
    assert len(mismatches) == 1 and "a_new_flag" in mismatches[0]


def test_off_incomplete_orchestrator_entries_name_a_blocking_epic() -> None:
    """E-041's own finding: 'off, no reason given' was never a legitimate
    state for a finished feature. Every off_incomplete entry must name what
    it's blocked on, not just assert the absence of a reason."""
    register = _load_register()
    unblocked = [
        entry["name"] for entry in register
        if entry.get("state") == "off_incomplete" and not entry.get("blocked_on")
    ]
    assert not unblocked, (
        f"Flag(s) marked off_incomplete with no blocked_on epic named: "
        f"{unblocked}. Name the specific epic this is waiting on."
    )


def _bar_equity_actually_on() -> bool:
    """bar_equity's engine default stays False by design (bit-identity); it
    is 'on' for research purposes only if the one caller that matters
    (run_protocol.py) explicitly passes bar_equity=True at every call site
    that runs a real protocol backtest."""
    text = _RUN_PROTOCOL_PATH.read_text(encoding="utf-8")
    # Prose references like "every run_backtest() call" (in comments) match
    # with an empty argument list -- exclude those, keep only real calls.
    call_sites = [
        site for site in re.findall(r"run_backtest\([^)]*\)", text, re.DOTALL)
        if site != "run_backtest()"
    ]
    assert call_sites, f"No real run_backtest(...) call sites found in {_RUN_PROTOCOL_PATH}"
    return all("bar_equity=True" in site for site in call_sites)


def _model_funding_actually_on() -> bool:
    text = _RUN_PROTOCOL_PATH.read_text(encoding="utf-8")
    return "model_funding=True" in text


def test_bar_equity_register_state_matches_the_real_caller() -> None:
    register = _load_register()
    entry = next((e for e in register if e["name"] == "bar_equity"), None)
    assert entry is not None, "bar_equity has no register entry"
    assert entry["kind"] == "engine_param"

    real_on = _bar_equity_actually_on()
    declared_on = entry.get("state") == "on"
    assert real_on == declared_on, (
        f"bar_equity register says state={entry.get('state')!r}, but "
        f"{_RUN_PROTOCOL_PATH.name}'s own run_backtest(...) call site(s) "
        f"{'do' if real_on else 'do not'} pass bar_equity=True. Update "
        f"whichever one is stale."
    )


def test_model_funding_register_state_matches_the_real_caller() -> None:
    register = _load_register()
    entry = next((e for e in register if e["name"] == "model_funding"), None)
    assert entry is not None, "model_funding has no register entry"
    assert entry["kind"] == "engine_param"
    assert entry.get("blocked_on") == "E-014", (
        "model_funding is documented as blocked on E-014 -- if that changed, "
        "update the register's blocked_on field deliberately."
    )

    real_on = _model_funding_actually_on()
    declared_on = entry.get("state") == "on"
    assert real_on == declared_on, (
        f"model_funding register says state={entry.get('state')!r}, but "
        f"{_RUN_PROTOCOL_PATH.name} {'does' if real_on else 'does not'} pass "
        f"model_funding=True anywhere. If this flipped, E-014 finished "
        f"unblocking it and the register needs a deliberate update, not a "
        f"silent one."
    )


def test_engine_defaults_stay_false_for_bit_identity() -> None:
    """The register's own criterion text asserts, for both engine_param
    flags, that the engine's OWN parameter default stays False -- the flag
    is turned on only by the research pipeline's caller explicitly passing
    True, never by changing the engine's default (that's the bit-identity
    discipline this whole repo runs on). Checks the claim rather than
    trusting the prose."""
    register = _load_register()
    problems = []
    for entry in register:
        if entry.get("kind") != "engine_param":
            continue
        name = entry["name"]
        for rel_path in entry.get("engine_default_files", []):
            full_path = _STRATEGY_RESEARCH_ROOT.parent / rel_path
            assert full_path.exists(), f"{rel_path} (named in the register for {name}) does not exist"
            text = full_path.read_text(encoding="utf-8")
            if not re.search(rf"\b{name}\s*:\s*bool\s*=\s*False\b", text):
                problems.append(f"{name}: no `{name}: bool = False` default found in {rel_path}")

    assert not problems, (
        "Engine default drift:\n  " + "\n  ".join(problems) +
        "\nEither the engine's own default changed (a much bigger behavior "
        "change than the register describes), or the register's "
        "engine_default_files list is stale."
    )


def test_register_has_exactly_the_two_known_engine_params() -> None:
    """Companion to the orchestrator drift checks above: engine_param flags
    can't be auto-discovered from a YAML file the way orchestrator flags
    can, so this pins the known set at exactly two. A new engine-level flag
    (a third bool parameter defaulting False on the trading-bot engine)
    needs a deliberate new entry and a new pinned check above -- this test
    failing is the signal that happened without one."""
    register = _load_register()
    engine_param_names = {e["name"] for e in register if e.get("kind") == "engine_param"}
    assert engine_param_names == {"bar_equity", "model_funding"}, (
        f"Expected exactly {{'bar_equity', 'model_funding'}} as engine_param "
        f"register entries, found {engine_param_names}. A new engine_param "
        f"flag needs its own test_..._register_state_matches_the_real_caller "
        f"function above, not just a register entry."
    )
