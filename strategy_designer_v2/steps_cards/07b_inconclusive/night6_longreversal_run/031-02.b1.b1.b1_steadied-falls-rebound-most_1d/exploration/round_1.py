import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    H = 30
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            lh = b.get("debug_info.components.ret30.last_history_value")
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                fwd = c[t + H] / c[t] - 1
                r30 = np.nan
                if lh is not None and pd.notna(lh.iloc[t]):
                    r30 = lh.iloc[t]
                elif t >= 30:
                    r30 = c[t] / c[t - 30] - 1
                r60 = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts.iloc[t].year, fwd=fwd,
                                 r30=r30, r60=r60, reg=b["regime"].iloc[t],
                                 fc=b["forecast"].iloc[t]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    out = {}
    out["n_all, n_regime"] = f"{len(df)}, {(df.reg=='mean_reversion').sum()}"
    # raw scale check of r30 in regime
    R = df[df.reg == "mean_reversion"].copy()
    out["regime r30 describe"] = R["r30"].describe()

    def reg(d, x="r30"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 5 or d[x].std() == 0:
            return pd.Series(dict(n=len(d)))
        s = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope / s.stderr,
                              mean_ex=d["ex"].mean(), mean_fwd=d["fwd"].mean()))

    out["regime: ex on fc"] = reg(R, "fc")
    out["regime: ex on r30"] = reg(R, "r30")
    R["side"] = np.where(R["fc"] > 0, "long", np.where(R["fc"] < 0, "short", "zero"))
    g = R.groupby("side")["ex"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["regime by side (ex)"] = g
    g2 = R.groupby("side")["fwd"].agg(["count", "mean"])
    out["regime by side (fwd)"] = g2
    R["q"] = pd.qcut(R["r30"].rank(method="first"), 4, labels=False)
    out["regime by r30 quartile"] = R.groupby("q").agg(n=("ex", "size"), r30=("r30", "mean"),
                                                        ex=("ex", "mean"), fwd=("fwd", "mean"))
    out["regime by year"] = R.groupby("year").apply(lambda d: reg(d, "fc")).unstack() if False else R.groupby("year").apply(lambda d: pd.Series(dict(n=len(d), ex=d.ex.mean(), ex_long=d[d.fc>0].ex.mean(), ex_short=d[d.fc<0].ex.mean())))
    out["regime by coin"] = R.groupby("coin").apply(lambda d: pd.Series(dict(n=len(d), ex=d.ex.mean(), ex_short=d[d.fc<0].ex.mean())))
    # all bars: 30d and 60d past return vs forward
    A = df.copy()
    out["all: ex on r30"] = reg(A, "r30")
    out["all: ex on r60"] = reg(A, "r60")
    A["q"] = pd.qcut(A["r30"].rank(method="first"), 5, labels=False)
    out["all by r30 quintile"] = A.dropna(subset=["r30"]).groupby("q").agg(n=("ex","size"), r30=("r30","mean"), ex=("ex","mean"))
    NR = A[A.reg != "mean_reversion"]
    out["non-regime: ex on r30"] = reg(NR, "r30")
    out["regime vs not mean ex"] = A.groupby(A.reg == "mean_reversion")["ex"].agg(["count", "mean", "std"])
    return out
