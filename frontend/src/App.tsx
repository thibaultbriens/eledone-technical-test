import React, { useState, useEffect, useRef } from 'react';
import Grid from './components/Grid';
import ControlPanel from './components/ControlPanel';
import StatsPanel from './components/StatsPanel';
import { GameConfig, GameState } from './types';
import { startGame, getGameStatus, nextRound, stopGame } from './services/api';
import './App.css';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPaused, setIsPaused] = useState(false);
  const [isAutoRunning, setIsAutoRunning] = useState(false);
  const autoRunIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const roundInterval = 300; // 300ms

  // Check for existing game on component mount
  useEffect(() => {
    const checkGameStatus = async () => {
      try {
        const state = await getGameStatus();
        setGameState(state);
        setError(null);
      } catch (err) {
        // It's normal to get a 404 if no game is active
        if (!(err instanceof Error && err.message.includes("No game found"))) {
          setError(`Error checking game status: ${err instanceof Error ? err.message : String(err)}`);
        }
      }
    };

    checkGameStatus();
  }, []);

  // Clear interval on unmount
  useEffect(() => {
    return () => {
      if (autoRunIntervalRef.current) {
        clearInterval(autoRunIntervalRef.current);
      }
    };
  }, []);

  // Check if the game is complete
  useEffect(() => {
    if (gameState && gameState.waste_collected === gameState.total_wastes && gameState.total_wastes > 0) {
      // The game has completed automatically
      stopAutoRun();
    }
  }, [gameState]);

  const stopAutoRun = () => {
    if (autoRunIntervalRef.current) {
      clearInterval(autoRunIntervalRef.current);
      autoRunIntervalRef.current = null;
    }
    setIsAutoRunning(false);
  };

  const startAutoRun = () => {
    if (!gameState || gameState.waste_collected === gameState.total_wastes) return;
    
    setIsPaused(false);
    setIsAutoRunning(true);
    
    autoRunIntervalRef.current = setInterval(async () => {
      try {
        const newGameState = await nextRound();
        setGameState(newGameState);
        
        // Check if game is complete
        if (newGameState.waste_collected === newGameState.total_wastes) {
          stopAutoRun();
        }
      } catch (err) {
        setError(`Failed to advance to next round: ${err instanceof Error ? err.message : String(err)}`);
        stopAutoRun();
        setIsPaused(true);
      }
    }, roundInterval); // Run next round every 300ms
  };

  const handleStart = async (config: GameConfig) => {
    try {
      // If game is complete or no game is active, start a new game
      if (!gameState || isGameComplete) {
        setError(null);
        const newGameState = await startGame(config);
        setGameState(newGameState);
        
        // Use the received game state directly instead of relying on the updated state beacuase React is not guaranteed to update immediately
        setTimeout(() => {
          if (newGameState && newGameState.waste_collected < newGameState.total_wastes) {
            setIsPaused(false);
            setIsAutoRunning(true);
            
            autoRunIntervalRef.current = setInterval(async () => {
              try {
                const updatedState = await nextRound();
                setGameState(updatedState);
                
                // Check if game is complete
                if (updatedState.waste_collected === updatedState.total_wastes) {
                  stopAutoRun();
                }
              } catch (err) {
                setError(`Failed to advance to next round: ${err instanceof Error ? err.message : String(err)}`);
                stopAutoRun();
                setIsPaused(true);
              }
            }, roundInterval);
          }
        }, 100);
        return;
      }
      
      // If game exists but is paused, resume it
      if (isPaused) {
        setIsPaused(false);
        startAutoRun();
        return;
      }
      
      // If game is running, pause it
      stopAutoRun();
      setIsPaused(true);
      
    } catch (err) {
      setError(`Failed to start/pause/resume game: ${err instanceof Error ? err.message : String(err)}`);
    }
  };

  const handleStop = async () => {
    try {
      // First stop the auto run
      stopAutoRun();
      
      setError(null);
      await stopGame();
      setGameState(null);
      setIsPaused(false);
    } catch (err) {
      setError(`Failed to stop game: ${err instanceof Error ? err.message : String(err)}`);
    }
  };

  const handleNextRound = async () => {
    if (!isPaused) return;
    
    try {
      setError(null);
      const newGameState = await nextRound();
      setGameState(newGameState);
    } catch (err) {
      setError(`Failed to advance to next round: ${err instanceof Error ? err.message : String(err)}`);
    }
  };

  const isGameComplete = gameState && gameState.waste_collected === gameState.total_wastes && gameState.total_wastes > 0;
  const isGameActive = !!gameState;

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
        isGameActive={isGameActive}
        isGamePaused={isPaused}
        isAutoRunning={isAutoRunning}
        isGameComplete={isGameComplete}
      />
      
      <div className="main-content">
        <Grid gameState={gameState} />
        <StatsPanel gameState={gameState} />
      </div>
    </div>
  );
};

export default App;
