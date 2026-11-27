# 设计稿审计：CAD Agent 系统设计（复审 2026-11-27）

- **当前审计对象**：[CAD Agent 系统设计 v5](2026-11-27-cad-agent-design.md)
- **审计基准**：`README-zh.md` / `README.md` 的作业要求
- **证据范围**：审计已复跑 SCA 2.3.0.post1 的手写 notebook 和直边 STEP 截面样件；正式生成器、完整 Agent、Web、`sca edit`、超时终止和 VLM 流程未做端到端验收。

<a id="current-audit-status"></a>

## 当前结论（v5）

**旧稿的 5 项高优先级和 8 项中优先级问题不是当前待修清单。** 原设计缺口已修订；其中 **H5 的课程限制口径和实际隔离方案仍待确定**。其余需要补的是实现和运行证据，或团队按试测作出的选型决定。下表是当前状态；[v4](#v4-audit-followup)、[v5 修订记录](#v5-audit-followup)及 v3 历史正文用于追溯，不覆盖本表。

| 编号 | v5 状态 | 结论或待验收证据 |
|---|---|---|
| B1 | **原问题已关闭** | 手写 T1 notebook 三组可复现。新交付契约要求 T1–T3 的正式生成源各自在新进程原样重建、单参改值并回读验收，尚待实测。 |
| B2、B3 | **设计已修订** | Web 是底线，PNG + STEP 仅替换查看方式；测量编号、选择器和命中数已有明确契约。Web 和通用测量层尚待联调。 |
| R1、R2、R4 | **设计已修订，有样件证据** | 参数与本轮快照绑定，T3 臂长基准和 STEP 测厚对象明确；两种宽度的直边样件已复跑，正式验收层须通过错选和壁厚超差反例。 |
| R3、R5、H4 | **设计已修订，仅在 T4 启动时验收** | 图像解读需确认，支撑角带朝向，双侧托唇分别验高，另验反倾、外伸和缺口被挡。T4 不是底线。 |
| H1、H2、H3 | **设计已修订** | 明确重试预算，保留 T3 复杂度基线，补需求映射和改参继承。实际重试、确认和复测轨迹待联调。 |
| H5 | **待确认、待验证** | 已区分工具路径白名单与生成代码的进程权限。P1 须确认课程认可的限制级别、选定执行方式，再验证越权写入拒绝与超时终止。 |
| M1、M4、M5、M8 | **设计已修订** | 已补版本清单、提交材料、报告大纲、自主与复用矩阵、SCA Skill 引用。实际产物随实现交付。 |
| M2、M7 | **设计已修订，待联调** | 必须证明真实 Agent 改方案才能修复；两类重试预算独立验。前后模型用共用取景范围，并实测两条展示路径的尺度。 |
| M3 | **版本处置规则已定，待实测** | marimo 0.26.0 无缓存样件已复现；自动生成、`sca edit` 和缓存路径待验证，再锁定版本。 |
| M6 | **旧口径已替换** | 60 人时缓冲不是现行指标。v5 按 148 人时基础任务、12–28 人时缓冲规划，仍需核算实际工作日。 |
| 编辑项 | **已修订；模型阈值待试测** | 编辑性缺口已处理。文本模型及通过阈值按已定流程先试测、再由团队确认，不算审计遗漏。 |

### 接下来要处理

1. **前置确认：**确定 H5 的受限执行口径与工作进程方案；验证生成器和 marimo 路径；按真实工具 schema 试测文本模型与通过阈值。
2. **基础联调：**用 T1–T3 正式交付源验证重建与改参；保留真实 Agent 修复、旧约束复测、失败回退、超时终止和 Web 同尺度展示的运行证据。
3. **可选联调：**只在 T4 进入范围后补 VLM 确认与 T4 反例结果。

<a id="v4-audit-followup"></a>

## v4 补全记录（2026-11-27，历史）

| 审计条目 | 补全结果 |
|---|---|
| B1/B2/B3 | 保留 notebook 实测证据、Web 底线和测量接口。 |
| R1–R2 | 从本轮确认快照解析测量实参，日志留存解析值。T3 分别指定底面和外墙来测臂长，并给出截面坐标图。 |
| R3–R5 | T4 改用带朝向的截面角度，规定 115° 反例。占地按用户确认包含底座和托唇足迹。壁厚和缺口从候选 STEP 回读后测；直边 T3 探测线两种宽度均已实测。[截面复现](../../research/experiment/README.md#step-截面探测验证) |
| H1/H3 | 总执行最多 4 次，每类最多 2 次修复，同因连续失败 2 次终止。确认清单补原话到约束的映射及阻塞项反馈。 |
| H2/H4 | Web 和 T1/T2/T3 为必做，T4 为可选第四组。报告记录模型复杂度。T4 若启动，先由用户确认图像解读，再进行建模和人工预览。 |
| H5/M2/M7 | 明确确定性生成、受控输出目录和失败恢复。规定超差、执行异常、超时和持续失败 fixture，以及 Web 前后展示和真实视频验收。 |
| M1/M4/M5/M8 | 补版本清单、提交物对照、报告结构与 SCA Skill 的适用范围。 |
| M3/M6 | marimo 按无缓存、编辑器和缓存三条证据判断。容量按工作日以上限 176 人时估算，基础工作预计 148 人时，实际容量决定缓冲。 |
| 低优先级编辑项 | 澄清 T1 几何证据、外部参数 JSON、调研推断、渲染封装名、孔径和阶梯轴基准。补限流、成本和视觉误读风险，统一基础工具与额外项口径。 |

文本模型及通过阈值按用户决定先实测，再提交团队确认。表中 fixture、运行时检查、编辑器和可选 T4 属于设计层验收约定，执行状态以实际运行证据记录。[修订后设计稿](2026-11-27-cad-agent-design.md)

---

## 0. v3 审计快照：已核实项

第 0–7 节保留 2026-11-27 对 v3（约 465 行）的评审现场。小节中的「现状」「未修」和原建议均指 v3 当时，不是当前状态；[回到 v5 状态表](#current-audit-status)。

| 设计稿声明 | 复核结果 |
|---|---|
| SCA 2.3.0.post1 | ✅ 与 `experiment/requirements.txt`、实验 README 一致 |
| `sca ops` 200 个带类型标注的操作 | ✅ `ops_dump.json`：200 个操作，935/935 个参数有类型 |
| SCA `editor` extra 仅 starlette/uvicorn/websockets，不含 FastAPI | ✅ 安装元数据确认 |
| marimo 警告 `checked against 0.25, found 0.26.0` | ✅ 可复现；`RuntimeWarning`，不是硬失败（`runtime/_marimo.py:128-143`） |
| `scad.var`、`Expr`、`ExpressionGraph`、`ToleranceGraph`、`GraphSession`、`OperationGraph`、`export_graph_json`、`import_graph_json`、`replay_graph`、`export_session_json`、`ql`、`run_notebook` | ✅ 均存在于 2.3.0.post1；`replay_graph(graph, *, strict=True)` 确无参数覆盖；`run_notebook(path, *, overrides=...)` 存在 |
| 每个参数必须独立成一个 cell | ✅ `runtime/runner.py:470-472` 报错原文一致；SCA 官方 Skill 的 `notebook-cell-design.md` C8 也支持该规则 |
| **notebook 交付样件（B1）** | ✅ **本轮实际复现**：`verify_notebook.py` 退出码 0；before/after/off_target 的 `measured_mm`、`volume_mm3`、`accepted`、`runtime_warnings` 与留存 `run.json` 完全一致 |
| notebook 每参数独立 cell | ✅ `offset_plate.py` 中 length/width/thickness/hole_d/hole_x/hole_y 各占一个 cell |
| T1 几何与验收基线 | ✅ `experiment/results/` + `cases.json`，数值与设计稿一致 |
| **测量接口（B3）** | ✅ 已列出 12 个 `measurement.id`、`args`、量纲与前置条件；选择器有 `expected_count`、`geometry`、`direction`、`at_extreme`、`adjacent_to` 等字段；圆角前有 selection card + 高亮图；T3 壁厚/夹角、T4 底座/倾角均有具体基准 |
| T2/T3/T4 端到端、自动生成 notebook、`sca edit`、超时终止、VLM 候选 | ⏳ 设计稿为计划，仓库无产物 |

---

## 1. v3 审计快照：需求覆盖矩阵

| README 要求 | 设计稿位置 | 状态 | 说明 |
|---|---|---|---|
| 需求理解：提取结构、尺寸、单位、位置关系；缺失/冲突先询问 | INTAKE/CLARIFY、约束集、确认规则 | ✅ | 覆盖较好；但未要求批量提问，T4 缺"描述并确认图片解读形状"（H4） |
| 建模执行：工具调用或生成程序驱动 SCA；实体、布尔、至少一种特征操作；关键尺寸参数化 | 工具层、T1 拉伸+切除、T3 圆角、notebook/`scad.var` | ✅ | notebook 证据已补齐（B1）；自动生成器仍待 D4–5 |
| 检查修正：有效性、实测尺寸/位置、反馈、重试上限、不得以无异常为成功 | 两份契约、双计数器、状态机、测量接口 | ✅ | 测量契约已可执行（B3）；重试上限仍无数值（H1）；有效性门禁未写明 |
| 交互修改：同会话改尺寸/局部特征、保留未改需求、前后展示、保存源文件、STEP、日志 | 版本规则、`runs/`、DELIVER | ✅ | 版本规则完整；"前后模型并排展示"未进入必须通过的轨迹（M7） |
| 测试分析：≥3 组结构不同，覆盖澄清、多轮修改、错误修正；验收条件+容差；记录成功、偏差、耗时、修复次数、失败原因 | T1–T3、必须通过的轨迹 | ✅ | 结构完整；故障注入与逐任务失败分析模板未定义（M2） |
| 进阶：图片+文字、装配、经验复用；复杂度是评分指标 | T4 额外承诺、T5 stretch | ⚠️ | 图片路径有设计；复杂度被明确降权，与 README 评分口径冲突（H2） |
| **交互界面：命令行或简单界面** | **Web 界面（D14–17）** | ✅ | **Web 定为底线，不再可放弃（B2 决议）**；降级为 PNG + STEP 下载 |
| 自主实现工具封装、流程控制、结果校验；用框架须说明模块与验证结果 | 自主实现边界表 | ✅ | 边界清楚；报告缺逐模块"自主/复用 + 验证证据"映射（M4） |
| 工具选择：SCA、模型版本、受限执行、超时 | 约束表、执行边界 | ⚠️ | SCA/marimo/Python/OS 已进 `run.json`；LLM 模型 ID/配置、提示词/工具 schema 版本未列为交付项（M1）；受限执行表述需补（H5） |
| 提交材料：代码、提示词、工具定义、测试需求与结果、源文件、STEP、日志、配置与运行说明、视频、4–6 页报告 | 交付物列表 | ⚠️ | "测试需求""配置和运行说明"、参数化源文件的具体文件集未显式列出（M5） |
| 视频：需求输入、自动建模、反馈修正、多轮修改 | 排期 D29–30 | ✅ | 需明确"提交视频必须是真实运行录屏，`--replay` 只作现场备份"（M7） |
| 报告：系统设计、测试结果、自主工作、成员分工 | 分工表、评审处理 | ⚠️ | 无报告大纲；未映射 README 四项（M4） |

---

## 2. v3 审计快照：阻塞问题复审

### B1. notebook 交付验收 —— 已解决

**原问题**：设计稿声称"新进程，仅凭 notebook + 参数"已实测，但仓库中没有 notebook、`run_notebook` 日志或输出，无法复现。

**修订内容**：

- 新增 `docs/research/experiment/notebook/offset_plate.py`：6 个 `scad.var` 各占一个 cell，末尾 `make_part_rpart` 输出 Part。
- 新增 `docs/research/experiment/notebook/README.md`：复现命令、留存结果、能力边界。
- 新增 `docs/research/experiment/verify_notebook.py`：用 `ProcessPoolExecutor(spawn, max_tasks_per_child=1)` 为每个工况开独立进程，调用 `run_notebook(overrides=..., cache=False)`，导出 STEP 并复用 `plate.py` 的 `check()` 回读判定。
- 新增 `notebook/results/run.json` 与三份 STEP。

**本轮复核**：在 `docs/research/experiment` 执行

```powershell
.venv/Scripts/python.exe -B verify_notebook.py --out <临时目录>
```

退出码 0；三组 `measured_mm`、`volume_mm3`、`accepted`、`runtime_warnings` 与留存 `run.json` 完全一致：

| 工况 | 留存 accepted | 复跑 accepted | 实测一致 | 体积一致 |
|---|---|---|---|---|
| before | true | true | ✅ | ✅ 31371.681469282106 |
| after | true | true | ✅ | ✅ 30768.49567979288 |
| off_target | false | false | ✅ | ✅ 30768.49567979285 |

**结论**：B1 关闭。"只改孔径、孔位保留"和"孔位反例被拒"都有可复现证据。

**仍需注意**：

- 该 notebook 是**手写**交付样件；设计稿已如实写明"自动生成器和 `sca edit` 界面仍待 D4–5 验证"。
- `run_notebook` 使用 `cache=False`；缓存路径未验证。设计稿已写明"缓存功能仍待验证"。
- 建议在报告中把"手写样件"与"自动生成"分开表述，避免读者误以为自动生成器已通。

### B2. Web 定位 —— 已解决（团队决定）

**原问题**：设计稿把 Web 列为额外承诺且可放弃，但 README 要求"命令行或简单界面"；Web 一降级，基线交互入口落空。

**团队决定**：Web 不可放弃，定为底线。

**设计稿同步修改**（本轮已写入）：

1. 头部版本：`v2` → `v3：补 notebook 交付证据与可执行测量接口；Web 定为底线。`
2. 人时口径：底线改为"T1/T2/T3 + Web 交付链路"；放弃顺序改为"复杂件 → 图文"；176 人时下限保住"底线三例与 Web"。
3. 额外承诺进入条件：删除 Web 行，注明"Web 为底线，不设进入条件，按 D14–17 排期执行"。
4. 降级线：补"Web 不因降级取消，改用 `render_screenshot_rpath` 的 PNG + STEP 下载视图"。
5. 风险表：新增"Web 集成超期"行，限定 Web 范围（聊天、视图、参数表、STEP 下载）与三维查看降级。
6. 评审处理表：新增"Web 可被放弃，缺基线界面 → 定为底线"行。

**结论**：B2 关闭。

**仍需注意（不阻塞）**：

- Web 现在是底线，D14–17 只有 4 天；若 D13 底线三例未全通过，Web 仍须开工，排期压力后移。建议 D10–13 结束时做一次 Web 接口契约冻结（P2↔P3 的约束集 JSON 与候选目录结构），避免 Web 阶段返工。
- Web 的"三维查看"依赖 `sca edit`；若 notebook 降级为脚本，Web 必须走 PNG + STEP 下载。建议在 Web 验收条件中同时列出两条路径，而不是只写"嵌入 `sca edit`"。
- "命令行或简单界面"已由 Web 满足；CLI 仍可作为调试入口，不必再列为交付要求。

### B3. 测量契约 —— 已解决，含 5 项残留

**原问题**：固定词汇表表达不了 T3 夹角、T4 倾角；`exactly(1)` 与"命中数须为声明值"冲突；selector 没有语法；圆角缺少选择证据；T4 底座用整体包围盒会被斜撑污染。

**修订内容**：新增两节：

- **测量接口（P1 ↔ P4）**：12 个 `measurement.id`，每个有 `args`、量纲、前置条件：
  `axis_plane_distance`、`diameter`/`radius`、`plane_spacing`、`axis_angle`、`axis_offset_at_section`、`plane_normal_angle`、`dihedral_angle`、`edge_angle`、`projected_span`、`section_wall_thickness`、`section_gap`、`through_hole`。
- **选择器与命中数**：`{"kind": "face|edge|solid", "expected_count": n, "where": {...}}`；`where` 支持 `geometry`、`tag`、`center_window_mm`、`axis_window_mm`、`direction`、`at_extreme`、`adjacent_to`；统一 `.exactly(n)`；0/过少/过多返回 `selection_mismatch`。
- **圆角/倒角前置证据**：selection card（选择器、预期/实际命中数、边长与中心或面中心与面积）+ 高亮图；`highlight_tags` 与 `highlight_edges` 同次预览。
- **T3**：两个测厚截面（水平臂 `x=20`、竖直臂 `z=20`）、内二面角、圆角前后两步检查。
- **T4**：支撑角用 `plane_normal_angle`；底座长宽用底面有界轮廓的 `projected_span`；托唇高度用 `plane_spacing`；缺口用 `section_gap` + `plane_spacing`。

**结论**：原 B3 的 7 个具体缺口均已关闭。以下是复审中发现的残留，建议在 D6 规格冻结前处理。

#### R1. 测量参数未与已确认参数绑定（高）

**问题**：`args` 目前是字面量，但多个测量依赖本轮确认的参数：

- T3 `section_wall_thickness` 的 probe 点 `(20, W/2, 0)` 依赖宽度 `W`；
- T2 `axis_offset_at_section` 的 `section` 依赖两段长度 30/20 的交界位置；
- T4 的局部位置窗口依赖设备尺寸。

改参后若不复算 `args`，探针或截面可能偏离预期位置；轻则测到非预期区域，重则测量失败。设计稿只写了"`expected_count` 由特征意图和已确认约束声明，重试与改参沿用"，没有说明 `args` 如何随参数更新。

**影响**："改参保约束"轨迹（T1/T3）要求改参后全量重测；若 `args` 冻结，重测可能在错误位置进行。

**建议**：

- 允许 `args` 引用已确认参数 ID（小表达式，例如 `{"expr": "W/2"}`），或由 harness 每轮按约束的 `statement`/`source` 重算；
- 在测量日志中记录**解析后的实参**（不仅是表达式），便于复核；
- 在 T3 宽度修改用例中明确验证 probe 随 `W` 移动。

#### R2. T3"两臂外侧平面"歧义（中）

**问题**：设计稿写"用两臂外侧平面的有界轮廓做 `projected_span`，分别实测两臂外长 40 ±0.1 mm"。若"外侧平面"指端面（`x=40`、`z=40`），投影得到的是壁厚 4 mm，不是臂长 40 mm；若指外表面（水平臂底面 `z=0`、竖直臂外墙面 `x=0`），投影才得到臂长。

**建议**：在 T3 夹具中写明具体面与 selector，例如"水平臂底面 `z=0`、法向 `-Z`、预期 1 面；竖直臂外墙面 `x=0`、法向 `-X`、预期 1 面"，并配一张坐标示意图。

#### R3. `plane_normal_angle` 无向，无法区分 65° 与 115°（中）

**问题**：`plane_normal_angle` 取 `acos(abs(dot))`，范围 0–90°。T4 支撑角若被建成 115° 的悬挑面，检查仍返回 65°，会放过错误几何。

**建议**：

- 增加方向谓词（例如支撑面法向的 `+Y` 分量为正），或提供带符号的倾角测量；
- 在 T4 夹具中加一个 115° 反例，证明检查能拒绝；
- 若保留无向角，至少在报告中说明该假设的适用范围。

#### R4. `section_wall_thickness` / `section_gap` 的测量对象未定（中）

**问题**：契约写"切割最终实体后沿探测线取…"，但验收路径是 STEP 回读。需要明确：是在内存实体上切，还是在导入的 STEP 上切。

- 若只在内存实体上测，这两项失去"STEP 回读独立验收"的意义；
- 若在 STEP 上切，需验证 OCCT 可对导入实体做布尔/切割。

**建议**：在契约中写明执行对象；若在 STEP 上执行，补一条实测（导入 STEP → 切割 → 测厚）；若在内存实体上执行，则明确这两项与 STEP 回读的关系，并在报告中说明。

#### R5. T4 底座长宽是否含托唇未定义（低）

**问题**：底面外轮廓包含托唇足迹；若托唇外伸，长宽会把它算进去。设计稿只写了"斜撑伸出底座的部分不计入"，没有说托唇。

**建议**：明确"底座长宽"是否含托唇；若不含，改用不含托唇的截面或面。

---

## 3. v3 审计快照：高优先级问题

### H1. 重试上限仍无数值与计数口径

**现状**：设计稿多处写"重试上限 / 修复预算 / 双计数器"（目标、状态机、轨迹表、排期），但全文仍无数字，也未说明"同一 cause 连续失败"如何计数。

**依据**：README 明确要求"设置重试上限"（`README-zh.md:13`）；SCA 官方 Skill 的 `failure-and-repair.md` 建议"同一检查、同一原因连续失败两次就不要再原样重试第三次"，按 cause 计数。

**建议**：写死并写入配置与日志：

- 执行异常与几何超差各自计数；
- 同一 cause 连续失败 ≤2 次，总尝试 ≤4 次（首次另计）；
- 达到上限 → `FAILED`，保留最后证据，报告剩余未通过项。

### H2. 复杂度仍被降权，与 README 评分口径冲突

**现状**：`设计稿:9` 仍写"作业给分点集中在'流程是否可信'而不是'几何是否炫技'"；复杂件仍是额外承诺，且是缓冲耗尽时第一个放弃的。

**依据**：README 明确写"同学们创建模型的复杂度也是成绩评价指标之一"（`README-zh.md:19`）。

**建议**：

- 改为"流程可信是底线，复杂度是加分项"；
- 底线范围内至少保留一个中等复杂度件（例如 T3 增加 boss/rib/多圆角，或把 T4 提升为底线备选）；
- 测试报告记录复杂度指标（特征数、布尔次数、圆角/阵列数、实体数）。

### H3. CONFIRM 仍缺"需求→约束"的完整性检查

**现状**：新增的三项检查是"覆盖（本轮每条生效的几何约束有合法测量）、解析、判定"。它保证"已确认的约束都有测量"，但仍不保证"用户说过的每条需求都变成了约束"。

**依据**：SCA 官方 Skill 的 `requirement-refinement.md` 要求"每条 blocking answer 和每条 user-stated requirement 都映射到一个 targeted measurement 或 rendered view，且在第一次建模调用前写下"。

**建议**：在 CONFIRM 增加"需求覆盖"：

- 把用户请求解析成需求列表；
- 每条需求映射到一个约束（含 measurement）或显式标注"本轮不做/待确认"；
- 在确认清单中展示这个映射；
- 增加轨迹："用户提出但未建模的需求被显式列出/拒绝"。

### H4. T4 仍缺"描述并确认解读形状"

**现状**：T4 澄清项仍是设备尺寸、支撑角度、横竖放、充电避让缺口；没有"描述解读出的形状并与用户确认"。

**依据**：SCA 官方 Skill 的 `requirement-refinement.md` 明确要求：图片含参考结构时，必须先描述整体形态、可见特征及位置、朝向、隐藏或不确定处，并在任何几何之前确认；不能用记录的假设替代。

**建议**：

- T4 澄清增加"解读形状描述 + 用户确认"，写入确认清单；
- 增加一次渲染视图供人工核对形态；
- 报告中如实说明：VLM 提供建议值，形态由用户确认。

### H5. 受限执行的合规表述与路径控制

**现状**：设计稿仍只写"时间上限 + 进程树终止 + 指定输出目录"，不声称文件系统/内存隔离。

**依据**：README 要求"生成代码应在受限环境中执行，并设置执行超时"（`README-zh.md:25`）。

**建议**：

- 明确主路径是工具调用，不是模型生成任意代码；notebook/脚本是确定性生成物；
- 工具 schema 只接受逻辑输出名，不接受路径；由 harness 解析到 `runs/<run-id>/attempt-<n>/`；
- 报告写明三段式边界；增加负向测试"工具尝试写出输出目录 → 被拒绝"。

---

## 4. v3 审计快照：中优先级问题

### M1. 版本记录不完整（部分改善）

**现状**：`notebook/results/run.json` 已记录 SCA、marimo、Python、platform；但 LLM 模型 ID/配置、提示词版本、工具 schema 版本仍未列为交付项。

**建议**：增加 `version-manifest.json`（SCA、marimo、Python、OS、uv/pip lock、LLM provider/model ID/temperature、prompt version、tool schema version），每次运行记录一份。

### M2. 故障注入与测试脚本仍未定义

**现状**：T2 的 A/B 修复用例、重试耗尽、超时恢复仍写"预置"，没有注入方式。

**建议**：定义固定 fixture：

- `--fault small_dia=14`（几何超差）；
- `--fault tool=cut_rsolid:invalid_radius`（执行异常）；
- `--fault sleep=<s>`（超时）；
- `--fault persistent`（重试耗尽）；
- 故障在工具层注入，测试日志记录完整命令；
- 另加一个"同轴度/夹角能失败"的反例，证明检查有效。

### M3. marimo 版本处置（证据已更新）

**现状**：设计稿仍写"实测报 checked against 0.25, found 0.26.0；D4 前钉回 0.25.x"，风险表仍写"编辑器接入失败"。

**新证据**：`notebook/results/run.json` 显示在 marimo 0.26.0 下，`run_notebook(cache=False)` 成功完成三组改参、导出与回读；只有一条 `RuntimeWarning`。这说明 0.26.0 对**无缓存运行**是可用的。

**建议**：

- 区分两条路径：`run_notebook(cache=False)` 已在 0.26.0 验证；`sca edit` 编辑器交互与缓存仍待验证；
- 若编辑器在 0.26.0 正常，不必降级；若异常，再钉 0.25.x 并重跑 notebook 检查；
- 在报告中写清"警告非致命"与最终选择。

### M4. 报告 / 自主工作 / 分工映射仍缺失

**建议**：增加报告大纲：

1. 系统设计与调用链；
2. 测试结果（逐任务/逐轨迹）；
3. 自主工作表（模块 | 自主/复用 | 验证证据）；
4. 实际成员分工与贡献。

明确写"未采用现成 Agent 框架"（如果属实），并列出复用的库（SCA、marimo、Starlette）与自研部分（工具封装、流程控制、结果校验）。

### M5. 提交清单仍与 README 不完全对齐

**建议**：改成 1:1 清单，并规定每次运行的文件集：

- notebook/脚本（参数化源文件）；
- `OperationGraph`/session JSON（如使用）；
- STEP；
- 前后视图 PNG；
- 对话、工具调用、验收日志；
- 版本清单；
- 运行命令；
- 测试需求（用户原话 + 澄清答复）。

### M6. 排期仍未体现 60 人时缓冲

**现状**：240h 容量、180h 计划、60h 缓冲；30 天排期填满所有天，D29–30 只标"演示视频 + 缓冲"（16h）。Web 改为底线后，D14–17 的压力更大。

**建议**：给每个里程碑加人时估算，合计 180h；显式写出 60h 缓冲的分布（例如每天 1.5–2h 余量 + D29–30）。

### M7. 前后模型展示、状态机重试边、笔误

- `README-zh.md:14` 要求"展示修改前后的模型"；设计稿只把"前后视图"列为交付物，未进入必须通过的轨迹或 UI 验收。建议增加轨迹："改参后并排展示前后模型（同视角/同尺度）"。
- 状态机仍无 `REPAIR → CANDIDATE/VERIFY` 的重试边；建议补上并标注计数器。
- `设计稿:416` 仍写"三人联调"，团队是四人；改为"四人联调"或"跨角色联调"。
- 视频要求：明确"提交视频必须是真实运行录屏；`--replay` 只用于现场答辩备份"。

### M8. 仍未引用 SCA 官方 Skill 规程

**现状**：设计稿仍未引用随 SCA 安装的官方 Skill 文档。

**建议**：在"自主实现边界"中加一段"参考了哪些 Skill 规程，哪些部分自研"，至少引用：

- `domains/requirement-refinement.md`：Ask-or-Record、brief 格式、图片必须描述并确认；
- `discipline/geometric-validation.md`：validity ≠ positive volume、每次布尔后检查、selection evidence gate、`.exactly(n)`；
- `discipline/failure-and-repair.md`：同一 cause 失败两次即停止、不得削弱检查；
- `discipline/notebook-cell-design.md`：C8 参数 cell、每 cell 一个特征。

---

## 5. v3 审计快照：低优先级 / 编辑项

| 位置 | 问题 | v3 时状态 |
|---|---|---|
| `设计稿:327` | "T1 已有实测基线"表述过强；实验是几何/验收基线，不是端到端 T1 Agent 运行 | 未修；建议改为"几何与验收基线" |
| `设计稿:141` | 说 `plate.py` 是"参数集中在文件顶部"，实际参数在 `cases.json` | 未修；建议改为"参数集中在外部 JSON" |
| `设计稿:61` | "Zoo 是唯一产品级验证过该形态的"是分析推断，不是调研结论 | 未修；建议标注"分析推断" |
| `设计稿:162` vs `:166` | `measurement` 示例是公式，规则要求词汇表项 | **已修**：改为 `id` + `args` |
| `设计稿:171` vs `:283` | `exactly(1)` 与"命中数须为声明值"冲突 | **已修**：统一为 `expected_count` |
| `设计稿:297` | 工具名 `render_view` 与实验用的 `render_screenshot_rpath` 不一致 | 未修；建议写实际函数名或注明封装名 |
| `设计稿:325` | "孔径 ±0.01"未说明是直径还是半径 | 未修；建议明确"直径" |
| `设计稿:332` | 阶梯轴"两段长度 30 / 20"未说明从哪个基准量 | 未修；建议明确从肩部量，并加总长 50 |
| `设计稿:340-343` | T3 壁厚"避开交接区"不可执行 | **已修**：给出 `x=20`/`z=20` 截面与探针 |
| `设计稿:353` | T4 底座长宽用整体包围盒，倾斜支撑会污染 | **已修**：改为底面有界轮廓的 `projected_span` |
| `设计稿:352` | T4 验收写死 65°，但目标是"用户确认的角度" | **已修**：改为"按用户确认的倾角验收，基线夹具取 65°" |
| `设计稿:428` | "设通过门槛"未量化 | 未修；例如 T1 的 8–10 个 schema，20 次运行中 ≥90% 工具+参数正确 |
| `设计稿:424-432` | 风险表缺 LLM API 限流/成本、VLM 误读图片 | 未修；建议补两条 |
| `设计稿:300` | "每个工具必须至少服务一个底线任务"与"标准件（额外承诺）"矛盾 | 未修；建议改为"底线工具必须服务底线任务；额外工具单列" |
| `设计稿:405` | "视觉不进降级线"但 T4 是额外承诺 | 未修；建议明确视觉失败时 T4 整体取消，不影响 T1–T3 |

---

## 6. v3 审计快照：当时建议的修订顺序

B1、B2、B3 已关闭。剩余工作按优先级：

1. **H1**：写死重试上限与按 cause 计数规则（0.5 天）。
2. **H3/H4**：CONFIRM 增加"需求→约束"覆盖检查；T4 增加"描述并确认解读形状"（0.5 天）。
3. **R1**：测量 `args` 与已确认参数的绑定规则（0.5 天）。
4. **H2**：重写复杂度口径，选定一个中等复杂度底线件（0.5 天）。
5. **M2/M3**：故障注入 fixture；marimo 两条路径的决策（0.5 天）。
6. **M1/M4/M5**：版本清单、报告大纲、提交清单（1 天）。
7. **H5/R2–R5/M6–M8**：受限执行表述、T3/T4 基准细化、排期缓冲、状态机/笔误（1 天）。

合计约 4.5 人日，可在 D1–D6 之间完成；H1、H3、R1 建议在 D6 规格冻结前完成。

---

## 7. v3 审计快照：做得好的地方

- **B1 的证据补齐方式正确**：不是补一段文字，而是补 notebook 源文件、独立进程复现脚本、STEP 和 `run.json`；我实际复跑后数值完全一致，这是可审计的交付。
- **B3 的契约已经可执行**：12 个测量 id 覆盖了距离、直径、间距、轴向角、截面偏距、面法向角、二面角、边角、投影跨度、壁厚、缺口、通孔；选择器有明确的 `expected_count` 和几何谓词；圆角前有 selection card + 高亮图。
- **T3/T4 的基准已经具体**：T3 给出两个测厚截面和探针方向；T4 给出底面轮廓投影、接触面法向角、缺口截面与位置基准。
- **B2 的处理干脆**：Web 定为底线，删除了放弃路径，并补了风险与评审行；这比"CLI 兜底"更符合作业示例（手机支架需要编辑器视图）。
- **诚实边界仍在**：手写 notebook vs 自动生成、`cache=False` vs 缓存、`sca edit` 未验证、文件系统隔离未实现，都写清楚了。
- **反目标、两份契约、版本规则、失败轨迹**仍是这份设计最强的部分。

---

**v3 当时的结论**：B1/B2/B3 的原始阻塞点已补齐；当时余项包括 H1（重试上限）、H3（需求覆盖）、R1（测量参数绑定）及排期和报告条款。现行判定见[顶部 v5 状态表](#current-audit-status)。

---

## 附录：复核命令与证据位置

| 复核项 | 命令 / 文件 |
|---|---|
| SCA 版本 | `importlib.metadata.version("simplecadapi")` → `2.3.0.post1` |
| 200 个操作与类型标注 | `docs/research/experiment/ops_dump.json`（`version=1`，200 ops，935 params，全部有 `type`） |
| editor extra 依赖 | `importlib.metadata.requires("simplecadapi")`：`starlette>=1.7.0; extra=="editor"`、`uvicorn`、`websockets`；无 FastAPI |
| marimo 版本检查 | `simplecadapi/runtime/_marimo.py:128-143`（`TESTED_MARIMO=(0,25)`，`warnings.warn(..., RuntimeWarning)`） |
| 参数独立 cell 规则 | `simplecadapi/runtime/runner.py:470-472` |
| `replay_graph` 签名 | `simplecadapi/recording/serializer.py:4918`：`replay_graph(graph, *, strict=True)` |
| `run_notebook` 签名 | `simplecadapi/runtime/runner.py:130`：`run_notebook(path, *, id=None, overrides=None, cache=True, through=None, product=True, timeout=None)` |
| `scad.var` 签名 | `simplecadapi/params/expr.py`：`var(name, default, comment=None, tolerance=None, *, unit=None, tolerance_unit=None, ui=None, control=None, min=None, max=None, step=None, label=None, group=None)` |
| `ql` 查询面 | `sca.ql.faces().where(...).exactly(...)` 均存在 |
| 官方 Skill 规程 | `simplecadapi/skill/resources/docs/skill/references/` 下 `discipline/requirement-and-cad-brief.md`、`domains/requirement-refinement.md`、`discipline/geometric-validation.md`、`discipline/failure-and-repair.md`、`discipline/notebook-cell-design.md` |
| T1 基线数据 | `docs/research/experiment/cases.json`、`results/run.json`、`results/*.brep.json` |
| notebook 交付样件 | `docs/research/experiment/notebook/offset_plate.py`、`notebook/README.md`、`notebook/results/run.json`、三份 STEP |
| notebook 复现 | `cd docs/research/experiment && .venv/Scripts/python.exe -B verify_notebook.py --out <临时目录>`；退出码 0 |
| 本轮复跑比对 | 三组 `measured_mm`、`volume_mm3`、`accepted`、`runtime_warnings` 与留存 `run.json` 完全一致 |

---

<a id="v5-audit-followup"></a>

## v5 修订记录（2026-11-27）

| 复查项 | [v5 设计](2026-11-27-cad-agent-design.md)的补充 | 仍需取得的证据 |
|---|---|---|
| M2：区分反馈驱动修复和瞬态重跑 | `T2-plan-repair` 的首轮错误留在建模计划，原样重跑仍失败；真实 Agent 收到反馈后须改计划，并用原快照和判据复测。另加 `V1 → V2 → V3` 验证验收失败类别的修复限额。 | 首轮反馈、前后实参差异、同一快照及通过结果；两类预算的实际轨迹。 |
| B1：正式交付源与验收模型一致 | 从保留参数绑定的计划生成正式源文件，由该源文件产出验收 STEP，发布时将实际运行源和参数与 STEP 绑定。T1–T3 都须在新进程重建和单参改值。 | T1 手写样件的证据仍有效，不替代三例正式源文件的运行记录。 |
| H3/R1：同会话改参不丢约束 | 以当前已验收版本的完整确认集为底稿，只合并经确认的变更。T1 明确重测未改尺寸及贯通、有效性等拓扑。 | 快照差异、约束清单完整性及 T1/T3 逐项实测。 |
| H5：执行环境与工具边界分开 | 两种源文件走同一受限执行门槛；工具路径拒绝不能代替实际进程的越权写入拒绝。 | 课程认可的限制级别仍待 P1 确认；按最终运行方式测试，不能提前宣称已隔离。 |
| M7：同尺度展示不是相同 `zoom` | 前后视图共用取景范围；以 T3 宽度 25 → 30 mm 检查宽度像素跨度按 `30/25` 变化、未改臂长的像素跨度不变。 | SCA 2.3.0.post1 已观察到 `40×25×4` 与 `80×50×8` 长方体在相同顶视角和 `zoom` 下单独渲染得到相同像素；两条 Web 路径的共用取景仍待验证。 |
| R4/R5：截面与托唇反例 | T3 补 5 mm 壁厚拒收；仅启动 T4 时分别验托唇双侧高度，以及 115° 反倾、托唇外伸和缺口被挡。 | 当前截面实验只证明直边样件的 STEP 回读与两种宽度下的正确测厚，不等于反例或通用测量层通过。 |

本节记录设计条款，不等同于实现或端到端验收。T1–T3 与 Web 仍为底线，T4 仍可选，排期人时口径不变。
