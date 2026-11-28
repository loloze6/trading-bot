"""Agreement of a model's sample answers with the operator-side reading (my own sides, written before the model's).
python3 runs/build_idea_sides/agreement.py sample_haiku.json"""
import json, sys
from pathlib import Path
d = Path(__file__).parent
m = json.loads((d / "sample_my_sides.json").read_text()); h = json.loads((d / sys.argv[1]).read_text())["ideas"]
ok = 0
for i, s in m.items():
    r = h.get(i, {})
    ok += r.get("side") == s
    if r.get("side") != s:
        print("DIFF", i, "mine", s, "model", r.get("side"), "|", r.get("sentence", "")[:110])
print(f"{sys.argv[1]}: agree {ok} of {len(m)}; answered {len(h)}; cost {sum(r['cost_usd'] for r in h.values()):.4f} USD")
