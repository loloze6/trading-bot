"""How expensive is a halt? Pairs each HALT with the next RESUME/STAGE line in
campaign_log.md and reports wall-clock downtime. Falsification test: if halts
are cheap, halt frequency is not the throughput constraint."""
import re, sys
from datetime import datetime
from pathlib import Path
p = Path(sys.argv[1] if len(sys.argv)>1 else "strategy-research/campaign_record/campaign_log.md")
TS = re.compile(r"^- (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z (.*)$")
ev = []
for line in p.read_text(encoding="utf-8").splitlines():
    m = TS.match(line)
    if not m: continue
    if "[DRY RUN]" in line: continue
    ev.append((datetime.fromisoformat(m.group(1)), m.group(2)))
halts = []
for i, (t, txt) in enumerate(ev):
    if not txt.startswith("HALT"):
        continue
    reason = re.sub(r"^HALT [—-] ", "", txt).split(":")[0].split(".")[0].strip()[:32]
    nxt = next((ev[j] for j in range(i+1, len(ev))), None)
    halts.append((t, reason, (nxt[0]-t).total_seconds()/3600 if nxt else None))
print(f"halts: {len(halts)}\n")
print(f"{'when':20s} {'reason':34s} downtime_hours")
tot = 0.0
for t, r, h in halts:
    print(f"{t.isoformat():20s} {r:34s} {'n/a' if h is None else f'{h:8.2f}'}")
    if h: tot += h
print(f"\ntotal recorded downtime : {tot:.1f} h  ({tot/24:.1f} days)")
known = [h for _,_,h in halts if h]
print(f"median halt downtime    : {sorted(known)[len(known)//2]:.2f} h")
span = (ev[-1][0]-ev[0][0]).total_seconds()/3600
print(f"campaign wall-clock span: {span:.1f} h  ({span/24:.1f} days)")
print(f"share of span halted    : {100*tot/span:.1f}%")
