# Data underlying the figures

Data for the manuscript *"Density diversity in training data shapes the thermodynamic
transferability of machine learning interatomic potentials in fluids"*.

All arrays are stored as compressed NumPy archives (`.npz`), readable with:

```python
import numpy as np
d = np.load("dimer_energy/CO2_7net-0-D3.npz")
print(list(d.keys()))
```

## Directory map

| Directory | Figures / tables it supports | Contents |
|---|---|---|
| `dimer_energy/` | Fig. 1; Tables S1–S3 | Pairwise interaction energy scans for the Ar–Ar, CO2–CO2, and H2O–H2O dimers |
| `foundation_rdf/` | Fig. 2 | Liquid-phase RDFs of CO2 and H2O from foundation MLIPs, with experimental references |
| `foundation_co2_density/` | Fig. 3; Fig. S2 | CO2 center-of-mass RDFs from foundation MLIPs across four reduced densities at 310 K |
| `co2_fromscratch/` | Fig. 4; Figs. S3–S5 | From-scratch CO2 MLIPs: RDFs, energy/force/stress labels, and learning curves |
| `h2o_distilled_structure/` | Figs. 5a–c, 6; Figs. S6–S8, S10 | Distilled H2O MLIPs: oxygen–oxygen RDFs and cumulative coordination numbers |
| `h2o_distilled_dynamics/` | Figs. 5d–i; Figs. S9, S11–S13; Tables S4–S5 | Distilled H2O MLIPs: mean-squared displacements, pressures, and learning curves |
| `scripts/` | — | Simulation and training input scripts used to generate the data above |

## Training-strategy labels

The three training strategies compared throughout the manuscript appear as directory names:

| Directory name | Manuscript name | Meaning |
|---|---|---|
| `NVar` | NoVar | No thermodynamic variance; extra frames drawn from the baseline condition |
| `TVar` | TempVar | Temperature variance at fixed density |
| `DVar` | DenVar | Density variance at fixed temperature |
| `BASE` / `REF` | reference | Reference data: MB-nrg for CO2, the 7net-omni teacher for H2O |

Note that the reference directory is named `BASE` under `co2_fromscratch/` and
`h2o_distilled_dynamics/`, but `REF` under `h2o_distilled_structure/`.

## Contents by directory

### `dimer_energy/` — Fig. 1, Tables S1–S3

Files are named `{species}_{model}.npz` for species `Ar`, `CO2`, `H2O` and models
`PBE-D3(BJ)` (reference), `7net-0-D3`, `7net-MF-OMPA-D3`, `7net-OMAT-D3`, and `SO3LR`.

| Key | Description |
|---|---|
| `x` | Intermolecular separation (Å) |
| `y` | Interaction energy (eV) |

### `foundation_rdf/` — Fig. 2

Files are named `{species}_{model}.npz`. `CO2_EPM2.npz` is the EPM2 classical force field.

| Key | Description |
|---|---|
| `radii` | Radial distance (Å) |
| `rdf` | Radial distribution function |
| `cn` | Cumulative coordination number |

### `foundation_co2_density/` — Fig. 3, Fig. S2

Files are named `rho{reduced_density}_{model}.npz` for reduced densities
0.34, 0.77, 1.20, and 1.50 at 310 K. The companion `rho{...}_T310K.csv` files hold the
experimental reference RDF at each density. Keys match `foundation_rdf/`.

### `co2_fromscratch/` — Fig. 4, Figs. S3–S5

State points are labelled in reduced units, `T{Tr}_R{rho_r}.npz`, with
Tr = T/Tc (Tc = 304 K) and rho_r = rho/rho_c (rho_c = 10.6 mol/L).

```
co2_fromscratch/{BASE,NVar,TVar,DVar}/
├── RDF/T{Tr}_R{rho_r}.npz     keys: radii, rdf, cn
├── EFS/T{Tr}_R{rho_r}.npz     keys: E, F, S
└── lc.csv                     training curve (BASE has none; it is the MB-nrg reference)
```

`EFS` holds per-frame labels for a 2001-frame trajectory of 64 CO2 molecules (192 atoms):
`E` energy (eV, shape `[n_frames]`), `F` forces (eV/Å, shape `[n_frames, 192, 3]`),
`S` stress (shape `[n_frames, 6]`). These feed the energy and force MAE panels
(Fig. 4b, c, e, f), computed against the `BASE` (MB-nrg) labels.

`lc.csv` columns: epoch, then the energy and force RMSE used in Fig. S5
(the plotting code reads columns 0, 2, 3).

### `h2o_distilled_structure/` — Figs. 5a–c, 6; Figs. S6–S8, S10

```
h2o_distilled_structure/{REF,NVar,TVar,DVar}/T{T}_rho{rr}.npz
```

State points are labelled in physical units: T in K (300, 500, 700, 900) and `rr` the
density in units of 0.1 g/cm^3 (`03`, `06`, `10` for 0.3, 0.6, 1.0 g/cm^3).

| Key | Description |
|---|---|
| `radii` | Radial distance (Å) |
| `rdf` | Oxygen–oxygen radial distribution function |
| `cn` | Cumulative coordination number; N(r_cut) in the manuscript is this evaluated at r_cut = 6.0 Å |

The RDF similarity score maps (Fig. 5a–c) and the coordination number analysis (Fig. 6)
are both derived from these files.

### `h2o_distilled_dynamics/` — Figs. 5d–i; Figs. S9, S11–S13; Tables S4–S5

```
h2o_distilled_dynamics/{BASE,NVar,TVar,DVar}/
├── MSD/T{T}_rho{rr}.npz    keys: tau, msd
├── PV/T{T}_rho{rr}.npz     keys: Pavg, Pstd, V
└── lc.csv                  training curve (BASE has none; it is the teacher)
```

`MSD` holds the mean-squared displacement: `tau` lag time (ps), `msd` (Å^2). The
self-diffusion coefficient is obtained from a linear fit over 10 ≤ tau < 100 ps
(Table S4, Fig. 5d–f).

`PV` holds the pressure averaged over the NVT trajectory: `Pavg` (GPa,
compressive-positive convention), `Pstd` the standard error of the mean (GPa), and
`V` the cell volume (Å^3). These feed Table S5 and Fig. 5g–i.

### `scripts/` — data generation

Input scripts for the simulations and trainings that produced the data above. They are
grouped by the figure whose data they generate, and are provided as a record of the
protocol; paths inside them refer to the original working directories, and the initial
structures and model checkpoints are not included here.

```
scripts/
├── Fig1/{Ar,CO2,H2O}.py                        Gaussian 16 dimer energy scans (PBE-D3(BJ)/def2-TZVP)
├── Fig2/
│   ├── 7net-0/run.py                           ASE NVT MD with SevenNet-0 + D3
│   ├── SO3LR/run.py                            ASE NVT MD with SO3LR
│   └── epm/{in.lmps,in.script}                 LAMMPS NVT MD with the EPM2 force field
├── Fig4/
│   ├── MB-nrg/{config.xml,config.nrg,mbx.json,config.xyz,run_i-pi.sh}
│   │                                           MB-nrg reference MD via MBX coupled to i-PI
│   ├── run.CO2.py                              ASE NVT MD with the from-scratch CO2 model
│   └── input.CO2.FromScratchModel.yaml         SevenNet training input (from-scratch CO2)
└── Fig5/
    ├── run.py                                  ASE NVT MD with the distilled H2O model
    └── input.H2O.DistillationModel.yaml        SevenNet training input (distilled H2O)
```
