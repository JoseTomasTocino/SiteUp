captureFreq = 1024;

t = 0:1/captureFreq:1;
numSamples = length(t);

disp(numSamples);

###################################
# PRIMER SENO

Amplitud1 = 5;
Frecuencia1 = 10;

x1 = Amplitud1 * sin(2 * pi * Frecuencia1 * t);
fd = fopen("seno1.mat", "wt");
fprintf(fd, "%14.6f\n", x1);
fclose(fd);

###################################
# SEGUNDO SENO

Amplitud2 = 2.5;
Frecuencia2 = 30;

x2 = Amplitud2 * sin(2 * pi * Frecuencia2 * t);
fd = fopen("seno2.mat", "wt");
fprintf(fd, "%14.6f\n", x2);
fclose(fd);

###################################
# SUMA DE SENOS

x = x1 + x2;
fd = fopen("seno3.mat", "wt");
fprintf(fd, "%14.6f\n", x);
fclose(fd);

###################################
# ESPECTRO

# Hacemos la transformada de Fourier
Y = fft(x, numSamples);

# Módulo
Y = abs(Y(1:(1+numSamples/2)));

# Normalización
Y = 2 * Y / numSamples;

# Cálculo de las abcisas (frecuencia)
f = captureFreq / numSamples * (0:numSamples/2);

fd = fopen("espectro.mat", "wt");
for x = (1:numSamples/2 + 1)
  fprintf(fd, "%14.6f %14.6f\n", f(x), Y(x));
endfor
fclose(fd);
