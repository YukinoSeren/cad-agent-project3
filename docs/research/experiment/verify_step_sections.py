"""Verify the two T3 wall probes on a STEP file, before and after a width change."""

from math import isclose
from pathlib import Path
from tempfile import TemporaryDirectory

import simplecadapi as sca
from simplecadapi.inspect.brep import inspect_section_rdescriptor
from simplecadapi.kernel.ocp_export import export_step_shapes


def measure_probe(step_path, origin, normal, probe_y, thickness_axis):
    section = inspect_section_rdescriptor(step_path, origin, normal)
    if section["closed_contour_count"] != 1 or section["open_contour_count"] != 0:
        raise AssertionError("The fixture section should have one closed contour.")

    # At x=20 or z=20 all contour edges of this fixture are straight.
    hits = []
    for edge in section["edges"]:
        start, end = edge["samples_3d"][0], edge["samples_3d"][-1]
        if min(start[1], end[1]) < probe_y < max(start[1], end[1]):
            fraction = (probe_y - start[1]) / (end[1] - start[1])
            hits.append(start[thickness_axis] + fraction * (end[thickness_axis] - start[thickness_axis]))

    if len(hits) != 2:
        raise AssertionError(f"Expected two section boundary hits, got {hits}.")
    return max(hits) - min(hits)


def main():
    with TemporaryDirectory(prefix="sca-step-sections-") as directory:
        for width in (25.0, 30.0):
            probe_y = width / 2
            horizontal = sca.make_box_rsolid(40, width, 4, (20, probe_y, 0))
            vertical = sca.make_box_rsolid(4, width, 40, (2, probe_y, 0))
            bracket = sca.union_rsolid(horizontal, vertical)
            step_path = Path(directory) / f"bracket-{width:g}.step"
            export_step_shapes([bracket.wrapped], str(step_path))

            horizontal_mm = measure_probe(step_path, (20, 0, 0), (1, 0, 0), probe_y, 2)
            vertical_mm = measure_probe(step_path, (0, 0, 20), (0, 0, 1), probe_y, 0)
            if not all(isclose(value, 4, abs_tol=1e-6) for value in (horizontal_mm, vertical_mm)):
                raise AssertionError(f"Unexpected measured thicknesses: {horizontal_mm}, {vertical_mm}.")
            print(f"W={width:g} mm, probe Y={probe_y:g} mm, walls={horizontal_mm:g}/{vertical_mm:g} mm")


if __name__ == "__main__":
    main()
