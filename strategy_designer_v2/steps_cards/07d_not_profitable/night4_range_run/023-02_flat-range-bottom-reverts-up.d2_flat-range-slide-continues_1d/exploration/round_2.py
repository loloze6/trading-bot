def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    grid = []; daily = []; tr = []
    for c in bars:
        cr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = cr.mean()
        g5 = []
        for w in bars[c]:
            cl = bars[c][w]["close"].values
            idx = np.arange(0, len(cl)-5, 5)
            g5 += list(cl[idx+5]/cl[idx]-1)
        d5 = np.mean(g5)
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            alloc = b["postRebalance_current_allocation"].fillna(0)
            nxt = cl.shift(-1)/cl-1
            r60 = cl/cl.shift(60)-1
            fwd = cl.shift(-5)/cl-1
            # bar-level book gain by forecast bucket held
            pv = b["postRebalance_total_value"]
            bret = pv.shift(-1)/pv-1  # includes next bar's fee
            for i in range(len(b)-1):
                daily.append(dict(f=b.loc[i,"forecast"], alloc=alloc[i], gain=alloc[i]*nxt[i], bret=bret[i], r60=r60[i]))
            for i in range(0, len(b)-5, 5):
                if b.loc[i,"regime"]=="mean_reversion" and b.loc[i,"forecast"]<0:
                    grid.append(dict(coin=c, f=b.loc[i,"forecast"], ex=fwd[i]-d5, fwd=fwd[i], r60=r60[i]))
            t = trades[c][w]
            if len(t):
                tr.append(t[["side","profit_loss_percent","net_profit_loss_percent","entry_forecast"]].assign(coin=c))
    g = pd.DataFrame(grid).dropna()
    def tt(x):
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    g["fb"] = pd.cut(g["f"], [-21,-15,-10,-5,0], labels=["<-15","-15..-10","-10..-5","-5..0"])
    out["ex_by_f_t"] = g.groupby("fb")["ex"].apply(tt).unstack()
    g["r60b"] = pd.cut(g["r60"], [-1,-0.2,-0.05,0.05,0.2,100], labels=["<-20%","-20..-5","-5..5","5..20",">20%"])
    out["ex_by_r60_t"] = g.groupby("r60b")["ex"].apply(tt).unstack()
    out["ex_by_r60_and_f"] = g.groupby(["r60b", g["f"]<-10])["ex"].mean().unstack()
    out["r60_slope"] = pd.Series(dict(zip(["slope","int","r","p","se"], stats.linregress(g["r60"].clip(-1,1), g["ex"]))))
    dd = pd.DataFrame(daily).dropna(subset=["gain"])
    dd = dd[dd.alloc!=0]
    dd["fb"] = pd.cut(dd["f"], [-21,-10,-5,-0.001,0.001,21], labels=["<-10","-10..-5","-5..0","0","pos"])
    out["held_gain_by_f"] = dd.groupby("fb").agg(n=("gain","size"), gain=("gain","mean"), bret=("bret","mean"), alloc=("alloc","mean"))
    T = pd.concat(tr)
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    T["eb"] = pd.cut(T["entry_forecast"], [-21,-10,-5,-0.001,21])
    out["trades_by_entry_f"] = T.groupby("eb").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    return out
