import numpy as np
from numpy import linspace

from ase.io import read, write
from ase.calculators.gaussian import Gaussian

from tqdm import tqdm


calc = Gaussian(
    label="g",
    xc="PBE",
    basis="def2tzvp",
    charge=0,
    mult=1,
    nprocshared=16,
    mem="16GB",
    EmpiricalDispersion="GD3BJ",
)

distances = linspace(1.0, 12.0, 120)

atom = read("../../1_OPT/Ar/opt.xyz")
atoms = []
E_list = []
for d in tqdm(distances):
    ref_atom = atom.copy()
    ref_atom.translate([0.0, 0.0, d])
    system = atom + ref_atom
    system.calc = calc
    atoms.append(system)
    E = system.get_potential_energy()
    E_list.append(E)
np.savez("./data.npz", d=distances, E=np.array(E_list))
write("./dist.xyz", atoms)
