# SimpleCADAPI 能替课程智能体完成哪些工作？

核对日期为 2026-11-25。本文按 PyPI 发行版 **2.3.0.post1** 核对，发布标签对应提交 `95cdd5fe5d2ea0b2524ad5dbf16d115c48313486`。当日 master 为 `389d4306`，后续提交涉及发布流水线。下文的源码链接固定到发布提交。状态「已核实」注明是阅读源码还是实际运行。「作者声明」限于上游说明，「分析推断」是对作业的解释，「待验证」需补实验。[PyPI 版本](https://pypi.org/project/simplecadapi/2.3.0.post1/) · [发布记录](https://github.com/PhySpace/SimpleCADAPI/releases/tag/v2.3.0.post1) · [发布后的提交](https://github.com/PhySpace/SimpleCADAPI/commit/389d430667679d5fda3188956b023542aa4237f2)

## 从用户确认的尺寸到可交付模型

| 环节 | 版本证据与验证状态 | 对作业的意义 |
|---|---|---|
| 需求 | **已核实·官方 Skill**。交互模式的 Role 1 要求记录形状解释、阻塞问题、候选假设和用户同意。无人值守模式允许自行登记假设。[需求确认规程][ask] | 课程明确要求先问清关键条件。可借用记录格式，自行保存参数来源、单位、基准、容差、确认轮次。比如“孔偏 10”还缺方向以及相对板中心还是板边，当前提议须等用户答复。 |
| 规划与工具 | **已核实·官方 Skill、源码**。单零件流程分需求、计划、分阶段验证契约、建模、交付。CLI 的 `sca ops` 查询操作，`sca run` 执行，`sca edit` 打开编辑器。各角色描述的是工作职责，流程文件本身不执行模型调用。[建模流程][flow] · [CLI 注册表][cli] | 生成 Python 和调用团队定义的参数化工具均可抵达 SCA。自行确定可调用的操作、参数范围，以及缺参、生成失败、验收失败各自转入什么状态。 |
| 参数与特征 | **已核实·源码**。官方 U 形电机连杆以 `ULinkDimensions` 保存原始尺寸、推导安装面和间隙，并由 `check()` 检查可行性。`u_link.py` 先扫掠，再切背平面和电机槽、融合柱体。安装面用平面类型、方向和位置范围共同定位，并要求唯一命中。[尺寸和守卫][dims] · [建模单元][ulink] | 修改电机直径会改变安装面和开槽深度。需要重新执行依赖它的验收。若选择边或面，重复特征可能命中多个对象，应把命中数也写进检查。 |
| 重建与展示 | **已核实·指南、源码**。notebook 是带元信息的 Python 文件，`run_notebook(overrides=...)` 可覆盖顶层单元变量；同一单元的输出需一同覆盖。运行时覆盖只对该次生效。编辑器能把用户选中对象转换成单元代码。官方示例也演示了独立参数模块。[运行指南][nb] · [run_notebook][runner] · [selection_cell_code][select] | 现场改参后须保存能重建新版的源文件或参数集。只保存本次覆盖的截图，会丢失下一次运行所需的输入。 |
| 几何查询与交付 | **已核实·源码**。官方验收脚本从真实形体求包围盒、按几何属性找面、用点分类判断预期材料或空腔，并汇集多项失败。示例把产品导出 STEP、STL 并渲染。[验收脚本][accept] · [导出脚本][export] | 可直接复用 SCA 内核和查询；团队定义需求对应的几何量、基准和通过条件。STEP 用于交换，保留参数化源文件才能重建特征。官方示例中直接导入的 `_cpp` 私有绑定应单独核对版本。 |
| 失败处理与终止 | **已核实·官方 Skill、运行源码**。单元异常可传给调用方。Skill 建议同一原因连续失败两次即更换建模策略；换策略仍失败应停止报告。这是指导文字。[修正规程][repair] · [运行器][runner] | 控制器需分别处理异常和有效实体的尺寸超差，计数器由程序维护。例如可设 `max_repairs=2`（首次执行另计），到限保存最后失败证据并结束。次数是待讨论的课程配置。 |
| 执行边界 | **已核实·源码**。`run_notebook(timeout=None)` 默认不限时；`_with_timeout` 启动 daemon 线程并 `join(timeout)`，到期向调用方抛出异常。该函数没有强杀线程或施加文件、网络权限的逻辑。[run_notebook 与 _with_timeout][runner] | **待验证**。若接收模型生成的代码，需在单独受限执行环境试验超时后进程树退出、仅可写指定输出目录；保留退出原因和输出。纯参数工具也需限制单次几何计算的资源消耗。 |

## 版本差异可能改变同一模型的检查结果

**已核实·依赖清单与发行说明。** 本次深入分析的 CADDesigner 固定了 SCA **2.0.8**。SCA 从 2.2.7b1 起把 C++/OpenCASCADE 几何引擎装入 wheel，默认安装的 B-rep 检查模块可用内置软件渲染器。分析 CADDesigner 的调度和反馈仍有价值；把其生成模板迁移至 2.3.0.post1 时，应先实际跑一个含切割和导出的案例，记录接口、模型和测量是否一致。跨这两个版本的兼容性尚待验证。[CADDesigner 依赖清单](https://github.com/562590763/CADDesigner-Code/blob/65b5f5219974eadbd3ea1d117e467f47cefb69b7/pyproject.toml) · [SCA 版本说明][changes]

**已核实·变更记录。** 2.3.0 对切割和相交默认合并同域面与边。旧图若缺少新参数 `clean`，重放会被拒绝；同形体的面数、边数和指纹也可能变化。2.2.8 已撤回，2.3.0 又明确一个 Part 只持有一个实体。2.3.0.post1 的编辑器改用动态端口和实例 ID，照抄旧端口 7180 的演示脚本有连错实例的风险。换版本后应先用同一个参数化源文件重建、对照实测尺寸，并确认编辑器所指的工作目录。[发行版本差异][changes]

## 作业对照与证据留存

### 实验记录 · 改大孔后仍须检查孔心

**已核实·本地实测，2026-11-25。** Windows 11、CPython 3.12.13、SCA 2.3.0.post1。先在独立输入表定义板件名义尺寸和容差。建模脚本从矩形面拉伸板体，再减去穿过上下表面的圆柱。每次将 STEP 写出并重新读入，从包围盒测板的长宽厚，从圆柱面半径和轴位置测孔径及孔心，从圆形边与上下表面的高度核对贯通。各长度验收采用绝对容差 ±0.01 mm。另起输出目录重跑脚本，重复得到下表结果。[实验记录与复现](experiment/README.md) · [输入](experiment/cases.json) · [建模及独立判定函数](experiment/plate.py) · [实测日志](experiment/results/run.json)

| STEP 回读 | 板长 × 宽 × 厚（mm） | 孔径（mm） | 孔心距左边、下边（mm） | 有效单实体、贯通 | 判定 |
|---|---|---:|---|---|---|
| [初版](experiment/results/before.png) | 80 × 50 × 8 | 10 | 20，15 | 是 | 六项尺寸偏差均为 0 |
| [只改孔径](experiment/results/after.png) | 80 × 50 × 8 | 14 | 20，15 | 是 | 六项尺寸偏差均为 0 |
| [故意移动孔](experiment/results/off_target.png) | 80 × 50 × 8 | 14 | 25，15 | 是 | 拒绝，X 方向偏差 +5 mm |

后两件的体积四舍五入后同为 30,768.50 mm³，包围盒也相同。若验收只查体积、外形尺寸、能否导出，就会放过错件。本例依靠唯一圆柱孔壁定位；有沉孔、圆角或多个等径孔的模型需要新的孔识别方法。此实验使用人工编写的参数和程序，检验范围是几何执行与验收。模型规划、真实用户澄清和反馈后自动修复仍待端到端验证。

以[课程说明](../../README-zh.md)为准。以下“自主实现”是判断一项能力能否计入课程成果的依据。

| 要求 | 可用证据和可复用部分 | 团队自主实现及检验方式 |
|---|---|---|
| 需求理解与澄清 | Role 1 的问题、假设、同意记录，见上表。**已核实·文档** | **待验证**。向系统输入缺单位或矛盾厚度，检查是否先询问，再保存答复与被覆盖的旧值；保留对话原文。 |
| 建模与参数化 | 单零件的实际操作、输入和几何见下方实验；官方源码另给扫掠、布尔示例。 | **待验证**。用用户原话触发 LLM 计划、自主工具封装和重建；记录计划、工具定义版本、实参和生成文件。 |
| 检查与修正 | SCA 查询返回几何量，实验对有效实体也执行验收。 | **待验证**。将异常类型或“目标、实测、误差、容差、基准”传回 Agent，重跑原验收；故意重复失败验证重试上限。 |
| 修改与交付 | 改参重建、前后查看文件、STEP 见实验；编辑器接入见上表。 | **待验证**。同一对话只改目标字段，比较已确认约束；交付前把新一轮输入、模型及检查关联到同一版本。 |
| 可复现与受限执行 | 实验记录环境和复现命令；运行器支持软超时。 | **待验证**。增加模型 ID、推理配置、提示词版本、源文件和日志；用无副作用的休眠任务验证强制终止，核对文件权限。 |
| 测试分析 | 下方有三种结构的验收记录样表；板件几何实验另附实测。 | **待验证**。三例均应经自然语言入口运行，同版配置记录耗时、修复、误差和失败原因。 |
| 演示与报告 | 参数源、STEP、查看结果和数值可作为几何部分的材料。 | **待验证**。视频依次展示澄清、建模、反馈、修正、同会话修改。提交智能体代码、提示词、工具定义、测试与日志、模型、配置和说明；4–6 页报告用调用链说明系统设计，用前后验收说明自主工作，再记实际分工。 |

上述 STEP 使用 `simplecadapi.kernel.ocp_export.export_step_shapes` 写出，文件头标识 AP214。官方 product 导出工具是另一条路径。本轮已验证 AP214 回读、改参源和静态模型视图；面向用户的编辑器交互仍待联调。[修改后 STEP](experiment/results/after.step) · [官方示例导出路径][export]

## 面向整机测试的验收记录样表

以下为拟议输入及判据，供组会确认。长度以 mm 计。每次填写实际模型版本、模型源、测量报告和对话日志位置。耗时从已确认需求进入执行到本轮通过或终止，另记澄清等待时间；修复数只计失败后发起的重新建模。三个案例的整机结果均待运行。

| 结构与用户交互 | 预先规定的验收条件 | 成功情况 | 实测偏差 | 耗时 | 修复次数 | 失败原因／证据 |
|---|---|---|---|---|---|---|
| 偏置通孔板。先说“孔靠左”，补问后确认所距边及孔心坐标，再只改孔径 | 单一有效实体；孔口两侧贯通；按实验指定的尺寸、孔中心与容差，复核保留约束 | 待测 | 待填 mm | 待填 s | 待填 | 附澄清轮次及改参前后结果 |
| 阶梯轴。确认同轴，长度两段分别 30、20，大径 20，小径 12；刻意把小径建成 14 | 两段圆柱直径和长度各 ±0.05；轴线间距 ≤0.05，方向夹角 ≤0.1°；预置错例应先失败，修正后复查 | 待测 | 待填 mm、° | 待填 s | 待填 | 附被拒的测量值和修正动作 |
| L 形支架。两臂外长均为 40，沿折线宽 25，壁厚 4，两板夹角 90°；随后仅把宽改为 30 | 单一有效实体；在避开交接区的截面测两臂厚，长度、宽度和厚度均 ±0.1；夹角 ±0.5°；复核两次版本 | 待测 | 待填 mm、° | 待填 s | 待填 | 附被保留的壁厚与夹角记录 |

[ask]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/docs/skill/references/workflows/single-part-modeling/role-1-requirements.md
[flow]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/docs/skill/references/workflows/single-part-modeling.md
[cli]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/src/simplecadapi/cli.py
[dims]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/examples/u_link_motor_mount/dimensions.py
[ulink]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/examples/u_link_motor_mount/u_link.py
[nb]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/docs/skill/references/docs/guides/notebook-runtime.md
[runner]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/src/simplecadapi/runtime/runner.py
[select]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/src/simplecadapi/editor/selection.py
[accept]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/examples/u_link_motor_mount/verify/acceptance.py
[export]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/examples/u_link_motor_mount/export.py
[repair]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/docs/skill/references/discipline/failure-and-repair.md
[changes]: https://github.com/PhySpace/SimpleCADAPI/blob/95cdd5fe5d2ea0b2524ad5dbf16d115c48313486/CHANGELOG.md
