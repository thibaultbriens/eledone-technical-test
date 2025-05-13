import React, { useState } from 'react';
import { GameConfig } from '../types';
import './ControlPanel.css';

interface ControlPanelProps {
  onStart: (config: GameConfig) => void;
  onStop: () => void;
  onNextRound: () => void;
  isGameActive: boolean;
}

const ControlPanel: React.FC<ControlPanelProps> = ({ 
  onStart, 
  onStop, 
  onNextRound,
  isGameActive 
}) => {
  const [config, setConfig] = useState<GameConfig>({
    num_agents: 5,
    num_wastes: 20,
    base_position_x: 15,
    base_position_y: 15,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: parseInt(value, 10)
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Empêche le comportement par défaut du formulaire
    onStart(config);
  };

  return (
    <div className="control-panel">
      <h2>Game Controls</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="num_agents">Number of Agents:</label>
          <input
            type="number"
            id="num_agents"
            name="num_agents"
            min="1"
            max="1000"
            value={config.num_agents}
            onChange={handleChange}
            disabled={isGameActive}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="num_wastes">Number of Wastes:</label>
          <input
            type="number"
            id="num_wastes"
            name="num_wastes"
            min="1"
            max="1000"
            value={config.num_wastes}
            onChange={handleChange}
            disabled={isGameActive}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="base_position_x">Base Position X:</label>
          <input
            type="number"
            id="base_position_x"
            name="base_position_x"
            min="0"
            max="31"
            value={config.base_position_x}
            onChange={handleChange}
            disabled={isGameActive}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="base_position_y">Base Position Y:</label>
          <input
            type="number"
            id="base_position_y"
            name="base_position_y"
            min="0"
            max="31"
            value={config.base_position_y}
            onChange={handleChange}
            disabled={isGameActive}
          />
        </div>
        
        <div className="button-group">
          <button 
            type="submit" 
            className="btn start-btn"
            disabled={isGameActive}
          >
            Start Game
          </button>
          
          <button 
            type="button" 
            className="btn next-btn"
            onClick={onNextRound}
            disabled={!isGameActive}
          >
            Next Round
          </button>
          
          <button 
            type="button" 
            className="btn stop-btn"
            onClick={onStop}
            disabled={!isGameActive}
          >
            Stop Game
          </button>
        </div>
      </form>
    </div>
  );
};

export default ControlPanel;
