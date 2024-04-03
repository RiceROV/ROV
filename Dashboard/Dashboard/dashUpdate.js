document.addEventListener('DOMContentLoaded', (event) => {
    const dataGraphs = document.getElementById('dataGraphs');
    const { div, chart } = getNewDataGraphs(); // Fetch new graphs at startup
    dataGraphs.appendChild(div); // Append new graphs
    liveChart = chart;
    yaw = 0;
    roll = 0;
    pitch = 0;
    let lastUpdateTime = 0;
    first = true;
    // Uncomment for Socket Connect
    var socket = io.connect('http://localhost:30001');

    socket.on('connect', function() {
        console.log('WebSocket connected!');
    });
    
    // Listen for 'sensor_data' events from the server
    socket.on('sensor_data', function(data) {
        console.log('Received sensor data:', data);
    
        // Update the dashboard with the received data
        document.getElementById('yawData').textContent = data.yaw.toFixed(2);
        document.getElementById('rollData').textContent = data.roll.toFixed(2);
        document.getElementById('rollControl').textContent = data.rollControl.toFixed(2);
        document.getElementById('pitchControl').textContent = data.pitchControl.toFixed(2);
        document.getElementById('pitchData').textContent = data.pitch.toFixed(2);
        document.getElementById('depth').textContent = data.depth.toFixed(2);
        document.getElementById('depthSet').textContent = data.depthSet.toFixed(2);
        document.getElementById('depthControl').textContent = data.depthControl.toFixed(2);
        document.getElementById('cpu').textContent = data.cpu.toFixed(2);
        document.getElementById('thruster1').textContent = data.thruster1.toFixed(2);
        document.getElementById('thruster2').textContent = data.thruster2.toFixed(2);
        document.getElementById('thruster3').textContent = data.thruster3.toFixed(2);
        document.getElementById('thruster4').textContent = data.thruster4.toFixed(2);
        document.getElementById('thruster5').textContent = data.thruster5.toFixed(2);
        document.getElementById('thruster6').textContent = data.thruster6.toFixed(2);
        document.getElementById('bcd1').textContent = data.bcd1.toFixed(2);
        document.getElementById('bcd2').textContent = data.bcd2.toFixed(2);
        document.getElementById('bcd3').textContent = data.bcd3.toFixed(2);
        document.getElementById('bcd4').textContent = data.bcd4.toFixed(2);
        document.getElementById('bcd1Volt').textContent = data.bcd1Volt.toFixed(2);
        document.getElementById('bcd2Volt').textContent = data.bcd2Volt.toFixed(2);
        document.getElementById('bcd3Volt').textContent = data.bcd3Volt.toFixed(2);
        document.getElementById('bcd4Volt').textContent = data.bcd4Volt.toFixed(2);

        const currentTime = Date.now();
        if (currentTime - lastUpdateTime >= 500 || first) {

            updateGraph(liveChart, data.yaw, data.roll, data.pitch);
            lastUpdateTime = currentTime;
            first = false;
        }

    });

    // Add event listener for the clear button
    const clearButton = document.getElementById('clearButton');
    clearButton.addEventListener('click', () => {
        clearGraphData(liveChart);
    });
});

function getNewDataGraphs(width = 700, height = 320) {
    const div = document.createElement('div');
    div.style.width = width + 'px'; // Set width
    div.style.height = height + 'px'; // Set height
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
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x'
                    },
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'x'
                    }
                }
            }
        }
    });

    return { div, chart };
}

function updateGraph(chart, yaw, roll, pitch) {
    try {
        const maxDataPoints = 100; // Set the maximum number of data points to display

        const newDepth = Math.random() * 100;
        const newTemp = Math.random() * 30;
        const newTime = chart.data.labels.length + 1;

        // Remove the oldest data point if the buffer is full
        if (chart.data.labels.length >= maxDataPoints) {
            chart.data.labels.shift();
            chart.data.datasets.forEach((dataset) => {
                dataset.data.shift();
            });
        }

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