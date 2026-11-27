import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    allrets = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            r1 = pd.Series(c).pct_change()
            allrets.append(r1.dropna().values)
            rng = pd.Series((h - l) / c)
            mrng = rng.rolling(20).mean()
            ratio = rng / mrng
            sd20 = r1.rolling(20).std()
            ret5lag = pd.Series(c).shift(1) / pd.Series(c).shift(6) - 1
            fall5 = ret5lag / (sd20 * np.sqrt(5))
            tr60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            fwd = {k: pd.Series(c).shift(-k) / pd.Series(c) - 1 for k in (1, 2, 3, 5)}
            fc = b["forecast"].values
            alloc = b["postRebalance_current_allocation"].values
            for t in range(n):
                if not (r1[t] > 0 and ratio[t] > 1 and fall5[t] <= -1):
                    continue
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"][t]).year,
                                 day=str(pd.Timestamp(b["timestamp"][t]).date()),
                                 fc=fc[t], alloc=alloc[t], up=r1[t], ratio=ratio[t], fall5=fall5[t],
                                 tr60=tr60[t], f1=fwd[1][t], f2=fwd[2][t], f3=fwd[3][t], f5=fwd[5][t],
                                 sd=sd20[t]))
    df = pd.DataFrame(rows)
    drift = np.concatenate(allrets).mean()
    df["u1"] = -(df["f1"] - drift)
    df["prof"] = np.where(df["tr60"] < -0.10, "falling", np.where(df["tr60"] > 0.10, "rising", np.where(df["tr60"].isna(), "na", "choppy")))
    df["active"] = df["fc"] < 0
    def summ(g):
        x = g["u1"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              m2=-(g["f2"] - 2 * drift).mean(), m3=-(g["f3"] - 3 * drift).mean(), m5=-(g["f5"] - 5 * drift).mean()))
    out["by_profile"] = df.groupby("prof").apply(summ)
    out["by_active"] = df[df.prof == "falling"].groupby("active").apply(summ)
    f = df[df.prof == "falling"].copy()
    for col in ["fall5", "up", "ratio", "tr60", "fc"]:
        f["q"] = pd.qcut(f[col].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out["falling_by_" + col] = f.groupby("q").apply(summ).assign(med=f.groupby("q")[col].median())
    out["spearman_falling"] = pd.Series({col: stats.spearmanr(f[col], f["u1"], nan_policy="omit")[0] for col in ["fall5", "up", "ratio", "tr60", "fc"]})
    out["falling_by_coin"] = f.groupby("coin").apply(summ)
    out["falling_by_year"] = f.groupby("year").apply(summ)
    # without fall5 condition: wide up days in falling, graded by width
    out["fc_unique_share"] = pd.Series({"n_active": int(f.active.sum()), "n_unique_fc": f.loc[f.active, "fc"].nunique(), "share_fc_-20": (f.loc[f.active, "fc"] <= -19.99).mean()})
    # book decomposition
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; x["year"] = pd.to_datetime(x["day"]).dt.year; d.append(x)
    D = pd.concat(d)
    out["book_by_coin_sum"] = D.groupby("coin")["book_return"].sum().sort_values()
    out["book_by_year_sum"] = D.groupby("year")["book_return"].sum()
    br = D["book_return"].dropna(); nz = br[br != 0].sort_values()
    out["book_top"] = pd.Series({"n_nonzero_days": len(nz), "sum_all": nz.sum(), "sum_top10": nz.tail(10).sum(), "sum_bottom10": nz.head(10).sum()})
    return out
