import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr) if allr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            rng = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret28": c / c.shift(28) - 1,
                "ret7": c / c.shift(7) - 1,
                "rng_ratio": rng.rolling(20).mean() / rng.rolling(90, min_periods=40).mean(),
                "volu_ratio": b["volume"].rolling(20).mean() / b["volume"].rolling(90, min_periods=40).mean(),
                "fwd": c.shift(-H) / c - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    out = {}

    def clustered_slope(d, col):
        d = d.dropna(subset=[col, "ex"]).copy()
        x = d[col].rank(pct=True) - 0.5
        y = d["ex"]
        beta = (x * (y - y.mean())).sum() / (x ** 2).sum()
        res = (y - y.mean()) - beta * x
        s = (x * res).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (x ** 2).sum()
        return beta, beta / se, len(d), d["day"].nunique()

    def by_win(d, col):
        d = d.dropna(subset=[col, "ex"])
        r = d.groupby("win").apply(lambda g: pd.Series({"n": len(g),
              "spearman": stats.spearmanr(g[col], g["ex"]).correlation if len(g) > 8 else np.nan}))
        r["pos"] = (r["spearman"] > 0).astype(int)
        return r.round(3)

    F = G[G["ret28"] <= 0].copy()
    W = F[F["rng_ratio"] >= 1].copy()
    W["fall"] = -W["ret28"]
    Lv = F[F["volu_ratio"] < 1].copy()
    Lv["fall"] = -Lv["ret28"]
    res = {}
    for name, d, col in [("all ret7", G, "ret7"),
                         ("falling wide-range: fall depth", W, "fall"),
                         ("falling low-volume: fall depth", Lv, "fall"),
                         ("falling all: rng_ratio", F, "rng_ratio"),
                         ("falling all: volu_ratio", F, "volu_ratio")]:
        b_, t_, n_, nd = clustered_slope(d, col)
        res[name] = {"slope_rankpct": round(b_, 4), "t_dayclust": round(t_, 2), "n": n_, "days": nd}
    out["clustered slopes"] = pd.DataFrame(res).T
    out["ret7 all by window"] = by_win(G, "ret7")
    out["wide-range fall depth by window"] = by_win(W, "fall")
    out["low-volume fall depth by window"] = by_win(Lv, "fall")
    # interaction: falling, depth x range ratio terciles
    F2 = F.dropna(subset=["rng_ratio"]).copy()
    F2["rt"] = pd.qcut(F2["rng_ratio"].rank(method="first"), 3, labels=["calm", "mid", "wide"])
    F2["dt"] = pd.qcut(F2["ret28"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["falling: mean ex by range tercile x depth tercile"] = F2.pivot_table(index="rt", columns="dt", values="ex", aggfunc="mean").round(4)
    out["falling: n by cell"] = F2.pivot_table(index="rt", columns="dt", values="ex", aggfunc="size")
    return out
