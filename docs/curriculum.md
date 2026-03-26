### Top-level UI Sections (Sidebar)

```
1. Signal Foundations
2. Systems & Convolution
3. Frequency Domain
4. Analog Communication
5. Digital Communication
6. Channel & Noise
7. Summary / Playground
```

Each section contains **small, focused lessons**, not huge pages.

---

# 2. Full Curriculum (Beginner → Complete)

I will mark:

- 🟢 **Beginner Entry Point**
- ⭐ **Core / must-understand**
- 🔵 **Advanced but important**

---

## SECTION 1: Signal Foundations 🟢

_(This is where every beginner starts)_

### 1.1 What is a Signal?

- Continuous-time vs Discrete-time
- Physical meaning (sound, voltage)
- Time axis intuition

**UI**

- Signal selector
- Time axis slider

---

### 1.2 Basic Signals ⭐

- Unit impulse
- Unit step
- Ramp
- Exponential
- Sinusoidal signal

**UI**

- Dropdown: signal type
- Sliders: amplitude, frequency, phase
- Single time-domain plot

---

### 1.3 Operations on Signals ⭐

- Time shifting
- Time scaling
- Time reversal
- Amplitude scaling

**UI**

- Slider for shift
- Toggle for reverse
- Before vs after plot

---

### 1.4 Energy & Power of Signals ⭐

- Energy signals
- Power signals
- Why this matters in communication

**UI**

- Energy calculation display
- Power over time plot

---

## SECTION 2: Systems & Convolution ⭐

_(This is the heart of Signals & Systems)_

### 2.1 What is a System?

- Input → Output
- Block diagram thinking

**UI**

- Input signal
- System response
- Output plot

---

### 2.2 System Properties

- Linearity
- Time-invariance
- Causality
- Stability

**UI**

- Toggle each property
- See output change

---

### 2.3 Impulse Response ⭐

- Why impulse matters
- System characterization

**UI**

- Choose impulse response
- Observe output

---

### 2.4 Convolution (Conceptual) ⭐

- Mathematical definition
- Why convolution exists

**UI**

- Step-by-step convolution animation (later)
- Input + impulse response

---

### 2.5 Convolution (Practical)

- Continuous vs discrete convolution
- Effect of impulse width

**UI**

- Slider-controlled convolution
- Final output plot

---

## SECTION 3: Frequency Domain ⭐

_(Where intuition usually breaks — your app shines here)_

### 3.1 Why Frequency Domain?

- Time vs frequency intuition
- Spectral representation

**UI**

- Time ↔ frequency toggle

---

### 3.2 Fourier Series (Intro)

- Periodic signals
- Harmonics

**UI**

- Number of harmonics slider
- Reconstructed signal

---

### 3.3 Fourier Transform ⭐

- Non-periodic signals
- Magnitude & phase

**UI**

- Time signal
- Magnitude spectrum
- Phase spectrum

---

### 3.4 Power Spectrum ⭐

- PSD meaning
- Bandwidth

**UI**

- Noise toggle
- Bandwidth highlight

---

### 3.5 Filtering

- Low-pass
- High-pass
- Band-pass

**UI**

- Cutoff frequency slider
- Before/after spectrum

---

## SECTION 4: Analog Communication ⭐

_(Now we actually transmit information)_

### 4.1 Why Modulation?

- Baseband vs passband
- Antenna size intuition

---

### 4.2 Amplitude Modulation (AM) ⭐

- Carrier
- Message signal
- Modulated signal

**UI**

- Message frequency
- Carrier frequency
- Modulation index

---

### 4.3 AM Spectrum

- Sidebands
- Bandwidth

**UI**

- Frequency-domain visualization

---

### 4.4 AM Demodulation

- Envelope detector
- Distortion

**UI**

- Demodulated signal
- Noise toggle

---

### 4.5 Frequency Modulation (FM) 🔵

- Frequency deviation
- Bandwidth

---

## SECTION 5: Digital Communication ⭐

_(Modern communication)_

### 5.1 Sampling ⭐

- Nyquist theorem
- Aliasing

**UI**

- Sampling frequency slider
- Aliasing visualization

---

### 5.2 Quantization ⭐

- Uniform quantization
- Quantization noise

**UI**

- Bits slider
- Error plot

---

### 5.3 Pulse Code Modulation (PCM)

- Encoder/decoder

---

### 5.4 Digital Modulation ⭐

- ASK
- FSK
- PSK

**UI**

- Bit stream
- Symbol mapping

---

### 5.5 Eye Diagram 🔵

- Noise effect
- ISI

---

## SECTION 6: Channel & Noise ⭐

### 6.1 Noise Models

- AWGN
- SNR

---

### 6.2 Channel Effects

- Attenuation
- Distortion

---

### 6.3 BER vs SNR 🔵

- Performance intuition

---

## SECTION 7: Playground / Summary 🎯

- Free signal builder
- Combine blocks
- Experiment without guidance

This is where users **test intuition**.

---
