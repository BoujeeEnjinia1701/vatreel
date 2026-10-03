---
doc_id: VTR-PRB-001
title: VatReel problem statement
project: VatReel
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 and 3 update; pit length and liquor level added to the environment; first co-design candidate; questions for the site survey
---

# VatReel problem statement

Pit and vat processes still depend on people moving wet, heavy material through chemical baths by hand. The simplest engineering control, keeping the body out of the liquor, is missing in the workshops that need it most.

## The problem

Tannery liquors include lime, sulphides, acids and chromium salts; dye baths can be hot and contain sensitising dyes. Studies in Kanpur and Sialkot link skin disease and raised chromium levels to this work, and the risk rises with the degree of skin contact ([Kashyap et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8530047); [Khan et al., 2013](https://journals.sagepub.com/doi/10.1177/0748233711430974)). Gloves and boots help, but workers in Hazaribagh reported that liquor still reaches the skin when they climb into pits ([HRW, 2012](https://www.hrw.org/report/2012/10/09/toxic-tanneries/health-repercussions-bangladeshs-hazaribagh-leather)).

Mechanised answers exist. The winch dyeing machine, one of the oldest forms of dyeing machine, pulls cloth over a reel through the bath ([Wikipedia](https://en.wikipedia.org/wiki/Winch_dyeing_machine)), and tanneries use powered paddlewheels and drums ([Exeter Machine](https://exetermachineco.com/machines/)). These are fixed, powered and built for a factory floor. Small workshops that work in pits have no portable, hand-powered way to move a load through the bath, so they use their hands.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Pit and vat workers | Move hides or yarn through the liquor without putting hands, arms or legs into it | Open pits and vats in small tanneries and dye yards, often wet floors and poor lighting |
| Workshop owners and cooperatives | A control they can afford, build locally and fit over the pits they already have | Low capital, no spare power supply, pits of mixed sizes |
| Local fabricators | Drawings and a cut list that use stock sections and hand tools | Small metal workshops near tannery or craft clusters |
| NGOs, unions and auditors | A documented engineering control to recommend to small suppliers | Worker safety programmes in leather and textile supply chains |

## Operating environment

- Set across open pits or vats about 1.0 to 2.5 m (3 to 8 ft) wide and at least 1.9 m (6.2 ft) long; exact range to be confirmed by site survey.
- Pits with the rim level with the floor and the liquor about 150 mm (6 in) below the rim (assumed).
- Liquors from strongly alkaline (liming) to acidic (pickling), with chromium salts, sulphides and dyes.
- Dye baths up to about 98 °C (208 °F), the top of the range used in winch dyeing ([Wikipedia](https://en.wikipedia.org/wiki/Winch_dyeing_machine)).
- Wet, slippery floors; outdoor or open-sided sheds; hot and humid climates.
- No reliable mains power assumed.

## Constraints

- Prototype parts budget: USD 1,500 or less.
- Hand powered only; no motor in the base design.
- Buildable with hand tools and stock steel or stainless sections; no casting or machining beyond drilling and cutting.
- Each module light enough for two people to carry (target 25 kg (55 lb) or less, estimate).
- Fits existing pits without civil works.
- Open design: hardware under CERN-OHL-S-2.0, any software or calculators under MIT.

## Out of scope

- Motorised drives, drums and automatic dosing.
- Effluent treatment and chemical substitution (important, but separate problems).
- Fixed plant for large tanneries.
- Personal protective equipment design.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Winch (beck) dyeing machine | Reel that pulls cloth in rope form through a dye bath in an endless loop | Fixed, powered factory machine with its own tank; not portable and not for hides or pits | [link](https://en.wikipedia.org/wiki/Winch_dyeing_machine) |
| US3513672A, paddle dyeing machine (expired) | Tilting cylindrical dye tank with an integral paddle for circulation, hydraulically powered | Powered, fixed tank; no hand operation or use over an existing pit | [link](https://patents.google.com/patent/US3513672A/en) |
| Tannery paddlewheels and drums (for example Exeter Machine) | Wooden paddlewheels from about 1.2 by 1.2 m and drums up to about 3.7 m for processing hides | Powered plant equipment that replaces the pit rather than working over it | [link](https://exetermachineco.com/machines/) |
| Traditional pit working (Chouara, Fez) | Workers stand in the vats and slosh hides by hand and foot | The status quo: full body contact with the liquor | [link](https://www.loe.org/shows/segments.html?programID=14-P13-00044&segmentID=4) |

## Co-design

A tannery or craft-dyeing cluster association, or a worker health NGO working with one, that can give access to real pits, liquors and workers, and help test loading and cranking with the people who do the job.

First candidate to approach (decided 2026-10-03 under Amish's pre-approval, VTR-DDR-001): a worker health NGO or tannery association in the Kanpur leather cluster, India, where the skin-contact evidence above was gathered. This is a candidate, not an agreed partner.

## Questions for the site survey

These are questions about the users' pits and processes, answered with the first partner; the design decisions themselves are in VTR-DEC-001.

- Which process steps matter most for exposure (liming, pickling, tanning, dyeing), and does one reel suit all of them?
- What pit sizes and depths are typical in the first partner cluster?
- How do workers load heavy wet hides onto carriers without handling liquor-soaked leather?
- Which materials (stainless grade, HDPE, coated steel) survive both lime and acid liquors at this budget?
- Is one reel per pit practical, or should the frame move between pits?

> **Safety:** The work described here involves corrosive liquors (lime, sulphides, acids, chromium salts), hot dye baths near 98 °C (208 °F), open pit edges and wet floors. VatReel adds a hand-cranked machine with moving parts. Any site work, survey or trial follows a local risk assessment, with gloves, eye protection and boots worn throughout.
