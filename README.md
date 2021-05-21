# ApiTesting
此框架是基于Python+Pytest+Requests+Allure+Yaml+Json实现全链路接口自动化测试。

主要流程：

> 解析接口数据包 ->生成接口基础配置(yml) ->生成测试用例(yaml+json) ->生成测试脚本(.py) ->运行测试(pytest) ->生成测试报告(allure)

测试流程：

> 初始化请求 ->处理接口基础信息 ->读取前置接口用例 ->发送前置接口 ->处理当前接口数据 ->发送当前接口  ->检查接口返回

ApiTesting全链路接口自动化测试框架 - 初版（一）
> 介绍：https://www.cnblogs.com/leozhanggg/p/14373878.html

ApiTesting全链路接口自动化测试框架 - 新增数据库校验（二）
> 介绍：https://www.cnblogs.com/leozhanggg/p/14522084.html

ApiTesting全链路接口自动化测试框架 - 实战应用
> 介绍：https://www.cnblogs.com/leozhanggg/p/14519800.html

运行配置说明：

> 运行项目名
project_name: PyDemo

> 运行模式:
auto_switch: 2

> 0 - 不开启自动生成测试用例功能，将直接运行测试

> 1 - 根据手工编写用例，自动生成测试脚本，然后运行测试

> 2 - 根据接口抓包数据，自动生成测试用例和测试脚本，然后运行测试

> 3 - 根据接口抓包数据，自动生成测试用例和测试脚本，但不运行测试

> 注意：目前解析仅支持(.chlsj)格式，请使用Charles工具抓包导出JSON Session File

> 扫描测试用例目录（且仅当auto_switch=1时有用）
scan_dir:

> 使用模糊匹配测试用例（空则匹配所有）
pattern:

> 执行并发线程数（0表示不开启）
process: 0

> 失败重试次数（0表示不重试）
reruns: 0

> 本轮测试最大允许失败数（超出则立即结束测试）
maxfail: 20

> 接口调用间隔时间（s）
interval: 1

> 测试结果校验方式说明（共5种方式）：

> 1 - no_check：不做任何校验

> 2 - check_code：仅校验接口返回码code

> 3 - check_json：校验接口返回码code，并进行json格式比较返回结果（默认方式）

> 4 - entirely_check：校验接口返回码code，并进行完整比较返回结果

> 5 - regular_check：校验接口返回码code，并进行正则匹配返回结果

