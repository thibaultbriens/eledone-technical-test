import React, { useState, useEffect } from 'react';
import Grid from './components/Grid';
import ControlPanel from './components/ControlPanel';
import StatsPanel from './components/StatsPanel';
import { GameConfig, GameState } from './types';
import { startGame, getGameStatus, nextRound, stopGame } from './services/api';
import './App.css';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Check for existing game on component mount
  useEffect(() => {
    const checkGameStatus = async () => {
      try {
        setIsLoading(true);
        const state = await getGameStatus();
        setGameState(state);
        setError(null);
      } catch (err) {
        // It's normal to get a 404 if no game is active
        if (!(err instanceof Error && err.message.includes("No game found"))) {
          setError(`Error checking game status: ${err instanceof Error ? err.message : String(err)}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    checkGameStatus();
  }, []);

  // Check if the game is complete
  useEffect(() => {
    if (gameState && gameState.waste_collected === gameState.total_wastes && gameState.total_wastes > 0) {
      // The game has completed automatically - no need to call stopGame again
      // The success message will be shown on the grid
    }
  }, [gameState]);

  const handleStart = async (config: GameConfig) => {
    try {
      setIsLoading(true);
      setError(null);
      const newGameState = await startGame(config);
      setGameState(newGameState);
    } catch (err) {
      setError(`Failed to start game: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await stopGame();
      setGameState(null);
    } catch (err) {
      setError(`Failed to stop game: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNextRound = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const newGameState = await nextRound();
      setGameState(newGameState);
    } catch (err) {
      setError(`Failed to advance to next round: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Wall-E Waste Collection Simulation</h1>
      </header>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <ControlPanel
        onStart={handleStart}
        onStop={handleStop}
        onNextRound={handleNextRound}
        isGameActive={!!gameState && !(gameState.waste_collected === gameState.total_wastes)}
      />
      
      <div className="main-content">
        <Grid gameState={gameState} />
        <StatsPanel gameState={gameState} />
      </div>

      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
        </div>
      )}
    </div>
  );
};

export default App;
