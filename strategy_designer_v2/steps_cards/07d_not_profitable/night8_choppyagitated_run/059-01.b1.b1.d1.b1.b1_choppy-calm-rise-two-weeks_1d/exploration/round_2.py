def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # trades with entry state recomputed from prices
    trs = []
    for c in trades:
        for w, t in trades[c].items():
            if c not in bars or w not in bars[c] or len(t) == 0:
                continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = pd.Series(b["close"].values)
            r7 = cl.pct_change(7)
            sc = r7 / r7.abs().rolling(30).mean()
            r60 = cl.pct_change(60)
            r1 = cl.pct_change(1)
            vol30 = r1.rolling(30).std()
            for _, x in t.iterrows():
                et = pd.to_datetime(x["entry_time"])
                idx = ts.searchsorted(et)
                if idx >= len(b):
                    idx = len(b) - 1
                xt = pd.to_datetime(x["exit_time"]); jdx = min(ts.searchsorted(xt), len(b) - 1)
                # path: return after 7 days
                p7 = cl.iloc[min(idx + 7, len(b) - 1)] / cl.iloc[idx] - 1
                # max adverse during trade
                seg = cl.iloc[idx:jdx + 1]
                mae = seg.min() / cl.iloc[idx] - 1
                trs.append(dict(coin=c, w=w, net=x["net_profit_loss_percent"], fc=x["entry_forecast"],
                                sc=sc.iloc[idx], r7=r7.iloc[idx], r60=r60.iloc[idx], vol30=vol30.iloc[idx],
                                p7=p7, mae=mae, dur=x["duration_minutes"] / 1440,
                                alloc=b["postRebalance_current_allocation"].iloc[idx]))
    tr = pd.DataFrame(trs)
    out["n_trades"] = len(tr)
    tr["scb"] = pd.cut(tr.sc, [-10, 0, 0.5, 1.0, 1.5, 10])
    out["trades_by_rawsc"] = tr.groupby("scb").agg(n=("net", "size"), net=("net", "mean"), med=("net", "median"),
                                                   win=("net", lambda x: (x > 0).mean()), fc=("fc", "mean"))
    tr["r60b"] = pd.cut(tr.r60, [-5, -0.10, -0.03, 0.03, 0.10, 5])
    out["trades_by_r60"] = tr.groupby("r60b").agg(n=("net", "size"), net=("net", "mean"), win=("net", lambda x: (x > 0).mean()))
    tr["p7b"] = pd.cut(tr.p7, [-5, -0.10, -0.03, 0.03, 0.10, 5])
    out["trades_by_first7"] = tr.groupby("p7b").agg(n=("net", "size"), net=("net", "mean"), p7=("p7", "mean"))
    tr["durb"] = pd.cut(tr.dur, [0, 10, 15, 20, 30, 1000])
    out["trades_by_dur"] = tr.groupby("durb").agg(n=("net", "size"), net=("net", "mean"))
    out["trades_by_window"] = tr.groupby("w").agg(n=("net", "size"), net=("net", "mean"), sc=("sc", "mean"),
                                                  alloc=("alloc", "mean"))
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("net", "size"), net=("net", "mean"), sumnet=("net", "sum"))

    # book days in w14-w16 by coin contribution
    br = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["w"] = w; br.append(x)
    br = pd.concat(br)
    ncoins = br.groupby(["w", "day"])["coin"].transform("size")
    br["contrib"] = br["book_return"] / ncoins
    out["contrib_w14_w17_by_coin"] = br[br.w.isin(["w14", "w15", "w16", "w17"])].groupby(["w", "coin"])["contrib"].sum().unstack().round(4)

    # grid 14-bar cases in profile: raw scaled rise bins (forecast>0 or not), and same bins outside profile
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values)
            r7 = cl.pct_change(7); sc = r7 / r7.abs().rolling(30).mean()
            prof = (b["regime"] == "unknown").values
            for h in (14, 21):
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=c, h=h, ret=cl.iloc[i + h] / cl.iloc[i] - 1, sc=sc.iloc[i], prof=prof[i],
                                     day=pd.to_datetime(b["timestamp"].iloc[i]).floor("D")))
    g = pd.DataFrame(rows)
    g["um"] = g.ret - g.groupby(["coin", "h"]).ret.transform("mean")
    g["scb"] = pd.cut(g.sc, [-10, 0, 0.5, 1.0, 10])
    def tday(x):
        d = x.groupby("day")["um"].sum()
        return d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan
    res = g.groupby(["h", "prof", "scb"]).apply(lambda x: pd.Series(dict(n=len(x), um=x.um.mean(), tot=x.ret.mean(), t=tday(x))))
    out["grid_by_rawsc"] = res
    return out
