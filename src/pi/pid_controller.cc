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
        // std::cout << "Error " << error << " integral " << integral << " derivative " << derivative << " setpoint " << setpoint << " pv " << pv
        //  << std::endl;
        return output; // This is the control output
    }
};