from stable_baselines3 import PPO
from game_env import ShooterEnv  # Ensure this is your environment file
import pygame
pygame.init()
def main():
    # Load the trained model
    try:
        model = PPO.load("shooter_model")
        print("Model loaded successfully.")
    except FileNotFoundError:
        print("Model file 'shooter_model.zip' not found. Please train the model first.")
        return

    # Create the environment
    env = ShooterEnv()

    obs = env.reset()
    done = False

    print("Observing the trained bot. Close the Pygame window to stop.")

    try:
        while True:
            # Handle Pygame events to allow window closure
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt("Pygame window closed by user.")

            # Get action from the model
            action, _states = model.predict(obs, deterministic=True)
            
            # Take action in the environment
            obs, reward, done, info = env.step(action)
            
            # Render the environment
            env.render()

            if done:
                print("Bot has been hit. Resetting environment.")
                obs = env.reset()

    except KeyboardInterrupt:
        print("Observation interrupted by user.")
    finally:
        env.close()

if __name__ == "__main__":
    main()
