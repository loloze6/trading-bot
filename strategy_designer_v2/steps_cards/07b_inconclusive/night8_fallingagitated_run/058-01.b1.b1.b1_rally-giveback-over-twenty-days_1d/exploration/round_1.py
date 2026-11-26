import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20, 30]
    drift = {}
    for coin, wins in bars.items():
        drift[coin] = {}
        for h in H:
            r = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    r.append(c[i + h] / c[i] - 1)
            drift[coin][h] = np.mean(r) if r else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"]).astype(str).str[:10].values
            n = len(c)
            for i in range(0, n - 20, 20):
                if f[i] < 0:
                    rec = dict(coin=coin, w=w, af=abs(f[i]), day=ts[i], year=ts[i][:4])
                    for h in H:
                        rec["x%d" % h] = (c[i + h] / c[i] - 1 - drift[coin][h]) if i + h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}

    def cl_t(s, days):
        m = pd.DataFrame({"s": s, "d": days}).dropna()
        if len(m) < 3:
            return np.nan
        mu = m["s"].mean()
        dev = (m["s"] - mu).groupby(m["d"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(m)
        return mu / se if se > 0 else np.nan

    hz = []
    for h in H:
        s = d["x%d" % h]
        ok = s.notna()
        lr = stats.linregress(d.loc[ok, "af"], s[ok])
        hz.append(dict(h=h, n=int(ok.sum()), mean=s.mean(), t_cl=cl_t(s, d["day"]),
                       slope=lr.slope, slope_t=lr.slope / lr.stderr))
    out["by_horizon"] = pd.DataFrame(hz)
    d["q"] = pd.qcut(d["af"], 3, labels=["low", "mid", "high"]).astype(str)
    out["by_tercile"] = d.groupby("q")[["x5", "x10", "x20", "x30"]].mean()
    out["tercile_counts"] = d.groupby("q")["x20"].agg(["count", "median"])
    out["by_window_x20"] = d.groupby("w")["x20"].agg(["count", "mean"])
    out["by_coin_x20"] = d.groupby("coin")["x20"].agg(["count", "mean"])
    out["n_days"] = int(d["day"].nunique())
    out["share_neg_x20"] = float((d["x20"] < 0).mean())
    out["share_capped"] = float((d["af"] >= 19.9).mean())
    return out
