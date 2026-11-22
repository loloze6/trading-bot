import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 6]
    rows = []
    drift = {}
    usual = {}
    # coin drift per horizon over all windows (non-overlapping grid)
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = rs.mean()
            usual[(coin, h)] = rs.std()
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = df["volume"].rolling(720, min_periods=240).mean().shift(1)
            z = r / sd
            vr = df["volume"] / vm
            year = pd.to_datetime(df["timestamp"]).dt.year
            f = df["forecast"].fillna(0).values
            n = len(df)
            cv = c.values
            for h in H:
                fwd = np.full(n, np.nan)
                fwd[: n - h] = cv[h:] / cv[: n - h] - 1
                df[f"x{h}"] = fwd - drift[(coin, h)]
                df[f"r{h}"] = fwd
            df["z"] = z; df["vr"] = vr; df["year"] = year
            df["coin"] = coin; df["win"] = w
            df["pos"] = np.arange(n)
            df["cell"] = df["pos"] // 6
            df["f"] = f
            rows.append(df[["coin", "win", "year", "pos", "cell", "z", "vr", "f"] + [f"x{h}" for h in H] + [f"r{h}" for h in H]])
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["z", "vr", "x6"])

    def summ(g, col="x6"):
        v = g[col].dropna()
        return pd.Series({"n": len(v), "mean_bp": v.mean() * 1e4, "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})

    # one case per 6-bar cell: first bar in cell with forecast >= 2 (approx of plan)
    C = A[A["f"] >= 2].groupby(["coin", "win", "cell"]).head(1)
    out = {}
    C["fbin"] = pd.cut(C["f"], [2, 3, 5, 8, 12, 20.01], right=False)
    out["cases_by_forecast_bin_x6"] = C.groupby("fbin").apply(summ)
    out["cases_by_coin_x6"] = C.groupby("coin").apply(summ)
    out["cases_by_year_x6"] = C.groupby("year").apply(summ)
    out["cases_by_horizon"] = pd.DataFrame({f"h{h}": summ(C, f"x{h}") for h in H}).T

    # event grid: z and volume ratio bins, one per 6-bar cell (most extreme |z| in cell)
    A["absz"] = A["z"].abs()
    E = A.loc[A.groupby(["coin", "win", "cell"])["absz"].idxmax()].copy()
    E["dir"] = np.sign(E["z"])
    big = E[E["absz"] >= 3].copy()
    big["vbin"] = pd.cut(big["vr"], [0, 1.5, 3, 5, 1e9])
    res = []
    for (d, vb), g in big.groupby(["dir", "vbin"]):
        for h in H:
            v = (g[f"x{h}"] * d).dropna()
            if len(v) > 5:
                res.append({"dir": d, "vbin": str(vb), "h": h, "n": len(v), "mean_bp_signed": v.mean() * 1e4,
                            "t": v.mean() / (v.std() / np.sqrt(len(v)))})
    out["bigmove_dir_volbin_signed_excess"] = pd.DataFrame(res)
    # by coin for big up/down with vr>=3, h=6 and h=2
    res2 = []
    for (coin, d), g in big[big["vr"] >= 3].groupby(["coin", "dir"]):
        for h in [2, 6]:
            v = (g[f"x{h}"] * d).dropna()
            res2.append({"coin": coin, "dir": d, "h": h, "n": len(v), "bp": v.mean() * 1e4, "t": v.mean() / (v.std() / np.sqrt(len(v)))})
    out["surge_bigmove_by_coin"] = pd.DataFrame(res2)
    out["usual_move_6"] = pd.Series({k[0]: v for k, v in usual.items() if k[1] == 6})
    return out
