#include <iostream>

class PIDController {
private:
    double Kp, Ki, Kd; // Gains
    double prev_error; // Store the previous error
    double integral;   // Accumulated error

public:
    PIDController(double Kp, double Ki, double Kd)
        : Kp(Kp), Ki(Ki), Kd(Kd), prev_error(0), integral(0) {}

    double compute(double setpoint, double pv) {
        double error = setpoint - pv;
        integral += error; // Accumulate the error
        double derivative = error - prev_error; // Calculate rate of error

        double output = Kp*error + Ki*integral + Kd*derivative;

        prev_error = error; // Update previous error
        return output; // This is the control output
    }
};

int main() {
    PIDController pid(1.0, 0.5, 0.01); // Example gains
    double setpoint = 100; // Desired position/depth/orientation
    double current_position = 90; // Measured position/depth/orientation

    double control_output = pid.compute(setpoint, current_position);

    // For demonstration purposes, simply print out the control output
    std::cout << "Control Output: " << control_output << std::endl;

    // In a real-world scenario, you would use the control_output to adjust your propellers or other actuators.
    return 0;
}
