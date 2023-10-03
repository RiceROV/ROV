# Rice ROV: Buoyancy-Controlled Underwater ROV 🌊🤖

Welcome to the Rice ROV senior design project repository. This project involves the collective effort of students from the departments of electrical & computer engineering and mechanical engineering.

## 🛠 Getting Started with Baymax Pro Dashboard

To set up the Baymax Pro Dashboard and integrate with the Raspberry Pi sensor data, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone -b dashboard https://github.com/RiceROV/ROV
    ```

2. **Navigate to the Dashboard Directory**:

    ```bash
    cd dashboard
    ```

3. **Initialize and install necessary packages**:

    ```bash
    npm init -y
    npm install electron --save
    ```

4. **SSH into your Raspberry Pi 4** through the IP over Rice Visitor.

5. **Once inside the Raspberry Pi, navigate to the sensor directory**:

    ```bash
    cd ROV/sensor
    ```

6. **Start the Flask Server on the Pi** to begin transmitting data:

    ```bash
    python3 server.py
    ```

7. **Finally, initiate the Baymax Pro Dashboard on your main machine**:

    ```bash
    npm start
    ```
    
## 🚀 Repository Purpose

This repository is dedicated to housing both the control code for the ROV and its machine learning applications.

## 🎯 Objectives

- **Buoyancy Control Device (BCD)**: Design, build, and test a new buoyancy control mechanism that utilizes a reversible fuel cell.
  
- **ROV Design**: Develop a compact, low-cost ROV capable of retrieving items of an undetermined weight and size at shallow depths.

## 🌐 Background

ROVs and AUVs play a crucial role in a myriad of subsurface operations across science, exploration, and industry domains. Traditional underwater vehicles maintain depth using high-energy-consuming actuators like thrusters. BCDs, on the other hand, offer a more energy-efficient alternative.

🔍 Our mission is to enhance the BCD designs originating from the University of Houston, emphasizing practicality and low cost.

## 📌 Milestones

1. **Buoyancy Control Device**: Construct a reversible fuel cell-powered BCD, enhancing upon existing University of Houston designs.

2. **ROV Construction**: Build a low-cost, compact ROV that can handle unpredictable undersea retrieval tasks.
