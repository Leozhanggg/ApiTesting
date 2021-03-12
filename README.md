# ApiTesting
此框架是基于Python+Pytest+Requests+Allure+Yaml+Json实现全链路接口自动化测试。

主要流程：解析接口数据包 ->生成接口基础配置(yml) ->生成测试用例(yaml+json) ->生成测试脚本(.py) ->运行测试(pytest) ->生成测试报告(allure)
测试流程：初始化请求 ->处理接口基础信息 ->读取前置接口用例 ->发送前置接口 ->处理当前接口数据 ->发送当前接口  ->检查接口返回

ApiTesting全链路接口自动化测试框架 - 初版（一）
> 介绍：https://www.cnblogs.com/leozhanggg/p/14373878.html

ApiTesting全链路接口自动化测试框架 - 新增数据库校验（二）
> 介绍：https://www.cnblogs.com/leozhanggg/p/14522084.html
