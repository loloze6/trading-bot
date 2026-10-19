"""
catalogue_section -- the component and op catalogue as one compact prompt section.

The analyst's vehicle names components and transform ops. This module renders
what exists, from the two docs that define it, so the prompt can never drift
from them and no class or op name is typed by hand here:

  * components: the rows between the CATALOG markers of docs/COMPONENT_CATALOG.md,
    read by forecast_rules.catalog_rows (the same parser the D-051 check uses);
  * ops: the tables under the "## Transform ops" heading of
    docs/STRATEGY_DESIGN_GUIDE.md (an op added to the table appears here by itself).

"Allowed or refused in strategies" is derived from the code that enforces it,
tools/forecast_rules.py: a class is refused when its catalogue Kind is on/off
(D-051); an op is refused when it is in DEAD_ZONE_OPS (D-051) or when
strategies_violations() reports D-149 for a component whose transforms hold
standardise followed by that op. No allowed/refused list is written by hand.

Pure text, no network, no run or data reads. Output order is the doc order, so it
is deterministic. A missing marker, heading or table raises CatalogSectionError
(a doc edit must not silently empty the section).

    python tools/catalogue_section.py        # prints the section
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import forecast_rules as fr  # noqa: E402

GUIDE_PATH = Path(__file__).resolve().parents[1] / "docs" / "STRATEGY_DESIGN_GUIDE.md"
OPS_HEADING = "## Transform ops"
KIND_HEADING = "### Kind legend"
_OP_ROW_RE = re.compile(r"^\|\s*`(\w+)`\s*\|", re.MULTILINE)
_COMPONENT_CELLS = 9   # class, params, exact output, range & sign, kind, units, warmup, data & NaN, notes
_OP_CELLS = 3          # op, params, output
_GROUP_RE = re.compile(r"^\*\*([\w-]+(?: [\w-]+)* ops)\*\*")   # '**History ops** recompute ...'
_GROUP_SUFFIX_RE = re.compile(r"ops$")
_PARAMS_CELL, _OUTPUT_CELL, _KIND_CELL = 1, 2, 4
MAX_LINE = 190         # characters of the one-line description


class CatalogueSectionError(RuntimeError):
    """A catalogue or guide doc cannot be read as the tables this section is built from."""


def _plain(cell: str) -> str:
    return cell.replace("`", "").replace("**", "").strip()


def _one_line(cell: str, limit: int = MAX_LINE) -> str:
    """The first sentence of a table cell, without backticks, cut at a word boundary."""
    text = _plain(cell)
    m = re.search(r"(?<![\d.])\.(\s|$)", text)
    if m:
        text = text[:m.start()]
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:(")
    return cut + " ..."


def _component_rows(catalog_path: Path) -> list:
    try:
        rows = fr.catalog_rows(catalog_path)
    except fr.CatalogError as exc:
        raise CatalogueSectionError(str(exc)) from exc
    for cells in rows:
        if len(cells) != _COMPONENT_CELLS:
            raise CatalogueSectionError(
                f"{catalog_path}: component row with {len(cells)} cells, expected "
                f"{_COMPONENT_CELLS}: {cells[0]}")
    return rows


def _parse_ops(guide_path: Path) -> tuple:
    """(rows, groups): each row is (op, params, output, group); groups maps a group name
    ('history op') to the first sentence of the guide paragraph that introduces its table."""
    path = Path(guide_path)
    if not path.is_file():
        raise CatalogueSectionError(f"{path}: design guide not found")
    text = path.read_text(encoding="utf-8")
    start = text.find("\n" + OPS_HEADING + "\n")
    if start < 0:
        raise CatalogueSectionError(f"{path}: no {OPS_HEADING!r} heading")
    body = text[start + 1:]
    nxt = re.search(r"^## ", body[len(OPS_HEADING):], re.MULTILINE)
    if nxt:
        body = body[:len(OPS_HEADING) + nxt.start()]
    rows, groups, group, paragraph = [], {}, None, []
    for line in body.splitlines() + [""]:
        head = _GROUP_RE.match(line)
        if head:
            if group is not None:
                groups[group] = _one_line(" ".join(paragraph), 300)
            group = _GROUP_SUFFIX_RE.sub("op", head.group(1).lower())
            paragraph = [line]
        elif group is not None and paragraph and line.strip() and not line.startswith("|"):
            paragraph.append(line.strip())
        elif _OP_ROW_RE.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != _OP_CELLS:
                raise CatalogueSectionError(
                    f"{path}: op row with {len(cells)} cells, expected {_OP_CELLS}: {cells[0]}")
            if group is None:
                raise CatalogueSectionError(
                    f"{path}: op {cells[0]} has no '**<Kind> ops**' group heading above its table")
            rows.append(cells + [group])
    if group is not None and group not in groups:
        groups[group] = _one_line(" ".join(paragraph), 300)
    if not rows:
        raise CatalogueSectionError(f"{path}: no op rows under {OPS_HEADING!r}")
    names = [c[0] for c in rows]
    if len(set(names)) != len(names):
        raise CatalogueSectionError(f"{path}: an op is listed twice under {OPS_HEADING!r}")
    return rows, groups


def op_rows(guide_path: Path = GUIDE_PATH) -> list:
    """The rows (op, params, output, group) of the tables under the Transform ops heading, in
    doc order. The group ('history op', 'scalar op', ...) comes from the bold '**<Kind> ops**'
    heading of the paragraph above each table."""
    return _parse_ops(guide_path)[0]


def op_placement(description_cell: str) -> str:
    """Where the guide says an op may be used: its bold 'Allowed only ...' / 'Not allowed ...' /
    'Not a ...' phrases; when the cell has none, the sentence that says what the op 'must be' and
    cites a validator rule '(V<n>)'. Empty when the guide states no placement."""
    bold = re.findall(r"\*\*((?:Allowed only|Not allowed|Not a)[^*]*)\*\*", description_cell)
    if bold:
        return "; ".join(_plain(b) for b in bold)
    m = re.search(r"[^.;]*\bmust be\b[^;]*?\(V\d+\)", description_cell)
    return _plain(m.group(0)) if m else ""


def _probe(pipeline: list) -> list:
    """The forecast_rules (D-051 / D-149) messages for one strategies component with this transforms."""
    config = {"strategies": {"regimes": {"probe": {"components": [
        {"class": "strategies.strategy_components.Probe", "id": "probe", "transforms": pipeline}]}}}}
    return fr.strategies_violations(config, frozenset())


def op_status(op: str) -> str:
    """'allowed' or 'refused' for `op` in a strategies component, with the rule that decides it,
    derived by running forecast_rules on a one-component config."""
    step = {"op": op, "params": {}}
    first = {"op": "standardise", "params": {}}
    if op in fr.DEAD_ZONE_OPS or any("D-051" in m for m in _probe([step])):
        return "refused in strategies (D-051: dead-zone op; belongs in the regime detector)"
    if not any("D-149" in m for m in _probe([step])):
        return "allowed in strategies (sets the forecast scale: D-149)"
    if any("D-149" in m for m in _probe([first, step])):
        return "refused in strategies (D-149: a scale op; the scale comes from standardise or vol_target)"
    return "allowed in strategies"


def kind_legend(catalog_path: Path = fr.CATALOG_PATH) -> list:
    """(kind, use as a forecast source) from the catalogue's 'Kind legend' table, in doc order."""
    path = Path(catalog_path)
    text = path.read_text(encoding="utf-8")
    start = text.find("\n" + KIND_HEADING + "\n")
    if start < 0:
        raise CatalogueSectionError(f"{path}: no {KIND_HEADING!r} heading")
    body = text[start + 1:]
    nxt = re.search(r"^#{2,3} ", body[len(KIND_HEADING):], re.MULTILINE)
    if nxt:
        body = body[:len(KIND_HEADING) + nxt.start()]
    rows = []
    for line in body.splitlines():
        cells = [_plain(c) for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) == 3 and cells[0] not in ("kind", "---") and not cells[0].startswith("-"):
            rows.append((cells[0], cells[2]))
    if not rows:
        raise CatalogueSectionError(f"{path}: no rows under {KIND_HEADING!r}")
    return rows


def catalogue_section(catalog_path: Path = fr.CATALOG_PATH, guide_path: Path = GUIDE_PATH) -> str:
    """The section text: the rules, one line per component class, one line per op."""
    comps = _component_rows(Path(catalog_path))
    legend = kind_legend(Path(catalog_path))
    unknown = sorted({_plain(c[_KIND_CELL]) for c in comps} - {k for k, _ in legend})
    if unknown:
        raise CatalogueSectionError(f"{catalog_path}: kind(s) {unknown} not in the Kind legend")
    ops, groups = _parse_ops(Path(guide_path))
    out = [
        "Every component class and transform op that exists is listed here; a name not listed "
        "is invented. A config refers to a class as strategies.strategy_components.<Class>. "
        "Parameters are written name (default); period and window parameters are counted in bars "
        "of the run's timeframe.",
        "",
        "Rules in force for components and ops in strategies (D-051 and D-149 are checked by "
        "tools/forecast_rules.py after step 1b and at 5a; the placement rules on the op lines "
        "are checked by validate_config at 5a):",
        "- D-051 (graded forecasts only): on/off classes and the dead-zone ops "
        + " and ".join(fr.DEAD_ZONE_OPS) + " are refused.",
        "- D-149: " + fr.RULE_SENTENCE,
        "- D-051 and D-149 do not apply to the regime detector; the placement rules on the op lines do.",
        "",
        "Kinds, as a forecast source in strategies: "
        + "; ".join(f"{k}: {use}" for k, use in legend) + ".",
        "",
        "Op groups, from the design guide: "
        + " ".join(f"[{g}] {s}." for g, s in groups.items()),
        "",
        f"Component classes ({len(comps)}) -- class [kind] (parameters): what it measures:",
    ]
    for cells in comps:
        name, kind = _plain(cells[0]), _plain(cells[_KIND_CELL])
        out.append(f"- {name} [{kind}] ({_plain(cells[_PARAMS_CELL])}): "
                   f"{_one_line(cells[_OUTPUT_CELL])}")
    out += ["", f"Transform ops ({len(ops)}) -- op [group] (parameters): what it does; status; "
                f"where the guide allows it:"]
    for cells in ops:
        name, status = _plain(cells[0]), op_status(_plain(cells[0]))
        line = (f"- {name} [{cells[3]}] ({_one_line(cells[1], 240)}): "
                f"{_one_line(cells[2])}; {status}")
        placement = op_placement(cells[2])
        if placement and not status.startswith("refused"):
            line += f"; {placement}"
        out.append(line)
    return "\n".join(out)


if __name__ == "__main__":
    print(catalogue_section())
