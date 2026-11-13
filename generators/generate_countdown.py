import re

with open('sponsorship_brochure/assets/SecLeaf_Official.svg', 'r') as f:
    svg_raw = f.read()

# Strip any xml declaration if present
if '<?xml' in svg_raw:
    svg_clean = svg_raw[svg_raw.find('<svg'):].strip()
else:
    svg_clean = svg_raw.strip()

# Ensure the SVG has clean responsive styles
svg_clean = svg_clean.replace('<svg ', '<svg class="brand-svg" ')

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SecLeaf Q3 2027 CTF — 24 & 25 July 2027</title>
  <meta name="description" content="Official countdown to SecLeaf Q3 2027 CTF. 36-hour global jeopardy cybersecurity competition on 24th and 25th July 2027.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    /* CSS RESET & CORE VARIABLES */
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    :root {{
      --bg: #090b0e;
      --bg-surface: #0e1117;
      --bg-card: #131720;
      --bg-elevated: #181d28;
      --border: #222938;
      --border-bright: #323d52;
      --border-accent: rgba(186, 236, 67, 0.4);
      
      --accent: #baec43;
      --accent-bright: #caff4a;
      --accent-muted: #82a82b;
      --accent-dim: rgba(186, 236, 67, 0.12);
      
      --text: #f0f3f6;
      --text-muted: #9ba6b8;
      --text-dim: #5c687d;
      
      --danger: #ff5555;
      --cyan: #1de1f3;
      
      --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    html, body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-display);
      min-height: 100vh;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
      selection-background-color: var(--accent);
      selection-color: #000;
    }}

    ::selection {{
      background: var(--accent);
      color: #090b0e;
    }}

    /* SUBTLE TACTICAL GRID BACKGROUND */
    .viewport-grid {{
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 48px 48px;
      pointer-events: none;
      z-index: 0;
    }}

    .viewport-noise {{
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at 50% 15%, rgba(186, 236, 67, 0.04) 0%, transparent 65%);
      pointer-events: none;
      z-index: 0;
    }}

    /* CONTAINER */
    .container {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 24px;
      position: relative;
      z-index: 1;
    }}

    /* TOP TELEMETRY BAR */
    .telemetry-bar {{
      border-bottom: 1px solid var(--border);
      padding: 12px 0;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-dim);
      display: flex;
      justify-content: space-between;
      align-items: center;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}

    .telemetry-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .status-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
      display: inline-block;
      animation: pulse 2s infinite ease-in-out;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    .telemetry-right {{
      display: flex;
      gap: 20px;
    }}

    .time-badge {{
      color: var(--text-muted);
      font-weight: 500;
    }}

    /* NAVIGATION / HEADER */
    .site-header {{
      padding: 28px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 16px;
      text-decoration: none;
      color: inherit;
    }}

    .logo-frame {{
      width: 52px;
      height: 52px;
      background: #010101;
      border: 1px solid var(--border-bright);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      padding: 4px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      transition: border-color 0.2s ease;
    }}

    .logo-frame:hover {{
      border-color: var(--accent);
    }}

    .brand-svg {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
    }}

    .brand-titles {{
      display: flex;
      flex-direction: column;
    }}

    .brand-name {{
      font-size: 19px;
      font-weight: 700;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-name span.leaf {{
      color: var(--accent);
    }}

    .brand-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-dim);
      letter-spacing: 0.08em;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .header-pill {{
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 6px;
      border: 1px solid var(--border-bright);
      background: var(--bg-surface);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .pill-accent {{
      border-color: var(--border-accent);
      background: var(--accent-dim);
      color: var(--accent-bright);
      font-weight: 600;
    }}

    /* HERO STAGE */
    .hero {{
      padding: 64px 0 32px 0;
      text-align: center;
    }}

    .hero-meta-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 6px 16px;
      border-radius: 4px;
      background: var(--bg-card);
      border: 1px solid var(--border-bright);
      color: var(--text-muted);
      margin-bottom: 24px;
    }}

    .hero-meta-badge .dot {{
      width: 6px;
      height: 6px;
      background: var(--accent);
      border-radius: 50%;
    }}

    .hero-title {{
      font-size: clamp(34px, 5.5vw, 64px);
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.05;
      margin-bottom: 18px;
      text-transform: uppercase;
    }}

    .hero-title .highlight {{
      color: var(--accent);
      position: relative;
    }}

    .hero-subtitle {{
      max-width: 680px;
      margin: 0 auto 36px auto;
      font-size: clamp(15px, 1.8vw, 18px);
      color: var(--text-muted);
      line-height: 1.6;
    }}

    .hero-subtitle strong {{
      color: var(--text);
      font-weight: 600;
    }}

    /* COUNTDOWN SECTION */
    .countdown-section {{
      margin: 20px 0 54px 0;
    }}

    .countdown-wrapper {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 40px 32px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
      position: relative;
      overflow: hidden;
    }}

    .countdown-wrapper::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 10%;
      right: 10%;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--accent), transparent);
      opacity: 0.7;
    }}

    .countdown-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
      padding-bottom: 16px;
      border-bottom: 1px dashed var(--border);
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-dim);
    }}

    .timezone-selector {{
      display: flex;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }}

    .tz-btn {{
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 500;
      padding: 4px 10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .tz-btn.active {{
      background: var(--bg-elevated);
      color: var(--accent);
      border: 1px solid var(--border-bright);
    }}

    /* COUNTDOWN GRID: MONTHS, DAYS, HOURS, MINUTES, SECONDS */
    .countdown-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
    }}

    @media (max-width: 820px) {{
      .countdown-grid {{
        grid-template-columns: repeat(3, 1fr);
      }}
    }}

    @media (max-width: 540px) {{
      .countdown-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .time-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px 16px;
      text-align: center;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .time-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-bright);
    }}

    .time-card.accent-card {{
      border-color: rgba(186, 236, 67, 0.35);
      background: linear-gradient(180deg, rgba(186, 236, 67, 0.05) 0%, var(--bg-card) 100%);
    }}

    .time-card-corner {{
      position: absolute;
      top: 6px;
      left: 8px;
      font-family: var(--font-mono);
      font-size: 9px;
      color: var(--text-dim);
      letter-spacing: 0.06em;
    }}

    .time-value {{
      font-family: var(--font-mono);
      font-size: clamp(38px, 4.5vw, 68px);
      font-weight: 800;
      line-height: 1;
      color: #ffffff;
      letter-spacing: -0.04em;
      margin-bottom: 10px;
      font-variant-numeric: tabular-nums;
      text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }}

    .accent-card .time-value {{
      color: var(--accent);
      text-shadow: 0 0 20px rgba(186, 236, 67, 0.25);
    }}

    .time-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.14em;
    }}

    .time-subtext {{
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--text-dim);
      margin-top: 6px;
    }}

    /* TOTAL DAYS BAR BELOW */
    .countdown-footer-meta {{
      margin-top: 28px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
    }}

    .meta-stat-group {{
      display: flex;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
    }}

    .meta-stat {{
      display: flex;
      align-items: baseline;
      gap: 6px;
    }}

    .meta-stat .val {{
      font-weight: 700;
      color: #fff;
    }}

    .meta-stat .lbl {{
      color: var(--text-dim);
    }}

    /* ACTION BUTTONS */
    .action-row {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin: 36px 0;
    }}

    .btn {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      padding: 13px 24px;
      border-radius: 8px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      transition: all 0.2s ease;
      letter-spacing: 0.02em;
      border: 1px solid transparent;
    }}

    .btn-primary {{
      background: var(--accent);
      color: #090b0e;
      border-color: var(--accent);
      box-shadow: 0 4px 18px rgba(186, 236, 67, 0.25);
    }}

    .btn-primary:hover {{
      background: var(--accent-bright);
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(186, 236, 67, 0.4);
    }}

    .btn-secondary {{
      background: var(--bg-card);
      color: var(--text);
      border-color: var(--border-bright);
    }}

    .btn-secondary:hover {{
      background: var(--bg-elevated);
      border-color: var(--text-muted);
      color: #ffffff;
      transform: translateY(-2px);
    }}

    /* EVENT SPECIFICATIONS SECTION */
    .specs-section {{
      margin: 40px 0 60px 0;
    }}

    .specs-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}

    @media (max-width: 900px) {{
      .specs-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 500px) {{
      .specs-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .spec-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
    }}

    .spec-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .spec-value {{
      font-size: 17px;
      font-weight: 700;
      color: var(--text);
      letter-spacing: -0.01em;
      margin-bottom: 4px;
    }}

    .spec-detail {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* DOMAINS / TRACKS STRIP */
    .domains-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px 32px;
      margin-bottom: 60px;
    }}

    .domains-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .domains-title {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .domains-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-dim);
    }}

    .tag-cloud {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .tag-item {{
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 6px 14px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }}

    .tag-item:hover {{
      border-color: var(--border-accent);
      color: var(--text);
    }}

    /* FOOTER */
    .site-footer {{
      border-top: 1px solid var(--border);
      padding: 36px 0 48px 0;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-dim);
    }}

    .footer-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .footer-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .footer-logo {{
      width: 28px;
      height: 28px;
      border-radius: 6px;
      border: 1px solid var(--border-bright);
      padding: 2px;
      background: #010101;
    }}

    .footer-links {{
      display: flex;
      gap: 20px;
    }}

    .footer-links a {{
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.15s ease;
    }}

    .footer-links a:hover {{
      color: var(--accent);
    }}

    /* TOAST NOTIFICATION */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-card);
      border: 1px solid var(--accent);
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 12px 20px;
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 100;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .toast.show {{
      transform: translateY(0);
      opacity: 1;
    }}

    .toast-icon {{
      color: var(--accent);
    }}
  </style>
</head>
<body>

  <div class="viewport-grid"></div>
  <div class="viewport-noise"></div>

  <div class="container">
    <!-- TOP TELEMETRY BAR -->
    <div class="telemetry-bar">
      <div class="telemetry-left">
        <span class="status-dot"></span>
        <span>OPERATION: <strong>SECLEAF_Q3_2027</strong></span>
        <span>// CLASS: FLAGSHIP CTF</span>
      </div>
      <div class="telemetry-right">
        <span>TARGET DATE: <span class="time-badge">24-JUL-2027</span></span>
        <span id="liveClock">CURRENT UTC: --:--:--</span>
      </div>
    </div>

    <!-- SITE HEADER WITH OFFICIAL SECLEAF LOGO -->
    <header class="site-header">
      <a href="#" class="brand-wrap">
        <div class="logo-frame" title="SecLeaf Official Logo">
          {svg_clean}
        </div>
        <div class="brand-titles">
          <div class="brand-name">Sec<span class="leaf">Leaf</span></div>
          <div class="brand-tag">GLOBAL CYBERSECURITY ARENA</div>
        </div>
      </a>

      <div class="header-actions">
        <div class="header-pill pill-accent">
          <span>Q3 2027 FLAGSHIP</span>
        </div>
        <div class="header-pill">
          <span>24 – 25 JULY 2027</span>
        </div>
      </div>
    </header>

    <!-- HERO INTRODUCTION -->
    <section class="hero">
      <div class="hero-meta-badge">
        <span class="dot"></span>
        <span>OFFICIAL TIMELINE // JEOPARDY FORMAT</span>
      </div>
      <h1 class="hero-title">
        SecLeaf <span class="highlight">Q3 2027 CTF</span>
      </h1>
      <p class="hero-subtitle">
        The flagship global cyber operations challenge. 36 hours of rigorous offensive security, cryptography, reverse engineering, and threat intelligence. Built for real operators.
      </p>
    </section>

    <!-- LIVE COUNTDOWN DISPLAY -->
    <section class="countdown-section">
      <div class="countdown-wrapper">
        <div class="countdown-header">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: var(--accent); font-weight: 700;">T-MINUS</span>
            <span>COUNTDOWN TO KICKOFF</span>
          </div>

          <div class="timezone-selector">
            <button class="tz-btn active" data-tz="utc" onclick="setTimezone('utc')">UTC</button>
            <button class="tz-btn" data-tz="ist" onclick="setTimezone('ist')">IST (UTC+5:30)</button>
            <button class="tz-btn" data-tz="local" onclick="setTimezone('local')">LOCAL</button>
          </div>
        </div>

        <!-- 5-UNIT COUNTDOWN GRID: MONTHS, DAYS, HOURS, MINUTES, SECONDS -->
        <div class="countdown-grid">
          <!-- MONTHS -->
          <div class="time-card accent-card">
            <span class="time-card-corner">MTH</span>
            <div class="time-value" id="valMonths">--</div>
            <div class="time-label">Months</div>
            <div class="time-subtext" id="subMonths">Calendar Units</div>
          </div>

          <!-- DAYS -->
          <div class="time-card">
            <span class="time-card-corner">DAY</span>
            <div class="time-value" id="valDays">--</div>
            <div class="time-label">Days</div>
            <div class="time-subtext" id="subDays">Remaining</div>
          </div>

          <!-- HOURS -->
          <div class="time-card">
            <span class="time-card-corner">HRS</span>
            <div class="time-value" id="valHours">--</div>
            <div class="time-label">Hours</div>
            <div class="time-subtext">00 – 23</div>
          </div>

          <!-- MINUTES -->
          <div class="time-card">
            <span class="time-card-corner">MIN</span>
            <div class="time-value" id="valMinutes">--</div>
            <div class="time-label">Minutes</div>
            <div class="time-subtext">00 – 59</div>
          </div>

          <!-- SECONDS -->
          <div class="time-card accent-card">
            <span class="time-card-corner">SEC</span>
            <div class="time-value" id="valSeconds">--</div>
            <div class="time-label">Seconds</div>
            <div class="time-subtext">Live Ticker</div>
          </div>
        </div>

        <!-- COUNTDOWN METADATA FOOTER -->
        <div class="countdown-footer-meta">
          <div class="meta-stat-group">
            <div class="meta-stat">
              <span class="lbl">TOTAL DAYS:</span>
              <span class="val" id="totalDaysStat">---</span>
            </div>
            <div class="meta-stat">
              <span class="lbl">TOTAL HOURS:</span>
              <span class="val" id="totalHoursStat">---</span>
            </div>
            <div class="meta-stat">
              <span class="lbl">START TIME:</span>
              <span class="val" id="startTimeDisplay">24 July 2027 • 00:00 UTC</span>
            </div>
          </div>
          <div id="targetDateStatus" style="color: var(--accent); font-weight: 600;">
            SYSTEM STATUS: CLOCK SYNCHRONIZED
          </div>
        </div>
      </div>

      <!-- ACTION BUTTONS -->
      <div class="action-row">
        <button class="btn btn-primary" onclick="downloadICS()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
          </svg>
          Add to Calendar (.ics)
        </button>

        <button class="btn btn-secondary" onclick="copyKickoffTimestamp()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
          </svg>
          Copy Timestamp
        </button>

        <button class="btn btn-secondary" onclick="shareEvent()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
          </svg>
          Share Countdown
        </button>
      </div>
    </section>

    <!-- KEY COMPETITION SPECIFICATIONS -->
    <section class="specs-section">
      <div class="specs-grid">
        <div class="spec-card">
          <div class="spec-label">
            <span>●</span> EVENT WINDOW
          </div>
          <div class="spec-value">24 – 25 July 2027</div>
          <div class="spec-detail">Saturday to Sunday • 36h Straight</div>
        </div>

        <div class="spec-card">
          <div class="spec-label">
            <span>●</span> FORMAT
          </div>
          <div class="spec-value">Jeopardy CTF</div>
          <div class="spec-detail">Dynamic Scoring • Flag Submissions</div>
        </div>

        <div class="spec-card">
          <div class="spec-label">
            <span>●</span> ELIGIBILITY
          </div>
          <div class="spec-value">Global Open</div>
          <div class="spec-detail">Solo & Teams up to 4 Members</div>
        </div>

        <div class="spec-card">
          <div class="spec-label">
            <span>●</span> DIFFICULTY SPREAD
          </div>
          <div class="spec-value">Beginner to Hard</div>
          <div class="spec-detail">Graduated curve with first-blood bonuses</div>
        </div>
      </div>
    </section>

    <!-- CHALLENGE DOMAINS -->
    <div class="domains-card">
      <div class="domains-header">
        <div class="domains-title">
          <span style="color: var(--accent);">///</span> COMPETITION TRACKS
        </div>
        <div class="domains-tag">TESTED ON PRODUCTION INFRASTRUCTURE</div>
      </div>
      <div class="tag-cloud">
        <div class="tag-item">Web Exploitation</div>
        <div class="tag-item">Binary Exploitation & Pwn</div>
        <div class="tag-item">Reverse Engineering</div>
        <div class="tag-item">Cryptography</div>
        <div class="tag-item">Digital Forensics & Incident Response</div>
        <div class="tag-item">Cloud & Container Security</div>
        <div class="tag-item">Hardware / RF & Firmware</div>
        <div class="tag-item">Open Source Intelligence (OSINT)</div>
      </div>
    </div>

    <!-- SITE FOOTER -->
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">
            {svg_clean}
          </div>
          <div>
            <strong>SecLeaf</strong> • Official Q3 2027 CTF Operations
          </div>
        </div>

        <div class="footer-links">
          <span>Target: 24th & 25th July 2027</span>
          <span>•</span>
          <span>Platform: SecLeaf Arena</span>
        </div>
      </div>
    </footer>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="toast">
    <span class="toast-icon">✓</span>
    <span id="toastMsg">Timestamp copied to clipboard</span>
  </div>

  <script>
    // TARGET EVENT TIMESTAMP: 24th July 2027, 00:00:00 UTC
    const TARGET_UTC_MS = Date.UTC(2027, 6, 24, 0, 0, 0); // Month is 0-indexed (6 = July)
    let selectedTz = 'utc';

    // ELEMENTS
    const elMonths = document.getElementById('valMonths');
    const elDays = document.getElementById('valDays');
    const elHours = document.getElementById('valHours');
    const elMinutes = document.getElementById('valMinutes');
    const elSeconds = document.getElementById('valSeconds');
    const elTotalDays = document.getElementById('totalDaysStat');
    const elTotalHours = document.getElementById('totalHoursStat');
    const elLiveClock = document.getElementById('liveClock');
    const elStartTimeDisplay = document.getElementById('startTimeDisplay');
    const elTargetStatus = document.getElementById('targetDateStatus');

    function updateCountdown() {{
      const now = new Date();
      const currentMs = now.getTime();
      const diffMs = TARGET_UTC_MS - currentMs;

      // Update live UTC clock in header
      const utcHours = String(now.getUTCHours()).padStart(2, '0');
      const utcMin = String(now.getUTCMinutes()).padStart(2, '0');
      const utcSec = String(now.getUTCSeconds()).padStart(2, '0');
      elLiveClock.textContent = `CURRENT UTC: ${{utcHours}}:${{utcMin}}:${{utcSec}}`;

      if (diffMs <= 0) {{
        elMonths.textContent = '00';
        elDays.textContent = '00';
        elHours.textContent = '00';
        elMinutes.textContent = '00';
        elSeconds.textContent = '00';
        elTargetStatus.textContent = 'OPERATION LIVE // CTF UNDERWAY';
        elTargetStatus.style.color = '#1de1f3';
        return;
      }}

      // TARGET DATE OBJECT
      const targetDate = new Date(TARGET_UTC_MS);

      // ACCURATE CALENDAR-AWARE MONTHS CALCULATION
      // Calculate remaining full months between now and target
      let months = (targetDate.getFullYear() - now.getFullYear()) * 12 + (targetDate.getMonth() - now.getMonth());
      
      // Candidate anchor date after adding 'months'
      let anchorDate = new Date(now.getFullYear(), now.getMonth() + months, now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds());
      if (anchorDate > targetDate) {{
        months--;
        anchorDate = new Date(now.getFullYear(), now.getMonth() + months, now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds());
      }}

      const remainingAfterMonthsMs = targetDate - anchorDate;
      const days = Math.floor(remainingAfterMonthsMs / (1000 * 60 * 60 * 24));
      const hours = Math.floor((remainingAfterMonthsMs / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((remainingAfterMonthsMs / (1000 * 60)) % 60);
      const seconds = Math.floor((remainingAfterMonthsMs / 1000) % 60);

      // Total aggregate counts for reference
      const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const totalHours = Math.floor(diffMs / (1000 * 60 * 60));

      // DISPLAY VALUES
      elMonths.textContent = String(months).padStart(2, '0');
      elDays.textContent = String(days).padStart(2, '0');
      elHours.textContent = String(hours).padStart(2, '0');
      elMinutes.textContent = String(minutes).padStart(2, '0');
      elSeconds.textContent = String(seconds).padStart(2, '0');

      elTotalDays.textContent = totalDays.toLocaleString();
      elTotalHours.textContent = totalHours.toLocaleString() + ' hrs';
    }}

    function setTimezone(tz) {{
      selectedTz = tz;
      document.querySelectorAll('.tz-btn').forEach(b => {{
        b.classList.toggle('active', b.dataset.tz === tz);
      }});

      if (tz === 'utc') {{
        elStartTimeDisplay.textContent = '24 July 2027 • 00:00:00 UTC';
      }} else if (tz === 'ist') {{
        elStartTimeDisplay.textContent = '24 July 2027 • 05:30:00 IST (UTC+5:30)';
      }} else {{
        const target = new Date(TARGET_UTC_MS);
        elStartTimeDisplay.textContent = target.toLocaleString(undefined, {{
          dateStyle: 'medium',
          timeStyle: 'short'
        }}) + ' (Your Local)';
      }}
    }}

    function showToast(message) {{
      const toast = document.getElementById('toast');
      const toastMsg = document.getElementById('toastMsg');
      toastMsg.textContent = message;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 3000);
    }}

    function copyKickoffTimestamp() {{
      const text = 'SecLeaf Q3 2027 CTF Kickoff: 24 July 2027 00:00:00 UTC (1816387200 UNIX)';
      navigator.clipboard.writeText(text).then(() => {{
        showToast('Kickoff timestamp copied to clipboard');
      }}).catch(() => {{
        showToast('24 July 2027 00:00:00 UTC');
      }});
    }}

    function shareEvent() {{
      if (navigator.share) {{
        navigator.share({{
          title: 'SecLeaf Q3 2027 CTF Countdown',
          text: 'Countdown to SecLeaf Q3 2027 CTF on 24th & 25th July 2027!',
          url: window.location.href
        }}).catch(() => {{}});
      }} else {{
        navigator.clipboard.writeText(window.location.href);
        showToast('Countdown page link copied to clipboard');
      }}
    }}

    function downloadICS() {{
      const icsData = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//SecLeaf//Q3 2027 CTF//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'BEGIN:VEVENT',
        'UID:secleaf-q3-2027-ctf@secleaf.com',
        'DTSTAMP:20261113T000000Z',
        'DTSTART:20270724T000000Z',
        'DTEND:20270725T120000Z',
        'SUMMARY:SecLeaf Q3 2027 CTF (Global Cyber Operations)',
        'DESCRIPTION:SecLeaf Flagship Q3 2027 Jeopardy CTF. 36-hour global cybersecurity competition featuring Web, Pwn, Rev, Crypto, Forensics, Hardware, Cloud, and OSINT.',
        'LOCATION:SecLeaf Online Arena',
        'STATUS:CONFIRMED',
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\\r\\n');

      const blob = new Blob([icsData], {{ type: 'text/calendar;charset=utf-8' }});
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.setAttribute('download', 'SecLeaf_Q3_2027_CTF.ics');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast('Calendar invite (.ics) downloaded');
    }}

    // INITIALIZE CLOCK
    updateCountdown();
    setInterval(updateCountdown, 1000);
  </script>
</body>
</html>
'''

with open('q3_2027_countdown.html', 'w') as f:
    f.write(html_template)

print("Generated q3_2027_countdown.html successfully!")
