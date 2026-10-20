"""
The catalogue section of the analyst prompt (tools/catalogue_section.py).

Covers:
  1. every component class between the catalogue markers, and every op in the design
     guide's Transform ops tables, is listed; every registry op (TRANSFORM_OPS_REGISTRY)
     is listed, and a registry op the guide table lacks is named in the failure;
  2. allowed / refused for ops follows forecast_rules (DEAD_ZONE_OPS for D-051, the
     scale op for D-149) and for classes follows the catalogue Kind (on/off -> D-051);
  3. the output is deterministic and reads no run or data file;
  4. a missing marker, heading or table raises;
  5. an op added to a guide table appears with no code change (no hard-coded op list);
  6. build_prompt carries the section after "The run context" and before the data dictionary.

  7. signed_power (CUL-354) is listed once among the ops, allowed in strategies, with its parameters.
  8. each op line carries its group and the guide's placement phrase; every op that
     trading-bot/tools/validate_config.py refuses by placement (V14, V15, V16) carries it;
     the section names no run id and no date.
No LLM, no backtest.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT.parent / "trading-bot"))

import catalogue_section as cs  # noqa: E402
import forecast_rules as fr  # noqa: E402

CATALOG = SR_ROOT / "docs" / "COMPONENT_CATALOG.md"
GUIDE = SR_ROOT / "docs" / "STRATEGY_DESIGN_GUIDE.md"
ROW = re.compile(r"^\|\s*`(\w+)`\s*\|", re.MULTILINE)


def _lines(section: str, heading_start: str) -> list:
    """The '- ' lines after the line starting `heading_start`, up to the next blank line."""
    lines = section.splitlines()
    i = next(n for n, line in enumerate(lines) if line.startswith(heading_start))
    out = []
    for line in lines[i + 1:]:
        if not line.strip():
            break
        out.append(line)
    return out


def _classes_in_catalog() -> list:
    text = CATALOG.read_text(encoding="utf-8")
    body = text[text.index(fr._START_MARKER):text.index(fr._END_MARKER)]
    return ROW.findall(body)


def _ops_in_guide() -> list:
    text = GUIDE.read_text(encoding="utf-8")
    start = text.index("\n## Transform ops\n")
    return ROW.findall(text[start:text.index("\n## ", start + 1)])


@pytest.fixture(scope="module")
def section() -> str:
    return cs.catalogue_section()


def test_every_catalogue_class_is_listed(section):
    classes = _classes_in_catalog()
    assert len(classes) >= 20
    comp_lines = _lines(section, "Component classes (")
    assert [line.split(" ", 2)[1] for line in comp_lines] == classes
    assert f"Component classes ({len(classes)})" in section


def test_every_guide_op_is_listed(section):
    ops = _ops_in_guide()
    op_lines = _lines(section, "Transform ops (")
    assert [line.split(" ", 2)[1] for line in op_lines] == ops
    assert f"Transform ops ({len(ops)})" in section


def test_every_registry_op_is_listed(section):
    from strategies.registry import TRANSFORM_OPS_REGISTRY
    listed = {line.split(" ", 2)[1] for line in _lines(section, "Transform ops (")}
    missing_from_guide = sorted(set(TRANSFORM_OPS_REGISTRY) - set(_ops_in_guide()))
    assert not missing_from_guide, f"registry op(s) the guide table lacks: {missing_from_guide}"
    assert set(TRANSFORM_OPS_REGISTRY) <= listed


def test_ops_allowed_or_refused_follow_forecast_rules(section):
    by_op = {line.split(" ", 2)[1]: line for line in _lines(section, "Transform ops (")}
    for op in fr.DEAD_ZONE_OPS:
        assert "refused in strategies (D-051" in by_op[op]
    assert "refused in strategies (D-149" in by_op["scale"]
    for op, line in by_op.items():
        if op in fr.DEAD_ZONE_OPS or op == "scale":
            continue
        assert "allowed in strategies" in line, line
        assert "refused" not in line, line
    # the sets agree with the code, op by op
    refused = {op for op, line in by_op.items() if "refused in strategies" in line}
    assert refused == set(fr.DEAD_ZONE_OPS) | {"scale"}


def test_on_off_classes_are_marked_refused_by_kind_and_nothing_else(section):
    on_off = fr.on_off_classes()
    for line in _lines(section, "Component classes ("):
        name = line.split(" ", 2)[1]
        assert (f"[{fr.ON_OFF_KIND}]" in line) == (name in on_off), line
    assert "on/off: refused (D-051" in section


def test_the_rules_are_stated_from_the_code(section):
    assert fr.RULE_SENTENCE in section
    for op in fr.DEAD_ZONE_OPS:
        assert op in section.split("Kinds, as a forecast source")[0]


def test_output_is_deterministic_and_each_entry_is_one_line(section):
    assert cs.catalogue_section() == section
    for line in _lines(section, "Component classes (") + _lines(section, "Transform ops ("):
        assert line.startswith("- ") and "\n" not in line and len(line) < 700, line
    assert "`" not in section and "**" not in section


def test_reads_only_the_two_docs_and_nothing_else(monkeypatch):
    opened = []
    real_read = Path.read_text

    def spy(self, *a, **k):
        opened.append(Path(self).name)
        return real_read(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", spy)
    cs.catalogue_section()
    assert set(opened) <= {"COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md"}


def _copy(tmp_path, catalog_text=None, guide_text=None):
    cat, guide = tmp_path / "COMPONENT_CATALOG.md", tmp_path / "STRATEGY_DESIGN_GUIDE.md"
    cat.write_text(catalog_text if catalog_text is not None else CATALOG.read_text(encoding="utf-8"),
                   encoding="utf-8")
    guide.write_text(guide_text if guide_text is not None else GUIDE.read_text(encoding="utf-8"),
                     encoding="utf-8")
    return cat, guide


def test_the_copied_docs_give_the_same_section(tmp_path, section):
    cat, guide = _copy(tmp_path)
    assert cs.catalogue_section(cat, guide) == section


@pytest.mark.parametrize("marker", [fr._START_MARKER, fr._END_MARKER])
def test_a_missing_catalogue_marker_raises(tmp_path, marker):
    cat, guide = _copy(tmp_path, CATALOG.read_text(encoding="utf-8").replace(marker, ""))
    with pytest.raises(cs.CatalogueSectionError, match="CATALOG"):
        cs.catalogue_section(cat, guide)


def test_a_missing_catalogue_file_raises(tmp_path):
    _, guide = _copy(tmp_path)
    with pytest.raises(cs.CatalogueSectionError, match="not found"):
        cs.catalogue_section(tmp_path / "nope.md", guide)


def test_a_missing_ops_heading_raises(tmp_path):
    cat, guide = _copy(tmp_path, guide_text=GUIDE.read_text(encoding="utf-8").replace(
        "\n## Transform ops\n", "\n## Transform operations\n"))
    with pytest.raises(cs.CatalogueSectionError, match="Transform ops"):
        cs.catalogue_section(cat, guide)


def test_an_ops_heading_with_no_rows_raises(tmp_path):
    cat, guide = _copy(tmp_path, guide_text="# Guide\n\n## Transform ops\n\nno table here\n\n## Next\n")
    with pytest.raises(cs.CatalogueSectionError, match="no op rows"):
        cs.catalogue_section(cat, guide)


def test_a_missing_kind_legend_raises(tmp_path):
    cat, guide = _copy(tmp_path, CATALOG.read_text(encoding="utf-8").replace(
        "### Kind legend", "### Kinds"))
    with pytest.raises(cs.CatalogueSectionError, match="Kind legend"):
        cs.catalogue_section(cat, guide)


def test_an_op_added_to_the_guide_table_appears_with_no_code_change(tmp_path):
    text = GUIDE.read_text(encoding="utf-8")
    anchor = "| `negate` | none | -v |"
    assert anchor in text
    cat, guide = _copy(tmp_path, guide_text=text.replace(
        anchor, anchor + "\n| `fake_graded_op` | `k` (2) | a made-up graded op. Second sentence. |"))
    out = cs.catalogue_section(cat, guide)
    line = next(ln for ln in out.splitlines() if ln.startswith("- fake_graded_op "))
    assert line == ("- fake_graded_op [scalar op] (k (2)): a made-up graded op; allowed in strategies")
    assert f"Transform ops ({len(_ops_in_guide()) + 1})" in out


def test_an_op_added_to_dead_zone_ops_is_refused_without_a_guide_change(tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "DEAD_ZONE_OPS", fr.DEAD_ZONE_OPS + ("negate",))
    assert cs.op_status("negate").startswith("refused in strategies (D-051")


def test_signed_power_is_listed_once_among_the_ops_with_its_status_and_parameters(section):
    op_lines = _lines(section, "Transform ops (")
    names = [line.split(" ", 2)[1] for line in op_lines]
    assert names.count("signed_power") == 1
    assert section.count("- signed_power ") == 1
    line = op_lines[names.index("signed_power")]
    # its status is the one forecast_rules derives: not a dead-zone op, so allowed in strategies
    assert "signed_power" not in fr.DEAD_ZONE_OPS
    assert cs.op_status("signed_power") == "allowed in strategies"
    # status, then the guide's bold placement phrase as the line ending
    assert line.endswith("; " + cs.op_status("signed_power")
                         + "; Allowed only in a strategies component's transforms, "
                         "in a regime without blocks"), line
    assert "refused" not in line
    # both parameters are on the line
    assert "exponent" in line and "pivot" in line
    assert line.startswith("- signed_power [scalar op] (exponent (")


# ---------------------------------------------------------------------------
# placement and group: the section states what validate_config enforces
# ---------------------------------------------------------------------------

VALIDATE_CONFIG = SR_ROOT.parent / "trading-bot" / "tools" / "validate_config.py"
# `<op> is allowed only in <where>` (V14, V16) and V15's `<op> belongs in` / `must be the first step`
# / `must be the only history op` messages, read as text from the validator source.
_ALLOWED_ONLY_RE = re.compile(r"(\w+) is allowed only in ")
_V15_RE = re.compile(r"\]: (\w+) (belongs in|must be the first step|must be the only history op)")
_V15_LINE_WORDS = {"belongs in": "first step", "must be the first step": "first step",
                   "must be the only history op": "only history op"}


def _validator_source() -> str:
    # adjacent string literals are joined, so a message split over two source lines reads whole
    return re.sub(r'"\s*\r?\n\s*f?"', "", VALIDATE_CONFIG.read_text(encoding="utf-8"))


def _op_lines(section: str) -> dict:
    return {line.split(" ", 2)[1]: line for line in _lines(section, "Transform ops (")}


def test_every_op_the_validator_refuses_by_placement_carries_that_placement_on_its_line(section):
    src = _validator_source()
    by_op = _op_lines(section)
    allowed_only = {m.group(1): src[m.end():].split('"')[0].split("(")[0].replace("`", "").strip()
                    for m in _ALLOWED_ONLY_RE.finditer(src)}
    # the validator has placement rules for these (vol_target V14, signed_power V16); a rule
    # added there for another op is checked here too, with no list kept by hand
    assert {"vol_target", "signed_power"} <= set(allowed_only)
    for op, where in allowed_only.items():
        assert op in by_op, f"validate_config places {op}, the guide table lacks it"
        assert f"allowed only in {where}".lower() in by_op[op].lower(), (
            f"validate_config says {op} is allowed only in {where!r}; the guide cell states no such "
            f"placement, so the catalogue section line does not carry it: {by_op[op]}")
    v15 = {(m.group(1), m.group(2)) for m in _V15_RE.finditer(src)}
    assert ("standardise", "belongs in") in v15
    for op, phrase in v15:
        assert op in by_op, f"validate_config places {op}, the guide table lacks it"
        assert _V15_LINE_WORDS[phrase] in by_op[op], (op, phrase, by_op[op])


def test_vol_adjusted_keeps_its_warning_and_dead_zone_ops_are_not_double_stated(section):
    by_op = _op_lines(section)
    assert by_op["vol_adjusted"].endswith("; Not a volatility scaler on its own")
    for op in fr.DEAD_ZONE_OPS:
        assert by_op[op].count("refused in strategies") == 1
        assert "Not allowed" not in by_op[op]


def test_every_op_line_carries_its_group_and_the_history_ops_match_the_registry(section):
    from strategies.registry import HISTORY_OPS
    for op, line in _op_lines(section).items():
        assert re.match(rf"- {op} \[[a-z-]+ op\] \(", line), line
        assert (f"- {op} [history op] (" in line) == (op in HISTORY_OPS), line
    assert "[history op] History ops recompute" in section


def test_the_section_names_no_run_and_no_date(section):
    assert not re.search(r"run_\d+", section)
    assert not re.search(r"\d{4}-\d{2}-\d{2}", section)


def test_the_header_says_d051_and_d149_skip_the_regime_detector_but_placement_does_not(section):
    assert "D-051 and D-149 do not apply to the regime detector; the placement rules on the op lines do." in section
    assert "the regime detector is not checked" not in section
    assert "period and window parameters are counted in bars of the run's timeframe" in section

# ---------------------------------------------------------------------------
# build_prompt
# ---------------------------------------------------------------------------

def test_build_prompt_carries_the_section_between_the_run_context_and_the_data_dictionary(tmp_path):
    import analyst_session as asm
    run = tmp_path / "runs" / "run_x"
    (run / "artifacts").mkdir(parents=True)
    text = asm.build_prompt("forecast", run, base_config_rel="artifacts/none.json", fold="A",
                            memory_view={})
    title = "## The component and op catalogue (what a vehicle may name)"
    ctx = text.index("## The run context")
    cat = text.index(title)
    dd = text.index("## The data dictionary")
    assert ctx < cat < dd
    assert text.count(title) == 1
    assert cs.catalogue_section() in text[cat:dd]
