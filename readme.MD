# web性能测试框架和工具对比 + 示例代码

## 概述
业内常用的url-api压测工具有ab、locust, loadrunner、httpLoad, jmeter等。
其中，ab、httpLoad是轻量级的，locust是开源的，而且提供web版本，非常推荐。
loadrunner是重量级别（软件时代的经典，需要付费，主要是windows 版本，目前很少有人在用）。

## 项目框架

api_perf_test  
&ensp;&ensp;│ ab_conf.yml             #ab压测case配置文件，例如ab文件路径，压测case压测参数等  
&ensp;&ensp;│ api_conf.yml            # 本项目略，可以具体的项目来具体配置待测api 请求参数设置，例如，headers，body，params，cookie等  
&ensp;&ensp;│ ab_test.py              #ab压测启动脚本，python3 ab_test.py  
&ensp;&ensp;│  
&ensp;&ensp;├─data                     #api参数，post数据存放路径  
&ensp;&ensp;├─lib                      #压测框架lib库,比如处理测试数据的，形成测试报告的一些工具类  
&ensp;&ensp;&ensp;&ensp;│ utils.py  
&ensp;&ensp;&ensp;&ensp;│ parser.py  
&ensp;&ensp;&ensp;&ensp;│ statis.py  
&ensp;&ensp;&ensp;&ensp;│ __init__.py  
&ensp;&ensp;&ensp;&ensp;│  
&ensp;&ensp;├─outputs                  #压测详细结果输出路径  
&ensp;&ensp;└─results                  #压测结果建议报表输出路径

## 配置文件说明
配置文件主要是对ab 或者locust命令的参数进行配置，比如对ab来说有最大请求数，和当前并发数，还有url等
对locust主要是当前并发数，和每一个并发数孵化的子请求数，比如如果是100个并发数，每一个孵化10个子请求，那么总请求数就是100\*10=1000个

## 测试结果分析
测试结果分析主要是把测试结果进行整理，形成一个很直观的报告，因为直接把测试结果给人看，不一定能获得有效信息，而且浪费他人时间，如果把主要了解的信息提取出来并且根据业务有对比，可能更有帮助。
有时候需要测试结果来完成CI的下一步，如果测试结果不合格，应该有自动预警比如发信给相关负责人。

当然，locust 的web方式做的非常棒，也可以不用自己再花精力整理报告，拿来就好了。
因为locust的运行方式两种，因此本案例是采用no web方式，方便CI，如果单纯做压力测试，推荐用web方式，启动后控制台出现(举个例子）：
```
Starting web monitor at *:8089
[2019-02-15 14:19:31,143] xxx: Starting Locust 0.9.0
[2019-02-15 14:19:59,655] xxx: Hatching and swarming 10 clients at the rate 10 clients/s...
```
这时候你去浏览器输入 localhost:8089 即可享受web方式带来的方便和良好体验。

## 工具对比
[对wrk，ab, locust, jmeter性能工具的对比：](https://testerhome.com/topics/17068)

工具|wrk|ab|locust|jmeter
---|:--:|--:|:---:|----:
安装|简单|简单|依赖python|依赖jdk
场景|压测|不支持|不支持|支持|支持
UI界面|无 |无 | 有 |  有
脚本录制|无 |无 | 无 | 利用本地ProxyServer或badboy
资源监控|无 |无 | 无 | 通过JMeterPlugins插件和ServerAgent实现
报告分析|无 |无 | 无 | 生成HTML报告
CI的支持|支持|支持|支持|支持

