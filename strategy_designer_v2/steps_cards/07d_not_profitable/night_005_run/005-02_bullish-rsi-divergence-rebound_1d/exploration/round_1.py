import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # Book daily returns
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    # allocation at end of day from bars
    alloc = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            bb = b[["timestamp","postRebalance_current_allocation","forecast","close","regime"]].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            a = bb.groupby("day").last().reset_index()
            a["coin"]=coin; a["w"]=w
            alloc.append(a[["day","coin","w","postRebalance_current_allocation"]])
    A = pd.concat(alloc)
    D["day"] = pd.to_datetime(D["day"])
    D = D.merge(A, on=["day","coin","w"], how="left")
    D["pos_prev"] = D.groupby(["coin","w"])["postRebalance_current_allocation"].shift(1)
    D["held"] = D["pos_prev"].abs() > 1e-6
    br = D.dropna(subset=["book_return"])
    out["book_summary"] = pd.DataFrame({
        "n_days":[len(br)], "share_held":[br["held"].mean()],
        "mean_book":[br["book_return"].mean()],
        "mean_book_held_days":[br.loc[br.held,"book_return"].mean()],
        "mean_coin_held_days":[br.loc[br.held,"coin_return"].mean()],
        "mean_coin_all":[br["coin_return"].mean()],
        "mean_pos_held":[br.loc[br.held,"pos_prev"].mean()]})
    out["book_by_coin"] = br.groupby("coin").apply(lambda g: pd.Series({
        "mean_book":g.book_return.mean(),"sharpe":g.book_return.mean()/g.book_return.std()*np.sqrt(365),
        "held_days":g.held.sum(),"coin_ret_held":g.loc[g.held,"coin_return"].mean()}))
    # Forward returns on new-low bars, grid per window
    recs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            c = b["close"].reset_index(drop=True)
            n = len(c)
            prior_min = c.shift(1).rolling(30, min_periods=30).min()
            newlow = c < prior_min
            depth = c/prior_min - 1
            r30 = c/c.shift(30)-1
            r90 = c/c.shift(90)-1
            ret1 = c.pct_change()
            vol20 = ret1.rolling(20).std()
            dd_hi = c/c.rolling(90,min_periods=30).max()-1
            fwd10 = c.shift(-10)/c - 1
            fwd3 = c.shift(-3)/c - 1
            fc = b["forecast"].reset_index(drop=True)
            last = -999
            for i in range(n):
                if newlow.iloc[i] and not np.isnan(fwd10.iloc[i]) and i - last > 10:
                    recs.append(dict(coin=coin,w=w,fc=fc.iloc[i],depth=depth.iloc[i],r30=r30.iloc[i],r90=r90.iloc[i],
                                     vol=vol20.iloc[i],ddhi=dd_hi.iloc[i],f10=fwd10.iloc[i],f3=fwd3.iloc[i]))
                    last = i
    R = pd.DataFrame(recs)
    R["div"] = R.fc > 0
    out["newlow_by_div"] = R.groupby("div").agg(n=("f10","size"),f10=("f10","mean"),f3=("f10","median"),
                                                 depth=("depth","mean"),r30=("r30","mean"),vol=("vol","mean"))
    def tgrp(g):
        return pd.Series({"n":len(g),"f10":g.f10.mean(),"t":stats.ttest_1samp(g.f10,0).statistic if len(g)>2 else np.nan})
    for col in ["r30","r90","depth","vol","ddhi"]:
        s = R.dropna(subset=[col])
        s = s.assign(q=pd.qcut(s[col],3,labels=["lo","mid","hi"]))
        out["f10_by_"+col] = s.groupby(["q","div"]).apply(tgrp).unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"] = T.groupby("coin").agg(n=("side","size"),pl=("profit_loss_percent","mean"),
                                        net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda x:x.mean()/1440),
                                        win=("profit_loss_percent",lambda x:(x>0).mean()))
    # book by year
    br = br.assign(year=br.day.dt.year)
    out["book_by_year"] = br.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),held=("held","mean"))
    return out
