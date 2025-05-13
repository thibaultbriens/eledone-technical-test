import { GameConfig, GameState } from '../types';

const BASE_URL = '/api';

export async function startGame(config: GameConfig): Promise<GameState> {
  const response = await fetch(`${BASE_URL}/start/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to start game');
  }

  return response.json();
}

export async function getGameStatus(): Promise<GameState> {
  const response = await fetch(`${BASE_URL}/stats/`);

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to get game status');
  }

  return response.json();
}

export async function nextRound(): Promise<GameState> {
  const response = await fetch(`${BASE_URL}/next-round/`, {
    method: 'POST',
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to advance to next round');
  }

  return response.json();
}

export async function stopGame(): Promise<GameState> {
  const response = await fetch(`${BASE_URL}/stop/`, {
    method: 'POST',
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to stop game');
  }

  return response.json();
}
