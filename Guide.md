# Insight 后端调用说明
> 乔毅 2019210472
> 2022.3.9

**本说明只针对Insight项目后端代码，且随版本不断更新**

## 模块介绍
1. 短信查询接口
	- 链接地址：http://abc.charlieqyq.top:32222/msg_search
	- 请求关键字
		- msg
			- 查询的短信内容
			- 字符串类型
	- 返回关键字（字典类型）
		- msg_id
			- 短信序号
		- msg_text
			- 短信内容
		- simi_times
			- 相似度超过阈值次数（即返回次数）
		- cs_value
			- 余弦相似度
2. 短信详情接口
    - 链接地址：http://abc.charlieqyq.top:32222/msg_info
    - 请求关键字
        - id
            - 查询的短信序号
            - 整型
        - wx_id
            - 微信用户的openid
            - 字符串类型
    - 返回关键字
        - msg_text
            - 短信内容
        - msg_analiysis
            - 案例分析
        - simi_times
            - 相似度超过阈值次数（即返回次数）
        - kind_name
            - 案例类别
        - laws
            - 相关法条
        - solutions
            - 解决方法
        - star
            - 是否收藏
3. 历史记录接口
	- 链接地址：http://abc.charlieqyq.top:32222/query_record
	- 请求关键字
		- id
			- 查询的用户微信ID
			- 字符串类型
	- 返回关键字
		- time
			- 查询时间，格式：YYYY-MM-DD hh-mm-ss
		- msg_text
			- 查询文本
4. 添加收藏接口
	- 链接地址：http://abc.charlieqyq.top:32222/add_star
	- 请求关键字
		- id
			- 用户微信ID
			- 字符串类型
		- msg_id
			- 收藏的短信序号
			- 整型
	- 返回关键字
		- true：添加成功
		- false：添加失败
5. 删除收藏接口
	- 链接地址：http://abc.charlieqyq.top:32222/remove_star
	- 请求关键字
		- id
			- 用户微信ID
			- 字符串类型
		- msg_id
			- 收藏的短信序号
			- 整型
	- 返回关键字
		- true：删除成功
		- false：删除失败
6. 查询收藏接口
	- 链接地址：http://abc.charlieqyq.top:32222/get_star
	- 请求关键字
		- id
			- 用户微信ID
			- 字符串类型
	- 返回关键字
		- msg_id
			- 短信序号
		- msg_text
			- 短信文本
7. 查询指定类别的案例
	- 链接地址：http://abc.charlieqyq.top:32222/get_category
	- 请求关键字
		- kind
			- 对应类别编号
			- 整型
			- 具体对应关系如下
				- 1 获赠类
				- 2 紧急情况类
				- 3 钱款类
				- 4 人情类
				- 5 生活类
				- 6 威胁类
				- 7 金融诈骗类
				- 其他 返回：[False]
	- 返回关键字
		- msg_id
			- 案例编号
		- msg_text
			- 短信内容
		- simi_times
			- 相似度超过阈值次数（即返回次数）
		- kind_name
			- 案例类别
		- kind_id
			- 类别编号

## 错误信息
- 1.NotFound
	- 输入URL错误时，将返回404错误信息“Room 404 Not Found”
- 2.ServerError
	- 程序运行错误时，将返回ServerError错误信息“Server Error”