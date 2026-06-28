# Materials Studio Agent Toolkit

[中文](#中文说明) | [English](#english)

## English

`materials-studio-agent-toolkit` is a public, local-first toolkit for helping agents work with BIOVIA Materials Studio through structured scripts, capability cards, templates, and result readers.

It is designed for the case where an agent shares a machine or workspace with a human operator and needs to:

1. generate `MaterialsScript` from approved capability definitions
2. execute those scripts through either a direct standalone bridge or a GUI-resident queue runner
3. prepare formal GUI submission packages
4. read, normalize, and analyze calculation results
5. publish selected outputs into project documents

This repository does **not** expose an MCP server. The current delivery is a lightweight CLI toolkit plus a generic `SKILL.md`.

What is real today:

- real script rendering
- real standalone execution
- real GUI-loop queue handoff
- real result parsing
- real round-report generation for next-step decisions
- real local publication into project documents

What this is not:

- not an MCP server
- not a self-starting GUI loop supervisor

### What this repository contains

#### Core toolkit

The main delivery lives under:

- `tools/ms_agent_toolkit`

It includes:

- capability registry loader and JSON capability cards
- Jinja2 `.pl.j2` templates
- command wrappers
- thin adapters
- contract tests
- mock fixtures
- package metadata in `tools/ms_agent_toolkit/pyproject.toml`
- a detailed delivery README in `tools/ms_agent_toolkit/README.md`

#### Generic skill guide

The agent-facing generic skill guide lives at:

- `skills/materials-studio-agent-toolkit/SKILL.md`

Use this with any skill-capable agent that can read or import a `SKILL.md` file.

#### Supporting bridge utilities

This repo also includes the validated bridge layer that the toolkit currently wraps:

- `tools/ms_bridge`

Reference-only historical or supporting Materials Studio automation assets are also present here:

- `tools/gateway_agent_bridge`

### First-release status

The current release includes:

- CLI command entrypoints declared in `pyproject.toml`
- static capability cards for:
  - `castep.energy`
  - `castep.geometry_optimization`
  - `forcite.geometry_optimization` now definition-complete, while execution remains out of scope for this release
- first-release templates for:
  - standalone CASTEP energy
  - GUI CASTEP geometry optimization
- result reading support for `castep`
- first-pass structured result analysis with candidate next-step options
- a generic skill guide
- passing toolkit tests
- passing legacy `ms_bridge` tests

Current state:

- `run_materialscript` supports a real standalone execution path
- `run_materialscript --backend gui_loop` supports queue-based handoff to a Materials Studio GUI-resident runner in the isolated repo
- `read_module_result` now returns both parsed output and a lightweight analysis block with next-step options
- `publish_to_project_documents` performs a real local publication step

Remaining limitation:

- the toolkit still does not start or supervise the Materials Studio GUI loop process by itself; the GUI-resident loop must already be running when `--backend gui_loop` is used

### Quick start

#### Python requirements

From `tools/ms_agent_toolkit/pyproject.toml`:

- Python `>=3.12`
- `pydantic>=2.0`
- `jinja2>=3.1`

#### Install locally

From the repository root:

```powershell
py -3.12 -m pip install -e .\tools\ms_agent_toolkit
```

This command is expected to work directly from the checked-out repo. The package metadata in `tools/ms_agent_toolkit/pyproject.toml` is rooted back to the repository top-level so editable install resolves the `tools.*` packages correctly.

#### Main commands

Declared console entrypoints:

- `ms_agent_toolkit_doctor`
- `run_materialscript`
- `get_gui_loop_status`
- `prepare_gui_submission_package`
- `read_module_result`
- `report_next_step`
- `publish_to_project_documents`

PowerShell-safe examples:

```powershell
$params = '{"input_xsd":"C:/work/model.xsd","quality":"Fine"}'
run_materialscript --capability castep.energy --params-json $params
```

```powershell
run_materialscript --capability castep.energy --params-file C:/work/params.json
```

```powershell
$params = '{"input_xsd":"model.xsd","quality":"Fine"}'
run_materialscript --backend gui_loop --capability castep.geometry_optimization --params-json $params
```

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package
```

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package --params-file C:/work/gui_params.json
```

```powershell
read_module_result --module castep --result-dir C:/work/job42
```

```powershell
report_next_step --module castep --result-dir C:/work/job42
```

```powershell
ms_agent_toolkit_doctor
```

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```

### Machine setup

This repo does **not** bundle `RunMatScript.bat`. That comes from the local Materials Studio installation.

Before using backend execution paths, review:

- `tools/ms_bridge/config/bridge_config.json`
- `tools/ms_agent_toolkit/config/toolkit_config.json`

Fallback behavior:

- toolkit commands that load runtime config prefer `bridge_config.json` and `toolkit_config.json`
- if a concrete file is missing, it falls back to the matching `*.example.json`

In particular, fix:

- `materialsStudioInstallRoot`
- `runMatScriptBat`
- `workspaceRoot`
- `defaultProjectDocumentsRoot`
- `capabilityRegistryPath`
- `templatesRoot`

If `runMatScriptBat` is wrong, the toolkit cannot launch MaterialsScript through the existing bridge.

For `gui_loop` execution, also review `guiLoopQueueRoot` in `tools/ms_agent_toolkit/config/toolkit_config.example.json`. In the current delivery it points at the isolated repo queue under `C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\gui_loop_queue`, not at the scientific workspace.

The shipped `tools/ms_agent_toolkit/knowledge/` tree is a curated set of official docs and examples. It is there so the toolkit can keep capability definitions, parameter guidance, and generated scripts aligned with the Materials Studio surface that is actually delivered in this repo.

If a required module knowledge pack or capability is missing, the intended extension path is to let the agent complete it from the local official Materials Studio installation sources rather than inventing it from memory. The repo-local guide for that workflow is:

- `tools/ms_agent_toolkit/knowledge/capability_completion_guide.md`

Current `gui_loop` preconditions:

- a Materials Studio GUI-resident loop must already be running
- the queue root must point at the intended queue directory
- the current recommended loop implementation is the `gui_loop_v2.pl` script already shipped in `tools/gateway_agent_bridge/perl/`

### How to give this to another agent

#### For a skill-capable agent

Provide:

- `skills/materials-studio-agent-toolkit/SKILL.md`
- the whole `tools/ms_agent_toolkit` directory
- the wrapped backend utilities under `tools/ms_bridge`

#### For a non-skill-capable agent

Provide:

- this repository
- `tools/ms_agent_toolkit/README.md`
- the command-line entrypoints
- the capability JSON files

### What is not included yet

This first version does not yet include:

- an MCP server
- non-CASTEP result readers
- a completed Forcite execution path
- experimental-mode command implementations in the delivered CLI wrappers
- automatic startup control for the Materials Studio GUI loop

For actual backend execution and low-level bridge behavior, continue to inspect and reuse `tools/ms_bridge/`.

---

## 中文说明

`materials-studio-agent-toolkit` 是一个面向 BIOVIA Materials Studio 的本地优先工具包，用来帮助 agent 通过结构化脚本、capability card、模板和结果读取器来协助建模与计算。

它适用于这样一种场景：

1. agent 与人工操作者共享同一台机器或同一个工作区
2. agent 需要根据约束好的能力卡生成 `MaterialsScript`
3. agent 需要准备正式 GUI 提交包
4. agent 需要读取和归一化计算结果
5. agent 需要把部分结果整理到 project documents 中

这个仓库 **不是** MCP 服务端。当前交付形态是：

- 一个轻量 CLI toolkit
- 一份通用 `SKILL.md`

### 仓库包含什么

#### 核心工具包

主交付目录在：

- `tools/ms_agent_toolkit`

其中包括：

- capability registry loader 和 capability JSON 文件
- Jinja2 `.pl.j2` 模板
- command wrapper
- thin adapter
- contract tests
- mock fixture
- 包元数据：`tools/ms_agent_toolkit/pyproject.toml`
- 更详细的交付说明：`tools/ms_agent_toolkit/README.md`

#### 通用 skill 指南

agent 用的通用 skill 在：

- `skills/materials-studio-agent-toolkit/SKILL.md`

任何支持 skill 机制、并且能读取或导入 `SKILL.md` 的 agent 都可以使用它。

#### 支撑 bridge 工具

当前 toolkit 还复用了已经验证过的 bridge 层：

- `tools/ms_bridge`

另外仓库里还保留了一些历史性或参考性的 Materials Studio 自动化资产：

- `tools/gateway_agent_bridge`

### 第一版现状

当前版本已经包含：

- 在 `pyproject.toml` 中声明的 CLI 入口
- 三张 capability card：
  - `castep.energy`
  - `castep.geometry_optimization`
  - 已定义完成的 `forcite.geometry_optimization`
- 两个首发模板：
  - standalone CASTEP energy
  - GUI CASTEP geometry optimization
- `castep` 结果读取支持
- 通用 `SKILL.md`
- 通过的 toolkit 测试
- 通过的 `ms_bridge` 既有测试

当前最重要的限制是：

- 这些命令现在更偏向于**生成结构化请求、打包元数据、结果归一化和发布响应整形**
- 它们**还不是**一个完整的一键式执行编排器，不能自动完成从生成、运行、监控到发布整个 Materials Studio 工作流

### 快速开始

#### Python 依赖

来自 `tools/ms_agent_toolkit/pyproject.toml`：

- Python `>=3.12`
- `pydantic>=2.0`
- `jinja2>=3.1`

#### 本地安装

在仓库根目录执行：

```powershell
py -3.12 -m pip install -e .\tools\ms_agent_toolkit
```

#### 主要命令

当前声明的命令入口：

- `run_materialscript`
- `prepare_gui_submission_package`
- `read_module_result`
- `publish_to_project_documents`

示例：

```powershell
run_materialscript --capability castep.energy --params-json "{\"input_xsd\":\"C:/work/model.xsd\",\"quality\":\"Fine\"}"
```

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package
```

```powershell
read_module_result --module castep --result-dir C:/work/job42
```

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```

### 新机器上的配置

这个仓库 **不包含** `RunMatScript.bat`。它来自本机安装的 Materials Studio。

在使用 backend 执行相关路径之前，请先检查：

- `tools/ms_bridge/config/bridge_config.example.json`
- `tools/ms_agent_toolkit/config/toolkit_config.example.json`

尤其需要修正：

- `materialsStudioInstallRoot`
- `runMatScriptBat`
- `workspaceRoot`
- `defaultProjectDocumentsRoot`
- `capabilityRegistryPath`
- `templatesRoot`

如果 `runMatScriptBat` 路径不对，toolkit 就无法通过现有 bridge 启动 MaterialsScript。

### 怎么交付给别的 agent

#### 给支持 skill 的 agent

交付：

- `skills/materials-studio-agent-toolkit/SKILL.md`
- 整个 `tools/ms_agent_toolkit` 目录
- 被包装的 backend 工具 `tools/ms_bridge`

#### 给不支持 skill 的 agent

交付：

- 这个仓库本身
- `tools/ms_agent_toolkit/README.md`
- 命令行入口
- capability JSON 文件

### 当前还不包含什么

这个第一版目前还**不包含**：

- MCP server
- 完整的一键式执行编排器
- 非 CASTEP 的结果读取器
- 已实现的 Forcite 正式执行路径
- 当前 CLI wrapper 中真正实现的 experimental-mode 路径

如果你需要低层 backend 执行行为，请继续直接查看和复用 `tools/ms_bridge/`。
