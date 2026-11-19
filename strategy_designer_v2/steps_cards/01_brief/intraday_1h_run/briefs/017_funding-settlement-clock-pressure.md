---
bar: 1h
---
On large perpetual futures venues, funding is paid between longs and shorts at fixed clock times several times a day. Spot prices are tied to perpetual prices by basis traders. So in the hours just before each settlement, a coin's spot price should lean against the crowded side of the perpetual market, then recover in the hours just after.

The reason is mine, not from a source. When one side is crowded, funding is expensive for that side. Some short-horizon holders on that side close before the payment is booked and reopen once it has passed. Basis traders who hold spot against the perpetual unwind or adjust around the same clock time and pass that pressure into spot. This flow is driven by timing, not by information, so it should reverse once the settlement passes.

Spot bars do not show funding directly. The crowded side is read from the coin's own recent trend: after a strong run up, longs are usually paying, and the reverse holds after a strong run down. The claim is that the return in the hours before settlement tends to run against the recent trend, and the return in the hours after tends to recover. Volume should also be raised around those clock times, unlike comparable hours of the day.

The theory is wrong if any of these hold:
- Pre-settlement hours show no return that runs against the trend, compared with other hours at a similar point in the trading day.
- The post-settlement hours do not give back that move.
- The effect appears just as strongly at clock times when no funding is settled.
