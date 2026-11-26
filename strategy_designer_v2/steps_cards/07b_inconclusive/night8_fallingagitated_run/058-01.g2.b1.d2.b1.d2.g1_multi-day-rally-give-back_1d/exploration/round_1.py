import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allret = {h: [] for h in [1,2,3,5,7,10]}
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30).std()
            r3p = pd.Series(c) / pd.Series(c).shift(3) - 1
            z = r3p / (sd30 * np.sqrt(3))
            fc = b["forecast"].astype(float).values
            reg = b["regime"].astype(str).values
            ts = pd.to_datetime(b["timestamp"])
            for h in allret:
                for i in range(0, n - h, h):
                    allret[h].append((coin, c[i+h]/c[i]-1))
            for i in range(0, n - 3, 3):
                d = {"coin": coin, "win": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "fc": fc[i], "reg": reg[i], "z": z.iloc[i], "sd": sd30.iloc[i]}
                for h in [1,2,3,5,7,10]:
                    d["r%d" % h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    drift = {h: pd.DataFrame(allret[h], columns=["coin","r"]).groupby("coin")["r"].mean() for h in allret}
    for h in allret:
        df["u%d" % h] = -(df["r%d" % h] - df["coin"].map(drift[h]))
    cases = df[df["fc"] < 0].copy()
    def tday(s, sub):
        g = sub.groupby("day")[s].sum()
        x = sub[s].dropna()
        m = x.mean()
        dev = (sub[s] - m).groupby(sub["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev**2).sum() * D/(D-1)) / len(x) if D > 1 else np.nan
        return m, m/se if se else np.nan, len(x), D
    out = {}
    out["main u3"] = pd.Series(tday("u3", cases), index=["mean","t","n","days"])
    hz = pd.DataFrame({h: tday("u%d" % h, cases) for h in [1,2,3,5,7,10]}, index=["mean","t","n","days"]).T
    out["by horizon (cases)"] = hz
    out["by coin"] = cases.groupby("coin")["u3"].agg(["mean","count"])
    out["by window"] = cases.groupby("win")["u3"].agg(["mean","count"])
    out["by year"] = cases.groupby("year")["u3"].agg(["mean","count"])
    cases["q"] = pd.qcut(cases["fc"].abs().rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["by |fc| quartile"] = cases.groupby("q")[["u3","u5","z"]].mean().join(cases.groupby("q")["u3"].count().rename("n"))
    # outside profile: raw z>0 among non-in-profile bars
    other = df[(df["reg"] != "unknown") & (df["z"] > 0)].copy()
    other["zq"] = pd.qcut(other["z"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["outside profile z>0 by z quartile (u3 = short dir)"] = other.groupby("zq")[["u3","u5","z"]].mean().join(other.groupby("zq")["u3"].count().rename("n"))
    inp = df[(df["reg"] == "unknown") & (df["z"] > 0)].copy()
    inp["zq"] = pd.qcut(inp["z"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["in profile z>0 by raw z quartile"] = inp.groupby("zq")[["u1","u3","u5","u7","z"]].mean().join(inp.groupby("zq")["u3"].count().rename("n"))
    out["in profile z>0 total move (short) r3"] = pd.Series({"mean -r3": -inp["r3"].mean(), "n": len(inp), "share fc<0": (inp["fc"]<0).mean()})
    out["regime counts"] = df["reg"].value_counts()
    return out
