def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f7": c.shift(-7) / c - 1,
                "r1": r1,
                "z1": r1 / r1.rolling(30, min_periods=10).std().shift(1),
                "vol_rel": r1.rolling(10, min_periods=5).std() / r1.rolling(60, min_periods=20).std(),
                "near_hi20": c / h.rolling(20, min_periods=10).max() - 1,
                "r10": c / c.shift(10) - 1,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def test(sub, ft, H):
        G = A[A["pos"] % H == 0].dropna(subset=["f%d" % H]).copy()
        st = G.groupby("coin")["f%d" % H].agg(["mean", "std"])
        G["exc"] = G["f%d" % H] - G["coin"].map(st["mean"])
        G["s"] = G["exc"] / G["coin"].map(st["std"])
        d = G[sub(G)].dropna(subset=[ft, "s"]).copy()
        d["rk"] = d.groupby("coin")[ft].rank(pct=True) - 0.5
        return d
    specs = [("down_volrel", lambda g: g["r1"] < 0, "vol_rel"),
             ("up_nearhi", lambda g: g["r1"] > 0, "near_hi20"),
             ("up_r10", lambda g: g["r1"] > 0, "r10"),
             ("up_volrel", lambda g: g["r1"] > 0, "vol_rel")]
    hz = []
    for nm, sub, ft in specs:
        for H in [1, 3, 7]:
            d = test(sub, ft, H)
            sl = stats.linregress(d["rk"], d["s"])
            q = pd.qcut(d["rk"], 5, labels=False)
            m = d.groupby(q)["exc"].mean()
            hz.append([nm, H, len(d), round(sl.slope / sl.stderr, 2), round(m.iloc[0] * 100, 3), round(m.iloc[-1] * 100, 3)])
    out["horizons_t_and_q1q5_exc_pct"] = pd.DataFrame(hz, columns=["spec", "H_days", "n", "t", "q1_exc%", "q5_exc%"])
    pcs, yrs = [], []
    for nm, sub, ft in specs[:2]:
        d = test(sub, ft, 3)
        for coin, x in d.groupby("coin"):
            sl = stats.linregress(x["rk"], x["s"]); pcs.append([nm, coin, len(x), round(sl.slope / sl.stderr, 2)])
        for y, x in d.groupby("yr"):
            sl = stats.linregress(x["rk"], x["s"]); yrs.append([nm, y, len(x), round(sl.slope / sl.stderr, 2)])
        # partial control: z1 and vol_rel together
        dd = d.dropna(subset=["z1"]).copy()
        dd["rz"] = dd.groupby("coin")["z1"].rank(pct=True) - 0.5
        X = np.column_stack([np.ones(len(dd)), dd["rk"], dd["rz"]]); y = dd["s"].values
        bet, res, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ bet; s2 = e @ e / (len(y) - 3); cov = s2 * np.linalg.inv(X.T @ X)
        out["%s_with_z1_control_t" % nm] = pd.Series({"t_feat": bet[1] / np.sqrt(cov[1, 1]), "t_z1": bet[2] / np.sqrt(cov[2, 2]), "n": len(dd)}).round(2)
    out["per_coin_t_H3"] = pd.DataFrame(pcs, columns=["spec", "coin", "n", "t"])
    out["per_year_t_H3"] = pd.DataFrame(yrs, columns=["spec", "yr", "n", "t"])
    return out
