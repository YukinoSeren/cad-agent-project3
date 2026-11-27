# 五种 CAD 产品形态，用户实际能改什么

调研日为 2026-11-25。最贴近作业流程的是 CADDesigner。CAD-Assistant 提供了另一种观察模型的办法，Zoo 展示了用户如何指向一个局部特征，Text2CAD 则提供了同一几何的不同难度描述。SCA 贯穿这些比较，作为课程指定的建模工具。下文的产品交互来自公开入口、源码或作者演示。本轮未登录商业服务，也未运行四个对照项目的在线模型。

## 按一次用户操作比较

| 对象 | 用户如何使用，能处理什么 | 澄清、改参和后续修改 | 检查、反馈和复用边界 |
|---|---|---|---|
| CADDesigner | **已核实·源码**，CLI 的 `main()` 循环接收输入。**作者声明·项目说明**，网页也可输入文本、附草图，得到代码与 STEP/STL。齿轮、法兰是作者给出的提示样例，实际成功率待测。[入口](https://github.com/562590763/CADDesigner-Code/blob/65b5f5219974eadbd3ea1d117e467f47cefb69b7/main.py) | **作者声明**，先澄清和扩写需求，再生成建模代码；界面支持会话。能否对每一项建议保留用户确认记录，以及再次改孔径时锁住其余尺寸，需要独立验收。[作者的流程说明](https://github.com/562590763/CADDesigner-Code/blob/65b5f5219974eadbd3ea1d117e467f47cefb69b7/README.md#workflow) | **作者声明**，执行失败后可修复，用渲染视图检查设计意图。课程可借鉴工具和结果的回传路径，对公差仍须实测。Redis、模型服务和工具运行环境都是复现实例时的依赖。[配置与示例](https://github.com/562590763/CADDesigner-Code/blob/65b5f5219974eadbd3ea1d117e467f47cefb69b7/README.md) |
| SimpleCADAPI | **作者声明·SDK 文档**，用户在编辑器中看实体、调参数或点选面，在命令行运行同一份建模文件。样例从带孔法兰到装配体。**已核实**，仓库包含独立的法兰及连杆机构样例。[示例目录](https://github.com/PhySpace/SimpleCADAPI/tree/389d430667679d5fda3188956b023542aa4237f2/examples) | **作者声明**，单件 Skill 给宿主 Agent 提供需求、规划、执行与检查的工作流程。编辑器将选择写入建模文件，使后续“改这条边”有几何参照。缺参时的用户确认由宿主交互实现。[SDK 与 Skill](https://github.com/PhySpace/SimpleCADAPI/blob/389d430667679d5fda3188956b023542aa4237f2/README.md) | **分析推断**，建模、几何查询和导出可作为课程工具的底层能力；需自主决定测哪些几何、如何解释失败，以及何时重试。此处的上游版本仅用于产品比较，实验所用版本见 SCA 专项记录。 |
| CAD-Assistant（ICCV 2025） | **作者声明·论文与演示**，输入可以是草图、文本或扫描，VLLM 规划并执行 FreeCAD Python 操作。**已核实·发布范围**，作者给出的可运行入口在已有 FreeCAD 文件上做 2D/3D 问答，发布说明列出草图、实体识别器。[项目演示](https://cadassistant.github.io/) · [发布说明](https://github.com/dimitrismallis/CAD-Assistant/blob/5fea47309b2db5245f9e01c7a2445cce9dd2d07e/README.md) | **已核实·源码**，一次用户提问内可以有多次规划和执行。**待验证**，连续用户指令是否保留确认过的参数；公开问答基准对此没有评分。[核心循环](https://github.com/dimitrismallis/CAD-Assistant/blob/5fea47309b2db5245f9e01c7a2445cce9dd2d07e/cad_assistant/core.py) | **已核实·源码**，`step` 接收 `max_iterations`（默认 10），识别终止标记，保留步骤日志；`postprocessing` 指定最终 FCStd 路径。论文用投影、草图约束和截面帮助决策，展示的扫描重建任务不能直接据此认定已在仓库完整发布。[实现](https://github.com/dimitrismallis/CAD-Assistant/blob/5fea47309b2db5245f9e01c7a2445cce9dd2d07e/cad_assistant/core.py) · [ICCV 论文](https://openaccess.thecvf.com/content/ICCV2025/papers/Mallis_CAD-Assistant_Tool-Augmented_VLLMs_as_Generic_CAD_Task_Solvers_ICCV_2025_paper.pdf) |
| Zoo Design Studio / Zookeeper | **作者声明·商业产品文档**，在编辑器会话中建模，用户可点选面或边再要求圆角，亦可用 KCL 和特征树调整零件。产品面向单件和装配。[交互说明](https://zoo.dev/docs/zoo-design-studio/zookeeper) | **作者声明**，支持讨论约束、形成计划、增量修改与变体。点选为“这里”提供上下文；官方另指出图形界面目前对自定义 KCL 函数内草图的编辑有限。是否对关键尺寸强制确认待验证。[发布演示](https://zoo.dev/blog/announcing-zookeeper) · [使用说明](https://zoo.dev/docs/zoo-design-studio/zookeeper) | **作者声明**，能用快照、面积、体积、质心和引擎反馈辅助调试。**待验证**，按指定基准面逐孔测量与容差失配的处理。公开客户端与专有云引擎的边界限制了完整本地复现。[技术说明](https://zoo.dev/research/zookeeper) · [产品架构](https://zoo.dev/docs/zoo-design-studio) |
| Text2CAD（NeurIPS 2024） | **已核实·源码**，`test_user_input.py` 接受文本并用训练过的模型预测 CAD 操作序列；**作者声明**，数据从“两个同心圆柱”等简述到逐步给出圆心、半径、拉伸量的详述。[推理入口](https://github.com/SadilKhan/Text2CAD/blob/669a81472ede2269837c22a4d00070eaac360c82/Cad_VLM/test_user_input.py) · [论文](https://arxiv.org/abs/2409.17106) | **已核实·源码**，用户文本入口逐条生成；序列能编码参数。**待验证**，本次检查的入口未展示同一会话的澄清、局部修改与旧约束保留。 | **作者声明**，评估包含参数精度与几何准确性。**分析推断**，适合借用“同一几何，不同描述详略”的出题方式，课程仍须自行实现反馈修正。预训练权重和推理环境是运行前提。[评估与复现说明](https://github.com/SadilKhan/Text2CAD/blob/669a81472ede2269837c22a4d00070eaac360c82/README.md) |

## 源码开放范围与维护记录

**已核实·GitHub 仓库元数据和许可原文。** 下表记录核查当时默认分支尖端的提交日期（UTC）。五个公开仓库均未标记归档。日期表明所见代码快照的新旧，无法推知作者承诺的维护频率。

| 仓库 | 默认分支最近提交 | 根目录许可与适用范围 |
|---|---|---|
| CADDesigner-Code | [2026-07-22 · 65b5f52](https://github.com/562590763/CADDesigner-Code/commit/65b5f5219974eadbd3ea1d117e467f47cefb69b7) | [GPL v2](https://github.com/562590763/CADDesigner-Code/blob/65b5f5219974eadbd3ea1d117e467f47cefb69b7/LICENSE) |
| SimpleCADAPI | [2026-11-17 · 389d430](https://github.com/PhySpace/SimpleCADAPI/commit/389d430667679d5fda3188956b023542aa4237f2) | [Apache 2.0](https://github.com/PhySpace/SimpleCADAPI/blob/389d430667679d5fda3188956b023542aa4237f2/LICENSE) |
| CAD-Assistant | [2025-10-30 · 5fea473](https://github.com/dimitrismallis/CAD-Assistant/commit/5fea47309b2db5245f9e01c7a2445cce9dd2d07e) | 研究代码公开，根许可含非商业条件。[CC BY-NC 4.0](https://github.com/dimitrismallis/CAD-Assistant/blob/5fea47309b2db5245f9e01c7a2445cce9dd2d07e/LICENSE.md) |
| Zoo 客户端 modeling-app | [2026-11-25 · bb3d46c](https://github.com/KittyCAD/modeling-app/commit/bb3d46c33011a3a3b35194db12d4dbaec3362749) | 客户端 [MIT](https://github.com/KittyCAD/modeling-app/blob/bb3d46c33011a3a3b35194db12d4dbaec3362749/LICENSE)。厂商称几何引擎专有；未取得 Zookeeper 服务端实现。[官方文档](https://zoo.dev/docs/zoo-design-studio) |
| Text2CAD | [2025-05-15 · 669a814](https://github.com/SadilKhan/Text2CAD/commit/669a81472ede2269837c22a4d00070eaac360c82) | 作者社区许可标明 [CC BY-NC-SA 4.0](https://github.com/SadilKhan/Text2CAD/blob/669a81472ede2269837c22a4d00070eaac360c82/LICENSE)。数据和权重另有下载入口。 |

## 组会上可以比较的用户体验

**分析推断。** 以“把左边的孔加大到 8 mm”为例，CLI 可以显示孔名、定位基准与已确认尺寸让人选择，图形编辑器可以由用户点选孔壁后提交指令。两种入口都需要从修改后的实体重新测量孔径和孔心位置。若模型有多个相似孔，可以用“是否改对那一个、是否仍保留孔间距、能否从日志找回确认内容”比较两种体验。CAD-Assistant 的标注视图和 Zoo 的点选交互分别提供这两类参照，课程中的开发成本与实际误选率仍待测试。
