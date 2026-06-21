# ms_bridge

一个通用的 `Materials Studio` 半自动桥。

## 前提

1. 用户已手动打开 `Materials Studio`
2. 用户已手动打开目标 `project`
3. 本桥默认不依赖常驻 `loop`

## 能力

1. 执行显式 `MaterialsScript`
2. 提交正式 `CASTEP` 任务
3. 读取 `CASTEP` 结果
4. 生成最小状态文件

## 结果分类

- `production`: 结果必须进入 GUI `Project` 树
- `diagnostic`: 结果可仅落在工作目录

## 目录结构

- `config/`: 桥接配置样例
- `scripts/`: PowerShell 与 Python 辅助脚本
- `materials/templates/`: 可复用 `MaterialsScript` 模板
- `tests/`: 本地测试

## 最小执行示例

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\invoke_materialscript.ps1 `
  -RunMatScriptBat "C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\etc\Scripting\bin\RunMatScript.bat" `
  -ScriptPath "C:\path\to\job.pl"
```
