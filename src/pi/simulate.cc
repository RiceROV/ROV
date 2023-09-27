#include <iostream>
#include <chrono>
#include <thread>

#include "sim_depth.cc"
#include "sim_angle.cc"
#include "pid_controller.cc"

void clearConsole() {
    std::system("clear");
}

int main() {
    PIDController pidDepth(1.0, 0.5, 0.01);
    PIDController pidAngleX(1, 0, 2);
    PIDController pidAngleY(1, 0, 2);

    DepthCalculator posCalc;
    AngleCalculator angleCalcX;
    AngleCalculator angleCalcY;

    double angle_setpoint = 0;  // Desired angle
    double depth_setpoint = -2;  // Desired depth
    double current_depth = posCalc.updateDepth(0);  // Get current depth without any control
    double current_angle_x = angleCalcX.updateAngle(0);  // Get current angle without any control
    double current_angle_y = angleCalcY.updateAngle(0);  // Get current angle without any control

    for (int i = 0; i < 1000; i++) {  // Simulate for 1000 iterations
        double control_output = pidDepth.compute(depth_setpoint, current_depth);  // Get control output from PID
        current_depth = posCalc.updateDepth(control_output);  // Update depth based on control


        double control_output_x = pidAngleX.compute(angle_setpoint, current_angle_x);  // Get control output from PID
        double control_output_y = pidAngleY.compute(angle_setpoint, current_angle_y);  // Get control output from PID
        current_angle_x = angleCalcX.updateAngle(control_output_x);  // Update angle based on control
        current_angle_y = angleCalcY.updateAngle(control_output_y);  // Update angle based on control

        std::this_thread::sleep_for(std::chrono::milliseconds(10));  // Sleep for 10 milliseconds
        clearConsole();

        std::cout << "Depth correction: " << control_output << std::endl
                  << "X angle correction: " << control_output_x << std::endl
                  << "Y angle correction: " << control_output_y << std::endl
                  << "Current Depth: " << current_depth << " meters" << std::endl
                  << "Current Angle (x): " << current_angle_x << " degrees" << std::endl
                  << "Current Angle (y): " << current_angle_y << " degrees" << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

