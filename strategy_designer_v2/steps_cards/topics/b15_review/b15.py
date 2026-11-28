"""B15 (topics/NEXT_STEPS.md, runs/B15_RUN.md): can a run's test, on its drawn coins, confirm an effect that is real
on the 25 portfolio coins? No model call.

For each sampled strategy (confirmed by step 5 on its common record):
1. step 4 is rerun on the 25 portfolio coins (common_record's own `backtest`, unchanged), into a local folder
   (never committed: the windows' bars);
2. step 5 (make_verdict.py --measure, the strategy's own stored measure.py) is applied to that record: on the 25 coins
   as the common record did (no data_use.json), on the 25 coins as a run does (data_use.json: the direction check on
   the check half), then on DRAWS draws of 8, 12 and 16 coins (the research draw's rule, coins.research_draw, the
   size its only change; the seed is the draw's name), each as a run does;
3. one small result file per strategy is written in draws/ (committed).

WHY THIS CANNOT LEAK: nothing changes how a bar is read. Step 4 and step 5 are called unchanged; a draw is a folder of
links to some of the record's coins. The coins come from portfolio_group(): no final coin is read.

  python3 b15.py --sample                      the sample (sample.json), drawn once by a fixed seed
  python3 b15.py --shard i/n --python VENV_PYTHON [--work DIR]
"""
import argparse, json, os, random, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
sys.path.insert(0, str(STEPS / "common"))
sys.path.insert(0, str(STEPS / "orchestration" / "common_record" / "helper"))
import coins  # noqa: E402
import common_record as cr  # noqa: E402

SEED, SAMPLE_SIZE = "B15", 30
SIZES, DRAWS = (8, 12, 16), 40
RESULTS, SAMPLE = HERE / "draws", HERE / "sample.json"     # not "results": git ignores that name here


def confirmed_records():
    out = []
    for f in sorted((STEPS / "orchestration" / "common_record").glob("*_run/*.json")):
        r = json.loads(f.read_text())
        if r["step5"]["status"] == "confirmed":
            out.append(r)
    return out


def make_sample():
    recs = confirmed_records()
    keys = sorted(f"{r['run']}/{r['id']}" for r in recs)
    picked = sorted(random.Random(SEED).sample(keys, SAMPLE_SIZE))
    by = {f"{r['run']}/{r['id']}": r for r in recs}
    # shards of about equal engine time: by the stored seconds, longest first, dealt in turn
    order = sorted(picked, key=lambda k: -by[k]["seconds"])
    SAMPLE.write_text(json.dumps({"seed": SEED, "among": len(keys), "order": order}, indent=1) + "\n")
    print(f"{len(picked)} of {len(keys)} confirmed common records; written {SAMPLE.name}")


def draw(name, drawable, size):
    """coins.research_draw with the size its only change."""
    old = coins.RESEARCH_SIZE
    coins.RESEARCH_SIZE = size
    try:
        return coins.research_draw(name, drawable)
    finally:
        coins.RESEARCH_SIZE = old


def verdict(plan, measure, python, record, coin_list, du, tmp):
    """Step 5 on the record's coins in coin_list, as it is; with du, as a run does (the direction check)."""
    root = Path(tempfile.mkdtemp(dir=tmp))
    sub = root / "records" / plan.stem
    sub.mkdir(parents=True)
    (sub / "config.json").write_bytes((record / "config.json").read_bytes())
    n = 0
    for c in coin_list:
        src = record / f"{c}USD"
        if list(src.glob("w*/bars.csv.gz")):
            os.symlink(src, sub / f"{c}USD")
            n += len(list(src.glob("w*/bars.csv.gz")))
    if du:
        (sub / "data_use.json").write_text(json.dumps({**du, "research_coins": coin_list}))
    r = subprocess.run([sys.executable, str(STEPS / "05_verification/helper/make_verdict.py"), str(plan), "--python",
                        python, "--records-root", str(root / "records"), "--verdicts-dir", str(root / "verdicts"),
                        "--measure", str(measure)], capture_output=True, text=True)
    p = root / "verdicts" / plan.stem / "result.json"
    if not p.exists():
        return {"coins": coin_list, "coin_windows": n, "status": "no verdict", "why": (r.stdout + r.stderr)[-300:]}
    v = json.loads(p.read_text())
    st = (v.get("main_measure") or {}).get("statistic")
    dc = v.get("direction_check") or {}
    return {"coins": coin_list, "coin_windows": n, "status": v["status"],
            "t": st.get("value") if isinstance(st, dict) else None, "main": (v.get("main_measure") or {}).get("value"),
            "direction_agrees": dc.get("agrees"), "direction_t": dc.get("statistic")}


def one(key, python, work):
    run, rid = key.split("/", 1)
    out = RESULTS / f"{run}__{rid}.json"
    if out.exists():
        return
    stored = json.loads((STEPS / "orchestration" / "common_record" / run / f"{rid}.json").read_text())
    plan = STEPS / stored["plan"]
    # the record's measure.py; a record made before the field existed used its own run's (common_record's default)
    measure = STEPS / stored.get("measure", f"05_verification/{run}/verdicts/{rid}/measure.py")
    windows = json.loads(cr.WINDOWS.read_text())
    group = coins.portfolio_group()
    record = work / "records" / run / rid
    t0 = time.time()
    if not cr.ran(record):
        print(cr.backtest(plan, python, record, windows, group), flush=True)
    t_engine = time.time() - t0
    du = coins.new_data_use("b15", python)
    drawable = coins.drawable(du["draw"]["testable"], du["draw"]["needed"])
    tmp = work / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    res = {"key": key, "stored": {"status": stored["step5"]["status"], "t": stored["step5"]["statistic"],
                                  "coin_windows": stored["windows_run"], "step6": stored["step6"]["status"]},
           "all25_as_common_record": verdict(plan, measure, python, record, group, None, tmp),
           "all25_as_a_run": verdict(plan, measure, python, record, group, du, tmp),
           "drawable": drawable, "draws": {}}
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:      # step 5 is one process per call
        for size in SIZES:
            lists = [draw(f"b15_draw_{i:03d}", drawable, size) for i in range(1, DRAWS + 1)]
            res["draws"][str(size)] = list(pool.map(lambda cl: verdict(plan, measure, python, record, cl, du, tmp), lists))
    res["seconds"] = {"engine": round(t_engine, 1), "all": round(time.time() - t0, 1)}
    RESULTS.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=1) + "\n")
    c = {s: sum(d["status"] == "confirmed" for d in ds) for s, ds in res["draws"].items()}
    print(f"{key}: 25 coins {res['all25_as_common_record']['status']} / as a run {res['all25_as_a_run']['status']}; "
          f"confirmed on {c['8']}/{DRAWS} draws of 8, {c['12']}/{DRAWS} of 12, {c['16']}/{DRAWS} of 16; "
          f"{res['seconds']['engine']:.0f} s engine, {res['seconds']['all']:.0f} s in all", flush=True)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--sample", action="store_true")
    a.add_argument("--shard")
    a.add_argument("--python")
    a.add_argument("--work", type=Path, default=Path.home() / "b15_work")
    args = a.parse_args()
    if args.sample:
        return make_sample()
    i, n = (int(x) for x in args.shard.split("/"))
    order = json.loads(SAMPLE.read_text())["order"]
    for key in order[i - 1::n]:
        one(key, args.python, args.work)


if __name__ == "__main__":
    main()
