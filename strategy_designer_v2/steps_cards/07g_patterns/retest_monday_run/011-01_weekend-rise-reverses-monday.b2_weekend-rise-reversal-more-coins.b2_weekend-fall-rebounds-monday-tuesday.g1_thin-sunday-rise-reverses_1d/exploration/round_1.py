import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        samp = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            samp += list(c[idx + 2] / c[idx] - 1)
        drift = np.mean(samp) if samp else 0.0
        for w, b in wins.items():
            d = pd.DataFrame()
            ts = pd.to_datetime(b["timestamp"], utc=True, errors="coerce")
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            cl = b["close"].astype(float).reset_index(drop=True)
            vo = b["volume"].astype(float).reset_index(drop=True)
            d["r1"] = cl / cl.shift(1) - 1
            d["r2p"] = cl / cl.shift(2) - 1
            d["mabs"] = d["r1"].abs().rolling(60, min_periods=20).mean()
            d["vr"] = vo.shift(1).rolling(60, min_periods=20).mean() / vo
            d["f1"] = cl.shift(-1) / cl - 1
            d["f2"] = cl.shift(-2) / cl - 1
            d["f2x"] = d["f2"] - drift
            d["coin"] = coin
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A.replace([np.inf, -np.inf], np.nan).dropna(subset=["r1", "f2x", "mabs", "vr"])
    A = A[A["mabs"] > 0]
    A["z"] = (A["r1"] / A["mabs"]).clip(-6, 6)
    A["rev"] = -np.sign(A["r1"]) * A["f2x"]

    def tt(x):
        x = pd.Series(x).dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    g = []
    for (wd, up), s in A.groupby(["wd", A["r1"] > 0]):
        r = tt(s["rev"]); r["wd"] = wd; r["up"] = int(up); g.append(r)
    out["reversal_by_weekday_and_side"] = pd.DataFrame(g)

    sl = []
    for wd, s in A.groupby("wd"):
        res = stats.linregress(s["z"], s["f2x"])
        sl.append({"wd": wd, "n": len(s), "slope": res.slope, "t": res.slope / res.stderr})
    out["slope_f2x_on_z_by_weekday"] = pd.DataFrame(sl)

    S = A[(A["wd"] == 6) & (A["r1"] > 0)].copy()
    S["vrq"] = pd.qcut(S["vr"], 3, labels=["thick", "mid", "thin"])
    S["zq"] = pd.qcut(S["z"], 3, labels=["small", "mid", "large"])
    out["sun_rise_by_volume_tercile"] = S.groupby("vrq", observed=True)["rev"].apply(tt).unstack().reset_index()
    out["sun_rise_by_size_tercile"] = S.groupby("zq", observed=True)["rev"].apply(tt).unstack().reset_index()
    out["sun_rise_by_year"] = S.groupby("year")["rev"].apply(tt).unstack().reset_index()
    out["sun_rise_monday_vs_tuesday"] = pd.Series({
        "monday_fall_mean": (-S["f1"]).mean(),
        "two_day_fall_mean": (-S["f2"]).mean(),
        "n": len(S)})

    F = A[(A["wd"] == 6) & (A["r1"] < 0)].copy()
    F["vrq"] = pd.qcut(F["vr"], 3, labels=["thick", "mid", "thin"])
    out["sun_fall_by_volume_tercile"] = F.groupby("vrq", observed=True)["rev"].apply(tt).unstack().reset_index()

    W = A[A["wd"] == 6].copy()
    W["zz"] = W["r2p"] / (W["mabs"] * np.sqrt(2))
    W["q"] = pd.qcut(W["zz"], 5, labels=False)
    out["sun_weekend_two_day_quintile"] = W.groupby("q").agg(
        n=("f2x", "size"), zz=("zz", "mean"), f2x=("f2x", "mean"),
        t=("f2x", lambda x: x.mean() / (x.std() / np.sqrt(len(x))))).reset_index()

    out["daily_return_by_weekday"] = A.groupby("wd")["r1"].apply(tt).unstack().reset_index()

    N = A[A["wd"] != 6].copy()
    N["vrq"] = pd.qcut(N["vr"], 3, labels=["thick", "mid", "thin"])
    out["non_sunday_reversal_by_volume_tercile"] = N.groupby("vrq", observed=True)["rev"].apply(tt).unstack().reset_index()

    try:
        bd = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                x = d[["day", "book_return", "coin_return"]].copy()
                x["wd"] = pd.to_datetime(x["day"], utc=True, errors="coerce").dt.weekday
                bd.append(x)
        B = pd.concat(bd, ignore_index=True).dropna(subset=["book_return"])
        out["book_return_by_weekday"] = B.groupby("wd")["book_return"].apply(tt).unstack().reset_index()
    except Exception as e:
        out["book_err"] = str(e)[:200]
    return out
