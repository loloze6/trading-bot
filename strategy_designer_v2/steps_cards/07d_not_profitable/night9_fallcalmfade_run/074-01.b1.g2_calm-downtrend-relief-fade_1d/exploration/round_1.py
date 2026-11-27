def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r = pd.Series(c).pct_change()
            dn = (r < 0).astype(int)
            run = np.zeros(len(b), int)
            for i in range(1, len(b)):
                run[i] = run[i-1] + 1 if r.iloc[i] < 0 else 0
            sd30 = r.rolling(30).std().shift(1)
            ret60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            ret5 = pd.Series(c) / pd.Series(c).shift(5) - 1
            for i in range(1, len(b) - 1):
                if b["forecast"].iloc[i] < 0:
                    rl = run[i-1]
                    runloss = c[i-1] / c[i-1-rl] - 1 if i-1-rl >= 0 else np.nan
                    f = lambda h: c[i+h] / c[i] - 1 if i + h < len(b) else np.nan
                    rows.append(dict(coin=coin, w=w, i=i, run=rl, runloss=runloss,
                        upday=r.iloc[i], sd=sd30.iloc[i], ret60=ret60.iloc[i], ret5=ret5.iloc[i],
                        alloc=b["postRebalance_current_allocation"].iloc[i],
                        fc=b["forecast"].iloc[i], depth=b["debug_info.components.depth.last_history_value"].iloc[i],
                        n1=f(1), n2=f(2), n3=f(3), n5=f(5), day=str(b["timestamp"].iloc[i])[:10],
                        year=str(b["timestamp"].iloc[i])[:4]))
    d = pd.DataFrame(rows)
    d["s1"] = -d["n1"]; d["s2"] = -d["n2"]; d["s3"] = -d["n3"]; d["s5"] = -d["n5"]
    d["upsd"] = d["upday"] / d["sd"]
    d["gain"] = d["s1"] * d["alloc"].abs()
    def summ(g):
        return pd.Series(dict(n=len(g), s1=g.s1.mean(), t1=stats.ttest_1samp(g.s1.dropna(), 0)[0] if len(g) > 2 else np.nan,
                              s2=g.s2.mean(), s3=g.s3.mean(), s5=g.s5.mean(), alloc=g.alloc.abs().mean(), gain=g.gain.mean()))
    out["all"] = summ(d).to_frame().T
    out["by_run"] = d.groupby(d.run.clip(upper=5)).apply(summ)
    out["by_depth_q"] = d.groupby(pd.qcut(d.depth, 4, duplicates="drop")).apply(summ)
    out["by_upday_sd_q"] = d.groupby(pd.qcut(d.upsd, 4)).apply(summ)
    out["by_ret60_q"] = d.groupby(pd.qcut(d.ret60, 4)).apply(summ)
    out["by_ret5_q"] = d.groupby(pd.qcut(d.ret5, 4)).apply(summ)
    out["by_fc_q"] = d.groupby(pd.qcut(d.fc, 4, duplicates="drop")).apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    # book daily
    bk = []
    for w in sorted(set(x for ws in data["days"].values() for x in ws), key=lambda s: int(s[1:])):
        frames = []
        for coin, ws in data["days"].items():
            if w in ws:
                frames.append(ws[w].set_index("day")[["book_return", "coin_return"]].add_suffix("_" + coin))
        f = pd.concat(frames, axis=1)
        br = f[[x for x in f if x.startswith("book_return")]].mean(axis=1)
        cr = f[[x for x in f if x.startswith("coin_return")]].mean(axis=1)
        bk.append(pd.DataFrame(dict(w=w, br=br.values, cr=cr.values)))
    bk = pd.concat(bk, ignore_index=True).dropna()
    v = (1 + bk.br).cumprod(); dd = v / v.cummax() - 1
    trough = dd.idxmin(); peak = v[:trough + 1].idxmax()
    out["book"] = pd.Series(dict(days=len(bk), mean=bk.br.mean(), sd=bk.br.std(), sharpe=bk.br.mean()/bk.br.std()*np.sqrt(365),
        hold_sharpe=bk.cr.mean()/bk.cr.std()*np.sqrt(365), maxdd=dd.min(), dd_len=trough - peak,
        dd_window_start=bk.w[peak], dd_window_end=bk.w[trough], yearly=v.iloc[-1]**(365/len(bk))-1))
    out["book_by_window"] = bk.groupby("w").agg(sumret=("br", "sum"), worst=("br", "min"), nz=("br", lambda x: (x != 0).sum()))
    # trades
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()], ignore_index=True)
    out["trades"] = pd.Series(dict(n=len(tr), gross=tr.profit_loss_percent.mean(), net=tr.net_profit_loss_percent.mean(),
        win=(tr.net_profit_loss_percent > 0).mean(), dur_days=tr.duration_minutes.mean()/1440,
        worst=tr.net_profit_loss_percent.min(), q05=tr.net_profit_loss_percent.quantile(.05)))
    # losing tail of cases
    out["tail"] = pd.Series(dict(share_s1_lt_m5pct=(d.s1 < -0.05).mean(), sum_loss_tail=d.s1[d.s1 < -0.05].sum(), sum_all=d.s1.sum(),
                                 n_loss_days_gt5=(d.s1 < -0.05).sum()))
    return out
