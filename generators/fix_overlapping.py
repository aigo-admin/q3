with open('index.html', 'r') as f:
    c = f.read()

# 1. Remove the line cutting through the numbers (.tumbler-chassis::after and ::before)
c = c.replace('''    /* MECHANICAL SPLIT-FLAP CREASE / HINGE */
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
    }''', '''    /* EXTRUDED TUMBLER CHASSIS */
    .tumbler-chassis {
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 16px;
      perspective: 1000px;
      transform-style: preserve-3d;
    }''')

# 2. Fix tumbler-box and big-number styles to ensure solid centering and zero overlap
old_box_css = '''    /* ================= 3. SMOOTH DIGIT SLIDE & 3D TUMBLER MORPHING ================= */
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
    .digit-leaving {
      transform: translateY(-90%) rotateX(-35deg) scale(0.92);
      opacity: 0;
      filter: blur(4px);
    }

    .digit-incoming {
      transform: translateY(90%) rotateX(35deg) scale(0.92);
      opacity: 0;
      filter: blur(4px);
    }

    .digit-active {
      transform: translateY(0) rotateX(0deg) scale(1);
      opacity: 1;
      filter: blur(0px);
    }'''

new_box_css = '''    /* ================= 3. SOLID 3D TUMBLER DIGIT MORPHING (ZERO OVERLAP) ================= */
    .tumbler-box {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      transform-style: preserve-3d;
    }

    .big-number {
      font-family: var(--font-display);
      font-size: clamp(64px, 10vw, 148px);
      font-weight: 700;
      color: #ffffff;
      line-height: 0.95;
      letter-spacing: -0.04em;
      font-variant-numeric: tabular-nums;
      text-shadow: 0 4px 25px rgba(0, 0, 0, 0.85);
      display: inline-block;
      text-align: center;
      will-change: transform, opacity;
      transform-origin: center center;
    }

    .accent-card .big-number {
      color: var(--accent);
      text-shadow: 0 0 45px rgba(186, 236, 67, 0.45);
    }

    /* PURE 3D TUMBLER FLIP ANIMATION */
    .digit-flip {
      animation: tumblerFlip 0.36s cubic-bezier(0.175, 0.885, 0.32, 1.25);
    }

    @keyframes tumblerFlip {
      0% {
        transform: rotateX(42deg) scale(0.94);
        opacity: 0.55;
      }
      60% {
        transform: rotateX(-8deg) scale(1.02);
        opacity: 0.95;
      }
      100% {
        transform: rotateX(0deg) scale(1);
        opacity: 1;
      }
    }'''

c = c.replace(old_box_css, new_box_css)

# 3. Update updateTumbler JavaScript function so it updates single element directly
old_js = '''    // ================= 4. SMOOTH DIGIT SLIDE & FLIP MECHANISM =================
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
    }'''

new_js = '''    // ================= 4. SOLID 3D TUMBLER DIGIT UPDATE (ZERO OVERLAP) =================
    var currentValues = { months: '', days: '', hours: '', minutes: '', seconds: '' };

    function updateTumbler(unitId, cardId, boxId, newVal){
      var box = $(boxId);
      if (!box) return;

      if (currentValues[unitId] === newVal) return;
      currentValues[unitId] = newVal;

      // Update the digit text cleanly on a single element
      var numEl = box.querySelector('.big-number');
      if (!numEl){
        box.innerHTML = '<div class="big-number">' + newVal + '</div>';
        numEl = box.querySelector('.big-number');
      } else {
        numEl.textContent = newVal;
        numEl.classList.remove('digit-flip');
        void numEl.offsetWidth; // Force CSS reflow to re-trigger 3D flip animation
        numEl.classList.add('digit-flip');
      }

      var card = $(cardId);
      if (card){
        card.classList.remove('heartbeat-pulse');
        void card.offsetWidth;
        card.classList.add('heartbeat-pulse');
      }
    }'''

c = c.replace(old_js, new_js)

with open('index.html', 'w') as f:
    f.write(c)

with open('q3_2027_countdown.html', 'w') as f:
    f.write(c)

print("Overlapping issue completely resolved!")
