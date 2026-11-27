"""Tests of step 1's own code (no model call): the header lines it accepts."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_brief as mb  # noqa: E402


def test_a_boxed_run_s_brief_may_carry_its_profile_line():
    """B2.1 (common/target_box.md): in a boxed run the brief's header names the box's profile and side."""
    text = "---\nbar: 1d\nprofile: falling calm\nside: long only\n---\nIn a falling, calm market, a theory.\nshort-name: calm fall rebound\n"
    header, body, short, *_ = mb.parse(text, False)
    assert header == ["bar: 1d", "profile: falling calm", "side: long only"] and short == "calm-fall-rebound"
    with pytest.raises(ValueError, match="outside the list"):
        mb.parse("---\nregime: calm\n---\nA theory.\n", False)
