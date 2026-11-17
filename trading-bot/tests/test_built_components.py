"""The standard checks (component_harness.py) on every component specified in tests/built_components/: warm-up, the
hand computation, the engine and the validator. The checks on real data and old defaults run when a component is built
(strategy_designer_v2/steps_cards/components), not here: they take minutes."""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import component_harness as H  # noqa: E402

SPECS = sorted((HERE / "built_components").glob("*.py"))


@pytest.mark.parametrize("spec_path", SPECS, ids=[p.stem for p in SPECS])
def test_standard_checks(spec_path):
    spec = H.load_spec(spec_path)
    cls = getattr(H.SC, spec.CLASS)
    fails = []
    for p in spec.SETTINGS:
        fails += H.check_warmup(cls, p) + H.check_engine(cls, p)
    fails += H.check_hand(cls, spec.SETTINGS, spec.hand)
    assert fails == []


def test_the_catalogue_lists_every_class_once():
    cat = HERE.parents[1] / "strategy_designer_v2" / "steps_cards" / "03_test_plan" / "helper" / "reference" / "component_catalogue.md"
    assert H.check_catalogue(cat) == []


def test_the_harness_catches_a_wrong_hand_computation_and_a_wrong_warmup():
    cls = H.SC.VolumeRatioComponent
    assert H.check_hand(cls, [{"period": 10}], lambda df, p: 1.0)
    early = type("Early", (cls,), {"is_ready": lambda self: self.data is not None})   # says ready on any row
    assert H.check_warmup(early, {"period": 10})
