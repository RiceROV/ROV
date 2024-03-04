# BayMax Pro - ROV Dashboard

## Overview

BayMax Pro - ROV Dashboard is a web-based dashboard designed to monitor and display real-time data from an ROV (Remotely Operated Vehicle). It showcases core system information, sensor data, and environmental data, along with a 3D simulation of the ROV in its operational environment. The dashboard utilizes technologies such as HTML, CSS, JavaScript, and libraries like Three.js and Chart.js to render 3D graphics and charts.

## Prerequisites

Before running the BayMax Pro - ROV Dashboard, ensure you have the following prerequisites installed on your system:

- Git: For cloning the repository.
- npm (Node Package Manager): To install dependencies.
- Vite: A build tool for modern web projects.

## Installation

1. **Clone the Repository**

   Use Git to clone the repository to your local machine:

   ```bash
   git clone https://github.com/RiceROV/ROV.git
   ```

2. **Navigate Project Directory**
   ```bash
   cd Dashboard/Dashboard
   ```
3. **Install Dependencies**
   ```bash
   npm install
   ```
4. **In another Terminal: Run Flask Handler**
   ```bash
   cd ../Flask
   python handler.py
   ```
   This Python Handler takes in sensor Data coming from the Pi and utilizes Web Sockets for high frequency data retrieval for the Dashboard.
5. **Run Dashboard**
   ```bash
   npm run dev
   ```
   This command will start a local development server using Vite. The terminal output will provide a clickable localhost:port to load in your browser. That is the Dashboard.

## Usage

Once the dashboard is running, you should see the BayMax Pro - ROV Dashboard interface. It consists of several sections displaying different types of data:

- **Core System Information**: Shows basic information about the ROV's status, battery level, and depth.
- **Sensor Data**: Displays data from various sensors, including temperature, accelerometer, gyroscope, and others.
- **Simulation**: A 3D simulation of the ROV in its environment, rendered using Three.js.
- **Data Graphs**: Real-time charts displaying sensor data over time, powered by Chart.js.

Interact with the dashboard as needed to monitor and analyze the ROV's performance and environmental conditions.

## Troubleshooting

- Ensure all prerequisites are correctly installed and up-to-date.
- Check the browser's console for any errors that might indicate issues with loading scripts or external libraries.
- Ensure the local server is running and accessible in your web browser.

## Reporting Issues

If you encounter any issues or have suggestions for improvements, please feel free to [open an issue](<repository-issues-url>) on the GitHub repository. Your feedback is valuable in helping make the dashboard better for everyone.

