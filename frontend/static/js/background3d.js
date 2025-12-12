var SEPARATION = 100, AMOUNTX = 60, AMOUNTY = 60;
var container;
var camera, scene, renderer;
var particles, count = 0;
var mouseX = 0, mouseY = 0;
var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

function init3DBackground() {
    container = document.createElement('div');
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100%";
    container.style.height = "100%";
    container.style.zIndex = "-1";
    container.style.pointerEvents = "none"; // Let clicks pass through

    // Add a dark overlay to make sure text is readable
    // container.style.background = "linear-gradient(to bottom, transparent, #0f0e17)";

    document.body.appendChild(container);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 10000);
    camera.position.z = 1000;
    camera.position.y = 500; // Looking down

    scene = new THREE.Scene();

    // Create thousands of particles
    var numParticles = AMOUNTX * AMOUNTY;
    var positions = new Float32Array(numParticles * 3);
    var scales = new Float32Array(numParticles);

    var i = 0, j = 0;

    for (var ix = 0; ix < AMOUNTX; ix++) {
        for (var iy = 0; iy < AMOUNTY; iy++) {
            positions[i] = ix * SEPARATION - ((AMOUNTX * SEPARATION) / 2); // x
            positions[i + 1] = 0; // y
            positions[i + 2] = iy * SEPARATION - ((AMOUNTY * SEPARATION) / 2); // z

            scales[j] = 1;

            i += 3;
            j++;
        }
    }

    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('scale', new THREE.BufferAttribute(scales, 1));

    var material = new THREE.PointsMaterial({
        color: 0x00d0ff, // Cyan Theme
        size: 5, // Base size
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);

    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    document.addEventListener('mousemove', onDocumentMouseMove, false);
    // Touch support
    document.addEventListener('touchstart', onDocumentTouchStart, false);
    document.addEventListener('touchmove', onDocumentTouchMove, false);

    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onDocumentMouseMove(event) {
    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;
}

function onDocumentTouchStart(event) {
    if (event.touches.length === 1) {
        event.preventDefault();
        mouseX = event.touches[0].pageX - windowHalfX;
        mouseY = event.touches[0].pageY - windowHalfY;
    }
}

function onDocumentTouchMove(event) {
    if (event.touches.length === 1) {
        event.preventDefault();
        mouseX = event.touches[0].pageX - windowHalfX;
        mouseY = event.touches[0].pageY - windowHalfY;
    }
}

function animate() {
    requestAnimationFrame(animate);
    render();
}

function render() {
    camera.position.x += (mouseX - camera.position.x) * 0.05;
    camera.position.y += (-mouseY + 200 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    var positions = particles.geometry.attributes.position.array;
    var i = 0, j = 0;

    for (var ix = 0; ix < AMOUNTX; ix++) {
        for (var iy = 0; iy < AMOUNTY; iy++) {

            // Updates Y position for Wave Effect using sine
            positions[i + 1] = (Math.sin((ix + count) * 0.3) * 50) +
                (Math.sin((iy + count) * 0.5) * 50);

            i += 3;
            j++;
        }
    }

    particles.geometry.attributes.position.needsUpdate = true;
    count += 0.1;

    renderer.render(scene, camera);
}
