import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H_list = [2, 6, 24]
    rows = []
    book = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = pd.Series(c).pct_change()
            mabs = r1.abs().rolling(720, min_periods=200).mean()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=200).mean()
            z = r1 / mabs
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            gross = alloc[:-1] * (c[1:] / c[:-1] - 1)
            v = b["postRebalance_total_value"].values
            tv = b["total_portfolio_value"].values
            fee = (tv[1:] - v[1:]) / tv[1:]
            book.append(dict(coin=coin, w=w, gross=np.nansum(gross), fee=np.nansum(fee),
                             turnover=np.nansum(np.abs(b["allocation_change"].fillna(0).values)), n=len(b)))
            for H in H_list:
                idx = np.arange(0, len(b) - H, H)
                fr = c[idx + H] / c[idx] - 1
                rows.append(pd.DataFrame(dict(coin=coin, w=w, H=H, z=z.values[idx], vr=vr.values[idx],
                                              fr=fr, alloc=alloc[idx])))
    d = pd.concat(rows)
    bk = pd.DataFrame(book)
    out["book gross vs fee (sum of bar returns, all coin-windows)"] = bk[["gross", "fee", "turnover", "n"]].sum()
    res = []
    for H in H_list:
        x = d[d.H == H].dropna(subset=["z", "vr", "fr"])
        drift = x.groupby("coin")["fr"].transform("mean")
        x = x.assign(ex=x.fr - drift)
        x["zb"] = pd.cut(x.z, [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
        x["vb"] = pd.cut(x.vr, [0, 0.5, 1.5, 3, np.inf])
        for (zb, vb), g in x.groupby(["zb", "vb"], observed=True):
            if len(g) < 30: continue
            res.append(dict(H=H, zb=str(zb), vb=str(vb), n=len(g), mean_ex_pct=100 * g.ex.mean(),
                            t=g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                            usual_pct=100 * x.fr.std()))
    res = pd.DataFrame(res)
    out["excess fwd return by hour z and vol ratio, H=6"] = res[res.H == 6].drop(columns="H")
    out["H=24"] = res[res.H == 24].drop(columns="H")
    out["H=2 extremes"] = res[(res.H == 2) & (~res.zb.isin(["(-1.5, 1.5]"]))].drop(columns="H")
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    t = pd.concat(tr)
    out["trades"] = pd.Series(dict(n=len(t), mean_pl=t.profit_loss_percent.mean(),
                                   mean_net=t.net_profit_loss_percent.mean(),
                                   med_dur_h=t.duration_minutes.median() / 60,
                                   share_short=(t.side == "SHORT").mean()))
    return out
