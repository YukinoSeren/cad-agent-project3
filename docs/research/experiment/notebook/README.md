# 偏置孔板 notebook 交付验证

交付样件为 [offset_plate.py](offset_plate.py)。六个尺寸各自定义在独立 cell 中，末尾输出一个 SCA Part。复现脚本读取 [cases.json](../cases.json)，用独立进程调用 `run_notebook(overrides=..., cache=False)`，将返回的 Part 导出为 STEP。校验沿用 [plate.py](../plate.py) 的 STEP 回读判据，使用预先确认的尺寸和 ±0.01 mm 容差。

## 复现

在 `docs/research/experiment` 使用 PowerShell。按[实验环境说明](../README.md#复现)准备 `.venv`，然后运行：

```powershell
.venv/Scripts/python.exe -B verify_notebook.py --out notebook-reproduced
```

脚本在指定目录写出三份 STEP 和 `run.json`。三个工况的实际判定与预期一致时退出码为 0。运行日志记录进程 ID、覆盖值、目标、实测、偏差、实体检查和运行时警告。

## 留存结果

Windows 11、CPython 3.12.13、SCA 2.3.0.post1、marimo 0.26.0。[运行日志与逐项实测](results/run.json)

| 工况 | 覆盖参数 | 实测孔径 | 实测孔心距左边 / 下边 | 判定 | STEP |
|---|---|---:|---:|---|---|
| 初始 | 无 | 10 mm | 20 / 15 mm | 通过 | [before.step](results/before.step) |
| 只改孔径 | `hole_d=14` | 14 mm | 20 / 15 mm | 通过 | [after.step](results/after.step) |
| 孔位反例 | `hole_d=14`、`hole_x=25` | 14 mm | 25 / 15 mm | 拒收，`hole_x` 偏差 +5 mm | [off_target.step](results/off_target.step) |

三个 STEP 均回读为单一有效实体，长宽厚实测为 80 × 50 × 8 mm，通孔检查通过。SCA 在导入 notebook 运行时发出 marimo 版本警告，本次禁用缓存的运行完成了改参、导出和回读。自动生成 notebook、`sca edit` 界面和缓存功能仍待验证。
