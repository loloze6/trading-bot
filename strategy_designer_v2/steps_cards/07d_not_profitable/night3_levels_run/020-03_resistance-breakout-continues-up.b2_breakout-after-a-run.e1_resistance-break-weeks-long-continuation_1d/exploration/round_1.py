def explore(data):
    import pandas as pd, numpy as np
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily returns: mean of coins per day, per window
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().dropna().reset_index()
        g["w"]=w
        chain.append(g)
    ch = pd.concat(chain, ignore_index=True)
    ch["idx"]=range(len(ch))
    v = (1+ch.book_return).cumprod(); peak=v.cummax(); dd=v/peak-1
    ch["dd"]=dd
    out["max_dd"]=float(dd.min())
    out["years"]=len(ch)/365
    out["yearly"]=float(v.iloc[-1]**(365/len(ch))-1)
    hv=(1+ch.coin_return).cumprod(); out["hold_maxdd"]=float((hv/hv.cummax()-1).min())
    # dd per window: return per window and worst in-window drawdown
    pw = ch.groupby("w").agg(book=("book_return",lambda x:(1+x).prod()-1), coin=("coin_return",lambda x:(1+x).prod()-1))
    pw["min_dd_level"]=ch.groupby("w")["dd"].min()
    out["per_window"]=pw.reindex(wins).round(3)
    # trades by features at entry
    rows=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].copy(); b["ts"]=pd.to_datetime(b.timestamp)
            cl=b.close
            b["r20"]=cl/cl.shift(20)-1; b["r60"]=cl/cl.shift(60)-1
            b["vol20"]=np.log(cl).diff().rolling(20).std()*np.sqrt(365)
            b["hi60"]=cl/cl.rolling(60).max()-1
            b["f20"]=cl.shift(-20)/cl-1
            t=trades[c].get(w)
            if t is None or len(t)==0: continue
            t=t.copy(); t["et"]=pd.to_datetime(t.entry_time)
            m=pd.merge_asof(t.sort_values("et"), b[["ts","r20","r60","vol20","hi60","postRebalance_current_allocation"]].sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            m["coin"]=c; m["w"]=w; rows.append(m)
    T=pd.concat(rows, ignore_index=True)
    T=T[T.side=="LONG"]
    out["n_trades"]=len(T)
    out["trade_pnl"]=T.net_profit_loss_percent.describe().round(3)
    for k in ["r20","r60","vol20","hi60"]:
        q=pd.qcut(T[k],3,duplicates="drop")
        out["by_"+k]=T.groupby(q).net_profit_loss_percent.agg(["count","mean","median",lambda x:(x<0).mean()]).round(3)
    out["by_coin"]=T.groupby("coin").net_profit_loss_percent.agg(["count","mean","sum"]).round(2)
    out["worst10_feats"]=T.nsmallest(30,"net_profit_loss_percent")[["r20","r60","vol20","hi60","net_profit_loss_percent"]].mean().round(3)
    out["all_feats"]=T[["r20","r60","vol20","hi60","net_profit_loss_percent"]].mean().round(3)
    return out
