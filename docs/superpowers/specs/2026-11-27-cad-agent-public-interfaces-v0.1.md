# CAD Agent 公共接口 v0.1（评审稿）

**状态：待 P1–P4 交叉评审，不是设计基线，也不是分工确认。** 本稿以[主规格 v6](2026-11-27-cad-agent-design.md)为准，只约定 T1 偏置通孔板的团队内部交接。以下 **【v6】** 表示已定规则，**【提案】** 表示本轮用于对接的字段、状态投影或协议细节。不要求每个模块单独部署或通过 HTTP 通信，不定义 T2–T5、完整 SCA 工具集或生产实现。

**【提案】采用四个边界的 JSON 消息样例，而不是先定 HTTP 路由或共享数据库。** P2/P3/P1 可直接交换这些记录或用进程适配器传递；P4 可以分别替换各边界做测试。显式区分「用户确认值」「源文件实际输入」「STEP 回读实测」「当前已发布版本」，不能以其中一个替代另一个。

## 0. 共用约定与样例入口

| 文件 | 先交给谁 | 可独立使用的样例 |
|---|---|---|
| [generation.json](examples/t1/generation.json) | P2、P3；在线判据也供 P1 消费 | 冻结快照、确认需求映射、T1 测量规则、固定计划 |
| [execution.json](examples/t1/execution.json) | P3、P1 | 实际执行入口、参数文件内容、预览基线和输出位置 |
| [verification.json](examples/t1/verification.json) | P1、P2、P4 | 执行结果、回读与在线判定、规范化失败及证据 |
| [web.json](examples/t1/web.json) | P2、P3；P4 核对轨迹 | Web 请求/响应、发布记录、运行状态和旧版下载 |

以上是 **`synthetic_review_data`**：文件内的实测字段、证据和产物引用都是模拟，不包含源文件、STEP、PNG 或几何实跑。数据取值参照 [T1 实验](../../research/experiment/README.md)与 [cases.json](../../research/experiment/cases.json)；既有实验不是 v6 全段净空或正式生成器联调的证据。各文件顶层只是评审数据容器，接入线上时传单条消息及明确引用的记录，不加载整套样例。`generation.json` 的 `offline_setup` 仅供离线测试适配器使用：按 `case_id` 和 `key` 选择夹具，在生成本次源和参数文件前替换候选执行值；不修改确认快照、计划参数引用或验收目标。生产生成器、模型和 Web 均不接收这个字段。

**【提案】** 下文表中字段均必填，特注明可空或按分支出现的除外。`*_mm` 内数值单位为 mm，`*_mm3` 为 mm³，`*_deg` 为度，方向与单位轴无量纲，不用字符串传数字。`key = {run_id, attempt, snapshot_id, plan_id}` 是一次候选的身份；`attempt` 是同一 `run_id` 内从 1 开始的整数；未执行时 Web 的 `last_attempt` 为 `null`。同一轮修复沿用 `run_id`、`snapshot_id`、`base_version_id`，另建 `plan_id`、递增 `attempt`。跨消息引用必须核对整个 `key`，不能只以文件名或尝试号关联。

- `session_id` 标识会话；`run_id` 标识本轮请求，澄清时已存在；`snapshot_id` 标识确认后的不可变记录，澄清中尚未生成。`version_id` 只在发布后分配。初次建模 `base_version_id = null`；改参记录所用已验收版本 ID 及其 `base_snapshot_id`。
- `*_ref` 是宿主管理的产物引用，不是客户端 URL 或任意文件路径。样例用 `runs/<run_id>/attempt-<n>/<file>` 表示，路径相对于宿主产物区。输入、候选 STEP 和报告均按本次 `key` 绑定；第 2 节的预览基线、Web 的已发布旧版引用可以显式指向另一尝试。
- `length / width / thickness / diameter / hole_x / hole_y` 是本稿唯一六个尺寸 ID。`hole_x` 是到左板边的轴线距离，`hole_y` 是到下板边的轴线距离；零件原点取底面左下角，`+X/+Y` 沿板长/宽，`+Z` 向上。生成样例采用同名源参数；手写试验 notebook 的 `hole_d` 对应公共 `diameter`，不是第七个参数。

## 1. P2 → P3：确认快照和固定建模计划

**提供方 P2** 冻结确认需求、计划与绑定；**消费方 P3** 据此确定性生成 notebook 或脚本。P1 与 P2 对齐工具 schema，P1 验收时读取同一份确认快照及其在线规则。

| 输入 | 必填字段与关系【提案】 |
|---|---|
| `Snapshot` | `snapshot_id, session_id, run_id, confirmation_id, base_version_id, base_snapshot_id, parameters_mm, constraint_set_id, requirements`。两项基线字段首次均为 `null`。`requirements[]` 每项有 `id, turn_id, quote, interpretation, constraint_ids`，原文见 Web 同 `turn_id` 的输入，确认后映射是完整的。`parameters_mm` 含六项确认值。 |
| 在线 `ConstraintSet` | `constraint_set_id, frame, selectors, derived, constraints`。`frame` 含 `id, origin_mm, axes{x,y,z}`，各轴为单位向量。每条约束有 `id, statement, source, unit, criterion, measurement{id,args}`；T1 六项 `criterion.mode=within`，`value` 用参数引用，`tolerance=0.01` mm，`through_hole` 用 `is_true`、单位 `bool`。测量实参中的 `{"selector":"bore"}` 是复用简写；调用前展开为 v6 的 `{kind, expected_count, where}`。`derived` 以派生 ID 记录 `unit, rule_id, depends_on`；T1 的 `diameter_lower_limit` 是注册函数，不接收自由公式。规则记录不可变，可内嵌于快照或按不可变 ID 引用；不能用会变的配置覆盖。 |
| `Plan` | `key, tool_schema_id, steps, result_step_id, repair_of_attempt`（初次为 `null`）。`steps[]` 有 `id, tool_id, args`；`{"param":"diameter"}` 引用命名参数，`{"step":"plate"}` 只能指向本计划已定义的上游结果。不同尝试各自校验，`result_step_id` 指定唯一交付实体的建模结果。 |

**【v6】** 澄清未完成不 BUILD：列出原话及轮次、需求 ID、约束和验收方式；自由文本回答要回显再确认。对不支持、缺失或冲突的关键要求不假装已解决。改参以已验收版的完整确认集为底稿，只应用用户明确确认的差量，继承其它约束的 ID、单位、基准、容差和测量定义。修复只改建模方案，不改确认快照及判据。

**【提案】** `tool_schema_id=t1-tools-v0.1` 下只需要四个建模工具；下表工具名沿用 v6 列举，实参名、返回引用和 T1 调用约定待评审。导出和留证由固定执行入口处理，不让模型填操作系统路径。

| `tool_id` | 必填 `args`（标量用 mm，结果以步骤 ID 引用） |
|---|---|
| `make_rectangle_face` | `length, width`；XY 矩形，左下锚在原点。 |
| `extrude` | `profile`（面引用）、`distance`（绑定 `thickness`）；沿 +Z。 |
| `make_cylinder` | `diameter, x, y, plate_thickness`；Z 向切削体，T1 模板从 `z=-1 mm` 到 `z=plate_thickness+1 mm`，轴经过实际输入 `(x,y)`。这 1 mm 是候选建模余量，不是验收容差。 |
| `cut` | `target, tool`（实体引用），板减切削体。 |

**成功／失败：** P3 成功生成第 2 节的交接记录及对应源文件、参数文件。P2 校验工具、类型、几何前置参数与引用；P3 校验实际收到的快照/计划对应且绑定无缺失，不接受未知 schema、自由 Python 或未确认快照。失败返回 `key`、阶段（`plan_validation` / `source_generation`）、稳定错误码、问题步骤/参数和摘要；不发执行请求、不伪造几何结果。只生成文件不算 v6 的「已执行一次」；是否再次规划以及准备阶段如何终止由 P2 详设，不挪用候选执行计数。

**独立测试：** P2 用生成器 stub 断言缺孔位或单位时不发计划，确认后才发完整绑定；Ø14 改参只提交孔径差量但生成器收到完整快照。P3 不启动 Agent、不访问 LLM，用 `generation.json` 逐个加载固定计划，检查无引用丢失、每个 notebook 参数独立成 cell，给未知工具及坏引用则不发执行请求。

## 2. P3 → P1：交付源执行请求

**提供方 P3** 交付实际源文本、参数及请求记录；**消费方 P1** 在宿主安排的独立尝试目录和新进程中运行。不同形式共用 `ExecutionRequest`：

| 必填字段【提案】 | 内容与单位 |
|---|---|
| `key` | 与 `Plan.key` 完全一致；快照和计划在启动前独立落盘。 |
| `source_kind, source_ref` | `notebook`（marimo `.py`，一个可导出的 SCA Part）或 `script`（确定性 Python `.py`，读取参数 JSON 并建模/导出）。宿主根据类型选固定适配器；不传命令串。 |
| `params_ref, actual_parameters_mm` | 参数文件引用与其中的完整六键数值映射，单位 mm；不是只有本轮变化的 override。P1 记录实际加载的内容并核对与交接一致。正常链路从确认值解析并运行；验收目标始终独立从 `snapshot_id` 解析。 |
| `step_ref` | 本次正式源运行应写到的最终 STEP 引用；预分配位置不是已生成的证据。 |
| `preview_baseline` | 初次为 `null`；其余为 `{version_id, step_ref}`，由 P2 随交接提供已发布基线的只读引用。仅用于可比视图，不是输入几何或待验候选；生成源文本时无需解析它。 |

**【v6】** notebook 每个参数独立成 cell。P1 用对应源和参数运行 notebook（适配器调用 `run_notebook` 并导出同一次返回的 Part），或运行降级脚本（读取相同参数映射并自行导出）。两条路径都不能拿试算 STEP 或从 `OperationGraph` 回放的 STEP 顶替。只凭实际交付源和参数，要能在新进程重建和单参修改。运行在 Windows 独立 Job Object 中；超时后确认整个 Job 清空才允许重试，无法确认则停止自动重试。STEP 临时写完、可读后原子重命名；超时遗留的 STEP 一律不进入验收。

**【v6】** 模型工具只给逻辑产物名；宿主校验候选目录与解析后的真实归属，拒绝绝对路径、目录跳转、越界链接。此约束与低权限/隔离执行分别测试；路径拒绝不能冒充沙箱。`sca edit` 若会在确认的边界外执行生成代码，走 PNG + STEP；D5 的脚本降级不取消 Web，不降低验收。

**成功／失败：** 执行成功只表示该入口生成可供回读的本次 STEP（`step_ready`），不表示几何合格。实际参数文件与请求不符、入口不可用、执行异常或超时均不进入 STEP 验收，按第 3 节返回证据。切削完成但布尔后几何门禁不通过，走几何拒收而非伪造可用 STEP。输入数值不能作为实测；偏位样例中的 25 mm 是离线适配器设定的候选实际输入，不是修改用户确认、不提供生产覆盖入口。

**独立测试：** P3 无需 P1 真正启动，验证两类输出都交给同一 stub、参数完整、不会提交试算文件；可用现有手写 notebook 对照入口。P1 用 `execution.json` 和团队自备 T1 源文件（样例引用不是文件）验证两种入口、参数文件不符拒绝、坏路径拒绝、超时清理及晚到产物不进入验收；保存实际入口与输出的留证。正式联调再换成 P3 实际生成的源。

## 3. P1 → P2 / P4：执行结果、在线验收与证据

**提供方 P1** 记录实际执行、候选 STEP 回读、选择与判定；**消费方 P2** 据此转状态/修复/发布；**消费方 P4** 只读收集在线结果，以独立需求、预期和试件判分。P4 的离线答案、故障 fixture 配置及期望失败项不进入运行时输入、提示词或生产 Web。

| 消息 | 必填字段与分支【提案】 |
|---|---|
| `AttemptResult` | 外层 `key`；`execution` 含 `status, source_ref, params_ref, actual_parameters_mm, step_ref, log_ref, post_boolean, error`。`step_ready` 时这些源/参数/STEP 引用须与执行请求相符，`error=null`。`execution_error` 时不可有可验 STEP，未产生成果的引用/未加载的实际参数可为 `null`，`error` 给 `stage, code, tool_id, args, cause_key, message`（没有工具阶段时工具与实参可空；超时附 `cleanup_confirmed` 布尔及日志）。`precheck_rejected` 时无可验 STEP，保留布尔后记录并附几何报告。`post_boolean[]` 每次布尔含 `step_id, valid, closed, positive_volume`，无法完成布尔时数组可空。 |
| `report`（同 `key`） | 执行异常时为 `null`；其余含 `status`（`passed`/`rejected`）、`stage`（`step_readback`/`post_boolean`）、`report_ref, step_ref, brep_ref, topology, checks, evidence, failure`。发布级回读有本次 STEP、BRep 证据引用，`topology` 给 `solid_count, valid, closed, positive_volume`；若布尔预检即拒收，三个回读引用/事实 `step_ref, brep_ref, topology` 为 `null`，`checks=[]`，失败原因在 `failure`。无法回读或测量则未取得的事实为 `null`，不得当作通过。 |
| `checks[]` | `constraint_id, measurement_id, criterion, unit, actual, delta, status, code, evidence_keys`。`criterion` 保存解析后的目标和容差（布尔只写 `mode:is_true`，隐含目标为真）；数值 `delta=actual−criterion.value`，同量纲；布尔或无实测时为 `null`。`status=passed\|failed`；通过 `code=null`，失败如 `out_of_tolerance`、`selection_mismatch` 或 `unsupported_measurement`。证据键指向同报告 `evidence` 的条目。 |
| `evidence` 与 `failure` | `evidence.selections` 按选择器名记录 `expected_count, actual_count, entity_ids`（仅本 STEP 内有效）；按快照解析的完整选择器、解析实参、候选实体摘要和内核诊断落 `log_ref` / `brep_ref`。`evidence.through_hole` 记录开口与全程探测证明，见下文。通过 `failure=null`；拒收时给 `code, failed_ids, cause_key`，几何事实失败可用 `topology`/布尔步骤作为原因，而不是伪造尺寸 ID。 |

**【v6】T1 验收必须全部满足：** 布尔后验 BRep 有效、壳闭合、正体积；以**同一候选 STEP** 回读，再检查这些条件与单一实体。板长/宽/厚按 X/Y/Z 整件外廓测；唯一竖直圆柱面给孔径和孔轴。左边距、下边距以各自外廓最小侧基准面测轴线垂距；选择器不靠目标孔位或目标孔径筛掉错件。六项尺寸均按 `abs(delta) ≤ 0.01 mm`（含边界），全部重测，未改项也不能省略。未知测量及选择器命中数不符不能当通过。

**【v6】通孔不是只看两开口。** 验证孔轴方向、两圆形开口分别在指定底面/顶面且邻接孔壁；再用**实测孔轴**构造从入口到出口的净空圆柱，在候选 STEP 回读实体上做 BRep 布尔求交。`min_clear_diameter = 确认孔径 − 孔径容差`，由快照解析（9.99 → 13.99 mm），不能用执行参数或实测孔径代替。成功且可判定无正体积交叠才通过；接触不算遮挡，失败或不可判定均拒收。证据至少包括两开口结果、净空探测体轴线与端点/跨度、直径、内核容差、布尔状态、交叠量/结论和失败原因（见样例 `evidence.through_hole`）。探测体不进入交付 STEP。不能用净空通过掩盖孔位超差，或用孔位超差替代净空失败测试。

**成功／失败归属：** 执行异常包括进程退出、工具抛异常、导出未完成、超时；无在线通过报告。工具完成但几何预检失败，或执行成功后回读无法证明满足约束（含选择失败、测量不可判定），是几何拒收。若进程崩溃或超时导致根本没产出验收报告，归执行异常，不合成几何结果。`cause_key` 用失败类型、验收项/工具、特征、稳定码归一化；不含浮点偏差或错误措辞。P2 两类分开计数：初次计入总执行，至多 3 次修复、4 次执行，两类各最多触发 2 次修复；连续两次同主因、对应预算或总预算用尽则终止。修复次数在进入下次执行时才递增。`stale_baseline` 是 P2 发布冲突，不是上述两类，不触发修复。

**独立测试：** P1 以确认快照和自备 STEP 验尺寸边界、命中数、+5 mm 偏位及「开口和尺寸通过但全段被挡」的 T1 反例，不需要 P2 或离线答案。P2 用 `verification.json` 的报告喂 stub，检查拒收/修复/终止；再单独喂执行异常与不可确认清理的超时记录。P4 拿原话、事件与可追溯产物，独立判断漏问、漏测、是否真可复建；把在线报告与离线预期比较，而非把在线 `passed` 直接当评测结论。正式联调须留下净空挡片反例、选择失败和输入与实测不一致的分层证据。

## 4. P2 ↔ P3 Web：会话、运行状态与下载

**P3 Web 提供请求，P2 会话/版本模块消费并返回权威状态；P3 只负责显示和发起操作。** 以下是逻辑操作，不指定 URL、框架、轮询或事件推送实现。`web.json` 的 `trace` 保存选定请求/响应，不是逐状态全日志。

| 操作【提案】 | 请求必填（都有 `session_id`） | 成功与拒绝 |
|---|---|---|
| `submit` | `text` | 创建轮次，回 `run_id, turn_id, status`。缺项为 `CLARIFY`，条件齐备也要 `CONFIRM`。首建基线为空；已有版本的改参用 `revise`。 |
| `clarify` | `run_id, text`；澄清答复带 `reply_to_turn_id`，修订当前确认清单带 `confirmation_id`，二选一 | 回 `run_id, turn_id, status`。缺项仍在则继续澄清，齐备则回显新清单并停在 `CONFIRM`，不直接 BUILD。 |
| `confirm` | `run_id, confirmation_id` | 确认当前展示的结构化清单；回 `run_id, snapshot_id, status=BUILD`。要修改清单先反馈、由 P2 重新回显，旧清单 ID 不可锁定快照。 |
| `revise` | `base_version_id, text` | 在指定的当前已验收版上发起同会话请求，回 `run_id, turn_id, status`。回显完整参数及变更/保留项；还需 `confirm`。入口已过期可拒绝请求并返回实际当前版；入口通过也不能免除最终发布检查。 |
| `get_status` | `run_id` | 返回本轮 `run` 及独立的 `current_version`，见下。只查询，不推进状态。 |
| `download` | `version_id, kind`（`source` / `params` / `step`） | 仅按该会话的已发布版本解析，返回 `version_id, kind, artifact_ref` 对应的内容；样例只列引用。未知/未发布的版本拒绝，不隐式回退到另一个版本，也不收客户端文件路径。 |

命令拒绝用 `{code, message}`，基线冲突另带 `base_version_id, current_version_id`；不改变当前版。运行终态通知与命令拒绝不同，即使一个命令成功接收，本轮也可能最终失败。

- **`run`** 含 `run_id, status, base_version_id, snapshot_id, last_attempt, published_version_id, clarification, confirmation, failure, counters`。`status` 投影 v6 的 `INTAKE/CLARIFY/CONFIRM/BUILD/CANDIDATE/VERIFY/REPAIR/ACCEPT/DELIVER/FAILED`。`CLARIFY` 给 `{turn_id, missing, question}`；`CONFIRM` 给 `{confirmation_id, parameters_mm, frame_id, changed_parameter_ids, retained_parameter_ids, requirements}`。确认清单按每条原文（`id, turn_id, quote, interpretation`）回显约束和测量方式（`constraint_ids, measurement_ids`），这里包含基准与单位；未处理阻塞项不允许确认。`failure` 在 `REPAIR/FAILED` 给 `kind, code`（`kind` 为 `execution_error`、`geometry_rejection` 或 `publication_conflict`，分别取对应业务码）。有报告带 `report_ref`；几何拒收可回显 `details[]`（`constraint_id, unit, target, actual, delta, code`，从失败测量项投影，缺失的实测值或不适用的偏差用 `null`）。终止时给 `terminal_reason`；发布冲突的 `code` 与 `terminal_reason` 均为 `stale_baseline`，并带 `base_version_id, current_version_id`。条件不适用的状态栏为 `null`。`counters` 含 `executions, execution_repairs, geometry_repairs`。`published_version_id` 只在**该轮**已发布时填写。
- **`current_version`** 独立于本轮，可为 `null`；有版本时至少给 `version_id, snapshot_id, parameters_mm, after_view_ref`。参数表、默认预览和下载目标都以它为准，不以 `run` 的最新候选覆盖。查询旧轮次时 `run.published_version_id` 可以不是当前版本；指定旧 `version_id` 仍可下载。
- **`Version`** 逻辑记录（样例 `published_versions`）含 `version_id, key, base_version_id, source_ref, params_ref, step_ref, report_ref, manifest_ref, comparison`。`comparison` 含 `before_version_id, before_view_ref`（初次均空）、`after_view_ref, view_spec`。对比用同一方向、投影和前后联合外廓定取景；`view_spec` 给 `direction, up, projection, bounds_mm{min,max}`。由展示适配器按这一约定读取前后已验收几何；预览不是验收输入。`manifest_ref` 指向 v6 要求的实际版本清单，绑定本次源、参数、STEP、在线报告及快照，记录环境、锁定版本、脱敏配置、视图、日志与复现命令；本稿不另定清单全字段。失败候选的产物/缺失原因留档，仅作诊断。

**【v6】发布门禁：** P2 在 `VERIFY → ACCEPT` 确认源文件、实际参数文件与由该源实际运行导出的 STEP 齐全且同一次尝试，在线报告针对这份 STEP 且全通过。然后比较快照 `base_version_id` 与会话实际当前版，**比较与更新当前指针必须在同一原子操作内**（首次比较 `null`）。匹配则记录版本，再 `DELIVER`；不匹配时以 `stale_baseline` 转 `FAILED`，留基线和实际当前版 ID、保留候选，不发布，不动当前指针，也不走修复。若要继续，从最新已验收版重新 `INTAKE`，回显待合并与保留项并重新确认。任何未通过或未发布的候选都不得成为下载或下轮改参基线。

**独立测试：** P2 以假 Web 请求与 P1 stub 验 `run`/`current_version` 分离、跨轮旧版下载、错 `confirmation_id` 拒绝，以及两个均通过几何的候选用同一基线竞争时仅首个能发布。P3 用 `web.json` 的响应序列驱动 mock，做澄清、确认、改参、状态与下载，不启动 P1/P2；对过期分支另喂 `FAILED/stale_baseline` 且 `current_version` 指向赢家的响应，断言提示冲突而当前预览和下载不跳到失败候选。

## 5. 同一会话的三段评审轨迹

| 工况 | 关联与预期（模拟） |
|---|---|
| 缺孔位 → 发布初版 | `run-01` 先 `CLARIFY`，缺孔径、两边距、单位和定位基准；收到答复后回显 `confirm-01`。确认后生成 `snap-01`（无基线）。第 1 次执行回读六尺寸合格，净空探测直径 9.99 mm，发布 `v1`。 |
| 只改 Ø10 → Ø14 | `run-02` 由 `v1/snap-01` 起步，确认 `snap-02`，仅 `diameter=14`，孔位仍 `(20,15)`。第 1 次尝试全量验收，净空重算为 13.99 mm，发布 `v2`。样例特意用脚本入口演示同一交接契约，不表示 D5 已决定走降级。 |
| 偏位 → 拒收并保留 `v2` | `run-03` 明确要求按 `v2/snap-02` 约束再做一份，不更改尺寸。`snap-03` 的 `hole_x` 仍是 20 mm；离线适配器在两次尝试中只让候选的实际 `hole_x` 输入为 25 mm。两份 STEP 均模拟可读并完成全量验收，只有 `hole_x` 失败，`25−20=+5 mm`。第二份计划仅调换独立建模步骤的先后，两次共用确认快照与基线；第二次同因失败终止（1 次几何修复、不消耗执行异常修复次数）。Web 显示本轮 `FAILED`，仍下载 `v2`，显式指定 `v1` 也可取回。该轨迹不是一次真实 Agent 修正或实测。 |

另在正式联调前明确 v6 要求的 T1 用例：并发基线过期、孔内挡片、未覆盖原需求，以及实际输出路径和受限环境分别验证。它们不以本套正负数值样例代替。

## 6. 交叉评审与正式发布前清单（建议分工）

| 暂定角色 | 建议负责的详细设计 | 建议交叉评审 | 需要组员决定的问题 | 正式发布本接口基线前验收清单 |
|---|---|---|---|---|
| **P1 几何、执行、在线验收** | 四工具的输入/输出与坐标约定；两类源入口；STEP 回读、选择与全段净空证据；Job 清理和运行限制。 | P3 审源入口与产物边界；P2/P4 审错误诊断和测量证据。 | SCA 净空布尔成功、边界接触和数值不可判定如何留证？课程认可的受限执行机制和验证方式是什么？ | ☐ 用样例独立验证执行请求的消费和验收报告的输出；☐ 锁定测量与命中证据，正常孔和挡片反例都有可验证的计划/夹具；☐ 确认两类源入口、路径限制与 Job/隔离测试责任。 |
| **P2 Agent、会话、版本** | 原文映射与确认快照；候选计划和修复预算；原子发布、冲突与可追溯版本。 | P1 审工具和故障分类；P3 审状态与下载；P4 审离线边界。 | 用何种事务或锁保证比较与更新原子性？怎样验证产物确由该源/参数/尝试产生（例如不可变落盘与内容摘要）？如何规范准备阶段失败？ | ☐ 用 stub 跑三段，验证差量继承和同因终止；☐ 并发双通过时只有一个发布，另一个保留证据但无版本；☐ 明确快照、版本和可下载产物各自的持久化/查询责任。 |
| **P3 Web、notebook／脚本生成** | 固定计划到两类源的确定性生成、参数映射、确认清单和双状态展示、下载与对比取景。 | P1 审可执行性；P2 审确认/版本展示；P4 审 mock 是否掩盖失败。 | D5 用什么证据选择 notebook 或脚本路径？状态查询采用什么传输方式，预览在受限环境不可行时如何切到 PNG？ | ☐ 无 LLM 用固定计划生成两种接口请求；☐ 澄清不能跳确认、失败仍下载旧版；☐ 与 P1 确认实际导出源、单独参数 cell 与同尺度展示的联调检查。 |
| **P4 独立评测** | 原话/缺项离线预期、T1 正反例与并发、旧版取回、正式源文件复建的复现记录。 | P1 审几何夹具和证据；P2/P3 审事件、产物可观测性与评测隔离。 | 离线注入在哪个适配器做、如何确保测试数据不进入生产？如何以独立观察验证未漏原始要求，并区分模拟数据、手写实验和联调证据？ | ☐ 独立预期可判三段轨迹，不从在线报告反推答案；☐ 列齐挡片、漏项、过期基线、越界路径与受限环境对照；☐ 约定实际复建、改单参并复测的证据和失败留档。 |

**本轮评审通过标准：** 四个角色都能只用约定的边界和同一套样例做各自的 stub/consumer 验证，能指出哪些行为已由 v6 固定、哪些仍是提案。由组员交换评审意见、处理未决项并重新核对样例后，再正式发布基线和确认分工；本稿不代替 v6 的实际系统验收。
