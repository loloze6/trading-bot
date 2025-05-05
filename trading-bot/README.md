Cryptocurrency Trading Bot Foundation
====================================
A modular architecture for a cryptocurrency trading bot using the Binance API.
This design emphasizes clean separation of concerns and extensibility.


/trading-bot/
│
├── config/
│   └── settings.py
│
├── core/                   #Idea - Could be splitted in data folder, risk folder
│   ├── bot.py               # Main trading bot class
│   ├── data_manager.py       # Data fetcher (class)
│   ├── execution_handler.py  # Execution handler (class)
│   ├── risk_manager.py       # Risk control (class)
│   ├── strategy_base.py      # Base Strategy class
│
├── strategies/
│   ├── simple_strategy.py    # Inherit from StrategyBase
│   ├── moving_average.py
│
├── logs/
│   └── bot.log
│
├── tests/
│   ├── test_strategy.py
│   ├── test_execution_handler.py
│
├── utils/
│   ├── logger.py
│   ├── api_helpers.py
│
├── main.py
├── requirements.txt
└── README.md
