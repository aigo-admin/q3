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
  <title>SecLeaf Q3 2027 CTF — 24 & 25 July 2027</title>
  <meta name="description" content="Official countdown to SecLeaf Q3 2027 CTF on 24th and 25th July 2027. 36 hours of competitive cybersecurity challenges.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    :root {{
      --bg: #090a0d;
      --surface: #111318;
      --surface-subtle: #161922;
      --border: #1f232d;
      --border-focus: #2d3342;
      
      --accent: #baec43;
      --accent-soft: rgba(186, 236, 67, 0.1);
      --accent-hover: #c9ff47;
      
      --text: #f4f6fa;
      --text-muted: #8c96a8;
      --text-dim: #545e70;
      
      --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, Menlo, Monaco, Consolas, monospace;
    }}

    html, body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      min-height: 100vh;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }}

    ::selection {{
      background: var(--accent);
      color: #000000;
    }}

    .container {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* HEADER */
    .site-header {{
      padding: 32px 0 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }}

    .brand-link {{
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      color: inherit;
    }}

    .brand-logo-frame {{
      width: 44px;
      height: 44px;
      background: #010101;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .brand-svg {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
    }}

    .brand-info {{
      display: flex;
      flex-direction: column;
    }}

    .brand-name {{
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
    }}

    .brand-name span {{
      color: var(--accent);
    }}

    .brand-subtitle {{
      font-size: 12px;
      color: var(--text-dim);
      font-weight: 500;
    }}

    .header-tag {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 6px 14px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 999px;
      color: var(--text-muted);
    }}

    .tag-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
    }}

    /* HERO */
    .hero {{
      padding: 72px 0 48px;
      text-align: center;
    }}

    .event-badge {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
      background: var(--accent-soft);
      border: 1px solid rgba(186, 236, 67, 0.25);
      border-radius: 6px;
      padding: 6px 16px;
      margin-bottom: 24px;
      letter-spacing: 0.02em;
    }}

    .hero-title {{
      font-size: clamp(38px, 6vw, 68px);
      font-weight: 800;
      letter-spacing: -0.035em;
      line-height: 1.1;
      margin-bottom: 20px;
      color: #ffffff;
    }}

    .hero-title span {{
      color: var(--accent);
    }}

    .hero-desc {{
      max-width: 620px;
      margin: 0 auto 36px;
      font-size: 18px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* COUNTDOWN SECTION */
    .countdown-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 40px 32px;
      margin-bottom: 40px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}

    .countdown-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      flex-wrap: wrap;
      gap: 16px;
    }}

    .countdown-controls-label {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }}

    .tz-switcher {{
      display: flex;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 3px;
      gap: 4px;
    }}

    .tz-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.15s ease;
    }}

    .tz-btn.active {{
      background: var(--surface-subtle);
      color: var(--text);
      font-weight: 600;
      border: 1px solid var(--border-focus);
    }}

    /* COUNTDOWN GRID: MONTHS, DAYS, HOURS, MINUTES, SECONDS */
    .countdown-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 32px;
    }}

    @media (max-width: 768px) {{
      .countdown-grid {{
        grid-template-columns: repeat(3, 1fr);
      }}
    }}

    @media (max-width: 480px) {{
      .countdown-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .time-tile {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px 16px;
      text-align: center;
      transition: border-color 0.2s ease;
    }}

    .time-tile:hover {{
      border-color: var(--border-focus);
    }}

    .time-tile.accent {{
      border-color: rgba(186, 236, 67, 0.35);
      background: linear-gradient(180deg, rgba(186, 236, 67, 0.04) 0%, var(--bg) 100%);
    }}

    .time-number {{
      font-family: var(--font-mono);
      font-size: clamp(40px, 4.8vw, 64px);
      font-weight: 700;
      color: #ffffff;
      line-height: 1;
      margin-bottom: 8px;
      font-variant-numeric: tabular-nums;
    }}

    .time-tile.accent .time-number {{
      color: var(--accent);
    }}

    .time-unit {{
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
    }}

    .countdown-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: var(--text-muted);
      flex-wrap: wrap;
      gap: 12px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
    }}

    .countdown-meta strong {{
      color: #ffffff;
      font-weight: 600;
    }}

    /* BUTTONS */
    .button-group {{
      display: flex;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
      margin: 40px 0 64px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 13px 24px;
      font-size: 14px;
      font-weight: 600;
      border-radius: 10px;
      border: 1px solid transparent;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .btn-primary {{
      background: var(--accent);
      color: #000000;
      font-weight: 700;
    }}

    .btn-primary:hover {{
      background: var(--accent-hover);
      transform: translateY(-1px);
    }}

    .btn-outline {{
      background: var(--surface);
      border-color: var(--border);
      color: var(--text);
    }}

    .btn-outline:hover {{
      background: var(--surface-subtle);
      border-color: var(--border-focus);
      transform: translateY(-1px);
    }}

    /* EVENT DETAILS GRID */
    .details-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 40px;
    }}

    @media (max-width: 800px) {{
      .details-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .detail-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
    }}

    .detail-heading {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-dim);
      margin-bottom: 12px;
    }}

    .detail-value {{
      font-size: 20px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 8px;
      letter-spacing: -0.01em;
    }}

    .detail-desc {{
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* CATEGORIES LIST */
    .categories-box {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 64px;
    }}

    .categories-title {{
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 16px;
    }}

    .category-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .pill {{
      font-size: 13px;
      font-weight: 500;
      padding: 8px 16px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
    }}

    /* FOOTER */
    .site-footer {{
      border-top: 1px solid var(--border);
      padding: 36px 0;
      margin-top: 40px;
    }}

    .footer-content {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 13px;
      color: var(--text-dim);
    }}

    .footer-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .footer-logo {{
      width: 24px;
      height: 24px;
      background: #010101;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 2px;
    }}

    /* TOAST */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--surface);
      border: 1px solid var(--accent);
      color: var(--text);
      font-size: 13px;
      font-weight: 500;
      padding: 12px 20px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s ease;
      z-index: 1000;
    }}

    .toast.show {{
      transform: translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>

  <div class="container">
    <!-- SITE HEADER -->
    <header class="site-header">
      <a href="#" class="brand-link">
        <div class="brand-logo-frame" title="SecLeaf Official Logo">
          {svg_clean}
        </div>
        <div class="brand-info">
          <div class="brand-name">Sec<span>Leaf</span></div>
          <div class="brand-subtitle">Cybersecurity Competitions</div>
        </div>
      </a>

      <div class="header-tag">
        <span class="tag-dot"></span>
        <span>24 – 25 July 2027</span>
      </div>
    </header>

    <!-- HERO -->
    <main class="hero">
      <div class="event-badge">Q3 2027 Flagship Event</div>
      <h1 class="hero-title">SecLeaf <span>Q3 2027 CTF</span></h1>
      <p class="hero-desc">
        A 36-hour global jeopardy competition for offensive security practitioners, students, and engineers worldwide.
      </p>

      <!-- COUNTDOWN CARD -->
      <section class="countdown-card">
        <div class="countdown-controls">
          <span class="countdown-controls-label">Countdown to Kickoff</span>

          <div class="tz-switcher">
            <button class="tz-btn active" data-tz="utc" onclick="setTz('utc')">UTC</button>
            <button class="tz-btn" data-tz="ist" onclick="setTz('ist')">IST (UTC+5:30)</button>
            <button class="tz-btn" data-tz="local" onclick="setTz('local')">Local Time</button>
          </div>
        </div>

        <div class="countdown-grid">
          <!-- MONTHS -->
          <div class="time-tile accent">
            <div class="time-number" id="boxMonths">--</div>
            <div class="time-unit">Months</div>
          </div>

          <!-- DAYS -->
          <div class="time-tile">
            <div class="time-number" id="boxDays">--</div>
            <div class="time-unit">Days</div>
          </div>

          <!-- HOURS -->
          <div class="time-tile">
            <div class="time-number" id="boxHours">--</div>
            <div class="time-unit">Hours</div>
          </div>

          <!-- MINUTES -->
          <div class="time-tile">
            <div class="time-number" id="boxMinutes">--</div>
            <div class="time-unit">Minutes</div>
          </div>

          <!-- SECONDS -->
          <div class="time-tile accent">
            <div class="time-number" id="boxSeconds">--</div>
            <div class="time-unit">Seconds</div>
          </div>
        </div>

        <div class="countdown-meta">
          <div>
            Total remaining: <strong id="totalDaysText">-- days</strong> (<span id="totalHoursText">-- hours</span>)
          </div>
          <div>
            Start time: <strong id="startDateTime">Saturday, 24 July 2027 at 00:00 UTC</strong>
          </div>
        </div>
      </section>

      <!-- BUTTONS -->
      <div class="button-group">
        <button class="btn btn-primary" onclick="downloadICS()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
          </svg>
          Add to Calendar
        </button>

        <button class="btn btn-outline" onclick="copyDate()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
          </svg>
          Copy Date
        </button>

        <button class="btn btn-outline" onclick="sharePage()">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
          </svg>
          Share
        </button>
      </div>

      <!-- EVENT DETAILS -->
      <section class="details-grid">
        <div class="detail-card">
          <div class="detail-heading">Duration & Window</div>
          <div class="detail-value">36 Hours</div>
          <div class="detail-desc">Runs continuously from Saturday morning through Sunday evening.</div>
        </div>

        <div class="detail-card">
          <div class="detail-heading">Competition Format</div>
          <div class="detail-value">Jeopardy Style</div>
          <div class="detail-desc">Progressive difficulty curve with first-blood scoring bonuses.</div>
        </div>

        <div class="detail-card">
          <div class="detail-heading">Participation</div>
          <div class="detail-value">Global & Open</div>
          <div class="detail-desc">Open to students, independent researchers, and industry professionals.</div>
        </div>
      </section>

      <!-- CHALLENGE TRACKS -->
      <section class="categories-box">
        <h2 class="categories-title">Challenge Categories</h2>
        <div class="category-pills">
          <span class="pill">Web Exploitation</span>
          <span class="pill">Binary Exploitation (Pwn)</span>
          <span class="pill">Reverse Engineering</span>
          <span class="pill">Cryptography</span>
          <span class="pill">Digital Forensics</span>
          <span class="pill">Cloud Security</span>
          <span class="pill">Hardware & Firmware</span>
          <span class="pill">Open Source Intelligence (OSINT)</span>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="site-footer">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="footer-logo">
            {svg_clean}
          </div>
          <span>SecLeaf — 24 & 25 July 2027</span>
        </div>

        <div>
          Official Q3 2027 Competition
        </div>
      </div>
    </footer>
  </div>

  <div id="toast" class="toast">Copied to clipboard</div>

  <script>
    const TARGET_MS = Date.UTC(2027, 6, 24, 0, 0, 0); // 24 July 2027 00:00:00 UTC
    let currentTz = 'utc';

    const elM = document.getElementById('boxMonths');
    const elD = document.getElementById('boxDays');
    const elH = document.getElementById('boxHours');
    const elMin = document.getElementById('boxMinutes');
    const elS = document.getElementById('boxSeconds');
    const elTotDays = document.getElementById('totalDaysText');
    const elTotHours = document.getElementById('totalHoursText');
    const elStartTime = document.getElementById('startDateTime');

    function update() {{
      const now = new Date();
      const diff = TARGET_MS - now.getTime();

      if (diff <= 0) {{
        elM.textContent = '00';
        elD.textContent = '00';
        elH.textContent = '00';
        elMin.textContent = '00';
        elS.textContent = '00';
        elTotDays.textContent = '0 days';
        elTotHours.textContent = '0 hours';
        return;
      }}

      const target = new Date(TARGET_MS);
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

      const totalDays = Math.floor(diff / (1000 * 60 * 60 * 24));
      const totalHours = Math.floor(diff / (1000 * 60 * 60));

      elM.textContent = String(months).padStart(2, '0');
      elD.textContent = String(days).padStart(2, '0');
      elH.textContent = String(hours).padStart(2, '0');
      elMin.textContent = String(minutes).padStart(2, '0');
      elS.textContent = String(seconds).padStart(2, '0');

      elTotDays.textContent = totalDays.toLocaleString() + ' days';
      elTotHours.textContent = totalHours.toLocaleString() + ' hours';
    }}

    function setTz(tz) {{
      currentTz = tz;
      document.querySelectorAll('.tz-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.tz === tz);
      }});

      if (tz === 'utc') {{
        elStartTime.textContent = 'Saturday, 24 July 2027 at 00:00 UTC';
      }} else if (tz === 'ist') {{
        elStartTime.textContent = 'Saturday, 24 July 2027 at 05:30 IST';
      }} else {{
        const target = new Date(TARGET_MS);
        elStartTime.textContent = target.toLocaleString(undefined, {{
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          timeZoneName: 'short'
        }});
      }}
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }}

    function copyDate() {{
      const text = 'SecLeaf Q3 2027 CTF: Saturday, 24 July 2027 at 00:00 UTC';
      navigator.clipboard.writeText(text).then(() => {{
        showToast('Date copied to clipboard');
      }}).catch(() => {{
        showToast('Saturday, 24 July 2027');
      }});
    }}

    function sharePage() {{
      if (navigator.share) {{
        navigator.share({{
          title: 'SecLeaf Q3 2027 CTF',
          text: 'Countdown to SecLeaf Q3 2027 CTF on 24 & 25 July 2027',
          url: window.location.href
        }}).catch(() => {{}});
      }} else {{
        navigator.clipboard.writeText(window.location.href);
        showToast('Link copied to clipboard');
      }}
    }}

    function downloadICS() {{
      const ics = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//SecLeaf//Q3 2027 CTF//EN',
        'BEGIN:VEVENT',
        'UID:secleaf-q3-2027@secleaf.com',
        'DTSTART:20270724T000000Z',
        'DTEND:20270725T120000Z',
        'SUMMARY:SecLeaf Q3 2027 CTF',
        'DESCRIPTION:36-hour global jeopardy cybersecurity competition by SecLeaf.',
        'LOCATION:Online (SecLeaf Arena)',
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
      showToast('Calendar invite downloaded');
    }}

    update();
    setInterval(update, 1000);
  </script>
</body>
</html>
'''

with open('q3_2027_countdown.html', 'w') as f:
    f.write(html_content)

print("Regenerated clean q3_2027_countdown.html!")
