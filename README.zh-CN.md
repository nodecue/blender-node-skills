[English](README.md) | 简体中文

# NodeCue Blender Node Skills

一个 agent skill，教 AI 编码 agent **正确构建 Blender 几何节点（Geometry Nodes）图——并对结果做出解释，让你能从中学习**。

## 为什么要装它？

强模型不装任何 skill 也能搭出一张"看起来能跑"的几何节点图。真正出问题的是让图**可用**的那些环节：需求被静默丢弃、连线没有实际生效、没有暴露任何控制参数、没有可学习的内容。

我们用同一个 agent（Codex CLI + Blender MCP）、同样的提示词，做了有/无 skill 的对照实验：

| 提示词要求 | 无 skill | 有 skill |
|---|---|---|
| 草叶散布，**带密度遮罩** | 密度遮罩**被静默丢弃**——没有噪声场，`Density Factor` 从未连接；暴露控制数为 0 | Noise → `Density Factor` 正确接线；暴露 `Density`、`Scale Min`、`Scale Max`；2 个教学 Frame |
| 沿曲线生成弧形管道 | 截面曲线**从未接入** `Curve to Mesh`——管道没有截面；5 个节点只有 2 条连线 | 截面正确接线；暴露 `Pipe Radius` |
| 噪声地形，**带高度控制** | 暴露控制数为 0 | 暴露 `Height`、`Noise Scale` |

两组都能通过"图连到输出"这种朴素检查——差异只有在检查**需求是否真正被满足**时才显现。（诚实说明：这是一次实际操作层面的对照，不是实验室级的无记忆隔离实验；复现用的 harness 在 [NodeCue 仓库](https://github.com/monswag/NodeCue)里。）

**在顶级模型上，差距从"对不对"转移到"工艺和约定"。** 用 Codex + gpt-5.6（extra-high 推理）做同提示词对照：两边几何结果都正确——但无 skill 时，提示词必须显式要求加解释 frame，模型还把每个节点都改名并写满解释标签（破坏了节点图与 Blender 界面、教程之间的对照），成品图里留着多余的 `Realize Instances`，多用了 2 个节点。有 skill 时：节点保持默认名、解释集中在双语 frame、用临时 realize **验证**了实例数量后主动撤销、图精简到 9 个节点——代价是多几次 MCP 调用。一句话：skill 是**固化的约定和验证纪律**——那些你本来每次都要在提示词里重复的要求，和你忘了要求时模型就会跳过的步骤。

## 包含内容

- `skills/geometry-nodes/SKILL.md` — 构建循环、可靠性规则、几何节点心智模型（数据流通道 vs field 通道）
- `skills/geometry-nodes/rules/` — 30+ 个节点族参考，含精确 `bl_idname` 和 socket 名
- `skills/geometry-nodes/patterns/` — 验证过的图模式（散布、拼接、位移、密度控制散布、Repeat Zone 技巧等）

## 安装

一条命令，通用于 Claude Code、Codex、Cursor 等 agent（基于开源的 [skills CLI](https://github.com/vercel-labs/skills)）：

```bash
npx skills add monswag/nodecue-blender-node-skills
```

其他方式：Claude Code 用户也可以用 `/plugin marketplace add monswag/nodecue-blender-node-skills` + `/plugin install blender-node-skills@nodecue`；或克隆本仓库后把 `skills/geometry-nodes/` 手动复制到 agent 的 skills 目录。

skill 有意不捆绑运行时系统提示词：每个 agent 使用自己的行为指令，把这个 skill 当作领域知识来读。

## 连接 Blender

skill 不绑定特定的 Blender 访问方式：

- **Blender 官方 [MCP server](https://www.blender.org/lab/mcp-server/)**（Blender Lab 出品，随 5.2 LTS 内置，可作插件安装）——优先推荐
- 社区的 [blender-mcp](https://github.com/ahujasid/blender-mcp) 项目
- **[NodeCue Blender 插件](https://github.com/monswag/NodeCue)** — 内置同一套 skill 的 Blender 内 agent，使用你自己的 API key

## 注释语言

Frame 标注和解释默认跟随你提示词的语言——用中文描述需求，就得到中文的教学标注。节点名、socket 名等 Blender 术语始终保持英文原文，与 Blender 界面和主流教程对照一致。

## 范围与准确性

- **仅支持几何节点，Blender 5.0+。** 规则基于 Blender 5.0 手册；大部分测试在 5.1 上进行。节点行为在不同 Blender 版本间可能有差异。
- **Shader Nodes 和 Compositing Nodes 在计划中**，规则和模式验证完成后会作为同级 skill 文件夹加入。
- **结果仍可能出错。** skill 能大幅减少凭空编造的节点名和被丢弃的需求，但 LLM 驱动的构建仍可能产出错误的图或有误导性的解释——模型质量很关键。依赖结果之前请在 Blender 中检查节点图，遇到失败请反馈。

## 反馈

当 agent 读取了这个 skill 之后仍然把 Blender 节点任务做错时，请用 `Skill feedback` 模板开 issue。有用的报告包括：提示词、agent/工具名称、使用的模型、节点图哪里错了，以及可分享的回读 JSON 或截图。

请勿在公开 issue 中包含 API key、私有资产库路径或不可公开的 `.blend` 文件。

## 许可

MIT — 见 [LICENSE](LICENSE)。规则中的节点行为参照 [Blender Manual](https://docs.blender.org/manual/en/latest/)（CC-BY-SA 4.0）核验。
