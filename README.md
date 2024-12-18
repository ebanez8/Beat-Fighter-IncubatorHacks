# Beat Fighter - README

https://www.youtube.com/watch?v=xerIO8IrcDI&ab_channel=EvanZhou

## Introduction
**Beat Fighter** is a rhythm-based fighting game created with Python and Pygame. Players must hit incoming notes accurately by pressing corresponding directional keys. Successful hits will attack the enemy, while misses reduce the player's health. With a mix of animations, health bars, and a scoring system, Beat Fighter delivers an engaging arcade experience.

<img width="1866" alt="Beat fighter" src="https://github.com/user-attachments/assets/904b5148-9ca5-4a3e-9400-ee73ff901ae1">


## Features
- **Rhythm-Based Gameplay**: Notes spawn in sync with a beat, and players must hit them in time to deal damage to the enemy.
- **Enemy Attack Animation**: The enemy retaliates on missed notes, adding intensity to the gameplay.
- **Score and Health System**: Track your score and monitor your health and enemy’s health through visual health bars.
- **Multiple Tracks and Animations**: Each track has unique animations to keep gameplay visually dynamic.

## Requirements
- Python 3.x
- Pygame library

To install Pygame:
```bash
pip install pygame
```
## Game Controls
- **Arrow Keys:** Press the corresponding arrow keys (←, ↓, ↑, →) to match notes.
- **Quit:** Press the close button on the window or ESC key.
## File Structure
- **bg.png:** Background image.
- **character.png:** Idle player character image.
- **enemy.png:** Idle enemy character image.
- **Animation Frames:** Files like characterp1.1.png, characterp1.2.png, characterp1.3.png, enemyp1.1.png, enemyp1.2.png, enemyp1.3.png, etc., used for player and enemy animations.
## How to Play
- Clone the repository and ensure all images are in the same directory as the code.
- Run the script using Python:
- bash
- Copy code
- python beat_fighter.py
- Follow the beat and press the corresponding arrow keys when notes align with the hit zone.
## Key Classes and Methods
- **Note:** Handles note properties and movement.
- **Game:** Main game loop, note spawning, health updates, score management, and rendering functions.
- **spawn_note:** Generates notes on random tracks.
- **draw_health_bar:** Draws the player's health bar.
- **check_note_hit:** Checks if a note is hit and animates accordingly.
- **update:** Updates game state, animations, and health.
- **draw:** Renders graphics on the screen
## Credits
- **Evan Zhou**
- **Vijay Shrivarshan Vijayaraja**
- **Aiden Lim**
- **Allan Wang**
