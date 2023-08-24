# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:10:54 2023

@author: D45geFEE
"""
from lammps import PyLammps
import numpy as np

#%%

# Crear objeto PyLammps
lammps = PyLammps()

# Establecer parámetros de simulación
lammps.units("real")
lammps.dimension(3)
lammps.boundary("p", "p", "p")
lammps.atom_style("full")



#Definir modelo para caluclo de propiedades class 2 (COMPASS)
lammps.pair_style("lj/charmm/coul/long", 6, 12)
lammps.pair_modify('mix arithmetic')
lammps.bond_style("harmonic")
lammps.angle_style("charmm")
lammps.dihedral_style("charmm")
lammps.improper_style("harmonic")
lammps.kspace_style("ewald/disp", 1e-6)

#Tomar datos de la celda
lammps.read_data("cell.data")

lammps.neighbor("2.0" ,"bin")
lammps.neigh_modify("every","20","delay", "0", "check", "yes")
lammps.minimize("1.0e-3", "1.0e-5", "1000", "10000")

lammps.run(1000)



lammps.timestep(0.5)
lammps.thermo(200)

# ----------------- Run Section -----------------
#equilibration
#lammps.run(0)
lammps.velocity('all','create', '300', '38564')
lammps.fix('1','all', 'nvt', 'temp', 300, 300, 100.0)
lammps.run(2000)
lammps.reset_timestep(0)

#calculate dipole moment vector
#WARNING: This definition of the dipole moment is ONLY valid when the system has 0 net charge, so you should verify that before use.
lammps.compute('1', 'all', 'property/atom', 'q', 'xu', 'yu', 'zu')
lammps.variable('dipolex', 'atom', 'c_1[1]*c_1[2]')
lammps.variable('dipoley', 'atom','c_1[1]*c_1[3]')
lammps.variable('dipolez', 'atom', 'c_1[1]*c_1[4]')
lammps.compute('2', 'all', 'reduce', 'sum', 'v_dipolex')
lammps.compute('3', 'all','reduce', 'sum', 'v_dipoley')
lammps.compute('4', 'all', 'reduce', 'sum', 'v_dipolez')
lammps.variable('totaldipolex', 'equal','c_2')
lammps.variable('totaldipoley', 'equal', 'c_3')
lammps.variable('totaldipolez', 'equal','c_4')
lammps.variable('mytime', 'equal', 'step*dt')
lammps.fix('printdipole','all','ave/time','1', '1', '2', 'v_mytime', 'v_totaldipolex','v_totaldipoley', 'v_totaldipolez', 'file dipole.txt', 'mode', 'scalar', 'format', '%.10f')
#Note that printing every 1 fs, as I do here, gets you wavenumbers up to the Nyquist frequency, 0.5/1 fs^-1 = 16,678 cm^-1.
#Printing every 2 fs only gets you wavenumbers up to 0.5/2 fs^-1 = 8,339 cm^-1, and so on.
#This indicates that you only need to print every 5 ns to have the IR spectra up to 3340 cm^-1, but this is incorrect. 
#Per the Nyquist-Shannon sampling theorem, you need to sample the system at a frequency greater than or equal to 2*f, where f is the highest frequency contained in the system.
#Otherwise, aliasing errors occur, and the FFT will show the higher frequency signals at a lower frequency than they are.
#Thus, if the highest-frequency bond in your system has a characteristic period of 20 fs, you need to print out at least every 10 fs.
#If you want to get around this, you'll need to apply a lowpass filter (aka an anti-aliasing filter) to get rid of the high frequency signals before you do the FFT. This is not implemented in this code.
#It makes more sense to print out frequently enough rather than to apply a filter; if you're doing MD, your timestep must be high enough to account for the high-frequency signal anyway, so the information is there!
#The only good reason for a filter in this case is if you want to sample a very long trajectory and storing it is computationally prohibitive.

#production
lammps.run(2000000)
#Note that running for 1,000,000 times the printout frequency, as I do here, gets you wavenumbers at 1,000,000 increments between 0 and the maximum wavenumber.
#If you only use the autocorrelation function up to 0.01 times the trajectory length for statistical purposes, then you only get 10,000 increments.
#e.g., you get the intensity calculated at every 16,678/9,999 = 1.668 cm^-1.
#Running for longer increases this precision, and also it betters the statistics of the spectra.