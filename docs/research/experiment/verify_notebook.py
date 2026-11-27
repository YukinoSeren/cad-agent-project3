"""Rebuild each offset-plate notebook case in a fresh process and measure its STEP."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import version
import json
from multiprocessing import get_context
import os
from pathlib import Path
import platform
import warnings

from plate import check
from simplecadapi.inspect.brep import inspect_step_rbrepinspection
from simplecadapi.kernel.ocp_export import export_step_shapes


def run_case(notebook, out, confirmed, tolerance, case):
    target = confirmed | case["confirmed_changes"]
    changes = case["confirmed_changes"] | case["model_overrides"]
    overrides = {"hole_d" if key == "diameter" else key: value for key, value in changes.items()}

    with warnings.catch_warnings(record=True) as recorded_warnings:
        warnings.simplefilter("always", RuntimeWarning)
        from simplecadapi.runtime import run_notebook

        result = run_notebook(notebook, overrides=overrides, cache=False)

    step = out / f"{case['name']}.step"
    export_step_shapes([result.product.body.wrapped], str(step))
    inspection = inspect_step_rbrepinspection(step)
    verdict = check(inspection, target, tolerance)
    return {
        "case": case["name"],
        "process_id": os.getpid(),
        "overrides": overrides,
        "step": step.name,
        "target_mm": target,
        **verdict,
        "volume_mm3": inspection.volume,
        "expected_failures": case["expected_failures"],
        "matches_expected_verdict": verdict["failed_checks"] == case["expected_failures"],
        "runtime_warnings": [str(item.message) for item in recorded_warnings],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Directory for STEP files and run.json")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    here = Path(__file__).resolve().parent
    notebook = here / "notebook" / "offset_plate.py"
    config = json.loads((here / "cases.json").read_text(encoding="utf-8-sig"))
    tolerance = config["absolute_tolerance_mm"]

    cases = []
    with ProcessPoolExecutor(max_workers=1, mp_context=get_context("spawn"), max_tasks_per_child=1) as pool:
        for case in config["cases"]:
            row = pool.submit(run_case, notebook, args.out, config["confirmed"], tolerance, case).result()
            cases.append(row)
            print(row["case"], row["accepted"], row["failed_checks"], row["measured_mm"], flush=True)

    report = {
        "sca": version("simplecadapi"),
        "marimo": version("marimo"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "notebook": notebook.name,
        "runtime": "simplecadapi.runtime.run_notebook",
        "cache": False,
        "absolute_tolerance_mm": tolerance,
        "cases": cases,
    }
    (args.out / "run.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if all(row["matches_expected_verdict"] for row in cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
