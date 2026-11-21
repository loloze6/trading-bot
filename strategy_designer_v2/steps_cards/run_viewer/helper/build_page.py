"""Run viewer: read the runs' committed files in steps_cards/ and write one self-contained page, runs.html.

Read only. Standard library only. No price data, no model call. Every figure on the page is a field of a committed
file, or a count, sum, mean or product of such fields (card: run_viewer/card.md).

    python build_page.py [--cards STEPS_CARDS_DIR] [--out FILE]
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARDS = HERE.parent.parent                      # steps_cards/
IDEA_ID = re.compile(r"^\d{3}-\d{2}_[\w.-]+$")   # 011-01_weekend-rise-reverses-monday.b1_...
BAR_SUFFIX = re.compile(r"_(\d+[smhdw])$")       # a backtest id is the idea id plus its bar: ..._1d
FULL_DATE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d")  # a journal "at" with its day (journals before 2026-11-17: time only)


def stamp(at):
    """'2026-11-17T19:41:09Z' or '...+00:00' -> '2026-11-17 19:41'; None for a time without its day."""
    return at[:16].replace("T", " ") if isinstance(at, str) and FULL_DATE.match(at) else None


def read_text(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def read_json(p):
    t = read_text(p)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def read_jsonl(p):
    t = read_text(p)
    out = []
    for line in (t or "").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def front_matter(text):
    """The `key: value` lines between the first two `---` lines, and the body after them."""
    if not text or not text.startswith("---"):
        return {}, text or ""
    parts = text.split("\n---", 1)
    head = parts[0][3:]
    body = parts[1].lstrip("-\n") if len(parts) > 1 else ""
    fm = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def words(slug):
    """'011-01_weekend-rise-reverses-monday' -> 'weekend rise reverses monday' (the id's last segment, in words)."""
    last = slug.split(".")[-1]
    last = last.split("_", 1)[1] if "_" in last else last
    return last.replace("-", " ")


def parent_of(idea):
    return idea.rsplit(".", 1)[0] if "." in idea else None


def line_of(idea):
    """The step 7 line that wrote the idea: the letter of its last segment (b1 -> 7.b); None for a step 2 idea."""
    if "." not in idea:
        return None
    m = re.match(r"([a-z])\d+_", idea.rsplit(".", 1)[1])
    return f"7.{m.group(1)}" if m else None


def idea_of_backtest(bid):
    return BAR_SUFFIX.sub("", bid)


def labelled(text, label):
    """The paragraph that starts with `label` (e.g. 'Reason:'), up to the next 'Word:' line or the end."""
    m = re.search(rf"^{re.escape(label)}\s*(.*?)(?=^\w[\w -]*:|\Z)", text or "", re.M | re.S)
    return m.group(1).strip() if m else None


def run_brief_file(cards, run):
    """The run brief is steps_cards/runs/<NAME>_RUN.md; the longest such name that the run's name starts with
    (night_005_run -> NIGHT_RUN.md)."""
    stem = run[: -len("_run")].upper()
    best = None
    for p in (cards / "runs").glob("*_RUN.md"):
        name = p.name[: -len("_RUN.md")]
        if (stem == name or stem.startswith(name + "_")) and (best is None or len(name) > len(best[0])):
            best = (name, p)
    return best[1] if best else None


def purpose(text):
    m = re.search(r"\*\*Purpose\.\*\*\s*(.*?)(?=\n\s*\n\*\*|\n## |\Z)", text or "", re.S)
    return m.group(1).strip() if m else None


def run_names(cards):
    names = set()
    for step in cards.iterdir():
        if step.is_dir():
            names |= {p.name for p in step.iterdir() if p.is_dir() and p.name.endswith("_run")}
    orch = cards / "orchestration"
    if orch.is_dir():
        for f in orch.iterdir():
            if f.is_dir():
                names |= {p.name for p in f.iterdir() if p.is_dir() and p.name.endswith("_run")}
    return sorted(names)


def idea_files(cards):
    """id -> path of the idea's file, for every idea file in step 2's and step 7's folders."""
    out = {}
    for p in sorted(cards.glob("02_ideation/*/ideas/*.md")) + sorted(cards.glob("07*/*/*/ideas/*.md")):
        if IDEA_ID.match(p.stem):
            out.setdefault(p.stem, []).append(p)
    return out


def idea_text(files, idea, run):
    paths = files.get(idea, [])
    own = [p for p in paths if p.parts[-3] == run and p.parts[-4] == "02_ideation"]
    for p in own + paths:
        t = read_text(p)
        if t is not None:
            return t
    return None


WINDOW_FIELDS = ("net_return_pct", "trade_count", "win_rate", "max_drawdown_pct", "sharpe", "exposure_pct")


def book_by_window(bt_dir):
    """Each window's net return (metrics.json) averaged over the coins, chained in the windows' time order (the
    window's last bar, manifest.json); per coin, its windows' own figures. Only years are returned, no data date; `ran`
    is when the engine ran (manifest created_utc, the earliest)."""
    per_window, coins, ran = {}, {}, []
    for coin in sorted(p for p in bt_dir.iterdir() if p.is_dir()):
        rows = {}
        for w in coin.glob("w*"):
            m = read_json(w / "metrics.json")
            man = read_json(w / "manifest.json")
            try:
                core = m["core"]
                r = float(core["net_return_pct"])
                end = str(man["data"]["end"])
            except (TypeError, KeyError, ValueError):
                continue
            be = m.get("bar_equity") or {}
            rows[w.name] = [r, core.get("trade_count"), core.get("win_rate"), be.get("max_drawdown_pct"),
                            be.get("sharpe"), be.get("exposure_pct")]
            slot = per_window.setdefault(w.name, {"returns": [], "end": end})
            slot["returns"].append(r)
            slot["end"] = max(slot["end"], end)
            if man.get("created_utc"):
                ran.append(str(man["created_utc"]))
        if rows:
            coins[coin.name] = rows
    if not per_window:
        return None
    order = sorted(per_window, key=lambda w: per_window[w]["end"])
    value, values, years = 1.0, [1.0], []
    for w in order:
        rs = per_window[w]["returns"]
        value *= 1 + sum(rs) / len(rs) / 100
        values.append(round(value, 5))
        years.append(per_window[w]["end"][:4])
    per_coin = {c: [rows.get(w) for w in order] for c, rows in coins.items()}
    return {"windows": order, "values": values, "years": years, "coins": list(coins),
            "coin_windows": sum(len(per_window[w]["returns"]) for w in order),
            "fields": list(WINDOW_FIELDS), "per_coin": per_coin,
            "ran": stamp(min(ran)) if ran else None, "ran_last": stamp(max(ran)) if ran else None}


def step3(plan_path):
    text = read_text(plan_path)
    if text is None:
        return None
    fm, body = front_matter(text)
    return {"outcome": fm.get("outcome") or "not in the record", "fit": fm.get("fit"),
            "reason": labelled(body, "Reason:"), "idea": fm.get("idea"),
            "data": ", ".join(x for x in (fm.get("data-instruments"), fm.get("data-bar"), fm.get("data-period")) if x)}


def step5(path):
    r = read_json(path)
    if not isinstance(r, dict):
        return None
    mm = r.get("main_measure") or {}
    st = mm.get("statistic") or {}
    sc = r.get("supporting_check") or {}
    return {"status": r.get("status"), "t": st.get("value"), "t_name": st.get("name"), "measure": mm.get("name"),
            "threshold": mm.get("threshold"), "decided_by": r.get("decided_by"),
            "support": sc.get("name"), "support_passed": sc.get("passed"), "counts": r.get("counts"),
            "situation": (r.get("situation_check") or {}).get("agreement"),
            "situation_passed": (r.get("situation_check") or {}).get("passed")}


def step6(path):
    r = read_json(path)
    if not isinstance(r, dict):
        return None
    ms = [{"label": m.get("label"), "value": m.get("value"), "threshold": m.get("threshold"),
           "comparison": m.get("comparison"), "passed": m.get("passed")} for m in r.get("measures", [])]
    sharpe = next((m.get("value") for m in r.get("measures", []) if m.get("measure") == "sharpe_min"), None)
    return {"status": r.get("status"), "measures": ms, "failed": [m["label"] for m in ms if m["passed"] is False],
            "decided_by": r.get("decided_by"), "sharpe": sharpe}


def step7(cards, run, bid):
    out = []
    for p in sorted(cards.glob(f"07*/{run}/{bid}/result.json")):
        r = read_json(p)
        if not isinstance(r, dict):
            continue
        ids = r.get("idea_ids") or []
        ideas = []
        for k, i in enumerate(r.get("ideas") or []):
            ideas.append({"name": i.get("name"), "idea": i.get("idea"), "id": ids[k] if k < len(ids) else None})
        out.append({"line": r.get("line"), "folder": p.parts[-4], "findings": r.get("findings") or {},
                    "ideas": ideas, "no_ideas": r.get("no_ideas"), "cost": r.get("cost")})
    return out


def all_briefs(cards):
    """brief number ('011') -> {id, title, text, runs}, from every run's brief folder."""
    out = {}
    for p in sorted(cards.glob("01_brief/*/briefs/*.md")):
        if not re.match(r"^\d{3}_", p.stem):
            continue
        b = out.setdefault(p.stem.split("_")[0], {"id": p.stem, "title": words(p.stem), "text": None, "runs": []})
        b["runs"].append(p.parts[-3])
        if b["text"] is None:
            b["text"] = front_matter(read_text(p))[1].strip()
    return out


def build_run(cards, run, files):
    rb = run_brief_file(cards, run)
    rb_text = read_text(rb) if rb else None
    briefs = []
    for p in sorted(cards.glob(f"01_brief/{run}/briefs/*.md")):
        fm, body = front_matter(read_text(p))
        briefs.append({"id": p.stem, "title": words(p.stem), "text": body.strip()})

    # the run's backtests: every id any step wrote for this run
    plans = {p.stem: p for p in cards.glob(f"03_test_plan/{run}/plans/*.md")
             if IDEA_ID.match(idea_of_backtest(p.stem)) and BAR_SUFFIX.search(p.stem)}
    bids = set(plans)
    for pat in (f"04_backtest/{run}/backtests/*", f"05_verification/{run}/verdicts/*",
                f"06_profitability/{run}/checks/*", f"07*/{run}/*"):
        bids |= {p.name for p in cards.glob(pat) if p.is_dir() and BAR_SUFFIX.search(p.name)}

    journal = read_jsonl(cards / f"orchestration/run_idea/{run}/journal.jsonl")
    brief_journal = read_jsonl(cards / f"orchestration/run_brief/{run}/journal.jsonl")
    turns = read_jsonl(cards / f"orchestration/loop/{run}/loop.jsonl")
    queue = read_json(cards / f"orchestration/loop/{run}/queue.json") or []

    backtests = {}
    for bid in sorted(bids):
        s3 = step3(plans[bid]) if bid in plans else None
        idea = (s3 or {}).get("idea") or idea_of_backtest(bid)
        cost, dated = {}, []
        for j in journal:
            if j.get("backtest") == bid:
                if stamp(j.get("at")):
                    dated.append(stamp(j.get("at")))
                c = cost.setdefault(j.get("step", "?"), {"usd": 0.0, "seconds": 0.0, "ran": False})
                c["ran"] = c["ran"] or j.get("action") == "called"
                c["usd"] += float(j.get("usd") or 0)
                c["seconds"] += float(j.get("seconds") or 0)
        bt_dir = cards / f"04_backtest/{run}/backtests/{bid}"
        backtests[bid] = {
            "id": bid, "idea": idea, "step3": s3, "dated": sorted(dated),
            # where its chart files would be; the page reads the committed names, then the .local ones (step 4)
            "chart": f"04_backtest/{run}/backtests/{bid}/" if bt_dir.is_dir() else None,
            "book": book_by_window(bt_dir) if bt_dir.is_dir() else None,
            "step5": step5(cards / f"05_verification/{run}/verdicts/{bid}/result.json"),
            "step6": step6(cards / f"06_profitability/{run}/checks/{bid}/result.json"),
            "step7": step7(cards, run, bid),
            "cost": {k: {"usd": round(v["usd"], 4), "seconds": round(v["seconds"], 1), "ran": v["ran"]} for k, v in cost.items()},
        }

    # the run's ideas: step 2's folder, the tested ones, the ones step 7 proposed, the queue
    ids = {p.stem for p in cards.glob(f"02_ideation/{run}/ideas/*.md") if IDEA_ID.match(p.stem)}
    ids |= {b["idea"] for b in backtests.values()}
    ids |= {i["id"] for b in backtests.values() for s in b["step7"] for i in s["ideas"] if i["id"]}
    ids |= {q["idea"] for q in queue if q.get("idea")}
    q_by = {q["idea"]: q for q in queue if q.get("idea")}
    turn_by = {}
    for t in turns:
        turn_by.setdefault(t.get("idea"), {"turn": t.get("turn"), "why": t.get("why")})
    ideas = {}
    for i in sorted(ids):
        fm, body = front_matter(idea_text(files, i, run))
        q = q_by.get(i)
        mine = [b for b in backtests if backtests[b]["idea"] == i]
        first = sorted(x for b in mine for x in backtests[b]["dated"])
        if not first:
            first = sorted(backtests[b]["book"]["ran"] for b in mine if backtests[b]["book"] and backtests[b]["book"]["ran"])
        ideas[i] = {"id": i, "title": words(i), "parent": parent_of(i), "line": line_of(i), "brief": i[:3],
                    "dated": first[0] if first else None,
                    "text": body.strip() or None, "statement": labelled(body, "Idea:"),
                    "backtests": sorted(b for b in backtests if backtests[b]["idea"] == i),
                    "queue": {"status": q.get("status"), "score": q.get("score")} if q else None,
                    "turn": turn_by.get(i)}
    for i in ideas.values():
        i["children"] = sorted(c for c in ideas if ideas[c]["parent"] == i["id"])
        i["root"] = i["parent"] not in ideas
    roots = [i for i in sorted(ideas) if ideas[i]["root"]]
    for i in ideas.values():
        bs = [backtests[b] for b in i["backtests"]]
        q = (i["queue"] or {}).get("status") or ""
        if any(b["book"] or b["step5"] for b in bs):
            i["state"] = "backtested"
        elif any(b["step3"] and b["step3"]["outcome"] not in ("plan", None) for b in bs):
            i["state"] = "blocked at step 3"
        elif bs:
            i["state"] = "planned, not backtested"
        elif q.startswith("duplicate"):
            i["state"] = "duplicate"
        elif q == "candidate":
            i["state"] = "waiting in the queue"
        else:
            i["state"] = "not tested"

    # totals: counts of the steps' own statuses, sums of the journals
    tested = [b for b in backtests.values() if b["step3"] or b["step5"] or b["book"]]
    count = lambda key: _count(b[key]["status"] for b in backtests.values() if b[key])
    lines = journal + brief_journal
    usd = sum(float(j.get("usd") or 0) for j in lines)
    secs = sum(float(j.get("seconds") or 0) for j in lines)
    return {
        "name": run, "run_brief": rb.name if rb else None, "run_brief_text": rb_text, "purpose": purpose(rb_text),
        "briefs": briefs, "ideas": ideas, "roots": roots, "backtests": backtests,
        "dates": run_dates(journal + brief_journal + turns, backtests),
        "totals": {"ideas": len(ideas), "backtests": len(tested), "idea_states": _count(i["state"] for i in ideas.values()),
                   "bars": _count(bar_of(b["id"]) for b in tested),
                   "step3": _count((b["step3"] or {}).get("outcome") for b in backtests.values() if b["step3"]),
                   "step5": count("step5"), "step6": count("step6"),
                   "best_t": best(backtests, "step5", "t"), "best_sharpe": best(backtests, "step6", "sharpe"),
                   "levels": levels(ideas),
                   "usd": round(usd, 2) if lines else None, "seconds": round(secs) if lines else None,
                   "turns": len(turns), "journal_lines": len(lines)},
    }


def run_dates(lines, backtests):
    """The earliest and latest full timestamps in the run's record: journal lines dated in full, backtests' engine runs."""
    when = [stamp(j.get("at")) for j in lines if stamp(j.get("at"))]
    for b in backtests.values():
        if b["book"] and b["book"]["ran"]:
            when += [b["book"]["ran"], b["book"]["ran_last"]]
    return [min(when), max(when)] if when else None


def best(backtests, step, key):
    """Per status of a step, the largest of its key figure (step 5: t; step 6: Sharpe) over the run's backtests."""
    out = {}
    for b in backtests.values():
        s = b[step]
        if s and isinstance(s.get(key), (int, float)):
            out[s["status"]] = max(out.get(s["status"], s[key]), s[key])
    return out


def bar_of(bid):
    """A backtest's bar size, the last part of its id: '..._1d' -> '1d', '..._4h' -> '4h'."""
    m = re.search(r"_(\d+[smhdw])$", bid)
    return m.group(1) if m else "bar not in the id"


def level_of(idea):
    """An idea's level below its brief: 1 for the brief's own ideas, 2 for an idea written from one of them, and so on
    (the id is the lineage: one segment per generation)."""
    return idea.count(".") + 1


def levels(ideas):
    """Per level: the ideas, and those backtested."""
    out = {}
    for iid, i in ideas.items():
        n = out.setdefault(level_of(iid), {"level": level_of(iid), "ideas": 0, "tested": 0})
        n["ideas"] += 1
        n["tested"] += i["state"] == "backtested"
    return [out[k] for k in sorted(out)]


def step7_lines(cards):
    """The step 7 lines' names, from their folders: 07g_patterns -> {"7.g": "patterns"}."""
    return {f"7.{p.name[2]}": p.name[4:].replace("_", " ") for p in sorted(cards.glob("07[a-z]_*")) if p.is_dir()}


def _count(values):
    out = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out


def build(cards):
    files = idea_files(cards)
    runs = [build_run(cards, r, files) for r in run_names(cards)]
    runs.sort(key=lambda r: (r["dates"] or ["", ""])[1], reverse=True)   # last updated first
    return {"runs": runs, "briefs": all_briefs(cards), "lines": step7_lines(cards)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cards", type=Path, default=CARDS)
    ap.add_argument("--out", type=Path, default=HERE.parent / "runs.html")
    a = ap.parse_args()
    data = build(a.cards)
    page = (HERE / "page.html").read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    a.out.write_text(page.replace("/*DATA*/null", blob), encoding="utf-8")
    n = sum(len(r["backtests"]) for r in data["runs"])
    print(f"{a.out}: {len(data['runs'])} runs, {n} backtests, {a.out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
