class Thruster {
  constructor(id) {
    this.id = id;
    this.value = 0;

    // Hardcoded positions based on ID
    let spacingX = width / 6;
    let spacingY = height / 6; // Adjusted spacing to move objects higher
    
    // Calculate positions based on ID
    if (id === 1 || id === 2) {
      this.y = spacingY; // Top row
    } else if (id === 5 || id === 6) {
      this.y = spacingY * 2.5; // Middle row (adjusted multiplier)
    } else {
      this.y = spacingY * 4; // Bottom row (adjusted multiplier)
    }

    if (id === 2 || id === 5 || id === 4) {
      this.x = width / 2 - spacingX; // Left positions for 2, 5, 4
    } else {
      this.x = width / 2 + spacingX; // Right positions for 1, 6, 3
    }

    // Adjust x for middle thrusters to be farther apart
    if (id === 5 || id === 6) {
      this.x = id === 5 ? this.x - spacingX : this.x + spacingX;
    }
  }

  updateValue(value) {
    this.value = value;
  }
  draw() {
    let radius = 30;

    // Set circle fill color based on thruster value
    if (this.value > 0) {
      fill('#90ee90'); // Light aesthetic green for positive values
    } else if (this.value < 0) {
      fill('#ffcccb'); // Light aesthetic red for negative values
    } else {
      fill('#f0f0f0'); // Default light color for neutral, if needed
    }

    stroke(0);
    circle(this.x, this.y, radius * 2); // Draw circle

    // Constant outline, moved further to the left
    stroke(0);
    noFill();
    rect(this.x - radius - 30, this.y - 50, 20, 100); // Outline rectangle

    // Fill rectangle based on value
    noStroke();
    let fillHeight = map(abs(this.value), 0, 1, 0, 50);
    if (this.value > 0) {
      fill(0, 255, 0); // Green for positive
      rect(this.x - radius - 30, this.y - fillHeight, 20, fillHeight);
    } else if (this.value < 0) {
      fill(255, 0, 0); // Red for negative
      rect(this.x - radius - 30, this.y, 20, fillHeight);
    }

    // Thruster text
    fill(0);
    text(`ID: ${this.id}\n${this.value.toFixed(2)} V`, this.x, this.y + radius + 20);
  }
}

class BCD {
  constructor(id) {
    this.id = id;
    this.mode = 0; // Initial mode set to 0
    // Assign x and y based on the specific BCD positions required
    this.x = id === 1 || id === 2 ? width / 2 - width / 6 * 2 : width / 2 + width / 6 * 2; // Left for 1 and 2, right for 3 and 4
    this.y = id === 1 || id === 4 ? 3/5 * height / 8 : height * 6 / 8; // Adjusted positions for top and bottom BCDs
    this.voltage = 0;
  }

  updateMode(mode) {
    this.mode = mode; // Directly set the mode to the new mode
  }
  
  updateVoltage(voltage) {
    this.voltage = voltage;
  }

  draw(width, height) {
    let radius = 20;

    // Set circle fill color based on BCD mode
    if (this.mode === 1) {
      fill('#90ee90'); // Light aesthetic green
    } else if (this.mode === -1) {
      fill('#ffcccb'); // Light aesthetic red
    } else {
      fill('#d3d3d3'); // Light aesthetic grey for neutral
    }

    stroke(0);
    circle(this.x, this.y, radius * 2); // Draw circle

    // Constant outline, moved further to the left
    stroke(0);
    noFill();
    rect(this.x - radius - 20, this.y - 25, 10, 50); // Outline rectangle

    // Fill based on mode
    noStroke();
    if (this.mode === 1) {
      fill(0, 255, 0); // Green top half
      rect(this.x - radius - 20, this.y - 25, 10, 25);
    } else if (this.mode === -1) {
      fill(255, 0, 0); // Red bottom half
      rect(this.x - radius - 20, this.y, 10, 25);
    }

    // BCD text
    fill(0);
    text(`Mode: ${this.mode}\nVoltage: ${this.voltage}`, this.x, this.y + radius + 20);
  }
}

let thrusters = [];
let bcds = [];

function setup() {
  width = 800
  height = 480
  let canvas = createCanvas(width, height);
  canvas.parent('top-down'); // Attach the canvas to the 'top-down' div
  // canvas.class('canvas-border'); // Add a CSS class to the canvas element

  textAlign(CENTER, CENTER);
  frameRate(10);

  // Initialize thruster and BCD instances
  thrusters = [
    new Thruster(1),
    new Thruster(2),
    new Thruster(3),
    new Thruster(4),
    new Thruster(5),
    new Thruster(6)
  ];

  bcds = [
    new BCD(1),
    new BCD(2),
    new BCD(3),
    new BCD(4)
  ];
}

function draw() {
  background(255);

  // Draw each thruster and BCD
  thrusters.forEach(thruster => thruster.draw());
  bcds.forEach(bcd => bcd.draw());
}

// Function to update thrusters and BCDs based on data received
function updateDevices(data) {
  thrusters.forEach((thruster, index) => {
    thruster.updateValue(data[`thruster${index + 1}`]);
  });

  bcds.forEach((bcd, index) => {
    bcd.updateMode(data[`bcd${index + 1}`]);
    bcd.updateVoltage(data[`bcd${index + 1}Volt`]);
  });
}

// Socket connection and event handling
var socket = io.connect('http://localhost:30001');

socket.on('connect', function() {
  console.log('WebSocket connected!');
});

socket.on('sensor_data', function(data) {
  console.log('Received sensor data:', data);
  updateDevices(data);
});

// Function to generate fake data
function generateFakeData() {
  // Generate fake data for thrusters and BCDs
  let fakeData = {};
  for (let i = 1; i <= 6; i++) {
      fakeData[`thruster${i}`] = Math.random() * 1; // Random value between 0 and 100
  }
  for (let i = 1; i <= 4; i++) {
      fakeData[`bcd${i}`] = Math.floor(Math.random() * 3) - 1; // Random mode between -1, 0, and 1
      fakeData[`bcd${i}Volt`] = Math.random() * 10; // Random voltage between 0 and 10
  }
  return fakeData;
}

// Function to update thrusters and BCDs for testing
function updateDevicesForTesting() {
  let fakeData = generateFakeData();
  updateDevices(fakeData);

  // Update HTML elements with fake data for visual confirmation
  for (let i = 1; i <= 6; i++) {
      document.getElementById(`thruster${i}`).textContent = fakeData[`thruster${i}`].toFixed(2);
  }
  for (let i = 1; i <= 4; i++) {
      document.getElementById(`bcd${i}`).textContent = fakeData[`bcd${i}`].toFixed(2);
      document.getElementById(`bcd${i}Volt`).textContent = fakeData[`bcd${i}Volt`].toFixed(2);
  }
}

// Call the function to update devices with fake data
// updateDevicesForTesting();
// You can also set an interval to update the devices with new fake data periodically
// setInterval(updateDevicesForTesting, 1000); // Update every second

