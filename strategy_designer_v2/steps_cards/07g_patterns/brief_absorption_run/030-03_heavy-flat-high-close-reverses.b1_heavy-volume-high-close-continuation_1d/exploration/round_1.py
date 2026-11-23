import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 10]
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            cl = (2*c - hi - lo) / rng
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            r1 = c.pct_change()
            r10p = c / c.shift(10) - 1
            vol20 = r1.rolling(20, min_periods=20).std()
            rngrel = (hi - lo) / c
            rngr = rngrel / rngrel.shift(1).rolling(20, min_periods=20).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "cl": cl, "vr": vr, "r1": r1, "r10p": r10p, "vol20": vol20,
                               "rngr": rngr, "fc": b["forecast"].astype(float),
                               "wd": ts.dt.dayofweek, "year": ts.dt.year})
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h in H:
        g = d[d["pos"] % h == 0].dropna(subset=[f"f{h}"])
        drift = g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(drift)
        d[f"g{h}"] = d["pos"] % h == 0
        out[f"drift_{h}d"] = drift
    def tab(key, h, mask=None):
        s = d[d[f"g{h}"]].dropna(subset=[key, f"u{h}"])
        if mask is not None: s = s[mask(s)]
        q = pd.qcut(s[key].rank(method="first"), 5, labels=False)
        r = s.groupby(q)[f"u{h}"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["key_mean"] = s.groupby(q)[key].mean()
        return r.drop(columns="std").round(4)
    heavy = lambda s: s["vr"] > s["vr"].quantile(0.8)
    out["cl_q_heavy_10d"] = tab("cl", 10, heavy)
    out["cl_q_heavy_3d"] = tab("cl", 3, heavy)
    out["cl_q_heavy_1d"] = tab("cl", 1, heavy)
    out["cl_q_all_10d"] = tab("cl", 10)
    out["vr_q_10d"] = tab("vr", 10)
    out["vr_q_3d"] = tab("vr", 3)
    out["r1_q_1d"] = tab("r1", 1)
    out["r1_q_10d"] = tab("r1", 10)
    out["r10p_q_10d"] = tab("r10p", 10)
    out["vol20_q_10d"] = tab("vol20", 10)
    out["rngr_q_3d"] = tab("rngr", 3)
    out["rngr_q_10d"] = tab("rngr", 10)
    s = d[d["g1"]].dropna(subset=["u1"])
    wd = s.groupby("wd")["u1"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday_1d"] = wd.drop(columns="std").round(5)
    s10 = d[d["g10"]].dropna(subset=["u10"])
    yr = s10.groupby("year")["u10"].agg(["mean", "count"]); out["year_u10"] = yr.round(4)
    s = d[d["g10"] & (d["fc"] > 0)].dropna(subset=["u10"])
    out["fc_pos_by_coin"] = s.groupby("coin")["u10"].agg(["mean", "count"]).round(4)
    return out
