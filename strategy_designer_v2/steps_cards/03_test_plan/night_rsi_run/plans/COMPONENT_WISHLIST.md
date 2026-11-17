# Component wish list

One block per idea that needs components the catalogue does not have.

## 010-08_rsi-below-streak-reversal_1d
- Component: RsiSideAgeComponent: from the closes, the Wilder RSI(`period` 14); outputs n, the number of consecutive bars up to bar t on which RSI has been below 50 (or signed: -n below and +n above), capped at `max_bars`; it is 0 or 1 on the first bar of a run and grows by 1 for each further bar RSI stays on the same side | measures: situation
