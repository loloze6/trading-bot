import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    hrs = []; daysl = []; ev = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values.astype(float); n = len(b)
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0).values
            nxt = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            gain = pos*nxt
            tv = b["total_portfolio_value"].astype(float).values
            pv = b["postRebalance_total_value"].astype(float).values
            fee = (tv-pv)/tv
            prevpos = b["previous_allocation"].astype(float).fillna(0).values
            turn = np.abs(pos-prevpos)
            hrs.append(pd.DataFrame({"hr": ts.dt.hour.values, "gain": gain, "fee": fee, "turn": turn, "pos": pos}))
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            vol = pd.Series(r1).rolling(168, min_periods=100).std().values
            idx = np.where(ts.dt.hour.values == 20)[0]
            idx = idx[idx+4 < n]
            g4 = np.array([np.nansum(gain[i:i+4]) for i in idx])
            f4 = np.array([np.nansum(fee[i:i+5]) for i in idx])
            ev.append(pd.DataFrame({"coin": c, "vol": vol[idx], "pos": pos[idx], "g4": g4, "fee": f4,
                                    "ret4": cl[idx+4]/cl[idx]-1}))
    h = pd.concat(hrs)
    out["by_hour_bps"] = (h.groupby("hr").agg(gain=("gain","mean"), fee=("fee","mean"), turn=("turn","mean"), pos=("pos","mean"))*np.array([1e4,1e4,1,1])).round(3)
    out["totals_bps_per_bar"] = pd.Series({"gain": h["gain"].mean()*1e4, "fee": h["fee"].mean()*1e4, "turn": h["turn"].mean(), "share_bars_rebal": (h["turn"]>1e-6).mean()})
    e = pd.concat(ev).dropna()
    e["volq"] = e.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["evening_book_by_volq"] = e.groupby("volq").agg(n=("g4","size"), pos=("pos","mean"), ret4_bps=("ret4", lambda x: x.mean()*1e4),
        book_gain_bps=("g4", lambda x: x.mean()*1e4), book_fee_bps=("fee", lambda x: x.mean()*1e4))
    # grind vs jump 72h, t by window halves and coin
    gj = []
    for c, ws in data["bars"].items():
        for wi, (w, b) in enumerate(ws.items()):
            cl = b["close"].values.astype(float); n = len(cl)
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]; ab = np.abs(r1)
            s = pd.Series(ab).rolling(72).sum().values
            past = np.full(n, np.nan); past[72:] = cl[72:]/cl[:-72]-1
            f72 = np.full(n, np.nan); f72[:n-72] = cl[72:]/cl[:-72]-1
            g = np.arange(72, n-72, 72)
            gj.append(pd.DataFrame({"coin": c, "wi": int(w[1:]), "past": past[g], "eff": np.abs(past[g])/s[g], "f72": f72[g]}))
    gj = pd.concat(gj).dropna()
    gj["u"] = gj["f72"] - gj.groupby("coin")["f72"].transform("mean")
    gj["eq"] = gj.groupby("coin")["eff"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    gj["up"] = gj["past"] > 0
    gj["half"] = np.where(gj["wi"] <= 12, "w1-12", "w13-24")
    tt = lambda x: x.mean()/(x.std()/np.sqrt(len(x)))
    out["up_eff_u72"] = gj[gj.up].groupby("eq")["u"].agg(n="size", bps=lambda x: x.mean()*1e4, t=tt)
    out["down_eff_u72"] = gj[~gj.up].groupby("eq")["u"].agg(n="size", bps=lambda x: x.mean()*1e4, t=tt)
    out["up_eff_by_half_bps"] = gj[gj.up].pivot_table(index="eq", columns="half", values="u", aggfunc=lambda x: x.mean()*1e4)
    out["up_eff_by_coin_bps"] = gj[gj.up].pivot_table(index="coin", columns="eq", values="u", aggfunc=lambda x: x.mean()*1e4)
    gj["sgn_eff"] = np.sign(gj["past"])*gj["eff"]
    out["corr_signed_eff_u72"] = pd.Series({"spearman": stats.spearmanr(gj["sgn_eff"], gj["u"])[0], "n": len(gj),
                                            "spearman_past": stats.spearmanr(gj["past"], gj["u"])[0]})
    return out
