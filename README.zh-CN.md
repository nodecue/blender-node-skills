[English](README.md) | 简体中文

# NodeCue Blender Node Skills

一个 agent skill，教 AI 编码 agent **正确构建 Blender 几何节点（Geometry Nodes）图——并对结果做出解释，让你能从中学习**。

给 agent 装上这个 skill，然后用自然语言描述需求（比如"在这个表面上散布草叶，带密度遮罩"）。agent 会把 skill 作为领域知识来阅读，在 Blender 里搭建真实的节点图：精确的节点标识和 socket 名、经过验证的图模式、field / 数据流推理、基于回读（readback）的自我纠错。生成的节点图自带**教学标注**——用 Frame 标注每个逻辑块、解释节点为什么这样组织——所以产出是可以研究学习的，不只是拿来用的。

这不是预设库，也不是 Python 脚本生成器。它是让通用 agent 真正掌握 Blender 节点系统的知识层。

## 包含内容

- `skills/geometry-nodes/SKILL.md` — 入口：构建循环、可靠性规则、几何节点心智模型（数据流通道 vs field 通道），以及 rules 和 patterns 的索引
- `skills/geometry-nodes/rules/` — 30+ 个节点族参考文件，含精确的 `bl_idname` 和 socket 名
- `skills/geometry-nodes/patterns/` — 验证过的图模式（散布分发、多部件拼接、表面位移、密度控制散布、Repeat Zone 技巧等）

## 适配的 Agent

任何能读取 skill 文件并操作 Blender 的 agent：

- **Claude Code / Codex CLI / 其他 agent CLI** — 通过社区的 [blender-mcp](https://github.com/ahujasid/blender-mcp) 项目连接 Blender（Blender 目前没有官方 MCP；如果将来官方发布，则优先使用官方版）
- **[NodeCue Blender 插件](https://github.com/monswag/NodeCue)** — 内置同一套 skill 的 Blender 内 agent，使用你自己的 API key 运行

## 已测试的组合

目前实际验证过的组合：

- Codex CLI + 社区 blender-mcp（含"有 skill vs 无 skill"对照实验）
- NodeCue 内建 agent + OpenRouter 模型（kimi-k2.6、deepseek-v4-pro），含自动化图结构校验：必需节点齐全、几何主干到达 Group Output、field 驱动接到真实消费端、教学 Frame 存在

Claude Code 及其他支持 MCP 的 agent 走同样的路径，但尚未正式评估——欢迎反馈使用结果。

## 安装

```bash
git clone https://github.com/monswag/nodecue-blender-node-skills.git
```

把 skill 文件夹复制到你的 agent 的 skills 目录：

```bash
# Claude Code
cp -r nodecue-blender-node-skills/skills/geometry-nodes ~/.claude/skills/

# Codex
cp -r nodecue-blender-node-skills/skills/geometry-nodes ~/.codex/skills/
```

其他 agent：把 `skills/geometry-nodes/` 复制到该 agent 加载 skills 的目录即可。

skill 有意不捆绑运行时系统提示词：每个 agent 使用自己的行为指令，把这个 skill 当作领域知识来读。

## 注释语言

生成的 Frame 标注和解释默认跟随你提示词的语言——用中文描述需求，就得到中文的教学标注。节点名、socket 名等 Blender 术语始终保持英文原文，与 Blender 界面和主流教程保持一致，便于对照学习。

## 范围与准确性

- **仅支持几何节点，Blender 5.0+。** 规则基于 Blender 5.0 手册编写；大部分测试在 5.1 上进行。节点行为在不同 Blender 版本间可能有差异。
- **Shader Nodes 和 Compositing Nodes 在计划中**，规则和模式验证完成后会作为同级 skill 文件夹加入本仓库。
- **结果可能出错。** skill 能大幅减少凭空编造的节点名和错误连线，但 LLM 驱动的构建仍可能产出错误的图或有误导性的解释——模型质量很关键。依赖结果之前请在 Blender 中检查节点图，遇到失败请反馈。

## 反馈

当 agent 读取了这个 skill 之后仍然把 Blender 节点任务做错时，请用 `Skill feedback` 模板开 issue。有用的报告包括：提示词、agent/工具名称、使用的模型、节点图哪里错了，以及可以分享的回读 JSON 或截图。

请勿在公开 issue 中包含 API key、私有资产库路径或不可公开的 `.blend` 文件。

## 许可

MIT — 见 [LICENSE](LICENSE)。
