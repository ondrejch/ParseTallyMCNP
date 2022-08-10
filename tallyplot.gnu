# Example script for gnuplot

set log x
set log y
unset bars
set grid
set format "10^{%L}"
set xlabel  "energy [MeV]"
set ylabel  "neutron flux per unit lethargy [n/(dξ cm^2 s)]"

set term pngcairo enh font "Ariel,24" size 1920, 1200
set out 'B4_10spectrum.png'
plot [1e-9:10][1e-8:]"mytally_604.dat" u 1:5:($3*$5)  w yerr lw 3 ps .7 pt 7  tit "BP4, More tallies, tally 604", "" u 1:5 w l lc "blue" notit
set out

set out 'B4_11spectrum.png'
plot [1e-9:10][1e-9:]"mytally_614.dat" u 1:5:($3*$5)  w yerr lw 3 ps .7 pt 7  tit "BP4, More tallies, tally 614", "" u 1:5 w l lc "blue" notit
set out

set out 'B4_12spectrum.png'
plot [1e-9:10][1e-11:]"mytally_624.dat" u 1:5:($3*$5)  w yerr lw 3 ps .7 pt 7  tit "BP4, More tallies, tally 624", "" u 1:5 w l lc "blue" notit
set out

