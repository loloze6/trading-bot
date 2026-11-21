import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            fwd = c.shift(-H) / c - 1
            sma50 = c.rolling(50, min_periods=50).mean()
            mad = c / sma50 - 1
            r20 = c / c.shift(20) - 1
            r5 = c / c.shift(5) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=20).std()
            hi30 = c.rolling(30, min_periods=30).max()
            near = c / hi30 - 1
            lo30 = c.rolling(30, min_periods=30).min()
            rng = (c - lo30) / (hi30 - lo30)
            ts = pd.to_datetime(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].astype(float)
            fc = b["forecast"].astype(float)
            pos = np.arange(n)
            df = pd.DataFrame(dict(coin=coin, win=w, fwd=fwd, mad=mad, r20=r20, r5=r5,
                                   vol20=vol20, near=near, rng=rng, fc=fc, alloc=alloc,
                                   year=ts.dt.year, wd=ts.dt.weekday, grid=(pos % H == 0)))
            recs.append(df)
            dd = pd.DataFrame(dict(coin=coin, win=w, r=r1, wd=ts.dt.weekday, year=ts.dt.year,
                                   gain=alloc.shift(1) * r1))
            daily.append(dd)
        cd = pd.concat(recs)
        g = cd[cd.grid & cd.fwd.notna()]
        drift = g.fwd.mean()
        usual = g.fwd.std()
        cd["un"] = cd.fwd - drift
        cd["str"] = cd.un / usual
        rows.append(cd)
    A = pd.concat(rows)
    G = A[A.grid & A.fwd.notna()].copy()
    out = {}
    def tab(col, q=5):
        x = G[G[col].notna()].copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = x.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), sd=("un", "std"), strength=("str", "mean"), lo=(col, "mean"))
        r["t"] = r.mean_un / (r.sd / np.sqrt(r.n))
        rho = stats.spearmanr(x[col], x["str"])
        r["spearman_all"] = rho.correlation
        return r.drop(columns="sd").round(4)
    for col in ["mad", "r20", "r5", "vol20", "near", "rng"]:
        out["fwd5_by_" + col] = tab(col)
    # vol interacting with r20
    x = G.dropna(subset=["r20", "vol20"]).copy()
    x["vq"] = x.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["rq"] = x.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["un_by_vol_x_r20"] = x.pivot_table(index="vq", columns="rq", values="str", aggfunc="mean").round(3)
    out["n_by_vol_x_r20"] = x.pivot_table(index="vq", columns="rq", values="str", aggfunc="size")
    # in-position vs not
    G["inpos"] = G.alloc > 0.01
    r = G.groupby("inpos").agg(n=("un", "size"), mean_un=("un", "mean"), sd=("un", "std"))
    r["t"] = r.mean_un / (r.sd / np.sqrt(r.n)); out["un_by_inpos"] = r.round(4)
    D = pd.concat(daily).dropna(subset=["r"])
    wd = D.groupby("wd").r.agg(["size", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["coin_ret_by_weekday"] = wd.round(5)
    out["book_gain_by_year"] = D.groupby("year").gain.agg(["mean", "sum", "size"]).round(5)
    out["coin_ret_by_year"] = D.groupby("year").r.mean().round(5)
    out["book_gain_by_coin"] = D.groupby("coin").gain.agg(["mean", "sum"]).round(5)
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["days"] = T.duration_minutes / 1440
    T["dq"] = pd.qcut(T.days.rank(method="first"), 4, labels=False)
    out["trades_by_duration"] = T.groupby("dq").agg(n=("days", "size"), days=("days", "mean"), pnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean())).round(3)
    T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = T.groupby("fq").agg(n=("days", "size"), fc=("entry_forecast", "mean"), pnl=("net_profit_loss_percent", "mean")).round(3)
    return out
