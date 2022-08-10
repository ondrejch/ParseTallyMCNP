
#!/bin/bash
#
# MCNP fmesh tally parser and plotter. This is for a cylindrical tally along the X coordinate, not supposed to be a general parser can be adapted.
#
# Ondrej Chvala, ondrejch@gmail.com
# MIT license

TALLYFILE=meshtally.out     # name out the FMESH tally file
GNUPLOTFILE=plotme.gnu      # name of the gnuplot script
XOFFSET=80                  # X-offset of the tally

#tmpdir=$(mktemp -d)
tmpdir=tmp
# keys=$(sed -e '1,/Energy         R         Z         Th    Result     Rel Error/d' meshtally.out | awk '{print $1}' | uniq)

cat << EOF1 > $GNUPLOTFILE
set log x
set log y
unset bars
set grid
set format "10^{%L}"
set xlabel  "energy [MeV]"
set ylabel  "neutron flux [n/(cm^2 s)]"
#set term pngcairo enh font "Ariel,24" size 1920, 1200
set term pdf enh
#font "Ariel,24" size 1920, 1200
set out "plots.pdf"
EOF1


# Midpoints of the bins along X
xbins=$(awk '{if ($1=="Total") print $3}' $TALLYFILE)

for x in $xbins; do
    tfile=$tmpdir/${x}.dat
    binx=$(echo $x - $XOFFSET |bc)
    echo "Procesing $x at $binx"
    awk "{if (\$3==${x} && \$1!=\"Total\") print \$3\" \"\$1\" \"\$5\" \"\$6}" $TALLYFILE > $tfile
#    echo "set out \"B1_flux_at_$binx.png\"" >> $GNUPLOTFILE
    echo "plot [1e-9:10][1e-9:1e-5] \"$tfile\" u 2:3:(\$3*\$4) w yerr lw 1 ps .2 pt 7  tit \"BP1, Charlton, x=$binx cm\", \"\" u 2:3 w l lc \"blue\" notit" >> $GNUPLOTFILE
#    echo "set out" >> $GNUPLOTFILE
done


# E-integrated flux
tfile=$tmpdir/total.dat
awk '{if ($1=="Total") print $3" "$5" "$6}' $TALLYFILE > $tfile

#echo "set out \"B1_integratedflux.png\""  >> $GNUPLOTFILE
echo "set xlabel \"x [cm]\"" >> $GNUPLOTFILE
echo "unset log x; unset format x" >> $GNUPLOTFILE
echo "plot \"$tfile\" u (\$1-$XOFFSET):2:(\$2*\$3) w yerr lw 1 ps .2 pt 7  tit \"BP1, Charlton, energy integrated flux along X\", \"\" u (\$1-$XOFFSET):2 w l lc \"blue\" notit" >> $GNUPLOTFILE
#echo "set out" >> $GNUPLOTFILE
gnuplot $GNUPLOTFILE
