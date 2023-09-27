#include <chrono>

class AngleCalculator {
private:
    double current_angle;
    double previous_angle_change_rate;  // Store the previous angle change rate (velocity)
    double drag_factor;  // Factor to simulate drag effects
    std::chrono::steady_clock::time_point last_update_time;

public:
    AngleCalculator(double initial_angle = 45.0, double drag = 0.1)
        : current_angle(initial_angle), previous_angle_change_rate(0.0), drag_factor(drag), last_update_time(std::chrono::steady_clock::now()) {}

    double updateAngle(double control_output) {
        auto current_time = std::chrono::steady_clock::now();
        double time_diff = std::chrono::duration<double>(current_time - last_update_time).count();  // Time difference in seconds
        
        // Model: control output affects angle change rate, with drag acting against it
        double angle_change_rate = control_output - drag_factor * previous_angle_change_rate;

        // Update current angle based on the calculated rate
        current_angle += angle_change_rate * time_diff;

        // Store the angle change rate for the next iteration
        previous_angle_change_rate = angle_change_rate;

        // Update the last update time
        last_update_time = current_time;

        return current_angle;
    }
};
