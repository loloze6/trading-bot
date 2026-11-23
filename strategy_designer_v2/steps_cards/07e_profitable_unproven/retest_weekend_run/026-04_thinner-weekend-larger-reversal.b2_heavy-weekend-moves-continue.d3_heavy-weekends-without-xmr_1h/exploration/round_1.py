import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    # drift per coin, 48h and 24h/72h
    drift = {}
    usual = {}
    for c in bars:
        for h in (24, 48, 72):
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    # book by coin and year
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d.dropna(subset=["book_return"]).copy()
            dd["coin"] = c; dd["win"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            rows.append(dd)
    D = pd.concat(rows)
    out["book_by_coin"] = D.groupby("coin")["book_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(365)])
    out["book_by_year"] = D.groupby("year")["book_return"].agg(["mean", "count"])
    # market-rise contribution
    mr = []
    for c in bars:
        allr = []
        for w, d in days[c].items():
            allr.extend(d["coin_return"].dropna().values)
        md = np.mean(allr)
        for w, b in bars[c].items():
            b2 = b.copy(); b2["day"] = pd.to_datetime(b2["timestamp"]).dt.floor("D")
            pos = b2.groupby("day")["postRebalance_current_allocation"].mean()
            mr.append(pd.DataFrame({"coin": c, "mkt": pos.values * md}))
    MR = pd.concat(mr)
    out["market_rise_vs_book_mean_daily"] = pd.Series({"book_mean_daily": D.groupby(["day"])["book_return"].mean().mean(),
                                                       "market_rise_part_approx": MR["mkt"].mean()})
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if len(t):
                t = t.copy(); t["coin"] = c; t["year"] = pd.to_datetime(t["entry_time"]).dt.year; T.append(t)
    T = pd.concat(T)
    g = T.groupby(["coin", "side"])["net_profit_loss_percent"]
    out["trades_coin_side"] = g.agg(["count", "mean", "sum"])
    s = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades_concentration"] = pd.Series({"n": len(s), "sum_all": s.sum(), "sum_top10": s.head(10).sum(),
                                             "sum_excl_top10": s.iloc[10:].sum(), "median": s.median(),
                                             "win_share": (s > 0).mean()})
    out["trades_by_year"] = T.groupby("year")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # recompute weekend situation from prices on every weekend and on midweek analog
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; vol = b["volume"].values
            n = len(cl)
            for kind, wd in (("weekend", 6), ("midweek", 2)):
                sel = np.where((ts.dt.weekday.values == wd) & (ts.dt.hour.values == 23))[0]
                for i in sel:
                    if i < 168 or i + 72 >= n: continue
                    m48 = cl[i] / cl[i-48] - 1
                    vr = vol[i-47:i+1].mean() / max(vol[i-167:i-47].mean(), 1e-12)
                    sg = np.sign(m48)
                    r = {"coin": c, "kind": kind, "year": ts.iloc[i].year, "vr": vr,
                         "z": abs(m48) / usual[(c, 48)], "sign": sg, "fc": b["forecast"].iloc[i]}
                    for h in (24, 48, 72):
                        r[f"u{h}"] = sg * (cl[i+h]/cl[i]-1 - drift[(c, h)])
                    recs.append(r)
    R = pd.DataFrame(recs)
    R["heavy"] = R["vr"] > 1
    def tt(x): return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x))})
    out["signed_u48_kind_heavy"] = R.groupby(["kind", "heavy"])["u48"].apply(tt).unstack()
    out["signed_u24_kind_heavy"] = R.groupby(["kind", "heavy"])["u24"].apply(tt).unstack()
    out["signed_u72_kind_heavy"] = R.groupby(["kind", "heavy"])["u72"].apply(tt).unstack()
    W = R[R.kind == "weekend"].copy()
    W["side"] = np.where(W["sign"] > 0, "up", "down")
    out["weekend_u48_side_heavy"] = W.groupby(["side", "heavy"])["u48"].apply(tt).unstack()
    W["zq"] = pd.qcut(W["z"], 3, labels=["small", "mid", "large"])
    W["vq"] = pd.qcut(W["vr"], 4, labels=["v1", "v2", "v3", "v4"])
    out["weekend_u48_by_zq"] = W.groupby("zq")["u48"].apply(tt).unstack()
    out["weekend_u48_by_vq"] = W.groupby("vq")["u48"].apply(tt).unstack()
    H = W[W.heavy]
    out["heavy_u48_by_coin"] = H.groupby("coin")["u48"].apply(tt).unstack()
    out["heavy_u48_by_year"] = H.groupby("year")["u48"].apply(tt).unstack()
    return out
