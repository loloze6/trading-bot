"""CUL-213 (class closure): every module that prints an emoji must carry a
module-level cp1252 stdout guard, so it cannot raise UnicodeEncodeError when its
stdout is redirected/piped/captured on a Windows console — the failure mode
already fixed one-off for setup_run.py (CUL-12), run_phase1_research.py, and the
spawned children prescreen_signal.py / run_protocol.py.

This is the structural control (cheapest that scales): rather than a subprocess
test per module, scan the entry-point/tool source trees for any `print(...)`
containing a non-ASCII character and assert the enclosing module installs the
guard at module level. Whitelist nothing — a module that legitimately cannot
carry the guard is a finding to surface here, not a skip to hide.
"""

import ast
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

# Trees that hold campaign entry points and the tools they spawn as captured
# subprocesses — every emoji print reachable by an unattended run lives here.
_SCAN_ROOTS = (
    "strategy-research/tools",
    "strategy-research/workflow",
    "trading-bot/tools",
)


def _has_emoji_print(src: str) -> bool:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            seg = ast.get_source_segment(src, node) or ""
            if any(ord(c) > 127 for c in seg):
                return True
    return False


def _has_module_level_stdout_guard(src: str) -> bool:
    """True if a *module-level* statement reconfigures sys.stdout with
    errors="replace" (the CUL-12 pattern). Walks only tree.body so a guard
    hidden inside a function — which would not run before the prints — does
    not count."""
    tree = ast.parse(src)
    top = "\n".join(seg for node in tree.body if (seg := ast.get_source_segment(src, node)))
    return "sys.stdout" in top and "reconfigure" in top and 'errors="replace"' in top


def _emoji_print_modules() -> list[Path]:
    mods: list[Path] = []
    for rel in _SCAN_ROOTS:
        root = _REPO / rel
        assert root.is_dir(), f"scan root missing: {rel}"
        for f in sorted(root.rglob("*.py")):
            if _has_emoji_print(f.read_text(encoding="utf-8")):
                mods.append(f)
    return mods


def test_every_emoji_printing_module_carries_the_cp1252_guard():
    mods = _emoji_print_modules()
    assert mods, "structural scan found no emoji-printing modules — roots wrong?"
    unguarded = [
        str(f.relative_to(_REPO)) for f in mods if not _has_module_level_stdout_guard(f.read_text(encoding="utf-8"))
    ]
    assert not unguarded, (
        "emoji-printing modules missing the module-level cp1252 stdout guard "
        '(reconfigure(errors="replace") on sys.stdout — the CUL-12 pattern): '
        f"{unguarded}"
    )
