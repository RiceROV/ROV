#include <iostream>
#include <chrono>
#include <thread>

#include "sim_depth.cc"
#include "sim_angle.cc"
#include "pid_controller.cc"

#define DEPTH_SETPOINT -2
#define ANGLE_SETPOINT 0

#define DEPTH_P 1.0
#define DEPTH_I 0.5
#define DEPTH_D 0.01

#define ANGLE_X_P 1.0
#define ANGLE_X_I 0.0 
#define ANGLE_X_D 2.0

#define ANGLE_Y_P 1.0
#define ANGLE_Y_I 0.0
#define ANGLE_Y_D 2.0

void clearConsole() {
    std::system("clear");
}

int main() {
    PIDController pidDepth(DEPTH_P, DEPTH_I, DEPTH_D);
    PIDController pidAngleX(ANGLE_X_P, ANGLE_X_I, ANGLE_X_D);
    PIDController pidAngleY(ANGLE_Y_P, ANGLE_Y_I, ANGLE_Y_D);

    DepthCalculator posCalc;
    AngleCalculator angleCalcX;
    AngleCalculator angleCalcY;

    double current_depth = posCalc.updateDepth(0);  // Get current depth without any control
    double current_angle_x = angleCalcX.updateAngle(0);  // Get current angle without any control
    double current_angle_y = angleCalcY.updateAngle(0);  // Get current angle without any control

    for (int i = 0; i < 1000; i++) {  // Simulate for 1000 iterations
        double control_output = pidDepth.compute(DEPTH_SETPOINT, current_depth);  // Get control output from PID
        current_depth = posCalc.updateDepth(control_output);  // Update depth based on control


        double control_output_x = pidAngleX.compute(ANGLE_SETPOINT, current_angle_x);  // Get control output from PID
        double control_output_y = pidAngleY.compute(ANGLE_SETPOINT, current_angle_y);  // Get control output from PID
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

