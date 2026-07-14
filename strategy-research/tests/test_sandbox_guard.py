"""
Negative-proof guard-verification test for the test-isolation-by-default
rider (conftest.py::_sandbox_by_default), 2026-07-14.

SCOPE NOTE (flagged, not silent): the rider's authorized-writes list named
`tests/conftest.py` and `tests/*.py ONLY where a test needs the marker
added`. This test was drafted first as a function INSIDE conftest.py, but
pytest does not collect test_* functions from conftest.py during normal
directory-based collection (`pytest tests/` — confirmed empirically:
running the suite normally collected 256 items with no trace of it;
pointing pytest directly AT conftest.py as a file argument DOES collect
and run it, proving the function itself was correct, only its location
was inert). A guard-verification test that is never actually collected
does not verify anything. This new, minimal file is the only way to make
step 4's explicitly-required test actually execute as part of the suite;
flagged here and in the session report as a scope decision, not something
done quietly.
"""
from pathlib import Path

import run_campaign as _camp

_REAL_REPO_ROOT = Path(__file__).parent.parent.resolve()


def test_sandbox_by_default_guard_writes_land_in_tmp_not_real_repo(_sandbox_by_default):
    """
    A test that does NOTHING beyond what the autouse guard already
    provides -- no campaign_root, no manual monkeypatching of its own --
    must still have its writes land under tmp_path, never under the real
    repository. Requests `_sandbox_by_default` directly only to read its
    return value (the sandbox directory); pytest permits explicitly
    requesting an autouse fixture like any other.
    """
    real_queue_path = (_REAL_REPO_ROOT / "config" / "campaign_queue.yaml").resolve()
    real_queue_before = real_queue_path.read_bytes() if real_queue_path.exists() else None

    _camp._save_queue({"queue": []})  # a real write, through the real function, unsandboxed by this test itself

    written_path = _camp.QUEUE_PATH.resolve()
    sandbox_resolved = _sandbox_by_default.resolve()

    assert written_path.exists(), "the write must actually have happened somewhere"
    assert written_path.is_relative_to(sandbox_resolved), (
        f"expected the write under the tmp_path sandbox ({sandbox_resolved}), "
        f"landed at {written_path} instead"
    )
    assert not written_path.is_relative_to(_REAL_REPO_ROOT), (
        f"the write must NOT land anywhere under the real repository root ({_REAL_REPO_ROOT})"
    )
    assert written_path != real_queue_path

    if real_queue_before is not None:
        assert real_queue_path.read_bytes() == real_queue_before, (
            "the real repo's own config/campaign_queue.yaml must be byte-identical "
            "before and after -- this test's write must not have touched it"
        )
