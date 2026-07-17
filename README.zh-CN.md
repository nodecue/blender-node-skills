[English](README.md) | 简体中文

# NodeCue Blender Node Skills

一个 agent skill，教 AI 编码 agent **正确构建 Blender 几何节点（Geometry Nodes）图——并对结果做出解释，让你能从中学习**：核验过的节点与 socket 标识、经过验证的图模式、基于回读的自我修复，以及跟随提示词语言的教学注释。

## 为什么要装它？

同一个 agent（Codex app，gpt-5.6，extra-high 推理），同一句提示词，通过 Blender MCP 各跑一次——一次要求不借助任何 skill，一次用这个 skill：

> 在场景中添加一个立方体，2米大小，在立方体的顶部4个顶点处分别添加一个高0.2米，直径0.2米的圆锥。

| 无 skill | 有 skill |
|---|---|
| ![无 skill：每个节点都被改名并加了解释标签，成品图里留着多余的 Realize Instances，共 11 个节点](docs/images/comparison-no-skill.png) | ![有 skill：节点保持默认名，4 个双语教学 Frame，共 9 个节点](docs/images/comparison-with-skill.png) |

*左侧的提示词还额外要求了一句："并对节点使用 frame 进行功能性解释。"用了 skill 之后，教学 Frame 会自动生成——不需要额外提这一句。*

两次几何结果都是对的——这是个强模型。差异在于图里留下了什么：

- **节点命名**：每个节点都被改名并加上解释性标签（`Cube_2m`、"读取每个顶点的位置"、"Z > 0.99 = 顶部顶点"……）vs. 保持 Blender 默认名（`Position`、`Compare`、`Cone`……）。改名会切断节点图与 Blender 界面、以及任何默认命名教程之间的对照关系。
- **解释放在哪里**：涂满在各个节点的标签上 vs. 集中收纳进 4 个双语 Frame（"02 顶部四点 — Select Z > 0.99"）。
- **多余节点**：成品图里留着一个 `Realize Instances` vs. 只在验证数量（4 个圆锥）时临时用一下，随后撤销。
- **图的大小**：同样的结果，11 个节点 / 11 条连线 vs. 9 个节点 / 9 条连线。
- **成本**：4 次 MCP 调用（约 4 分 17 秒）vs. 7 次 MCP 调用（约 5 分 46 秒）——多出来的回读-校验-修复循环不是免费的。

在强模型上，skill 带来的不是"能跑 vs. 跑不通"的差距，而是**固化的约定**（默认命名、Frame、双语标签）和**验证纪律**（先检查再宣称完成）——省去了你每次都要在提示词里重申"请用 frame 解释"、并且自己去检查结果对不对。

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
