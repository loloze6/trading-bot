import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r1": r1,
                "z1": r1 / r1.rolling(30, min_periods=15).std().shift(1),
                "vol30": r1.rolling(30, min_periods=15).std(),
                "vol7": r1.rolling(7, min_periods=5).std(),
                "wd": ts.dt.weekday, "year": ts.dt.year,
            })
            df["vratio"] = df["vol7"] / df["vol30"]
            for h in (1, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (1, 10):
        g = A[A["pos"] % h == 0]
        d = g.groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(d)
        A[f"g{h}"] = (A["pos"] % h == 0)
    A["volrank"] = A.groupby("coin")["vol30"].rank(pct=True)
    def tt(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan, "n": len(s)})
    # weekday stability: Thu+Fri minus Mon+Wed, by year and by coin
    g = A.dropna(subset=["u1"]).copy()
    g["wdgrp"] = np.where(g["wd"].isin([3,4]), 1, np.where(g["wd"].isin([0,2]), -1, 0))
    g2 = g[g["wdgrp"] != 0].copy(); g2["s"] = g2["u1"]*g2["wdgrp"]
    out["wd_signed_by_year"] = g2.groupby("year")["s"].apply(tt).unstack()
    out["wd_signed_by_coin"] = g2.groupby("coin")["s"].apply(tt).unstack()
    out["wd_by_coin_mean"] = g.groupby(["coin","wd"])["u1"].mean().unstack()
    # fc slope by vol tercile, and continuous interaction
    G = A[A["g10"]].dropna(subset=["fc","u10","volrank"]).copy()
    G["vt"] = pd.cut(G["volrank"], [0,1/3,2/3,1], labels=False, include_lowest=True)
    vi = {}
    for k, gg in G.groupby("vt"):
        s = stats.linregress(gg["fc"], gg["u10"])
        sg = gg["u10"]*np.sign(gg["fc"]); sg = sg/gg["vol30"]/np.sqrt(10)
        vi[k] = {"slope": s.slope, "t": s.slope/s.stderr, "n": len(gg),
                 "signed_u10": (gg["u10"]*np.sign(gg["fc"])).mean(), "strength": sg.mean(),
                 "vol30": gg["vol30"].mean()}
    out["fc_by_vol_tercile"] = pd.DataFrame(vi).T
    G["fcxv"] = G["fc"]*(G["volrank"]-0.5)
    X = np.column_stack([np.ones(len(G)), G["fc"], G["volrank"]-0.5, G["fcxv"]]); y = G["u10"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X@beta
    se = np.sqrt(np.diag(e@e/(len(y)-4)*np.linalg.inv(X.T@X)))
    out["interaction"] = pd.DataFrame({"b": beta, "t": beta/se}, index=["c","fc","vol","fcxvol"])
    # fc slope by window half (stability)
    G["half"] = (G["wn"] > 12).astype(int)
    hh = {}
    for k, gg in G.groupby("half"):
        s = stats.linregress(gg["fc"], gg["u10"]); hh[k] = {"slope": s.slope, "t": s.slope/s.stderr, "n": len(gg)}
    out["fc_by_halves"] = pd.DataFrame(hh).T
    # abs z1 (big day either way) vs u10, and vol-ratio vs u10
    G2 = A[A["g10"]].dropna(subset=["z1","u10","vratio"]).copy()
    G2["az"] = G2["z1"].abs()
    G2["q"] = G2.groupby("coin")["az"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["absz_q_u10"] = G2.groupby("q")["u10"].apply(tt).unstack()
    G2["q2"] = G2.groupby("coin")["vratio"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["vratio_q_u10"] = G2.groupby("q2")["u10"].apply(tt).unstack()
    # book: daily, around largest losses
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    B = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    B = B.dropna()
    B["bq"] = pd.qcut(B["book_return"].rank(method="first"), 10, labels=False)
    out["book_decile_vs_coin"] = B.groupby("bq")[["book_return","coin_return"]].mean()
    # book by window, long vs short share
    A["long"] = (A["alloc"]>0).astype(float); A["short"]=(A["alloc"]<0).astype(float)
    A["gain"] = A["alloc"]*A["f1"]
    out["gain_by_side"] = pd.DataFrame({
        "long_gain": [A.loc[A["alloc"]>0,"gain"].mean()], "short_gain": [A.loc[A["alloc"]<0,"gain"].mean()],
        "long_share":[A["long"].mean()], "short_share":[A["short"].mean()],
        "abs_alloc":[A["alloc"].abs().mean()]})
    return out
