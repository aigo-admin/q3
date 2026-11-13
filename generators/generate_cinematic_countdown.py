with open('sponsorship_brochure/assets/SecLeaf_Official.svg', 'r') as f:
    svg_raw = f.read()

if '<?xml' in svg_raw:
    svg_clean = svg_raw[svg_raw.find('<svg'):].strip()
else:
    svg_clean = svg_raw.strip()

svg_clean = svg_clean.replace('<svg ', '<svg class="brand-svg" ')

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SecLeaf Q3 2027 CTF</title>
  <meta name="description" content="SecLeaf Q3 2027 CTF — 24 July 12:00 PM IST to 25 July 12:00 PM IST. Official countdown.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    :root {{
      --bg: #040507;
      --surface: rgba(18, 22, 30, 0.65);
      --surface-hover: rgba(26, 32, 44, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(186, 236, 67, 0.3);
      
      --accent: #baec43;
      --accent-glow: rgba(186, 236, 67, 0.28);
      --accent-light: #d4ff5e;
      
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #475569;
      
      --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    html, body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      position: relative;
    }}

    /* CINEMATIC CANVAS & LIGHTING */
    #ambientCanvas {{
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
    }}

    .cinematic-glow {{
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 900px;
      height: 500px;
      background: radial-gradient(ellipse, rgba(186, 236, 67, 0.05) 0%, rgba(9, 14, 24, 0.15) 50%, transparent 75%);
      filter: blur(80px);
      pointer-events: none;
      z-index: 0;
    }}

    .cinematic-vignette {{
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at center, transparent 40%, rgba(4, 5, 7, 0.85) 100%);
      pointer-events: none;
      z-index: 1;
    }}

    /* MAIN WRAPPER */
    .page-stage {{
      position: relative;
      z-index: 2;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 32px 40px;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
    }}

    @media (max-width: 768px) {{
      .page-stage {{
        padding: 24px 20px;
      }}
    }}

    /* TOP BAR */
    .top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      color: inherit;
    }}

    .brand-logo-frame {{
      width: 48px;
      height: 48px;
      background: #010101;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }}

    .brand-logo-frame:hover {{
      border-color: var(--accent);
      box-shadow: 0 0 25px rgba(186, 236, 67, 0.25);
    }}

    .brand-svg {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
    }}

    .brand-meta {{
      display: flex;
      flex-direction: column;
    }}

    .brand-title {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.15;
    }}

    .brand-title span {{
      color: var(--accent);
    }}

    .brand-tag {{
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      letter-spacing: 0.04em;
    }}

    /* CALENDAR DROPDOWN MENU */
    .calendar-menu-wrap {{
      position: relative;
    }}

    .calendar-trigger-btn {{
      background: var(--surface);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: var(--font-main);
      font-size: 13px;
      font-weight: 600;
      padding: 10px 18px;
      border-radius: 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .calendar-trigger-btn:hover {{
      background: var(--surface-hover);
      border-color: var(--border-accent);
      color: #ffffff;
      transform: translateY(-1px);
    }}

    .calendar-icon {{
      color: var(--accent);
      display: flex;
      align-items: center;
    }}

    .calendar-caret {{
      opacity: 0.6;
      transition: transform 0.2s ease;
    }}

    .calendar-menu-wrap.open .calendar-caret {{
      transform: rotate(180deg);
    }}

    .calendar-dropdown {{
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      background: rgba(13, 17, 24, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      width: 250px;
      padding: 8px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7);
      opacity: 0;
      visibility: hidden;
      transform: translateY(-8px) scale(0.97);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 50;
    }}

    .calendar-menu-wrap.open .calendar-dropdown {{
      opacity: 1;
      visibility: visible;
      transform: translateY(0) scale(1);
    }}

    .dropdown-header {{
      padding: 8px 12px 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      margin-bottom: 4px;
    }}

    .calendar-option {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      color: var(--text);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease;
      background: transparent;
      border: none;
      width: 100%;
      text-align: left;
    }}

    .calendar-option:hover {{
      background: rgba(186, 236, 67, 0.12);
      color: #ffffff;
    }}

    .calendar-option svg {{
      width: 16px;
      height: 16px;
      opacity: 0.85;
      flex-shrink: 0;
    }}

    /* CENTER HERO STAGE */
    .center-stage {{
      text-align: center;
      padding: 40px 0;
      margin: auto 0;
      width: 100%;
    }}

    .edition-pill {{
      display: inline-block;
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
      background: rgba(186, 236, 67, 0.08);
      border: 1px solid rgba(186, 236, 67, 0.22);
      border-radius: 999px;
      padding: 6px 18px;
      margin-bottom: 24px;
      letter-spacing: 0.04em;
    }}

    .cinematic-headline {{
      font-family: var(--font-display);
      font-size: clamp(34px, 5.5vw, 68px);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.1;
      color: #ffffff;
      margin-bottom: 16px;
    }}

    .cinematic-headline span {{
      color: var(--accent);
    }}

    /* DATE AND TIME SECTION */
    .date-hero {{
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      margin-bottom: 48px;
    }}

    .date-main {{
      font-size: clamp(17px, 2.2vw, 24px);
      font-weight: 600;
      color: #e2e8f0;
      letter-spacing: -0.01em;
    }}

    .date-sub {{
      font-size: clamp(13px, 1.4vw, 15px);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .date-dot {{
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--accent);
      display: inline-block;
    }}

    /* BIG CINEMATIC COUNTDOWN DISPLAY */
    .countdown-monolith {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: clamp(12px, 2.5vw, 32px);
      margin: 0 auto 36px;
      flex-wrap: wrap;
    }}

    .countdown-unit-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: clamp(100px, 14vw, 180px);
      padding: clamp(16px, 2.5vw, 32px) clamp(12px, 1.8vw, 24px);
      background: rgba(14, 18, 26, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 20px;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
      position: relative;
      transition: border-color 0.3s ease, transform 0.3s ease;
    }}

    .countdown-unit-card:hover {{
      border-color: rgba(255, 255, 255, 0.16);
      transform: translateY(-2px);
    }}

    .countdown-unit-card.accent-card {{
      border-color: rgba(186, 236, 67, 0.28);
      background: radial-gradient(circle at 50% 0%, rgba(186, 236, 67, 0.07) 0%, rgba(14, 18, 26, 0.5) 80%);
    }}

    .big-number {{
      font-family: var(--font-display);
      font-size: clamp(48px, 8.5vw, 110px);
      font-weight: 700;
      color: #ffffff;
      line-height: 0.95;
      letter-spacing: -0.04em;
      font-variant-numeric: tabular-nums;
      margin-bottom: 12px;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }}

    .accent-card .big-number {{
      color: var(--accent);
      text-shadow: 0 0 40px rgba(186, 236, 67, 0.35);
    }}

    .unit-label {{
      font-size: clamp(11px, 1.1vw, 13px);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      color: var(--text-muted);
    }}

    .accent-card .unit-label {{
      color: rgba(186, 236, 67, 0.9);
    }}

    /* FOOTER BAR */
    .bottom-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: var(--text-dim);
      padding-top: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      flex-wrap: wrap;
      gap: 12px;
    }}

    .bottom-status {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .status-pulse-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
      animation: pulse 2.5s infinite ease-in-out;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(0.85); }}
    }}

    .bottom-tz-toggle {{
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
    }}

    .bottom-tz-toggle:hover {{
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    /* TOAST */
    .toast {{
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%) translateY(80px);
      background: rgba(18, 24, 34, 0.96);
      border: 1px solid var(--accent);
      color: #ffffff;
      font-size: 13px;
      font-weight: 500;
      padding: 12px 24px;
      border-radius: 10px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.8);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 100;
      pointer-events: none;
    }}

    .toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>

  <!-- AMBIENT BACKGROUND -->
  <canvas id="ambientCanvas"></canvas>
  <div class="cinematic-glow"></div>
  <div class="cinematic-vignette"></div>

  <div class="page-stage">

    <!-- TOP BAR -->
    <header class="top-bar">
      <a href="#" class="brand-wrap">
        <div class="brand-logo-frame" title="SecLeaf Logo">
          {svg_clean}
        </div>
        <div class="brand-meta">
          <div class="brand-title">Sec<span>Leaf</span></div>
          <div class="brand-tag">Cybersecurity CTF</div>
        </div>
      </a>

      <!-- ADD TO CALENDAR BUTTON & COMPATIBLE DROPDOWN -->
      <div class="calendar-menu-wrap" id="calendarMenu">
        <button class="calendar-trigger-btn" onclick="toggleCalendarMenu()" aria-expanded="false">
          <span class="calendar-icon">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </span>
          <span>Add to Calendar</span>
          <span class="calendar-caret">▾</span>
        </button>

        <div class="calendar-dropdown">
          <div class="dropdown-header">Compatible Calendars</div>
          
          <!-- GOOGLE CALENDAR -->
          <a class="calendar-option" href="#" onclick="addToGoogleCalendar(event)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11zM11 11h2v5h-2zm-4 0h2v5H7zm8 0h2v5h-2z"/>
            </svg>
            <span>Google Calendar</span>
          </a>

          <!-- APPLE CALENDAR -->
          <a class="calendar-option" href="#" onclick="downloadIcs(event, 'Apple Calendar')">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.62-.75 1.04-1.8 0.92-2.85-.9.04-1.98.6-2.62 1.35-.57.65-1.07 1.72-.93 2.74 1 .08 2.02-.49 2.63-1.24z"/>
            </svg>
            <span>Apple Calendar</span>
          </a>

          <!-- OUTLOOK.COM -->
          <a class="calendar-option" href="#" onclick="addToOutlook(event)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M21.5 5h-7v14h7c.8 0 1.5-.7 1.5-1.5v-11c0-.8-.7-1.5-1.5-1.5zm-8 1h7c.3 0 .5.2.5.5v11c0 .3-.2.5-.5.5h-7V6zm-2-1H3.5C2.7 5 2 5.7 2 6.5v11c0 .8.7 1.5 1.5 1.5h8c.8 0 1.5-.7 1.5-1.5v-11c0-.8-.7-1.5-1.5-1.5zm.5 12.5c0 .3-.2.5-.5.5h-8c-.3 0-.5-.2-.5-.5v-11c0-.3.2-.5.5-.5h8c.3 0 .5.2.5.5v11z"/>
            </svg>
            <span>Outlook.com</span>
          </a>

          <!-- MICROSOFT 365 -->
          <a class="calendar-option" href="#" onclick="addToOffice365(event)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 2H3c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H3V4h18v16zM6 7h4v4H6zm0 6h4v4H6zm6-6h6v4h-6zm0 6h6v4h-6z"/>
            </svg>
            <span>Microsoft 365</span>
          </a>

          <!-- YAHOO CALENDAR -->
          <a class="calendar-option" href="#" onclick="addToYahoo(event)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <span>Yahoo Calendar</span>
          </a>

          <!-- DOWNLOAD ICAL (.ICS) -->
          <a class="calendar-option" href="#" onclick="downloadIcs(event, 'iCal File')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>Download iCal (.ics)</span>
          </a>
        </div>
      </div>
    </header>

    <!-- CENTER HERO: THE CINEMATIC COUNTDOWN -->
    <main class="center-stage">
      <div class="edition-pill">SecLeaf Flagship CTF</div>
      <h1 class="cinematic-headline">SecLeaf <span>Q3 2027 CTF</span></h1>

      <!-- EXACT DATE AND TIME -->
      <div class="date-hero">
        <div class="date-main" id="primaryDateDisplay">
          24 July 12:00 PM – 25 July 12:00 PM IST
        </div>
        <div class="date-sub">
          <span>Saturday to Sunday</span>
          <span class="date-dot"></span>
          <span>24 Hours Continuous</span>
          <span class="date-dot"></span>
          <span id="utcEquivalent">06:30 UTC</span>
        </div>
      </div>

      <!-- BIG COUNTDOWN MONOLITH: MONTHS, DAYS, HOURS, MINUTES, SECONDS -->
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
      </div>
    </main>

    <!-- BOTTOM BAR -->
    <footer class="bottom-bar">
      <div class="bottom-status">
        <span class="status-pulse-dot"></span>
        <span>SecLeaf Operations</span>
      </div>

      <div>
        <button class="bottom-tz-toggle" onclick="toggleTimezoneMode()" id="tzToggleBtn">
          Showing: IST (UTC+5:30) • Switch to Local
        </button>
      </div>
    </footer>

  </div>

  <div id="toast" class="toast">Calendar link opened</div>

  <script>
    // EVENT TIMELINE: 24 July 2027, 12:00 PM IST to 25 July 2027, 12:00 PM IST
    // In UTC: 24 July 2027 06:30:00Z to 25 July 2027 06:30:00Z
    const START_MS = Date.UTC(2027, 6, 24, 6, 30, 0); // Month is 0-indexed: 6 = July
    const END_MS   = Date.UTC(2027, 6, 25, 6, 30, 0);

    let isLocalTz = false;

    // COUNTDOWN ELEMENTS
    const elMonths = document.getElementById('numMonths');
    const elDays = document.getElementById('numDays');
    const elHours = document.getElementById('numHours');
    const elMinutes = document.getElementById('numMinutes');
    const elSeconds = document.getElementById('numSeconds');
    const elDateMain = document.getElementById('primaryDateDisplay');
    const elTzBtn = document.getElementById('tzToggleBtn');

    function updateCountdown() {{
      const now = new Date();
      const diff = START_MS - now.getTime();

      if (diff <= 0) {{
        elMonths.textContent = '00';
        elDays.textContent = '00';
        elHours.textContent = '00';
        elMinutes.textContent = '00';
        elSeconds.textContent = '00';
        return;
      }}

      // Calendar-aware months & days computation
      const target = new Date(START_MS);
      let months = (target.getFullYear() - now.getFullYear()) * 12 + (target.getMonth() - now.getMonth());
      let anchor = new Date(now.getFullYear(), now.getMonth() + months, now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds());
      if (anchor > target) {{
        months--;
        anchor = new Date(now.getFullYear(), now.getMonth() + months, now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds());
      }}

      const rem = target - anchor;
      const days = Math.floor(rem / (1000 * 60 * 60 * 24));
      const hours = Math.floor((rem / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((rem / (1000 * 60)) % 60);
      const seconds = Math.floor((rem / 1000) % 60);

      elMonths.textContent = String(months).padStart(2, '0');
      elDays.textContent = String(days).padStart(2, '0');
      elHours.textContent = String(hours).padStart(2, '0');
      elMinutes.textContent = String(minutes).padStart(2, '0');
      elSeconds.textContent = String(seconds).padStart(2, '0');
    }}

    function toggleTimezoneMode() {{
      isLocalTz = !isLocalTz;
      const startObj = new Date(START_MS);
      const endObj = new Date(END_MS);

      if (isLocalTz) {{
        const startStr = startObj.toLocaleString(undefined, {{
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        }});
        const endStr = endObj.toLocaleString(undefined, {{
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZoneName: 'short'
        }});
        elDateMain.textContent = `${{startStr}} – ${{endStr}}`;
        elTzBtn.textContent = 'Showing: Your Local Time • Switch to IST';
      }} else {{
        elDateMain.textContent = '24 July 12:00 PM – 25 July 12:00 PM IST';
        elTzBtn.textContent = 'Showing: IST (UTC+5:30) • Switch to Local';
      }}
    }}

    // CALENDAR MENU INTERACTIONS
    function toggleCalendarMenu() {{
      const menu = document.getElementById('calendarMenu');
      menu.classList.toggle('open');
    }}

    document.addEventListener('click', (e) => {{
      const menu = document.getElementById('calendarMenu');
      if (!menu.contains(e.target)) {{
        menu.classList.remove('open');
      }}
    }});

    function showToast(text) {{
      const toast = document.getElementById('toast');
      toast.textContent = text;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }}

    // CALENDAR PROVIDERS
    const EVENT_TITLE = 'SecLeaf Q3 2027 CTF';
    const EVENT_DESC = 'SecLeaf Q3 2027 Flagship CTF. 24-hour global cybersecurity competition (24 July 12:00 PM IST to 25 July 12:00 PM IST).';
    const EVENT_LOC = 'Online (SecLeaf Arena)';
    const DATES_GGL = '20270724T063000Z/20270725T063000Z';
    const ISO_START = '2027-07-24T06:30:00Z';
    const ISO_END   = '2027-07-25T06:30:00Z';

    function addToGoogleCalendar(e) {{
      e.preventDefault();
      const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${{encodeURIComponent(EVENT_TITLE)}}&dates=${{DATES_GGL}}&details=${{encodeURIComponent(EVENT_DESC)}}&location=${{encodeURIComponent(EVENT_LOC)}}`;
      window.open(url, '_blank', 'noopener,noreferrer');
      toggleCalendarMenu();
      showToast('Opening Google Calendar...');
    }}

    function addToOutlook(e) {{
      e.preventDefault();
      const url = `https://outlook.live.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt=${{ISO_START}}&enddt=${{ISO_END}}&subject=${{encodeURIComponent(EVENT_TITLE)}}&body=${{encodeURIComponent(EVENT_DESC)}}&location=${{encodeURIComponent(EVENT_LOC)}}`;
      window.open(url, '_blank', 'noopener,noreferrer');
      toggleCalendarMenu();
      showToast('Opening Outlook Calendar...');
    }}

    function addToOffice365(e) {{
      e.preventDefault();
      const url = `https://outlook.office.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt=${{ISO_START}}&enddt=${{ISO_END}}&subject=${{encodeURIComponent(EVENT_TITLE)}}&body=${{encodeURIComponent(EVENT_DESC)}}&location=${{encodeURIComponent(EVENT_LOC)}}`;
      window.open(url, '_blank', 'noopener,noreferrer');
      toggleCalendarMenu();
      showToast('Opening Microsoft 365...');
    }}

    function addToYahoo(e) {{
      e.preventDefault();
      const url = `https://calendar.yahoo.com/?v=60&view=d&type=20&title=${{encodeURIComponent(EVENT_TITLE)}}&st=20270724T063000Z&et=20270725T063000Z&desc=${{encodeURIComponent(EVENT_DESC)}}&in_loc=${{encodeURIComponent(EVENT_LOC)}}`;
      window.open(url, '_blank', 'noopener,noreferrer');
      toggleCalendarMenu();
      showToast('Opening Yahoo Calendar...');
    }}

    function downloadIcs(e, label) {{
      e.preventDefault();
      const ics = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//SecLeaf//Q3 2027 CTF//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'BEGIN:VEVENT',
        'UID:secleaf-q3-2027-ctf@secleaf.com',
        'DTSTAMP:20261113T010000Z',
        'DTSTART:20270724T063000Z',
        'DTEND:20270725T063000Z',
        'SUMMARY:' + EVENT_TITLE,
        'DESCRIPTION:' + EVENT_DESC,
        'LOCATION:' + EVENT_LOC,
        'STATUS:CONFIRMED',
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\\r\\n');

      const blob = new Blob([ics], {{ type: 'text/calendar;charset=utf-8' }});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'SecLeaf_Q3_2027_CTF.ics';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      toggleCalendarMenu();
      showToast(`Downloaded for ${{label}}`);
    }}

    // CINEMATIC PARTICLES CANVAS
    (function initParticles() {{
      const canvas = document.getElementById('ambientCanvas');
      const ctx = canvas.getContext('2d');
      let w, h;
      let particles = [];
      const count = 35;

      function resize() {{
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
      }}
      window.addEventListener('resize', resize);
      resize();

      for (let i = 0; i < count; i++) {{
        particles.push({{
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 1.8 + 0.4,
          vx: (Math.random() - 0.5) * 0.25,
          vy: -Math.random() * 0.35 - 0.1,
          alpha: Math.random() * 0.35 + 0.1,
          pulse: Math.random() * 0.02 + 0.01
        }});
      }}

      function loop() {{
        ctx.clearRect(0, 0, w, h);
        for (let p of particles) {{
          p.x += p.vx;
          p.y += p.vy;
          p.alpha += Math.sin(Date.now() * p.pulse * 0.05) * 0.005;

          if (p.y < -10) {{ p.y = h + 10; p.x = Math.random() * w; }}
          if (p.x < -10) {{ p.x = w + 10; }}
          if (p.x > w + 10) {{ p.x = -10; }}

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(186, 236, 67, ${{Math.max(0.05, Math.min(0.45, p.alpha))}})`;
          ctx.fill();
        }}
        requestAnimationFrame(loop);
      }}
      loop();
    }})();

    updateCountdown();
    setInterval(updateCountdown, 1000);
  </script>
</body>
</html>
'''

with open('q3_2027_countdown.html', 'w') as f:
    f.write(html_content)

print("Cinematic countdown generated in q3_2027_countdown.html")
