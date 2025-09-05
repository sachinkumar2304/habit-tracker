
import * as THREE from 'https://cdn.skypack.dev/three@0.132.2';

let scene, camera, renderer, stars, starGeo;

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
  camera.position.z = 1;
  camera.rotation.x = Math.PI / 2;

  renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById('background-canvas'),
    alpha: true
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  starGeo = new THREE.BufferGeometry();
  const starVertices = [];
  for (let i = 0; i < 6000; i++) {
    const x = (Math.random() - 0.5) * 2000;
    const y = (Math.random() - 0.5) * 2000;
    const z = (Math.random() - 0.5) * 2000;
    starVertices.push(x, y, z);
  }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));


  let sprite = new THREE.TextureLoader().load('https://threejs.org/examples/textures/sprites/disc.png');
  let starMaterial = new THREE.PointsMaterial({
    color: 0xaaaaaa,
    size: 0.7,
    map: sprite,
    transparent: true
  });

  stars = new THREE.Points(starGeo, starMaterial);
  scene.add(stars);

  window.addEventListener('resize', onWindowResize, false);

  animate();
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  starGeo.attributes.position.array.forEach((_, i) => {
    if (i % 3 === 1) { // y-coordinate
        starGeo.attributes.position.array[i] -= 0.2;
    }
    if (starGeo.attributes.position.array[i] < -1000) {
        starGeo.attributes.position.array[i] = 1000;
    }
  });
  starGeo.attributes.position.needsUpdate = true;
  stars.rotation.y += 0.0002;


  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

init();
