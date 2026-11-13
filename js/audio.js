/**
 * SecLeaf Sector 404: Audio Engine
 * Supports real multi-track engine audio, tire screeches, impacts, horns,
 * arcade gadget sound effects, and seamless procedural Web Audio fallback.
 */

class SoundEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.initialized = false;
    this.audioBuffers = {};
    this.soundNodes = {};
    this.engineLayers = {};
    this.isFilesLoaded = false;

    // Procedural Fallback Nodes
    this.synthOsc = null;
    this.synthOsc2 = null;
    this.synthGain = null;
    this.synthFilter = null;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContextClass();

      // Master output gain
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0.85, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);

      // Initialize synthesized fallback engine
      this.initSynthFallback();

      // Load authentic real audio files
      this.loadRealAudioFiles();

      this.initialized = true;
    } catch (e) {
      console.warn('[Audio] Web Audio initialization warning:', e);
    }
  }

  initSynthFallback() {
    try {
      this.synthOsc = this.ctx.createOscillator();
      this.synthOsc2 = this.ctx.createOscillator();
      this.synthGain = this.ctx.createGain();
      this.synthFilter = this.ctx.createBiquadFilter();

      this.synthOsc.type = 'sawtooth';
      this.synthOsc2.type = 'triangle';
      this.synthOsc.frequency.setValueAtTime(55, this.ctx.currentTime);
      this.synthOsc2.frequency.setValueAtTime(27.5, this.ctx.currentTime);

      this.synthFilter.type = 'lowpass';
      this.synthFilter.frequency.setValueAtTime(220, this.ctx.currentTime);

      this.synthGain.gain.setValueAtTime(0.02, this.ctx.currentTime);

      this.synthOsc.connect(this.synthFilter);
      this.synthOsc2.connect(this.synthFilter);
      this.synthFilter.connect(this.synthGain);
      this.synthGain.connect(this.masterGain);

      this.synthOsc.start();
      this.synthOsc2.start();
    } catch (e) {
      console.warn('[Audio] Synth fallback init error:', e);
    }
  }

  async loadRealAudioFiles() {
    const soundList = [
      { key: 'idle', url: 'assets/sounds/engine_idle.mp3' },
      { key: 'low', url: 'assets/sounds/engine_low_on.mp3' },
      { key: 'med', url: 'assets/sounds/engine_med_on.mp3' },
      { key: 'high', url: 'assets/sounds/engine_high_on.mp3' },
      { key: 'screech', url: 'assets/sounds/screech-1.mp3' },
      { key: 'hit1', url: 'assets/sounds/car-hit-1.mp3' },
      { key: 'hit2', url: 'assets/sounds/car-hit-2.mp3' },
      { key: 'pin', url: 'assets/sounds/pin-1.mp3' },
      { key: 'horn', url: 'assets/sounds/horn-1.mp3' },
      { key: 'flag', url: 'assets/sounds/area-1.mp3' },
      { key: 'pebbles', url: 'assets/sounds/pebbles_road.mp3' },
      { key: 'spring', url: 'assets/sounds/suspension_spring.mp3' },
      { key: 'air', url: 'assets/sounds/suspension_air.mp3' },
      { key: 'energy', url: 'assets/sounds/boost_energy.mp3' },
      { key: 'stoneCrash', url: 'assets/sounds/stone_crash.mp3' },
      { key: 'wind', url: 'assets/sounds/wind_ambience.mp3' }
    ];

    try {
      await Promise.all(soundList.map(async (item) => {
        try {
          const resp = await fetch(item.url);
          if (!resp.ok) return;
          const arrayBuf = await resp.arrayBuffer();
          const audioBuf = await this.ctx.decodeAudioData(arrayBuf);
          this.audioBuffers[item.key] = audioBuf;
        } catch (err) {
          // File fetch/decode fallback
        }
      }));

      // Setup continuous multi-track engine playback if files were decoded
      if (this.audioBuffers['idle']) {
        this.startEngineAudioLayers();
        this.isFilesLoaded = true;
        if (this.synthGain) {
          this.synthGain.gain.setValueAtTime(0, this.ctx.currentTime);
        }
      }
    } catch (e) {
      console.warn('[Audio] Using synthesized fallback:', e);
    }
  }

  startEngineAudioLayers() {
    const keys = ['idle', 'low', 'med', 'high'];
    keys.forEach(k => {
      if (!this.audioBuffers[k]) return;
      const src = this.ctx.createBufferSource();
      const gain = this.ctx.createGain();
      src.buffer = this.audioBuffers[k];
      src.loop = true;
      gain.gain.setValueAtTime(k === 'idle' ? 0.3 : 0, this.ctx.currentTime);
      src.connect(gain);
      gain.connect(this.masterGain);
      src.start(0);

      this.engineLayers[k] = { src, gain };
    });

    // Continuous road rumble loop
    if (this.audioBuffers['pebbles']) {
      const src = this.ctx.createBufferSource();
      const gain = this.ctx.createGain();
      src.buffer = this.audioBuffers['pebbles'];
      src.loop = true;
      gain.gain.setValueAtTime(0, this.ctx.currentTime);
      src.connect(gain);
      gain.connect(this.masterGain);
      src.start(0);
      this.roadRumble = { src, gain };
    }

    // Gentle ambient wind loop
    if (this.audioBuffers['wind']) {
      const src = this.ctx.createBufferSource();
      const gain = this.ctx.createGain();
      src.buffer = this.audioBuffers['wind'];
      src.loop = true;
      gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
      src.connect(gain);
      gain.connect(this.masterGain);
      src.start(0);
      this.windAmbience = { src, gain };
    }
  }

  updateEngine(speedKmh, throttle) {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.ctx.state === 'suspended') this.ctx.resume();

    const now = this.ctx.currentTime;
    const absSpeed = Math.abs(speedKmh);
    const speedNorm = Math.min(absSpeed / 120, 1.0); // 0 to 1

    if (this.isFilesLoaded && this.engineLayers['idle']) {
      // Real Multi-Track Engine Crossfade
      const idleVol = Math.max(0, 0.45 * (1 - speedNorm * 2.5));
      const lowVol = Math.max(0, 0.5 * (1 - Math.abs(speedNorm - 0.25) * 3.5));
      const medVol = Math.max(0, 0.55 * (1 - Math.abs(speedNorm - 0.55) * 3));
      const highVol = Math.max(0, 0.6 * ((speedNorm - 0.45) * 2.2));

      const throttleBoost = Math.abs(throttle) > 0 ? 1.2 : 0.6;

      this.engineLayers['idle'].gain.gain.setTargetAtTime(idleVol * (this.enabled ? 1 : 0), now, 0.08);
      if (this.engineLayers['low']) this.engineLayers['low'].gain.gain.setTargetAtTime(lowVol * throttleBoost * (this.enabled ? 1 : 0), now, 0.08);
      if (this.engineLayers['med']) this.engineLayers['med'].gain.gain.setTargetAtTime(medVol * throttleBoost * (this.enabled ? 1 : 0), now, 0.08);
      if (this.engineLayers['high']) this.engineLayers['high'].gain.gain.setTargetAtTime(highVol * throttleBoost * (this.enabled ? 1 : 0), now, 0.08);

      // Modulate pitch slightly with speed for natural acceleration sound
      const playbackRate = 0.95 + speedNorm * 0.4;
      if (this.engineLayers['high']) this.engineLayers['high'].src.playbackRate.setTargetAtTime(playbackRate, now, 0.1);
    } else if (this.synthGain) {
      // Procedural Synth Fallback Engine
      const baseFreq = 50 + speedNorm * 280;
      const targetVol = this.enabled ? (0.03 + (Math.abs(throttle) ? 0.07 : 0.015) + speedNorm * 0.04) : 0;

      this.synthOsc.frequency.setTargetAtTime(baseFreq, now, 0.05);
      this.synthOsc2.frequency.setTargetAtTime(baseFreq * 0.5, now, 0.05);
      this.synthFilter.frequency.setTargetAtTime(150 + baseFreq * 2.5, now, 0.05);
      this.synthGain.gain.setTargetAtTime(targetVol, now, 0.05);
    }
  }

  playOneShot(key, volume = 0.6) {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers[key]) {
      const src = this.ctx.createBufferSource();
      const gain = this.ctx.createGain();
      src.buffer = this.audioBuffers[key];
      gain.gain.setValueAtTime(volume, this.ctx.currentTime);
      src.connect(gain);
      gain.connect(this.masterGain);
      src.start(0);
      return;
    }
  }

  playCrash(intensity = 1.0) {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers['hit1']) {
      const key = Math.random() < 0.5 ? 'hit1' : 'hit2';
      this.playOneShot(key, Math.min(intensity * 0.5, 0.8));
      return;
    }
    // Procedural Fallback Crash
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(140, now);
    osc.frequency.exponentialRampToValueAtTime(30, now + 0.25);
    gain.gain.setValueAtTime(Math.min(intensity * 0.35, 0.6), now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(now);
    osc.stop(now + 0.3);
  }

  playHit(intensity = 1.0) {
    this.playCrash(intensity);
  }

  playScreech(intensity = 0.5) {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers['screech']) {
      if (this.lastScreechTime && this.ctx.currentTime - this.lastScreechTime < 0.35) return;
      this.lastScreechTime = this.ctx.currentTime;
      this.playOneShot('screech', Math.min(intensity * 0.45, 0.6));
    }
  }

  playHorn() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers['horn']) {
      this.playOneShot('horn', 0.8);
      return;
    }
    // Procedural Horn
    const now = this.ctx.currentTime;
    [440, 554.37].forEach(f => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(f, now);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.masterGain);
      osc.start(now);
      osc.stop(now + 0.35);
    });
  }

  playHop() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(180, now);
    osc.frequency.exponentialRampToValueAtTime(380, now + 0.2);
    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(now);
    osc.stop(now + 0.25);
  }

  playNitro() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    const now = this.ctx.currentTime;
    // White noise blast + rising resonance
    const bufferSize = this.ctx.sampleRate * 0.4;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(800, now);
    filter.frequency.exponentialRampToValueAtTime(2200, now + 0.35);
    filter.Q.setValueAtTime(3.0, now);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.28, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);

    whiteNoise.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    whiteNoise.start(now);
    whiteNoise.stop(now + 0.45);
  }

  playEMP() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    const now = this.ctx.currentTime;
    // Sub-bass pitch drop + electrical zap
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(320, now);
    osc.frequency.exponentialRampToValueAtTime(25, now + 0.6);

    gain.gain.setValueAtTime(0.45, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.65);

    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(now);
    osc.stop(now + 0.7);
  }

  playFlagPickup() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers['flag']) {
      this.playOneShot('flag', 0.9);
      return;
    }
    // Chime chords
    [523.25, 659.25, 783.99, 1046.5].forEach((f, idx) => {
      const now = this.ctx.currentTime + idx * 0.07;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(f, now);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
      osc.connect(gain);
      gain.connect(this.masterGain);
      osc.start(now);
      osc.stop(now + 0.55);
    });
  }

  playBowlingPin() {
    if (!this.initialized || !this.enabled || !this.ctx) return;
    if (this.audioBuffers['pin']) {
      this.playOneShot('pin', 0.7);
    }
  }

  toggle() {
    this.enabled = !this.enabled;
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setValueAtTime(this.enabled ? 0.85 : 0, this.ctx.currentTime);
    }
    return this.enabled;
  }
}

// Global audio singleton
window.soundEngine = new SoundEngine();
