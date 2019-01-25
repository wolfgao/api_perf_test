# web性能测试框架和工具对比

## 概述
业内常用的url-api压测工具有ab、locust, loadrunner、httpLoad, jmeter等。
其中，ab、httpLoad是轻量级的，locust是开源的，而且提供web版本，非常推荐。
loadrunner是重量级别（软件时代的经典，需要付费，主要是windows 版本，目前很少有人在用）。

## 项目框架

api_perf_test
    │ ab_conf.yml             #ab压测case配置文件，例如ab文件路径，压测case压测参数等
    │ api_conf.yml            # 本项目略，可以具体的项目来具体配置待测api 请求参数设置，例如，headers，body，params，cookie等
    │ ab_test.py              #ab压测启动脚本，python3 ab_test.py
    │
    ├─data                     #api参数，post数据存放路径
    ├─lib                      #压测框架lib库,比如处理测试数据的，形成测试报告的一些工具类
        │ utils.py
        │ parser.py
        │ statis.py
        │ __init__.py
        │
    ├─outputs                  #压测详细结果输出路径
    └─results                  #压测结果建议报表输出路径

## 配置文件说明

## 测试结果分析


## 工具对比
