import numpy as np, pandas as pd

def _er(c, n=60, s=5):
    ch = (c - c.shift(n)).abs()
    vol = c.diff().abs().rolling(n).sum()
    return (ch / vol).rolling(s).mean()

def _t(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            ph = hi.shift(1).rolling(60).max(); pl = lo.shift(1).rolling(60).min()
            df = pd.DataFrame({"coin": coin, "w": w, "ts": ts, "c": c, "er": _er(c),
                               "up": (c / ph - 1) * 100, "dn": (c / pl - 1) * 100,
                               "width": (ph / pl - 1) * 100, "pos": np.arange(len(b)),
                               "f10": c.shift(-10) / c - 1, "f5": c.shift(-5) / c - 1})
            df["yr"] = ts.dt.year
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    d10 = A[(A.pos % 10 == 0)].groupby("coin")["f10"].mean()
    d5 = A[(A.pos % 5 == 0)].groupby("coin")["f5"].mean()
    A["ex10"] = A.f10 - A.coin.map(d10); A["ex5"] = A.f5 - A.coin.map(d5)
    A["cell"] = A.pos // 10
    prev_up = A.groupby(["coin", "w"])["up"].shift(1); prev_dn = A.groupby(["coin", "w"])["dn"].shift(1)
    Dn = A[(A.dn < 0) & (prev_dn >= 0)].drop_duplicates(["coin", "w", "cell"]).dropna(subset=["ex10", "er"]).copy()
    Dn["trendless"] = Dn.er <= 0.3
    out["down_ex10_by_trendless"] = Dn.groupby("trendless")["ex10"].agg(n="size", mean="mean", t=_t).round(4)
    Dt = Dn[Dn.trendless].copy()
    out["down_trendless_ex5_ex10"] = pd.DataFrame({k: {"n": Dt[k].notna().sum(), "mean": Dt[k].mean(), "t": _t(Dt.groupby("ts")[k].mean())} for k in ["ex5", "ex10"]}).T.round(4)
    out["down_trendless_ex10_by_year"] = Dt.groupby("yr")["ex10"].agg(n="size", mean="mean").round(4)
    out["down_trendless_ex10_by_coin"] = Dt.groupby("coin")["ex10"].agg(n="size", mean="mean").round(4)
    Dt["lw"] = np.log(Dt.width)
    out["down_trendless_slope_ex10_on_logwidth"] = float(np.polyfit(Dt.lw, Dt.ex10, 1)[0])
    out["down_trendless_corr_ex10_logwidth"] = float(np.corrcoef(Dt.lw, Dt.ex10)[0, 1])
    U = A[(A.up > 0) & (prev_up <= 0) & (A.er <= 0.3)].drop_duplicates(["coin", "w", "cell"]).dropna(subset=["ex10"]).copy()
    out["up_trendless_ex10_by_year"] = U.groupby("yr")["ex10"].agg(n="size", mean="mean").round(4)
    out["up_trendless_corr_ex10_logwidth"] = float(np.corrcoef(np.log(U.width), U.ex10)[0, 1])
    out["up_trendless_n_coins_positive"] = int((U.groupby("coin")["ex10"].mean() > 0).sum())
    out["up_trendless_n_coins"] = int(U.coin.nunique())
    return out
