def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # book daily stats per coin
    rows = []
    allbook = []
    for c in days:
        for w, d in days[c].items():
            b = d["book_return"].dropna(); allbook.append(b)
            rows.append((c, w, b.mean(), b.std(), (d["coin_return"].dropna()).mean()))
    df = pd.DataFrame(rows, columns=["coin","win","book_mean","book_sd","coin_mean"])
    out["book_by_coin"] = df.groupby("coin")[["book_mean","coin_mean"]].mean()
    out["book_by_window"] = df.groupby("win")[["book_mean","coin_mean"]].mean().round(5)
    # per bar gain, position, events forward returns
    ev = []; gains = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.shift(-1)/cl - 1
            pos = b["postRebalance_current_allocation"]
            g = pos*r1
            gains.append(pd.DataFrame({"coin":c,"pos":pos,"g":g,"r1":r1,"fc":b["forecast"],
                                       "fee": b["total_portfolio_value"]-b["postRebalance_total_value"]}))
            f20 = cl.shift(-20)/cl - 1
            f5 = cl.shift(-5)/cl - 1
            ret30 = cl/cl.shift(30)-1
            # events: first bar forecast<0 per 20 span
            last = -999
            for i in range(len(b)):
                if b["forecast"].iloc[i] < 0 and i - last >= 20:
                    last = i
                    ev.append((c, w, b["forecast"].iloc[i], ret30.iloc[i], f5.iloc[i], f20.iloc[i]))
    G = pd.concat(gains)
    G["state"] = np.where(G["pos"]<0,"short",np.where(G["pos"]>0,"long","flat"))
    out["gain_by_state"] = G.groupby("state").agg(n=("g","size"), mean_g=("g","mean"), mean_r1=("r1","mean"))
    E = pd.DataFrame(ev, columns=["coin","win","fc","ret30","f5","f20"]).dropna()
    # coin mean 20-bar grid
    gm = {}
    for c in bars:
        vals=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            vals += list(cl[20::20]/cl[:-20:20][:len(cl[20::20])]-1)
        gm[c]=np.mean(vals)
    E["ex20"] = E["f20"] - E["coin"].map(gm)
    out["events"] = pd.Series({"n":len(E),"mean_ex20":E["ex20"].mean(),"t":stats.ttest_1samp(E["ex20"],0).statistic,
                               "mean_f5":E["f5"].mean(),"slope_ex20_absfc":np.polyfit(E["fc"].abs(),E["ex20"],1)[0]})
    E["q"] = pd.qcut(E["fc"].abs(), 3, labels=["shallow","mid","deep"])
    out["events_by_depth"] = E.groupby("q").agg(n=("ex20","size"), ex20=("ex20","mean"), f5=("f5","mean"), ret30=("ret30","mean"))
    E["q30"] = pd.qcut(E["ret30"], 3, labels=["deepest","mid","mild"])
    out["events_by_ret30"] = E.groupby("q30").agg(n=("ex20","size"), ex20=("ex20","mean"), f5=("f5","mean"))
    out["events_by_coin"] = E.groupby("coin").agg(n=("ex20","size"), ex20=("ex20","mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades"] = pd.Series({"n":len(T),"mean_pl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),
                               "win_share":(T["net_profit_loss_percent"]>0).mean(),"mean_days":T["duration_minutes"].mean()/1440})
    out["share_short_bars"] = (G["pos"]<0).mean()
    return out
