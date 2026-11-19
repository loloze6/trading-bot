"""The bot's decision rule on simple forecast paths: position target = forecast / 10 (the volatility sizing left out:
it scales every position alike); the 0.2 band; the holding period after a trade (as built), or after a trade that
leaves a position (the variant); forced flats and a window's end are never held."""
import json, math, random
random.seed(7)

def run(fc, rule, N, forced=(), end=None):
    """free: today's book. hold: as built (after any trade, no trade for N bars). variant: the hold starts at a trade
    that leaves a position (not at a close to flat), and a forecast that confirms the held position (within the band)
    after the hold renews it."""
    pos, last, out, trades, units = 0.0, None, [], 0, 0.0
    for i, f in enumerate(fc):
        tgt = max(-20, min(20, f)) / 10
        if i in forced or (end is not None and i == end):
            if pos != 0: trades += 1; units += abs(pos); pos = 0.0
            last = None if rule == "variant" else i
            out.append(pos); continue
        held = rule != "free" and last is not None and i - last < N
        if not held:
            if abs(tgt - pos) >= 0.2 - 1e-12 or (tgt == 0 and pos != 0):
                trades += 1; units += abs(tgt - pos); pos = tgt
                last = i if (rule == "hold" or (rule == "variant" and pos != 0)) else None
            elif rule == "variant" and pos != 0 and tgt != 0 and (tgt > 0) == (pos > 0):
                last = i                       # the forecast confirms the held position: the hold is renewed
        out.append(round(pos, 3))
    return out, trades, round(units, 2)


L = 96
def spikes(at, size=12): return [size if i in at else 0 for i in range(L)]
S = []
def add(key, title, fc, N, note, forced=(), end=None):
    r = {k: run(fc, k, N, forced, end) for k in ("free", "hold", "variant")}
    S.append({"key": key, "title": title, "N": N, "forecast": [round(max(-20, min(20, x)), 2) for x in fc],
              "free": r["free"][0], "hold": r["hold"][0], "variant": r["variant"][0],
              "stats": {k: {"trades": v[1], "units": v[2]} for k, v in r.items()}, "note": note, "forced": list(forced)})

add("rise", "The forecast rises", [min(20, i * 20 / 60) for i in range(L)], 24, "")
add("fall", "The forecast falls to 0", [max(0, 16 - i * 16 / 70) for i in range(L)], 24, "")
add("cap", "At the cap (+20)", [min(26, 6 + i * 0.5) for i in range(L)], 24, "")
add("noise", "Back and forth around a level", [8 + 4 * math.sin(i * 1.3) + random.uniform(-2, 2) for i in range(L)], 24, "")
add("flip", "From positive to negative", [10 if i < 10 else -10 for i in range(L)], 24, "")
add("regime", "A regime switches the strategy off", [12 if i < 12 or i >= 60 else 0 for i in range(L)], 24, "")
add("moment", "A one-moment signal each day (horizon 24 h)", spikes({4, 28, 52, 76}), 24, "")
add("moment72", "One-moment signals, horizon 72 h", spikes({2, 26, 50, 74}), 72, "")
add("gap", "Closed at the end of a hold, then a new signal", [12 if i < 2 else (0 if i < 80 else 12) for i in range(L)] if False else spikes({0, 30}, 12), 24, "")
add("forced", "A forced flat (risk gate or large data gap) during a hold", [10] * L, 24, "", forced=(12,))
json.dump(S, open("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/holdviz/scenarios.json", "w"))
for s in S:
    print(f"{s['key']:9s} N={s['N']:2d} | " + " | ".join(f"{k}: {v['trades']} trades, {v['units']} units" for k, v in s["stats"].items()))
