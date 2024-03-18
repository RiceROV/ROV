document.addEventListener('DOMContentLoaded', (event) => {
    const dataGraphs = document.getElementById('dataGraphs');
    const { div, chart } = getNewDataGraphs(); // Fetch new graphs at startup
    dataGraphs.appendChild(div); // Append new graphs
    liveChart = chart;
    yaw = 0;
    roll = 0;
    pitch = 0;

    // Uncomment for Socket Connect
    var socket = io.connect('http://localhost:30001');

    socket.on('connect', function() {
        console.log('WebSocket connected!');
    });
    
    // Listen for 'sensor_data' events from the server
    socket.on('sensor_data', function(data) {
        console.log('Received sensor data:', data);
    
        // Update the dashboard with the received data
        document.getElementById('yawData').textContent = data.yaw.toFixed(8);
        document.getElementById('rollData').textContent = data.roll.toFixed(8);
        document.getElementById('rollControl').textContent = data.rollControl.toFixed(8);
        document.getElementById('pitchControl').textContent = data.pitchControl.toFixed(8);
        document.getElementById('pitchData').textContent = data.pitch.toFixed(8);
        document.getElementById('depth').textContent = data.depth.toFixed(8);
        document.getElementById('depthSet').textContent = data.depthSet.toFixed(8);
        document.getElementById('depthControl').textContent = data.depthControl.toFixed(8);
        document.getElementById('cpu').textContent = data.cpu.toFixed(8);
        document.getElementById('water').textContent = data.water.toFixed(8);
        document.getElementById('thruster1').textContent = data.thruster1.toFixed(8);
        document.getElementById('thruster2').textContent = data.thruster2.toFixed(8);
        document.getElementById('thruster3').textContent = data.thruster3.toFixed(8);
        document.getElementById('thruster4').textContent = data.thruster4.toFixed(8);
        document.getElementById('thruster5').textContent = data.thruster5.toFixed(8);
        document.getElementById('thruster6').textContent = data.thruster6.toFixed(8);
        document.getElementById('bcd1').textContent = data.bcd1.toFixed(8);
        document.getElementById('bcd2').textContent = data.bcd2.toFixed(8);
        document.getElementById('bcd3').textContent = data.bcd3.toFixed(8);
        document.getElementById('bcd4').textContent = data.bcd4.toFixed(8);
        document.getElementById('bcd1Volt').textContent = data.bcd1Volt.toFixed(8);
        document.getElementById('bcd2Volt').textContent = data.bcd2Volt.toFixed(8);
        document.getElementById('bcd3Volt').textContent = data.bcd3Volt.toFixed(8);
        document.getElementById('bcd4Volt').textContent = data.bcd4Volt.toFixed(8);

        // Update the graph with the new data
        // updateGraph(chart, data.yaw, data.roll, data.pitch);
    });

    // Set interval to update every second (1000 milliseconds)
    
    // Uncomment for BCD Thruster stuff - BROKEN  RIGHT NOW
    // setInterval(updateAllDevices, 1000);

    // Update interval to be set correctly
    // setInterval(function() {
    //     updateGraph(liveChart, 0, 100, 0); // Pass the chart object and other necessary values here
    // }, 1000);
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
        const newDepth = Math.random() * 100; // Replace with actual depth sensor data
        const newTemp = Math.random() * 30; // Replace with actual temperature sensor data
        const newTime = chart.data.labels.length + 1; // Simulating time in seconds

        // Update the graph with new data points
        chart.data.labels.push(newTime);
        chart.data.datasets[0].data.push(newDepth);
        chart.data.datasets[1].data.push(newTemp);
        chart.data.datasets[2].data.push(yaw);
        chart.data.datasets[3].data.push(roll);
        chart.data.datasets[4].data.push(pitch);
        chart.update();
    } catch (error) {
        console.error('Error updating graph:', error);
    }
}


// Uncomment FOR BCD / THRUSTER

// function updateOutput(deviceId, output) {
//     const outputBar = document.getElementById(`output-${deviceId}`);
//     if (output >= 0) {
//         outputBar.style.backgroundColor = "green";
//         outputBar.style.height = `${Math.abs(output) / 100 * 50}px`; // Adjust based on your range
//         outputBar.style.bottom = "50%";
//     } else {
//         outputBar.style.backgroundColor = "red";
//         outputBar.style.height = `${Math.abs(output) / 100 * 50}px`;
//         outputBar.style.top = "50%";
//     }
// }

// function updateVoltage(deviceId, voltage) {
//     const voltageDisplay = document.getElementById(`voltage-${deviceId}`);
//     voltageDisplay.innerText = `${voltage}V`;
// }

// function generateRandomBCDOutput() {
//     // Generates -1, 0, or 1 for BCDs
//     return Math.floor(Math.random() * 3) - 1;
// }

// function generateRandomThrusterOutput() {
//     // Generates a random number between -32000 and 32000 for thrusters
//     return Math.floor(Math.random() * (32000 - (-32000) + 1)) + (-32000);
// }

// function generateRandomVoltage() {
//     // Generates a random voltage between 0V and 24V
//     return Math.floor(Math.random() * 25); // 0 to 24
// }

// function updateAllDevices() {
//     // Update BCDs
//     for (let i = 1; i <= 4; i++) { // Assuming 4 BCDs
//         const bcdOutput = generateRandomBCDOutput();
//         updateOutput(`bcd${i}`, bcdOutput);
//         updateVoltage(`bcd${i}`, generateRandomVoltage());
//     }

//     // Update Thrusters
//     for (let i = 1; i <= 6; i++) { // Assuming 6 Thrusters
//         const thrusterOutput = generateRandomThrusterOutput();
//         updateOutput(`thruster${i}`, thrusterOutput);
//         updateVoltage(`thruster${i}`, generateRandomVoltage());
//     }
// }


