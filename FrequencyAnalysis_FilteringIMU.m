%%Script for FFT on IMU data and testing of different digital filters
%ONCE correct filtering technique and FFT is completed in here, can be
%implemented in python GUI

%remember index starts at 1 in this dumb language
sample_Data = xlsread('justForThesisFFTPlot.xlsx');

sample_Number = sample_Data(:, 1);
y_Acceleration = sample_Data(:, 2); %this is the axis in the direction of motion

%%FFT part 
Fs = 100;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = 3000;             % Length of signal
t = (0:L-1)*T;        % Time vector

figure(1)
plot(sample_Number, y_Acceleration); %time series data

%COMPUTE FFT

Y = fft(y_Acceleration);

P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L; %frequency domain signal
figure(2)
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')

%GAY FILTER SECTION
order = 2;
Rs = 40; %stop band attenuation, only used in cheby filter not in butterworth
Ws = 3.5/50; %cutoff freq (everything past is faggy stopband)/sample rat nyquist bullshit

%[b, a] = cheby2(order, Rs, Ws); %cheby2 filter cuz look at the pics it makes sense 
[b, a] = butter(order, Ws);

dataOut = filter(b, a, y_Acceleration); %apply filter characteristics 

figure(3)
plot(sample_Number, y_Acceleration); %raw data
hold on
plot(sample_Number, dataOut); %filtered data overlayed

figure(4)
plot(sample_Number, dataOut);

x_axis_column_vector = f';
%y_axis_column_vector = P1'; %nvm P1 is already column vector






