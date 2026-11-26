import numpy as np
import pandas as pd
from scipy import stats

def qc(x, q):
    return pd.qcut(x.rank(method="first"), q, labels=False)

def explore(data):
    bars = data["bars"]
    days = data["days"]
    out = {}
    H = 20
    coin_mean = {}; coin_sd = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                rs.append(cl[i + H] / cl[i] - 1)
        coin_mean[c] = np.mean(rs); coin_sd[c] = np.std(rs, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].reset_index(drop=True).astype(float)
            n = len(cl)
            pmax = cl.shift(1).rolling(60).max()
            pmin = cl.shift(1).rolling(60).min()
            r60 = cl.shift(1) / cl.shift(61) - 1
            r1 = cl / cl.shift(1) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            r5 = cl / cl.shift(5) - 1
            r20 = cl / cl.shift(20) - 1
            dhi = cl / pmax - 1
            dlo = cl / pmin - 1
            rng = pmax / pmin - 1
            pos = (cl - pmin) / (pmax - pmin)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            def rec(kind, i):
                return dict(coin=c, w=w, kind=kind, i=i, day=ts[i].normalize(),
                            fwd=cl[i + H] / cl[i] - 1, fwd5=(cl[i + 5] / cl[i] - 1) if i + 5 < n else np.nan,
                            r60=r60[i], r20=r20[i], r5=r5[i], r1=r1[i], vol20=vol20[i], vr=vol20[i] / vol60[i],
                            dhi=dhi[i], dlo=dlo[i], rng=rng[i], pos=pos[i], wd=ts[i].dayofweek, yr=ts[i].year)
            for g in range(0, n - H, H):
                rows.append(rec("grid", g))
                for i in range(g, min(g + H, n - H)):
                    if not np.isnan(pmax[i]) and cl[i] > pmax[i]:
                        rows.append(rec("up", i)); break
                for i in range(g, min(g + H, n - H)):
                    if not np.isnan(pmin[i]) and cl[i] < pmin[i]:
                        rows.append(rec("dn", i)); break
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d["coin"].map(coin_mean)
    d["z"] = d["ex"] / d["coin"].map(coin_sd)
    def summ(g):
        e = g["ex"].dropna()
        dd = g.dropna(subset=["ex"]).groupby("day")["ex"].sum()
        tcl = dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd))) * 1.0 if len(dd) > 2 else np.nan
        return pd.Series(dict(n=len(e), days=len(dd), mean_ex=e.mean(), mean_z=g["z"].mean(),
                              t=stats.ttest_1samp(e, 0).statistic if len(e) > 2 else np.nan,
                              t_day=tcl, hit=(g["fwd"] > 0).mean()))
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as ex:
            out[name] = "err: " + str(ex)[:80]
    safe("by_kind", lambda: d.groupby("kind").apply(summ))
    safe("up_by_coin", lambda: d[d.kind == "up"].groupby("coin").apply(summ))
    safe("dn_by_coin", lambda: d[d.kind == "dn"].groupby("coin").apply(summ))
    safe("kind_by_year", lambda: d[d.kind != "grid"].groupby(["kind", "yr"]).apply(summ))
    up = d[d.kind == "up"].dropna(subset=["r60", "dhi", "rng", "vr"]).copy()
    for col in ["r60", "dhi", "rng", "vr", "r5", "vol20"]:
        safe("up_by_" + col, lambda col=col: up.assign(q=qc(up[col], 3)).groupby("q").apply(
            lambda g: pd.concat([summ(g), pd.Series({"med_" + col: g[col].median()})])))
    dn = d[d.kind == "dn"].dropna(subset=["r60", "dlo", "rng"]).copy()
    for col in ["r60", "dlo", "rng"]:
        safe("dn_by_" + col, lambda col=col: dn.assign(q=qc(dn[col], 3)).groupby("q").apply(
            lambda g: pd.concat([summ(g), pd.Series({"med_" + col: g[col].median()})])))
    gr = d[d.kind == "grid"].dropna(subset=["r60", "vol20", "pos", "r20"]).copy()
    for col in ["r60", "r20", "r5", "r1", "pos", "vol20", "rng", "vr"]:
        safe("grid_by_" + col, lambda col=col: gr.assign(q=qc(gr[col], 5)).groupby("q").apply(
            lambda g: pd.concat([summ(g), pd.Series({"med_" + col: g[col].median()})])))
    safe("grid_by_weekday", lambda: gr.groupby("wd").apply(summ))
    # book: daily returns, largest days
    def book():
        rr = []
        for c in days:
            for w, df in days[c].items():
                x = df[["book_return", "coin_return"]].copy(); x["coin"] = c
                rr.append(x)
        b = pd.concat(rr).dropna()
        b["inpos"] = b["book_return"] != 0
        res = {}
        res["n_days_inpos"] = b["inpos"].sum()
        res["mean_book_inpos"] = b.loc[b.inpos, "book_return"].mean()
        top = b[b.inpos].sort_values("book_return")
        k = max(1, int(0.05 * len(top)))
        res["share_gain_top5pct_days"] = top["book_return"].tail(k).sum() / top["book_return"].sum()
        res["share_gain_by_coin"] = None
        return pd.Series(res)
    safe("book_summary", book)
    def book_coin():
        rr = []
        for c in days:
            for w, df in days[c].items():
                x = df[["book_return"]].dropna(); rr.append(pd.Series({"coin": c, "sum": x["book_return"].sum()}))
        return pd.DataFrame(rr).groupby("coin")["sum"].sum()
    safe("book_sum_by_coin", book_coin)
    def trades():
        tt = []
        for c in data["trades"]:
            for w, t in data["trades"][c].items():
                if len(t): tt.append(t.assign(coin=c))
        t = pd.concat(tt)
        t["days"] = t["duration_minutes"] / 1440
        t["q"] = qc(t["entry_forecast"], 3)
        return t.groupby("q").agg(n=("net_profit_loss_percent", "size"), mean_pl=("net_profit_loss_percent", "mean"),
                                  hit=("net_profit_loss_percent", lambda s: (s > 0).mean()),
                                  med_fc=("entry_forecast", "median"), med_days=("days", "median"))
    safe("trades_by_entry_fc", trades)
    return out
