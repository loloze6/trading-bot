"""Mechanical checks on saved test plans, for the exercise readings (not a gate: the helper's own refusals are in
make_test_plan.py). For each plan: the config's hard rules, and markers of the criterion's required parts.
Judgement items (faithful to the idea, same side, settings) stay with the reader.

  python check_plans.py PLANS_DIR [PLANS_DIR ...]
"""
import json, re, sys
from pathlib import Path

ON_OFF = {"SmaTrendLongOnlyComponent", "GatedSmaTrendLongOnlyComponent", "FundingRateMeanReversionComponent",
          "FearGreedContrarianComponent", "MacdHistogramCrossoverComponent", "WhaleLargeTradeImbalanceComponent",
          "VolumeExpansionHedgeComponent"}
DEAD_ZONE = {"threshold_filter", "volume_filter"}


def config_faults(cfg):
    out = []
    rd = cfg.get("regime_detector", {})
    gated = bool(rd.get("rules") or rd.get("vetoes"))
    for name, reg in (cfg.get("strategies", {}).get("regimes") or {}).items():
        if not reg:
            continue
        for c in reg.get("components", []):
            cls = str(c.get("class", "")).split(".")[-1]
            ops = [t.get("op") for t in c.get("transforms", [])]
            if not ops or ops[0] != "standardise":
                out.append(f"{name}/{c.get('id')}: standardise is not the first transform")
            if cls in ON_OFF:
                out.append(f"{name}/{c.get('id')}: on/off class {cls} in strategies")
            if set(ops) & DEAD_ZONE or {t.get("op") for t in c.get("history_transforms", [])} & DEAD_ZONE:
                out.append(f"{name}/{c.get('id')}: dead-zone op in strategies")
            if cls == "BuyAndHoldStrategy" and gated:
                out.append(f"{name}/{c.get('id')}: a constant inside a gated regime")
            if "vol_target" in ops:
                out.append(f"{name}/{c.get('id')}: vol_target used")
    return out


def criterion_markers(text):
    t = text.lower()
    return {
        "horizon": bool(re.search(r"horizon|\b\d+[- ]bar", t)),
        "number": bool(re.search(r"t(-stat\w*)?\s*(≥|>=|≤|<=|of at least|of|at or (above|below)|below|above)\s*[-−+]?\d|p\s*[<≤]\s*0\.\d|percentage point|\d+(\.\d+)?\s*%", t)),
        "no_overlap": bool(re.search(r"overlap|every \d+(st|nd|rd|th)|one (bar|sample) (per|every)|\bapart\b|count(ed|s|ing)? (each \S+ (\S+ )?)?once|counted once|1-bar", t)),
        "supporting": "supporting" in t,
        "inconclusive": "inconclusive:" in t.replace("**", ""),
        "no_fading": "fading" not in t,
    }


def main():
    for d in sys.argv[1:]:
        for p in sorted(Path(d).glob("*.md")):
            if p.name in ("INDEX.md", "COMPONENT_WISHLIST.md", "REVIEW.md"):
                continue
            text = p.read_text()
            if "\nUntestable:" in text:   # plans written before the fidelity rule
                print(f"{p.name}: untestable")
                continue
            m = re.search(r"^outcome:\s*(\S+)", text, re.M)
            if m and m.group(1) != "plan":
                ok = "\nFidelity:" in text and "\nReason:" in text
                print(f"{p.name}: {m.group(1)} ({'fidelity and reason present' if ok else 'MISSING fidelity or reason'})")
                continue
            cfg_path = p.with_name(p.stem + "_config.json")
            faults = config_faults(json.loads(cfg_path.read_text())) if cfg_path.exists() else ["no config file"]
            missing = [k for k, v in criterion_markers(text).items() if not v]
            print(f"{p.name}: config {'ok' if not faults else faults}; criterion {'ok' if not missing else 'missing ' + str(missing)}")


if __name__ == "__main__":
    main()
