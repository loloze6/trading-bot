import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(180, min_periods=180).mean()
            dist = c / sma - 1
            vol360 = r1.rolling(360, min_periods=120).std()
            p18 = c / c.shift(18) - 1
            p6 = c / c.shift(6) - 1
            vr = np.log(v.rolling(6).mean() / v.rolling(36).mean())
            vr18 = np.log(v.rolling(18).mean() / v.rolling(108).mean())
            vrel = np.log(r1.rolling(36).std() / vol360)
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values, "fwd6": fwd6.iloc[idx].values,
                "dist": dist.iloc[idx].values,
                "pz18": (p18 / (vol360 * np.sqrt(18))).iloc[idx].values,
                "pz6": (p6 / (vol360 * np.sqrt(6))).iloc[idx].values,
                "vr": vr.iloc[idx].values, "vr18": vr18.iloc[idx].values,
                "vrel": vrel.iloc[idx].values,
                "usual": (vol360 * np.sqrt(18)).iloc[idx].values,
                "year": pd.to_datetime(b["timestamp"]).dt.year.iloc[idx].values,
            })
            rows.append(d)
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["exz"] = g["ex"] / g["usual"]
    out = {}
    def reg(df, xs, y="exz"):
        s = df.dropna(subset=xs + [y])
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xs])
        beta, *_ = np.linalg.lstsq(X, s[y].values, rcond=None)
        res = s[y].values - X @ beta
        sig2 = res @ res / (len(s) - X.shape[1])
        se = np.sqrt(np.diag(sig2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + xs).assign(n=len(s))
    out["single_vr"] = reg(g, ["vr"])
    out["single_vrel"] = reg(g, ["vrel"])
    out["single_pz6"] = reg(g, ["pz6"])
    out["joint"] = reg(g, ["dist", "pz18", "pz6", "vr", "vrel"])
    g["sgn18"] = np.sign(g["pz18"])
    g["vr_signed"] = g["vr"] * g["sgn18"]
    g["vrel_signed"] = g["vrel"] * g["sgn18"]
    out["signed_terms"] = reg(g, ["vr", "vr_signed", "vrel", "vrel_signed"])
    # vr by up/down past moves
    res = {}
    for k, ss in g.groupby("sgn18"):
        r = reg(ss, ["vr"]); res[str(k)] = [r.loc["vr", "beta"], r.loc["vr", "t"], len(ss)]
    out["vr_by_past_sign"] = pd.DataFrame(res, index=["beta", "t", "n"]).T
    # stability by coin and by year of vr and vrel
    bc = {}
    for k, ss in g.groupby("coin"):
        a = reg(ss, ["vr"]).loc["vr", "t"]; b2 = reg(ss, ["vrel"]).loc["vrel", "t"]; c2 = reg(ss, ["pz6"]).loc["pz6", "t"]
        bc[k] = [a, b2, c2]
    out["by_coin_t"] = pd.DataFrame(bc, index=["vr_t", "vrel_t", "pz6_t"]).T
    by = {}
    for k, ss in g.groupby("year"):
        by[k] = [reg(ss, ["vr"]).loc["vr", "t"], reg(ss, ["vrel"]).loc["vrel", "t"], len(ss)]
    out["by_year_t"] = pd.DataFrame(by, index=["vr_t", "vrel_t", "n"]).T
    # vr quintiles, raw excess and strength
    s = g.dropna(subset=["vr"]).copy()
    s["q"] = s.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["q_vr_strength"] = s.groupby("q").agg(ex=("ex", "mean"), exz=("exz", "mean"), n=("ex", "count"), pz18=("pz18", "mean"))
    s = g.dropna(subset=["vr18"]).copy()
    out["single_vr18"] = reg(s, ["vr18"])
    return out
