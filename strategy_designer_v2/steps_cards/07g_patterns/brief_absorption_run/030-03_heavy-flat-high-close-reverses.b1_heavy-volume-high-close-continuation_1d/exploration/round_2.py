import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 2, 3, 5]
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            cl = (2*c - hi - lo) / rng
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            r1 = c.pct_change()
            vol20 = r1.shift(1).rolling(20, min_periods=20).std()
            z1 = r1 / vol20
            rngrel = (hi - lo) / c
            rngr = rngrel / rngrel.shift(1).rolling(20, min_periods=20).mean()
            ts = pd.to_datetime(b["timestamp"])
            wn = int(str(w).lstrip("w"))
            df = pd.DataFrame({"coin": coin, "win": w, "wn": wn, "pos": np.arange(len(b)),
                               "cl": cl, "vr": vr, "r1": r1, "z1": z1, "rngr": rngr,
                               "year": ts.dt.year, "wd": ts.dt.dayofweek})
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in H:
        g = d[d["pos"] % h == 0].dropna(subset=[f"f{h}"])
        drift = g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(drift)
        d[f"g{h}"] = d["pos"] % h == 0
    def stat(s, col):
        x = s[col].dropna()
        return pd.Series({"mean": x.mean(), "n": len(x), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    s = d[d["g1"]].dropna(subset=["u1", "cl", "vr", "z1"]).copy()
    vq = s["vr"].quantile(0.8)
    lowh = s[(s["vr"] > vq) & (s["cl"] < -0.5)]
    # grade by volume within low-close heavy days
    s["vrq"] = pd.qcut(s["vr"].rank(method="first"), 5, labels=False)
    s["clq"] = pd.qcut(s["cl"].rank(method="first"), 3, labels=False)
    t = s.groupby(["vrq", "clq"])["u1"].agg(["mean", "count"]).round(4)
    out["u1_by_vrq_clq"] = t.unstack()
    # z1 terciles x cl terciles, all days
    s["zq"] = pd.qcut(s["z1"].rank(method="first"), 5, labels=False)
    out["u1_by_zq_clq"] = s.groupby(["zq", "clq"])["u1"].mean().round(4).unstack()
    out["u1_by_zq_clq_n"] = s.groupby(["zq", "clq"])["u1"].count().unstack()
    # control: within z1 quintile 0 (big down days) split by volume heavy vs not
    dn = s[s["zq"] == 0]
    out["bigdown_by_heavy"] = dn.groupby(dn["vr"] > vq).apply(lambda x: stat(x, "u1")).round(4)
    out["bigdown_by_vrq"] = dn.groupby(pd.qcut(dn["vr"].rank(method="first"), 4, labels=False)).apply(lambda x: stat(x, "u1")).round(4)
    out["bigdown_by_clq"] = dn.groupby(pd.qcut(dn["cl"].rank(method="first"), 3, labels=False)).apply(lambda x: stat(x, "u1")).round(4)
    # horizons for low-close heavy
    hz = {}
    for h in H:
        sh = d[d[f"g{h}"]].dropna(subset=[f"u{h}", "cl", "vr"])
        sh = sh[(sh["vr"] > vq) & (sh["cl"] < -0.5)]
        hz[f"{h}d"] = stat(sh, f"u{h}")
    out["lowheavy_horizons"] = pd.DataFrame(hz).T.round(4)
    out["lowheavy_by_coin"] = lowh.groupby("coin").apply(lambda x: stat(x, "u1")).round(4)
    out["lowheavy_by_year"] = lowh.groupby("year").apply(lambda x: stat(x, "u1")).round(4)
    out["lowheavy_by_wd"] = lowh.groupby("wd").apply(lambda x: stat(x, "u1")).round(4)
    # regression u1 on z1, cl, cl*log(vr)
    x = s.copy(); x["lv"] = np.log(x["vr"]); x["clv"] = x["cl"] * x["lv"]
    X = np.column_stack([np.ones(len(x)), x["z1"].clip(-6, 6), x["cl"], x["lv"], x["clv"]])
    y = x["u1"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(y) - X.shape[1])
    out["reg_u1"] = pd.DataFrame({"beta": beta, "t": beta/np.sqrt(np.diag(cov))}, index=["const", "z1", "cl", "logvr", "cl_x_logvr"]).round(5)
    # range expansion 3d by sign of day
    s3 = d[d["g3"]].dropna(subset=["u3", "rngr", "r1"])
    big = s3[s3["rngr"] > s3["rngr"].quantile(0.8)]
    out["rngexp_3d_by_sign"] = big.groupby(big["r1"] > 0).apply(lambda x: stat(x, "u3")).round(4)
    # window halves stability for low-heavy
    out["lowheavy_by_winhalf"] = lowh.groupby(lowh["wn"] > 12).apply(lambda x: stat(x, "u1")).round(4)
    return out
