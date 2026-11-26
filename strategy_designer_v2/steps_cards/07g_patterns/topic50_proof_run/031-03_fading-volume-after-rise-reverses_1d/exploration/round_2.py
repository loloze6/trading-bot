import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].astype(float).values
            h_ = df["high"].astype(float).values; l_ = df["low"].astype(float).values
            n = len(c)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            sd = pd.Series(r).rolling(30, min_periods=15).std().shift(1).values
            sdl = pd.Series(r).rolling(120, min_periods=60).std().shift(1).values
            ts = pd.to_datetime(df["timestamp"])
            for t in range(1, n):
                z = r[t]/sd[t] if sd[t] > 0 else np.nan
                row = {"coin": coin, "w": w, "t": t, "z": z, "yr": ts.iloc[t].year,
                       "agit": (sd[t]/sdl[t]) if (sdl[t] and sdl[t] > 0) else np.nan,
                       "past20": c[t]/c[t-20]-1 if t >= 20 else np.nan,
                       "past60": c[t]/c[t-60]-1 if t >= 60 else np.nan,
                       "clv": (c[t]-l_[t])/(h_[t]-l_[t]) if h_[t] > l_[t] else np.nan}
                for k in [1, 2, 3, 5]:
                    row[f"f{k}"] = c[t+k]/c[t]-1 if t+k < n else np.nan
                rows.append(row)
    d = pd.DataFrame(rows)
    for k in [1, 2, 3, 5]:
        d[f"e{k}"] = d[f"f{k}"] - d.groupby("coin")[f"f{k}"].transform("mean")
    # graded: down-side z regression, next 1,2,3 days excess, non-overlapping via grid t%k==0
    res = []
    for k in [1, 2, 3, 5]:
        s = d[(d["t"] % k == 0) & (d["z"] < 0)].dropna(subset=["z", f"e{k}"])
        lr = stats.linregress(-s["z"], s[f"e{k}"])
        su = d[(d["t"] % k == 0) & (d["z"] > 0)].dropna(subset=["z", f"e{k}"])
        lu = stats.linregress(su["z"], su[f"e{k}"])
        res.append({"h": k, "down_n": len(s), "down_slope": lr.slope, "down_t": lr.slope/lr.stderr,
                    "up_n": len(su), "up_slope": lu.slope, "up_t": lu.slope/lu.stderr})
    out["graded: size of today's move vs next k days excess"] = pd.DataFrame(res).round(4)
    big = d[d["z"] <= -2].dropna(subset=["e1"])
    out["big down day: next-day excess by window"] = big.groupby("w")["e1"].agg(["mean", "count"]).round(4)
    out["big down day: by coin"] = big.groupby("coin")["e1"].agg(["mean", "count"]).round(4)
    out["big down day: by year"] = big.groupby("yr")["e1"].agg(["mean", "count"]).round(4)
    b2 = big.dropna(subset=["agit", "past60"]).copy()
    b2["agitated"] = b2["agit"] > 1
    b2["trend"] = pd.cut(b2["past60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    g = b2.groupby(["trend", "agitated"])["e1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["big down day: by profile"] = g.round(4)
    bc = big.dropna(subset=["clv"]).copy()
    bc["clvq"] = pd.cut(bc["clv"], [0, 0.2, 0.5, 1.01], include_lowest=True)
    out["big down day: by close location"] = bc.groupby("clvq")["e1"].agg(["mean", "count"]).round(4)
    # momentum 20d -> next 5d by window
    m = d[(d["t"] % 5 == 0)].dropna(subset=["past20", "e5"])
    mw = []
    for w, s in m.groupby("w"):
        lr = stats.linregress(s["past20"], s["e5"])
        mw.append({"w": w, "n": len(s), "slope": lr.slope, "t": lr.slope/lr.stderr})
    out["20d return -> next 5d excess, by window"] = pd.DataFrame(mw).round(3)
    mc = []
    for cn, s in m.groupby("coin"):
        lr = stats.linregress(s["past20"], s["e5"])
        mc.append({"coin": cn, "n": len(s), "slope": lr.slope, "t": lr.slope/lr.stderr})
    out["20d return -> next 5d excess, by coin"] = pd.DataFrame(mc).round(3)
    # cluster by day: big down days on same day
    big2 = big.copy()
    big2["day"] = big2["yr"].astype(str) + "_" + big2["w"] + "_" + big2["t"].astype(str)
    out["big down day: n distinct (w,t)"] = int(big.groupby(["w", "t"]).ngroups)
    return out
