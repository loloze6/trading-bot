"""The wishes of the runs and their answers: what the components step reads, and what select_next and run_idea ask it.

A wish is one line step 3 wrote in a run's COMPONENT_WISHLIST.md when it refused an idea as missing-components. Its
answer is one line in components/INDEX.md: `<run> | <plan id> | <wish name> | built: ... | exists: ... | cannot build: ...`.
Card: ../card.md. Code only: no model call.
"""
import re, sys
from pathlib import Path

STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import CATALOGUE, catalogue_version, header_fields  # noqa: E402  (shared helpers, common/lib.py)

WISH = re.compile(r"^- Component:\s*(.+)$", re.M)
ANSWERS = ("built", "exists", "cannot build")


def wish_name(line):
    """A wish's name: what step 3 wrote before the first colon (its short name)."""
    return line.split(":", 1)[0].strip().strip("`").strip()


def wishes_of(run, root=STEPS):
    """{plan id: [(wish name, wish text), ...]} from the run's COMPONENT_WISHLIST.md, as it stands."""
    p = root / "03_test_plan" / run / "plans" / "COMPONENT_WISHLIST.md"
    out = {}
    if not p.exists():
        return out
    for block in re.split(r"^## ", p.read_text(), flags=re.M)[1:]:
        pid, _, body = block.partition("\n")
        out[pid.strip()] = [(wish_name(w), w.strip()) for w in WISH.findall(body)]
    return out


def index_path(root=STEPS):
    return root / "components" / "INDEX.md"


def answers(root=STEPS):
    """{(run, plan id, wish name): answer} from components/INDEX.md (the last line wins)."""
    p = index_path(root)
    out = {}
    for l in (p.read_text().splitlines() if p.exists() else []):
        parts = [x.strip() for x in l.split(" | ", 3)]
        if len(parts) == 4 and parts[0].endswith("_run"):
            out[tuple(parts[:3])] = parts[3]
    return out


def answer_kind(answer):
    return next((k for k in ANSWERS if answer.startswith(k + ":")), None)


def open_wishes(runs, root=STEPS):
    """[(run, plan id, wish name, wish text)] for the wishes of these runs with no line in the index."""
    done = answers(root)
    return [(run, pid, name, text) for run in runs for pid, ws in wishes_of(run, root).items() for name, text in ws
            if (run, pid, name) not in done]


def answered(runs, root=STEPS):
    """[(run, plan id, wish name, answer)] for the wishes of these runs that have a line in the index."""
    done = answers(root)
    return [(run, pid, name, done[(run, pid, name)]) for run in runs for pid, ws in wishes_of(run, root).items()
            for name, _ in ws if (run, pid, name) in done]


def unblocked(plan, root=STEPS, catalogue=CATALOGUE):
    """True when a missing-components plan's idea can be planned again: every wish of its refusal is answered built
    or exists, and the catalogue has changed since the refusal (a refusal written with today's catalogue would be the
    same refusal again: it stays blocked, a finding on step 3)."""
    from_header = header_fields(Path(plan).read_text())
    if from_header.get("outcome") != "missing-components":
        return False
    if from_header.get("catalogue") == catalogue_version(catalogue):
        return False
    run, pid = Path(plan).parents[1].name, Path(plan).stem
    ws = wishes_of(run, root).get(pid, [])
    done = answers(root)
    return bool(ws) and all(answer_kind(done.get((run, pid, name), "")) in ("built", "exists") for name, _ in ws)
