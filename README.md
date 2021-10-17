# ApiTesting-excel
此框架是基于Python+Pytest+Requests+Allure+Excel 实现接口自动化测试。

测试流程：

> 初始化请求 ->处理接口基础信息 ->读取前置接口用例 ->发送前置接口 ->处理当前接口数据 ->发送当前接口  ->检查接口返回

测试结果校验方式说明（共5种方式）：

> 1 - no_check：不做任何校验

> 2 - check_code：仅校验接口返回码code

> 3 - check_json：校验接口返回码code，并进行json格式比较返回结果

> 4 - entirely_check：校验接口返回码code，并进行完整比较返回结果

> 5 - regular_check：校验接口返回码code，并进行正则匹配返回结果

