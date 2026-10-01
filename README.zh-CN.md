[English](README.md) | 简体中文

# NodeCue Blender Node Skills

> **已归档（2026-10-02），不再维护。**
>
> 2026-10-01 做过一次对照测试：Codex（`gpt-5.6-sol`）、Blender 5.2.2 加官方 Blender Lab MCP，题目是一道有 50 项检查的 Geometry Nodes 任务，每组跑 1 次：
>
> | | 得分 | Codex 耗时 | input tokens |
> | --- | --- | --- | --- |
> | 不用 skill | 50/50 | 183 秒 | 45.6 万 |
> | 本仓库 v0.7 skill | 50/50 | 273 秒 | 89.9 万 |
> | 只写交付规范的 1.6 KB 精简 skill | 50/50 | 223 秒 | 70.8 万 |
>
> 强模型配合官方 MCP，不用 skill 就能正确搭出节点图。v0.7 skill 的流程和脚本增加了对话轮次和上下文，却没有减少出错。出错大多是可以自行恢复的 Blender 5.2 API 变化，例如修改器输入要通过 `modifier.properties.inputs` 设置。只写交付规范的精简 skill 对可读性有帮助：保持 Blender 节点名、分组框有标题、节点不重叠。更难的问题，比如不报错但值是错的、结果"看起来"对不对，这类 skill 解决不了。
>
> 代码保留供参考，不再更新，issue 已全部关闭。

现在可以直接使用的，是已经发布的 **v0.7 几何节点 skill**，位置在 [`skills/geometry-nodes/`](skills/geometry-nodes/)。它由 [`SKILL.md`](skills/geometry-nodes/SKILL.md)、四份参考文件和四个脚本组成：

- 参考文件：[`nodes.tsv`](skills/geometry-nodes/references/nodes.tsv)、[`versions.md`](skills/geometry-nodes/references/versions.md)、[`reuse.md`](skills/geometry-nodes/references/reuse.md)、[`diagnostics.md`](skills/geometry-nodes/references/diagnostics.md)
- 脚本：[`find_nodes.py`](skills/geometry-nodes/scripts/find_nodes.py)、[`read_graph.py`](skills/geometry-nodes/scripts/read_graph.py)、[`probe_node.py`](skills/geometry-nodes/scripts/probe_node.py)、[`capture.py`](skills/geometry-nodes/scripts/capture.py)、[`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py)、[`verify_result.py`](skills/geometry-nodes/scripts/verify_result.py)

agent 用它搭建一份可以核对的几何节点图，也可以在不改动图的情况下解释一份已有的图。

> **状态。** 已发布的 **v0.7 几何节点 skill** 是当前稳定产品边界。公开 GitHub `main` 是产品和开发源。Codex plugin 已合入公开 `main`，但不是带 tag 的 plugin release。Codex plugin 已经完成**本地**验收，分两层。**A.** 在已安装 Codex plugin 的前提下，于本仓库之外启动的全新 Codex 任务自动发现了 `geometry-nodes` skill，自动获得了 Blender MCP tool，连接到 portable Blender 5.1.2，并以只读方式返回了真实版本、文件状态、活动对象，以及没有 GN modifier。这条路径证明 plugin 的 install、discovery、MCP entry 和 live read-only。**B.** 单独通过相同 blender-mcp transport 的 live host 测试已验证 Blender 5.1.2 portable 与 5.2.2 的目标实例识别和隔离，以及最小 GN create、nodes/links/socket readback、求值包围盒和视口证据。B 层由独立验收执行，不是 A 那个全新 Codex plugin 任务完成的，不能写成 plugin 端到端 mutation 或 image acceptance。在新机器或 VM 上从 GitHub 安装、Claude、Pi 以及其他宿主均未验证。本项目仍在演进。在依赖某一次安装或某一个 host 之前，请先看最新的 README、[Releases](https://github.com/nodecue/blender-node-skills/releases) 和 [Issues](https://github.com/nodecue/blender-node-skills/issues)。欢迎根据真实 host 上的实际使用来反馈。

## v0.7 skill 做什么

1. 读取 Blender 版本和当前节点图。
2. 用 `references/nodes.tsv` 筛选候选节点。这个文件是路由索引，不能拿来直接连线。
3. 连线之前，在正在运行的 Blender 里确认节点、socket 和属性的身份。
4. 搭建、修改或解释时，按可以单独核对的小段进行。解释模式只读，不改图。
5. 核对的是从请求推导出来的结果。节点个数只说明图本身。尺寸、位置，或请求里明确要的数量，才是该核对的内容。
6. 请求要求改图时，保留 Blender 的默认节点名，把解释写在教学 Frame 上。

任务需要时，可以使用 [`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py)。它不能代替对 Blender 的实时读取。

## 安装独立 skill

NodeCue 目前没有一条已经验收、可以同时覆盖 Claude Code、Codex、Cursor、Pi 和其他 agent 的安装命令。skill 放在哪里、host 如何发现它，彼此不同。请按你正在使用的那个 agent 的现行 skill 安装文档操作。

**手动路径，不限定哪一个 host。** 克隆或下载本仓库，把 [`skills/geometry-nodes/`](skills/geometry-nodes/) 放到该 agent 安装能够识别 skill 的位置。

**便利命令。** 下面是现有的 [skills CLI](https://github.com/vercel-labs/skills) 命令。NodeCue 还没有完成它在各个 host 上的行为验收。它不会配置 Blender，也不会安装下文那个 Codex plugin。

```bash
npx skills add nodecue/blender-node-skills
```

## 把 agent 接到正在运行的 Blender

这个 skill 不建立 Blender 连接。它要求一条已经可用的执行通道。这条通道必须在正在运行的 Blender 内部执行随仓库发布的 Python，并把结果返回来。Blender 外面的 host Python 看不到当前打开的文件。

这里说明的接入方式是官方 [Blender Lab MCP](https://projects.blender.org/lab/blender_mcp) 的 stdio 通道。按上游命令安装 server：

```bash
pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp
```

Blender 扩展需要单独安装：添加 Blender Lab Extensions 仓库（`https://lab.blender.org/`），找到并安装 MCP 扩展，启用后从扩展偏好设置中启动 server。步骤由上游维护，之后可能变化。本仓库的 MCP client 命令是 `blender-mcp`，不带参数，见 [`.mcp.json`](.mcp.json)；确保 host 能从 `PATH` 找到该命令，配置后重启 MCP client。

连接后，使用以下只读冒烟提示词：

> 不要修改任何内容。请返回 `bpy.app.version_string`、当前 `.blend` 文件路径（`bpy.data.filepath`），以及活动对象名称（没有则返回 `none`）。

返回的信息与预期打开的 Blender 窗口一致，才算通道已接通。如果 host 无法返回这些值，请先不要继续操作。

**Blender Lab MCP** 的运行下限是 **Blender 5.1 或更新**。这个下限与 v0.7 skill 在 [`versions.md`](skills/geometry-nodes/references/versions.md) 和 `nodes.tsv` 里对 Blender 4.5 LTS、5.0 的知识覆盖是分开的。skill 路由仍然记录这些更早版本；Lab MCP 不能在它们上面运行。

## Codex plugin（已合入公开 main）

把这个 skill 打包成 NodeCue 的 agent plugin，是已发布的 v0.7 skill 之外的另一项工作。Codex plugin 已合入公开 `main`，但不是带 tag 的 plugin release。本地验收就是下面两层。plugin 命令不是安装 v0.7 skill 的通用已验证方式。

本地 Codex 证据，分两层：

- **A. 全新 Codex plugin 任务（live read-only）。** 在已安装 Codex plugin 的前提下，于本仓库之外启动的 Codex 任务自动发现了 `geometry-nodes` skill，自动获得了 Blender MCP tool，连接到 portable Blender **5.1.2**，并以**只读**方式返回了真实版本、文件状态、活动对象，以及没有 GN modifier。这条路径证明 plugin 的 install、discovery、MCP entry 和 live read-only。
- **B. 单独的 blender-mcp transport / live host 测试。** 独立验收通过相同 blender-mcp transport，已验证 Blender **5.1.2 portable** 与 **5.2.2** 的目标实例识别和隔离，以及最小 GN **create**、nodes/links/socket **readback**、**求值包围盒**和**视口证据**。B 层不是 A 那个全新 Codex plugin 任务完成的。它不是 plugin 端到端 mutation 或 image acceptance。

仍未验证：在新机器或 VM 上从 GitHub 安装；Claude；Pi；其他宿主。packaging 与安装步骤仍可能变化。

已提交的 [`.claude-plugin/`](.claude-plugin/) 元数据，即 [`plugin.json`](.claude-plugin/plugin.json) 和 [`marketplace.json`](.claude-plugin/marketplace.json)，记录的是早期的 Claude 封装表面。它不能证明当前的 Claude host 已经接受这个 plugin。那些早期 Claude plugin 命令不是推荐或已验证的安装路径。它们不会配置 Blender。Claude 兼容性先留在仓库里，等以后再验证。

## 第一次使用

这条路径只使用本公开仓库。

1. 安装或找到独立 skill，目录是 `skills/geometry-nodes/`。
2. 按上面的步骤连接 Blender，并通过只读冒烟检查。
3. 启用几何节点 skill，从一份测试用 `.blend` 开始。
4. 提出搭建、修改或解释的请求，然后在 Blender 里查看求值后的结果。节点图看起来整齐，并不等于结果正确。
5. 失败时，用 [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) 模板开 issue。写上提示词、agent 或工具、模型、Blender 版本，以及结果错在哪里。不要放入 API key、凭据、私有资产库路径，以及不能公开的 `.blend` 文件。

## 范围与准确性

- **只有几何节点。** Shader Nodes 和 Compositing Nodes 都没有发布。
- **带版本的证据用来路由，不是行为保证。** [`versions.md`](skills/geometry-nodes/references/versions.md) 和 `nodes.tsv` 的 `version` 列覆盖 Blender 4.5 LTS、5.0、5.1 和 5.2 LTS。它们记录候选节点出现在哪些版本，以及一部分跨版本差异长什么样。它们不保证同一张图在这些版本上行为一致。skill 对 4.5 和 5.0 的知识覆盖，与要求 Blender 5.1 或更新的 Blender Lab MCP 是分开的。
- **当前身份以正在运行的 Blender 为准。** 节点、socket、属性和 RNA 身份，以及合法取值，都从你连上的那一个 Blender 读取。
- **从输入参考重建节点图，没有随这个版本发布。** 对求值结果做自动视觉质检，也没有发布。[`capture.py`](skills/geometry-nodes/scripts/capture.py) 截取的是节点编辑器。它不判断最终的渲染或视口求值结果。
- **请求要求改图时，Frame 注释跟随提示词的语言。** 节点、socket 和标识符保持 Blender 显示的原文，以便和界面、教程对照。
- **结果仍然可能是错的。** 早前的静态检查和运行时回归记录，不等于 Claude、Codex 或任何其他 host 上的验收。本 README 不把那些早前运行写成当前的通过结论。在依赖节点图之前，先查看 Blender 里求值后的输出。

## 反馈

请使用 [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) 模板。说明你问了什么、用的 agent 和模型、当时的 Blender 版本、执行通道是怎么接上的，以及求值结果实际怎样。只提交可以公开的证据：不要包含 API key、凭据、私有路径，或不能公开的 `.blend` 文件。

## 许可

MIT。见 [LICENSE](LICENSE)。当前身份和行为以正在运行的 Blender 为准。
