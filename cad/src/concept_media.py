"""VatReel concept media from the TRL 3 parametric model (constructable design, VTR-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process. Geometry comes
from cad/src/model.py; the drive figures come from VTR-CAL-001 (docs/04-calcs/sizing.py). The pictures are
made with the pieces of .kit/concept.py render_all, one at a time.

The reel is shown at mid depth (arms 20 degrees below horizontal, lowest carrier 658 mm below the rim)
over a 1.6 m wide pit; the pit is drawn cut open (near wall and right end left out) with the liquor
150 mm below the rim, for context only.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad/src"))
sys.path.insert(0, str(ROOT / "docs/04-calcs"))
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as m  # noqa: E402

PROJECT, TITLE, DWG, DATE = "VatReel", "Hand-cranked reel frame over a pit, concept", "VTR-DWG-010", "2026-10-03"
MD = ROOT / "media"
P = m.PARAMS


def parts(theta=None):
    return [Part(name, shape, color, bom, explode) for name, shape, color, bom, explode in m.build_parts(theta=theta)]


def pit_parts():
    """Pit walls (far side and left end only, so the reel can be seen) and the liquor, for context."""
    W, x0, D = P["PIT_W"], P["PIT_END"], 800.0
    x1 = x0 + P["PIT_LEN"]
    far = m.box(x0 - 150, x0 + 150, W, W + 150, -D, 0)
    end = m.box(x0 - 150, x0, -150, W + 150, -D, 0)
    near = m.box(x0 - 150, x1, -150, 0, -D, 0)
    floor = m.box(x0 - 150, x1, -150, W + 150, -D - 100, -D)
    liquor = m.box(x0, x1, 0, W, P["LIQUOR"] - 4, P["LIQUOR"])
    return [Part("Pit walls (context)", near + end + floor, "#D6D3D1")]


def hero():
    ps = parts(P["THETA_SHALLOW"])
    fig = K.human_figure(1750.0, x=-250.0, y=-1150.0, z=0.0)
    return K._render(ps + [fig] + pit_parts(), MD / "hero.png", title=PROJECT, azim=62, elev=22,
                     note="Seen from across the pit, right of centre, and above, 22 deg elevation; reel at its shallowest "
                          "working depth. Grey figure: 1.75 m person at the crank for scale; pit walls drawn cut open")


def cutaway():
    ps = [p for p in parts() if p.bom not in (6, 15, 20)]
    return K._render(K.cutaway_parts(ps, keep="+Y"), MD / "cutaway.png", azim=-90, elev=18, title=f"{PROJECT}: cutaway",
                     note="Near half removed through the middle of the reel, splash shield left out; seen from the front "
                          "and above, 18 deg elevation")


def exploded():
    return K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     azim=58, elev=24,
                     note="Seen from across the pit, right of centre, and above, 24 deg elevation; numbers match bom/bom.csv")


def web():
    return K.export_web_model(parts(), "media", title=f"{PROJECT}: {TITLE}")


def flow():
    import sizing
    d = sizing.drive()
    return K.flow_diagram(
        [("Hand on the crank", f"{d['crank_force']:.0f} N at {P['CRANK_R']:.0f} mm radius"),
         ("Crank shaft", f"{d['t_crank']:.0f} N m"),
         (f"Chain 1, {P['Z_CRANK']} to {P['Z_JACK1']} teeth", f"{d['t_jack']:.0f} N m on the jackshaft"),
         (f"Chain 2, {P['Z_JACK2']} to {P['Z_AXLE']} teeth", f"{d['t_reel']:.0f} N m on the reel"),
         ("Load through the liquor", f"{d['load_kg']:.0f} kg wet load at {P['RC']:.0f} mm radius")],
        MD / "flow.png",
        f"{PROJECT}: drive train at the worst case, the whole wet load on one carrier bar level with the axle "
        "(all values are estimates)", "", ())


def blueprint():
    import sizing
    from build123d import Compound
    from drawing import Sheet, project_views
    d = sizing.drive()
    ms = sizing.mass_summary()
    ps = parts()
    shown = K.with_scale_figure(ps)
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Massing model for concept communication",
              revisions=[("P1", "Concept sheet from the constructable model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    g_lo, g_hi = m.geometry(P["THETA_SHALLOW"]), m.geometry(P["THETA_DEEP"])
    s.add_notes("Key figures", [
        "Reel 1.18 m over the spokes, 0.6 m long; 6 carrier bars",
        f"Lowest bar {-g_lo['low_bar']:.0f} to {-g_hi['low_bar']:.0f} mm below the rim",
        "Serves pits 1.0 to 2.5 m wide and 1.95 m long or more",
        f"Crank force about {d['crank_force']:.0f} N, 25 kg on one bar (est.)",
        "Drive 6 to 1 by two roller chains; ratchet holds",
        f"Self-locking lift screw, {sizing.lift()['turns']:.0f} turns end to end",
        f"About {ms['total']:.0f} kg; heaviest carry {ms['heaviest']:.0f} kg (est.)",
        "Wetted parts 316L; frame 304 stainless",
    ], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w]())
