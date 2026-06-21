# gateway_agent_bridge

Gateway/job-control 子层。

## 目的

1. 提交 Gateway 标准 job
2. 查询 Gateway job 状态
3. 停止 Gateway job

## 非目标

1. 不重写 Gateway
2. 不模拟 GUI 点击
3. 不取代 standalone ms_bridge

## 现阶段范围

1. 最小 `Scripting` job 验证
2. 最小 `CASTEP Energy` job 验证
3. 为后续正式长任务切换到 Gateway 模式提供依据
