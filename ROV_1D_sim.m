% Plot rise of ROV in 1D using only BCDs
% after picking up a small object
% Assumptions made by this model:
% - ROV only travels in 1D
% - No inertia
% - No thrust
% - O2 and H2 are ideal gasses
% This model does incorporate
% - Pressure change with ROV depth
% - EOM to account for change in buoyancy force
% Andrew Bare 9/17/23
close all;clc;

% constants
rho_H2_STP = 0.08988; % Density H2 at STP g/L
rho_O2_STP = 1.429; % Density O2 at STP g/L

r_H2 = 42.684; % [Input] Rate of H2 production cc/min @ STP
r_O2 = r_H2/2; % Rate of O2 production cc/min @ STP
mdot_H2 = r_H2*rho_H2_STP/(1000*1000*60); % Rate of H2 production kg/s
mdot_O2 = r_O2*rho_O2_STP/(1000*1000*60); % Rate of O2 production kg/s

d = 23

tspan = [0 10];
q0 = [0 0 0]'; % State vector, start 1m deep, zero velocity, small BCD vol
[t,q] = ode45(@(t,y) BCD_ROV(t,y,[mdot_H2; mdot_O2],d), tspan, q0);

hold on
plot(t,q(:,1));
ylabel("Z position (m)")
yyaxis("right");
plot(t,q(:,2));
title("ROV Position & Velocity")
ylabel("Z velocity (m/s)")
xlabel("Time (s)")
hold off; figure;

plot(t,q(:,3)*1e6);
ylabel("BCD Volume (cm^3)")
xlabel("Time (s)");
title("BCD Volume")

zPosition = q(:,1);
zVelocity = q(:,2);
BCDVol = q(:,3);

T = table(zPosition,zVelocity,BCDVol);
disp(T)

function dqdt = BCD_ROV(t,q,mdot,d)
    g = 9.81; % m/s^2 acceleration due to gravity
    rho = 997; % kg/m^3 density of water
    R = 8.314; % J/K*mol Universal gas constant
    T = 300; % Water temperature K
    P_standard = 101324; % Standard pressure Pa

    M_H2 = 1.008/1000; % Molar mass of H2 kg/mol
    M_O2 = 15.999/1000; % Molar mass of O2 kg/mol
    
    P = P_standard + q(1)*rho*g; % Pressure at depth

    % (kg/s)*(J/K*mol)*K/(Pa*g/mol)

    dV_H2 = mdot(1)*R*T/(M_H2*P); % Change in volume of hydrogen m^3/s
    dV_O2 = mdot(2)*R*T/(M_O2*P); % Change in volume of oxygen m^3/s

    B_BCD = rho*g*q(3); % Buoyancy added by BCDs kg*m/s^2

    %W = 0.1*g; % Weight of small object picked up at t=0
    W = 0;

    m = 10; % Total mass of ROV + BCDs kg

    dqdt = zeros(3,1);
    % 2nd order EOM
    dqdt(1) = q(2); % velocity m/s
    dqdt(2) = (-d.*q(2)+B_BCD-W)./m; % acceleration m/s^2
    dqdt(3) = dV_O2+dV_H2; % BCD volume change m^3/s
end
