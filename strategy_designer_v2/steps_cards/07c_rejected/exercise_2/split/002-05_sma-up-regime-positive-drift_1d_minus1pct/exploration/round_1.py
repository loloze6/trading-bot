import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    allb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().sort_values("timestamp")
            b["ret"] = b["close"].pct_change().shift(-1)
            b["oc"] = (b["close"]/b["open"]-1).shift(-1)
            b["gap"] = (b["open"].shift(-1)/b["close"]-1)
            b["spread"] = b["debug_info.components.sma_cross_spread.last_history_value"]
            b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["inst"] = b["forecast"] > 0
            b["rawpos"] = b["spread"] > 0
            allb.append(b.dropna(subset=["ret"]))
    a = pd.concat(allb)
    def summ(g):
        i = g[g.inst]; o = g[~g.inst]
        t = stats.ttest_ind(i.ret, o.ret, equal_var=False).statistic if len(i)>2 and len(o)>2 else np.nan
        return pd.Series({"n_in": len(i), "n_out": len(o), "mean_in": i.ret.mean(), "mean_out": o.ret.mean(),
                          "up_in": (i.ret>0).mean(), "up_out": (o.ret>0).mean(), "t": t,
                          "rawpos_share": g.rawpos.mean()})
    out["by_window"] = a.groupby("win").apply(summ)
    out["by_year"] = a.groupby("year").apply(summ)
    out["total"] = summ(a)
    a["fbin"] = pd.cut(a.forecast, [-0.1, 0, 5, 10, 15, 20.1])
    out["by_forecast_bin"] = a.groupby("fbin").agg(n=("ret","size"), mean=("ret","mean"), med=("ret","median"),
                                                  up=("ret", lambda x:(x>0).mean()), sd=("ret","std"))
    out["raw_vs_clip"] = a.groupby(["rawpos","inst"]).agg(n=("ret","size"), mean=("ret","mean"), up=("ret",lambda x:(x>0).mean()))
    out["decomp_gap_oc"] = a.groupby("inst")[["gap","oc","ret"]].mean()
    out["ret_quantiles"] = a.groupby("inst")["ret"].quantile([0.05,0.25,0.5,0.75,0.95]).unstack()
    out["by_weekday"] = a.groupby(["wd","inst"]).ret.mean().unstack()
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["win"]=w; tr.append(t)
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("win").agg(n=("side","size"), pl=("profit_loss_percent","mean"),
                                             net=("net_profit_loss_percent","sum"), dur_d=("duration_minutes", lambda x: x.mean()/1440))
    dd = pd.concat([d.assign(win=w) for c,ws in data["days"].items() for w,d in ws.items()])
    out["days"] = dd.groupby("win").agg(book=("book_return", lambda x:(1+x.fillna(0)).prod()-1),
                                        coin=("coin_return", lambda x:(1+x.fillna(0)).prod()-1))
    return out
