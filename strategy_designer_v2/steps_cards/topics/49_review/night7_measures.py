"""Night 7, measures M4 to M8 (the operator, 2026-11-25: "go for measures"; runs/NIGHT7_RUN.md). Both arms, the whole
night, from committed files only (the runs' branches `origin/night7-<name>`, `origin/night7c-<name>`; the P4 books' records
here) and the local daily closes. Reads `night7_ideas_full.csv` (one row per idea tested).

M4  Per profile named: ideas tested, step 5's verdicts, its number of cases and its t (positive = the idea's way). Tells
    whether a profile with no confirmed idea lacks the effect (many cases, t near 0) or the cases (few cases).
M5  Distinct effects among confirmed books, per profile: two books of one arm are one effect when their daily returns
    (the folds) correlate at 0.7 or more (about half of one explained by the other); groups by linking, across profiles.
M6  Profile specialists combined, against each alone, the old code's books and P4's 20, in-sample (the folds) and on the
    two unseen periods. The rule, fixed before any unseen number is read: the specialists are the confirmed, profitable
    enough books whose idea names a profile; the combination takes profiles that cannot hold on the same coin-day (a
    different trend word, or a different agitation word), those with the most books first; in each profile one book per
    distinct effect (M5), the highest step 6 Sharpe; equal capital per profile, split equally across its effects (P10's
    rule). Sharpe on daily returns (mean / sd x sqrt 365), yearly return, worst fall.
M7  Each unseen-tested specialist: the share of its coins' days inside its profile in each period, its days in a
    position and its Sharpe there. Tells whether a book failed on a period or had little of its profile to trade.
M8  A specialist's days in a position outside its profile: within the idea's horizon after its last day inside (the
    holding period, by design) or beyond it (a position left open: topic 51), and the median size of each.

Why this can't leak: it reads finished records after the fact; the profile of a day uses closes up to that day only.
  python3 topics/49_review/night7_measures.py      (writes night7_m4.csv ... night7_m8.csv beside it; its print: night7_measures.txt)"""
import functools, io, json, pathlib, subprocess, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]; REPO = STEPS.parents[1]
DATA = REPO / "trading-bot" / "local_data"; SC = "strategy_designer_v2/steps_cards"
PERIODS = ["backtests", "unseen_2016_2017", "unseen_2026"]
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_colwidth", 60)


def where(arm, theme):
    c = "c" if arm == "control" else ""
    return f"origin/night7{c}-{theme}", f"night7{c}_{theme}_run"


def show(ref, path, binary=False):
    out = subprocess.run(["git", "show", f"{ref}:{SC}/{path}"], cwd=REPO, capture_output=True).stdout
    return out if binary else out.decode()


def jshow(ref, path):
    t = show(ref, path)
    return json.loads(t) if t.strip() else {}


@functools.lru_cache(None)
def profile_of(coin):
    """The coin's market profile each day (common/market_profile.md), from its own daily closes."""
    d = pd.read_csv(DATA / f"kraken_{coin}_1d.csv", usecols=["timestamp", "close"])
    d["day"] = pd.to_datetime(d.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    c = d.drop_duplicates("day").set_index("day").close
    tr = (c / c.shift(60) - 1) * 100
    vol = (c.diff() / c).rolling(30).std()
    rk = vol.rolling(366).apply(lambda w: (w <= w[-1]).mean(), raw=True)
    t = np.where(tr > 10, "rising", np.where(tr < -10, "falling", "choppy"))
    a = np.where(rk > 0.5, "agitated", "calm")
    p = pd.Series([f"{x} {y}" for x, y in zip(t, a)], index=c.index)
    p[tr.isna() | rk.isna()] = None
    return p


def inside(profiles, named):
    return profiles.fillna("").apply(lambda p: bool(p) and all(w in p.split() for w in named.split()))


def chart(arm, theme, period, bt):
    ref, run = where(arm, theme)
    sub = "backtests" if period == "backtests" else f"{period}/backtests"
    raw = show(ref, f"04_backtest/{run}/{sub}/{bt}/chart_bars.csv.gz", binary=True)
    if not raw:
        return None
    b = pd.read_csv(io.BytesIO(raw), compression="gzip", usecols=["coin", "window", "timestamp", "position", "value"])
    b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    b["profile"] = None
    for coin, g in b.groupby("coin"):
        b.loc[g.index, "profile"] = g.day.map(profile_of(coin)).values
    return b


def daily(b):
    """The book's daily returns: per coin its value at each day's last bar, returns inside each window, mean of coins."""
    last = b.groupby(["window", "day", "coin"]).value.last().reset_index()
    last["w"] = last.window.str[1:].astype(int)
    r = last.pivot_table(index=["w", "day"], columns="coin", values="value").groupby(level="w").pct_change()
    return r.mean(axis=1).dropna().groupby(level="day").mean()


def local_daily(rec):
    b = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "value"])
    b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    return daily(b)


def stats(r):
    r = r.fillna(0.0)
    if len(r) < 20 or r.std() == 0:
        return {"sharpe": np.nan, "yearly": np.nan, "worst_fall": np.nan}
    c = (1 + r).cumprod()
    return {"sharpe": round(r.mean() / r.std() * np.sqrt(365), 2), "yearly": round(c.iloc[-1] ** (365 / len(r)) - 1, 3),
            "worst_fall": round(float((1 - c / c.cummax()).max()), 3)}


ideas = pd.read_csv(HERE / "night7_ideas_full.csv", dtype={"brief": str})
ideas["profile"] = ideas.profile.fillna("")
ideas["bt"] = ideas.idea + "_1d"
ideas["confirmed"] = ideas.step5.fillna("").str.startswith("confirmed")
ideas["profitable"] = ideas.step6.fillna("").str.startswith("profitable")

# ---------------- M4
rows = []
for r in ideas.itertuples():
    ref, run = where(r.arm, r.theme)
    v = jshow(ref, f"05_verification/{run}/verdicts/{r.bt}/result.json")
    rows.append({"arm": r.arm, "profile": r.profile or "-", "idea": r.idea, "status": v.get("status", r.step5),
                 "cases": (v.get("counts") or {}).get("cases"), "t": ((v.get("main_measure") or {}).get("statistic") or {}).get("value")})
m4 = pd.DataFrame(rows); m4.to_csv(HERE / "night7_m4.csv", index=False, float_format="%.4g")
s = str
m4["st"] = m4.status.astype(s)
print("M4  per profile named: verdicts, cases, t (positive = the idea's way)")
print(m4.groupby(["arm", "profile"]).apply(lambda g: pd.Series({
    "tested": len(g), "confirmed": g.st.str.startswith("confirmed").sum(), "inconclusive": g.st.str.startswith("inconclusive").sum(),
    "rejected": g.st.str.startswith("rejected").sum(), "not observable": g.st.str.startswith("not observable").sum(),
    "median cases": g.cases.median(), "median t": round(g.t.median(), 2), "t 1 to 2": ((g.t >= 1) & (g.t < 2)).sum()}),
    include_groups=False).to_string())

# ---------------- M5
conf = ideas[ideas.confirmed].copy()
cret_all = {}
for r in conf.itertuples():
    b = chart(r.arm, r.theme, "backtests", r.bt)
    if b is not None:
        cret_all[(r.arm, r.idea)] = daily(b)
SAME = 0.7          # a correlation of 0.7 is about half of one book's daily returns explained by the other
parent = {k: k for k in cret_all}


def find(k):
    while parent[k] != k:
        k = parent[k]
    return k


ks = list(cret_all)
for i, a in enumerate(ks):
    for b_ in ks[i + 1:]:
        if a[0] == b_[0]:
            c = pd.concat([cret_all[a], cret_all[b_]], axis=1, join="inner").corr().iloc[0, 1]
            if abs(c) >= SAME:
                parent[find(b_)] = find(a)
conf["effect"] = [find((a, i))[1] if (a, i) in parent else i for a, i in zip(conf.arm, conf.idea)]
conf[["arm", "theme", "idea", "profile", "profitable", "nearest_held", "effect"]].to_csv(HERE / "night7_m5.csv", index=False, float_format="%.4g")
print("\nM5  distinct effects among confirmed books, per profile (one effect = daily returns correlated at 0.7 or more)")
print(conf.assign(profile=conf.profile.replace("", "-")).groupby(["arm", "profile"]).agg(
    confirmed=("idea", "size"), effects=("effect", "nunique"),
    profitable_effects=("effect", lambda e: e[conf.loc[e.index, "profitable"]].nunique())).to_string())
for (a, p), g in conf.groupby(["arm", "profile"]):
    print(f"   {a:7} {p or '-':17} " + "; ".join(f"{e} ({n})" for e, n in g.effect.value_counts().items()))

# ---------------- M6
spec = ideas[ideas.confirmed & ideas.profitable & (ideas.profile != "") & (ideas.arm == "new")].merge(
    conf[["idea", "theme", "arm", "effect"]], on=["idea", "theme", "arm"])
spec["sharpe6"] = [next((m["value"] for m in jshow(where(r.arm, r.theme)[0], f"06_profitability/{where(r.arm, r.theme)[1]}/checks/{r.bt}/result.json").get("measures", [])
                         if m["measure"] == "sharpe_min"), np.nan) for r in spec.itertuples()]
ret = {}
for r in spec.itertuples():
    for per in PERIODS:
        b = chart(r.arm, r.theme, per, r.bt)
        if b is not None:
            ret[(r.idea, per)] = daily(b)


def disjoint(p, q):
    tp, tq = [w for w in p.split() if w in ("rising", "choppy", "falling")], [w for w in q.split() if w in ("rising", "choppy", "falling")]
    ap, aq = [w for w in p.split() if w in ("calm", "agitated")], [w for w in q.split() if w in ("calm", "agitated")]
    return bool(tp and tq and tp != tq) or bool(ap and aq and ap != aq)


order = spec.profile.value_counts().index.tolist()
chosen = []
for p in order:
    if all(disjoint(p, q) for q in chosen):
        chosen.append(p)
members = {}
for p in chosen:
    g = spec[spec.profile == p].sort_values("sharpe6", ascending=False).drop_duplicates("effect")
    for r in g.itertuples():
        members[r.idea] = 1 / len(chosen) / len(g)
print(f"\nM6  profiles combined (cannot hold on the same coin-day): {chosen}; books and weights: "
      + ", ".join(f"{k} {v:.2f}" for k, v in members.items()))

ctrl = ideas[(ideas.arm == "control") & ideas.confirmed & ideas.profitable]
cret = {}
for r in ctrl.itertuples():
    for per in PERIODS:
        b = chart(r.arm, r.theme, per, r.bt)
        if b is not None:
            cret[(r.idea, per)] = daily(b)
p4 = pd.read_csv(STEPS / "topics" / "44_review" / "p1_candidates_earning.csv"); p4 = p4[p4.status == "candidate"]
pret = {}
p1r = pd.read_csv(STEPS / "topics" / "44_review" / "p1_returns_earning.csv.gz", index_col=["w", "day"], parse_dates=["day"])
for col in p1r.columns:
    pret[(col.split("_")[0], "backtests")] = p1r[col].dropna().groupby(level="day").mean()
for r in p4.itertuples():
    for per in PERIODS[1:]:
        rec = STEPS / "04_backtest" / r.run / per / "backtests" / r.id
        if (rec / "chart_bars.csv.gz").exists():
            pret[(r.family, per)] = local_daily(rec)


def combo(series, weights=None):
    df = pd.concat(series, axis=1).fillna(0.0)
    w = np.ones(df.shape[1]) / df.shape[1] if weights is None else np.array(weights)
    return (df * w).sum(axis=1)


rows = []
for per in PERIODS:
    for p in sorted(spec.profile.unique()):
        g = spec[spec.profile == p].sort_values("sharpe6", ascending=False).drop_duplicates("effect")
        ss = [ret[(i, per)] for i in g.idea if (i, per) in ret]
        if ss:
            rows.append({"period": per, "what": f"profile '{p}' alone ({len(ss)} effects)", **stats(combo(ss))})
    ss = [ret[(i, per)] for i in members if (i, per) in ret]
    S = combo(ss, [members[i] for i in members if (i, per) in ret]) if ss else None
    if S is not None:
        rows.append({"period": per, "what": "S: the profiles combined", **stats(S)})
    cs = [cret[(i, per)] for i in ctrl.idea if (i, per) in cret]
    if cs:
        rows.append({"period": per, "what": f"old code: its {len(cs)} profitable confirmed books", **stats(combo(cs))})
    ps = [pret[(f, per)] for f in p4.family if (f, per) in pret]
    P = combo(ps)
    rows.append({"period": per, "what": f"P4: the {len(ps)} portfolio books", **stats(P)})
    if S is not None:
        rows.append({"period": per, "what": "P4 and S, equal capital per book", **stats(combo(ps + ss, [1 / (len(ps) + 1)] * len(ps) + [w / sum(members[i] for i in members if (i, per) in ret) / (len(ps) + 1) for w in [members[i] for i in members if (i, per) in ret]]))})
        rows.append({"period": per, "what": "correlation of S with P4", "sharpe": round(pd.concat([S, P], axis=1, join="inner").corr().iloc[0, 1], 2)})
m6 = pd.DataFrame(rows); m6.to_csv(HERE / "night7_m6.csv", index=False)
print(m6.to_string(index=False))

# ---------------- M7 and M8
r7, r8 = [], []
for r in ideas[ideas.confirmed & (ideas.profile != "")].itertuples():
    hz = jshow(where(r.arm, r.theme)[0], f"05_verification/{where(r.arm, r.theme)[1]}/verdicts/{r.bt}/size.json").get("horizon_bars", 5)
    for per in PERIODS:
        b = chart(r.arm, r.theme, per, r.bt)
        if b is None:
            continue
        b["in"] = inside(b.profile, r.profile).values
        b["held"] = b.position.abs() > 1e-9
        if r.profitable:
            r7.append({"idea": r.idea, "profile": r.profile, "period": per, "coin-days": len(b), "share in profile": round(b["in"].mean(), 2),
                       "days in a position": int(b.held.sum()), **stats(daily(b))})
        if per != "backtests":
            continue
        out_h = out_l = 0; size_h, size_l = [], []
        for (_, _), g in b.sort_values("timestamp").groupby(["coin", "window"]):
            last_in = -10 ** 9
            for i, (ins, held, pos) in enumerate(zip(g["in"].values, g.held.values, g.position.abs().values)):
                if ins:
                    last_in = i
                elif held:
                    if i - last_in <= hz:
                        out_h += 1; size_h.append(pos)
                    else:
                        out_l += 1; size_l.append(pos)
        n = int(b.held.sum())
        r8.append({"idea": r.idea, "profile": r.profile, "days in a position": n, "inside": round((b.held & b["in"]).sum() / n, 2),
                   "outside, holding period": round(out_h / n, 2), "outside, beyond it": round(out_l / n, 2),
                   "median size inside": round(b.position.abs()[b.held & b["in"]].median(), 3),
                   "median size beyond": round(np.median(size_l), 3) if size_l else np.nan})
m7 = pd.DataFrame(r7); m7.to_csv(HERE / "night7_m7.csv", index=False)
m8 = pd.DataFrame(r8); m8.to_csv(HERE / "night7_m8.csv", index=False)
print("\nM7  profitable specialists: their profile's share of coin-days and their result, per period")
print(m7.to_string(index=False))
print("\nM8  confirmed specialists: days in a position inside the profile, in the holding period after it, beyond it")
print(m8.to_string(index=False))
print(m8[["inside", "outside, holding period", "outside, beyond it"]].median().to_string())
