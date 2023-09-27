#include <chrono>

class DepthCalculator {
private:
    double current_depth;
    double previous_depth_change_rate;  // Store the previous depth change rate (velocity)
    double drag_factor;  // Factor to simulate drag effects
    std::chrono::steady_clock::time_point last_update_time;

public:
    DepthCalculator(double initial_depth = 0.0, double drag = 0.1)
        : current_depth(initial_depth), previous_depth_change_rate(0.0), drag_factor(drag), last_update_time(std::chrono::steady_clock::now()) {}

    double updateDepth(double control_output) {
        auto current_time = std::chrono::steady_clock::now();
        double time_diff = std::chrono::duration<double>(current_time - last_update_time).count();  // Time difference in seconds
        
        // Model: control output affects depth change rate, with drag acting against it
        double depth_change_rate = control_output - drag_factor * previous_depth_change_rate;

        // Update current depth based on the calculated rate
        current_depth += depth_change_rate * time_diff;

        // Store the depth change rate for the next iteration
        previous_depth_change_rate = depth_change_rate;

        // Update the last update time
        last_update_time = current_time;

        return current_depth;
    }
};
