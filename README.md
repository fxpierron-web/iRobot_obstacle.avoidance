# iRobot_obstacle.avoidance
Autonomous obstacle avoidance for iRobot Create using FSM (Python, Webots)
# Webots iRobot Create – Obstacle Avoidance (FSM)

![Demo](media/demo.gif)

Autonomous obstacle avoidance for the **iRobot Create** simulated in **Webots**, implemented in **Python** using a **Finite State Machine (FSM)**.  
The robot navigates an arena with obstacles, reacts to collisions and cliffs, and recovers robustly using deterministic and stochastic logic.

---

## 🎯 Project Overview

This project demonstrates:
- Reactive autonomous navigation
- Finite State Machine control
- Differential-drive velocity control
- Multi-sensor integration (bumpers + cliff sensors)
- Robust recovery behaviour in unknown environments

The controller is designed to be **simple, readable, and extensible**, following robotics best practices.

---

## 🧠 Control Architecture

**Robot:** iRobot Create  
**Control mode:** Velocity control (differential drive)  
**Paradigm:** Finite State Machine (FSM)

### FSM States
| State     | Description |
|----------|-------------|
| FORWARD  | Default motion, robot moves forward |
| BACKUP   | Triggered on bumper or cliff detection |
| TURNING  | Recovery turn with directional or random choice |

### State Transitions
- **FORWARD → BACKUP**  
  Triggered by bumper activation or cliff detection
- **BACKUP → TURNING**  
  After a fixed reverse duration
- **TURNING → FORWARD**  
  After completing recovery turn

Randomised turn direction is used when sensor data is ambiguous, improving escape from local minima.

---

## 🔧 Sensors & Actuators

### Sensors
- Left bumper
- Right bumper
- Cliff sensors:
  - Left
  - Front-left
  - Front-right
  - Right

### Actuators
- Left wheel motor
- Right wheel motor

All devices are **validated at startup**, and the controller exits safely if a required device is missing.

---

## ⚙️ Key Engineering Decisions

- **FSM over purely reactive control**  
  Improves predictability, debugging, and extensibility.
- **Velocity control mode**  
  Matches real-world differential drive behaviour.
- **Randomised recovery turns**  
  Prevents repeated oscillations and deadlocks.
- **Explicit constants**  
  All tuning parameters are grouped and easy to modify.

---

## ▶️ How to Run

1. Install **Webots R2025a** or later  
2. Clone this repository:
   ```bash
   git clone https://github.com/fxpierron-web/webots-irobot-create-obstacle-avoidance.git
