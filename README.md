# Nirvana

This project covers stock market data retrieval, automated trading, and quantitative strategies:

```bash
nirvana/
│
├── LICENSE                      # Open source license file
├── README.md                    # Project documentation, including background, functionality, installation, etc.
├── backtest/                     # Contains backtesting-related code
│   ├── __init__.py
│   ├── backtest_engine.py        # Backtesting engine
│   ├── performance_metrics.py    # Performance evaluation (e.g., returns, Sharpe ratio)
│   └── portfolio.py              # Portfolio management (e.g., asset allocation)
│
├── config/                       # Contains configuration files
│   ├── __init__.py
│   ├── settings.py               # Global configuration file (e.g., API keys, database connections)
│   └── strategy_config.py        # Strategy configuration (e.g., parameter settings)
│
├── logs/                         # Contains log files
│   └── trading.log               # Trading logs
│
├── main.py                       # Project entry point, orchestrates various modules
├── requirements.txt              # Project dependencies, lists all third-party libraries
├── src/                          # Contains the main source code of the project
│   ├── constants.py              # Constants file, contains global constants
│   ├── quotes/                   # Stock market data-related code
│   │   ├── __init__.py
│   │   ├── monitor.py            # Real-time market monitoring
│   │   └── snapshot.py           # Fetch stock snapshot data
│   ├── strategies/               # Quantitative strategies-related code
│   │   ├── __init__.py
│   │   ├── moving_average.py     # Moving average strategy
│   │   ├── mean_reversion.py     # Mean reversion strategy
│   │   └── momentum.py           # Momentum strategy
│   └── trading/                  # Automated trading-related code
│       ├── __init__.py
│       └── trading.py            # Trade management and execution (order execution, risk management, etc.)
│
└── tests/                        # Contains unit tests
    ├── __init__.py
    ├── test_data.py              # Tests for data loading, cleaning, etc.
    ├── test_strategies.py        # Tests for quantitative strategies
    ├── test_trading.py           # Tests for trading module
    └── test_backtest.py          # Tests for backtesting module

```

### Directory Structure Explanation:

- **LICENSE**: The open-source license for the project (MIT).
- **README.md**: Basic project introduction, usage instructions, installation guide, etc.
- **backtest/**: Contains modules related to backtesting, including backtest engine, performance evaluation, etc.
- **config/**: Contains configuration files for the project, such as global settings and strategy parameters.
- **logs/**: Contains log files generated during project execution, useful for debugging and tracking.
- **main.py**: The entry point of the project, responsible for orchestrating the functionality of various modules and starting the entire project.
- **requirements.txt**: Lists all dependencies required for the project, aiding in installation and environment setup.
- **src/**: The source code directory for the project, including constants, stock market data, quantitative strategies, and automated trading-related code.
  - **constants.py**: Contains global constants, such as stock codes, API configuration information, etc.
  - **quotes/**: Includes functionality for real-time market monitoring and snapshot retrieval.
  - **strategies/**: Contains different quantitative trading strategies.
  - **trading/**: Manages trade execution and risk control.
- **tests/**: Unit test code to ensure the functionality of each module.
  - **test_data.py**: Tests for data modules, such as loading and cleaning.
  - **test_strategies.py**: Tests the correctness of quantitative strategies.
  - **test_trading.py**: Tests the functionality of the trading module.
  - **test_backtest.py**: Tests the performance and logic of the backtesting module.

This project structure is both simple and modular, making it easy to maintain and expand in the future. It also follows the typical organization found in quantitative trading projects.