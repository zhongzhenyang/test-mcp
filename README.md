# service_b

一个基于 Python MCP SDK 的服务B示例：

- 对外暴露 MCP tools 给 agent
- 内部通过 RESTful 调用服务A
- 使用用户名/密码登录服务A获取 token
- 请求服务A接口时携带 Bearer token
- 不主动刷新 token
- 当服务A返回 401 时，重新登录并重试一次
- 复用 HTTP client
- 分层架构
- 每个 MCP tool 都有明确的输入/输出 schema
- 结构化 JSON 日志
- 统一错误码与 request_id

## 安装

```bash
pip install -r requirements.txt
```

## 配置

```bash
cp .env.example .env
```

然后修改 `.env`。

## 启动

```bash
python main.py
```
