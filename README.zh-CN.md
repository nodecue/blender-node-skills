[English](README.md) | 简体中文

# NodeCue Blender Node Skills

一个 agent skill，教 AI 编码 agent **正确构建 Blender 几何节点（Geometry Nodes）图——并对结果做出解释，让你能从中学习**：核验过的节点与 socket 标识、经过验证的图模式、基于回读的自我修复，以及跟随提示词语言的教学注释。

## 为什么要装它？

强模型不装它也能搭出能跑的图。skill 负责的是那些**你本来每次都要在提示词里重复的要求，以及你忘了要求时模型就会跳过的步骤**：

| 同一 agent，同一提示词 | 无 skill | 有 skill |
|---|---|---|
| 草叶散布，**带密度遮罩** | 遮罩被静默丢弃 | Noise → `Density Factor` 正确接线；暴露控制参数 |
| 沿曲线生成管道 | 截面从未接线——管道没有截面 | 接线正确；暴露 `Pipe Radius` |
| 可学习的产出 | 解释涂满被改名的节点，或干脆没有 | 节点保持默认名；双语教学 Frame；图更精简 |

数据来自 Codex + Blender MCP 对照实验（复现 harness 在 [NodeCue 仓库](https://github.com/monswag/NodeCue)）；对比截图即将补充。

## 安装

一条命令，通用于 Claude Code、Codex、Cursor 等 agent（基于开源的 [skills CLI](https://github.com/vercel-labs/skills)）：

```bash
npx skills add monswag/nodecue-blender-node-skills
```

其他方式：Claude Code plugin（`/plugin marketplace add monswag/nodecue-blender-node-skills`，然后 `/plugin install blender-node-skills@nodecue`），或克隆仓库后把 `skills/geometry-nodes/` 复制到 agent 的 skills 目录。

## 连接 Blender

skill 不绑定特定的 Blender 访问方式：

- **Blender 官方 [MCP server](https://www.blender.org/lab/mcp-server/)**（Blender Lab 出品，随 5.2 LTS 内置，可作插件安装）——优先推荐
- 社区的 [blender-mcp](https://github.com/ahujasid/blender-mcp) 项目
- **[NodeCue Blender 插件](https://github.com/monswag/NodeCue)** — 内置同一套 skill 的 Blender 内 agent，使用你自己的 API key

## 范围与准确性

- **仅支持几何节点，Blender 5.0+。** 规则基于 Blender 5.0 手册，大部分测试在 5.1 上进行。Shader Nodes 和 Compositing Nodes 计划作为同级 skill 文件夹加入。
- **注释跟随提示词语言**（中文提示词 → 中文教学标注）；Blender 术语始终保持英文，与界面和教程对照一致。
- **结果仍可能出错。** skill 能大幅减少凭空编造的节点名和被丢弃的需求，但模型质量很关键。依赖结果之前请在 Blender 中检查节点图，遇到失败请反馈。

## 反馈

当 agent 读取了这个 skill 之后仍然把 Blender 节点任务做错时，请用 `Skill feedback` 模板开 issue，附上提示词、agent/工具、模型和图错在哪里。请勿在公开 issue 中包含 API key、私有资产库路径或不可公开的 `.blend` 文件。

## 许可

MIT — 见 [LICENSE](LICENSE)。规则中的节点行为参照 [Blender Manual](https://docs.blender.org/manual/en/latest/)（CC-BY-SA 4.0）核验。
