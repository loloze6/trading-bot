"""Exercise 3: the test plan in two closed-book calls instead of one.
Call 1 writes the plan in plain words (no reference documents). Call 2 turns that plan into a strategy config
(with the two trimmed references). Reuses the call and file helpers of ../../helper/make_test_plan.py.

  python run_split.py IDEA.md --briefs-dir DIR --out-dir DIR --plan-model M --config-model M [--plan-from DIR]
--plan-from reuses call 1's saved answer instead of calling again (so two config models share one plan).
This script reads no market data and runs no backtest.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "helper"))
from make_test_plan import call, header, write_atomic, DEFAULT_DATA  # noqa: E402

REF = HERE.parent.parent / "helper" / "reference"


def fields(text, keys):
    pat = "|".join(keys)
    return dict((k, " ".join(v.split())) for k, v in
                re.findall(rf"^({pat}):\s*(.*?)(?=^(?:{pat}):|\Z)", text.replace("**", ""), re.M | re.S))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path)
    a.add_argument("--briefs-dir", type=Path, required=True)
    a.add_argument("--out-dir", type=Path, required=True)
    a.add_argument("--plan-model", default="claude-opus-5-5")
    a.add_argument("--config-model", default="claude-opus-5-5")
    a.add_argument("--plan-from", type=Path)
    args = a.parse_args()

    idea_text, idea_id = args.idea.read_text(), args.idea.stem
    h, _ = header(idea_text)
    hf = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in h)}
    brief_text = (args.briefs_dir / f"{hf['brief']}.md").read_text()
    data = {k: hf.get(k, DEFAULT_DATA[k]) for k in DEFAULT_DATA}
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Call 1: the plan in words
    if args.plan_from:
        plan_text, c1 = (args.plan_from / f"{idea_id}_call1.txt").read_text(), 0.0
    else:
        req1 = (f"[DATA THE TEST RUNS ON]\ncoins: {data['instruments']}\nbar size: {data['bar']}\n\n"
                f"[IDEA]\n{idea_text}\n[BRIEF]\n{brief_text}\nWrite the test plan for this idea.")
        plan_text, c1 = call(args.plan_model, (HERE / "prompt_1_plan_in_words.md").read_text(), req1)
    write_atomic(args.out_dir / f"{idea_id}_call1.txt", plan_text)
    p = fields(plan_text, ["forecast", "confirm", "reject", "inconclusive", "deviation", "untestable"])
    head = ("---\n" + f"idea: {idea_id}\nbrief: {hf['brief']}\n"
            + "".join(f"data-{k}: {v}\n" for k, v in data.items()) + "---\n")
    if "untestable" in p and "forecast" not in p:
        write_atomic(args.out_dir / f"{idea_id}.md", head + f"Untestable (call 1): {p['untestable']}\n")
        print(f"untestable at call 1: {p['untestable'][:150]}")
        print(f"cost: call1 {c1:.4f} call2 0.0000 total {c1:.4f} USD")
        return

    # Call 2: the config
    req2 = (f"[TEST PLAN]\n{plan_text}\n\n[IDEA]\n{idea_text}\n"
            f"[STRATEGY CONFIG GUIDE]\n{(REF / 'strategy_config_guide.md').read_text()}\n"
            f"[COMPONENT CATALOGUE]\n{(REF / 'component_catalogue.md').read_text()}\n"
            f"Write the strategy config for this test plan.")
    cfg_text, c2 = call(args.config_model, (HERE / "prompt_2_config.md").read_text(), req2)
    write_atomic(args.out_dir / f"{idea_id}_call2.txt", cfg_text)
    clean = re.sub(r"```(?:json)?", "", cfg_text).replace("**", "")
    m = re.search(r"^config:\s*(\{.*\})\s*^differs:", clean, re.M | re.S)
    body = "".join(f"{k.capitalize()}: {p.get(k, 'not given')}\n" for k in ["forecast", "confirm", "reject", "inconclusive", "deviation"])
    if m:
        config = json.loads(m.group(1))
        write_atomic(args.out_dir / f"{idea_id}_config.json", json.dumps(config, indent=2) + "\n")
        d = fields(clean, ["differs"]).get("differs", "not given")
        write_atomic(args.out_dir / f"{idea_id}.md", head + f"Config: {idea_id}_config.json\n" + body + f"Config differs: {d}\n")
        print(f"plan and config: {args.out_dir / (idea_id + '.md')}")
    else:
        u = fields(clean, ["untestable"]).get("untestable", "no config and no untestable line")
        write_atomic(args.out_dir / f"{idea_id}.md", head + body + f"Untestable (call 2): {u}\n")
        print(f"untestable at call 2: {u[:150]}")
    print(f"cost: call1 {c1:.4f} call2 {c2:.4f} total {c1 + c2:.4f} USD")


if __name__ == "__main__":
    main()
