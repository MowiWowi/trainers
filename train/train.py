import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from game_env import ShooterEnv  # Make sure this is your environment file

class RenderCallback(BaseCallback):
    """
    Custom callback for rendering the environment during training.
    """
    def __init__(self, verbose=0):
        super(RenderCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Render every step
        self.training_env.envs[0].render()
        return True

# Create the environment
env = DummyVecEnv([lambda: ShooterEnv()])

# Initialize the PPO model with adjusted parameters
model = PPO(
    "MlpPolicy", 
    env, 
    verbose=1, 
    ent_coef=0.02,    # Increase exploration to encourage new actions
    gamma=0.97        # Slightly lower discount factor to focus on immediate actions
)

# Initialize the custom callback
render_callback = RenderCallback()

try:
    print("Training started. Close the Pygame window to stop training.")
    
    # Training loop
    while True:
        # Train the model in chunks of timesteps
        model.learn(total_timesteps=1000, callback=render_callback)
        
        # Save the model after each chunk
        model.save("shooter_model")
        print("Model saved as 'shooter_model.zip'")
        
except KeyboardInterrupt:
    print("Training interrupted by user.")
    model.save("shooter_model")
    print("Final model saved as 'shooter_model.zip'")
finally:
    env.close()
