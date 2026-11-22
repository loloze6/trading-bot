def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda s:int(s[1:]))
    # book daily returns: per window, mean across coins per day
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna()
        g["win"] = w
        chain.append(g.reset_index(drop=True))
    ch = pd.concat(chain, ignore_index=True)
    eq = (1+ch["book"]).cumprod()
    dd = eq/eq.cummax()-1
    ch["dd"] = dd
    out["deepest_fall"] = float(dd.min())
    # per-window book stats
    pw = ch.groupby("win").agg(book_sum=("book","sum"), hold_sum=("hold","sum"), worst_dd=("dd","min"), n=("book","size"))
    pw["book_mean"] = pw.book_sum/pw.n
    out["per_window"] = pw.loc[wins].round(4)
    # yearly-ish stats
    out["book_mean_std"] = pd.Series({"mean":ch.book.mean(),"std":ch.book.std(),"hold_mean":ch.hold.mean(),"hold_std":ch.hold.std(),"corr":ch.book.corr(ch.hold)})
    # trades with context
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            r30 = pd.Series(cl).pct_change(180).values
            r7 = pd.Series(cl).pct_change(42).values
            r1 = pd.Series(cl).pct_change(6).values
            lr = np.log(pd.Series(cl)).diff()
            vol30 = lr.rolling(180).std().values
            vol30_long = lr.rolling(1080, min_periods=360).std().values
            pp = b.get("debug_info.components.panic.post_pipeline_value")
            tr = data["trades"][c].get(w)
            if tr is None or len(tr)==0: continue
            et = pd.to_datetime(tr["entry_time"])
            idx = np.searchsorted(ts.values, et.values)
            idx = np.clip(idx,0,len(b)-1)
            for k,(i) in enumerate(idx):
                i_ = i
                fwd6 = cl[min(i_+6,len(cl)-1)]/cl[i_]-1
                rows.append(dict(coin=c, win=w, net=tr["net_profit_loss_percent"].iloc[k], side=tr["side"].iloc[k],
                    dur=tr["duration_minutes"].iloc[k]/1440, r30=r30[i_], r7=r7[i_], r1=r1[i_], volratio=vol30[i_]/vol30_long[i_] if vol30_long[i_] else np.nan,
                    ef=tr["entry_forecast"].iloc[k], fwd1d=fwd6))
    T = pd.DataFrame(rows)
    out["trades_summary"] = pd.Series({"n":len(T),"mean_net":T.net.mean(),"median":T.net.median(),"share_neg":(T.net<0).mean(),"mean_dur_days":T.dur.mean()})
    for col in ["r30","r7","r1","volratio","ef","fwd1d"]:
        q = pd.qcut(T[col], 4, labels=False, duplicates="drop")
        out["by_"+col] = T.groupby(q).agg(n=("net","size"), x_mean=(col,"mean"), net_mean=("net","mean"), net_med=("net","median"), share_neg=("net",lambda s:(s<0).mean()), worst=("net","min")).round(3)
    # worst trades
    out["worst20_context"] = T.nsmallest(20,"net")[["net","r30","r7","r1","volratio","ef","fwd1d"]].describe().round(3)
    out["by_coin"] = T.groupby("coin").net.agg(["size","mean","min"]).round(2)
    return out
