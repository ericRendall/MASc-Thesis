%%testing out PID controller 

%create num and denom of transfer function
%laplace transform of system output signal divided by LT of input signal
numerator = [1]; %LAPLACE OF SYSTEM OUTPUT
denominator = [1 3 1]; %LAPLACE OF SYSTEM INPUT - tune this to experiment with different input systems (represents some random physical system)

%set up plant 
Gp = tf(numerator, denominator)
H = [1]; %feedback transfer function (simple for now)

M_no_Controller = feedback(Gp, H) %basically does G/1+GH
%Gp is forward transfer function and H is feedback transfer function
%M is like closed loop transfer function

%now input a step response to see how system responds 
%step input is basically a instant rise of 0 to 1 in input signal to see
%how system behaves to rapid changes

%figure(1)
%step(M_no_Controller)
%grid on

%% now add in controller
%set PID gain variables
%PLOTS ARE SUPPOSED TO GO TO 1 CAUSE STEP INPUT IS 1 but don't go to 1
%wihtout control cause steady state error is present

Kp = 24; %FIRST: reduces rise time to SS at expense of higher overshoot, also makes SS closer to Step input value of 1
Ki = 1; %THIRD: integrates out remaining steady state error to hit desired step input value of 1
Kd = 8; %SECOND: dampens oscillations and overshoot due to high P gain

Gc = pid(Kp, Ki, Kd) %this is PID controller

M_controller = feedback(Gc*Gp, H)
%so now controller in forward path but since initially p = 1, i = 0, d = 0,
%plot output should be exact same as w no controller since gain is just 1 

figure(1)
step(M_controller)
grid on
hold on




