def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []; daily = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            pos = b["postRebalance_current_allocation"].fillna(0).values.astype(float)
            prev = b["previous_allocation"].fillna(0).values.astype(float)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            fee = (b["postRebalance_total_value"]-b["total_portfolio_value"]).values/b["total_portfolio_value"].values
            ch = np.abs(pos-prev)
            kind = np.where((prev==0)&(pos!=0),"open",np.where((prev!=0)&(pos==0),"close",np.where(ch>0,"resize","none")))
            f = b["forecast"].fillna(0).values
            # vol rank proxy: 168h mean abs move ranked over 720
            ar = pd.Series(np.abs(np.r_[np.nan, c[1:]/c[:-1]-1]))
            m = ar.rolling(168).mean()
            vr = m.rolling(720, min_periods=200).rank(pct=True).values
            # 2h z
            r2 = pd.Series(c).pct_change(2)
            sd = pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1]).rolling(168).std()*np.sqrt(2)
            z = (r2/sd).values
            for h in [2,24]:
                idx = np.arange(0, len(c)-24, 2)
                recs.append(pd.DataFrame(dict(coin=coin, w=w, h=h, z=z[idx], vr=vr[idx], f=f[idx],
                    fr=c[idx+h]/c[idx]-1)))
            daily.append(pd.DataFrame(dict(kind=kind, gross=pos*r1, fee=fee, ch=ch, f=f, pos=pos)))
    D = pd.concat(daily)
    out["by_trade_kind"] = D.groupby("kind").agg(n=("ch","size"), turnover=("ch","sum"), fee=("fee","sum"))
    D["fb"] = pd.cut(D.f, [-0.1,0.001,5,10,15,20.1])
    out["gross_fee_by_held_forecast"] = D.groupby("fb").agg(n=("f","size"), gross=("gross","sum"), fee=("fee","sum"), meanpos=("pos","mean"))
    R = pd.concat(recs).dropna()
    R["ex"] = R.fr - R.groupby(["coin","h"]).fr.transform("mean")
    R["zb"] = pd.cut(R.z, [-99,-3,-2,-1,0,99])
    R["vb"] = pd.cut(R.vr, [0,0.25,0.5,0.75,0.9,1.0])
    out["ex2_bp_z_by_volrank"] = (R[R.h==2].groupby(["zb","vb"]).ex.mean()*1e4).unstack()
    out["ex24_bp_z_by_volrank"] = (R[R.h==24].groupby(["zb","vb"]).ex.mean()*1e4).unstack()
    out["n_z_by_volrank"] = R[R.h==2].groupby(["zb","vb"]).size().unstack()
    return out
