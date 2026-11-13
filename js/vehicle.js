/**
 * SecLeaf Sector 404: Vehicle Controller
 * Loads realistic 3D supercar model, binds RaycastVehicle physics,
 * handles correct inverted steering, dual headlights, dynamic tail lights,
 * nitro exhaust flames, and arcade vehicle gadgets (Hop, Nitro, EMP).
 */

class VehicleController {
  constructor(scene, physics, audio) {
    this.scene = scene;
    this.physics = physics;
    this.audio = audio;

    this.group = new THREE.Group();
    this.scene.add(this.group);

    this.wheelMeshes = [];
    this.modelLoaded = false;
    this.nitroActive = false;
    this.nitroTimer = 0;
    this.empCooldown = 0;

    this.setupPhysics();
    this.setupProceduralFallback();
    this.loadRealisticModel();
  }

  setupPhysics() {
    // Chassis RigidBody
    const width = 1.8;
    const height = 0.75;
    const length = 4.2;

    const chassisShape = new CANNON.Box(new CANNON.Vec3(width / 2, height / 2, length / 2));
    this.chassisBody = new CANNON.Body({
      mass: 320,
      material: this.physics.materials.chassis
    });
    // Low center of mass (Bruno Simon RAPID stability principle)
    this.chassisBody.addShape(chassisShape, new CANNON.Vec3(0, -0.35, 0));
    this.chassisBody.position.set(0, 0.80, -10);
    this.chassisBody.linearDamping = 0.04;
    this.chassisBody.angularDamping = 0.35;
    this.physics.world.addBody(this.chassisBody);

    // Raycast Vehicle
    this.vehicle = new CANNON.RaycastVehicle({
      chassisBody: this.chassisBody,
      indexRightAxis: 0,  // X
      indexUpAxis: 1,     // Y
      indexForwardAxis: 2 // Z
    });

    this.wheelRadius = 0.40;
    this.wheelThickness = 0.36;
    const wheelOptions = {
      radius: this.wheelRadius,
      directionLocal: new CANNON.Vec3(0, -1, 0),
      suspensionStiffness: 32,
      suspensionRestLength: 0.38,
      frictionSlip: 2.8,
      dampingRelaxation: 2.4,
      dampingCompression: 2.8,
      maxSuspensionForce: 100000,
      rollInfluence: 0.02,
      axleLocal: new CANNON.Vec3(-1, 0, 0),
      chassisConnectionPointLocal: new CANNON.Vec3(),
      maxSuspensionTravel: 0.35,
      customSlidingRotationalSpeed: -30,
      useCustomSlidingRotationalSpeed: true
    };

    const wFrontZ = 1.25;
    const wBackZ = -1.25;
    const wSpreadX = 0.90;

    // Front Left (0)
    wheelOptions.chassisConnectionPointLocal.set(wSpreadX, -0.05, wFrontZ);
    this.vehicle.addWheel(wheelOptions);

    // Front Right (1)
    wheelOptions.chassisConnectionPointLocal.set(-wSpreadX, -0.05, wFrontZ);
    this.vehicle.addWheel(wheelOptions);

    // Rear Left (2)
    wheelOptions.chassisConnectionPointLocal.set(wSpreadX, -0.05, wBackZ);
    this.vehicle.addWheel(wheelOptions);

    // Rear Right (3)
    wheelOptions.chassisConnectionPointLocal.set(-wSpreadX, -0.05, wBackZ);
    this.vehicle.addWheel(wheelOptions);

    this.vehicle.addToWorld(this.physics.world);
  }

  setupProceduralFallback() {
    this.visualGroup = new THREE.Group();
    this.group.add(this.visualGroup);

    this.fallbackChassisGroup = new THREE.Group();
    this.visualGroup.add(this.fallbackChassisGroup);

    // --- High-Fidelity Cyber Buggy (Matches Bruno Simon Aesthetic) ---
    const bodyMat = new THREE.MeshStandardMaterial({
      color: 0x1d182e, // Deep midnight cyber violet
      metalness: 0.70,
      roughness: 0.35
    });

    const cageMat = new THREE.MeshStandardMaterial({
      color: 0x222634, // Dark titanium roll cage
      metalness: 0.85,
      roughness: 0.40
    });

    const lightbarMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 }); // Glowing warm amber lightbar
    const roofCellMat = new THREE.MeshBasicMaterial({ color: 0xff1088 }); // Glowing magenta roof cells
    const xenonMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

    // 1. Lower Buggy Body & Skid Plate
    const lowerBody = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.45, 3.2), bodyMat);
    lowerBody.position.y = 0.36;
    lowerBody.castShadow = true;
    lowerBody.receiveShadow = true;
    this.fallbackChassisGroup.add(lowerBody);

    // Front Nose Taper
    const nose = new THREE.Mesh(new THREE.BoxGeometry(1.40, 0.32, 0.8), bodyMat);
    nose.position.set(0, 0.32, 1.6);
    nose.rotation.x = 0.15;
    nose.castShadow = true;
    this.fallbackChassisGroup.add(nose);

    // 2. Cockpit / Cabin
    const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.40, 1.7), bodyMat);
    cabin.position.set(0, 0.72, -0.15);
    cabin.castShadow = true;
    this.fallbackChassisGroup.add(cabin);

    // Dark Tinted Windshield
    const glassMat = new THREE.MeshStandardMaterial({ color: 0x090c14, metalness: 0.95, roughness: 0.1 });
    const windshield = new THREE.Mesh(new THREE.PlaneGeometry(1.10, 0.42), glassMat);
    windshield.position.set(0, 0.74, 0.72);
    windshield.rotation.x = -Math.PI / 4;
    this.fallbackChassisGroup.add(windshield);

    // 3. Roll Cage Frame Pillars
    const pillarGeo = new THREE.CylinderGeometry(0.032, 0.032, 0.65, 8);
    const pillarPositions = [
      { x: 0.54, y: 0.82, z: 0.65, rotX: -0.22, rotZ: -0.12 },
      { x: -0.54, y: 0.82, z: 0.65, rotX: -0.22, rotZ: 0.12 },
      { x: 0.54, y: 0.82, z: -0.90, rotX: 0.22, rotZ: -0.12 },
      { x: -0.54, y: 0.82, z: -0.90, rotX: 0.22, rotZ: 0.12 }
    ];
    pillarPositions.forEach(p => {
      const pillar = new THREE.Mesh(pillarGeo, cageMat);
      pillar.position.set(p.x, p.y, p.z);
      pillar.rotation.x = p.rotX;
      pillar.rotation.z = p.rotZ;
      this.fallbackChassisGroup.add(pillar);
    });

    // 4. Roof Energy Cells (3 Glowing Magenta Blocks)
    for (let c = -1; c <= 1; c++) {
      const cell = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.12, 0.32), roofCellMat);
      cell.position.set(c * 0.32, 0.98, -0.15);
      this.fallbackChassisGroup.add(cell);
    }

    // 5. Front Glowing Amber Lightbar & Headlights
    const lightbar = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.07, 0.10), lightbarMat);
    lightbar.position.set(0, 0.44, 1.95);
    this.fallbackChassisGroup.add(lightbar);

    [-0.50, 0.50].forEach(x => {
      const hl = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.06), xenonMat);
      hl.position.set(x, 0.34, 1.96);
      this.fallbackChassisGroup.add(hl);
    });

    // 6. Tail Lights (Cherry Red)
    this.tailMat = new THREE.MeshStandardMaterial({
      color: 0xff1122,
      emissive: 0xff1122,
      emissiveIntensity: 0.6
    });
    this.tailL = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.10, 0.06), this.tailMat);
    this.tailL.position.set(0.52, 0.40, -1.62);
    this.fallbackChassisGroup.add(this.tailL);
    this.tailR = this.tailL.clone();
    this.tailR.position.x = -0.52;
    this.fallbackChassisGroup.add(this.tailR);

    // 7. Dual Nitro Exhaust Pipes & Flame Emitters
    this.nitroFlames = [];
    const flameGeo = new THREE.ConeGeometry(0.14, 0.8, 8);
    flameGeo.rotateX(-Math.PI / 2);
    const flameMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0
    });

    [-0.36, 0.36].forEach(x => {
      const flame = new THREE.Mesh(flameGeo, flameMat.clone());
      flame.position.set(x, 0.30, -1.90);
      this.visualGroup.add(flame);
      this.nitroFlames.push(flame);
    });

    // 8. Chunky Off-Road Monster Wheels with Vivid Neon Purple Rims
    const tireGeo = new THREE.CylinderGeometry(this.wheelRadius, this.wheelRadius, this.wheelThickness, 24);
    tireGeo.rotateZ(Math.PI / 2);
    const tireMat = new THREE.MeshStandardMaterial({ color: 0x14151b, roughness: 0.90, metalness: 0.10 });
    const rimMat = new THREE.MeshStandardMaterial({
      color: 0x9333ea, // Vivid neon purple rim
      emissive: 0x7e22ce,
      emissiveIntensity: 0.75,
      roughness: 0.25,
      metalness: 0.80
    });

    for (let i = 0; i < 4; i++) {
      const wg = new THREE.Group();
      const tire = new THREE.Mesh(tireGeo, tireMat);
      tire.castShadow = true;
      wg.add(tire);

      const rim = new THREE.Mesh(
        new THREE.CylinderGeometry(this.wheelRadius * 0.62, this.wheelRadius * 0.62, this.wheelThickness + 0.02, 16),
        rimMat
      );
      rim.rotateZ(Math.PI / 2);
      wg.add(rim);

      this.scene.add(wg);
      this.wheelMeshes.push(wg);
    }
  }

  loadRealisticModel() {
    if (typeof THREE.GLTFLoader === 'undefined') {
      console.warn('[Vehicle] GLTFLoader not loaded, using procedural sports car.');
      return;
    }

    const loader = new THREE.GLTFLoader();

    if (typeof THREE.DRACOLoader !== 'undefined') {
      const dracoLoader = new THREE.DRACOLoader();
      dracoLoader.setDecoderPath('assets/draco/');
      loader.setDRACOLoader(dracoLoader);
    }

    // Load authentic Cyber Stunt Buggy model
    loader.load('assets/models/buggy.glb', (gltf) => {
      this.initBuggyModel(gltf.scene);
    }, undefined, (err) => {
      console.warn('[Vehicle] Buggy load failed, fallback to car.glb:', err);
      loader.load('assets/models/car.glb', (gltf) => {
        this.initSupercarModel(gltf.scene);
      }, undefined, (err2) => {
        console.warn('[Vehicle] Using procedural chassis fallback:', err2);
      });
    });
  }

  initBuggyModel(scene) {
    const chassis = scene.getObjectByName('chassis.001') || scene.getObjectByName('chassis001') || scene;
    const wheelSource = scene.getObjectByName('wheelContainer.001') || scene.getObjectByName('wheelContainer001');

    if (!chassis || !wheelSource) {
      this.visualGroup.add(scene);
      this.modelLoaded = true;
      return;
    }

    // Reference lights and blinkers
    this.parts = {
      chassis,
      stopLights: chassis.getObjectByName('stopLights.001') || chassis.getObjectByName('stopLights'),
      backLights: chassis.getObjectByName('backLights'),
      blinkerLeft: chassis.getObjectByName('blinkerLeft.001') || chassis.getObjectByName('blinkerLeft'),
      blinkerRight: chassis.getObjectByName('blinkerRight.001') || chassis.getObjectByName('blinkerRight')
    };

    // Authentic Stylized Materials Matching Bruno Simon Reference
    const bodyMat = new THREE.MeshStandardMaterial({
      color: 0x1d182e, // Deep midnight cyber violet
      metalness: 0.70,
      roughness: 0.32
    });

    const rollCageMat = new THREE.MeshStandardMaterial({
      color: 0x232737, // Matte dark titanium cage
      metalness: 0.85,
      roughness: 0.40
    });

    const neonLightbarMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 }); // Glowing warm amber lightbar
    const neonCellsMat = new THREE.MeshBasicMaterial({ color: 0xff1088 }); // Glowing magenta roof cells
    const xenonHeadlightMat = new THREE.MeshBasicMaterial({ color: 0xffffff }); // Xenon headlights
    
    this.stopLightsMat = new THREE.MeshStandardMaterial({
      color: 0xff1122,
      emissive: 0xff1122,
      emissiveIntensity: 0.6
    });

    const tireMat = new THREE.MeshStandardMaterial({
      color: 0x14151b,
      roughness: 0.90,
      metalness: 0.10
    });

    const rimMat = new THREE.MeshStandardMaterial({
      color: 0x9333ea, // Vivid neon purple rim centers
      emissive: 0x7e22ce,
      emissiveIntensity: 0.75,
      roughness: 0.25,
      metalness: 0.80
    });

    const strutMat = new THREE.MeshStandardMaterial({
      color: 0x94a3b8,
      roughness: 0.20,
      metalness: 0.90
    });

    // Apply materials to chassis
    chassis.traverse(child => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;

        const n = child.name.toLowerCase();
        if (n.includes('body')) {
          child.material = bodyMat;
        } else if (n.includes('cell') && n.includes('energy')) {
          child.material = neonCellsMat; // 3 neon magenta roof rack cells
        } else if (n.includes('cell') && n.includes('cage')) {
          child.material = rollCageMat;
        } else if (n.includes('headlight')) {
          child.material = neonLightbarMat; // Glowing amber front lightbar
        } else if (n.includes('energy') && !n.includes('cell')) {
          child.material = bodyMat; // Side/spoiler energy trim matches metallic chassis
        } else if (n.includes('stoplight') || n.includes('backlight')) {
          child.material = this.stopLightsMat;
        } else if (n.includes('blinker')) {
          child.material = new THREE.MeshBasicMaterial({ color: 0xffa500 });
        } else {
          child.material = rollCageMat;
        }
      }
    });

    // Buggy model chassis oriented along +X; rotate -Math.PI / 2 so it faces +Z (forward)
    chassis.rotation.y = -Math.PI / 2;
    chassis.position.set(0, -0.32, 0);
    this.visualGroup.add(chassis);

    // Subtle warm amber forward glow on asphalt
    const frontGlow = new THREE.PointLight(0xffa500, 1.4, 7.0);
    frontGlow.position.set(0, 0.28, 1.75);
    this.visualGroup.add(frontGlow);

    // Apply materials to wheelSource template
    wheelSource.traverse(child => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        const n = child.name.toLowerCase();
        if (n.includes('wheel') && !n.includes('paint') && !n.includes('guard')) {
          child.material = tireMat;
        } else if (n.includes('paint') || n.includes('rim')) {
          child.material = rimMat;
        } else if (n.includes('suspension')) {
          child.material = strutMat;
        } else {
          child.material = bodyMat;
        }
      }
    });

    // Hide procedural fallback primitives
    if (this.fallbackChassisGroup) this.fallbackChassisGroup.visible = false;
    this.wheelMeshes.forEach(w => w.visible = false);

    // Build 4 realistic wheels from wheelSource template
    this.buggyWheels = [];
    // 0: FL, 1: FR, 2: RL, 3: RR
    for (let i = 0; i < 4; i++) {
      const wheelGroup = new THREE.Group();
      const container = wheelSource.clone(true);
      container.position.set(0, 0, 0);

      let cylinder = null;
      let suspension = null;
      let guard = null;

      container.traverse(c => {
        if (c.name.includes('wheelCylinder')) cylinder = c;
        if (c.name.includes('wheelSuspension')) suspension = c;
        if (c.name.includes('wheelGuard')) guard = c;
      });

      if (cylinder) cylinder.position.set(0, 0, 0);
      if (suspension) suspension.visible = false; // Hide raw Blender shock strut

      // Left wheels face out with -Math.PI/2, right wheels face out with Math.PI/2
      const isLeft = (i === 0 || i === 2);
      container.rotation.y = isLeft ? -Math.PI / 2 : Math.PI / 2;

      wheelGroup.add(container);
      this.scene.add(wheelGroup);

      this.buggyWheels.push({
        group: wheelGroup,
        container,
        cylinder: cylinder || container,
        suspension,
        isLeft
      });
    }

    this.modelLoaded = true;
    this.isBuggyModel = true;
    console.log('[Vehicle] High-fidelity Cyber Stunt Buggy active.');
  }

  initSupercarModel(model) {
    const cyberBodyMat = new THREE.MeshPhysicalMaterial({
      color: 0x121722,
      metalness: 0.9,
      roughness: 0.2,
      clearcoat: 0.85,
      clearcoatRoughness: 0.15
    });
    const neonCaliperMat = new THREE.MeshBasicMaterial({ color: 0xbaec43 });

    model.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        const n = child.name.toLowerCase();
        if (n.includes('body')) child.material = cyberBodyMat;
        else if (n.includes('brake') || n.includes('caliper')) child.material = neonCaliperMat;
        else if (n.includes('rim')) { child.material.metalness = 0.95; child.material.roughness = 0.15; }
      }
    });

    model.scale.set(0.95, 0.95, 0.95);
    model.rotation.y = Math.PI;
    model.position.set(0, 0.08, 0);

    if (this.fallbackChassisGroup) this.fallbackChassisGroup.visible = false;
    this.wheelMeshes.forEach(w => w.visible = false);

    this.modelWheels = {
      fl: model.getObjectByName('wheel_fl'),
      fr: model.getObjectByName('wheel_fr'),
      rl: model.getObjectByName('wheel_rl'),
      rr: model.getObjectByName('wheel_rr')
    };

    this.visualGroup.add(model);
    this.modelLoaded = true;
  }

  // --- CONTROLS & GADGETS ---
  applyControls(input) {
    const maxSteer = 0.46;
    let enginePower = 2400;

    // Smooth speed-sensitive steering
    const speed = this.chassisBody.velocity.length();
    const speedFactor = Math.max(0.60, 1 - (speed / 38) * 0.40);
    const steerLimit = maxSteer * speedFactor;

    let desiredSteer = 0;
    if (input.left) desiredSteer += steerLimit;
    if (input.right) desiredSteer -= steerLimit;

    this.currentSteer = THREE.MathUtils.lerp(this.currentSteer || 0, desiredSteer, 0.22);
    this.vehicle.setSteeringValue(this.currentSteer, 0);
    this.vehicle.setSteeringValue(this.currentSteer, 1);

    // Nitro Gadget
    if (input.nitro && this.nitroTimer <= 0) {
      this.activateNitro();
    }

    if (this.nitroActive) {
      enginePower *= 3.0; // 3x nitro acceleration
    }

    const maxSpeed = this.nitroActive ? 34 : 20; // m/s (~72 - 122 km/h)
    const accel = this.nitroActive ? 12500 : 6800; // Snappy arcade propulsion

    const forwardCANNON = new CANNON.Vec3(0, 0, 1);
    this.chassisBody.vectorToWorldFrame(forwardCANNON, forwardCANNON);

    const currentSpeed = this.chassisBody.velocity.dot(forwardCANNON);

    // Apply active yaw torque when steering while in motion for sharp, responsive handling
    if (desiredSteer !== 0 && Math.abs(currentSpeed) > 0.2) {
      const yawSign = currentSpeed >= 0 ? 1 : -1;
      const yawTorque = (desiredSteer / maxSteer) * 1100 * yawSign;
      this.chassisBody.angularVelocity.y += (yawTorque / this.chassisBody.mass) * 0.04;
    }

    if (input.forward) {
      if (currentSpeed < -1.0) {
        // Active brake if currently moving backwards
        const brakeVec = forwardCANNON.scale(8500);
        this.chassisBody.applyForce(brakeVec, this.chassisBody.position);
        this.vehicle.setBrake(40, 0);
        this.vehicle.setBrake(40, 1);
        this.vehicle.setBrake(40, 2);
        this.vehicle.setBrake(40, 3);
      } else if (currentSpeed < maxSpeed) {
        // Snappy forward drive
        const pushForce = forwardCANNON.scale(accel);
        this.chassisBody.applyForce(pushForce, this.chassisBody.position);
        this.vehicle.applyEngineForce(-2200, 0);
        this.vehicle.applyEngineForce(-2200, 1);
        this.vehicle.applyEngineForce(-2200, 2);
        this.vehicle.applyEngineForce(-2200, 3);
        this.vehicle.setBrake(0, 0);
        this.vehicle.setBrake(0, 1);
        this.vehicle.setBrake(0, 2);
        this.vehicle.setBrake(0, 3);
      }
    } else if (input.backward) {
      if (currentSpeed > 1.0) {
        // Active brake if currently moving forward
        const brakeVec = forwardCANNON.scale(-8500);
        this.chassisBody.applyForce(brakeVec, this.chassisBody.position);
        this.vehicle.setBrake(40, 0);
        this.vehicle.setBrake(40, 1);
        this.vehicle.setBrake(40, 2);
        this.vehicle.setBrake(40, 3);
      } else if (currentSpeed > -14) {
        // Reverse drive
        const revForce = forwardCANNON.scale(-accel * 0.70);
        this.chassisBody.applyForce(revForce, this.chassisBody.position);
        this.vehicle.applyEngineForce(1800, 0);
        this.vehicle.applyEngineForce(1800, 1);
        this.vehicle.applyEngineForce(1800, 2);
        this.vehicle.applyEngineForce(1800, 3);
        this.vehicle.setBrake(0, 0);
        this.vehicle.setBrake(0, 1);
        this.vehicle.setBrake(0, 2);
        this.vehicle.setBrake(0, 3);
      }
    } else {
      // Natural rolling resistance without drag
      this.vehicle.applyEngineForce(0, 0);
      this.vehicle.applyEngineForce(0, 1);
      this.vehicle.applyEngineForce(0, 2);
      this.vehicle.applyEngineForce(0, 3);
      const idleBrake = input.brake ? 60 : 0.4;
      this.vehicle.setBrake(idleBrake, 0);
      this.vehicle.setBrake(idleBrake, 1);
      this.vehicle.setBrake(idleBrake, 2);
      this.vehicle.setBrake(idleBrake, 3);
    }

    // Bunny Hop Gadget
    if (input.hop) {
      this.triggerBunnyHop();
    }

    // EMP Shockwave Gadget
    if (input.emp && this.empCooldown <= 0) {
      this.triggerEMPShockwave();
    }
  }

  autoRightCar() {
    this.chassisBody.position.y += 1.3;
    this.chassisBody.velocity.set(0, 3.5, 0);
    this.chassisBody.angularVelocity.set(0, 0, 0);
    const quat = new THREE.Quaternion(
      this.chassisBody.quaternion.x,
      this.chassisBody.quaternion.y,
      this.chassisBody.quaternion.z,
      this.chassisBody.quaternion.w
    );
    const euler = new THREE.Euler().setFromQuaternion(quat, 'YXZ');
    const upright = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, euler.y, 0, 'YXZ'));
    this.chassisBody.quaternion.set(upright.x, upright.y, upright.z, upright.w);
    if (this.audio) this.audio.playHop();
  }

  activateNitro() {
    this.nitroActive = true;
    this.nitroTimer = 2.4; // 2.4s burst
    if (this.audio) this.audio.playNitro();

    // Ignite exhaust flames
    this.nitroFlames.forEach(f => {
      f.material.opacity = 0.95;
      f.scale.set(1.4, 2.2, 1.4);
    });
  }

  triggerBunnyHop() {
    // Only hop if grounded
    let isGrounded = false;
    for (let i = 0; i < this.vehicle.wheelInfos.length; i++) {
      if (this.vehicle.wheelInfos[i].isInContact) {
        isGrounded = true;
        break;
      }
    }
    if (isGrounded) {
      this.chassisBody.applyImpulse(new CANNON.Vec3(0, 1500, 0), this.chassisBody.position);
      if (this.audio) this.audio.playHop();
    }
  }

  triggerEMPShockwave() {
    this.empCooldown = 3.5; // 3.5s cooldown
    if (this.audio) this.audio.playEMP();

    // Trigger visual EMP shockwave ring in world
    if (window.worldManager) {
      window.worldManager.spawnEMPRing(this.chassisBody.position.x, this.chassisBody.position.z);
    }

    // Physical blast: send nearby dynamic bodies flying in 360 degrees
    const carPos = this.chassisBody.position;
    const blastRadius = 28;
    const blastForce = 4800;

    this.physics.dynamicBodies.forEach(item => {
      const b = item.body;
      if (b === this.chassisBody) return;
      const dist = b.position.distanceTo(carPos);
      if (dist < blastRadius && dist > 0.1) {
        const dir = b.position.vsub(carPos);
        dir.y = Math.max(dir.y, 0.4);
        dir.normalize();
        const factor = (1 - dist / blastRadius);
        b.wakeUp();
        b.applyImpulse(dir.scale(blastForce * factor), b.position);
      }
    });
  }

  respawn(spawnX = 0, spawnZ = -10) {
    this.chassisBody.position.set(spawnX, 0.80, spawnZ);
    this.chassisBody.velocity.set(0, 0, 0);
    this.chassisBody.angularVelocity.set(0, 0, 0);
    this.chassisBody.quaternion.set(0, 0, 0, 1);
  }

  update(delta) {
    // Sync chassis mesh position & rotation
    this.visualGroup.position.copy(this.chassisBody.position);
    this.visualGroup.quaternion.copy(this.chassisBody.quaternion);

    const speedKmh = Math.round(this.chassisBody.velocity.length() * 3.6);

    // Cool down gadgets
    if (this.nitroTimer > 0) {
      this.nitroTimer -= delta;
      if (this.nitroTimer <= 0) {
        this.nitroActive = false;
        this.nitroFlames.forEach(f => {
          f.material.opacity = 0;
        });
      }
    }
    if (this.empCooldown > 0) {
      this.empCooldown -= delta;
    }

    // Dynamic Tail Lights
    const isBraking = this.vehicle.wheelInfos[2].brake > 10;
    if (isBraking) {
      this.tailMat.color.setHex(0xff1111);
      this.tailMat.emissive.setHex(0xff1111);
      this.tailMat.emissiveIntensity = 1.2;
    } else {
      this.tailMat.color.setHex(0xef4444);
      this.tailMat.emissive.setHex(0xef4444);
      this.tailMat.emissiveIntensity = 0.4;
    }

    // Update Wheels Transform & Wheel Slip Screech
    let maxSlip = 0;
    for (let i = 0; i < this.vehicle.wheelInfos.length; i++) {
      this.vehicle.updateWheelTransform(i);
      const t = this.vehicle.wheelInfos[i].worldTransform;
      this.wheelMeshes[i].position.copy(t.position);
      this.wheelMeshes[i].quaternion.copy(t.quaternion);

      if (this.vehicle.wheelInfos[i].isInContact) {
        const slip = Math.abs(this.vehicle.wheelInfos[i].skidInfo);
        if (slip > maxSlip) maxSlip = slip;

        if (slip > 0.45 && speedKmh > 18 && window.worldManager) {
          window.worldManager.addSkidMark(t.position.x, t.position.z);
        }
      }

      // Authentic Cyber Buggy Wheel Articulation & Spin
      if (this.isBuggyModel && this.buggyWheels && this.buggyWheels[i]) {
        const bw = this.buggyWheels[i];
        bw.group.position.copy(t.position);
        bw.group.quaternion.copy(this.chassisBody.quaternion);

        // Steer front wheels (0: FL, 1: FR)
        if (i === 0 || i === 1) {
          bw.group.rotateY(this.currentSteer || 0);
        }

        // Spin wheel cylinder around its axle
        const forwardDir = new THREE.Vector3(0, 0, 1).applyQuaternion(this.visualGroup.quaternion);
        const velDir = new THREE.Vector3(this.chassisBody.velocity.x, 0, this.chassisBody.velocity.z);
        const moveSign = velDir.dot(forwardDir) >= 0 ? 1 : -1;
        const rollDelta = (this.chassisBody.velocity.length() * delta) / this.wheelRadius;

        bw.cylinder.rotation.z += (bw.isLeft ? 1 : -1) * rollDelta * moveSign;

        // Realistic Suspension Travel Compression
        if (bw.suspension) {
          const travel = this.vehicle.wheelInfos[i].suspensionLength / 0.38;
          bw.suspension.scale.y = Math.max(0.35, Math.min(1.3, travel));
        }
      }
    }

    // Dynamic Stop Lights & Blinkers for Buggy Model
    if (this.parts) {
      if (this.parts.stopLights) this.parts.stopLights.visible = isBraking;
      if (this.parts.backLights) this.parts.backLights.visible = isBraking;
      if (this.parts.blinkerLeft) {
        this.parts.blinkerLeft.visible = (this.currentSteer > 0.08) && ((Date.now() % 400) < 200);
      }
      if (this.parts.blinkerRight) {
        this.parts.blinkerRight.visible = (this.currentSteer < -0.08) && ((Date.now() % 400) < 200);
      }
    }

    // Rotate and steer realistic supercar model wheels if loaded
    if (this.modelLoaded && this.modelWheels && this.modelWheels.fl) {
      const rollDelta = (this.chassisBody.velocity.length() * delta) / this.wheelRadius;
      const currentSteer = this.vehicle.wheelInfos[0].steering;
      this.modelWheels.fl.rotation.y = -currentSteer;
      this.modelWheels.fr.rotation.y = -currentSteer;

      const forwardDir = new THREE.Vector3(0, 0, 1).applyQuaternion(this.visualGroup.quaternion);
      const velDir = new THREE.Vector3(this.chassisBody.velocity.x, 0, this.chassisBody.velocity.z);
      const moveSign = velDir.dot(forwardDir) >= 0 ? 1 : -1;

      this.modelWheels.fl.rotation.x += rollDelta * moveSign;
      this.modelWheels.fr.rotation.x += rollDelta * moveSign;
      this.modelWheels.rl.rotation.x += rollDelta * moveSign;
      this.modelWheels.rr.rotation.x += rollDelta * moveSign;
    }

    // Audio Screech Trigger on hard drift
    if (maxSlip > 0.5 && speedKmh > 20 && this.audio) {
      this.audio.playScreech(maxSlip);
    }

    // Engine Audio Update
    if (this.audio) {
      this.audio.updateEngine(speedKmh, 1);
    }
  }
}

window.VehicleController = VehicleController;
