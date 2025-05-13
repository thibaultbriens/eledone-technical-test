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

  // Check if the game is complete (all waste collected)
  const isGameComplete = gameState.waste_collected === gameState.total_wastes;

  // Generate a 32x32 grid
  const grid = Array.from({ length: 32 }, (_, y) =>
    Array.from({ length: 32 }, (_, x) => {
      // Check if this cell has an agent
      const agent = gameState.agent_positions.find(pos => pos[0] === x && pos[1] === y);
      // Check if this cell is the base
      const isBase = gameState.base_position[0] === x && gameState.base_position[1] === y;
      // Check if this cell has waste
      const hasWaste = gameState.waste_positions.some(pos => pos[0] === x && pos[1] === y);
      
      // Classes to apply to this cell
      const classes = [];
      
      if (isBase) {
        classes.push('base');
      }
      
      if (hasWaste) {
        classes.push('waste');
      }
      
      if (agent) {
        classes.push(agent[2] ? 'agentWithWaste' : 'agent');
      }
      
      return classes.join(' ');
    })
  );

  return (
    <div className="grid-container">
      {grid.map((row, y) => (
        <div key={y} className="grid-row">
          {row.map((cellClasses, x) => (
            <div
              key={`${x}-${y}`}
              className={`grid-cell ${cellClasses}`}
              data-x={x}
              data-y={y}
            />
          ))}
        </div>
      ))}
      
      {isGameComplete && (
        <div className="success-overlay">
          <div className="success-message">
            <h2>Mission Complete!</h2>
            <p>All waste has been successfully collected.</p>
            <div className="final-stats">
              <div className="stat-item">
                <span className="stat-label">Total Turns:</span>
                <span className="stat-value">{gameState.turn_number}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Waste Collected:</span>
                <span className="stat-value">{gameState.waste_collected} / {gameState.total_wastes}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Agents Used:</span>
                <span className="stat-value">{gameState.agent_positions.length}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Grid;
