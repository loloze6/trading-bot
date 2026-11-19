import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 72
    rows = []
    hr_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < 3 * H:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            ts = pd.to_datetime(b["timestamp"])
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                                         "r_next": np.r_[r1[1:], np.nan]}))
            for t in range(H, n - H, H):
                past = r1[t - H + 1:t + 1]
                pr = c[t] / c[t - H] - 1
                fr = c[t + H] / c[t] - 1
                eff = abs(np.nansum(past)) / np.nansum(np.abs(past))
                maxshare = np.nanmax(np.abs(past)) / np.nansum(np.abs(past))
                vv = v[t - H + 1:t + 1]
                vconc = np.nanmax(vv) / np.nanmean(vv) if np.nanmean(vv) > 0 else np.nan
                vol = np.nanstd(past)
                pr24 = c[t] / c[t - 24] - 1
                rows.append(dict(coin=coin, w=w, pr=pr, fr=fr, eff=eff, maxshare=maxshare,
                                 vconc=vconc, vol=vol, pr24=pr24, fc=b["forecast"].iloc[t]))
    d = pd.DataFrame(rows)
    d["fr_x"] = d["fr"] - d.groupby("coin")["fr"].transform("mean")
    d["sign"] = np.sign(d["pr"])
    out = {}
    def tbl(col, q=5):
        g = d.copy()
        g["b"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = g.groupby("b")["fr_x"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a
    out["n"] = len(d)
    out["by_pr_quint"] = tbl("pr")
    out["by_vol_quint"] = tbl("vol")
    out["by_eff_quint"] = tbl("eff")
    out["by_maxshare_quint"] = tbl("maxshare")
    out["by_vconc_quint"] = tbl("vconc")
    # signed move x efficiency interaction: regress fr_x on pr_z, pr_z*eff_z
    rr = []
    for coin, g in d.groupby("coin"):
        g = g.dropna(subset=["pr", "eff", "fr_x", "vol"])
        z = (g["pr"] / g["vol"]).values
        e = (g["eff"] - g["eff"].mean()).values / g["eff"].std()
        X = np.c_[np.ones(len(g)), z, z * e]
        rr.append(pd.DataFrame({"y": g["fr_x"].values, "z": z, "ze": z * e, "e": e, "coin": coin}))
    R = pd.concat(rr)
    X = np.c_[np.ones(len(R)), R["z"], R["ze"], R["e"]]
    y = R["y"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg_z_ze_e"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "z", "z*eff", "eff"])
    # per coin signed slope
    pc = []
    for coin, g in R.groupby("coin"):
        sl = stats.linregress(g["z"], g["y"])
        pc.append((coin, sl.slope, sl.slope / sl.stderr, len(g)))
    out["per_coin_signed"] = pd.DataFrame(pc, columns=["coin", "slope", "t", "n"])
    hh = pd.concat(hr_rows).dropna()
    a = hh.groupby("hour")["r_next"].agg(["mean", "std", "count"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["by_hour"] = a[["mean", "t"]]
    a = hh.groupby("wd")["r_next"].agg(["mean", "std", "count"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["by_wd"] = a[["mean", "t"]]
    return out
