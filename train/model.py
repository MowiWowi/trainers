from stable_baselines3 import PPO
from game_env import ShooterEnv

def create_model():
    env = ShooterEnv()
    model = PPO('MlpPolicy', env, verbose=1)
    return model
