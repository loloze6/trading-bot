import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            sd = pd.Series(r).rolling(30, min_periods=20).std().shift(1).values
            # up run before bar t
            runlen = np.zeros(n, int); rungain = np.zeros(n)
            for t in range(1, n):
                if r[t] < 0:
                    k = t-1; g = 1.0; L = 0
                    while k >= 1 and r[k] > 0 and L < 30:
                        g *= (1+r[k]); L += 1; k -= 1
                    runlen[t] = L; rungain[t] = g-1
            for t in range(n):
                d = {"coin": coin, "win": w, "pos": t, "regime": b["regime"].iloc[t],
                     "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                     "r0": r[t], "runlen": runlen[t], "runz": rungain[t]/sd[t] if sd[t] > 0 else np.nan,
                     "dipz": r[t]/sd[t] if sd[t] > 0 else np.nan}
                for h in (1, 3, 5, 10):
                    d[f"f{h}"] = c[t+h]/c[t]-1 if t+h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    # drift per coin over all windows, 3-bar grid
    drift = {}
    for h in (1, 3, 5, 10):
        g = df[df["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in (1, 3, 5, 10):
        df[f"u{h}"] = -(df[f"f{h}"] - df["coin"].map(drift[h]))  # short-direction unusual
    ev = df[(df["runlen"] > 0) & (df["r0"] < 0)].copy()
    ev["inprof"] = ev["regime"] != "chop"
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["regime counts"] = df["regime"].value_counts()
    out["events by profile, short unusual by horizon"] = pd.concat(
        {f"u{h}": ev.groupby("inprof").apply(lambda g: summ(g, f"u{h}")) for h in (1, 3, 5, 10)}, axis=1)
    ip = ev[ev["inprof"]].copy()
    ip["runq"] = pd.qcut(ip["runz"], 3, labels=["small", "mid", "large"])
    out["in-profile by run size tercile"] = pd.concat(
        {f"u{h}": ip.groupby("runq").apply(lambda g: summ(g, f"u{h}")) for h in (1, 3, 5, 10)}, axis=1)
    ip["lenq"] = ip["runlen"].clip(upper=4)
    out["in-profile by run length (4=4+)"] = pd.concat(
        {f"u{h}": ip.groupby("lenq").apply(lambda g: summ(g, f"u{h}")) for h in (3, 5, 10)}, axis=1)
    ip["dipq"] = pd.qcut(ip["dipz"], 3, labels=["deep", "mid", "shallow"])
    out["in-profile by dip-day size"] = pd.concat(
        {f"u{h}": ip.groupby("dipq").apply(lambda g: summ(g, f"u{h}")) for h in (1, 3, 5, 10)}, axis=1)
    out["in-profile by coin u3"] = ip.groupby("coin").apply(lambda g: summ(g, "u3"))
    out["in-profile by year u3"] = ip.groupby("year").apply(lambda g: summ(g, "u3"))
    # all in-profile days (non-chop) baseline
    allin = df[df["regime"] != "chop"]
    out["all in-profile days, short unusual"] = pd.DataFrame({f"u{h}": summ(allin[allin["pos"] % h == 0], f"u{h}") for h in (1, 3, 5, 10)})
    # in profile: after big up day (r0/sd) itself
    allin = allin.copy(); allin["rz"] = allin["r0"] / (allin["r0"].abs() / allin["dipz"].abs()).replace(0, np.nan)
    allin["runz_all"] = np.where(allin["r0"] < 0, allin["runz"], np.nan)
    sl = ip.dropna(subset=["runz", "u3"])
    res = stats.linregress(sl["runz"], sl["u3"])
    out["slope u3 on runz in-profile"] = pd.Series({"slope%": 100*res.slope, "t": res.slope/res.stderr, "n": len(sl)})
    return out
