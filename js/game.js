/**
 * SecLeaf Sector 404: Main Game Loop & Input System
 * Orchestrates rendering, physics, world streaming, vehicle gadgets,
 * dynamic camera tracking, and minimal UI integration.
 */

(function initGame() {
  const canvas = document.getElementById('webgl-canvas');
  let width = window.innerWidth;
  let height = window.innerHeight;

  // Three.js Scene
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x1a1329); // Dusk twilight atmosphere
  scene.fog = new THREE.FogExp2(0x1a1329, 0.007);

  // Isometric Follow Camera with Telephoto Miniature Look (matching Bruno Simon)
  const camera = new THREE.PerspectiveCamera(27, width / height, 0.5, 500);
  let targetFOV = 27;

  // High-Performance WebGL Renderer
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: 'high-performance'
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // Scene Lighting - Moody dusk atmosphere matching Bruno Simon reference
  const ambientLight = new THREE.AmbientLight(0x8476a3, 0.88);
  scene.add(ambientLight);

  const sunLight = new THREE.DirectionalLight(0xffe4cc, 1.25);
  sunLight.position.set(45, 60, 35);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 10;
  sunLight.shadow.camera.far = 160;
  const d = 50;
  sunLight.shadow.camera.left = -d;
  sunLight.shadow.camera.right = d;
  sunLight.shadow.camera.top = d;
  sunLight.shadow.camera.bottom = -d;
  sunLight.shadow.bias = -0.0004;
  scene.add(sunLight);

  const rimLight = new THREE.DirectionalLight(0x4f46e5, 0.45);
  rimLight.position.set(-45, 30, -35);
  scene.add(rimLight);

  // Initialize Core Engines
  const audio = window.soundEngine;
  const physics = window.physicsEngine;
  const vehicle = new window.VehicleController(scene, physics, audio);
  window.vehicleController = vehicle;

  const world = new window.WorldManager(scene, physics, audio);
  window.worldManager = world;

  // --- INPUT CONTROLLER ---
  const input = {
    forward: false,
    backward: false,
    left: false,
    right: false,
    brake: false,
    nitro: false,
    hop: false,
    emp: false
  };

  window.addEventListener('keydown', (e) => {
    audio.init();
    switch (e.code) {
      case 'KeyW':
      case 'ArrowUp': input.forward = true; e.preventDefault(); break;
      case 'KeyS':
      case 'ArrowDown': input.backward = true; e.preventDefault(); break;
      case 'KeyA':
      case 'ArrowLeft': input.left = true; e.preventDefault(); break;
      case 'KeyD':
      case 'ArrowRight': input.right = true; e.preventDefault(); break;
      case 'Space': input.hop = true; e.preventDefault(); break;
      case 'ShiftLeft':
      case 'ShiftRight': input.nitro = true; break;
      case 'KeyE': input.hop = true; break;
      case 'KeyF': input.emp = true; break;
      case 'KeyB':
      case 'KeyC': input.brake = true; break;
      case 'KeyR': resetCar(); break;
      case 'KeyH': audio.playHorn(); break;
    }
  });

  window.addEventListener('keyup', (e) => {
    switch (e.code) {
      case 'KeyW':
      case 'ArrowUp': input.forward = false; e.preventDefault(); break;
      case 'KeyS':
      case 'ArrowDown': input.backward = false; e.preventDefault(); break;
      case 'KeyA':
      case 'ArrowLeft': input.left = false; e.preventDefault(); break;
      case 'KeyD':
      case 'ArrowRight': input.right = false; e.preventDefault(); break;
      case 'Space': input.hop = false; break;
      case 'ShiftLeft':
      case 'ShiftRight': input.nitro = false; break;
      case 'KeyE': input.hop = false; break;
      case 'KeyF': input.emp = false; break;
      case 'KeyB':
      case 'KeyC': input.brake = false; break;
    }
  });

  // Touch Support
  function bindTouch(id, key) {
    const el = document.getElementById(id);
    if (!el) return;
    const start = (e) => { e.preventDefault(); audio.init(); input[key] = true; };
    const end = (e) => { e.preventDefault(); input[key] = false; };
    el.addEventListener('touchstart', start, { passive: false });
    el.addEventListener('touchend', end, { passive: false });
    el.addEventListener('mousedown', start);
    el.addEventListener('mouseup', end);
  }
  bindTouch('touch-gas', 'forward');
  bindTouch('touch-brake', 'backward');
  bindTouch('touch-left', 'left');
  bindTouch('touch-right', 'right');
  bindTouch('touch-drift', 'brake');
  bindTouch('touch-nitro', 'nitro');
  bindTouch('touch-hop', 'hop');

  // Minimal UI Button Listeners
  const resetEl = document.getElementById('btn-reset');
  if (resetEl) {
    resetEl.addEventListener('click', () => { audio.init(); resetCar(); });
  }

  const soundBtn = document.getElementById('btn-sound');
  if (soundBtn) {
    soundBtn.addEventListener('click', () => {
      audio.init();
      const on = audio.toggle();
      const icon = document.getElementById('sound-icon');
      const label = document.getElementById('sound-label');
      if (icon) icon.textContent = on ? '🔊' : '🔇';
      if (label) label.textContent = on ? 'SOUND' : 'MUTED';
    });
  }

  // --- HOLOGRAPHIC FLAG POPUP NOTIFICATION ---
  const flagToast = document.getElementById('flag-toast');
  const flagTextEl = document.getElementById('flag-text');
  const flagProgressEl = document.getElementById('flag-progress');
  const flagCopyBtn = document.getElementById('flag-copy-btn');

  window.showFlagToast = function(flagString, collected, total) {
    if (!flagToast) return;
    if (flagTextEl) flagTextEl.textContent = flagString;
    if (flagProgressEl) flagProgressEl.textContent = `FLAGS FOUND: ${collected}/${total}`;

    // Update Top Counter Badge
    const badge = document.getElementById('hud-flag-badge');
    if (badge) badge.textContent = `🚩 ${collected}/${total}`;

    flagToast.classList.add('show');
    setTimeout(() => {
      flagToast.classList.remove('show');
    }, 6000);
  };

  if (flagCopyBtn && flagTextEl) {
    flagCopyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(flagTextEl.textContent).then(() => {
        flagCopyBtn.textContent = 'COPIED!';
        setTimeout(() => { flagCopyBtn.textContent = 'COPY'; }, 2000);
      });
    });
  }

  function resetCar() {
    vehicle.respawn(0, -10);
    camTarget.set(0, 0.80, -10);
  }

  // --- 3D INTERACTIVE ORBIT CAMERA FOR POV ---
  const defaultTheta = -Math.PI * 0.75;
  const defaultPhi = 0.67;
  const defaultRadius = 20.5;

  let orbitTheta = defaultTheta;
  let orbitPhi = defaultPhi;
  let orbitRadius = defaultRadius;

  let isOrbitDragging = false;
  let lastPointerX = 0;
  let lastPointerY = 0;

  canvas.style.cursor = 'grab';

  canvas.addEventListener('pointerdown', (e) => {
    // Only orbit on primary button or touch outside UI buttons
    if (e.button !== 0 && e.pointerType === 'mouse') return;
    isOrbitDragging = true;
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;
    canvas.style.cursor = 'grabbing';
  });

  window.addEventListener('pointermove', (e) => {
    if (!isOrbitDragging) return;
    const dx = e.clientX - lastPointerX;
    const dy = e.clientY - lastPointerY;
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;

    orbitTheta -= dx * 0.007;
    orbitPhi = Math.max(0.10, Math.min(Math.PI / 2 - 0.06, orbitPhi + dy * 0.0055));
  });

  window.addEventListener('pointerup', () => {
    isOrbitDragging = false;
    canvas.style.cursor = 'grab';
  });

  window.addEventListener('pointercancel', () => {
    isOrbitDragging = false;
    canvas.style.cursor = 'grab';
  });

  // Mouse Wheel Zoom
  window.addEventListener('wheel', (e) => {
    orbitRadius = Math.max(7.5, Math.min(42.0, orbitRadius + e.deltaY * 0.018));
  }, { passive: true });

  // Double Click to Reset Orbit POV
  canvas.addEventListener('dblclick', () => {
    orbitTheta = defaultTheta;
    orbitPhi = defaultPhi;
    orbitRadius = defaultRadius;
  });

  // Camera Target & Spring State
  const camTarget = new THREE.Vector3(0, 0.80, -10);
  const currentOffset = new THREE.Vector3(
    orbitRadius * Math.cos(orbitPhi) * Math.sin(orbitTheta),
    orbitRadius * Math.sin(orbitPhi),
    orbitRadius * Math.cos(orbitPhi) * Math.cos(orbitTheta)
  );
  camera.position.copy(camTarget).add(currentOffset);
  camera.lookAt(camTarget);
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.05);

    // Apply Controls to Vehicle
    vehicle.applyControls(input);

    // Step Physics Simulation
    physics.step(delta);

    // Update Physics Visual Meshes
    physics.updateVisuals();

    // Update Vehicle
    vehicle.update(delta);

    const carPos = vehicle.chassisBody.position;
    const carVel = vehicle.chassisBody.velocity;

    // Strategic Chunk Streaming (Updates active chunks based on car position)
    world.updateChunks(carPos.x, carPos.z);

    // Update Animated World Elements (Flags, EMP Shockwave)
    world.update(delta, carPos);

    // Calculate Spherical Orbit Target Offset
    const targetOffsetX = orbitRadius * Math.cos(orbitPhi) * Math.sin(orbitTheta);
    const targetOffsetY = orbitRadius * Math.sin(orbitPhi);
    const targetOffsetZ = orbitRadius * Math.cos(orbitPhi) * Math.cos(orbitTheta);

    currentOffset.x = THREE.MathUtils.lerp(currentOffset.x, targetOffsetX, 0.12);
    currentOffset.y = THREE.MathUtils.lerp(currentOffset.y, targetOffsetY, 0.12);
    currentOffset.z = THREE.MathUtils.lerp(currentOffset.z, targetOffsetZ, 0.12);

    // Dynamic Camera Tracking with Velocity Lookahead
    const lookAhead = carVel.clone().scale(0.18);
    camTarget.x = THREE.MathUtils.lerp(camTarget.x, carPos.x + lookAhead.x, 0.10);
    camTarget.y = THREE.MathUtils.lerp(camTarget.y, carPos.y + 0.7, 0.10);
    camTarget.z = THREE.MathUtils.lerp(camTarget.z, carPos.z + lookAhead.z, 0.10);

    camera.position.copy(camTarget).add(currentOffset);
    camera.lookAt(camTarget);

    // Sun Shadow Follows Car
    sunLight.position.set(carPos.x + 45, 60, carPos.z + 35);
    sunLight.target.position.copy(carPos);

    // Dynamic Nitro Camera FOV Expansion
    targetFOV = vehicle.nitroActive ? 33 : 27;
    if (Math.abs(camera.fov - targetFOV) > 0.1) {
      camera.fov = THREE.MathUtils.lerp(camera.fov, targetFOV, 0.1);
      camera.updateProjectionMatrix();
    }

    renderer.render(scene, camera);
  }

  // Window Resize
  window.addEventListener('resize', () => {
    width = window.innerWidth;
    height = window.innerHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  });

  animate();
})();
