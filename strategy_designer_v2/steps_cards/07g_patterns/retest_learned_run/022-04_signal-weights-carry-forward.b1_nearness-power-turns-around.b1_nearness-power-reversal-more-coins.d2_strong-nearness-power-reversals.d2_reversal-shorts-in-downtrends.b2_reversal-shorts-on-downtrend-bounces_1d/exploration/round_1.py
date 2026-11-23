import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vol120 = r1.rolling(120, min_periods=60).std()
            hi90 = c.rolling(90, min_periods=30).max()
            near = c / hi90 - 1
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            idx = np.arange(0, len(df), 5)
            sub = pd.DataFrame({
                "coin": coin, "win": w, "r1": r1.values[idx], "r5": r5.values[idx],
                "r20": r20.values[idx], "r60": r60.values[idx],
                "volratio": (vol20 / vol120).values[idx], "vol20": vol20.values[idx],
                "near": near.values[idx], "f5": f5.values[idx],
                "fc": df["forecast"].values[idx], "wd": ts.dt.weekday.values[idx],
                "year": ts.dt.year.values[idx],
            })
            rows.append(sub)
    g = pd.concat(rows, ignore_index=True)
    g = g.dropna(subset=["f5"])
    drift = g.groupby("coin")["f5"].transform("mean")
    sd = g.groupby("coin")["f5"].transform("std")
    g["ex"] = g["f5"] - drift
    g["z"] = g["ex"] / sd
    out = {}
    def summ(df, by):
        a = df.groupby(by)["z"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["ex_mean_pct"] = df.groupby(by)["ex"].mean() * 100
        return a.drop(columns="std")
    gg = g.dropna(subset=["r20", "r5"]).copy()
    gg["gate"] = np.where((gg.r20 < 0) & (gg.r5 > 0), "bounce_in_down",
                  np.where((gg.r20 < 0) & (gg.r5 <= 0), "down_down",
                  np.where((gg.r20 >= 0) & (gg.r5 > 0), "up_up", "dip_in_up")))
    gg["active"] = gg.fc < 0
    out["by_gate_active"] = summ(gg, ["gate", "active"])
    gg["r5q"] = gg.groupby("coin")["r5"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_r5_quintile"] = summ(gg, "r5q")
    gg["r20q"] = gg.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_r20_quintile"] = summ(gg, "r20q")
    g1 = g.dropna(subset=["r1"]).copy()
    g1["r1q"] = g1.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_r1_quintile"] = summ(g1, "r1q")
    gv = g.dropna(subset=["volratio"]).copy()
    gv["vq"] = gv.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_volratio_quintile"] = summ(gv, "vq")
    gn = g.dropna(subset=["near"]).copy()
    gn["nq"] = gn.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_near90_quintile"] = summ(gn, "nq")
    g6 = g.dropna(subset=["r60"]).copy()
    g6["q"] = g6.groupby("coin")["r60"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["by_r60_quintile"] = summ(g6, "q")
    out["by_weekday"] = summ(g, "wd")
    act = gg[gg.active].copy()
    act["fq"] = pd.qcut(act.fc.rank(method="first"), 4, labels=False)
    out["active_by_fc_quartile(0=most_neg)"] = summ(act, "fq")
    out["active_by_year"] = summ(act, "year")
    # within bounce gate: r5 size
    b = gg[gg.gate == "bounce_in_down"].copy()
    b["q"] = pd.qcut(b.r5.rank(method="first"), 4, labels=False)
    out["bounce_by_r5_quartile"] = summ(b, "q")
    b["q2"] = pd.qcut(b.r20.rank(method="first"), 4, labels=False)
    out["bounce_by_r20_quartile"] = summ(b, "q2")
    out["n_total"] = len(g)
    return out
