# Component wish list

One block per idea that needs components the catalogue does not have.

## 020-04_support-breakdown-continues-down_1d
- Component: SupportTouchCount: over bars t-90 .. t-1, finds the swing lows (a low below the lows of its n neighbouring bars on each side), groups those within a band (for example 1 percent) into levels, and for the level nearest above the close gives the number of swing lows in it; from low and close; grows by one with each further turn at that level | measures: comparison
- Component: HeldLevelBreakDepth: at bar t, the percent distance of the close below the most-touched support level of bars t-90 .. t-1 (as above), times its touch count, and 0 when the close is above every such level; from low and close; grows continuously with the depth of the break and with the count of times the level held | measures: situation
