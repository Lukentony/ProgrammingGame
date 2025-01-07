import pygame
import sys
from level import load_levels
from ui_elements import Button, VirtualKeyboard

class ProgrammingGame:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Impara la Programmazione")
        self.clock = pygame.time.Clock()

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (200, 200, 200)

        # Font
        self.font = pygame.font.Font(None, 28)

        # Game States
        self.current_level = 0
        self.score = 0
        self.current_input = []
        self.feedback = ""
        self.show_keyboard = False
        self.player_name = ""
        self.show_congratulations = False

        # Input Box (Multiline)
        self.input_box = pygame.Rect(20, 200, 760, 150)
        self.line_height = 32  # Line height for text rendering

        # Levels
        self.levels = load_levels("levels.json")

        # UI Elements
        self.keyboard_button = Button(650, 500, 120, 40, "Keyboard", self.font)
        self.enter_button = Button(650, 550, 120, 40, "Enter", self.font)  # Always visible Enter button
        self.virtual_keyboard = VirtualKeyboard(self.font)
        self.next_level_button = Button(300, 400, 200, 50, "Next Level", self.font)

        # State Flags
        self.start_screen = True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.start_screen:
                        self.handle_name_input(event)
                    elif not self.start_screen and not self.show_congratulations:
                        self.handle_text_input(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_mouse_click(self, event):
        x, y = event.pos

        if self.start_screen:
            return  # No clickable UI elements on the start screen

        if self.show_congratulations:
            # Handle "Next Level" button
            if self.next_level_button.is_clicked(x, y):
                self.show_congratulations = False  # Hide congratulations
                self.current_input = []  # Reset input for the next level
                return

        # Keyboard toggle button
        if self.keyboard_button.is_clicked(x, y):
            self.show_keyboard = not self.show_keyboard

        # Always-visible "Enter" button
        if self.enter_button.is_clicked(x, y):
            self.check_answer()

        # Virtual keyboard
        if self.show_keyboard and not self.show_congratulations:
            key = self.virtual_keyboard.get_key_at(x, y)
            if key == "Enter":
                self.check_answer()
            elif key:
                self.add_character_to_input(key)

        # Restart button (if on victory screen)
        if self.current_level >= len(self.levels) and 300 <= x <= 500 and 500 <= y <= 550:
            self.restart_game()

    def handle_name_input(self, event):
        """Handle name input on the start screen."""
        if event.key == pygame.K_RETURN and self.player_name.strip():
            self.start_screen = False  # Move to the game
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        else:
            self.player_name += event.unicode

    def handle_text_input(self, event):
        """Handle multiline input for the game."""
        if event.key == pygame.K_RETURN:
            self.add_character_to_input("\n")  # Add newline for multiline
        elif event.key == pygame.K_BACKSPACE:
            self.remove_character_from_input()
        else:
            self.add_character_to_input(event.unicode)

    def add_character_to_input(self, char):
        """Add a character (or newline) to the input."""
        if not self.current_input:
            self.current_input.append("")
        if char == "\n":
            self.current_input.append("")
        else:
            self.current_input[-1] += char

    def remove_character_from_input(self):
        """Remove a character, handling backspace across lines."""
        if not self.current_input:
            return
        if not self.current_input[-1]:
            self.current_input.pop()
        else:
            self.current_input[-1] = self.current_input[-1][:-1]

    def restart_game(self):
        """Restart the game."""
        self.current_level = 0
        self.score = 0
        self.current_input = []
        self.feedback = ""
        self.show_keyboard = False
        self.show_congratulations = False

    def update(self):
        """Update game state."""
        if self.current_level >= len(self.levels):
            return  # Victory screen

    def draw(self):
        """Render the game."""
        self.screen.fill(self.WHITE)

        if self.start_screen:
            self.draw_start_screen()
        elif self.current_level >= len(self.levels):
            self.draw_victory_screen()
        elif self.show_congratulations:
            self.draw_congratulations_screen()
        else:
            self.draw_game_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        """Render the start screen where the player enters their name."""
        title = self.font.render("Impara la Programmazione", True, self.BLACK)
        self.screen.blit(title, (self.width // 2 - 150, 100))

        prompt = self.font.render("Inserisci il tuo nome:", True, self.BLACK)
        self.screen.blit(prompt, (self.width // 2 - 150, 200))

        name_surface = self.font.render(self.player_name, True, self.BLUE)
        pygame.draw.rect(self.screen, self.GRAY, (self.width // 2 - 150, 250, 300, 50), 2)
        self.screen.blit(name_surface, (self.width // 2 - 140, 260))

    def draw_game_screen(self):
        """Render the main game screen."""
        current_level = self.levels[self.current_level]
        title = self.font.render(f"Livello {self.current_level + 1}: {current_level.title}", True, self.BLACK)
        instructions = self.font.render(current_level.instructions, True, self.BLACK)
        feedback_surface = self.font.render(self.feedback, True, self.RED if "Incorrect" in self.feedback else self.GREEN)

        # Draw input box
        pygame.draw.rect(self.screen, self.GRAY, self.input_box, 2)
        for i, line in enumerate(self.current_input):
            line_surface = self.font.render(line, True, self.BLUE)
            self.screen.blit(line_surface, (self.input_box.x + 5, self.input_box.y + 5 + i * self.line_height))

        self.screen.blit(title, (20, 20))
        self.screen.blit(instructions, (20, 80))
        self.screen.blit(feedback_surface, (20, 360))

        # Draw UI Buttons
        self.keyboard_button.draw(self.screen)
        self.enter_button.draw(self.screen)

        # Draw virtual keyboard if visible
        if self.show_keyboard:
            self.virtual_keyboard.draw(self.screen, show_keyboard=True)

    def draw_congratulations_screen(self):
        """Render the congratulations screen after completing a level."""
        congrats_text = self.font.render("Congratulazioni!", True, self.GREEN)
        score_text = self.font.render(f"Punteggio: {self.score}", True, self.BLACK)

        self.screen.blit(congrats_text, (self.width // 2 - 100, 200))
        self.screen.blit(score_text, (self.width // 2 - 100, 260))
        self.next_level_button.draw(self.screen)

    def draw_victory_screen(self):
        """Render the victory screen."""
        victory_text = self.font.render(f"Congratulazioni, {self.player_name}! Punteggio: {self.score}", True, self.BLACK)
        restart_text = self.font.render("Restart", True, self.WHITE)
        restart_button_rect = pygame.Rect(300, 500, 200, 50)

        self.screen.blit(victory_text, (self.width // 2 - 200, self.height // 2 - 50))
        pygame.draw.rect(self.screen, self.BLACK, restart_button_rect)
        self.screen.blit(restart_text, (restart_button_rect.x + 50, restart_button_rect.y + 10))

    def check_answer(self):
        """Validate the user's input."""
        user_input = "\n".join(self.current_input).strip()  # Combine multiline input
        correct_answers = [ans.strip() for ans in self.levels[self.current_level].valid_answers]

        if user_input in correct_answers:
            self.score += 1
            self.current_level += 1
            self.current_input = []
            self.feedback = ""
            if self.current_level < len(self.levels):
                self.show_congratulations = True  # Show congratulations only if there are more levels
            else:
                self.show_congratulations = False
        else:
            self.feedback = "Incorrect! Try again."
