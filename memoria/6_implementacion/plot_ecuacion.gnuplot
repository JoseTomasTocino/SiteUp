set xrange [0:1]
set yrange [0:1]
set size square
set nokey
set xlabel "tiempo"
set ylabel "posición"
set terminal pdf
set output "imagen_ecuacion1.pdf"
plot x*x*x
