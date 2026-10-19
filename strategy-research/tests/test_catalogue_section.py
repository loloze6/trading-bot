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

The test that the section lists signed_power (CUL-354) is added once that op is merged.
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
    assert line == ("- fake_graded_op (k (2)): a made-up graded op; allowed in strategies")
    assert "Transform ops (18)" in out


def test_an_op_added_to_dead_zone_ops_is_refused_without_a_guide_change(tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "DEAD_ZONE_OPS", fr.DEAD_ZONE_OPS + ("negate",))
    assert cs.op_status("negate").startswith("refused in strategies (D-051")


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
