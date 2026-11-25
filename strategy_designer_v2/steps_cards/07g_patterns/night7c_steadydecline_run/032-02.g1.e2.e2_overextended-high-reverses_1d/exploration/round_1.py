import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            df = pd.DataFrame({"coin": coin, "win": w})
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            df["fwd5"] = c.shift(-5) / c - 1
            df["r28"] = c / c.shift(28) - 1
            df["r5p"] = c / c.shift(5) - 1
            df["r1p"] = c / c.shift(1) - 1
            df["dh28"] = c / c.rolling(28).max() - 1
            df["dl28"] = c / c.rolling(28).min() - 1
            lr = np.log(c).diff()
            df["vol20"] = lr.rolling(20).std()
            df["volrel"] = df["vol20"] / lr.rolling(60, min_periods=40).std()
            df["rng"] = ((h - l) / c).rolling(5).mean() / ((h - l) / c).rolling(60, min_periods=40).mean()
            vv = b["volume"].astype(float)
            df["vrel"] = vv.rolling(5).mean() / vv.rolling(60, min_periods=40).mean()
            df["runraw"] = pd.to_numeric(b.get("debug_info.components.runup.last_history_value"), errors="coerce")
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["grid"] = (np.arange(len(b)) % 5) == 0
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D[D.grid].groupby("coin")["fwd5"].mean()
    sd = D[D.grid].groupby("coin")["fwd5"].std()
    D["ex"] = D["fwd5"] - D["coin"].map(drift)
    D["exz"] = D["ex"] / D["coin"].map(sd)
    G = D[D.grid & D.ex.notna()].copy()
    out = {"n_grid": len(G), "drift_by_coin": drift.round(4)}

    def qtab(var, q=5, sub=None):
        S = G if sub is None else sub
        S = S[S[var].notna()].copy()
        S["q"] = S.groupby("coin")[var].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = S.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_z=("exz", "mean"), mid=(var, "median"))
        t["t"] = S.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t.round(4)

    def corr(var, sub=None):
        S = G if sub is None else sub
        S = S[[var, "exz", "day"]].dropna()
        S = S.assign(rz=S.groupby(G.loc[S.index, "coin"])[var].rank(pct=True) - 0.5)
        S["p"] = S.rz * S.exz
        d = S.groupby("day")["p"].sum()
        return f"n={len(S)} days={len(d)} mean(rank*exz)={S.p.mean():.4f} t_day={d.mean()/(d.std()/np.sqrt(len(d))):.2f}"

    for v in ["r28", "dh28", "dl28", "r5p", "r1p", "vol20", "volrel", "rng", "vrel"]:
        out["q_" + v] = qtab(v)
        out["c_" + v] = corr(v)
    out["wd"] = G.groupby("wd")["ex"].agg(["size", "mean"]).round(4)
    out["by_win_athigh"] = G[G.dh28 >= 0].groupby("win")["ex"].agg(["size", "mean"]).round(4)
    out["athigh_vs_not"] = G.groupby(G.dh28 >= 0)["ex"].agg(["size", "mean", "std"]).round(4)
    out["q_r28_athigh"] = qtab("r28", 3, G[G.dh28 >= 0])
    out["c_r28_athigh"] = corr("r28", G[G.dh28 >= 0])
    calm = G[(G.r28 < 0)]
    out["q_rng_in_decline"] = qtab("rng", 3, calm)
    out["c_r28_in_decline"] = corr("r28", calm)
    return out
