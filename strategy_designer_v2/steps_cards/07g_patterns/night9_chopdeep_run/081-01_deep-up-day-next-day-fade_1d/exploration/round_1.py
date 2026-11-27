import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            hi20 = c.rolling(20, min_periods=20).max()
            sd20 = r.rolling(20, min_periods=15).std()
            depth = (c - hi20) / hi20 / sd20
            lo20 = c.rolling(20, min_periods=20).min()
            height = (c - lo20) / lo20 / sd20
            ret60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c / sd20
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol_rel = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            sd_rel = sd20 / r.rolling(60, min_periods=40).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "r": r, "rz": r / sd20, "nxt": nxt, "depth": depth,
                "height": height, "ret60": ret60, "rng": rng, "clpos": clpos,
                "vol_rel": vol_rel, "sd_rel": sd_rel,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["nxt", "r"])
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["up"] = d["r"] > 0
    d["pnl"] = d["pos"] * d["nxt"]

    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    dd = d.dropna(subset=["depth"]).copy()
    dd["dq"] = pd.qcut(dd["depth"], 5, labels=["deep1", "q2", "q3", "q4", "shallow5"])
    out["depth_quint_by_up"] = dd.groupby(["up", "dq"]).apply(summ)
    dd["rzq"] = pd.qcut(dd["rz"], 6, labels=False)
    out["today_move_sextile"] = dd.groupby("rzq").apply(summ)
    out["up_depth_x_move"] = dd[dd.up].assign(dq3=pd.qcut(dd[dd.up]["depth"], 3, labels=["deep", "mid", "shal"]),
        mq=pd.qcut(dd[dd.up]["rz"], 3, labels=["small", "mid", "big"])).groupby(["dq3", "mq"]).apply(summ)
    t = dd.dropna(subset=["ret60"]).copy()
    t["trend"] = np.where(t.ret60 > .1, "rising", np.where(t.ret60 < -.1, "falling", "choppy"))
    t["agit"] = np.where(t.sd_rel > 1, "agit", "calm")
    t["dq3"] = pd.qcut(t["depth"], 3, labels=["deep", "mid", "shal"])
    out["up_trend_agit_depth"] = t[t.up].groupby(["trend", "agit", "dq3"]).apply(summ)
    out["down_trend_agit_depth"] = t[~t.up].groupby(["trend", "agit", "dq3"]).apply(summ)
    hh = d.dropna(subset=["height"]).copy()
    hh["hq"] = pd.qcut(hh["height"], 5, labels=False)
    out["height_quint_by_up"] = hh.groupby(["up", "hq"]).apply(summ)
    cc = d.dropna(subset=["clpos"]).copy()
    cc["cq"] = pd.qcut(cc["clpos"], 4, labels=["low", "q2", "q3", "high"])
    out["closepos_by_up"] = cc.groupby(["up", "cq"]).apply(summ)
    vv = d.dropna(subset=["vol_rel"]).copy()
    vv["vq"] = pd.qcut(vv["vol_rel"], 4, labels=False)
    out["volume_by_up"] = vv.groupby(["up", "vq"]).apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    out["pnl_by_window"] = d.groupby("w").agg(pnl_mean_bp=("pnl", lambda x: 1e4 * x.mean()), n=("pnl", "size"))
    out["pnl_by_coin"] = d.groupby("coin").agg(pnl_bp=("pnl", lambda x: 1e4 * x.mean()), n=("pnl", "size"), ex_up_mean=("ex", "mean"))
    return out
