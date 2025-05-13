# Wall-E Waste Collection Simulation

This project consists of a Django REST API backend and a TypeScript React frontend that together simulate a waste collection game featuring autonomous agents (inspired by Wall-E). It was developed as a technical assessment for Eledone.

## Installation

### Backend Setup

1. Clone the repository
2. Install the dependencies (recommended in a virtual environment)
   ```
   pip install django djangorestframework
   ```
3. Configure the database
   ```
   cd backend
   python manage.py makemigrations walle
   python manage.py migrate walle
   ```
4. Launch the backend server
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory
   ```
   cd frontend
   ```
2. Install dependencies
   ```
   npm install
   ```
3. Start the development server
   ```
   npm run dev
   ```

## How to Play

1. Set the game parameters in the control panel:
   - Number of cleaning agents
   - Number of waste items
   - Base position (X,Y coordinates)
2. Click "Start Game" to initialize the simulation
3. Use "Next Round" to advance the simulation step by step
4. Click "Stop Game" to end the current simulation

## API Documentation

The API exposes several endpoints to manage the waste collection simulation.

### Start a new simulation

**Endpoint:** `POST /start/`

Starts a new simulation with the specified parameters.

**Body:**

- `num_agents`: Number of cleaning agents (integer)
- `num_wastes`: Number of waste items to collect (integer)
- `base_position_x`: Base X position (integer, 0-31)
- `base_position_y`: Base Y position (integer, 0-31)

**Request example:**

```json
{
  "num_agents": 5,
  "num_wastes": 20,
  "base_position_x": 15,
  "base_position_y": 15
}
```

**Response example:**

```json
{
  "waste_collected": 0,
  "total_wastes": 20,
  "agent_positions": [[x1, y1, false], [x2, y2, false], ...],
  "waste_positions": [[x1, y1], [x2, y2], ...],
  "base_position": [15, 15],
  "turn_number": 0
}
```

### Get the current simulation state

**Endpoint:** `GET /status/`

Returns the current state of the ongoing simulation.

**Response example:**

```json
{
  "waste_collected": 5,
  "total_wastes": 20,
  "agent_positions": [[x1, y1, true], [x2, y2, false], ...],
  "waste_positions": [[x1, y1], [x2, y2], ...],
  "base_position": [15, 15],
  "turn_number": 10
}
```

### Proceed to the next turn

**Endpoint:** `POST /next/`

Advances the simulation by one turn, agents move according to the game logic.

**Response example:**

```json
{
  "waste_collected": 6,
  "total_wastes": 20,
  "agent_positions": [[x1, y1, false], [x2, y2, true], ...],
  "waste_positions": [[x1, y1], [x2, y2], ...],
  "base_position": [15, 15],
  "turn_number": 11
}
```

### Stop the simulation

**Endpoint:** `POST /stop/`

Stops the current simulation and deletes the game data.

**Response example:**

```json
{
  "waste_collected": 6,
  "total_wastes": 20,
  "agent_positions": [[x1, y1, false], [x2, y2, true], ...],
  "waste_positions": [[x1, y1], [x2, y2], ...],
  "base_position": [15, 15],
  "turn_number": 11
}
```
