import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    recs = {}
    for H in [72, 168, 336]:
        L = []
        for c, ws in bars.items():
            allr = []; tmp = []
            for w, df in ws.items():
                cl = df["close"].values
                s = pd.Series(cl)
                r30 = s.pct_change(720).values
                lr = np.log(s).diff()
                vol30 = (lr.rolling(720).std() * np.sqrt(720)).values
                hi30 = s.rolling(720).max().values
                idx = np.arange(0, len(cl) - H, H)
                fwd = cl[idx + H] / cl[idx] - 1
                allr.append(fwd)
                ts = pd.to_datetime(df["timestamp"].values[idx])
                tmp.append(pd.DataFrame({"r30": r30[idx], "z30": r30[idx] / vol30[idx],
                                         "dd": cl[idx] / hi30[idx] - 1, "fwd": fwd,
                                         "fc": df["forecast"].values[idx], "year": ts.year, "w": w}))
            allr = np.concatenate(allr); mu, sd = np.nanmean(allr), np.nanstd(allr)
            t = pd.concat(tmp); t["s"] = (t["fwd"] - mu) / sd; t["coin"] = c
            L.append(t)
        T = pd.concat(L).dropna(subset=["r30", "s", "z30"])
        T["zq"] = T.groupby("coin")["z30"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
        recs[H] = T
    rows = []
    for H, T in recs.items():
        g = T.groupby("zq")["s"].agg(["mean", "std", "count"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        for q, r in g.iterrows():
            rows.append({"H": H, "z30_decile": q, "strength": r["mean"], "n": r["count"], "t": r["t"]})
    out["strength_by_vol_scaled_r30_decile"] = pd.DataFrame(rows)
    T = recs[168]
    neg = T[T["r30"] < 0]
    res = []
    for H, TT in recs.items():
        n = TT[TT["r30"] < 0]
        sl = stats.linregress(n["z30"], n["s"])
        res.append({"H": H, "neg_slope_on_z30": sl.slope, "t": sl.slope / sl.stderr, "n": len(n)})
        p = TT[TT["r30"] > 0]
        sl = stats.linregress(p["z30"], p["s"])
        res.append({"H": H, "pos_slope_on_z30": sl.slope, "t": sl.slope / sl.stderr, "n": len(p)})
        sl = stats.linregress(TT["dd"], TT["s"])
        res.append({"H": H, "slope_on_drawdown_from_30d_high": sl.slope, "t": sl.slope / sl.stderr, "n": len(TT)})
    out["slopes"] = pd.DataFrame(res)
    # negative side by year: correlation of r30 with s (expect negative = deeper fall -> better)
    yr = []
    for y, g in neg.groupby("year"):
        if len(g) > 20:
            r, p = stats.spearmanr(g["z30"], g["s"])
            yr.append({"year": y, "rho_neg_side": r, "n": len(g)})
    out["neg_side_by_year"] = pd.DataFrame(yr)
    cc = []
    for c, g in neg.groupby("coin"):
        r, p = stats.spearmanr(g["z30"], g["s"]); cc.append({"coin": c, "rho_neg_side": r, "n": len(g)})
    out["neg_side_by_coin"] = pd.DataFrame(cc)
    # positive side: forecast deciles saturation
    pos = T[T["fc"] > 0].copy()
    pos["fq"] = pd.qcut(pos["fc"].rank(method="first"), 5, labels=False)
    g = pos.groupby("fq").agg(fc=("fc", "mean"), s=("s", "mean"), sd=("s", "std"), n=("s", "count"))
    g["t"] = g["s"] / (g["sd"] / np.sqrt(g["n"]))
    out["pos_forecast_quintile_168"] = g
    # hour 21-22 effect by year and coin
    Hh = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"])
            r = df["close"].pct_change()
            Hh.append(pd.DataFrame({"hour": ts.dt.hour, "year": ts.dt.year, "r": r, "coin": c}))
    Hh = pd.concat(Hh).dropna()
    e = Hh[Hh["hour"].isin([21, 22])]
    gy = e.groupby("year")["r"].agg(["mean", "std", "count"]); gy["t"] = gy["mean"] / (gy["std"] / np.sqrt(gy["count"]))
    gy["mean"] *= 1e4
    out["h21_22_by_year_bps"] = gy[["mean", "t", "count"]]
    gc = e.groupby("coin")["r"].agg(["mean", "std", "count"]); gc["t"] = gc["mean"] / (gc["std"] / np.sqrt(gc["count"]))
    gc["mean"] *= 1e4
    out["h21_22_by_coin_bps"] = gc[["mean", "t"]]
    # book: around largest losses/gains days
    D = []
    for c, ws in days.items():
        for w, df in ws.items():
            d = df.copy().reset_index(drop=True)
            d["next7_coin"] = d["close"].shift(-7) / d["close"] - 1
            d["next7_book"] = d["book_value"].shift(-7) / d["book_value"] - 1
            d["coin"] = c; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["bq"] = D.groupby("coin")["book_return"].transform(lambda x: pd.qcut(x.rank(method="first"), 20, labels=False))
    g = D[D["bq"].isin([0, 19])].groupby("bq")[["book_return", "coin_return", "next7_coin", "next7_book"]].mean()
    out["book_extreme_days_after"] = g
    return out
