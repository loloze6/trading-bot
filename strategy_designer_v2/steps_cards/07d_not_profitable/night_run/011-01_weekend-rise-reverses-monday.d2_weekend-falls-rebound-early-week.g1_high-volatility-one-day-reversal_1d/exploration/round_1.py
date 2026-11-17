def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; dayrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            b["ret"]=r
            b["nxt"]=c.shift(-1)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["prev"]=b["previous_allocation"]
            b["gross"]=b["pos"]*b["nxt"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["turn"]=(b["pos"]-b["prev"]).abs()
            b["sd20"]=r.rolling(20).std()
            b["mad60"]=r.abs().shift(1).rolling(60,min_periods=20).mean()
            b["volratio"]=b["sd20"]/(r.abs().rolling(120,min_periods=60).mean())
            b["z"]=r/b["sd20"]
            b["ret5"]=c/c.shift(5)-1
            b["ret20"]=c/c.shift(20)-1
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"]=coin; b["w"]=w
            rows.append(b)
            d=data["days"][coin][w].copy(); d["coin"]=coin; d["w"]=w
            dayrows.append(d)
    B=pd.concat(rows,ignore_index=True); D=pd.concat(dayrows,ignore_index=True)
    cm=B.groupby("coin")["ret"].mean()
    B["cm"]=B["coin"].map(cm)
    B["mkt"]=B["pos"]*B["cm"]; B["timing"]=B["pos"]*(B["nxt"]-B["cm"])
    out={}
    bk=D.groupby("day")[["book_return","coin_return"]].mean()
    out["summary"]=pd.Series({
        "gross_bar_gain_mean":B["gross"].mean(),
        "fee_per_bar_mean":B["fee"].mean(),
        "turnover_per_bar":B["turn"].mean(),
        "mean_abs_pos":B["pos"].abs().mean(),
        "mean_pos":B["pos"].mean(),
        "market_part":B["mkt"].mean(),
        "timing_part":B["timing"].mean(),
        "book_daily_mean":bk["book_return"].mean(),
        "hold_daily_mean":bk["coin_return"].mean(),
        "share_long_bars":(B["pos"]>0).mean(),
    })
    B["side"]=np.sign(B["pos"])
    g=B.groupby("side").agg(n=("gross","size"),gross=("gross","mean"),timing=("timing","mean"),fee=("fee","mean"))
    out["by_side"]=g
    B["fq"]=pd.qcut(B["forecast"].abs().rank(method="first"),5,labels=False)
    out["by_absforecast_q"]=B.groupby("fq").agg(gross=("gross","mean"),timing=("timing","mean"),fee=("fee","mean"),turn=("turn","mean"),abspos=("pos",lambda x:x.abs().mean()))
    B["vq"]=pd.qcut(B["volratio"],3,labels=False)
    B["zq"]=pd.qcut(B["z"].abs(),3,labels=False)
    def tstat(x):
        x=x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan
    out["by_volratio_x_absz"]=B.groupby(["vq","zq"]).agg(n=("timing","size"),timing=("timing","mean"),t=("timing",tstat),fee=("fee","mean"))
    # trend context: fading against 20d trend
    B["with20"]=np.sign(B["pos"])*np.sign(B["ret20"])
    out["pos_vs_20d_trend"]=B[B["pos"]!=0].groupby("with20").agg(n=("timing","size"),gross=("gross","mean"),timing=("timing","mean"),t=("timing",tstat))
    out["by_coin"]=B.groupby("coin").agg(gross=("gross","mean"),timing=("timing","mean"),fee=("fee","mean"))
    wk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().groupby("w").mean()
    out["by_window_daily"]=wk
    out["by_weekday"]=B.groupby("wd").agg(timing=("timing","mean"),t=("timing",tstat))
    return out
