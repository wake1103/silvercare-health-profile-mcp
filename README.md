# SilverCare Health Profile MCP

SilverCare 健康档案查询 MCP 服务。当前使用模拟数据，仅提供档案查询，不执行健康诊断或风险判断。

## 工具说明

### `get_health_profile`

根据用户 ID 查询 SilverCare 健康档案。

**输入**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `user_id` | `string` | 要查询的用户 ID |

**输出**

返回包含 `success`、`user_id`、`data_source`、`profile` 和 `error` 字段的字典。`data_source` 当前固定为 `simulated`。

三种返回场景：

1. **查询成功**：`user_id=user_001` 时，`success=true`，`profile` 返回模拟档案，`error=null`。
2. **档案不存在**：其他普通用户 ID 返回 `success=false`、`profile=null`，错误码为 `PROFILE_NOT_FOUND`。
3. **模拟服务超时**：`user_id=user_timeout` 时返回 `success=false`、`profile=null`，错误码为 `MCP_TIMEOUT`。这是开发阶段的模拟故障，真实部署时应替换为实际的超时和异常处理逻辑。

## 本地运行

要求 Python 3.10 或更高版本。

### 使用 pip

```bash
pip install -e .
python -m silvercare_mcp
```

默认通过 stdio 通信。也可以安装依赖后直接运行：

```bash
pip install mcp[cli]
python -m silvercare_mcp
```

如需启动 Streamable HTTP 服务：

```bash
MCP_TRANSPORT=streamable-http python -m silvercare_mcp
```

Windows PowerShell：

```powershell
$env:MCP_TRANSPORT = "streamable-http"
python -m silvercare_mcp
```

HTTP 服务默认监听 `0.0.0.0:8000`，可通过 `MCP_HOST` 和 `MCP_PORT` 修改。

### 使用 uvx

在项目目录运行：

```bash
uvx --from . silvercare-mcp
```

从 GitHub 直接运行（替换 `<GITHUB_USERNAME>`）：

```bash
uvx --from git+https://github.com/<GITHUB_USERNAME>/silvercare-health-profile-mcp.git silvercare-mcp
```

uvx 默认以 stdio 方式启动。如需 HTTP：

```bash
MCP_TRANSPORT=streamable-http uvx --from . silvercare-mcp
```

## AgentArts 接入

> AgentArts 是公有云服务，无法访问本地或内网。UVX 方式由平台托管运行；Streamable HTTP 方式必须部署到公网可访问的地址。

### 方式 A：UVX（推荐）

在 AgentArts 创建 MCP 服务时选择 **UVX** 安装方式，使用以下配置（替换 `<GITHUB_USERNAME>`）：

```json
{
  "mcpServers": {
    "silvercare-health": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/<GITHUB_USERNAME>/silvercare-health-profile-mcp.git",
        "silvercare-mcp"
      ]
    }
  }
}
```

入口默认使用 stdio，适配 UVX 托管调用；无需额外设置 `MCP_TRANSPORT`。

### 方式 B：Streamable HTTP（备选）

先将服务部署到公网服务器，并启动：

```bash
MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 MCP_PORT=8000 silvercare-mcp
```

在 AgentArts 中选择 **Streamable HTTP** 接入方式，填写公网 MCP Endpoint：

```text
https://<YOUR_PUBLIC_DOMAIN>/mcp
```

请使用 HTTPS，并确认安全组、防火墙和反向代理已开放对应端口及 `/mcp` 路径。不要把仅监听本机或内网的地址直接填给 AgentArts。
