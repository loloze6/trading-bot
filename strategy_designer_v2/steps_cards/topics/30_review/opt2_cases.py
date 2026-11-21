"""Option 2, case by case: the position expected by the definition, against (a) the engine's block as built today
(events = moves of the sized target) and (b) the corrected rule (events = rises of the forecast on its side, sized at
their bar), with the band as coded (a trade passes when the forecast/10 moved >= 0.2 since the position was last set,
or the sized change >= 0.2). Optional: (c) = (b) with an event threshold (a rise counts only when it reaches the band,
2 forecast points, above the forecast's lowest level since its last event)."""
import collections, math

BAND = 0.2
def sim(fc, k=None, N=3, rule="today", forced=(), cap=2.0, zero_fix=False):
    k = k or [1.0] * len(fc)
    moves = collections.deque(maxlen=N); pt = pf = 0.0; trough = None
    pos = 0.0; held_sig = 0.0; out = []
    for t, f in enumerate(fc):
        nan = not math.isfinite(f)
        sig = 0.0 if nan else f / 10
        tgt = pos if nan else max(-cap, min(cap, f / 10 * k[t]))
        # --- the hold (engine block), three event rules
        if rule == "today":
            ev = tgt - pt; pt = tgt
        else:
            ev = 0.0
            if not nan:
                s = (f > 0) - (f < 0)
                if rule == "forecast":
                    base = max(0.0, s * pf) if s else 0.0
                else:   # threshold: from the lowest level on this side since the last event
                    if trough is None or s == 0 or (pf > 0) != (f > 0): trough = 0.0
                    base = max(0.0, trough)
                if s and s * f > base and (rule == "forecast" or s * f - base >= BAND * 10 - 1e-9):
                    ev = tgt * (s * f - base) / (s * f)
                    if rule == "threshold": trough = s * f
                elif rule == "threshold" and s:
                    trough = min(trough, s * f) if trough is not None else s * f
                pf = f
        moves.append(ev)
        prev = pos
        hl = sum(m for m in moves if m > 0); hs = sum(-m for m in moves if m < 0)
        if prev > 0 and tgt < prev and (hl > 0 or not zero_fix):
            tgt = max(tgt, min(prev, hl))
        elif prev < 0 and tgt > prev and (hs > 0 or not zero_fix):
            tgt = min(tgt, max(prev, -hs))
        if t in forced:
            tgt = 0.0
            if pos != 0: pos = 0.0; held_sig = 0.0
            out.append(round(pos, 3)); continue
        ch = tgt - prev
        if ch != 0 and (abs(sig - held_sig) >= BAND - 1e-6 or abs(ch) >= BAND - 1e-6) and not nan:
            pos = tgt; held_sig = sig
        out.append(round(pos, 3))
    return out

CASES = [  # (name, forecast, vol factor k or None, N, forced bars, expected by the definition, why)
 ("operator's example", [10, 5, 15, 0, 0, 0], None, 3, (), [1, 1, 1.5, 1, 1, 0],
  "the rise of 10 at bar 3 is held 3 bars (bars 3-5); the first 10 expires after bar 3"),
 ("short mirror", [-10, -5, -15, 0, 0, 0], None, 3, (), [-1, -1, -1.5, -1, -1, 0], "the same, short"),
 ("a one-moment signal", [0, 12, 0, 0, 0, 0], None, 3, (), [0, 1.2, 1.2, 1.2, 0, 0], "held 3 bars, then closed"),
 ("a fall within the horizon", [10, 10, 6, 6, 6], None, 3, (), [1, 1, 1, 0.6, 0.6],
  "the 10 is held to its third bar, then the position follows the forecast down to 0.6"),
 ("volatility alone rises then falls", [10, 10, 10, 10, 10, 10], [1, 1, 1.5, 1, 1, 1], 3, (), [1, 1, 1.5, 1, 1, 1],
  "the sizing moves the position (a sized change of 0.5 passes the band) but no bet is made: no hold"),
 ("an old short, then +20 while volatility drifts", [-10, 20, 20, 20, 20, 20, 20],
  [1, 1, .99, .98, .97, .96, .95], 3, (), [-1, -1, -1, 1.96, 1.96, 1.96, 1.96],
  "the short bet is held its 3 bars, then the long (a new bet at bar 2) is taken; a drifting long size is not a short bet; resizes of 0.02 are below the band"),
 ("a side switch", [10, 10, -10, -10, -10, -10], None, 3, (), [1, 1, 1, -1, -1, -1],
  "the long bet is held its 3 bars, then the short"),
 ("slow small rises, then 0", [10, 10.5, 11, 11.5, 0, 0], None, 3, (), [1, 1, 1, 1, 0, 0],
  "rises of 0.5 point are noise (the operator, 2026-11-20): no bet, nothing held; the first 10 has expired at bar 4"),
 ("a slow rise in steps of 2 points", [10, 12, 14, 0, 0, 0, 0], None, 3, (), [1, 1.2, 1.4, 0.4, 0.2, 0, 0],
  "each 2-point rise is a bet of 0.2, held 3 bars"),
 ("a forced flat during a hold", [10, 10, 10, 10, 10], None, 3, (2,), [1, 1, 0, 1, 1],
  "a forced flat is never held; the forecast still asks 1, so the book re-enters (no new bet: not held)"),
 ("a NaN forecast", [10, float("nan"), 0, 0, 0], None, 3, (), [1, 1, 1, 0, 0],
  "NaN: the position is kept, no bet; the 10 is held to its third bar"),
]

if __name__ == "__main__":
    for name, fc, k, N, forced, exp, why in CASES:
        print(f"\n{name}  (horizon {N}; {why})\n   forecast  {fc}\n   expected  {exp}")
        for rule, zf in (("today", False), ("forecast", False), ("threshold", False), ("threshold", True)):
            got = sim(fc, k, N, rule, forced, zero_fix=zf); rule = rule + ("+zero" if zf else "")
            ok = all(abs(a - b) < 0.011 for a, b in zip(got, exp))
            print(f"   {rule:15s} {got}  {'OK' if ok else 'DIFFERS'}")
