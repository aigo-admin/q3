import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. ADD CSS FOR 3D SPLIT-FLAP TUMBLERS, DIGIT SLIDE, AND TRAILER REVEAL
new_css = '''
    /* ================= 1. TRAILER-STYLE TITLE REVEAL (KINETIC ENTRANCE) ================= */
    .cinematic-headline {
      font-family: var(--font-display);
      font-size: clamp(42px, 6.5vw, 84px);
      font-weight: 700;
      line-height: 1.05;
      color: #ffffff;
      margin-bottom: 20px;
      text-transform: uppercase;
      will-change: transform, filter, letter-spacing, opacity;
      opacity: 0;
      filter: blur(32px);
      letter-spacing: 0.55em;
      transform: scale(1.14) translateY(-6px);
      animation: trailerTitleReveal 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s;
    }

    .cinematic-headline span {
      color: var(--accent);
      text-shadow: 0 0 35px rgba(186, 236, 67, 0.45);
    }

    @keyframes trailerTitleReveal {
      0% {
        opacity: 0;
        filter: blur(32px);
        letter-spacing: 0.55em;
        transform: scale(1.14) translateY(-6px);
      }
      35% {
        opacity: 0.6;
        filter: blur(16px);
      }
      80% {
        filter: blur(2px);
      }
      100% {
        opacity: 1;
        filter: blur(0px);
        letter-spacing: -0.035em;
        transform: scale(1) translateY(0);
      }
    }

    .date-hero {
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      margin-bottom: 48px;
      opacity: 0;
      transform: translateY(16px);
      animation: heroFadeIn 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.8s;
    }

    @keyframes heroFadeIn {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* ================= 2. EXTRUDED 3D SPLIT-FLAP COUNTER TUMBLERS ================= */
    .countdown-monolith {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: clamp(14px, 2.2vw, 32px);
      margin: 0 auto 36px;
      flex-wrap: wrap;
      max-width: 1400px;
      perspective: 1400px;
    }

    .countdown-unit-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: clamp(115px, 16.5vw, 225px);
      padding: clamp(22px, 3vw, 40px) clamp(14px, 2vw, 28px);
      background: linear-gradient(180deg, #161b26 0%, #0d1017 50%, #080a0f 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      /* Extruded physical bevel & 3D shadow depth */
      box-shadow: 
        0 2px 0 rgba(255, 255, 255, 0.1) inset,
        0 -2px 0 rgba(0, 0, 0, 0.8) inset,
        0 12px 0 #06070a,
        0 14px 2px rgba(0, 0, 0, 0.6),
        0 30px 60px rgba(0, 0, 0, 0.85);
      position: relative;
      transform-style: preserve-3d;
      will-change: transform, box-shadow;
      transition: border-color 0.3s ease, transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      opacity: 0;
      transform: translateY(30px) rotateX(15deg);
      animation: cardStaggerDrop 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .countdown-unit-card:nth-child(1) { animation-delay: 0.9s; }
    .countdown-unit-card:nth-child(2) { animation-delay: 1.0s; }
    .countdown-unit-card:nth-child(3) { animation-delay: 1.1s; }
    .countdown-unit-card:nth-child(4) { animation-delay: 1.2s; }
    .countdown-unit-card:nth-child(5) { animation-delay: 1.3s; }

    @keyframes cardStaggerDrop {
      to {
        opacity: 1;
        transform: translateY(0) rotateX(0deg);
      }
    }

    .countdown-unit-card:hover {
      border-color: rgba(255, 255, 255, 0.22);
      transform: translateY(-4px) scale(1.015);
    }

    .countdown-unit-card.accent-card {
      border-color: rgba(186, 236, 67, 0.38);
      background: linear-gradient(180deg, #1b232f 0%, #10151f 50%, #090c12 100%);
      box-shadow: 
        0 2px 0 rgba(186, 236, 67, 0.3) inset,
        0 -2px 0 rgba(0, 0, 0, 0.8) inset,
        0 12px 0 #070a0e,
        0 14px 2px rgba(0, 0, 0, 0.6),
        0 30px 65px rgba(0, 0, 0, 0.9),
        0 0 45px rgba(186, 236, 67, 0.12);
    }

    /* MECHANICAL SPLIT-FLAP CREASE / HINGE */
    .tumbler-chassis {
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      border-radius: 14px;
      perspective: 800px;
    }

    .tumbler-chassis::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      top: 50%;
      height: 2px;
      background: rgba(0, 0, 0, 0.95);
      box-shadow: 0 1px 0 rgba(255, 255, 255, 0.08), 0 -1px 0 rgba(0, 0, 0, 0.8);
      z-index: 10;
      pointer-events: none;
    }

    /* MECHANICAL SIDE PINS / RIVETS */
    .tumbler-chassis::before {
      content: '';
      position: absolute;
      top: calc(50% - 4px);
      left: 4px;
      width: 8px;
      height: 8px;
      background: #252d3d;
      border-radius: 50%;
      box-shadow: 
        calc(100% - 16px) 0 0 #252d3d,
        0 1px 0 rgba(255,255,255,0.1),
        inset 0 1px 2px rgba(0,0,0,0.8);
      z-index: 12;
      pointer-events: none;
    }

    /* ================= 3. SMOOTH DIGIT SLIDE & 3D TUMBLER MORPHING ================= */
    .tumbler-box {
      position: relative;
      height: clamp(68px, 11vw, 150px);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      width: 100%;
    }

    .digit-strip {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
    }

    .big-number {
      font-family: var(--font-display);
      font-size: clamp(64px, 10vw, 146px);
      font-weight: 700;
      color: #ffffff;
      line-height: 1;
      letter-spacing: -0.04em;
      font-variant-numeric: tabular-nums;
      text-shadow: 0 4px 25px rgba(0, 0, 0, 0.85);
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      will-change: transform, opacity, filter;
      transition: transform 0.38s cubic-bezier(0.175, 0.885, 0.32, 1.2), 
                  opacity 0.28s ease, 
                  filter 0.28s ease;
    }

    .accent-card .big-number {
      color: var(--accent);
      text-shadow: 0 0 45px rgba(186, 236, 67, 0.45);
    }

    /* DIGIT TRANSITION STATES WITH VERTICAL MOTION BLUR & ELASTIC SETTLE */
    .big-number.digit-leaving {
      transform: translateY(-90%) rotateX(-35deg) scale(0.92);
      opacity: 0;
      filter: blur(4px);
    }

    .big-number.digit-incoming {
      transform: translateY(90%) rotateX(35deg) scale(0.92);
      opacity: 0;
      filter: blur(4px);
    }

    .big-number.digit-active {
      transform: translateY(0) rotateX(0deg) scale(1);
      opacity: 1;
      filter: blur(0px);
    }

    /* AUDIO SUBWOOFER PULSE ON CARDS */
    .countdown-unit-card.heartbeat-pulse {
      animation: subPulse 0.42s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes subPulse {
      0% {
        transform: translateY(-2px) scale(1.028);
        border-color: rgba(186, 236, 67, 0.7);
        box-shadow: 
          0 2px 0 rgba(186, 236, 67, 0.5) inset,
          0 12px 0 #070a0e,
          0 35px 75px rgba(0, 0, 0, 0.95),
          0 0 55px rgba(186, 236, 67, 0.28);
      }
      100% {
        transform: translateY(0) scale(1);
        border-color: rgba(186, 236, 67, 0.38);
      }
    }
'''

# Replace old headline and countdown CSS
html = re.sub(r'\.cinematic-headline\s*\{[^}]*\}', '', html)
html = re.sub(r'\.cinematic-headline span\s*\{[^}]*\}', '', html)
html = re.sub(r'\.countdown-monolith\s*\{[^}]*\}', '', html)
html = re.sub(r'\.countdown-unit-card\s*\{[^}]*\}', '', html)
html = re.sub(r'\.countdown-unit-card:hover\s*\{[^}]*\}', '', html)
html = re.sub(r'\.countdown-unit-card\.accent-card\s*\{[^}]*\}', '', html)
html = re.sub(r'\.big-number\s*\{[^}]*\}', '', html)
html = re.sub(r'\.accent-card \.big-number\s*\{[^}]*\}', '', html)

# Insert the new CSS right before </style>
html = html.replace('</style>', new_css + '\n  </style>')

# 2. UPDATE THE COUNTDOWN CARD HTML STRUCTURE WITH TUMBLER CHASSIS
old_countdown_html = '''      <!-- BIG COUNTDOWN MONOLITH: MONTHS, DAYS, HOURS, MINUTES, SECONDS -->
      <div class="countdown-monolith">
        <!-- MONTHS -->
        <div class="countdown-unit-card accent-card">
          <div class="big-number" id="numMonths">--</div>
          <div class="unit-label">Months</div>
        </div>

        <!-- DAYS -->
        <div class="countdown-unit-card">
          <div class="big-number" id="numDays">--</div>
          <div class="unit-label">Days</div>
        </div>

        <!-- HOURS -->
        <div class="countdown-unit-card">
          <div class="big-number" id="numHours">--</div>
          <div class="unit-label">Hours</div>
        </div>

        <!-- MINUTES -->
        <div class="countdown-unit-card">
          <div class="big-number" id="numMinutes">--</div>
          <div class="unit-label">Minutes</div>
        </div>

        <!-- SECONDS -->
        <div class="countdown-unit-card accent-card">
          <div class="big-number" id="numSeconds">--</div>
          <div class="unit-label">Seconds</div>
        </div>
      </div>'''

new_countdown_html = '''      <!-- EXTRUDED 3D SPLIT-FLAP COUNTDOWN MONOLITH -->
      <div class="countdown-monolith">
        <!-- MONTHS -->
        <div class="countdown-unit-card accent-card" id="card-months">
          <div class="tumbler-chassis">
            <div class="tumbler-box" id="box-months">
              <div class="big-number digit-active" id="numMonths">--</div>
            </div>
          </div>
          <div class="unit-label">Months</div>
        </div>

        <!-- DAYS -->
        <div class="countdown-unit-card" id="card-days">
          <div class="tumbler-chassis">
            <div class="tumbler-box" id="box-days">
              <div class="big-number digit-active" id="numDays">--</div>
            </div>
          </div>
          <div class="unit-label">Days</div>
        </div>

        <!-- HOURS -->
        <div class="countdown-unit-card" id="card-hours">
          <div class="tumbler-chassis">
            <div class="tumbler-box" id="box-hours">
              <div class="big-number digit-active" id="numHours">--</div>
            </div>
          </div>
          <div class="unit-label">Hours</div>
        </div>

        <!-- MINUTES -->
        <div class="countdown-unit-card" id="card-minutes">
          <div class="tumbler-chassis">
            <div class="tumbler-box" id="box-minutes">
              <div class="big-number digit-active" id="numMinutes">--</div>
            </div>
          </div>
          <div class="unit-label">Minutes</div>
        </div>

        <!-- SECONDS -->
        <div class="countdown-unit-card accent-card" id="card-seconds">
          <div class="tumbler-chassis">
            <div class="tumbler-box" id="box-seconds">
              <div class="big-number digit-active" id="numSeconds">--</div>
            </div>
          </div>
          <div class="unit-label">Seconds</div>
        </div>
      </div>'''

html = html.replace(old_countdown_html, new_countdown_html)

# 3. UPGRADE PARTICLES ENGINE TO 3D HYPERSPACE TUNNEL WITH AUDIO WARP-DRIVE PULSE
old_particles_regex = r'// ================= CINEMATIC AMBIENT PARTICLES.*?updateCountdown\(\);'

new_particles_and_countdown_engine = '''// ================= 3D HYPERSPACE PARTICLE TUNNEL & WARP DRIVE ENGINE =================
    var warpSpeed = 2.2;
    var baseWarpSpeed = 2.2;
    var targetWarpSpeed = 2.2;
    var mouseX = 0, mouseY = 0;
    var targetMouseX = 0, targetMouseY = 0;

    (function initHyperspaceTunnel(){
      var canvas = $('ambientCanvas');
      var ctx = canvas.getContext('2d');
      var w, h, cx, cy;
      var stars = [];
      var count = 1400; // Deep 3D star field
      var fov = 340;

      function resize(){
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
        cx = w / 2;
        cy = h / 2;
      }
      window.addEventListener('resize', resize);
      resize();

      window.addEventListener('mousemove', function(e){
        targetMouseX = (e.clientX - cx) * 0.18;
        targetMouseY = (e.clientY - cy) * 0.18;
      });

      for (var i = 0; i < count; i++){
        stars.push({
          x: (Math.random() - 0.5) * 2600,
          y: (Math.random() - 0.5) * 2600,
          z: Math.random() * 1900 + 1,
          pz: 0,
          r: Math.random() * 1.5 + 0.4,
          type: Math.random() < 0.28 ? 'lime' : Math.random() < 0.15 ? 'cyan' : 'white'
        });
      }

      function loop(){
        // Smooth camera drift with mouse
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        // Smooth warp speed decay back to base speed
        warpSpeed += (targetWarpSpeed - warpSpeed) * 0.08;
        if (targetWarpSpeed > baseWarpSpeed) {
          targetWarpSpeed += (baseWarpSpeed - targetWarpSpeed) * 0.04;
        }

        ctx.clearRect(0, 0, w, h);

        var curCx = cx + mouseX;
        var curCy = cy + mouseY;

        for (var i = 0; i < stars.length; i++){
          var s = stars[i];
          s.pz = s.z;
          s.z -= warpSpeed;

          // Recycle stars passing the viewer
          if (s.z <= 1){
            s.z = 1900;
            s.pz = s.z;
            s.x = (Math.random() - 0.5) * 2600;
            s.y = (Math.random() - 0.5) * 2600;
          }

          var k = fov / s.z;
          var px = s.x * k + curCx;
          var py = s.y * k + curCy;

          if (px < -40 || px > w + 40 || py < -40 || py > h + 40) continue;

          var pk = fov / s.pz;
          var prevX = s.x * pk + curCx;
          var prevY = s.y * pk + curCy;

          var alpha = Math.min(1, Math.max(0.15, (1 - s.z / 1900) * 1.2));
          var size = Math.max(0.6, (1 - s.z / 1900) * s.r * 2.8);

          ctx.beginPath();
          if (warpSpeed > 3.5){
            // High speed warp light streak
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(px, py);
            ctx.lineWidth = size * 1.2;
            if (s.type === 'lime'){
              ctx.strokeStyle = 'rgba(186, 236, 67, ' + (alpha * 0.85) + ')';
            } else if (s.type === 'cyan'){
              ctx.strokeStyle = 'rgba(29, 225, 243, ' + (alpha * 0.65) + ')';
            } else {
              ctx.strokeStyle = 'rgba(255, 255, 255, ' + (alpha * 0.75) + ')';
            }
            ctx.stroke();
          } else {
            // Normal 3D starlight particle
            ctx.arc(px, py, size, 0, Math.PI * 2);
            if (s.type === 'lime'){
              ctx.fillStyle = 'rgba(186, 236, 67, ' + alpha + ')';
            } else if (s.type === 'cyan'){
              ctx.fillStyle = 'rgba(29, 225, 243, ' + (alpha * 0.8) + ')';
            } else {
              ctx.fillStyle = 'rgba(240, 245, 255, ' + alpha + ')';
            }
            ctx.fill();
          }
        }

        requestAnimationFrame(loop);
      }
      loop();
    })();

    // Function to trigger a warp pulse on audio heartbeat thump
    function triggerWarpPulse(){
      targetWarpSpeed = 10.5;
      var secCard = $('card-seconds');
      if (secCard){
        secCard.classList.remove('heartbeat-pulse');
        void secCard.offsetWidth; // Force reflow
        secCard.classList.add('heartbeat-pulse');
      }
    }

    // ================= 4. SMOOTH DIGIT SLIDE & FLIP MECHANISM =================
    var currentValues = { months: '', days: '', hours: '', minutes: '', seconds: '' };

    function updateTumbler(unitId, cardId, boxId, newVal){
      var box = $(boxId);
      if (!box) return;

      var oldVal = currentValues[unitId];
      if (oldVal === newVal) return;
      currentValues[unitId] = newVal;

      if (!oldVal || oldVal === '--'){
        box.innerHTML = '<div class="big-number digit-active">' + newVal + '</div>';
        return;
      }

      var currentEl = box.querySelector('.digit-active');
      if (currentEl){
        currentEl.classList.remove('digit-active');
        currentEl.classList.add('digit-leaving');
        setTimeout(function(){ if (currentEl.parentNode) currentEl.remove(); }, 400);
      }

      var newEl = document.createElement('div');
      newEl.className = 'big-number digit-incoming';
      newEl.textContent = newVal;
      box.appendChild(newEl);

      // Trigger 3D drop-down slide with elastic settle
      requestAnimationFrame(function(){
        newEl.classList.remove('digit-incoming');
        newEl.classList.add('digit-active');
      });
    }

    function updateCountdown(){'''

html = re.sub(old_particles_regex, new_particles_and_countdown_engine, html, flags=re.DOTALL)

# Update the display calls in updateCountdown to use updateTumbler
old_display_calls = '''      elM.textContent = String(months).padStart(2, '0');
      elD.textContent = String(days).padStart(2, '0');
      elH.textContent = String(hours).padStart(2, '0');
      elMin.textContent = String(minutes).padStart(2, '0');
      elS.textContent = String(seconds).padStart(2, '0');

      // Trigger synthesized sound tick
      if (window.__slSound) window.__slSound.tick(seconds);'''

new_display_calls = '''      var sM = String(months).padStart(2, '0');
      var sD = String(days).padStart(2, '0');
      var sH = String(hours).padStart(2, '0');
      var sMin = String(minutes).padStart(2, '0');
      var sS = String(seconds).padStart(2, '0');

      updateTumbler('months', 'card-months', 'box-months', sM);
      updateTumbler('days', 'card-days', 'box-days', sD);
      updateTumbler('hours', 'card-hours', 'box-hours', sH);
      updateTumbler('minutes', 'card-minutes', 'box-minutes', sMin);
      updateTumbler('seconds', 'card-seconds', 'box-seconds', sS);

      // Trigger warp-drive pulse on each second tick
      triggerWarpPulse();

      // Trigger synthesized sound tick
      if (window.__slSound) window.__slSound.tick(seconds);'''

html = html.replace(old_display_calls, new_display_calls)

with open('index.html', 'w') as f:
    f.write(html)

with open('q3_2027_countdown.html', 'w') as f:
    f.write(html)

print("Updated index.html and q3_2027_countdown.html with all 4 cinematic animations!")
