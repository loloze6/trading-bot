def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; drows = []; trows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            c = b["close"].values
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            pos = b["postRebalance_current_allocation"].fillna(0).values
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            ret72 = pd.Series(c).pct_change(72).values
            ret24 = pd.Series(c).pct_change(24).values
            fwd72 = np.r_[c[72:]/c[:-72]-1, [np.nan]*72] if len(c)>72 else np.full(len(c),np.nan)
            absr = pd.Series(np.abs(np.r_[np.nan, c[1:]/c[:-1]-1]))
            er = np.abs(ret72)/ (absr.rolling(72).sum().values+1e-12)
            vol = b["volume"].values
            vr = pd.Series(vol).rolling(72).max()/pd.Series(vol).rolling(72).mean()
            hr = pd.Series(np.abs(np.r_[np.nan, c[1:]/c[:-1]-1])).rolling(72).max()/(absr.rolling(72).sum()+1e-12)
            df = pd.DataFrame({"coin":coin,"w":w,"pos":pos,"r1":r1,"g":pos*r1,"fee":fee,
                               "fc":b["forecast"].values,"ret72":ret72,"ret24":ret24,"fwd72":fwd72,
                               "er":er,"vr":vr.values,"hr":hr.values,"i":np.arange(len(c))})
            rows.append(df)
            d = data["days"][coin][w]
            drows.append(pd.DataFrame({"coin":coin,"w":w,"br":d["book_return"].values,"cr":d["coin_return"].values}))
        for w,t in data["trades"][coin].items():
            trows.append(t.assign(coin=coin,w=w))
    A = pd.concat(rows); D = pd.concat(drows); T = pd.concat(trows)
    # book daily
    bd = D.groupby(["w","coin"]).size()
    out["book_daily_mean"] = D["br"].mean(); out["coin_daily_mean"] = D["cr"].mean()
    # per-bar decomposition
    act = A[A.pos!=0]
    out["share_bars_long"] = (A.pos>0).mean()
    out["mean_pos_when_active"] = act.pos.mean()
    out["sum_gross_per_bar_mean"] = A.g.mean()
    out["fee_per_bar_mean"] = A.fee.mean()
    cm = A.groupby("coin").r1.mean()
    A["mkt"] = A.pos*A.coin.map(cm)
    out["market_part_per_bar"] = A.mkt.mean()
    out["timing_part_per_bar"] = (A.g-A.mkt).mean()
    out["gross_x24_per_day"] = A.g.mean()*24; out["fee_x24_per_day"] = A.fee.mean()*24
    # fees per coin
    out["by_coin"] = A.groupby("coin").agg(gross=("g","mean"),fee=("fee","mean"),long=("pos",lambda x:(x>0).mean()))*24
    # trades
    out["trades"] = pd.Series({"n":len(T),"mean_dur_h":T.duration_minutes.mean()/60,"median_dur_h":T.duration_minutes.median()/60,
        "mean_pl":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean()})
    # grid analysis: fwd72 excess by forecast bucket and by features, among active
    G = A[(A.i%72==0)].dropna(subset=["fwd72"])
    m72 = G.groupby("coin").fwd72.mean()
    G["ex"] = G.fwd72-G.coin.map(m72)
    Ga = G[G.fc>0].copy()
    Ga["fcq"] = pd.qcut(Ga.fc,4,labels=False,duplicates="drop")
    out["grid_by_fc_q"] = Ga.groupby("fcq").agg(n=("ex","size"),ex=("ex","mean"),fc=("fc","mean"))
    Ga["r72q"] = pd.qcut(Ga.ret72,4,labels=False)
    out["grid_by_ret72_q"] = Ga.groupby("r72q").agg(n=("ex","size"),ex=("ex","mean"),r72=("ret72","mean"))
    Ga["hrq"] = pd.qcut(Ga.hr,4,labels=False)
    out["grid_by_maxhour_share_q"] = Ga.groupby("hrq").agg(n=("ex","size"),ex=("ex","mean"),hr=("hr","mean"))
    out["grid_flat_vs_active"] = G.assign(a=G.fc>0).groupby("a").agg(n=("ex","size"),ex=("ex","mean"))
    # per-bar gain by fc quartile hourly
    act = A[A.fc>0].copy()
    act["fcq"] = pd.qcut(act.fc,4,labels=False,duplicates="drop")
    out["hourly_gain_by_fcq_x1e4"] = act.groupby("fcq").agg(g=("g","mean"),fee=("fee","mean"),r1=("r1","mean"))*1e4
    return out
