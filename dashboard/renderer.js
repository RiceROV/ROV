
const RASPBERRY_PI_IP = '168.5.140.178';

// Initialize Graphs Logic
document.addEventListener('DOMContentLoaded', (event) => {
    const dataGraphs = document.getElementById('dataGraphs');
    const { div, chart } = getNewDataGraphs(); // Fetch new graphs
    dataGraphs.appendChild(div); // Append new graphs
    
    // Simulate sensor data and update the graph at regular intervals
    setInterval(() => {
        fetch('http://168.5.140.178:5000/sensor_data')
        .then(response => response.json())
        .then(data => {
            let sensorTemp = data.temp;
            let accelX = data.acceleration_x;
            let accelY = data.acceleration_y;
            let accelZ = data.acceleration_z;
            let gyroX = data.gyro_x;
            let gyroY = data.gyro_y;
            let gyroZ = data.gyro_z;

            document.getElementById('sensorTemp').querySelector('.status-black').textContent = data.temp + "°C";
            document.getElementById('accelData').querySelectorAll('.status-black')[0].textContent = data.acceleration_x;
            document.getElementById('accelData').querySelectorAll('.status-black')[1].textContent = data.acceleration_y;
            document.getElementById('accelData').querySelectorAll('.status-black')[2].textContent = data.acceleration_z;
            document.getElementById('gyroData').querySelectorAll('.status-black')[0].textContent = data.gyro_x;
            document.getElementById('gyroData').querySelectorAll('.status-black')[1].textContent = data.gyro_y;
            document.getElementById('gyroData').querySelectorAll('.status-black')[2].textContent = data.gyro_z;

            updateGraph(chart, sensorTemp, accelZ);  // Using acceleration Z as a placeholder for depth
        })
        .catch(error => console.error('Error fetching sensor data:', error));
    }, 1000); // Update every 1 second. Adjust as needed.

    // Initialize Status Updates
    setInterval(() => {
        updateStatus();
    }, 1000); // The interval time should be adjusted according to your needs.
});

function getNewDataGraphs() {
    const div = document.createElement('div');
    const canvas = document.createElement('canvas');
    canvas.id = "myChart";
    div.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Initial data setup
    const data = {
        labels: [], // Initial labels (times will be pushed here)
        datasets: [{
            label: 'Depth (m)',
            data: [], // Initial data points for Depth
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            fill: false
        }, {
            label: 'Temperature (°C)',
            data: [], // Initial data points for Temperature
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false
        }]
    };
    
    // Create Chart
    const chart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false, // Added to make the graph fill the container
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });
    
    return {div, chart}; // Return both the div and the chart
}

function updateGraph(chart, newTemp, newDepth) {
    try {
        // Simulate new sensor data
        // const newDepth = Math.random() * 100; // Replace with actual depth sensor data
        // const newTemp = Math.random() * 30; // Replace with actual temperature sensor data
        const newTime = chart.data.labels.length + 1; // Simulating time in seconds

        // Update the graph with new data points
        chart.data.labels.push(newTime);
        chart.data.datasets[0].data.push(newDepth);
        chart.data.datasets[1].data.push(newTemp);
        chart.update();
    } catch (error) {
        console.error('Error updating graph:', error);
    }
}

function updateStatus() {
    try {
        // Replace this with actual logic to fetch and update status.
        document.getElementById('rovStatus').textContent = `ROV Status: ${getROVStatus()}`;
        document.getElementById('batteryLevel').textContent = `Battery Level: ${getBatteryLevel()}%`;
        document.getElementById('depthGauge').textContent = `Depth: ${getDepth()}m`;
        document.getElementById('gpsData').textContent = `GPS Data: Lat ${getLatitude()}, Lon ${getLongitude()}`;
        document.getElementById('waterQuality').textContent = `Water Quality: ${getWaterQuality()}`;
        document.getElementById('waterTemp').textContent = `Water Temperature: ${getWaterTemperature()}°C`;
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// ... (existing placeholder functions)

// Fetch sensor data from Raspberry Pi and update the dashboard
// setInterval(() => {
    
// }, 1000);
