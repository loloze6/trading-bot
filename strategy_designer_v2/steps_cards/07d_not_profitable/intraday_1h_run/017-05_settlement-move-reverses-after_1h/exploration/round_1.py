def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades: gross vs net, commission
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                d = t[["profit_loss_percent","net_profit_loss_percent","total_commission","duration_minutes","entry_forecast"]].copy()
                d["coin"] = c; tr.append(d)
    tr = pd.concat(tr)
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        dur=("duration_minutes","median"))
    out["trades_all"] = pd.Series({"n":len(tr),"gross_mean":tr.profit_loss_percent.mean(),
        "net_mean":tr.net_profit_loss_percent.mean(),
        "gross_t":stats.ttest_1samp(tr.profit_loss_percent.dropna(),0).statistic,
        "dur_mean":tr.duration_minutes.mean()})
    # settlement bars: forward returns at 1,2,3,4 bars, signed by sign of forecast
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b.close.values
            f = b.forecast.values
            pos = b.postRebalance_current_allocation.values
            n = len(b)
            idx = np.where((b.regime=="mean_reversion") & (b.forecast!=0))[0]
            for i in idx:
                r = {"coin":c,"f":f[i],"pos":pos[i],"prev":b.previous_allocation.values[i]}
                for h in (1,2,3,4):
                    r[f"r{h}"] = cl[i+h]/cl[i]-1 if i+h<n else np.nan
                r["pre2"] = cl[i]/cl[i-2]-1 if i>=2 else np.nan
                r["tc"] = (b.total_portfolio_value.values[i]-b.postRebalance_total_value.values[i])/b.total_portfolio_value.values[i]
                r["gain1"] = pos[i]*r["r1"]
                r["hour"] = pd.Timestamp(b.timestamp.values[i]).hour
                rows.append(r)
    s = pd.DataFrame(rows)
    s["sg"] = np.sign(s.f)
    for h in (1,2,3,4):
        s[f"s{h}"] = s.sg*s[f"r{h}"]
    out["signed_fwd_bps"] = (s[["s1","s2","s3","s4"]].mean()*1e4).to_frame("mean_bps").assign(
        t=[stats.ttest_1samp(s[k].dropna(),0).statistic for k in ["s1","s2","s3","s4"]])
    out["cost_vs_gain_bps"] = pd.Series({"n":len(s),"mean_abs_pos":s.pos.abs().mean(),
        "fee_per_settle_bps":s.tc.mean()*1e4,"gain1_bps":s.gain1.mean()*1e4,
        "abs_pre2_bps":s.pre2.abs().mean()*1e4})
    s["q"] = pd.qcut(s.f.abs(), 5, labels=False)
    out["by_absf_quintile_bps"] = s.groupby("q").agg(n=("s1","size"),absf=("f",lambda x: x.abs().mean()),
        s1=("s1",lambda x: x.mean()*1e4), s2=("s2",lambda x:x.mean()*1e4), absmove=("pre2",lambda x:x.abs().mean()*1e4))
    out["by_hour_bps"] = s.groupby("hour").agg(n=("s1","size"),s1=("s1",lambda x:x.mean()*1e4),s2=("s2",lambda x:x.mean()*1e4))
    out["by_coin_bps"] = s.groupby("coin").agg(s1=("s1",lambda x:x.mean()*1e4),s2=("s2",lambda x:x.mean()*1e4),fee=("tc",lambda x:x.mean()*1e4))
    # book daily
    d = pd.concat([x for ws in data["days"].values() for x in ws.values()])
    out["book_daily"] = pd.Series({"mean":d.book_return.mean(),"coin_mean":d.coin_return.mean()})
    return out
