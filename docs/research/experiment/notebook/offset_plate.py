# /// script
# requires-python = ">=3.12"
# dependencies = ["simplecadapi==2.3.0.post1", "marimo==0.26.0"]
#
# [tool.simplecadapi]
# id = "offset-plate"
# kind = "part"
# ///
import marimo

app = marimo.App()

with app.setup:
    import simplecadapi as scad


@app.cell
def _():
    length = scad.var("length", 80.0, unit="mm")
    return (length,)


@app.cell
def _():
    width = scad.var("width", 50.0, unit="mm")
    return (width,)


@app.cell
def _():
    thickness = scad.var("thickness", 8.0, unit="mm")
    return (thickness,)


@app.cell
def _():
    hole_d = scad.var("hole_d", 10.0, unit="mm")
    return (hole_d,)


@app.cell
def _():
    hole_x = scad.var("hole_x", 20.0, unit="mm")
    return (hole_x,)


@app.cell
def _():
    hole_y = scad.var("hole_y", 15.0, unit="mm")
    return (hole_y,)


@app.cell
def _(length, width):
    profile = scad.make_rectangle_rface(length, width, center=(length / 2, width / 2, 0))
    return (profile,)


@app.cell
def _(profile, thickness):
    plate = scad.extrude_rsolid(profile, (0, 0, 1), thickness)
    return (plate,)


@app.cell
def _(hole_d, hole_x, hole_y, thickness):
    cutter = scad.make_cylinder_rsolid(hole_d / 2, thickness + 2, (hole_x, hole_y, -1))
    return (cutter,)


@app.cell
def _(cutter, plate):
    body = scad.cut_rsolid(plate, cutter)
    return (body,)


@app.cell
def _(body):
    offset_plate = scad.make_part_rpart(part_id="offset-plate", body=body, name="Offset hole plate")
    return (offset_plate,)


if __name__ == "__main__":
    app.run()
