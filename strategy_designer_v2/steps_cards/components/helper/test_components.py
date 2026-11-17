"""Tests of the components step's code: the wishes and their answers, the unblocking rule, the answer's parsing, the
files a build writes, the proof's comparison. No model call, no backtest (a fake call stands in for the model)."""
import gzip
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_component as B  # noqa: E402
import wishes as W  # noqa: E402

WISHLIST = """# Component wish list

## 003-01_a_1d
- Component: VolumeRatio: volume over its mean | measures: situation

## 012-01_b_1d
- Component: VolumeRatio: the same | measures: situation
- Component: LowerWick: the wick | measures: situation
"""


def run_with_wishes(root, run="x_run"):
    d = root / "03_test_plan" / run / "plans"
    d.mkdir(parents=True)
    (d / "COMPONENT_WISHLIST.md").write_text(WISHLIST)
    return d


def index(root, *lines):
    (root / "components").mkdir(exist_ok=True)
    (root / "components" / "INDEX.md").write_text("# header\n\n" + "".join(l + "\n" for l in lines))


def test_open_and_answered_wishes(tmp_path):
    run_with_wishes(tmp_path)
    assert [w[1:3] for w in W.open_wishes(["x_run"], tmp_path)] == [
        ("003-01_a_1d", "VolumeRatio"), ("012-01_b_1d", "VolumeRatio"), ("012-01_b_1d", "LowerWick")]
    index(tmp_path, "x_run | 003-01_a_1d | VolumeRatio | built: VolumeRatioComponent {}")
    assert len(W.open_wishes(["x_run"], tmp_path)) == 2
    assert W.answered(["x_run"], tmp_path)[0][3].startswith("built:")
    assert W.open_wishes(["other_run"], tmp_path) == []


def test_unblocked_needs_every_wish_answered_and_a_changed_catalogue(tmp_path):
    plans = run_with_wishes(tmp_path)
    cat = tmp_path / "catalogue.md"
    cat.write_text("v1")
    old = W.catalogue_version(cat)
    (plans / "003-01_a_1d.md").write_text(f"---\noutcome: missing-components\ncatalogue: {old}\n---\n")
    (plans / "012-01_b_1d.md").write_text("---\noutcome: missing-components\n---\n")          # before the field existed
    index(tmp_path, "x_run | 003-01_a_1d | VolumeRatio | exists: VolumeRatioComponent {}",
          "x_run | 012-01_b_1d | VolumeRatio | built: VolumeRatioComponent {}",
          "x_run | 012-01_b_1d | LowerWick | cannot build: no idea")
    assert not W.unblocked(plans / "003-01_a_1d.md", tmp_path, cat)         # same catalogue: the same refusal again
    cat.write_text("v2")
    assert W.unblocked(plans / "003-01_a_1d.md", tmp_path, cat)
    assert not W.unblocked(plans / "012-01_b_1d.md", tmp_path, cat)         # one wish cannot be built: still blocked
    (plans / "p_1d.md").write_text("---\noutcome: plan\n---\n")
    assert not W.unblocked(plans / "p_1d.md", tmp_path, cat)


CAT = """There are 2 classes.
## Component rows
### Regime measures

| Class | params (defaults) | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|
| `AComponent` | `period` (20) | x | x | x | x | x | x | x |

### Directional components

| Class | params (defaults) | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|
| `BComponent` | `window` (5), `k` (1) | x | x | x | x | x | x | x |
## Variant patterns
"""

BUILT = """answer: built
class: VolumeMeanRatioComponent
settings: {"short_period": 5, "period": 30}
reason: no class averages several bars of volume.
table: Directional components
row: | `VolumeMeanRatioComponent` | `period` (30), `short_period` (1) | o | r | graded | ratio | 30 | volume | n |

```python class
class VolumeMeanRatioComponent(SubStrategyComponent):
    pass
```

```python hand
def hand(df, params):
    return 1.0
```
"""


def test_parse_a_built_answer_and_refusals():
    a = B.parse(BUILT, CAT)
    assert a["answer"] == "built" and a["name"] == "VolumeMeanRatioComponent" and a["settings"]["short_period"] == 5
    assert a["table"] == "Directional components" and "def hand(df, params)" in a["hand"]
    assert B.parse("answer: exists\nclass: BComponent\nsettings: {\"window\": 3}\nreason: r", CAT)["name"] == "BComponent"
    assert B.parse("answer: cannot build\nreason: needs another coin", CAT)["answer"] == "cannot build"
    for bad, why in (("answer: exists\nclass: ZComponent\nsettings: {}\nreason: r", "not a class"),
                     ("answer: exists\nclass: BComponent\nsettings: {\"period\": 3}\nreason: r", "does not take"),
                     ("answer: maybe\nreason: r", "answer line"),
                     (BUILT.replace("settings: {", "settings: ["), "JSON"),
                     (BUILT.replace("table: Directional components", "table: Other"), "table line"),
                     (BUILT.replace("    pass", "    import os"), "import")):
        with pytest.raises(ValueError, match=why):
            B.parse(bad, CAT)


def test_the_files_a_build_writes():
    module = "x = 1\n\n\nclass AComponent(Base):\n    a = 1\n\n\nclass BComponent(Base):\n    b = 1\n"
    replaced = B.with_class(module, "AComponent", "class AComponent(Base):\n    a = 2\n")
    assert "a = 2" in replaced and "a = 1" not in replaced and "b = 1" in replaced
    added = B.with_class(module, "CComponent", "class CComponent(Base):\n    c = 1\n")
    assert B.classes_in(added) == ["AComponent", "BComponent", "CComponent"]
    row = "| `CComponent` | `n` (2) | x | x | x | x | x | x | x |"
    cat = B.with_count(B.with_row(CAT, "CComponent", "Regime measures", row), 3)
    lines = cat.splitlines()
    assert lines.index(row) == lines.index([l for l in lines if l.startswith("| `AComponent`")][0]) + 1
    assert cat.startswith("There are 3 classes.")
    again = B.with_row(cat, "CComponent", "Regime measures", row.replace("`n` (2)", "`n` (3)"))
    assert again.count("| `CComponent` |") == 1 and "`n` (3)" in again
    spec = B.spec_text("CComponent", {"n": 3}, "def hand(df, params):\n    return 0.0", before=[{}, {"n": 2}])
    assert 'SETTINGS = [{}, {"n": 2}, {"n": 3}]' in spec


def test_compare_leaves_out_run_ids_and_times(tmp_path):
    a, b = tmp_path / "a" / "BTCUSD", tmp_path / "b" / "BTCUSD"
    for d, rid in ((a, "r1"), (b, "r2")):
        d.mkdir(parents=True)
        (d / "protocol_summary.json.gz").write_bytes(gzip.compress(json.dumps({"run_id": rid, "x": 1}).encode()))
        (d / "metrics.json").write_text('{"sharpe": 1}')
    assert B.compare(tmp_path / "a", tmp_path / "b") == (2, [])
    (b / "metrics.json").write_text('{"sharpe": 2}')
    assert B.compare(tmp_path / "a", tmp_path / "b")[1] == ["differs: BTCUSD/metrics.json"]


def test_answers_without_a_build(monkeypatch):
    replies = iter(["answer: exists\nclass: VolumeRatioComponent\nsettings: {\"period\": 20}\nreason: same measure",
                    "nonsense", "answer: cannot build\nreason: it needs the order book"])
    monkeypatch.setattr(B, "call", lambda model, system, request: (next(replies), 0.01))
    line, usd, attempts, _, built = B.answer_wish(("x_run", "p_1d", "VolumeRatio", "- ..."), "python", "m")
    assert line == 'exists: VolumeRatioComponent {"period": 20}' and attempts == 1 and built is None
    line, usd, attempts, _, _ = B.answer_wish(("x_run", "p_1d", "Book", "- ..."), "python", "m")
    assert line == "cannot build: it needs the order book" and attempts == 2 and usd == pytest.approx(0.02)


def test_a_build_undone_keeps_its_answers_and_checks(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path / "components")
    monkeypatch.setattr(B.W, "index_path", lambda root=None: tmp_path / "components" / "INDEX.md")
    log = ["## attempt 1\n\nanswer: built\n", "checks:\nFAIL real data {}: BTCUSD: 3 of 900 bars\n"]
    B.record(("x_run", "p_1d", "Lower Wick", "- ..."), "cannot build: no answer passed", 0.1, 5.0, 3, log, None)
    kept = tmp_path / "components" / "builds" / "not_built" / "x_run" / "p_1d" / "Lower_Wick" / "answer.md"
    assert "FAIL real data" in kept.read_text()
    assert "x_run | p_1d | Lower Wick | cannot build" in (tmp_path / "components" / "INDEX.md").read_text()


def test_a_spec_s_settings_are_read_with_its_comments():
    spec = 'CLASS = "X"\nSETTINGS = [{"period": 30}, {"period": 10}]   # the first is the defaults\n'
    assert B.spec_settings(spec) == [{"period": 30}, {"period": 10}]
    assert B.spec_settings('CLASS = "X"\nSETTINGS = [{}, {"n": 2}]  # a comment\n') == [{}, {"n": 2}]
