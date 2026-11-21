import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    # trades with entry state
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            t = data["trades"][c].get(w)
            if t is None or len(t) == 0: continue
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                idx = np.searchsorted(ts.values, np.datetime64(et.tz_localize(None) if et.tzinfo else et), side="right") - 1
                if idx < 0: continue
                p10 = cl[idx]/cl[idx-10]-1 if idx >= 10 else np.nan
                p26 = cl[idx]/cl[idx-26]-1 if idx >= 26 else np.nan
                lr = np.diff(np.log(cl[max(0,idx-30):idx+1]))
                vol = lr.std() if len(lr) > 10 else np.nan
                rows.append(dict(coin=c, pnl=r["net_profit_loss_percent"], side=r["side"],
                                 p10=p10, p26=p26, vol=vol, ef=r["entry_forecast"],
                                 dur=r["duration_minutes"]/1440))
    d = pd.DataFrame(rows)
    out["n_trades"] = len(d)
    out["side"] = d.groupby("side")["pnl"].agg(["mean","count"])
    out["dur"] = d["dur"].describe()
    for col in ["p10","p26","vol","ef"]:
        dd = d.dropna(subset=[col])
        q = pd.qcut(dd[col].rank(method="first"), 4, labels=False)
        g = dd.groupby(q).agg(x=(col,"mean"), pnl=("pnl","mean"), med=("pnl","median"), n=("pnl","size"))
        out["trq_"+col] = g
    # book daily: position, timing vs market
    br = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].values
            cl = b["close"].values
            g = pos[:-1] * (cl[1:]/cl[:-1]-1)
            p10 = pd.Series(cl).pct_change(10).values[:-1]
            p26 = pd.Series(cl).pct_change(26).values[:-1]
            br.append(pd.DataFrame(dict(coin=c, win=w, pos=pos[:-1], g=g, r=cl[1:]/cl[:-1]-1, p10=p10, p26=p26)))
    br = pd.concat(br)
    act = br[br["pos"] != 0].copy()
    out["active_share"] = float(len(act)/len(br))
    out["mean_pos_active"] = float(act["pos"].mean())
    mr = br.groupby("coin")["r"].mean()
    act["mkt"] = act["pos"] * act["coin"].map(mr)
    out["gain_split_bps"] = pd.Series({"gain": act["g"].mean()*1e4, "market": act["mkt"].mean()*1e4,
                                       "timing": (act["g"]-act["mkt"]).mean()*1e4})
    for col in ["p10","p26"]:
        dd = act.dropna(subset=[col])
        q = pd.qcut(dd[col].rank(method="first"), 5, labels=False)
        out["daygain_by_"+col] = dd.groupby(q).agg(x=(col,"mean"), g_bps=("g", lambda s: s.mean()*1e4),
                                                    t=("g", lambda s: s.mean()/s.std()*np.sqrt(len(s))), n=("g","size"))
    # big losing days: share of loss from top 5% worst days
    srt = act["g"].sort_values()
    k = int(len(srt)*0.05)
    out["loss_concentration"] = pd.Series({"sum_all": srt.sum(), "sum_worst5pct": srt.iloc[:k].sum(),
                                           "sum_rest": srt.iloc[k:].sum()})
    worst = act.loc[act["g"] <= srt.iloc[k]]
    out["worst_days_state"] = pd.Series({"p10_mean": worst["p10"].mean(), "p26_mean": worst["p26"].mean(),
                                         "all_p10": act["p10"].mean(), "all_p26": act["p26"].mean(),
                                         "share_p10_pos": (worst["p10"]>0).mean(), "all_share_p10_pos": (act["p10"]>0).mean()})
    return out
