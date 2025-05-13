import React from 'react';
import { GameState } from '../types';
import './StatsPanel.css';

interface StatsPanelProps {
  gameState: GameState | null;
}

const StatsPanel: React.FC<StatsPanelProps> = ({ gameState }) => {
  if (!gameState) {
    return (
      <div className="stats-panel">
        <h2>Game Statistics</h2>
        <p className="no-game">No active game</p>
      </div>
    );
  }

  // Calculate remaining wastes
  const remainingWastes = gameState.total_wastes - gameState.waste_collected;
  
  // Calculate completion percentage
  const completionPercentage = Math.round((gameState.waste_collected / gameState.total_wastes) * 100);

  return (
    <div className="stats-panel">
      <h2>Game Statistics</h2>
      
      <div className="stat-item">
        <span className="stat-label">Current Turn:</span>
        <span className="stat-value">{gameState.turn_number}</span>
      </div>
      
      <div className="stat-item">
        <span className="stat-label">Wastes Collected:</span>
        <span className="stat-value">{gameState.waste_collected} / {gameState.total_wastes}</span>
      </div>
      
      <div className="stat-item">
        <span className="stat-label">Wastes Remaining:</span>
        <span className="stat-value">{remainingWastes}</span>
      </div>
      
      <div className="stat-item">
        <span className="stat-label">Completion:</span>
        <span className="stat-value">{completionPercentage}%</span>
      </div>
      
      <div className="stat-item">
        <span className="stat-label">Agents:</span>
        <span className="stat-value">{gameState.agent_positions.length}</span>
      </div>
      
      <div className="stat-item">
        <span className="stat-label">Base Position:</span>
        <span className="stat-value">[{gameState.base_position[0]}, {gameState.base_position[1]}]</span>
      </div>
      
      <div className="progress-container">
        <div 
          className="progress-bar" 
          style={{ width: `${completionPercentage}%` }}
        />
      </div>
    </div>
  );
};

export default StatsPanel;
