// Global variables
import './style.css'
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Water } from 'three/addons/objects/Water.js';


// Global ROV
let rov;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                            //
//                                 Setup the Scene, Camera, and Renderer                                      //
//                                                                                                            //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB); // Sky blue color
// Initialize camera with a smaller FOV to zoom in
const camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 0.1, 1000); // Decrease FOV to zoom in
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#nav'),
    antialias: true
});

const canvas = document.querySelector('#nav');
const width = canvas.clientWidth;
const heightMagic = -200
const height = canvas.clientHeight - heightMagic; // Adjust the height to leave space for the dashboard

// Initial setup for renderer size based on the canvas client size
renderer.setSize(width, height); // The third parameter `false` tells the renderer to not set the canvas size style, only the drawing buffer size.
camera.aspect = width / height;
camera.updateProjectionMatrix();

// Add an event listener for window resize to adjust the canvas and renderer size
window.addEventListener('resize', () => {
    // Update sizes based on the canvas's client size
    const width = canvas.clientWidth;
    const height = canvas.clientHeight - heightMagic;

    // Update renderer and camera
    renderer.setSize(width, height, false); // Adjust drawing buffer size without changing the style
    camera.aspect = width / height;
    camera.updateProjectionMatrix();

});

// Make sure the initial render call uses the updated size
renderer.render(scene, camera);

//
// Set up lighting
//

const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(10, 10, 10);
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

//
// Set up water
//

const waterGeometry = new THREE.PlaneGeometry(10000, 10000);
scene.fog = new THREE.FogExp2(0xaaaaaa, 0.0007); // Adjust color and density

const water = new Water(waterGeometry, {
    textureWidth: 512,
    textureHeight: 512,
    waterNormals: new THREE.TextureLoader().load('textures/waternormals.jpg', function (texture) {
        texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
    }),
    alpha: 1.0,
    sunDirection: directionalLight.position.clone().normalize(),
    sunColor: 0xffffff,
    waterColor: 0x001e0f,
    distortionScale: 3.7,
    fog: scene.fog !== undefined
});

water.material.side = THREE.DoubleSide;
water.material.uniforms['waterColor'].value.set(0x70b4e0); // Lighter blue for water

water.rotation.x = -Math.PI / 2;
scene.add(water);

//
// Set up sunlight
//

const sunLight = new THREE.DirectionalLight(0xffffff, 1.0); // Sun-like light
sunLight.position.set(5, 10, 5); // Adjust to simulate the sun's position
sunLight.intensity = 0.5; // Adjust this value as needed
scene.add(sunLight);


//
// Set up seafloor
// 
const seafloorTexture = new THREE.TextureLoader().load('textures/seafloorTexture.jpg'); 

// Create seafloor geometry
const seafloorGeometry = new THREE.PlaneGeometry(10000, 10000);
const seafloorMaterial = new THREE.MeshStandardMaterial({ map: seafloorTexture });
const seafloor = new THREE.Mesh(seafloorGeometry, seafloorMaterial);

seafloor.rotation.x = -Math.PI / 2; // Orient the plane horizontally
seafloor.position.y = -80; // Adjust the depth

// Adjust texture repeat for larger seafloor
seafloorTexture.wrapS = seafloorTexture.wrapT = THREE.RepeatWrapping;
seafloorTexture.repeat.set(50, 50); // Adjust these values as needed

seafloorTexture.generateMipmaps = true;
seafloorTexture.minFilter = THREE.LinearMipmapLinearFilter;

scene.add(seafloor);

// 
// Load the ROV model
//

const loader = new GLTFLoader();
//untitled_scaled.glb is the ROV CAD model
loader.load('textures/untitled_scaled.glb', function (gltf) {
    gltf.scene.traverse(function (child) {
        if (child.isMesh) {
            child.material = new THREE.MeshStandardMaterial({ color: 0xffffff }); // White color
        }
    });
    rov = gltf.scene;
    scene.add(rov);
}, undefined, function (error) {
    console.error(error);
});

// OrbitControls setup for camera
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Optional, but can provide a smoother control experience
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;

// Camera position
// camera.position.z = 15;  // Decreased from 10
// camera.position.y = -5;  // Decreased from 20
// camera.position.x = -5;  // Decreased from 20
// camera.lookAt(0, 0, 0);


// Currently not working
// function resizeListen() {
//       window.addEventListener('resize', () => {
//           const container = document.getElementById('nav');
//           const newWidth = container.clientWidth - 2*margin;
//           const newHeight = newWidth * aspectRatio;
//           camera.aspect = 1/aspectRatio; // Set the aspect ratio for the camera
//           camera.updateProjectionMatrix();
//           renderer.setSize(newWidth, newHeight);
//       });
//   }

// GET SENSOR DATA FOR ROTATION

function initSocketConnection() {
    var socket = io.connect('http://localhost:30001');

    socket.on('connect', function() {
        console.log('WebSocket connected!');
    });

    // Listen for 'sensor_data' events from the server
    socket.on('sensor_data', function(data) {
        console.log('Received sensor data:', data);

        if (data && rov) {
            // Assuming the data contains yaw, roll, and pitch in degrees
            const yaw = THREE.MathUtils.degToRad(data.yaw);
            const roll = THREE.MathUtils.degToRad(data.roll);
            const pitch = THREE.MathUtils.degToRad(data.pitch);
            const depth = data.depth;

            // Apply rotation to the ROV model
            // Note: Three.js uses Euler angles in the order of rotation: 'XYZ', which is a common standard.
            // You might need to adjust the order or the axes depending on how your IMU data is oriented.
            rov.rotation.set(pitch, yaw, roll);
            rov.position.y = -depth; // Adjust the depth based on the sensor data
        }
    });
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                            //
//                                    Animation and Keyboard Controls                                         //
//                                                                                                            //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const xMagic = 10; // Adjust these values as needed
const yMagic = 10; // Adjust these values as needed
const zMagic = -1.3; // Adjust these values as needed
const magic = 5;
function animate() {
    requestAnimationFrame(animate)
    // Check if camera is below 'water level' (assuming water level is y=0)
    if (camera.position.y < 0) {
        // Underwater settings
        scene.fog.color.set(0x020202); // Darker, bluish fog
        ambientLight.intensity = 0.2; // Reduced ambient light underwater
    } else {
        // Above water settings
        scene.fog.color.set(0xaaaaaa);
        ambientLight.intensity = 0.5; // Normal ambient light above water
    }

    // Update water
    const time = performance.now() * 0.001;
    water.material.uniforms['time'].value += 1.0 / 60.0;

    // Make the camera follow the ROV from a greater distance
    if (autoFollow && rov) {
        const distance = 30; // Increase this value to zoom out
        camera.position.x = rov.position.x + distance + xMagic;
        camera.position.y = rov.position.y + distance / 2 + yMagic; // Adjust Y position for a better angle
        camera.position.z = rov.position.z + distance + zMagic;
        camera.lookAt(rov.position.x + xMagic + magic, rov.position.y + yMagic + magic, rov.position.z + zMagic + magic);
    }

    renderer.render(scene, camera)
}

let moveSpeed = 1.1; // Adjust speed as needed
let autoFollow = true;

function onDocumentKeyDown(event) {
    if (event.key === 'f' || event.key === 'F') { // 'f' or 'F' key to toggle follow mode
        autoFollow = !autoFollow;
        controls.enabled = !autoFollow;
        event.preventDefault(); // Prevent default to ensure 'F' key is not used for other purposes
        console.log("Auto-follow mode:", autoFollow); // Log the status for debugging
    }

    if (!rov || !autoFollow) return;

    // Updated to use `event.key`
    switch(event.key) {
        case 'w':
        case 'W':
            event.preventDefault(); // Prevent the default action (scrolling)
            rov.position.z -= moveSpeed;
            break;
        case 's':
        case 'S':
            event.preventDefault(); // Prevent the default action (scrolling)
            rov.position.z += moveSpeed;
            break;
        case 'a':
        case 'A':

            rov.position.x -= moveSpeed;
            break;
        case 'd':
        case 'D':
            rov.position.x += moveSpeed;
            break;
        case ' ':
            event.preventDefault(); // Prevent the default action (scrolling)
            rov.position.y += moveSpeed;
            console.log("seen");
            break;
        case 'Shift':
            event.preventDefault(); // Prevent the default action (scrolling)
            if (rov.position.y > -80) { // Check if above seafloor
                rov.position.y -= moveSpeed;
            }
            break;
    }
}


// resizeListen()
window.onload = function() {
    document.getElementById('nav').focus();
};
document.getElementById('nav').addEventListener("keydown", onDocumentKeyDown, false);

// Call this function once to set up the WebSocket connection and event listeners
initSocketConnection();
animate()
