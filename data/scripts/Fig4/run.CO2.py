# %%
from pathlib import Path
from ase.io import read, write
from ase.md import MDLogger
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.langevin import Langevin
from ase.md.nose_hoover_chain import NoseHooverChainNVT
from ase.units import fs

from sevenn.calculator import SevenNetCalculator

if __name__ == "__main__":
    Tc = 304.13

    folder = Path("./").absolute()
    Tr = folder.name[2:]
    Rr = folder.parent.name[2:]
    print(f"{Tr=}, {Rr=}")
    ininitial = folder.parent.parent.parent.parent.parent / "init" / f"T{Tr}_R{Rr}.extxyz"
    assert ininitial.is_file(), f"{ininitial} is absent"
    init = read(ininitial)
    temperature = Tc * float(Tr)
    calc = SevenNetCalculator(
        model="../../../checkpoint.pth",
        device="cuda",
        enable_cueq=False,
        enable_flash=True,
    )
    init.calc = calc
    MaxwellBoltzmannDistribution(init, temperature_K=temperature)
    dyn = Langevin(init, timestep=fs * 0.5, temperature_K=temperature, friction=1 / (100 * fs), fixcm=False)
    # dyn = NoseHooverChainNVT(init, timestep=fs * 0.5, temperature_K=temperature, tdamp=100 * fs)

    def write_trajectory(atoms=init):
        write("md.extxyz", atoms, append=True)

    dyn.attach(write_trajectory, interval=20)
    dyn.attach(MDLogger(dyn, init, "md.log"), interval=20)
    dyn.run(steps=200000)
