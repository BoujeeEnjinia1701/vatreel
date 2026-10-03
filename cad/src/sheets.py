"""VatReel general arrangement drawing VTR-DWG-001 (Rev P2).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/VTR-DWG-001.svg, .pdf and .png from the parametric model, arms at the modelled
mid-depth angle. The concept sheet in media/ uses VTR-DWG-010; the making sketches for the build plan
are VTR-DWG-101 onward. Figures in the notes come from VTR-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "docs/04-calcs"))
from drawing import Sheet, project_views  # noqa: E402
import model as m  # noqa: E402
import sizing  # noqa: E402
from build123d import Compound  # noqa: E402

P = m.PARAMS
DATE = "2026-10-03"
parts = m.build_parts()
asm = m.assembly(parts)
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
bb = asm.bounding_box()
d = sizing.drive()
lf = sizing.lift()
ms = sizing.mass_summary()
sp = sizing.spans()
g_lo, g_hi, g_up = m.geometry(P["THETA_SHALLOW"]), m.geometry(P["THETA_DEEP"]), m.geometry(P["THETA_LIFT"])

s = Sheet(project="VatReel", title="Hand-cranked reel frame over a pit: general arrangement", dwg_no="VTR-DWG-001",
          rev="P2", author="Amish Chadha", date=DATE, concept=True, scale=None,
          material="304 stainless frame; 316L wetted parts; PTFE and UHMW-PE bushes. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (VTR-CAL-001)", DATE, "AC"),
                     ("P2", "Design for construction (VTR-DDR-002)", DATE, "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 57, 140, 62, label="Isometric view", sublabel="Not to scale; arms 20 deg below level")
s.add_notes("Key dimensions (mm) and data", [
    f"Frame {bb.size.X:.0f} long; {bb.size.Y:.0f} across a 1,600 pit",
    f"Pivot line {P['PIV_Z']:.0f} above the rim; arms {P['ARM_L']:.0f} long",
    f"Reel {2 * P['SPOKE_R']:.0f} over spokes, bars at {P['RC']:.0f} radius",
    f"Lowest bar {-g_lo['low_bar']:.0f} to {-g_hi['low_bar']:.0f} below the rim",
    f"Lifted: lowest bar {g_up['low_bar']:.0f} above the rim",
    f"Pits {sp['a_only'][0]:.0f} to 2,500 wide, {sp['pit_len']:.0f} long or more",
    f"Crank {P['CRANK_Z']:.0f} high, {P['CRANK_R']:.0f} radius, 6 to 1",
    f"About {d['crank_force']:.0f} N at the crank, 25 kg on one bar",
    f"Lift screw Tr24 x 5, {lf['turns']:.0f} turns; ratchet on crank",
    f"Chains 08B: {P['Z_CRANK']}/{P['Z_JACK1']} and {P['Z_JACK2']}/{P['Z_AXLE']} teeth",
    f"Shield {P['SHIELD_X'][1] - P['SHIELD_X'][0]:.0f} wide, {P['SHIELD_Z'][0]:.0f} to {P['SHIELD_Z'][1]:.0f} high",
    f"About {ms['total']:.0f} kg; heaviest carry {ms['heaviest']:.0f} kg by two",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=130, width=140)
s.save(ROOT / "cad/drawings/VTR-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/VTR-DWG-001.svg, .pdf, .png")
