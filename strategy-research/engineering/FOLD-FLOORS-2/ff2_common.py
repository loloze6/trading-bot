"""FOLD-FLOORS-2: shared pieces of the three measurement scripts (measurement only).

Nothing here reads market data or writes a file. `load_tools(path)` puts the given
strategy-research/tools directory first on sys.path and imports claim_tests, claim_measure
and fold_confirm FROM THERE. Every script of this folder takes --tools and is run with
--tools <worktree of PR #496>/strategy-research/tools, so "pass" means
fold_confirm.grade_test(result, fold_windows=<the fold's window labels>) == confirmed
under R5 (the claim's floor first, then all but one of the FOLD's windows, a window with
no value counting against). The claim_tests / claim_measure blocks are taken unchanged
from that same tools path.

Cell A of FOLD-FLOORS-2026-10-19 (PR #495): selector past_return(5) >= +5% (event),
outcome fwd_return at h = 3, mean_diff against the complement, floor min_events 100 /
min_windows 4, both directions. `cell_a_fold` evaluates one fold of windows under:
  R5          the tool's measurement, graded by R5's grade_test;
  rem1a       remedy 1 (one value per non-overlapping stretch), selected side only:
              the selected bars are thinned greedily in time order -- a selected bar is
              kept only if it is at least bars + h = 8 bars after the last KEPT selected
              bar of the window -- and mean_diff is taken over the kept bars against the
              tool's complement (every valid unselected bar). The next kept bar's
              selection then reads returns that start after the previous kept bar's
              outcome window, so a kept bar's outcome cannot lengthen or shorten the
              run of kept bars after it;
  rem1b       remedy 1 on both sides: the complement bars are thinned by the same greedy
              rule (spacing 8 among complement bars);
              for rem1a / rem1b the claim's floor is checked on the UNTHINNED counts
              (claim_measure's n_events, as R5 reads it): the remedy changes the value
              compared, not the claim's floor; the thinned counts are reported;
  rem2_pooled remedy 2 (a simulated null per selector): R5 confirmed AND the fold's
              pooled oriented value is above the 95th percentile of the pooled oriented
              value of the same selector, direction and layout on no-edge reference
              paths drawn with an independent seed;
  rem2_share  remedy 2 on the per-window share: R5 confirmed AND k / n_fold (the fold's
              windows with the claimed sign) is STRICTLY above the 95th percentile of
              that share on the reference paths (k is discrete: when the reference 95th
              percentile is 6/6 this rule can never pass; the percentile is reported).
"""
from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path

import numpy as np

FLOOR = {"min_events": 100, "min_windows": 4}
BARS, H, CUT = 5, 3, 0.05
SPACING = BARS + H


def load_tools(tools: Path):
    tools = Path(tools).resolve()
    if not (tools / "fold_confirm.py").exists():
        raise SystemExit(f"--tools {tools}: no fold_confirm.py there")
    sys.path.insert(0, str(tools))
    for m in ("claim_tests", "claim_measure", "fold_confirm", "claim_card"):
        sys.modules.pop(m, None)
    ct = importlib.import_module("claim_tests")
    cmeas = importlib.import_module("claim_measure")
    fcf = importlib.import_module("fold_confirm")
    for mod in (ct, cmeas, fcf):
        if Path(mod.__file__).resolve().parent != tools:
            raise SystemExit(f"{mod.__name__} imported from {mod.__file__}, not from {tools}")
    import inspect
    if "fold_windows" not in inspect.signature(fcf.grade_test).parameters:
        raise SystemExit(f"{tools}/fold_confirm.py: grade_test has no fold_windows (not R5)")
    return ct, cmeas, fcf


def rate(x, n):
    p = x / n if n else None
    return {"rate": None if p is None else round(p, 4), "count": int(x), "n": int(n),
            "se": None if p is None else round(math.sqrt(p * (1 - p) / n), 4)}


def ms(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return {"mean": None, "se": None, "n": int(len(x))}
    return {"mean": round(float(x.mean()), 6), "se": round(float(x.std(ddof=1) / math.sqrt(len(x))), 6),
            "n": int(len(x))}


def selector():
    return {"kind": "event", "field": "past_return", "bars": BARS, "op": ">=", "value": CUT}


def cell_a_test(direction):
    return {"name": "cell_a", "selector": selector(),
            "outcome": {"kind": "fwd_return", "horizons": [H]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff",
            "direction": direction, "floor": dict(FLOOR)}


def thin(mask, spacing=SPACING):
    """Greedy, in time order: keep a True bar only if it is >= spacing rows after the last
    kept one."""
    out = np.zeros(len(mask), dtype=bool)
    last = -10 ** 9
    for t in np.nonzero(mask)[0]:
        if t - last >= spacing:
            out[t] = True
            last = t
    return out


def _result(ct, cmeas, per, d, key_mask, key_wref, raw_counts):
    """A claim_measure-shaped result for one horizon from prepared per-window arrays."""
    stat = ct.STATISTICS["mean_diff"]
    pw = {}
    for p in per:
        y, m, wr = p["y"], p[key_mask], p[key_wref]
        o = stat(y, m, wr, np.full(len(y), np.nan), d)[1]
        pw[p["label"]] = {"oriented": None if not np.isfinite(o) else float(o),
                          "n_events": int((m & np.isfinite(y)).sum())}
    y = np.concatenate([p["y"] for p in per])
    m = np.concatenate([p[key_mask] for p in per])
    wr = np.concatenate([p[key_wref] for p in per])
    raw, o = stat(y, m, wr, np.full(len(y), np.nan), d)
    n_ev, n_win = raw_counts
    floor_not_met = []
    if n_ev < FLOOR["min_events"]:
        floor_not_met.append(f"min_events={FLOOR['min_events']} at h={H} (have {n_ev})")
    if n_win < FLOOR["min_windows"]:
        floor_not_met.append(f"min_windows={FLOOR['min_windows']} at h={H} (have {n_win})")
    status = cmeas.NO_EVENTS if n_ev == 0 else cmeas.MEASURED
    return {"status": status, "floor_not_met": floor_not_met,
            "horizons": {H: {"value": None if not np.isfinite(raw) else float(raw),
                             "oriented": None if not np.isfinite(o) else float(o),
                             "n_events": int(n_ev), "n_windows_with_events": int(n_win),
                             "per_window": pw}}}


def prepare(ct, windows, edge=0.0, direction="less", outcome_windows=None):
    """Per-window arrays of cell A. `edge`: a real effect of the claimed sign added to the
    selected bars' outcome (as #495 plants it). `outcome_windows`: an independent second
    path per window for the outcome (#495's shadow cells); None = the tool's outcome."""
    per = []
    ow = outcome_windows or windows
    sgn = 1.0 if direction == "greater" else -1.0
    for w, wo in zip(windows, ow):
        mask, valid = ct.SELECTORS["event"](w, selector())
        mask = mask & valid
        y = ct.out_fwd_return(wo, H)
        if edge:
            y = y + np.where(mask, sgn * edge, 0.0)
        comp = valid & ~mask
        m1 = thin(mask)
        per.append({"label": w.label, "y": y, "mask": mask, "wref": comp.astype(float),
                    "mask1": m1, "wref1b": thin(comp).astype(float)})
    return per


def cell_a_fold(ct, cmeas, fcf, windows, direction, fold_labels, edge=0.0, outcome_windows=None,
                check=False):
    """{rule: {"confirmed", "k", "pooled"}} for one fold (windows = the fold's windows,
    labels "<sym>/<label>"). check=True: the R5 path is re-run through the full chain
    claim_measure.measure_test -> fold_confirm.grade_test and must agree exactly."""
    per = prepare(ct, windows, edge, direction, outcome_windows)
    n_ev = sum(int((p["mask"] & np.isfinite(p["y"])).sum()) for p in per)
    n_win = sum(1 for p in per if (p["mask"] & np.isfinite(p["y"])).any())
    out = {}
    thinned = {}
    for rule, km, kw in (("R5", "mask", "wref"), ("rem1a", "mask1", "wref"),
                         ("rem1b", "mask1", "wref1b")):
        res = _result(ct, cmeas, per, direction, km, kw, (n_ev, n_win))
        g = fcf.grade_test(res, fold_windows=fold_labels)
        hz = res["horizons"][H]
        k = sum(1 for c in hz["per_window"].values() if c["oriented"] is not None and c["oriented"] > 0)
        out[rule] = {"confirmed": g["status"] == fcf.CONFIRMED, "status": g["status"], "k": k,
                     "pooled": hz["oriented"],
                     "per_window": [hz["per_window"][p["label"]]["oriented"] for p in per]}
        thinned[rule] = sum(int((p[km] & np.isfinite(p["y"])).sum()) for p in per)
        if check and rule == "R5" and outcome_windows is None and not edge:
            real = cmeas.measure_test(windows, cell_a_test(direction), None)
            g2 = fcf.grade_test(real, fold_windows=fold_labels)
            assert g2["status"] == g["status"], (g2, g)
            a = real["horizons"][H]
            assert a["n_events"] == n_ev and a["n_windows_with_events"] == n_win
            assert list(real.get("floor_not_met") or []) == res["floor_not_met"]
            for lab, cell in a["per_window"].items():
                x, z = cell["oriented"], hz["per_window"][lab]["oriented"]
                assert (x is None and z is None) or abs(x - z) < 1e-12, (lab, x, z)
            x, z = a["oriented"], hz["oriented"]
            assert (x is None and z is None) or abs(x - z) < 1e-12
    out["_events"] = {"selected": n_ev, "selected_thinned": thinned["rem1a"],
                      "complement_thinned": sum(int(((p["wref1b"] > 0) & np.isfinite(p["y"])).sum())
                                                for p in per)}
    return out


def q95(x):
    x = np.asarray([v for v in x if v is not None and np.isfinite(v)], dtype=float)
    return float(np.quantile(x, 0.95)) if len(x) else None


class Tally:
    """Confirm counts per rule (R5, rem1a, rem1b, rem2_pooled, rem2_share) and the per-window
    share with the claimed sign (R5's per-window values)."""
    RULES = ("R5", "rem1a", "rem1b", "rem2_pooled", "rem2_share")

    def __init__(self, n_fold, ref=None):
        self.n_fold = n_fold
        self.ref = ref                       # {"pooled_q95": x, "share_q95": s} or None
        self.conf = {r: 0 for r in self.RULES}
        self.sims = 0
        self.win_pos = self.win_tot = 0
        self.pooled, self.share = [], []
        self.ev, self.ev_thin, self.comp_thin = [], [], []
        self.status = {}

    def add(self, r):
        self.sims += 1
        for rule in ("R5", "rem1a", "rem1b"):
            self.conf[rule] += int(r[rule]["confirmed"])
        self.status[r["R5"]["status"]] = self.status.get(r["R5"]["status"], 0) + 1
        vals = [v for v in r["R5"]["per_window"] if v is not None]
        self.win_tot += len(vals)
        self.win_pos += sum(1 for v in vals if v > 0)
        self.pooled.append(r["R5"]["pooled"] if r["R5"]["pooled"] is not None else np.nan)
        sh = r["R5"]["k"] / self.n_fold
        self.share.append(sh)
        if self.ref is not None:
            p = r["R5"]["pooled"]
            self.conf["rem2_pooled"] += int(r["R5"]["confirmed"] and p is not None
                                            and p > self.ref["pooled_q95"])
            self.conf["rem2_share"] += int(r["R5"]["confirmed"] and sh > self.ref["share_q95"] + 1e-12)
        self.ev.append(r["_events"]["selected"])
        self.ev_thin.append(r["_events"]["selected_thinned"])
        self.comp_thin.append(r["_events"]["complement_thinned"])

    def summary(self):
        out = {"sims": self.sims,
               "per_window_claimed_sign": rate(self.win_pos, self.win_tot),
               "confirm": {r: (rate(v, self.sims) if (r in ("R5", "rem1a", "rem1b") or self.ref)
                               else None) for r, v in self.conf.items()},
               "r5_status": dict(sorted(self.status.items())),
               "pooled_oriented": ms(self.pooled),
               "selected_events_per_fold": round(float(np.mean(self.ev)), 1),
               "selected_thinned_per_fold": round(float(np.mean(self.ev_thin)), 1),
               "complement_thinned_per_fold": round(float(np.mean(self.comp_thin)), 1)}
        if self.ref is not None:
            out["remedy2_reference"] = dict(self.ref)
        return out

    def reference(self):
        """This tally as a remedy-2 reference null: the 95th percentiles."""
        return {"pooled_q95": q95(self.pooled), "share_q95": q95(self.share), "ref_sims": self.sims}
