"""SCA single-part experiment. All model inputs and measured lengths are in mm."""
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform
from time import perf_counter

import simplecadapi as sca
from simplecadapi.inspect.brep import inspect_step_rbrepinspection
from simplecadapi.kernel.ocp_export import export_step_shapes


def build(length, width, thickness, diameter, hole_x, hole_y):
    """Place the lower left corner at the origin and extrude toward +Z."""
    profile = sca.make_rectangle_rface(length, width, center=(length / 2, width / 2, 0))
    plate = sca.extrude_rsolid(profile, (0, 0, 1), thickness)
    cutter = sca.make_cylinder_rsolid(diameter / 2, thickness + 2, (hole_x, hole_y, -1))
    return sca.cut_rsolid(plate, cutter)


def check(inspection, target, tolerance):
    box = inspection.bounding_box
    measured = dict(zip(("length", "width", "thickness"), (box[i+3] - box[i] for i in range(3))))
    walls = [f for f in inspection.faces if f["surface"]["type"] == "Cylinder"]
    topology = {"valid": inspection.valid, "single_solid": inspection.counts["solid"] == 1,
                "single_cylindrical_wall": len(walls) == 1, "through_hole": False}
    if len(walls) == 1:
        wall = walls[0]
        surface = wall["surface"]
        x, y, _ = surface["location"]
        measured.update(diameter=2 * surface["radius"], hole_x=x-box[0], hole_y=y-box[1])
        rims = [edge for edge in inspection.edges
                if edge["type"] == "Circle" and wall["index"] in edge["face_indices"]]
        heights = sorted(rim["center"][2] for rim in rims)
        topology["through_hole"] = (len(heights) == 2 and
                                    abs(heights[0] - box[2]) <= tolerance and
                                    abs(heights[1] - box[5]) <= tolerance and
                                    abs(abs(surface["axis"][2]) - 1) <= 1e-6)
    deviations = {key: value - target[key] for key, value in measured.items()}
    failed = [key for key in target if key not in deviations or abs(deviations[key]) > tolerance]
    failed.extend(key for key, ok in topology.items() if not ok)
    return {"measured_mm": measured, "deviation_mm": deviations, "geometry_checks": topology,
            "failed_checks": failed, "accepted": not failed}


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=here / "cases.json")
    parser.add_argument("--out", type=Path, default=here / "results")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.cases.read_text(encoding="utf-8-sig"))
    result = {"sca": version("simplecadapi"), "python": platform.python_version(),
              "platform": platform.platform(), "absolute_tolerance_mm": config["absolute_tolerance_mm"],
              "cases": []}
    for case in config["cases"]:
        start = perf_counter()
        name = case["name"]
        target = config["confirmed"] | case["confirmed_changes"]
        inputs = target | case["model_overrides"]
        solid = build(**inputs)
        step = args.out / f"{name}.step"
        export_step_shapes([solid.wrapped], str(step))
        inspection = inspect_step_rbrepinspection(step)
        row = check(inspection, target, config["absolute_tolerance_mm"])
        raw = inspection.to_dict()
        raw["source"] = step.name
        (args.out / f"{name}.brep.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
        sca.render_screenshot_rpath(solid, str(args.out / f"{name}.png"), view="iso",
                                    image_size=(800, 500), show_axes=False, show_legend=False)
        row.update(case=name, target_mm=target, model_inputs_mm=inputs,
                   volume_mm3=inspection.volume, elapsed_s=round(perf_counter()-start, 4),
                   matches_expected_verdict=row["failed_checks"] == case["expected_failures"])
        result["cases"].append(row)
        print(name, row["accepted"], row["failed_checks"], row["measured_mm"], flush=True)
    (args.out / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return 0 if all(row["matches_expected_verdict"] for row in result["cases"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
