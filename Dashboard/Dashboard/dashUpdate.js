

// Need to replace with RPI ethernet static IP
// Right now this is set to RPI IP when on Rice Visitor Network
// Seems to be UNNEEDED now as Sensor Data is transmitting from Matlab
// const RASPBERRY_PI_IP = '168.5.140.178';


document.addEventListener('DOMContentLoaded', (event) => {
    const dataGraphs = document.getElementById('dataGraphs');
    const { div, chart } = getNewDataGraphs(); // Fetch new graphs at startup
    dataGraphs.appendChild(div); // Append new graphs
    
    yaw = 0;
    roll = 0;
    pitch = 0;

    // Get sensor data and update the graph at regular intervals
    setInterval(() => {
        var socket = io.connect('http://localhost:5000');

        socket.on('connect', function() {
            console.log('WebSocket connected!');
        });
        
        // Listen for 'sensor_data' events from the server
        socket.on('sensor_data', function(data) {
            console.log('Received sensor data:', data);
        
            // Update the dashboard with the received data
            document.getElementById('yawData').textContent = data.yaw.toFixed(2);
            document.getElementById('rollData').textContent = data.roll.toFixed(2);
            document.getElementById('pitchData').textContent = data.pitch.toFixed(2);
        
            // Update the graph with the new data
            // updateGraph(chart, data.yaw, data.roll, data.pitch);
        });

        updateGraph(chart, yaw, roll, pitch)
    }, 1000); // Fetch the Euler angles every 1 second

});

function getNewDataGraphs() {
    const div = document.createElement('div');
    const canvas = document.createElement('canvas');
    canvas.id = "myChart";
    div.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    //
    // LATER TODO: Replace Depth and Temperature with actual sensor data/other sensor data needed
    //
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
        }, {
            label: 'Yaw',
            data: [], // Initial data points for Temperature
            // Purple
            borderColor: 'rgba(128, 0, 128, 1)',
            borderWidth: 1,
            fill: false
        }, {
            label: 'Roll',
            data: [], // Initial data points for Temperature
            // Green
            borderColor: 'rgba(0, 128, 0, 1)',
            borderWidth: 1,
            fill: false
        }, {
            label: 'Pitch',
            data: [], // Initial data points for Temperature
            // Orange
            borderColor: 'rgba(255, 165, 0, 1)',
            borderWidth: 1,
            fill: false
        }
    
        ]
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
    
    return {div, chart}; 
}

function updateGraph(chart, yaw, roll, pitch) {
    try {
        // Uncomment to simulate new sensor data
        // const newDepth = Math.random() * 100; // Replace with actual depth sensor data
        // const newTemp = Math.random() * 30; // Replace with actual temperature sensor data
        const newTime = chart.data.labels.length + 1; // Simulating time in seconds

        // Update the graph with new data points
        chart.data.labels.push(newTime);
        // chart.data.datasets[0].data.push(newDepth);
        // chart.data.datasets[1].data.push(newTemp);
        chart.data.datasets[2].data.push(yaw);
        chart.data.datasets[3].data.push(roll);
        chart.data.datasets[4].data.push(pitch);
        chart.update();
    } catch (error) {
        console.error('Error updating graph:', error);
    }
}
