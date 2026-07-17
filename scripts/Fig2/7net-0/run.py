import numpy as np

from ase.io import read, write
from ase.md import MDLogger
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.nose_hoover_chain import NoseHooverChainNVT
from ase.units import fs

from sevenn.calculator import SevenNetD3Calculator


calc = SevenNetD3Calculator(model="7net-0", device="cuda", enable_cueq=True)

init = read("../in.extxyz")
init.calc = calc
MaxwellBoltzmannDistribution(init, temperature_K=314)
dyn = NoseHooverChainNVT(
    init,
    timestep=fs * 0.5,
    temperature_K=314,
    tdamp=fs * 0.5 * 100,
)


def write_trajectory(atoms=init):
    write("md.extxyz", atoms, append=True)


dyn.attach(write_trajectory, interval=200)
dyn.attach(MDLogger(dyn, init, "md.log"), interval=200)
dyn.run(steps=2000000)
