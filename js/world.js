/**
 * SecLeaf Sector 404: World Manager & Infinite Chunk System
 * Handles multi-district stunt park, strategic chunk streaming culling,
 * destructible physics monoliths, domino megastructures, and collectible CTF flags.
 */

class WorldManager {
  constructor(scene, physics, audio) {
    this.scene = scene;
    this.physics = physics;
    this.audio = audio;

    this.chunkSize = 120; // 120m x 120m per chunk
    this.activeChunkRadius = 2; // Active distance
    this.chunks = new Map();
    this.currentChunkKey = '0,0';

    // Flag Collectibles
    this.flags = [
      {
        id: 'flag1',
        text: 'SecLeaf{BUNNY_HOP_H4CK3R_0X404}',
        hint: 'District Central: Atop 404 Monolith',
        pos: new THREE.Vector3(0, 6.2, 7),
        collected: false
      },
      {
        id: 'flag2',
        text: 'SecLeaf{404_DR1V3_BY_PWN_2027}',
        hint: 'District North: Skyway Stunt Tower',
        pos: new THREE.Vector3(0, 14.5, 120),
        collected: false
      },
      {
        id: 'flag3',
        text: 'SecLeaf{DOM1NO_COLL1S1ON_OR4CL3}',
        hint: 'District East: Domino Wall Canyon',
        pos: new THREE.Vector3(120, 2.0, 0),
        collected: false
      },
      {
        id: 'flag4',
        text: 'SecLeaf{SP33D_D3MON_OV3RDR1V3}',
        hint: 'District West: Drift Speedway Apex',
        pos: new THREE.Vector3(-120, 3.5, 0),
        collected: false
      }
    ];

    this.flagMeshes = [];
    this.collectedCount = 0;
    this.windRibbons = [];

    // Materials Library - Twilight / Synthwave Palette Matching Bruno Simon
    this.materials = {
      darkTile: new THREE.MeshStandardMaterial({ color: 0x1a1329, roughness: 0.85, metalness: 0.2 }),
      road: new THREE.MeshStandardMaterial({ color: 0x1f1a2c, roughness: 0.85, metalness: 0.15 }),
      asphalt: new THREE.MeshStandardMaterial({ color: 0x1c1729, roughness: 0.85, metalness: 0.15, side: THREE.DoubleSide }),
      kerbRed: new THREE.MeshStandardMaterial({
        color: 0x5c1522, // Rich dark maroon red matching Bruno Simon reference
        roughness: 0.82,
        metalness: 0.08,
        side: THREE.DoubleSide
      }),
      kerbBlue: new THREE.MeshStandardMaterial({
        color: 0x343ca6, // Rich royal cobalt blue matching Bruno Simon reference
        roughness: 0.82,
        metalness: 0.08,
        side: THREE.DoubleSide
      }),
      sidewalk: new THREE.MeshStandardMaterial({
        color: 0x4e466d, // Soft lavender slate paver
        roughness: 0.65,
        metalness: 0.12,
        side: THREE.DoubleSide
      }),
      debris: new THREE.MeshBasicMaterial({ color: 0x161022, side: THREE.DoubleSide }),
      grass: new THREE.MeshStandardMaterial({ color: 0x242a35, roughness: 0.85, metalness: 0.1, flatShading: true }),
      grassTip: new THREE.MeshStandardMaterial({ color: 0x3d6b5e, roughness: 0.75, metalness: 0.1, flatShading: true }),
      foliage: new THREE.MeshStandardMaterial({ color: 0x22382e, roughness: 0.85, flatShading: true }),
      treeTrunk: new THREE.MeshStandardMaterial({ color: 0x241812, roughness: 0.90 }),
      barrelBlue: new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.45, metalness: 0.35 }),
      barrelWhite: new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.30, metalness: 0.20 }),
      barrelLid: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.80 }),
      windRibbon: new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.45, side: THREE.DoubleSide }),
      accentLime: new THREE.MeshBasicMaterial({ color: 0xbaec43 }),
      accentCyan: new THREE.MeshBasicMaterial({ color: 0x00f0ff }),
      monolithBlock: new THREE.MeshStandardMaterial({ color: 0x221a36, roughness: 0.4, metalness: 0.6 }),
      monolithTop: new THREE.MeshStandardMaterial({ color: 0xffaa00, emissive: 0xffaa00, emissiveIntensity: 0.5 }),
      rampMat: new THREE.MeshStandardMaterial({ color: 0x26203a, roughness: 0.5, metalness: 0.5 }),
      crateMat: new THREE.MeshStandardMaterial({ color: 0x322849, roughness: 0.7, metalness: 0.3 })
    };

    // Shared Skid Marks Canvas & Texture
    this.setupSkidCanvas();

    // Setup Procedural Paved Sidewalk Texture
    this.setupSidewalkTexture();

    // Setup Asphalt Noise Pebble Texture
    this.setupAsphaltTexture();

    // Setup Flags
    this.setupFlagMeshes();

    // Setup Shockwave Ring Effect
    this.setupShockwavePool();

    // Initial load around origin
    this.updateChunks(0, 0);
  }

  setupSidewalkTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#504870';
    ctx.fillRect(0, 0, 256, 256);

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.16)';
    ctx.lineWidth = 2.5;

    for (let i = -256; i <= 512; i += 32) {
      ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i + 256, 256); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(i, 256); ctx.lineTo(i + 256, 0); ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    this.materials.sidewalk.color.setHex(0xffffff);
    this.materials.sidewalk.map = tex;
    this.materials.sidewalk.needsUpdate = true;
  }

  setupAsphaltTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#261f36'; // Authentic twilight purple-grey asphalt
    ctx.fillRect(0, 0, 512, 512);

    // Fine asphalt grains and subtle gravel flakes matching Bruno Simon reference
    for (let i = 0; i < 4500; i++) {
      const x = Math.random() * 512;
      const y = Math.random() * 512;
      const r = Math.random() * 1.5 + 0.4;
      const shade = Math.random();
      if (shade > 0.65) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
      } else if (shade > 0.3) {
        ctx.fillStyle = 'rgba(95, 80, 130, 0.22)';
      } else {
        ctx.fillStyle = 'rgba(12, 8, 20, 0.35)';
      }
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 16);
    this.materials.asphalt.color.setHex(0xffffff);
    this.materials.asphalt.roughness = 0.86;
    this.materials.asphalt.metalness = 0.08;
    this.materials.asphalt.map = tex;
    this.materials.asphalt.needsUpdate = true;
  }

  setupSkidCanvas() {
    this.skidCanvas = document.createElement('canvas');
    this.skidCanvas.width = 1024;
    this.skidCanvas.height = 1024;
    this.skidCtx = this.skidCanvas.getContext('2d');
    this.skidCtx.fillStyle = '#1a1329';
    this.skidCtx.fillRect(0, 0, 1024, 1024);

    // Initial Twilight Cyber Grid
    this.skidCtx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
    this.skidCtx.lineWidth = 1;
    for (let i = 0; i < 1024; i += 32) {
      this.skidCtx.beginPath();
      this.skidCtx.moveTo(i, 0); this.skidCtx.lineTo(i, 1024); this.skidCtx.stroke();
      this.skidCtx.beginPath();
      this.skidCtx.moveTo(0, i); this.skidCtx.lineTo(1024, i); this.skidCtx.stroke();
    }
    this.skidTexture = new THREE.CanvasTexture(this.skidCanvas);
    this.skidTexture.anisotropy = 8;
  }

  addSkidMark(worldX, worldZ) {
    const u = ((worldX % 240 + 240) % 240 / 240) * 1024;
    const v = ((worldZ % 240 + 240) % 240 / 240) * 1024;
    this.skidCtx.fillStyle = 'rgba(0, 0, 0, 0.22)';
    this.skidCtx.beginPath();
    this.skidCtx.arc(u, v, 3.5, 0, Math.PI * 2);
    this.skidCtx.fill();
    this.skidTexture.needsUpdate = true;
  }

  setupFlagMeshes() {
    this.flags.forEach(flag => {
      const group = new THREE.Group();
      group.position.copy(flag.pos);

      // Flag Pole
      const poleGeo = new THREE.CylinderGeometry(0.04, 0.05, 3.0, 8);
      const poleMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9 });
      const pole = new THREE.Mesh(poleGeo, poleMat);
      pole.position.y = 1.5;
      group.add(pole);

      // Holographic Flag Banner
      const bannerGeo = new THREE.PlaneGeometry(1.4, 0.8);
      bannerGeo.translate(0.7, 0, 0);
      const bannerMat = new THREE.MeshBasicMaterial({
        color: 0xbaec43,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.85
      });
      const banner = new THREE.Mesh(bannerGeo, bannerMat);
      banner.position.y = 2.4;
      group.add(banner);

      // Hologram Base Ring
      const ringGeo = new THREE.RingGeometry(0.6, 0.9, 16);
      ringGeo.rotateX(-Math.PI / 2);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0xbaec43,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.5
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.y = 0.05;
      group.add(ring);

      // Beacon Light
      const light = new THREE.PointLight(0xbaec43, 2.0, 15);
      light.position.y = 2.0;
      group.add(light);

      this.scene.add(group);
      this.flagMeshes.push({ group, banner, ring, light, flag });
    });
  }

  setupShockwavePool() {
    const geo = new THREE.RingGeometry(0.5, 1.2, 32);
    geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({
      color: 0xbaec43,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0
    });
    this.empRing = new THREE.Mesh(geo, mat);
    this.scene.add(this.empRing);
    this.empRingState = { active: false, radius: 1, maxRadius: 32, alpha: 0 };
  }

  spawnEMPRing(x, z) {
    this.empRing.position.set(x, 0.1, z);
    this.empRing.scale.set(1, 1, 1);
    this.empRingState = { active: true, radius: 1, maxRadius: 32, alpha: 0.95 };
  }

  // --- STRATEGIC CHUNK STREAMING ---
  updateChunks(carX, carZ) {
    const cx = Math.floor((carX + this.chunkSize / 2) / this.chunkSize);
    const cz = Math.floor((carZ + this.chunkSize / 2) / this.chunkSize);
    const key = `${cx},${cz}`;

    if (key === this.currentChunkKey && this.chunks.size > 0) return;
    this.currentChunkKey = key;

    // Load active radius
    const activeKeys = new Set();
    for (let dx = -this.activeChunkRadius; dx <= this.activeChunkRadius; dx++) {
      for (let dz = -this.activeChunkRadius; dz <= this.activeChunkRadius; dz++) {
        const ckX = cx + dx;
        const ckZ = cz + dz;
        const cKey = `${ckX},${ckZ}`;
        activeKeys.add(cKey);

        if (!this.chunks.has(cKey)) {
          this.buildChunk(ckX, ckZ);
        } else {
          // Reactivate chunk
          const chunkData = this.chunks.get(cKey);
          chunkData.group.visible = true;
          chunkData.bodies.forEach(b => b.wakeUp());
        }
      }
    }

    // Culling distant chunks
    this.chunks.forEach((chunkData, cKey) => {
      if (!activeKeys.has(cKey)) {
        chunkData.group.visible = false;
        chunkData.bodies.forEach(b => b.sleep());
      }
    });
  }

  buildChunk(cx, cz) {
    const chunkGroup = new THREE.Group();
    const bodies = [];
    const worldX = cx * this.chunkSize;
    const worldZ = cz * this.chunkSize;

    // Chunk Floor Mesh
    const floorGeo = new THREE.PlaneGeometry(this.chunkSize, this.chunkSize);
    const floorMat = new THREE.MeshStandardMaterial({
      map: this.skidTexture,
      roughness: 0.8,
      metalness: 0.2
    });
    const floorMesh = new THREE.Mesh(floorGeo, floorMat);
    floorMesh.rotation.x = -Math.PI / 2;
    floorMesh.position.set(worldX, 0, worldZ);
    floorMesh.receiveShadow = true;
    chunkGroup.add(floorMesh);

    // Border Neon Grid Lines for Strategic Visual Depth
    const borderGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(worldX - this.chunkSize / 2, 0.05, worldZ - this.chunkSize / 2),
      new THREE.Vector3(worldX + this.chunkSize / 2, 0.05, worldZ - this.chunkSize / 2),
      new THREE.Vector3(worldX + this.chunkSize / 2, 0.05, worldZ + this.chunkSize / 2),
      new THREE.Vector3(worldX - this.chunkSize / 2, 0.05, worldZ + this.chunkSize / 2),
      new THREE.Vector3(worldX - this.chunkSize / 2, 0.05, worldZ - this.chunkSize / 2)
    ]);
    const borderLine = new THREE.Line(borderGeo, new THREE.LineBasicMaterial({ color: 0x1e293b, transparent: true, opacity: 0.35 }));
    chunkGroup.add(borderLine);

    // DISTRICT DISPATCHER
    if (cx === 0 && cz === 0) {
      this.buildDistrictCentral(chunkGroup, bodies, worldX, worldZ);
    } else if (cx === 0 && cz === 1) {
      this.buildDistrictStuntPark(chunkGroup, bodies, worldX, worldZ);
    } else if (cx === 1 && cz === 0) {
      this.buildDistrictDominoCanyon(chunkGroup, bodies, worldX, worldZ);
    } else if (cx === -1 && cz === 0) {
      this.buildDistrictSpeedway(chunkGroup, bodies, worldX, worldZ);
    } else if (cx === 0 && cz === -1) {
      this.buildDistrictPinball(chunkGroup, bodies, worldX, worldZ);
    } else {
      this.buildProceduralEndlessChunk(chunkGroup, bodies, worldX, worldZ, cx, cz);
    }

    this.scene.add(chunkGroup);
    this.chunks.set(`${cx},${cz}`, { group: chunkGroup, bodies });
  }

  // --- DISTRICT 1: CENTRAL ARENA (Authentic Bruno Simon Style Racetrack) ---
  buildDistrictCentral(group, bodies, wx, wz) {
    // 1. Build Sweeping Curved Asphalt Racetrack, Alternating Kerbs, 3D Barrels, Trees & Ribbons
    this.buildCurvedRacetrack(group, bodies, wx, wz);

    // 2. 3D 404 Destructible Monolith Blocks (Positioned near track curve apex)
    const bSize = 1.0;
    const patterns = {
      '4_1': [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
      '0':   [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
      '4_2': [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]
    };

    const startZ = wz + 16;
    const letterSpacing = 5.0;
    const letters = [
      { grid: patterns['4_1'], offsetX: wx - letterSpacing },
      { grid: patterns['0'], offsetX: wx },
      { grid: patterns['4_2'], offsetX: wx + letterSpacing }
    ];

    letters.forEach(letter => {
      const grid = letter.grid;
      for (let r = 0; r < grid.length; r++) {
        for (let c = 0; c < grid[0].length; c++) {
          if (grid[r][c] === 1) {
            const x = letter.offsetX + (c - 1) * 1.05;
            const y = (grid.length - 1 - r) * 1.05 + bSize / 2 + 0.1;
            const z = startZ;
            const isTop = (r === 0);

            const mesh = new THREE.Mesh(
              new THREE.BoxGeometry(bSize, bSize, bSize),
              isTop ? this.materials.monolithTop : this.materials.monolithBlock
            );
            mesh.castShadow = true;
            group.add(mesh);

            const body = new CANNON.Body({ mass: 4.5, material: this.physics.materials.obstacle });
            body.addShape(new CANNON.Box(new CANNON.Vec3(bSize / 2, bSize / 2, bSize / 2)));
            body.position.set(x, y, z);
            this.physics.addDynamicBody(body, mesh);
            bodies.push(body);
          }
        }
      }
    });

    // 10-Pin Bowling Triangle
    const startX = wx - 26;
    const bZ = wz + 16;
    const pinGeo = new THREE.CylinderGeometry(0.2, 0.32, 1.4, 14);
    const pinMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 });
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });

    for (let row = 0; row < 4; row++) {
      const count = row + 1;
      const rOffset = -(count - 1) * 0.5;
      for (let p = 0; p < count; p++) {
        const x = startX + rOffset + p * 1.0;
        const z = bZ + row * 1.2;

        const pGroup = new THREE.Group();
        const base = new THREE.Mesh(pinGeo, pinMat);
        base.castShadow = true;
        pGroup.add(base);
        const r = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.21, 0.2, 14), ringMat);
        r.position.y = 0.25;
        pGroup.add(r);
        group.add(pGroup);

        const body = new CANNON.Body({ mass: 2.5, material: this.physics.materials.obstacle });
        body.addShape(new CANNON.Cylinder(0.2, 0.32, 1.4, 12));
        body.position.set(x, 0.7, z);
        this.physics.addDynamicBody(body, pGroup);
        bodies.push(body);
      }
    }

    // Launch Ramp
    this.createRamp(group, bodies, wx + 24, 0, wz - 10, 8, 2.2, 9, 0);
  }

  buildCurvedRacetrack(group, bodies, wx, wz) {
    const trackPoints = [
      new THREE.Vector3(wx - 26, 0, wz - 36),
      new THREE.Vector3(wx - 14, 0, wz - 24),
      new THREE.Vector3(wx - 1,  0, wz - 10), // passes right through spawn
      new THREE.Vector3(wx + 8,  0, wz + 4),
      new THREE.Vector3(wx + 22, 0, wz + 16), // sweeping apex around monolith
      new THREE.Vector3(wx + 36, 0, wz + 6),
      new THREE.Vector3(wx + 34, 0, wz - 16),
      new THREE.Vector3(wx + 16, 0, wz - 34),
      new THREE.Vector3(wx - 6,  0, wz - 40)
    ];
    const curve = new THREE.CatmullRomCurve3(trackPoints, true, 'centripetal');

    const segments = 96;
    const roadHalfWidth = 6.2;
    const kerbWidth = 1.35;
    const sidewalkWidth = 4.2;

    const samples = [];
    for (let i = 0; i <= segments; i++) {
      const u = i / segments;
      const pt = curve.getPointAt(u % 1.0);
      const tangent = curve.getTangentAt(u % 1.0).normalize();
      const normal = new THREE.Vector3(-tangent.z, 0, tangent.x).normalize();
      samples.push({ pt, tangent, normal });
    }

    // 1. Asphalt Road Surface Ribbon
    const roadPositions = [];
    const roadNormals = [];
    const roadUVs = [];
    const roadIndices = [];

    for (let i = 0; i <= segments; i++) {
      const s = samples[i];
      const pLeft = s.pt.clone().sub(s.normal.clone().multiplyScalar(roadHalfWidth));
      const pRight = s.pt.clone().add(s.normal.clone().multiplyScalar(roadHalfWidth));
      pLeft.y = 0.04;
      pRight.y = 0.04;

      roadPositions.push(pLeft.x, pLeft.y, pLeft.z);
      roadPositions.push(pRight.x, pRight.y, pRight.z);
      roadNormals.push(0, 1, 0, 0, 1, 0);
      roadUVs.push(0, i / 6, 1, i / 6);
    }

    for (let i = 0; i < segments; i++) {
      const v0 = i * 2;
      const v1 = i * 2 + 1;
      const v2 = (i + 1) * 2;
      const v3 = (i + 1) * 2 + 1;
      roadIndices.push(v0, v1, v2);
      roadIndices.push(v1, v3, v2);
    }

    const roadGeo = new THREE.BufferGeometry();
    roadGeo.setAttribute('position', new THREE.Float32BufferAttribute(roadPositions, 3));
    roadGeo.setAttribute('normal', new THREE.Float32BufferAttribute(roadNormals, 3));
    roadGeo.setAttribute('uv', new THREE.Float32BufferAttribute(roadUVs, 2));
    roadGeo.setIndex(roadIndices);
    const roadMesh = new THREE.Mesh(roadGeo, this.materials.asphalt);
    roadMesh.receiveShadow = true;
    group.add(roadMesh);

    // 2. Alternating Red & Blue 3D Rumble Kerbs with Beveled Drop-Down Walls
    const kerbRedPositions = [];
    const kerbBluePositions = [];

    function addKerbSegment(pIn0, pOut0, pIn1, pOut1, isRed, isLeft) {
      const targetPos = isRed ? kerbRedPositions : kerbBluePositions;

      if (isLeft) {
        // Top beveled ramp (Counter-Clockwise)
        targetPos.push(pIn0.x, pIn0.y, pIn0.z, pIn1.x, pIn1.y, pIn1.z, pOut0.x, pOut0.y, pOut0.z);
        targetPos.push(pIn1.x, pIn1.y, pIn1.z, pOut1.x, pOut1.y, pOut1.z, pOut0.x, pOut0.y, pOut0.z);

        // Outer vertical drop wall to sidewalk
        const w0 = pOut0.clone(); w0.y = 0.04;
        const w1 = pOut1.clone(); w1.y = 0.04;
        targetPos.push(pOut0.x, pOut0.y, pOut0.z, pOut1.x, pOut1.y, pOut1.z, w0.x, w0.y, w0.z);
        targetPos.push(pOut1.x, pOut1.y, pOut1.z, w1.x, w1.y, w1.z, w0.x, w0.y, w0.z);
      } else {
        // Right side top beveled ramp (Counter-Clockwise)
        targetPos.push(pIn0.x, pIn0.y, pIn0.z, pOut0.x, pOut0.y, pOut0.z, pIn1.x, pIn1.y, pIn1.z);
        targetPos.push(pOut0.x, pOut0.y, pOut0.z, pOut1.x, pOut1.y, pOut1.z, pIn1.x, pIn1.y, pIn1.z);

        // Outer vertical drop wall to sidewalk
        const w0 = pOut0.clone(); w0.y = 0.04;
        const w1 = pOut1.clone(); w1.y = 0.04;
        targetPos.push(pOut0.x, pOut0.y, pOut0.z, w0.x, w0.y, w0.z, pOut1.x, pOut1.y, pOut1.z);
        targetPos.push(w0.x, w0.y, w0.z, w1.x, w1.y, w1.z, pOut1.x, pOut1.y, pOut1.z);
      }
    }

    for (let i = 0; i < segments; i++) {
      const s0 = samples[i];
      const s1 = samples[i + 1];
      const isRed = (i % 2 === 0);

      // Inner / Left Kerb
      const L0_in = s0.pt.clone().sub(s0.normal.clone().multiplyScalar(roadHalfWidth));
      const L0_out = s0.pt.clone().sub(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const L1_in = s1.pt.clone().sub(s1.normal.clone().multiplyScalar(roadHalfWidth));
      const L1_out = s1.pt.clone().sub(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      L0_in.y = 0.04; L1_in.y = 0.04;
      L0_out.y = 0.18; L1_out.y = 0.18;
      addKerbSegment(L0_in, L0_out, L1_in, L1_out, isRed, true);

      // Outer / Right Kerb
      const R0_in = s0.pt.clone().add(s0.normal.clone().multiplyScalar(roadHalfWidth));
      const R0_out = s0.pt.clone().add(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const R1_in = s1.pt.clone().add(s1.normal.clone().multiplyScalar(roadHalfWidth));
      const R1_out = s1.pt.clone().add(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      R0_in.y = 0.04; R1_in.y = 0.04;
      R0_out.y = 0.18; R1_out.y = 0.18;
      addKerbSegment(R0_in, R0_out, R1_in, R1_out, isRed, false);
    }

    if (kerbRedPositions.length > 0) {
      const redGeo = new THREE.BufferGeometry();
      redGeo.setAttribute('position', new THREE.Float32BufferAttribute(kerbRedPositions, 3));
      redGeo.computeVertexNormals();
      const redMesh = new THREE.Mesh(redGeo, this.materials.kerbRed);
      redMesh.receiveShadow = true;
      redMesh.castShadow = true;
      group.add(redMesh);
    }

    if (kerbBluePositions.length > 0) {
      const blueGeo = new THREE.BufferGeometry();
      blueGeo.setAttribute('position', new THREE.Float32BufferAttribute(kerbBluePositions, 3));
      blueGeo.computeVertexNormals();
      const blueMesh = new THREE.Mesh(blueGeo, this.materials.kerbBlue);
      blueMesh.receiveShadow = true;
      blueMesh.castShadow = true;
      group.add(blueMesh);
    }

    // 3. Paved Sidewalk Ribbons with Diamond Paver Texture
    const swPositions = [];
    const swUVs = [];
    const swIndices = [];
    let swVIdx = 0;

    for (let i = 0; i < segments; i++) {
      const s0 = samples[i];
      const s1 = samples[i + 1];

      // Left Sidewalk
      const L0_in = s0.pt.clone().sub(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const L0_out = s0.pt.clone().sub(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth + sidewalkWidth));
      const L1_in = s1.pt.clone().sub(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const L1_out = s1.pt.clone().sub(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth + sidewalkWidth));
      L0_in.y = 0.15; L0_out.y = 0.13; L1_in.y = 0.15; L1_out.y = 0.13;

      swPositions.push(L0_in.x, L0_in.y, L0_in.z, L0_out.x, L0_out.y, L0_out.z, L1_in.x, L1_in.y, L1_in.z, L1_out.x, L1_out.y, L1_out.z);
      swUVs.push(0, i * 0.4, 1, i * 0.4, 0, (i + 1) * 0.4, 1, (i + 1) * 0.4);
      // Counter-Clockwise face winding for Left
      swIndices.push(swVIdx, swVIdx + 2, swVIdx + 1, swVIdx + 1, swVIdx + 2, swVIdx + 3);
      swVIdx += 4;

      // Right Sidewalk
      const R0_in = s0.pt.clone().add(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const R0_out = s0.pt.clone().add(s0.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth + sidewalkWidth));
      const R1_in = s1.pt.clone().add(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth));
      const R1_out = s1.pt.clone().add(s1.normal.clone().multiplyScalar(roadHalfWidth + kerbWidth + sidewalkWidth));
      R0_in.y = 0.15; R0_out.y = 0.13; R1_in.y = 0.15; R1_out.y = 0.13;

      swPositions.push(R0_in.x, R0_in.y, R0_in.z, R0_out.x, R0_out.y, R0_out.z, R1_in.x, R1_in.y, R1_in.z, R1_out.x, R1_out.y, R1_out.z);
      swUVs.push(0, i * 0.4, 1, i * 0.4, 0, (i + 1) * 0.4, 1, (i + 1) * 0.4);
      // Counter-Clockwise face winding for Right
      swIndices.push(swVIdx, swVIdx + 1, swVIdx + 2, swVIdx + 1, swVIdx + 3, swVIdx + 2);
      swVIdx += 4;
    }

    const swGeo = new THREE.BufferGeometry();
    swGeo.setAttribute('position', new THREE.Float32BufferAttribute(swPositions, 3));
    swGeo.setAttribute('uv', new THREE.Float32BufferAttribute(swUVs, 2));
    swGeo.setIndex(swIndices);
    swGeo.computeVertexNormals();
    const swMesh = new THREE.Mesh(swGeo, this.materials.sidewalk);
    swMesh.receiveShadow = true;
    group.add(swMesh);

    // 4. Authentic 3D Traffic Safety Barrels / Drums
    const barrelIndices = [6, 16, 28, 42, 54, 68, 80];
    barrelIndices.forEach(idx => {
      const s = samples[idx % segments];
      const side = (idx % 2 === 0) ? -1 : 1;
      const bPos = s.pt.clone().add(s.normal.clone().multiplyScalar(side * (roadHalfWidth + kerbWidth + 0.9)));
      bPos.y = 0.58;

      const barrelGroup = new THREE.Group();
      // Blue Body
      const bodyMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.44, 1.15, 18), this.materials.barrelBlue);
      bodyMesh.castShadow = true;
      bodyMesh.receiveShadow = true;
      barrelGroup.add(bodyMesh);

      // Two White Reflective Stripes
      const stripeGeo = new THREE.CylinderGeometry(0.43, 0.43, 0.16, 18);
      const stripe1 = new THREE.Mesh(stripeGeo, this.materials.barrelWhite);
      stripe1.position.y = 0.22;
      barrelGroup.add(stripe1);

      const stripe2 = new THREE.Mesh(stripeGeo, this.materials.barrelWhite);
      stripe2.position.y = -0.18;
      barrelGroup.add(stripe2);

      // Dark Top Lid & Handle Loop
      const lid = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.42, 0.08, 18), this.materials.barrelLid);
      lid.position.y = 0.58;
      barrelGroup.add(lid);

      const handle = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.028, 8, 16, Math.PI), this.materials.barrelLid);
      handle.position.y = 0.62;
      handle.rotation.x = Math.PI / 2;
      barrelGroup.add(handle);

      barrelGroup.position.copy(bPos);
      group.add(barrelGroup);

      // Cannon Physical Body with real crash dynamics
      const barrelBody = new CANNON.Body({ mass: 3.5, material: this.physics.materials.obstacle });
      barrelBody.addShape(new CANNON.Cylinder(0.44, 0.44, 1.15, 12));
      barrelBody.position.set(bPos.x, bPos.y, bPos.z);
      barrelBody.addEventListener('collide', () => {
        if (this.audio) this.audio.playHit(1.2);
      });
      this.physics.addDynamicBody(barrelBody, barrelGroup);
      bodies.push(barrelBody);
    });

    // 5. Low-Poly Trees along Track Borders
    const treeIndices = [3, 12, 22, 33, 47, 59, 71, 84, 92];
    treeIndices.forEach((idx, tIdx) => {
      const s = samples[idx % segments];
      const side = (tIdx % 2 === 0) ? -1 : 1;
      const tPos = s.pt.clone().add(s.normal.clone().multiplyScalar(side * (roadHalfWidth + kerbWidth + sidewalkWidth + 2.5)));
      tPos.y = 0;

      const treeGroup = new THREE.Group();
      // Trunk
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.32, 2.4, 7), this.materials.treeTrunk);
      trunk.position.y = 1.2;
      trunk.castShadow = true;
      treeGroup.add(trunk);

      // Faceted Canopy
      const canopy = new THREE.Mesh(new THREE.IcosahedronGeometry(1.6 + (tIdx % 3) * 0.25, 1), this.materials.foliage);
      canopy.position.y = 2.9 + (tIdx % 2) * 0.3;
      canopy.rotation.y = tIdx * 0.8;
      canopy.castShadow = true;
      canopy.receiveShadow = true;
      treeGroup.add(canopy);

      treeGroup.position.copy(tPos);
      group.add(treeGroup);
    });

    // 6. Stylized Grass Clumps Lining Both Track Sides (Matching Bruno Simon)
    for (let i = 0; i < segments; i++) {
      const s = samples[i];
      [-1, 1].forEach((side, sIdx) => {
        // Skip some segments randomly for organic rhythm
        if ((i + sIdx) % 3 === 0) return;
        const offset = roadHalfWidth + kerbWidth + sidewalkWidth + 0.35 + ((i * 7) % 5) * 0.15;
        const gPos = s.pt.clone().add(s.normal.clone().multiplyScalar(side * offset));

        const tuftGroup = new THREE.Group();
        const bladeCount = 4 + (i % 3);
        for (let b = 0; b < bladeCount; b++) {
          const bladeMat = (b % 2 === 0) ? this.materials.grass : this.materials.grassTip;
          const bladeH = 0.65 + ((b + i) % 4) * 0.12;
          const blade = new THREE.Mesh(new THREE.ConeGeometry(0.09, bladeH, 3), bladeMat);
          const fanAngle = ((b / (bladeCount - 1)) - 0.5) * 0.8;
          blade.position.set(Math.sin(fanAngle) * 0.22, bladeH / 2, Math.cos(fanAngle) * 0.08);
          blade.rotation.z = -fanAngle * 0.7;
          blade.rotation.y = (b * 1.1 + i * 0.4);
          blade.castShadow = true;
          tuftGroup.add(blade);
        }
        tuftGroup.position.set(gPos.x, 0.08, gPos.z);
        group.add(tuftGroup);
      });
    }

    // 7. Subtle Aerial Wind Streamers Floating Elegantly along the Outer Bend
    const ribbonConfigs = [
      { startIdx: 2, endIdx: 32, height: 1.6, speed: 1.2, side: 1, latOffset: 2.2 },
      { startIdx: 8, endIdx: 36, height: 2.4, speed: 1.6, side: 1, latOffset: 3.5 }
    ];

    ribbonConfigs.forEach((cfg) => {
      const pts = [];
      for (let i = cfg.startIdx; i <= cfg.endIdx; i++) {
        const s = samples[i % segments];
        const lateral = cfg.side * (roadHalfWidth + kerbWidth + sidewalkWidth + cfg.latOffset) + Math.sin(i * 0.35) * 1.2;
        const p = s.pt.clone().add(s.normal.clone().multiplyScalar(lateral));
        p.y = cfg.height + Math.sin(i * 0.25) * 0.45;
        pts.push(p);
      }
      const rCurve = new THREE.CatmullRomCurve3(pts);
      const rGeo = new THREE.TubeGeometry(rCurve, 28, 0.025, 4, false);
      const rMesh = new THREE.Mesh(rGeo, this.materials.windRibbon);
      group.add(rMesh);
      this.windRibbons.push({ mesh: rMesh, basePoints: pts, speed: cfg.speed });
    });

    // 8. Scattered Track Debris & Flakes Across Road and Sidewalk
    const debrisGeo = new THREE.PlaneGeometry(0.20, 0.20);
    debrisGeo.rotateX(-Math.PI / 2);
    for (let i = 0; i < 140; i++) {
      const s = samples[(i * 3 + 1) % segments];
      const side = (i % 2 === 0) ? -1 : 1;
      const spread = (i % 3 === 0) 
        ? ((i * 13) % 9) * 0.6 // On asphalt
        : (roadHalfWidth + kerbWidth * 0.5 + ((i * 7) % 6) * 0.6); // Along kerb/sidewalk
      const pos = s.pt.clone().add(s.normal.clone().multiplyScalar(side * spread));
      pos.y = 0.05 + ((i % 5) * 0.03);

      const dMesh = new THREE.Mesh(debrisGeo, this.materials.debris);
      dMesh.position.copy(pos);
      dMesh.rotation.y = (i * 1.83) % Math.PI;
      group.add(dMesh);
    }
  }

  // --- DISTRICT 2: MEGA STUNT PARK ---
  buildDistrictStuntPark(group, bodies, wx, wz) {
    // Giant Mega-Launch Ramp
    this.createRamp(group, bodies, wx, 0, wz - 35, 16, 6.5, 24, 0);

    // Elevated Skyway Landing Platform
    const platW = 28, platL = 38, platH = 7.0;
    const platMesh = new THREE.Mesh(new THREE.BoxGeometry(platW, 0.8, platL), this.materials.rampMat);
    platMesh.position.set(wx, platH, wz + 15);
    platMesh.castShadow = true;
    platMesh.receiveShadow = true;
    group.add(platMesh);

    const platBody = new CANNON.Body({ mass: 0 });
    platBody.addShape(new CANNON.Box(new CANNON.Vec3(platW / 2, 0.4, platL / 2)));
    platBody.position.set(wx, platH, wz + 15);
    this.physics.world.addBody(platBody);
    bodies.push(platBody);

    // Exit Down-Ramp
    this.createRamp(group, bodies, wx, platH, wz + 40, 16, -platH, 20, 0);

    // Quarter-Pipe Curved Wall-Ride (Constructed from angled segments)
    const curveRadius = 22;
    for (let a = 0; a < 6; a++) {
      const angle = (a / 5) * (Math.PI / 2);
      const y = Math.sin(angle) * curveRadius * 0.4;
      const x = wx - 42 + Math.cos(angle) * 6;
      const z = wz + (a - 3) * 6;
      this.createRamp(group, bodies, x, y, z, 12, 1.5, 6, Math.PI / 2);
    }
  }

  // --- DISTRICT 3: DOMINO CANYON ---
  buildDistrictDominoCanyon(group, bodies, wx, wz) {
    // 40+ Giant Physics Domino Slabs
    const dW = 1.2, dH = 3.6, dD = 0.4;
    const dominoGeo = new THREE.BoxGeometry(dW, dH, dD);
    const dominoMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.3,
      metalness: 0.7
    });

    const dominoCount = 36;
    for (let i = 0; i < dominoCount; i++) {
      const angle = (i / dominoCount) * Math.PI * 1.5;
      const r = 24 + (i * 0.4);
      const x = wx + Math.cos(angle) * r;
      const z = wz + Math.sin(angle) * r;

      const mesh = new THREE.Mesh(dominoGeo, dominoMat);
      mesh.castShadow = true;
      group.add(mesh);

      const body = new CANNON.Body({ mass: 14, material: this.physics.materials.obstacle });
      body.addShape(new CANNON.Box(new CANNON.Vec3(dW / 2, dH / 2, dD / 2)));
      body.position.set(x, dH / 2 + 0.1, z);
      body.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 1, 0), -angle);

      this.physics.addDynamicBody(body, mesh);
      bodies.push(body);
    }

    // Stacked Cargo Crates Pyramid
    for (let y = 0; y < 4; y++) {
      const count = 4 - y;
      for (let i = 0; i < count; i++) {
        const s = 1.6;
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(s, s, s), this.materials.crateMat);
        mesh.castShadow = true;
        group.add(mesh);

        const body = new CANNON.Body({ mass: 12, material: this.physics.materials.obstacle });
        body.addShape(new CANNON.Box(new CANNON.Vec3(s / 2, s / 2, s / 2)));
        body.position.set(wx - 10 + i * (s + 0.2), y * s + s / 2 + 0.1, wz - 15);
        this.physics.addDynamicBody(body, mesh);
        bodies.push(body);
      }
    }
  }

  // --- DISTRICT 4: SPEEDWAY & NITRO BOOST HIGHWAY ---
  buildDistrictSpeedway(group, bodies, wx, wz) {
    // Banked Turn Loop Track
    const roadW = 18;
    const loopGeo = new THREE.RingGeometry(25, 25 + roadW, 32);
    loopGeo.rotateX(-Math.PI / 2);
    const loopMesh = new THREE.Mesh(loopGeo, this.materials.road);
    loopMesh.position.set(wx, 0.08, wz);
    group.add(loopMesh);

    // Ground Speed Booster Strips
    [-20, 0, 20].forEach(offsetZ => {
      const boostMesh = new THREE.Mesh(new THREE.PlaneGeometry(8, 4), this.materials.accentLime);
      boostMesh.rotation.x = -Math.PI / 2;
      boostMesh.position.set(wx, 0.1, wz + offsetZ);
      group.add(boostMesh);

      const boostBody = new CANNON.Body({ mass: 0 });
      boostBody.addShape(new CANNON.Box(new CANNON.Vec3(4, 0.2, 2)));
      boostBody.position.set(wx, 0.1, wz + offsetZ);

      // Boost impulse on car touch
      boostBody.addEventListener('collide', (e) => {
        if (e.body === window.vehicleController?.chassisBody) {
          window.vehicleController.activateNitro();
        }
      });
      this.physics.world.addBody(boostBody);
      bodies.push(boostBody);
    });
  }

  // --- DISTRICT 5: PINBALL & BOUNCERS ---
  buildDistrictPinball(group, bodies, wx, wz) {
    const bumperLocations = [
      { x: wx - 18, z: wz - 12 },
      { x: wx + 18, z: wz - 12 },
      { x: wx, z: wz + 16 }
    ];

    bumperLocations.forEach(loc => {
      const bGroup = new THREE.Group();
      const base = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.2, 1.4, 24), this.materials.monolithBlock);
      bGroup.add(base);
      const ring = new THREE.Mesh(new THREE.CylinderGeometry(2.02, 2.22, 0.3, 24), this.materials.accentLime);
      ring.position.y = 0.3;
      bGroup.add(ring);
      bGroup.position.set(loc.x, 0.7, loc.z);
      group.add(bGroup);

      const body = new CANNON.Body({ mass: 0 });
      body.addShape(new CANNON.Cylinder(2.0, 2.2, 1.4, 16));
      body.position.set(loc.x, 0.7, loc.z);

      body.addEventListener('collide', (e) => {
        if (e.body === window.vehicleController?.chassisBody) {
          if (this.audio) this.audio.playHop();
          const dir = window.vehicleController.chassisBody.position.vsub(body.position);
          dir.y = 0.3;
          dir.normalize();
          window.vehicleController.chassisBody.applyImpulse(dir.scale(5500), window.vehicleController.chassisBody.position);
        }
      });

      this.physics.world.addBody(body);
      bodies.push(body);
    });
  }

  // --- PROCEDURAL ENDLESS CHUNKS ---
  buildProceduralEndlessChunk(group, bodies, wx, wz, cx, cz) {
    // Random procedural layout based on chunk coordinates hash
    const seed = Math.abs(Math.sin(cx * 12.9898 + cz * 78.233) * 43758.5453);
    const rampCount = Math.floor(seed % 3);

    for (let r = 0; r < rampCount; r++) {
      const rx = wx + ((seed * (r + 1) * 17) % 60) - 30;
      const rz = wz + ((seed * (r + 1) * 31) % 60) - 30;
      const rH = 2.0 + (seed % 3);
      this.createRamp(group, bodies, rx, 0, rz, 7, rH, 8, (seed * r) % Math.PI);
    }
  }

  createRamp(group, bodies, x, y, z, w, h, l, rotY) {
    const angle = Math.atan2(h, l);
    const rampGeo = new THREE.BoxGeometry(w, 0.4, l);
    const mesh = new THREE.Mesh(rampGeo, this.materials.rampMat);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.position.set(x, y + Math.abs(h) / 2, z);
    mesh.rotation.y = rotY;
    mesh.rotation.x = angle;
    group.add(mesh);

    const rampBody = new CANNON.Body({ mass: 0 });
    rampBody.addShape(new CANNON.Box(new CANNON.Vec3(w / 2, 0.2, l / 2)));
    rampBody.position.set(x, y + Math.abs(h) / 2, z);
    rampBody.quaternion.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), angle);
    this.physics.world.addBody(rampBody);
    bodies.push(rampBody);
  }

  // --- UPDATE ANIMATIONS & FLAG PICKUPS ---
  update(delta, carPos) {
    // Animate Rotating Holographic Flags & Check Pickups
    const now = performance.now() * 0.002;
    this.flagMeshes.forEach(item => {
      if (item.flag.collected) return;

      item.group.rotation.y = now * 1.5;
      item.ring.rotation.z = -now * 2.0;
      item.group.position.y = item.flag.pos.y + Math.sin(now * 3) * 0.2;

      // Pickup Distance Check
      const dist = item.group.position.distanceTo(carPos);
      if (dist < 3.8) {
        this.collectFlag(item);
      }
    });

    // Animate EMP Shockwave Ring
    if (this.empRingState.active) {
      this.empRingState.radius += delta * 45;
      this.empRingState.alpha -= delta * 1.5;
      const s = this.empRingState.radius;
      this.empRing.scale.set(s, s, s);
      this.empRing.material.opacity = Math.max(0, this.empRingState.alpha);

      if (this.empRingState.radius >= this.empRingState.maxRadius || this.empRingState.alpha <= 0) {
        this.empRingState.active = false;
        this.empRing.material.opacity = 0;
      }
    }

    // Animate Flowing Cyan Wind Ribbons
    const time = performance.now() * 0.0015;
    this.windRibbons.forEach((r, idx) => {
      if (r.mesh) {
        r.mesh.position.y = Math.sin(time * r.speed + idx) * 0.35;
        r.mesh.rotation.y = Math.sin(time * 0.8 + idx) * 0.05;
      }
    });
  }

  collectFlag(flagItem) {
    flagItem.flag.collected = true;
    this.collectedCount++;
    flagItem.group.visible = false;

    if (this.audio) this.audio.playFlagPickup();

    // Trigger Cyber Toast UI
    if (window.showFlagToast) {
      window.showFlagToast(flagItem.flag.text, this.collectedCount, this.flags.length);
    }
  }
}

window.WorldManager = WorldManager;
