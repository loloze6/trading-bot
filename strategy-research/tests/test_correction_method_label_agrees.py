"""
Issue #40: the two DSR paths must write the SAME correction_method label.

The deflated-Sharpe correction is computed in two places meant to be in
lockstep, and they wrote different labels for the same method:

    workflow/run_phase1_research.py  ->  "baiey_lopez_prado_2014"   (misspelled)
    tools/deflate_sharpe.py          ->  "bailey_lopezdeprado_2014" (correct)

`correction_method` is written into artifacts, so anything filtering on the
library spelling silently returned NOTHING for pipeline-produced runs -- a
query that looks like "no results" rather than "broken filter", which is the
failure mode worth guarding.

Fixed by correcting the pipeline spelling. No backward-compatibility shim was
needed and none was added: at fix time the misspelling appeared in exactly one
file (the pipeline's own write sites), no committed artifact carried it, and
nothing in either repo READ the field. Verified before changing anything --
adding a dual-spelling reader would have been complexity paying for a
compatibility problem that did not exist.

This test pins AGREEMENT rather than the literal string, because the defect was
divergence between two mirrored sites, not the typo itself. Renaming the method
in future is fine; renaming it in only one of the two places is not.
"""
import re
import sys
from pathlib import Path

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

_PIPELINE = _SR / "workflow" / "run_phase1_research.py"
_LIBRARY = _SR / "tools" / "deflate_sharpe.py"

# The Bailey/Lopez de Prado deflated Sharpe label. Other correction methods
# (e.g. the expectancy t-stat Bonferroni path) are deliberately out of scope --
# they are a different method, not a mirrored copy of this one.
_DSR_LABEL_RE = re.compile(r'"correction_method"\s*:\s*"(bail\w*|baiey\w*)"')


def _dsr_labels(path: Path) -> set:
    return set(_DSR_LABEL_RE.findall(path.read_text(encoding="utf-8")))


def test_both_paths_write_the_same_dsr_label():
    pipeline = _dsr_labels(_PIPELINE)
    library = _dsr_labels(_LIBRARY)
    assert pipeline, f"no DSR correction_method label found in {_PIPELINE.name}"
    assert library, f"no DSR correction_method label found in {_LIBRARY.name}"
    assert pipeline == library, (
        f"the two DSR paths disagree on correction_method: "
        f"{_PIPELINE.name} writes {sorted(pipeline)}, "
        f"{_LIBRARY.name} writes {sorted(library)}. They are mirrored "
        f"computations and must label themselves identically, or a filter on "
        f"one spelling silently returns nothing for runs produced by the other."
    )


def test_each_path_is_internally_consistent():
    """Four write sites in the pipeline, two in the library -- each file must
    use ONE spelling throughout, or the divergence is inside a single file."""
    assert len(_dsr_labels(_PIPELINE)) == 1, "pipeline uses more than one DSR label"
    assert len(_dsr_labels(_LIBRARY)) == 1, "library uses more than one DSR label"


def test_the_known_misspelling_is_gone():
    """The specific regression. Guards the exact string so a revert is caught
    by name, not only by the agreement test above."""
    for path in (_PIPELINE, _LIBRARY):
        assert "baiey_lopez_prado_2014" not in path.read_text(encoding="utf-8"), (
            f"{path.name} still carries the issue #40 misspelling"
        )
