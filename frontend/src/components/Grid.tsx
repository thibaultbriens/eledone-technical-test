import React from 'react';
import { GameState } from '../types';
import './Grid.css';

interface GridProps {
  gameState: GameState | null;
}

const Grid: React.FC<GridProps> = ({ gameState }) => {
  if (!gameState) {
    return <div className="grid-container empty-grid">No active game</div>;
  }

  // Generate a 32x32 grid
  const grid = Array.from({ length: 32 }, (_, y) =>
    Array.from({ length: 32 }, (_, x) => {
      // Default cell is empty
      let cellType = 'empty';

      // Check if this cell is the base
      if (gameState.base_position[0] === x && gameState.base_position[1] === y) {
        cellType = 'base';
      } 
      // Check if this cell has waste
      else if (gameState.waste_positions.some(pos => pos[0] === x && pos[1] === y)) {
        cellType = 'waste';
      }
      
      // Check if this cell has an agent
      const agent = gameState.agent_positions.find(pos => pos[0] === x && pos[1] === y);
      if (agent) {
        cellType = agent[2] ? 'agentWithWaste' : 'agent';
      }

      return cellType;
    })
  );

  return (
    <div className="grid-container">
      {grid.map((row, y) => (
        <div key={y} className="grid-row">
          {row.map((cellType, x) => (
            <div
              key={`${x}-${y}`}
              className={`grid-cell ${cellType}`}
              data-x={x}
              data-y={y}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Grid;
