/**
 * SecLeaf Sector 404: Physics Engine
 * High-performance Cannon.js physics setup with strategic body sleeping,
 * custom materials, and impact listeners.
 */

class PhysicsEngine {
  constructor() {
    this.world = new CANNON.World();
    this.world.gravity.set(0, -22, 0);
    this.world.broadphase = new CANNON.SAPBroadphase(this.world);
    this.world.allowSleep = true;
    this.world.defaultContactMaterial.friction = 0.4;
    this.world.defaultContactMaterial.restitution = 0.2;

    // Contact Materials
    this.materials = {
      ground: new CANNON.Material('ground'),
      wheel: new CANNON.Material('wheel'),
      chassis: new CANNON.Material('chassis'),
      obstacle: new CANNON.Material('obstacle'),
      bumper: new CANNON.Material('bumper'),
      boost: new CANNON.Material('boost')
    };

    // Wheel <-> Ground Contact
    const wheelGroundContact = new CANNON.ContactMaterial(
      this.materials.wheel,
      this.materials.ground,
      {
        friction: 0.65,
        restitution: 0.05,
        contactEquationStiffness: 1000
      }
    );
    this.world.addContactMaterial(wheelGroundContact);

    // Obstacle <-> Ground
    const obstacleGroundContact = new CANNON.ContactMaterial(
      this.materials.obstacle,
      this.materials.ground,
      {
        friction: 0.45,
        restitution: 0.3
      }
    );
    this.world.addContactMaterial(obstacleGroundContact);

    // Obstacle <-> Chassis
    const obstacleChassisContact = new CANNON.ContactMaterial(
      this.materials.obstacle,
      this.materials.chassis,
      {
        friction: 0.3,
        restitution: 0.4
      }
    );
    this.world.addContactMaterial(obstacleChassisContact);

    // Setup Main Ground Body
    this.groundBody = new CANNON.Body({
      mass: 0,
      material: this.materials.ground
    });
    this.groundBody.addShape(new CANNON.Plane());
    this.groundBody.quaternion.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI / 2);
    this.world.addBody(this.groundBody);

    this.dynamicBodies = [];
  }

  step(delta) {
    this.world.step(1 / 60, Math.min(delta, 0.05), 3);
  }

  addDynamicBody(body, mesh, isSmasheable = true) {
    this.world.addBody(body);
    this.dynamicBodies.push({ body, mesh, isSmasheable });

    if (isSmasheable) {
      body.addEventListener('collide', (e) => {
        const impact = e.contact.getImpactVelocityAlongNormal();
        if (impact > 2.0 && window.soundEngine) {
          window.soundEngine.playCrash(impact / 12);
        }
      });
    }
  }

  updateVisuals() {
    for (let i = 0; i < this.dynamicBodies.length; i++) {
      const item = this.dynamicBodies[i];
      if (item.mesh && item.body) {
        item.mesh.position.copy(item.body.position);
        item.mesh.quaternion.copy(item.body.quaternion);
      }
    }
  }
}

window.physicsEngine = new PhysicsEngine();
