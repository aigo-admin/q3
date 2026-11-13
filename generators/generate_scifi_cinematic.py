import re

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  
  <!-- PRIMARY SEO METADATA -->
  <title>SecLeaf Q3 2027 CTF — 24 & 25 July 2027 | Official Countdown</title>
  <meta name="title" content="SecLeaf Q3 2027 CTF — 24 & 25 July 2027 | Official Countdown">
  <meta name="description" content="Official countdown for SecLeaf Q3 2027 CTF. 24-hour global jeopardy cybersecurity competition running from 24 July 12:00 PM IST to 25 July 12:00 PM IST. Add to your calendar with multi-stage reminders.">
  <meta name="keywords" content="SecLeaf, SecLeaf CTF, Q3 2027 CTF, Cybersecurity Competition, Jeopardy CTF, Ethical Hacking, Pwn, Reverse Engineering, Web Exploitation, Cryptography, DFIR, ctf.secleaf.xyz, q3.secleaf.xyz">
  <meta name="author" content="SecLeaf">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="https://ctf.secleaf.xyz/">
  <link rel="alternate" hreflang="x-default" href="https://ctf.secleaf.xyz/">
  <link rel="alternate" href="https://q3.secleaf.xyz/">
  <link rel="alternate" href="https://ctf.secleaf.tech/">
  <link rel="alternate" href="https://q3.secleaf.tech/">
  <meta name="theme-color" content="#040507">
  <meta name="color-scheme" content="dark">

  <!-- OPEN GRAPH / FACEBOOK / DISCORD / LINKEDIN -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://ctf.secleaf.xyz/">
  <meta property="og:site_name" content="SecLeaf Operations">
  <meta property="og:title" content="SecLeaf Q3 2027 CTF — 24 & 25 July 2027">
  <meta property="og:description" content="Official countdown to SecLeaf Q3 2027 CTF. 24-hour continuous global cybersecurity operations: 24 July 12:00 PM IST to 25 July 12:00 PM IST.">
  <meta property="og:image" content="https://ctf.secleaf.xyz/og-image.png">
  <meta property="og:image:secure_url" content="https://ctf.secleaf.xyz/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="SecLeaf Q3 2027 CTF Official Open Graph Card">

  <!-- TWITTER CARDS -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://ctf.secleaf.xyz/">
  <meta name="twitter:title" content="SecLeaf Q3 2027 CTF — 24 & 25 July 2027">
  <meta name="twitter:description" content="Official countdown to SecLeaf Q3 2027 CTF. 24-hour continuous global cybersecurity operations: 24 July 12:00 PM IST to 25 July 12:00 PM IST.">
  <meta name="twitter:image" content="https://ctf.secleaf.xyz/og-image.png">
  <meta name="twitter:site" content="@SecLeaf">
  <meta name="twitter:creator" content="@SecLeaf">

  <!-- SCHEMA.ORG JSON-LD STRUCTURED DATA -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "SecLeaf Q3 2027 CTF",
    "description": "SecLeaf Flagship Q3 2027 Jeopardy CTF. 24-hour global cybersecurity competition featuring Web Exploitation, Binary Exploitation, Reverse Engineering, Cryptography, Forensics, Cloud, and OSINT.",
    "startDate": "2027-07-24T12:00:00+05:30",
    "endDate": "2027-07-25T12:00:00+05:30",
    "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
    "eventStatus": "https://schema.org/EventScheduled",
    "location": {{
      "@type": "VirtualLocation",
      "url": "https://ctf.secleaf.xyz"
    }},
    "image": "https://ctf.secleaf.xyz/og-image.png",
    "organizer": {{
      "@type": "Organization",
      "name": "SecLeaf",
      "url": "https://secleaf.xyz"
    }},
    "offers": {{
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock",
      "url": "https://ctf.secleaf.xyz",
      "validFrom": "2026-11-01T00:00:00Z"
    }}
  }}
  </script>

  <!-- FONTS -->
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
      --surface: rgba(14, 18, 26, 0.65);
      --surface-hover: rgba(22, 28, 40, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(186, 236, 67, 0.35);
      
      --accent: #baec43;
      --accent-glow: rgba(186, 236, 67, 0.35);
      --accent-light: #d6ff62;
      
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

    /* CINEMATIC SCI-FI TRAILER EFFECTS */
    #ambientCanvas {{
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
    }}

    /* ANAMORPHIC HORIZONTAL FLARE STREAK */
    .anamorphic-beam {{
      position: fixed;
      top: 50%;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(186, 236, 67, 0.05) 15%, 
        rgba(186, 236, 67, 0.4) 50%, 
        rgba(186, 236, 67, 0.05) 85%, 
        transparent 100%);
      filter: blur(1.5px);
      pointer-events: none;
      z-index: 1;
      transform: translateY(-20px);
      opacity: 0.7;
    }}

    .cinematic-glow {{
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 1000px;
      height: 520px;
      background: radial-gradient(ellipse, rgba(186, 236, 67, 0.055) 0%, rgba(13, 20, 32, 0.25) 55%, transparent 75%);
      filter: blur(90px);
      pointer-events: none;
      z-index: 0;
    }}

    .cinematic-vignette {{
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at center, transparent 35%, rgba(4, 5, 7, 0.88) 100%);
      pointer-events: none;
      z-index: 1;
    }}

    /* DYNAMIC FILM GRAIN OVERLAY */
    .film-grain {{
      position: fixed;
      inset: 0;
      opacity: 0.038;
      pointer-events: none;
      z-index: 1;
      background-image: var(--grain, none);
      background-repeat: repeat;
    }}

    /* PAGE WRAPPER */
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
      gap: 16px;
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
      padding: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }}

    .brand-logo-frame:hover {{
      border-color: var(--accent);
      box-shadow: 0 0 25px rgba(186, 236, 67, 0.3);
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

    /* TOP RIGHT ACTIONS */
    .top-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    /* SOUND TOGGLE BUTTON */
    .sound-btn {{
      background: var(--surface);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-family: var(--font-main);
      font-size: 13px;
      font-weight: 600;
      padding: 10px 16px;
      border-radius: 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .sound-btn:hover {{
      background: var(--surface-hover);
      border-color: var(--border-accent);
      color: #ffffff;
      transform: translateY(-1px);
    }}

    .sound-btn[data-s="on"] {{
      border-color: var(--border-accent);
      color: var(--accent);
    }}

    .sound-icon-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--text-dim);
      transition: background 0.2s ease, box-shadow 0.2s ease;
    }}

    .sound-btn[data-s="on"] .sound-icon-dot {{
      background: var(--accent);
      box-shadow: 0 0 8px var(--accent);
      animation: pulse 2s infinite ease-in-out;
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
      background: rgba(13, 17, 24, 0.96);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      width: 270px;
      padding: 8px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
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
      display: flex;
      justify-content: space-between;
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
      color: var(--accent);
    }}

    .dropdown-footer {{
      margin-top: 6px;
      padding: 8px 12px;
      font-size: 11px;
      color: var(--text-dim);
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      line-height: 1.4;
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
      padding: 6px 20px;
      margin-bottom: 24px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .cinematic-headline {{
      font-family: var(--font-display);
      font-size: clamp(38px, 6vw, 76px);
      font-weight: 700;
      letter-spacing: -0.035em;
      line-height: 1.05;
      color: #ffffff;
      margin-bottom: 18px;
      text-transform: uppercase;
    }}

    .cinematic-headline span {{
      color: var(--accent);
      text-shadow: 0 0 35px rgba(186, 236, 67, 0.35);
    }}

    /* DATE AND TIME SECTION */
    .date-hero {{
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      margin-bottom: 44px;
    }}

    .date-canonical {{
      font-size: clamp(18px, 2.4vw, 26px);
      font-weight: 700;
      color: #f1f5f9;
      letter-spacing: -0.01em;
    }}

    /* AUTOMATIC TIMEZONE CONVERSION CALLOUT */
    .local-tz-banner {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 6px 16px;
      background: rgba(186, 236, 67, 0.06);
      border: 1px solid rgba(186, 236, 67, 0.18);
      border-radius: 8px;
      font-size: clamp(13px, 1.4vw, 15px);
      color: #cbd5e1;
    }}

    .local-tz-banner strong {{
      color: var(--accent);
    }}

    .date-sub {{
      font-size: 13px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 2px;
    }}

    .date-dot {{
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--accent);
      display: inline-block;
    }}

    /* BIG CINEMATIC COUNTDOWN MONOLITH */
    .countdown-monolith {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: clamp(10px, 2vw, 28px);
      margin: 0 auto 36px;
      flex-wrap: wrap;
    }}

    .countdown-unit-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: clamp(95px, 13vw, 175px);
      padding: clamp(16px, 2.2vw, 30px) clamp(10px, 1.6vw, 22px);
      background: rgba(14, 18, 26, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 20px;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
      position: relative;
      transition: border-color 0.3s ease, transform 0.3s ease;
    }}

    .countdown-unit-card:hover {{
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateY(-2px);
    }}

    .countdown-unit-card.accent-card {{
      border-color: rgba(186, 236, 67, 0.32);
      background: radial-gradient(circle at 50% 0%, rgba(186, 236, 67, 0.08) 0%, rgba(14, 18, 26, 0.55) 85%);
    }}

    .big-number {{
      font-family: var(--font-display);
      font-size: clamp(48px, 8vw, 108px);
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
      text-shadow: 0 0 35px rgba(186, 236, 67, 0.38);
    }}

    .unit-label {{
      font-size: clamp(11px, 1vw, 13px);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      color: var(--text-muted);
    }}

    .accent-card .unit-label {{
      color: rgba(186, 236, 67, 0.9);
    }}

    /* DOMAIN ACCESS PILLS */
    .domain-pills {{
      display: flex;
      justify-content: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
    }}

    .domain-pill {{
      font-size: 12px;
      font-family: var(--font-display);
      color: var(--text-muted);
      background: rgba(14, 18, 26, 0.6);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 4px 12px;
      text-decoration: none;
      transition: all 0.15s ease;
    }}

    .domain-pill:hover {{
      color: var(--accent);
      border-color: var(--border-accent);
    }}

    /* BOTTOM BAR */
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
      padding: 5px 12px;
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

  <!-- CINEMATIC SCI-FI TRAILER EFFECTS -->
  <canvas id="ambientCanvas"></canvas>
  <div class="anamorphic-beam"></div>
  <div class="cinematic-glow"></div>
  <div class="cinematic-vignette"></div>
  <div class="film-grain"></div>

  <div class="page-stage">

    <!-- TOP BAR -->
    <header class="top-bar">
      <a href="https://ctf.secleaf.xyz" class="brand-wrap">
        <div class="brand-logo-frame" title="SecLeaf Official Logo">
          {svg_clean}
        </div>
        <div class="brand-meta">
          <div class="brand-title">Sec<span>Leaf</span></div>
          <div class="brand-tag">Cybersecurity CTF</div>
        </div>
      </a>

      <div class="top-actions">
        <!-- SYNTHESIZED SOUND TOGGLE (From Downloads) -->
        <button class="sound-btn" id="snd" type="button" data-s="blocked" aria-pressed="true" aria-label="Toggle cinematic audio">
          <span class="sound-icon-dot"></span>
          <span id="snd-label">Tap for sound</span>
        </button>

        <!-- ADD TO CALENDAR BUTTON & COMPATIBLE DROPDOWN -->
        <div class="calendar-menu-wrap" id="calendarMenu">
          <button class="calendar-trigger-btn" id="cal-btn" onclick="toggleCalendarMenu()" aria-expanded="false">
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

          <div class="calendar-dropdown" id="cal-menu">
            <div class="dropdown-header">
              <span>Sync With Calendar</span>
              <span style="color: var(--accent);">Multi-Reminder</span>
            </div>
            
            <!-- GOOGLE CALENDAR -->
            <a class="calendar-option" id="c-google" href="#" target="_blank" rel="noopener noreferrer">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11zM11 11h2v5h-2zm-4 0h2v5H7zm8 0h2v5h-2z"/>
              </svg>
              <span>Google Calendar</span>
            </a>

            <!-- APPLE CALENDAR -->
            <button class="calendar-option" type="button" data-ics="apple">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.62-.75 1.04-1.8 0.92-2.85-.9.04-1.98.6-2.62 1.35-.57.65-1.07 1.72-.93 2.74 1 .08 2.02-.49 2.63-1.24z"/>
              </svg>
              <span>Apple Calendar (.ics)</span>
            </button>

            <!-- OUTLOOK.COM -->
            <a class="calendar-option" id="c-outlook" href="#" target="_blank" rel="noopener noreferrer">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M21.5 5h-7v14h7c.8 0 1.5-.7 1.5-1.5v-11c0-.8-.7-1.5-1.5-1.5zm-8 1h7c.3 0 .5.2.5.5v11c0 .3-.2.5-.5.5h-7V6zm-2-1H3.5C2.7 5 2 5.7 2 6.5v11c0 .8.7 1.5 1.5 1.5h8c.8 0 1.5-.7 1.5-1.5v-11c0-.8-.7-1.5-1.5-1.5zm.5 12.5c0 .3-.2.5-.5.5h-8c-.3 0-.5-.2-.5-.5v-11c0-.3.2-.5.5-.5h8c.3 0 .5.2.5.5v11z"/>
              </svg>
              <span>Outlook.com</span>
            </a>

            <!-- MICROSOFT 365 -->
            <a class="calendar-option" id="c-office" href="#" target="_blank" rel="noopener noreferrer">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 2H3c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H3V4h18v16zM6 7h4v4H6zm0 6h4v4H6zm6-6h6v4h-6zm0 6h6v4h-6z"/>
              </svg>
              <span>Microsoft 365</span>
            </a>

            <!-- YAHOO CALENDAR -->
            <a class="calendar-option" id="c-yahoo" href="#" target="_blank" rel="noopener noreferrer">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
              </svg>
              <span>Yahoo Calendar</span>
            </a>

            <!-- DOWNLOAD ICAL (.ICS) WITH 4 ALARMS -->
            <button class="calendar-option" type="button" data-ics="standard">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              <span>Download iCal (.ics)</span>
            </button>

            <div class="dropdown-footer">
              Includes 4 reminders: 1 day, 12 hours, 1 hour, & 15 minutes before event.
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- CENTER HERO: THE CINEMATIC COUNTDOWN -->
    <main class="center-stage">
      <div class="edition-pill">SecLeaf Flagship Operations</div>
      <h1 class="cinematic-headline">SecLeaf <span>Q3 2027 CTF</span></h1>

      <!-- EXACT DATE AND TIME + AUTOMATIC TIMEZONE CONVERSION -->
      <div class="date-hero">
        <div class="date-canonical" id="primaryDateDisplay">
          24 July 12:00 PM – 25 July 12:00 PM IST
        </div>

        <!-- AUTOCONVERTED LOCAL TIME BANNER -->
        <div class="local-tz-banner" id="localTzBanner">
          <span>Your Local Kickoff:</span>
          <strong id="localKickoffText">Detecting timezone...</strong>
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

      <!-- DOMAINS PILLS -->
      <div class="domain-pills">
        <a href="https://ctf.secleaf.xyz" class="domain-pill" target="_blank" rel="noopener">ctf.secleaf.xyz</a>
        <a href="https://q3.secleaf.xyz" class="domain-pill" target="_blank" rel="noopener">q3.secleaf.xyz</a>
        <a href="https://ctf.secleaf.tech" class="domain-pill" target="_blank" rel="noopener">ctf.secleaf.tech</a>
        <a href="https://q3.secleaf.tech" class="domain-pill" target="_blank" rel="noopener">q3.secleaf.tech</a>
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
          Showing: IST (UTC+5:30) • Switch to Local Time
        </button>
      </div>
    </footer>

  </div>

  <div id="toast" class="toast">Calendar link opened</div>

  <script>
  (function(){{
    // ================= EVENT TIMING =================
    // 24 July 2027 12:00 PM IST to 25 July 2027 12:00 PM IST
    // UTC: 24 July 2027 06:30:00Z to 25 July 2027 06:30:00Z
    var START = 1816410600000; // Date.UTC(2027, 6, 24, 6, 30, 0)
    var END   = 1816497000000; // Date.UTC(2027, 6, 25, 6, 30, 0)

    var EV = {{
      title: 'SecLeaf Q3 2027 CTF',
      desc: 'SecLeaf Q3 2027 Flagship CTF. 24-hour global cybersecurity competition.\\n\\nOfficial Portals:\\n• https://ctf.secleaf.xyz\\n• https://q3.secleaf.xyz\\n• https://ctf.secleaf.tech\\n• https://q3.secleaf.tech\\n\\nStarts: 24 July 2027 at 12:00 PM IST (06:30 UTC)\\nEnds: 25 July 2027 at 12:00 PM IST (06:30 UTC)\\nFormat: Jeopardy (Web, Pwn, Rev, Crypto, Forensics, Cloud, Hardware, OSINT)',
      loc: 'Online (SecLeaf Arena - ctf.secleaf.xyz)',
      url: 'https://ctf.secleaf.xyz'
    }};

    var $ = function(id){{ return document.getElementById(id); }};

    // ================= DYNAMIC FILM GRAIN GENERATOR =================
    (function generateGrain(){{
      try {{
        var g = document.createElement('canvas');
        g.width = g.height = 128;
        var gc = g.getContext('2d'), gd = gc.createImageData(128, 128), b = gd.data;
        for (var i = 0; i < b.length; i += 4) {{
          var v = (Math.random() * 255) | 0;
          b[i] = b[i+1] = b[i+2] = v;
          b[i+3] = 28;
        }}
        gc.putImageData(gd, 0, 0);
        document.documentElement.style.setProperty('--grain', 'url(' + g.toDataURL() + ')');
      }} catch(e){{}}
    }})();

    // ================= SYNTHESIZED SOUND ENGINE (From Downloads) =================
    (function sound(){{
      var KEY = 'secleaf-sound', AC = window.AudioContext || window.webkitAudioContext;
      var btn = $('snd'), lab = $('snd-label');
      var on = true, ctx, master, bus, built = false;
      try {{ if (localStorage.getItem(KEY) === 'off') on = false; }} catch(e){{}}

      function ui(){{
        var running = !!ctx && ctx.state === 'running';
        var s = !on ? 'off' : running ? 'on' : 'blocked';
        btn.setAttribute('data-s', s);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        lab.textContent = s === 'on' ? 'Sound on' : s === 'off' ? 'Sound off' : 'Tap for sound';
      }}

      function impulse(sec, decay){{
        var rate = ctx.sampleRate, len = rate * sec, buf = ctx.createBuffer(2, len, rate);
        for (var c = 0; c < 2; c++){{
          var d = buf.getChannelData(c);
          for (var i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, decay);
        }}
        return buf;
      }}

      function build(){{
        if (built) return; built = true;
        master = ctx.createGain(); master.gain.value = 0;
        var comp = ctx.createDynamicsCompressor(); master.connect(comp); comp.connect(ctx.destination);
        var conv = ctx.createConvolver(); conv.buffer = impulse(3.4, 2.4);
        var wet = ctx.createGain(); wet.gain.value = 0.55; conv.connect(wet); wet.connect(master);
        bus = ctx.createGain(); bus.connect(master); bus.connect(conv);

        // Dark sci-fi bass drone
        var dg = ctx.createGain(); dg.gain.value = 0.17; dg.connect(bus);
        var lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 360; lp.Q.value = 0.8; lp.connect(dg);
        [[55, 'sine', 0, 0.9], [55.25, 'sawtooth', -6, 0.22], [82.4, 'sine', 4, 0.5], [110.2, 'sawtooth', 3, 0.1], [164.8, 'triangle', -4, 0.1]].forEach(function(o){{
          var osc = ctx.createOscillator(); osc.type = o[1]; osc.frequency.value = o[0]; osc.detune.value = o[2];
          var g = ctx.createGain(); g.gain.value = o[3]; osc.connect(g); g.connect(lp); osc.start();
        }});
        var lfo = ctx.createOscillator(); lfo.frequency.value = 0.06;
        var lg = ctx.createGain(); lg.gain.value = 170;
        lfo.connect(lg); lg.connect(lp.frequency); lfo.start();

        // Shimmer pad (A minor)
        var pad = ctx.createGain(); pad.gain.value = 0.03; pad.connect(bus);
        [220, 261.63, 329.63, 440].forEach(function(f, i){{
          var osc = ctx.createOscillator(); osc.type = 'sine'; osc.frequency.value = f; osc.detune.value = (i - 1.5) * 3;
          var g = ctx.createGain(); g.gain.value = 0; osc.connect(g); g.connect(pad); osc.start();
          var l = ctx.createOscillator(); l.frequency.value = 0.05 + i * 0.021;
          var lgn = ctx.createGain(); lgn.gain.value = 0.5; l.connect(lgn); lgn.connect(g.gain);
          var off = ctx.createConstantSource ? ctx.createConstantSource() : null;
          if (off){{ off.offset.value = 0.5; off.connect(g.gain); off.start(); }}
          l.start();
        }});
      }}

      function fadeIn(){{ if (!master) return; var t = ctx.currentTime; master.gain.cancelScheduledValues(t); master.gain.setValueAtTime(master.gain.value, t); master.gain.linearRampToValueAtTime(0.55, t + 5); }}
      function fadeOut(){{ if (!master) return; var t = ctx.currentTime; master.gain.cancelScheduledValues(t); master.gain.setValueAtTime(master.gain.value, t); master.gain.linearRampToValueAtTime(0, t + 0.25); }}
      function active(){{ return on && ctx && ctx.state === 'running' && built && !document.hidden; }}

      function thump(vol, f0){{
        var t = ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'sine'; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(36, t + 0.3);
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.5);
        o.connect(g); g.connect(bus); o.start(t); o.stop(t + 0.55);
      }}

      function ping(f, vol, len){{
        var t = ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'sine'; o.frequency.value = f;
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t + len);
        o.connect(g); g.connect(bus); o.start(t); o.stop(t + len + 0.05);
      }}

      var prevSec = -1;
      window.__slSound = {{
        tick: function(secs){{
          if (!active()) return;
          if (secs === prevSec) return;
          prevSec = secs;
          if (secs % 60 === 0){{
            thump(0.7, 70); ping(220, 0.1, 1.6);
          }} else {{
            thump(0.28, 88);
          }}
        }}
      }};

      function start(){{
        if (!on || !AC) return;
        if (!ctx){{
          try {{ ctx = new AC({{ latencyHint: 'playback' }}); }} catch(e){{ ctx = new AC(); }}
          ctx.addEventListener('statechange', function(){{
            if (ctx.state === 'running' && on){{ build(); fadeIn(); }}
            ui();
          }});
        }}
        try {{ var p = ctx.resume(); if (p && p.catch) p.catch(function(){{}}); }} catch(e){{}}
        if (ctx.state === 'running'){{ build(); fadeIn(); }}
        ui();
      }}

      var unlockEvents = ['pointerup', 'touchend', 'click', 'keydown'];
      function unlock(e){{
        if (e.target && e.target.closest && e.target.closest('[data-ui]')) return;
        if (on) start();
        if (ctx && ctx.state === 'running') unlockEvents.forEach(function(n){{ removeEventListener(n, unlock, true); }});
      }}
      unlockEvents.forEach(function(n){{ addEventListener(n, unlock, true); }});

      btn.addEventListener('click', function(){{
        if (on && ctx && ctx.state === 'running'){{
          on = false; fadeOut(); try {{ localStorage.setItem(KEY, 'off'); }} catch(e){{}}
        }} else if (on){{
          start();
        }} else {{
          on = true; try {{ localStorage.setItem(KEY, 'on'); }} catch(e){{}}
          start();
        }}
        ui();
      }});

      document.addEventListener('visibilitychange', function(){{
        if (!ctx) return;
        if (document.hidden){{
          fadeOut(); setTimeout(function(){{ if (document.hidden) ctx.suspend().catch(function(){{}}); }}, 300);
        }} else if (on){{
          ctx.resume().then(function(){{ fadeIn(); }}).catch(function(){{}});
        }}
      }});

      ui();
      start();
    }})();

    // ================= COUNTDOWN & TIMEZONE AUTOCONVERSION =================
    var elM = $('numMonths'), elD = $('numDays'), elH = $('numHours'), elMin = $('numMinutes'), elS = $('numSeconds');
    var elDateMain = $('primaryDateDisplay'), elLocalTzText = $('localKickoffText'), elTzBtn = $('tzToggleBtn');
    var isLocalTz = false;

    // Autoconvert kickoff time to user's local timezone
    function initLocalTimezone(){{
      var startObj = new Date(START);
      try {{
        var userTz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Local';
        var localFormatted = startObj.toLocaleString(undefined, {{
          weekday: 'short',
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          timeZoneName: 'short'
        }});
        elLocalTzText.textContent = localFormatted + ' (' + userTz + ')';
      }} catch(e){{
        elLocalTzText.textContent = startObj.toLocaleString();
      }}
    }}
    initLocalTimezone();

    function updateCountdown(){{
      var now = Date.now();
      var diff = START - now;

      if (diff <= 0){{
        elM.textContent = '00';
        elD.textContent = '00';
        elH.textContent = '00';
        elMin.textContent = '00';
        elS.textContent = '00';
        return;
      }}

      var target = new Date(START);
      var nowDate = new Date(now);

      var months = (target.getFullYear() - nowDate.getFullYear()) * 12 + (target.getMonth() - nowDate.getMonth());
      var anchor = new Date(nowDate.getFullYear(), nowDate.getMonth() + months, nowDate.getDate(), nowDate.getHours(), nowDate.getMinutes(), nowDate.getSeconds());
      if (anchor > target){{
        months--;
        anchor = new Date(nowDate.getFullYear(), nowDate.getMonth() + months, nowDate.getDate(), nowDate.getHours(), nowDate.getMinutes(), nowDate.getSeconds());
      }}

      var rem = target - anchor;
      var days = Math.floor(rem / (1000 * 60 * 60 * 24));
      var hours = Math.floor((rem / (1000 * 60 * 60)) % 24);
      var minutes = Math.floor((rem / (1000 * 60)) % 60);
      var seconds = Math.floor((rem / 1000) % 60);

      elM.textContent = String(months).padStart(2, '0');
      elD.textContent = String(days).padStart(2, '0');
      elH.textContent = String(hours).padStart(2, '0');
      elMin.textContent = String(minutes).padStart(2, '0');
      elS.textContent = String(seconds).padStart(2, '0');

      // Trigger synthesized sound tick
      if (window.__slSound) window.__slSound.tick(seconds);
    }}

    window.toggleTimezoneMode = function(){{
      isLocalTz = !isLocalTz;
      var startObj = new Date(START);
      var endObj = new Date(END);

      if (isLocalTz){{
        var startStr = startObj.toLocaleString(undefined, {{
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        }});
        var endStr = endObj.toLocaleString(undefined, {{
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZoneName: 'short'
        }});
        elDateMain.textContent = startStr + ' – ' + endStr;
        elTzBtn.textContent = 'Showing: Your Local Time • Switch to IST';
      }} else {{
        elDateMain.textContent = '24 July 12:00 PM – 25 July 12:00 PM IST';
        elTzBtn.textContent = 'Showing: IST (UTC+5:30) • Switch to Local Time';
      }}
    }};

    // ================= CALENDAR PROVIDERS & ICS WITH 4 REMINDERS =================
    function pad2(n){{ return String(n).padStart(2, '0'); }}
    function stamp(ms){{
      var d = new Date(ms);
      return d.getUTCFullYear() + pad2(d.getUTCMonth()+1) + pad2(d.getUTCDate()) + 'T' + pad2(d.getUTCHours()) + pad2(d.getUTCMinutes()) + pad2(d.getUTCSeconds()) + 'Z';
    }}
    function iso(ms){{ return new Date(ms).toISOString().replace(/\.\d{{3}}Z$/, 'Z'); }}
    function q(o){{ return Object.keys(o).map(function(k){{ return k + '=' + encodeURIComponent(o[k]); }}).join('&'); }}

    // Direct Web Links
    $('c-google').href  = 'https://calendar.google.com/calendar/render?' + q({{ action: 'TEMPLATE', text: EV.title, dates: stamp(START)+'/'+stamp(END), details: EV.desc, location: EV.loc }});
    var ol = {{ path: '/calendar/action/compose', rru: 'addevent', subject: EV.title, startdt: iso(START), enddt: iso(END), body: EV.desc, location: EV.loc }};
    $('c-outlook').href = 'https://outlook.live.com/calendar/0/deeplink/compose?' + q(ol);
    $('c-office').href  = 'https://outlook.office.com/calendar/0/deeplink/compose?' + q(ol);
    $('c-yahoo').href   = 'https://calendar.yahoo.com/?' + q({{ v: 60, title: EV.title, st: stamp(START), et: stamp(END), desc: EV.desc, in_loc: EV.loc }});

    function esc(s){{ return s.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n'); }}
    function fold(l){{ var o = ''; while(l.length > 74){{ o += l.slice(0, 74) + '\r\n '; l = l.slice(74); }} return o + l; }}

    // BUILD ICS WITH MULTIPLE ALARMS (1 Day, 12 Hours, 1 Hour, 15 Minutes)
    function buildICS(){{
      var L = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//SecLeaf//Q3 2027 CTF Countdown//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'X-WR-CALNAME:' + esc(EV.title),
        'BEGIN:VEVENT',
        'UID:q3-2027-ctf@secleaf.xyz',
        'DTSTAMP:' + stamp(Date.now()),
        'DTSTART:' + stamp(START),
        'DTEND:' + stamp(END),
        'SUMMARY:' + esc(EV.title),
        'DESCRIPTION:' + esc(EV.desc),
        'LOCATION:' + esc(EV.loc),
        'URL:' + EV.url,
        'STATUS:CONFIRMED',
        'TRANSP:OPAQUE'
      ];

      // 4 Proactive Reminders
      [
        ['-P1D', 'in 1 day'],
        ['-PT12H', 'in 12 hours'],
        ['-PT1H', 'in 1 hour'],
        ['-PT15M', 'in 15 minutes']
      ].forEach(function(a){{
        L.push('BEGIN:VALARM');
        L.push('ACTION:DISPLAY');
        L.push('DESCRIPTION:' + esc(EV.title + ' starts ' + a[1]));
        L.push('TRIGGER:' + a[0]);
        L.push('END:VALARM');
      }});

      L.push('END:VEVENT');
      L.push('END:VCALENDAR');
      return L.map(fold).join('\r\n') + '\r\n';
    }}

    function downloadICSFile(label){{
      var ics = buildICS();
      var ios = /iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
      if (ios){{
        location.href = 'data:text/calendar;charset=utf-8,' + encodeURIComponent(ics);
        showToast('Adding to Apple Calendar...');
        return;
      }}
      var blob = new Blob([ics], {{ type: 'text/calendar;charset=utf-8' }});
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'SecLeaf_Q3_2027_CTF.ics';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function(){{ URL.revokeObjectURL(a.href); }}, 5000);
      showToast('Downloaded .ics with 4 reminders for ' + label);
    }}

    var calWrap = $('calendarMenu');
    window.toggleCalendarMenu = function(){{
      calWrap.classList.toggle('open');
    }};

    document.addEventListener('click', function(e){{
      if (!calWrap.contains(e.target)) calWrap.classList.remove('open');
    }});

    document.addEventListener('keydown', function(e){{
      if (e.key === 'Escape' && calWrap.classList.contains('open')) calWrap.classList.remove('open');
    }});

    Array.prototype.forEach.call(document.querySelectorAll('[data-ics]'), function(b){{
      b.addEventListener('click', function(){{
        var type = b.getAttribute('data-ics') === 'apple' ? 'Apple Calendar' : 'Calendar App';
        downloadICSFile(type);
        calWrap.classList.remove('open');
      }});
    }});

    Array.prototype.forEach.call(document.querySelectorAll('.calendar-dropdown a'), function(a){{
      a.addEventListener('click', function(){{
        setTimeout(function(){{ calWrap.classList.remove('open'); }}, 100);
      }});
    }});

    function showToast(text){{
      var toast = $('toast');
      toast.textContent = text;
      toast.classList.add('show');
      setTimeout(function(){{ toast.classList.remove('show'); }}, 2800);
    }}

    // ================= CINEMATIC AMBIENT PARTICLES (60 FPS CANVAS) =================
    (function initParticles(){{
      var canvas = $('ambientCanvas');
      var ctx = canvas.getContext('2d');
      var w, h;
      var particles = [];
      var count = 42;

      function resize(){{
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
      }}
      window.addEventListener('resize', resize);
      resize();

      for (var i = 0; i < count; i++){{
        particles.push({{
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 1.6 + 0.4,
          vx: (Math.random() - 0.5) * 0.22,
          vy: -Math.random() * 0.32 - 0.08,
          alpha: Math.random() * 0.35 + 0.1,
          pulse: Math.random() * 0.02 + 0.01
        }});
      }}

      function loop(){{
        ctx.clearRect(0, 0, w, h);
        for (var i = 0; i < particles.length; i++){{
          var p = particles[i];
          p.x += p.vx;
          p.y += p.vy;
          p.alpha += Math.sin(Date.now() * p.pulse * 0.05) * 0.005;

          if (p.y < -10){{ p.y = h + 10; p.x = Math.random() * w; }}
          if (p.x < -10){{ p.x = w + 10; }}
          if (p.x > w + 10){{ p.x = -10; }}

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(186, 236, 67, ' + Math.max(0.04, Math.min(0.42, p.alpha)) + ')';
          ctx.fill();
        }}
        requestAnimationFrame(loop);
      }}
      loop();
    }})();

    updateCountdown();
    setInterval(updateCountdown, 1000);
  }})();
  </script>
</body>
</html>
'''

# Write to both root index.html (for GitHub Pages / repo) and q3_2027_countdown.html
with open('index.html', 'w') as f:
    f.write(html_content)

with open('q3_2027_countdown.html', 'w') as f:
    f.write(html_content)

print("Generated GitHub-ready index.html and q3_2027_countdown.html successfully!")
