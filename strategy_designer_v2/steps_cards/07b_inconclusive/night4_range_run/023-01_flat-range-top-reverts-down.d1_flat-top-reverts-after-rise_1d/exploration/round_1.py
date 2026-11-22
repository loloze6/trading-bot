import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            hi = c.rolling(30).max(); lo = c.rolling(30).min()
            rng = (hi - lo).replace(0, np.nan)
            pos = (c - (hi + lo) / 2) / (rng / 2)
            net = (c - c.shift(29)).abs()
            flat = 1 - net / rng
            raw = pos * flat
            z = (raw - raw.rolling(60, min_periods=20).mean()) / raw.rolling(60, min_periods=20).std()
            year = pd.to_datetime(d["timestamp"]).dt.year
            for h in [1, 3, 5, 10, 20]:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(d), h)
                sub = pd.DataFrame({"coin": coin, "w": w, "h": h, "raw": raw.iloc[idx].values,
                                    "z": z.iloc[idx].values, "pos": pos.iloc[idx].values,
                                    "flat": flat.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                    "mr": (d["regime"].iloc[idx] == "mean_reversion").values,
                                    "fc": d["forecast"].iloc[idx].values,
                                    "year": year.iloc[idx].values})
                rows.append(sub)
    A = pd.concat(rows)
    A = A.dropna(subset=["fwd"])
    drift = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["un"] = A["fwd"] - drift
    A = A.dropna(subset=["z"])
    out = {}
    def summ(g):
        # reversion: short direction for z>0 -> -un*sign(z)
        r = -np.sign(g["z"]) * g["un"]
        corr = stats.spearmanr(g["z"], g["un"])[0] if len(g) > 10 else np.nan
        return pd.Series({"n": len(g), "spearman_z_un": corr,
                          "rev_mean": r.mean(), "rev_t": r.mean() / (r.std() / np.sqrt(len(g)))})
    out["by_h_regime"] = A.groupby(["h", "mr"]).apply(summ)
    B = A[A.h == 5].copy()
    B["side"] = np.where(B.z >= 2, "top_z>=2", np.where(B.z <= -2, "bot_z<=-2", "mid"))
    out["h5_side_regime"] = B.groupby(["mr", "side"])["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["h5_flat_tercile_top"] = B[B.z >= 2].assign(ft=pd.qcut(B[B.z >= 2].flat, 3, labels=["lo", "mid", "hi"])).groupby(["mr", "ft"])["un"].agg(["count", "mean"])
    Bt = B[(B.z >= 2) & B.mr]
    out["h5_top_mr_by_coin"] = Bt.groupby("coin")["un"].agg(["count", "mean"])
    out["h5_top_mr_by_year"] = Bt.groupby("year")["un"].agg(["count", "mean"])
    out["h5_pos_quint_all"] = B.assign(q=pd.qcut(B.pos, 5, labels=False)).groupby(["mr", "q"])["un"].agg(["count", "mean"])
    return out
