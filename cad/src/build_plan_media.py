"""VatReel prototype build plan pictures (VTR-BLD-001, STANDARDS section 18).

Run from the repo root (one group per process on a small machine):
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py components(), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/VTR-DWG-101 to 116        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DATE = "2026-10-03"
_C = {}


def comps(theta=None):
    th = P["THETA"] if theta is None else theta
    if th not in _C:
        _C[th] = {c.key: c for c in m.components(theta=th)}
    return _C[th]


def fuse(keys, src):
    """A compound of the components named, built without re-parenting them (a build123d Compound made
    with children= takes its children away from any compound made earlier)."""
    import build123d as b
    return b.Compound([src[k].shape for k in keys])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def K(keys, name, color, explode=(0, 0, 0), theta=None):
    keys = [keys] if isinstance(keys, str) else keys
    return part(name, fuse(keys, comps(theta)), color, explode)


def win(shape, x0, x1, y0, y1, z0, z1):
    import build123d as b
    w = box(x0, x1, y0, y1, z0, z1)
    try:
        sols = list(shape.solids()) or [shape]
    except Exception:
        sols = [shape]
    kept = []
    for s_ in sols:
        bb = s_.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        r = s_ & w
        if r is not None and r.volume > 1e-3:
            kept.append(r)
    return b.Compound(kept) if kept else None


def W(keys, name, color, bx, theta=None):
    keys = [keys] if isinstance(keys, str) else keys
    return part(name, win(fuse(keys, comps(theta)), *bx), color)


COL = {"base": "#6B7280", "tower": "#4B5563", "brace": "#9CA3AF", "shaft": "#94A3B8", "spr": "#B45309", "chain": "#374151",
       "crank": "#0F766E", "ratchet": "#0D9488", "pawl": "#DC2626", "shield": "#93C5FD", "bracket": "#475569",
       "screw": "#CBD5E1", "trun": "#B08D57", "wheel": "#111827", "tube": "#9CA3AF", "ext": "#A3A3A3", "far": "#6B7280",
       "tt": "#14B8A6", "arm": "#0F766E", "bush": "#F5F5F4", "ptfe": "#E7E5E4", "keeper": "#DC2626", "guard": "#A8A29E",
       "axle": "#CBD5E1", "spider": "#64748B", "bars": "#0EA5E9", "hooks": "#B91C1C", "pads": "#1F2937", "collar": "#111827"}

# Build order (STANDARDS section 18): groups of model components
GROUPS = [
    ("base", "Base frame with pads", ["base", "pads"], COL["base"]),
    ("tower", "Bearing tower and braces", ["tower", "braces"], COL["tower"]),
    ("shafts", "Jackshaft, crank shaft, bushes", ["jackshaft", "crankshaft", "tower_bushes"], COL["shaft"]),
    ("drive1", "Sprockets and chain 1", ["sprocket_j1", "sprocket_c", "sprocket_j2", "chain1"], COL["spr"]),
    ("crank", "Crank and grip", ["crank", "grip"], COL["crank"]),
    ("ratchet", "Ratchet, pawl and cover", ["ratchet", "pawl", "ratchet_cover"], COL["ratchet"]),
    ("shield", "Splash shield", ["shield_frame", "shield_sheet"], COL["shield"]),
    ("far", "Far stand", ["far_stand", "sleeve", "far_pads"], COL["far"]),
    ("tube", "Pivot tube, plug, collars", ["tube_a", "plug", "collars"], COL["tube"]),
    ("armframe", "Arm frame and its bushes", ["torque_tube", "near_arm", "far_arm", "near_arm_bush", "far_arm_bush"], COL["arm"]),
    ("ext", "Extension tube", ["tube_b"], COL["ext"]),
    ("bracket", "Lift screw bracket", ["bracket"], COL["bracket"]),
    ("screw", "Lift screw, trunnions, handwheel", ["screw", "trunnion_up", "trunnion_nut", "handwheel"], COL["screw"]),
    ("reel", "Reel with axle bushes", ["axle", "spider_near", "spider_far", "axle_bushes"], COL["spider"]),
    ("bars", "Carrier bars", ["bars"], COL["bars"]),
    ("keeper", "Saddle keeper", ["keeper"], COL["keeper"]),
    ("drive2", "Axle sprocket and chain 2", ["sprocket_a", "chain2"], COL["chain"]),
    ("guard", "Chain 2 guard", ["guard2"], COL["guard"]),
    ("hooks", "Loading hooks", ["hooks"], COL["hooks"]),
]


def G(key, explode=(0, 0, 0), theta=None, name=None, color=None):
    for k, n, keys, c in GROUPS:
        if k == key:
            return part(name or n, fuse(keys, comps(theta)), color or c, explode)
    raise KeyError(key)


def overview():
    off = {"base": (0, -900, -500), "tower": (0, -900, 0), "shafts": (0, -900, 900), "drive1": (0, -1500, 700),
           "crank": (0, -1600, 300), "ratchet": (0, -1400, 1200), "shield": (0, -400, 0), "far": (0, 900, -300),
           "tube": (0, 300, -500), "armframe": (0, 200, -900), "ext": (0, 1200, -500), "bracket": (-300, 0, 900),
           "screw": (-700, 0, 900), "reel": (900, 300, 300), "bars": (1600, 300, 300), "keeper": (700, 900, -500),
           "drive2": (0, -300, -1300), "guard": (0, -700, -1300), "hooks": (0, -2200, -500)}
    parts = [G(k, off[k]) for k, *_ in GROUPS]
    return bv.overview(parts, OUT / "overview.png", "VatReel prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; arms 20 deg below level",
                       elev=20, azim=-50, size=(13, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheet(n, keys, name, color, neighbours, title, material, notes, theta=None, flat=False, inset=(24, -58)):
    c = comps(theta)
    keys = [keys] if isinstance(keys, str) else keys
    shp = fuse(keys, c)
    view = fuse(keys, comps(0.0)) if flat else None
    nb = [part(k, c[k].shape, "#D1D5DB") for k in neighbours]
    return bv.component_sheet(part(name, shp, color), nb, project="VatReel", dwg_no=f"VTR-DWG-{n}",
                              title=f"VatReel: {title}", material=material, notes=notes, date=DATE,
                              view_shape=view, inset_view=inset)


def sheets(which=None):
    S = {}
    S[101] = lambda: sheet(101, "base", "Base frame", COL["base"], ["tower", "pads", "shield_frame"], "near stand base frame (make 1)",
        "304 stainless SHS 40 x 40 x 2", [
            "Four rails 1750 long and two side rails 580 long, all 40 x 40 x 2 SHS.",
            "Front rail and back rail 660 apart, outside faces; mid rail 320 from front.",
            "Mid rail carries the rear tower plate; front rail the front plate.",
            "Saw square, deburr, tack on a flat floor, check diagonals equal within 3.",
            "Weld all round each joint; cap the open rail ends with 2 mm plate.",
            "Drill 9 mm for M8: four in each rail under the tower plate tabs,",
            "two at each brace foot on the mid rail, four for the shield posts.",
            "Glue an 80 x 80 x 10 EPDM pad under each corner.",
            "Fits: the tower plates stand on the front and mid rails, bolted.",
            "Check: frame flat within 3 mm when standing on its pads."])
    S[102] = lambda: sheet(102, ["tower", "braces"], "Bearing tower and braces", COL["tower"], ["base", "jackshaft", "crankshaft"],
        "bearing tower and braces (make 1)", "304 stainless plate 5, sheet 1.5, plate 6; SHS 30 x 30 x 2", [
            "Two plates 160 x 1050 x 5, set 290 apart (centres), front and rear.",
            "In both plates: a 50 hole 150 up from the bottom edge (jackshaft) and",
            "a 38 hole 950 up (crank shaft), both on the centre line. Drill as a pair.",
            "Rear plate only: 12 hole for the pawl pin, 70 right of and 75 above",
            "the crank hole.",
            "Weld 1.5 mm side sheets on both long edges and a bottom sheet, so the",
            "box is closed round the chain; weld a 6 mm top plate on.",
            "Bend 40 mm tabs at the foot of each plate for 2 x M8 into the rails.",
            "Braces: 30 x 30 x 2 SHS from 830 up the tower side to the mid rail",
            "ends; cut the ends to sit flat; bolt M8 both ends.",
            "Check: a 40 bar passes through both 50 holes square to the plates."])
    S[103] = lambda: sheet(103, ["jackshaft"], "Jackshaft", COL["shaft"], ["tower", "tube_a", "torque_tube"], "jackshaft (make 1)",
        "316 stainless round bar 40", [
            "Saw 660 long from 40 bar; chamfer both ends 1 x 45 with a file.",
            "Mark from the rear end: rear bush at 40, chain 1 sprocket at 185,",
            "front bush at 330, chain 2 sprocket at 480, torque tube bush 495 to",
            "590, pivot tube plug 600 to 660.",
            "Drill 6 mm cross holes for the roll pins through each sprocket hub",
            "with the sprocket on the bar (drill through hub and bar together).",
            "Polish the bush and plug lengths with fine emery; no ridges.",
            "Fits: turns in two flanged bushes in the tower; carries the arm frame",
            "and the pivot tube plug on its front end.",
            "Check: turns freely by hand in both bushes with the tower bolted."])
    S[104] = lambda: sheet(104, ["crankshaft", "crank"], "Crank shaft and crank", COL["crank"], ["tower", "ratchet", "grip"],
        "crank shaft and crank (make 1)", "316 bar 30; 304 flat bar 40 x 10; 304 round 50 for the boss", [
            "Crank shaft: saw 30 bar 512 long; chamfer the ends.",
            "Crank arm: 40 x 10 flat bar, holes 280 apart: 30 for the shaft,",
            "12 for the grip pin. Weld a 50 x 30 boss (bored 30) on the shaft hole.",
            "Weld the 12 grip pin (120 long) into the outer hole, square.",
            "Fit the crank on the shaft end with its face 20 in from the end;",
            "drill 6 through boss and shaft together; roll pin.",
            "Ratchet goes on the same shaft 150 from the crank (sheet 105).",
            "Fits: the shaft turns in the two 30 bushes, 1000 above the rim.",
            "Check: crank arm square to the shaft; grip turns on its pin."])
    S[105] = lambda: sheet(105, ["ratchet", "pawl", "ratchet_cover"], "Ratchet, pawl and cover", COL["ratchet"],
        ["tower", "crankshaft", "crank"], "ratchet, pawl and cover (make 1 set)", "304 plate 8; 304 sheet 1.5; 12 pin; spring", [
            "Ratchet: 24 teeth on a 120 circle, roots on a 104 circle, from 8 plate.",
            "Mark with a printed template; saw and file each tooth: steep face",
            "toward the way the reel would run back. Weld a 44 boss, bore 30.",
            "Pawl: 8 plate, 50 long, with a 12 hole; its tip sits in a tooth root.",
            "Pin: 12 bar through the rear plate, welded to the pawl, with a",
            "release lever outside the cover; spring holds the pawl in.",
            "Cover: 1.5 sheet box 175 x 170 x 52 over wheel and pawl, with holes",
            "for the crank shaft and the pin; 4 M6 into the rear plate.",
            "Fits: wheel pinned on the crank shaft just behind the rear plate.",
            "Check: crank turns one way only; lever lifts the pawl clear."])
    S[106] = lambda: sheet(106, ["shield_frame", "shield_sheet"], "Splash shield", COL["shield"], ["tower", "base"],
        "splash shield (make 1)", "304 angle 25 x 25 x 3; 4 mm translucent polypropylene", [
            "Frame: two posts 1400 long and two cross members 1270 long of angle,",
            "mitred, welded into a rectangle 1320 x 1400 (outside).",
            "One leg lies flat toward the pit; the other leg points back to the",
            "tower so the frame bolts to the front tower plate.",
            "Sheet: 4 PP 1270 x 1140 with a 52 hole for the jackshaft,",
            "centre 60 right of the left edge of the sheet and 115 up.",
            "Drill the sheet 8 at 200 pitch round its edge, frame 6.5; M6 A4",
            "with large washers (PP moves with heat).",
            "Fits: posts bolt to the front rail; the frame to the tower plate.",
            "Check: no gap over 10 mm round the jackshaft or along the posts."])
    S[107] = lambda: sheet(107, ["bracket"], "Lift screw bracket", COL["bracket"], ["tower", "trunnion_up", "screw"],
        "lift screw bracket (make 1)", "304 SHS 50 x 50 x 3; 304 plate 8", [
            "Member 1: 390 of SHS; member 2: 265 of SHS, welded at a right",
            "angle at one end of member 1, pointing toward the pit.",
            "Two fork plates 115 x 66 x 8 under the end of member 2, 50 apart",
            "inside, each with a 16.5 hole 26 up from the bottom, in line.",
            "Member 1 lies on the tower top plate: two 10.5 holes 100 apart.",
            "Weld all round; full fillets on the fork plates (screw load 3.8 kN).",
            "Fits: bolts on the tower top with 2 M10; the upper trunnion block",
            "hangs between the fork plates on two 16 pins.",
            "Check: the two fork holes line up with a 16 bar through both."])
    S[108] = lambda: sheet(108, ["trunnion_up", "trunnion_nut"], "Trunnion blocks", COL["trun"], ["bracket", "screw", "near_arm"],
        "trunnion blocks (make 2)", "316 block 50 x 50 x 50; 16 pins; bronze nut; thrust bearing", [
            "Two 50 cubes. Drill 25 through both on one axis (the screw axis).",
            "Upper block: counterbore 47 x 12 on top for the 51105 thrust bearing.",
            "Nut block: counterbore for the bronze flanged nut; 2 M6 hold it.",
            "Both: drill and tap two opposite faces M16, 25 deep, on the centre,",
            "square to the screw hole; screw in 16 pins with a shoulder.",
            "Fits: upper block hangs in the bracket forks; nut block sits between",
            "the two lever plates on the arm frame. Both pivot on their pins.",
            "Check: each block swings freely on its pins without play over 0.5."])
    S[109] = lambda: sheet(109, ["tube_a", "plug"], "Pivot tube with plug", COL["tube"], ["jackshaft", "torque_tube", "tube_b"],
        "pivot tube with plug (make 1)", "304 pipe 60.3 x 5.54 (2 in schedule 80); UHMW-PE bush", [
            "Saw 1205 long; deburr inside and out.",
            "Plug: a 304 ring 49 outside, 70 long, holding a UHMW bush bored 40;",
            "push it into the near end flush and plug weld through three 8 holes.",
            "At the far end drill 10 cross holes at 100 pitch for the extension pin,",
            "the first 30 from the end, five holes in all.",
            "Slide on the 68 inner collar before the arm frame (sheet 112).",
            "Fits: the plug slides onto the jackshaft tip; the arm frame's far",
            "bush turns on this tube; the extension slides inside it.",
            "Check: the extension tube slides in by hand its whole length."], flat=True)
    S[110] = lambda: sheet(110, ["tube_b"], "Extension tube", COL["ext"], ["tube_a", "sleeve", "far_stand"], "extension tube (make 1)",
        "304 pipe 48.3 x 3.68", [
            "Saw 1550 long; deburr; round the near end edge with a file.",
            "Drill 10 cross holes at 100 pitch along its whole length,",
            "the first 50 from the near end, all in one line.",
            "Mark each hole with the pit width it suits (punch marks).",
            "Fits: slides inside the pivot tube; one lynch pin through both",
            "tubes sets the reach; the far stand clamps on it in a split sleeve.",
            "Not needed for pits up to 1.22 m wide.",
            "Check: at least 250 of it stays inside the pivot tube when pinned."])
    S[111] = lambda: sheet(111, ["far_stand", "sleeve"], "Far stand", COL["far"], ["tube_b", "far_pads"], "far stand (make 1)",
        "304 SHS 50 x 50 x 3; plate 6; block 90 x 60 x 90", [
            "Crossbeam 1650 of SHS; two legs 94 of SHS at its ends, welded.",
            "Foot plates 100 x 100 x 6 under the legs; EPDM pads glued under.",
            "Clamp block 90 x 60 x 90, bored 60.5 on a centre 40 above its base,",
            "then sawn across on the bore centre line; 2 M10 hold the cap.",
            "Weld the lower half on the crossbeam centre, bore along the pit.",
            "Sleeve: 60.3 pipe 60 long bored to fit the extension, sawn in two",
            "along its length; used only when clamping the extension tube.",
            "Fits: stands on the far rim 100 back from the edge.",
            "Check: bore centre 200 above the pad undersides."])
    S[112] = lambda: sheet(112, ["torque_tube", "near_arm", "far_arm"], "Arm frame", COL["arm"], ["jackshaft", "tube_a", "axle"],
        "arm frame (make 1)", "316L tube 76.1 x 3; 316L RHS 60 x 40 x 3; 316L plate 8 and block", [
            "Torque tube 845 long. Arms 812 of RHS, axle centres 900 from the",
            "tube centre; near arm 55 in from the near end, far arm 795.",
            "Weld both arms on a flat jig so the axle holes line up within 1.",
            "Reel end of each arm: a 100 x 90 x 40 block bored 60 for the bush;",
            "near block sawn and bolted (cap); far block open at the top (saddle).",
            "Two lever plates 280 x 50 x 8 on the tube behind the pivot, 50 apart",
            "inside, holes 16.5 at 250 from the tube centre for the nut block.",
            "Press in the UHMW bushes: 40 bore at the near end, 60.3 at the far.",
            "Fits: near bush turns on the jackshaft, far bush on the pivot tube.",
            "Check: axle bar passes both blocks with the tube on a 40/60 mandrel."], flat=True)
    S[113] = lambda: sheet(113, ["guard2"], "Chain 2 guard", COL["guard"], ["near_arm", "chain2", "sprocket_a"],
        "chain 2 guard (make 1)", "316 sheet 1.5; 316 tube 16", [
            "Two side plates: outline of a 112 circle and a 250 circle with",
            "centres 900 apart, joined by straight tangents (print a template).",
            "Holes: outer plate 44 at the small end; inner plate 44 and 52.",
            "Rim strip 34 wide, bent round the outline by hand on a former,",
            "welded or riveted to both plates to make a closed case.",
            "Two spacer tubes 16 x 58 at 300 and 600 from the small end",
            "on the inner plate, with M8 through bolts into the near arm.",
            "Fits: closes chain 2 on all sides; the jackshaft and axle pass",
            "through its holes.",
            "Check: chain 2 runs inside without touching the case."], flat=True)
    S[114] = lambda: sheet(114, ["axle", "spider_near", "spider_far"], "Reel", COL["spider"], ["near_arm", "far_arm", "bars"],
        "reel: axle and two spiders (make 1)", "316L pipe 48.3 x 3.68; 316L flat bar 30 x 6 and 25 x 6; 60.3 hub", [
            "Axle: 900 of pipe. Spider hubs 40 long, at 180 and 780 from the near end.",
            "Each spider: six spokes 30 x 6, 560 long, every 60 degrees,",
            "and six ties 25 x 6 between them at 420 radius (a hexagon).",
            "Make a plywood jig with the six spoke lines so both spiders match;",
            "weld spokes to the hub, then ties, then the hubs to the axle,",
            "with the spokes of both spiders in line along the axle.",
            "Drill each spoke tip 2 x 10.5 for the carrier bar end plates.",
            "Fits: axle ends in the bushes in the arm blocks.",
            "Check: spoke tips run true within 5 when the axle is spun."], flat=True, inset=(20, -40))
    S[115] = lambda: sheet(115, ["bars"], "Carrier bars", COL["bars"], ["spider_near", "spider_far"], "carrier bars (make 6)",
        "316L tube 33.7 x 2; plate 6; eye tabs 6", [
            "Tube 582 long; weld a 75 x 50 x 6 end plate on each end, square.",
            "End plates: 2 x 10.5 holes matching the spoke tips.",
            "Three eye tabs 30 x 22 x 6 (12 hole) on the outer side, at 100,",
            "300 and 500 from the near end plate, for the snap hooks.",
            "Grind welds smooth so hides and yarn do not snag.",
            "Fits: bolted with 2 M10 A4 each end on the inner faces of the",
            "spoke tips; bars run parallel to the axle at 550 radius.",
            "Check: all six the same length within 1."], flat=True)
    S[116] = lambda: sheet(116, ["hooks"], "Loading hooks", COL["hooks"], ["base"], "loading hooks (make 2)",
        "316 round bar 12; PP handle 28", [
            "Rod 1500 long; bend a 60 hook at one end in a vice, smooth the tip.",
            "Push a 120 PP handle on the other end and pin it.",
            "Used from behind the shield to guide hides and hanks onto the bars",
            "and to clip and unclip the snap hooks.",
            "Stored on the back rail of the base frame.",
            "Check: hook end smooth, no burrs that tear hides."])
    for n in sorted(S):
        if which and n not in which:
            continue
        print(n, "->", S[n]())


# ----------------------------------------------------------------- joints
def joints(which=None):
    J = {}
    J[1] = lambda: bv.joint([W("base", "Front and mid rails", COL["base"], (-150, 150, -420, -20, 0, 260)),
                             W("tower", "Tower plates, sheets", COL["tower"], (-150, 150, -420, -20, 0, 260)),
                             W("pads", "EPDM pad", COL["pads"], (-150, 150, -420, -20, 0, 260))],
                            OUT / "joint-01.png", "Joint 1: tower on the base frame",
                            "Plates stand on the front and mid rails, 2 M8 each; bottom sheet closes the box", elev=28, azim=-40)
    bx2 = (-80, 80, -110, 290, 110, 290)
    J[2] = lambda: bv.joint([W("tower", "Front tower plate", COL["tower"], bx2), W("tower_bushes", "Flanged bush", COL["bush"], bx2),
                             W("jackshaft", "Jackshaft", COL["shaft"], bx2), W("sprocket_j2", "Chain 2 sprocket", COL["spr"], bx2),
                             W("guard2", "Chain 2 guard case", COL["guard"], bx2), W("near_arm_bush", "Torque tube bush", COL["bush"], bx2),
                             W("torque_tube", "Torque tube", COL["tt"], bx2), W("plug", "Plug and bush", COL["ptfe"], bx2),
                             W("tube_a", "Pivot tube", COL["tube"], bx2)],
                            OUT / "joint-02.png", "Joint 2: jackshaft tip, arm frame and pivot tube (cut open)",
                            "The torque tube turns on the jackshaft; the pivot tube's plug sits on its tip", cut="-X", elev=20, azim=-35)
    bx3 = (-100, 120, -460, -340, 900, 1120)
    J[3] = lambda: bv.joint([W("tower", "Rear tower plate", COL["tower"], bx3), W("crankshaft", "Crank shaft", COL["shaft"], bx3),
                             W("ratchet", "Ratchet wheel", COL["ratchet"], bx3), W("pawl", "Pawl, pin and lever", COL["pawl"], bx3)],
                            OUT / "joint-03.png", "Joint 3: ratchet and pawl (cover left off)",
                            "Pawl on a pin through the rear plate; spring holds it in a tooth root", elev=15, azim=-140)
    bx4 = (-160, 160, -90, -20, 20, 330)
    J[4] = lambda: bv.joint([W("shield_frame", "Shield frame (angle)", COL["bracket"], bx4), W("shield_sheet", "PP sheet", COL["shield"], bx4),
                             W("tower", "Front tower plate", COL["tower"], bx4), W("base", "Front rail", COL["base"], bx4),
                             W("jackshaft", "Jackshaft", COL["shaft"], bx4)],
                            OUT / "joint-04.png", "Joint 4: shield to tower and base",
                            "Frame bolted to the front plate and front rail; sheet hole round the jackshaft", elev=25, azim=-130)
    bx5 = (-60, 60, 840, 980, 130, 270)
    J[5] = lambda: bv.joint([W("tube_a", "Pivot tube", COL["tube"], bx5), W("collars", "Inner and outer collars", COL["collar"], bx5),
                             W("far_arm_bush", "Far bush", COL["bush"], bx5), W("torque_tube", "Torque tube", COL["tt"], bx5),
                             W("far_arm", "Far arm", COL["arm"], bx5)],
                            OUT / "joint-05.png", "Joint 5: far end of the arm frame (cut open)",
                            "Bush turns on the pivot tube; a collar each side holds it along the tube", cut="-X", elev=20, azim=-35)
    bx6 = (-110, 110, 1330, 1860, 90, 270)
    J[6] = lambda: bv.joint([W("tube_a", "Pivot tube", COL["tube"], bx6), W("tube_b", "Extension tube", COL["ext"], bx6),
                             W("sleeve", "Split sleeve", COL["ptfe"], bx6), W("far_stand", "Far stand clamp", COL["far"], bx6)],
                            OUT / "joint-06.png", "Joint 6: extension tube and far stand clamp (cut open)",
                            "Extension pinned inside the pivot tube; clamp grips it through the split sleeve", cut="-X", elev=22, azim=-30)
    lx, lz = m.lug_xz()
    bx7 = (lx - 80, lx + 120, 80, 180, lz - 90, lz + 90)
    J[7] = lambda: bv.joint([W("near_arm", "Lever plates", COL["arm"], bx7), W("trunnion_nut", "Nut block", COL["trun"], bx7),
                             W("screw", "Lift screw", COL["screw"], bx7), W("torque_tube", "Torque tube", COL["tt"], bx7)],
                            OUT / "joint-07.png", "Joint 7: nut block between the lever plates",
                            "Block pivots on two 16 pins; the screw turns in the bronze nut", elev=20, azim=-50)
    ux, uz = P["SCREW_PIV"]
    bx8 = (ux - 120, ux + 140, 60, 200, uz - 60, uz + 230)
    J[8] = lambda: bv.joint([W("bracket", "Bracket and forks", COL["bracket"], bx8), W("trunnion_up", "Upper block", COL["trun"], bx8),
                             W("screw", "Lift screw", COL["screw"], bx8), W("handwheel", "Handwheel", COL["wheel"], bx8)],
                            OUT / "joint-08.png", "Joint 8: upper trunnion and handwheel",
                            "Block hangs in the forks on two pins; thrust bearing under the handwheel", elev=22, azim=-50)
    ax, az = m.axle_xz()
    bx9 = (ax - 140, ax + 140, 40, 280, az - 140, az + 140)
    J[9] = lambda: bv.joint([W("near_arm", "Near arm block and cap", COL["arm"], bx9), W("axle_bushes", "PTFE bush", COL["ptfe"], bx9),
                             W("axle", "Axle", COL["axle"], bx9), W("sprocket_a", "Axle sprocket", COL["spr"], bx9),
                             W("chain2", "Chain 2", COL["chain"], bx9), W("guard2", "Guard case", COL["guard"], bx9),
                             W("spider_near", "Near spider", COL["spider"], bx9)],
                            OUT / "joint-09.png", "Joint 9: axle in the near arm (cut open)",
                            "Split block with a bolted cap; sprocket inside the guard case", cut="-X", elev=20, azim=-35)
    bx10 = (ax - 80, ax + 80, 860, 970, az - 70, az + 70)
    J[10] = lambda: bv.joint([W("far_arm", "Far arm saddle", COL["arm"], bx10), W("keeper", "Keeper", COL["keeper"], bx10),
                              W("axle_bushes", "PTFE bush", COL["ptfe"], bx10), W("axle", "Axle", COL["axle"], bx10)],
                             OUT / "joint-10.png", "Joint 10: axle in the far saddle",
                             "Axle drops in from above; the keeper swings shut over it and is pinned", elev=25, azim=-35)
    tx, tz = ax, az + P["RC"]
    bx11 = (tx - 70, tx + 70, 215, 330, tz - 60, tz + 70)
    J[11] = lambda: bv.joint([W("spider_near", "Spoke tip", COL["spider"], bx11), W("bars", "Carrier bar and end plate", COL["bars"], bx11)],
                             OUT / "joint-11.png", "Joint 11: carrier bar on a spoke",
                             "End plate on the inner face of the spoke tip, 2 M10 A4", elev=25, azim=-35)
    out = []
    for n in sorted(J):
        if which and n not in which:
            continue
        out.append(J[n]())
        print(n, "->", out[-1])
    return out


# ----------------------------------------------------------------- steps
def steps(which=None):
    TL = P["THETA_LIFT"]
    # One arm angle per process: the frame does not depend on it, and mixing two model builds in one
    # picture has dropped parts from the render. Steps 1 to 12 use the lifted angle; step 13 the working one.
    th0 = P["THETA"] if which == [13] else TL
    g0 = globals()["G"]
    def G(key, explode=(0, 0, 0), theta=None, name=None, color=None):  # noqa: F811
        return g0(key, explode, th0, name, color)
    def st(n, done, new, title, sub, **kw):
        kw.setdefault("elev", 22)
        kw.setdefault("azim", -50)
        return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)
    E = {}
    E[1] = lambda: st(1, [], [G("base", (0, 0, 300))], "base frame on the near rim",
                      "Check the rim is sound; set the frame 40 mm back from the edge, level on its pads")
    E[2] = lambda: st(2, [G("base")], [G("tower", (0, 0, 500))], "tower and braces",
                      "Stand the tower on the rails, 2 M8 each plate; bolt the braces to the mid rail")
    E[3] = lambda: st(3, [G("base"), G("tower")], [G("shafts", (0, -500, 0)), G("drive1", (0, -250, 300))],
                      "shafts, bushes, sprockets and chain 1", "Bushes in; feed each shaft through with its sprocket inside the box; join chain 1; pin")
    E[4] = lambda: st(4, [G("base"), G("tower"), G("shafts"), G("drive1")], [G("crank", (0, -300, 0)), G("ratchet", (0, -200, 0))],
                      "ratchet, pawl, cover and crank", "Ratchet pinned behind the rear plate; pawl and spring; cover on; crank pinned last",
                      azim=-130)
    near = [G("base"), G("tower"), G("shafts"), G("drive1"), G("crank"), G("ratchet")]
    E[5] = lambda: st(5, near, [G("shield", (0, 400, 0))], "splash shield",
                      "Bolt the frame to the front plate and front rail; sheet hole over the jackshaft")
    near2 = near + [G("shield")]
    E[6] = lambda: st(6, near2, [G("far", (0, 0, 300))], "far stand on the far rim",
                      "Set it 100 mm back from the far edge, in line with the jackshaft (string line)")
    E[7] = lambda: st(7, near2 + [G("far")], [part("Pivot tube with the arm frame on it", fuse(
                          ["tube_a", "plug", "collars", "torque_tube", "near_arm", "far_arm", "near_arm_bush", "far_arm_bush"], comps(th0)),
                          COL["arm"], (0, 450, 0))],
                      "pivot tube and arm frame onto the jackshaft",
                      "Two people on opposite rims, 13.5 kg each: slide the plug and bush onto the jackshaft tip. Hold point")
    armTL = part("Arm frame", fuse(["torque_tube", "near_arm", "far_arm", "near_arm_bush", "far_arm_bush"], comps(th0)), COL["arm"])
    tube = G("tube", theta=TL)
    E[8] = lambda: st(8, near2 + [G("far"), tube, armTL], [G("ext", (0, 700, 0), theta=TL)],
                      "extension tube and far clamp", "Push the extension out to the far stand, pin it, close the clamp on the sleeve")
    frame = near2 + [G("far"), tube, armTL, G("ext", theta=TL)]
    E[9] = lambda: st(9, frame, [G("bracket", (0, 0, 300), theta=TL), G("screw", (0, 0, 500), theta=TL)],
                      "bracket and lift screw", "Bolt the bracket on the tower top; hang the screw in the forks; nut block between the lever plates",
                      azim=-60)
    frame2 = frame + [G("bracket", theta=TL), G("screw", theta=TL)]
    E[10] = lambda: st(10, frame2, [G("reel", (0, 0, 500), theta=TL), G("bars", (0, 0, 500), theta=TL)],
                       "reel onto the raised arms", "Arms raised; two people on opposite rims carry the reel on the assembly bar and lower it in. Hold point",
                       label_done=False)
    frame3 = frame2 + [G("reel", theta=TL), G("bars", theta=TL)]
    E[11] = lambda: st(11, frame3, [G("keeper", (0, 0, 250), theta=TL), G("drive2", (0, -300, 0), theta=TL)],
                       "keeper, near cap, axle sprocket, chain 2", "Near cap bolted; keeper swung shut and pinned; sprocket pinned; chain 2 joined",
                       label_done=False)
    frame4 = frame3 + [G("keeper", theta=TL), G("drive2", theta=TL)]
    E[12] = lambda: st(12, frame4, [G("guard", (0, -350, 0), theta=TL)], "chain 2 guard",
                       "Fit the case round chain 2; two M8 bolts through the spacers into the near arm", label_done=False)
    allw = [G(k) for k, *_ in GROUPS if k != "hooks"]
    E[13] = lambda: st(13, allw, [G("hooks", (0, -300, 200))], "lower to the working depth; hooks on the base",
                       "Wind the handwheel down to the depth marked for this pit; store the hooks on the back rail", label_done=False)
    out = []
    for n in sorted(E):
        if which and n not in which:
            continue
        out.append(E[n]())
        print(n, "->", out[-1])
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview"]
    what, nums = args[0], [int(a) for a in args[1:]]
    {"overview": lambda: print("overview ->", overview()), "sheets": lambda: sheets(nums or None),
     "joints": lambda: joints(nums or None), "steps": lambda: steps(nums or None)}[what]()
