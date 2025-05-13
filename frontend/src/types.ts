export interface GameConfig {
  num_agents: number;
  num_wastes: number;
  base_position_x: number;
  base_position_y: number;
}

export interface GameState {
  waste_collected: number;
  total_wastes: number;
  agent_positions: [number, number, boolean][]; // [x, y, hasWaste]
  waste_positions: [number, number][]; // [x, y]
  base_position: [number, number]; // [x, y]
  turn_number: number;
}

export interface Cell {
  x: number;
  y: number;
  type: 'empty' | 'base' | 'waste' | 'agent' | 'agentWithWaste';
}
