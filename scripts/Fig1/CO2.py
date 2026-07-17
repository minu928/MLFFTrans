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

distances = linspace(2.5, 12.5, 120)
angles = linspace(0.0, 90.0, 30)

atom = read("../1_OPT/opt.xyz")
atoms = []
E_list = []
for d in tqdm(distances):
    E_ = []
    for a in angles:
        ref_atom = atom.copy()
        ref_atom.translate([0.0, 0.0, d])
        ref_atom.rotate(a, "z", center=ref_atom.get_positions()[0])
        system = atom + ref_atom
        system.calc = calc
        atoms.append(system)
        E_.append(system.get_potential_energy())
    E_list.append(E_)
np.savez("./data.npz", d=distances, a=angles, E=np.array(E_list))
write("./dist.xyz", atoms)
