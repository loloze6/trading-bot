"""The earlier ideas' sides (common/target_box.md, "The earlier ideas' sides"; next steps B13 and A12).

One pass gives a side to each earlier untested idea that names a market profile exactly, so that a boxed run can take it.
One closed-book model call per idea (`lib.call`), the idea's own text only (its Idea and Consequence lines: never its
"Why", which carries measured numbers). The sides go in one file, `common/earlier_idea_sides.json`; the earlier runs'
idea files are not rewritten.

  python3 common/earlier_idea_sides.py count                       the ideas concerned, by profile
  python3 common/earlier_idea_sides.py sample --n 30 --seed 1      the sample: ids and texts (to read by hand)
  python3 common/earlier_idea_sides.py ask --model haiku --file F [--ids a,b | --sample N SEED] [--max-usd 8]
                                                                    ask the model, resumable (an id in F is not asked again)

Why this cannot leak: the pass reads an idea's text only, never a result, a price or a bar.
Placed in common/ beside target_box.py: it writes the file `target_box.idea_side` reads, and both are shared definitions.
"""
import argparse, collections, json, random, re, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parent
sys.path.insert(0, str(HERE))
from lib import call, header, header_fields, profile_name, utc_now, write_atomic, IDEA_SIDES  # noqa: E402
import target_box  # noqa: E402

FILE_NAME = "earlier_idea_sides.json"
ANSWERS = IDEA_SIDES + ("unknown",)

SYSTEM = """You read one trading idea and say which side it bets, as the idea itself states it.
- long: the price rises after the idea's situation occurs (a trader would buy).
- short: the price falls after it (a trader would sell).
- both: the idea says the move goes either way, following its situation (a rise after one kind of case, a fall after the other).
- unknown: the text does not say which way the price moves.
Use only the text you are given. Do not guess from the market or the topic.
Answer on two lines. Line 1: one word, long, short, both or unknown. Line 2: the sentence of the idea, copied exactly, that shows it (empty for unknown)."""


def side_file(steps=STEPS):
    return steps / "common" / FILE_NAME


def load(path):
    return json.loads(path.read_text())["ideas"] if path.exists() else {}


def save(path, ideas):
    write_atomic(path, json.dumps({"ideas": ideas}, indent=1, ensure_ascii=False) + "\n")


def idea_text(text):
    """What the model is given: the idea's Idea and Consequence lines, nothing else."""
    try:
        _, body = header(text)
    except SystemExit:
        body = text
    lines = [m.group(0).strip() for f in ("Idea", "Consequence") if (m := re.search(rf"^{f}:\s*.+$", body, re.M))]
    return "\n".join(lines)


def earlier_ideas(steps=STEPS):
    """Every idea written in any run: {id: (run, file)}, the first run by name for an id (as B13 takes it)."""
    sys.path.insert(0, str(steps / "orchestration" / "select_next" / "helper"))
    from select_next import written_in
    runs = sorted({p.parent.name for p in steps.glob("02_ideation/*_run/ideas")}
                  | {p.parents[1].name for p in steps.glob("07?_*/*_run/*/ideas")})
    out = {}
    for r in runs:
        for f in written_in(r, steps):
            out.setdefault(f.stem, (r, f))
    return out


def concerned(steps=STEPS):
    """The ideas the pass is for: untested (no step 5 answer in any run), their `profile:` line names a profile exactly
    (two words), and nothing else gives their side (no `side:` line, no "long only" or "short only" brief).
    Returns ({id: (run, file, profile)}, counts) where counts says how many were left out and why."""
    done = target_box.answered(steps)
    out, why = {}, collections.Counter()
    for i, (r, f) in earlier_ideas(steps).items():
        text = f.read_text()
        prof = profile_name(header_fields(text).get("profile"))
        if i in done:
            why["tested"] += 1
        elif not prof or len(prof.split()) != 2:
            why["profile not exact"] += 1
        elif target_box.idea_side(text, r, steps, idea_id=None, use_file=False):
            why["side already known"] += 1
        else:
            out[i] = (r, f, prof)
    return out, why


def parse_answer(answer, text):
    """(side, sentence, sentence_in_text) from the model's answer; an answer outside the four words is `unknown`
    with the refusal recorded (common/target_box.md)."""
    lines = [l.strip() for l in answer.strip().splitlines() if l.strip()]
    word = re.sub(r"[^a-z]", "", lines[0].lower()) if lines else ""
    sentence = lines[1].strip().strip('"“”') if len(lines) > 1 else ""
    if word not in ANSWERS:
        return "unknown", "", False, f"refused: the answer began with {lines[0][:40]!r}" if lines else "refused: empty answer"
    if word == "unknown":
        return "unknown", "", False, None
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    return word, sentence, bool(sentence) and norm(sentence) in norm(text), None


def ask_one(i, run, f, prof, model):
    text = idea_text(f.read_text())
    answer, cost = call(model, SYSTEM, text)
    side, sentence, found, refused = parse_answer(answer, text)
    rec = {"run": run, "id": i, "profile": prof, "side": side, "sentence": sentence, "model": model, "date": utc_now(),
           "cost_usd": round(cost, 5)}
    if side != "unknown" and not found:
        rec["sentence_found_in_idea"] = False
    if refused:
        rec["note"] = refused
    return rec


def ask(ids, model, path, max_usd=None, workers=6, steps=STEPS):
    """Ask for the ids not yet in `path`; written after each answer; stops (nothing lost) when the spend passes max_usd."""
    todo, _ = concerned(steps)
    ideas, lock, spent = load(path), threading.Lock(), [0.0]
    ids = [i for i in ids if i in todo and i not in ideas]
    stop = threading.Event()

    def work(i):
        if stop.is_set():
            return
        r, f, prof = todo[i]
        try:
            rec = ask_one(i, r, f, prof, model)
        except SystemExit as e:                   # a refused or killed call: nothing recorded, the id stays to ask
            print(f"{i}: not answered ({e})", file=sys.stderr)
            return
        with lock:
            ideas[i] = rec
            spent[0] += rec["cost_usd"]
            save(path, ideas)
            if max_usd is not None and spent[0] >= max_usd:
                stop.set()
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(work, ids))
    print(f"asked {len(ids)}; answered now {sum(1 for i in ids if i in ideas)}; spent {spent[0]:.4f} USD; "
          f"{'STOPPED at the cap' if stop.is_set() else 'done'}")
    return spent[0], stop.is_set()


def sample_ids(todo, n, seed):
    return random.Random(seed).sample(sorted(todo), n)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("cmd", choices=["count", "sample", "ask"])
    a.add_argument("--n", type=int, default=30)
    a.add_argument("--seed", type=int, default=1)
    a.add_argument("--model", default="haiku")
    a.add_argument("--file", type=Path, default=side_file())
    a.add_argument("--ids")
    a.add_argument("--sample", nargs=2, type=int, metavar=("N", "SEED"))
    a.add_argument("--max-usd", type=float)
    a.add_argument("--workers", type=int, default=6)
    args = a.parse_args()
    todo, why = concerned()
    if args.cmd == "count":
        print(f"concerned: {len(todo)}; left out: {dict(why)}")
        c = collections.Counter(p for _, _, p in todo.values())
        for p, n in sorted(c.items()):
            print(f"  {p}: {n}")
    elif args.cmd == "sample":
        for i in sample_ids(todo, args.n, args.seed):
            r, f, p = todo[i]
            print(f"=== {i}  ({r}; {p})\n{idea_text(f.read_text())}\n")
    else:
        ids = (args.ids.split(",") if args.ids else sample_ids(todo, *args.sample) if args.sample else sorted(todo))
        ask(ids, args.model, args.file, args.max_usd, args.workers)


if __name__ == "__main__":
    main()
