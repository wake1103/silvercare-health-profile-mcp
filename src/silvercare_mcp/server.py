from mcp.server import MCPServer
import asyncio

mcp = MCPServer("SilverCare-Health-Profile")

# 模拟档案数据（开发阶段，data_source = simulated）
MOCK_PROFILES = {
    "user_001": {
        "age": 72,
        "allergies": [],
        "medical_history": [],
        "health_notes": ["当前为项目模拟档案"],
        "updated_at": "2026-11-02T09:00:00Z",
    }
}

@mcp.tool()
async def get_health_profile(user_id: str) -> dict:
    """根据用户ID查询SilverCare系统中的健康档案。只返回档案数据，不执行健康诊断或风险判断。"""

    # 场景1：模拟档案查询服务故障（必须放在最前面，否则会被当成"档案不存在"）
    if user_id == "user_timeout":
        await asyncio.sleep(0.1)
        return {
            "success": False,
            "user_id": user_id,
            "data_source": "simulated",
            "profile": None,
            "error": {
                "code": "MCP_TIMEOUT",
                "message": "Profile service timeout"
            }
        }

    # 模拟查询耗时
    await asyncio.sleep(0.05)

    # 场景2：档案不存在
    if user_id not in MOCK_PROFILES:
        return {
            "success": False,
            "user_id": user_id,
            "data_source": "simulated",
            "profile": None,
            "error": {
                "code": "PROFILE_NOT_FOUND",
                "message": "No profile found for this user"
            }
        }

    # 正常返回
    return {
        "success": True,
        "user_id": user_id,
        "data_source": "simulated",
        "profile": MOCK_PROFILES[user_id],
        "error": None
    }
