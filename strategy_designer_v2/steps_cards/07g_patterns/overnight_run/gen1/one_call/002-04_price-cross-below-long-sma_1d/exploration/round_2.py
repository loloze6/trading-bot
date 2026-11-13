import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            o = b["open"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "w": w, "i": np.arange(len(b)),
                "dist": b["debug_info.components.below_ma.last_history_value"].astype(float),
                "r1": r1, "r5": c / c.shift(5) - 1, "r20": c / c.shift(20) - 1,
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f10": c.shift(-10) / c - 1,
                "clpos": (c - l) / (h - l).replace(0, np.nan),
                "vol20": r1.rolling(20).std(),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "bv": b["postRebalance_total_value"].astype(float),
            })
            d["br1"] = d["bv"].shift(-1) / d["bv"] - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["z1"] = A["r1"] / A.groupby(["coin", "w"])["vol20"].shift(1)
    A["below"] = A["dist"] < 0
    out = {}
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "up": (x > 0).mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    big = A[A["z1"] < -2]
    out["drop_z<-2_f1_f3"] = pd.DataFrame({"f1": summ(big["f1"]), "f3": summ(big["f3"]), "all_f1": summ(A["f1"])})
    out["drop_z<-2_f1_by_year"] = big.groupby("yr")["f1"].apply(summ).unstack()
    out["drop_z<-2_f1_by_coin"] = big.groupby("coin")["f1"].apply(summ).unstack()
    out["drop_z<-2_f1_by_below"] = big.groupby("below")["f1"].apply(summ).unstack()
    big["clq"] = pd.cut(big["clpos"], [-0.01, 0.2, 0.5, 1.01])
    out["drop_z<-2_f1_by_closepos"] = big.groupby("clq")["f1"].apply(summ).unstack()
    up = A[A["z1"] > 2]
    out["rise_z>2_f1"] = summ(up["f1"])
    # weekday by year, Thu+Fri
    A["thfr"] = A["wd"].isin([3, 4])
    out["thfr_minus_other_f1_by_year"] = A.groupby("yr").apply(lambda g: g.loc[g.thfr, "f1"].mean() - g.loc[~g.thfr, "f1"].mean())
    out["f1_by_wd_below"] = A[A.below].groupby("wd")["f1"].apply(summ).unstack()
    # above MA momentum, non-overlapping (every 10th bar)
    NO = A[A["i"] % 10 == 0].copy()
    NO["r5q"] = NO.groupby("coin")["r5"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["nonovl_f10_above_by_r5q"] = NO[~NO.below].groupby("r5q")["f10"].apply(summ).unstack()
    out["nonovl_f10_below_by_r5q"] = NO[NO.below].groupby("r5q")["f10"].apply(summ).unstack()
    out["nonovl_top_r5_above_by_year"] = NO[(~NO.below) & (NO.r5q == 4)].groupby("yr")["f10"].apply(summ).unstack()
    # book's largest daily losses and gains: what preceded
    act = A[A.alloc != 0].dropna(subset=["br1"])
    lo = act[act.br1 <= act.br1.quantile(0.05)]; hi = act[act.br1 >= act.br1.quantile(0.95)]
    out["before_book_tails"] = pd.DataFrame({
        "worst5%": [lo.r1.mean(), lo.r5.mean(), lo.dist.mean(), lo.alloc.mean(), (lo.r1 < 0).mean()],
        "best5%": [hi.r1.mean(), hi.r5.mean(), hi.dist.mean(), hi.alloc.mean(), (hi.r1 < 0).mean()],
        "all_active": [act.r1.mean(), act.r5.mean(), act.dist.mean(), act.alloc.mean(), (act.r1 < 0).mean()]},
        index=["r1", "r5", "dist", "alloc", "share_r1_neg"])
    return out
