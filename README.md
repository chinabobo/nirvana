# nirvana

本项目涵盖了股票行情数据获取、自动化交易、量化策略等内容：

```bash
nirvana/
│
├── LICENSE                      # 项目开源协议文件
├── README.md                    # 项目说明文档，介绍项目背景、功能、安装等
├── backtest/                     # 存放回测相关代码
│   ├── __init__.py
│   ├── backtest_engine.py        # 回测引擎
│   ├── performance_metrics.py    # 性能评估（收益率、夏普比率等）
│   └── portfolio.py              # 投资组合管理（资产配置等）
│
├── config/                       # 存放配置文件
│   ├── __init__.py
│   ├── settings.py               # 全局配置文件（例如API密钥、数据库连接等）
│   └── strategy_config.py        # 策略配置（例如参数设定）
│
├── logs/                         # 存放日志文件
│   └── trading.log               # 交易日志
│
├── main.py                       # 项目入口，调度各模块
├── requirements.txt              # 项目依赖库，列出所有第三方依赖
├── src/                          # 存放项目的主要源代码
│   ├── constants.py              # 常量文件，存放全局常量
│   ├── quotes/                   # 股票行情相关代码
│   │   ├── __init__.py
│   │   ├── monitor.py            # 实时行情监控
│   │   └── snapshot.py           # 获取股票快照数据
│   ├── strategies/               # 量化策略相关代码
│   │   ├── __init__.py
│   │   ├── moving_average.py     # 移动平均策略
│   │   ├── mean_reversion.py     # 均值回归策略
│   │   └── momentum.py           # 动量策略
│   └── trading/                  # 自动化交易相关代码
│       ├── __init__.py
│       └── trading.py            # 交易管理和执行（订单执行、风险管理等）
│
└── tests/                        # 存放单元测试代码
    ├── __init__.py
    ├── test_data.py              # 测试数据加载、清洗等功能
    ├── test_strategies.py        # 测试量化策略
    ├── test_trading.py           # 测试交易模块
    └── test_backtest.py          # 测试回测模块
```

### 目录结构说明：

- **LICENSE**：项目的开源协议，MIT。
- **README.md**：项目的基本介绍，使用说明、安装指南等。
- **backtest/**：存放回测相关的模块，包括回测引擎、性能评估等。
- **config/**：存放项目的配置文件，如全局设置和策略参数等。
- **logs/**：存放项目运行过程中产生的日志文件，便于调试和追踪。
- **main.py**：项目入口文件，负责调度各个模块的功能，启动整个项目。
- **requirements.txt**：列出项目所需的所有依赖库，便于项目的安装和环境配置。
- **src/**：项目的源代码目录，包含常量文件、股票行情数据、量化策略和自动化交易相关代码。
  - **constants.py**：存放全局常量，如股票代码、API配置信息等。
  - **quotes/**：包含实时行情监控和快照获取的功能。
  - **strategies/**：存放不同的量化交易策略。
  - **trading/**：管理交易的执行和风险控制。
- **tests/**：单元测试代码，确保每个模块的功能正常。
  - **test_data.py**：测试数据模块的功能，如数据加载、清洗等。
  - **test_strategies.py**：测试量化策略的正确性。
  - **test_trading.py**：测试交易模块的功能。
  - **test_backtest.py**：测试回测模块的性能和逻辑。

这个项目结构既简洁又模块化，方便后期维护和扩展，同时也符合常见的量化交易项目组织方式。