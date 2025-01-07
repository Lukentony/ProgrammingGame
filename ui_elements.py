import pygame

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def draw(self, screen):
        """Render the button."""
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, mouse_x, mouse_y):
        """Check if the button was clicked."""
        return self.rect.collidepoint(mouse_x, mouse_y)

class VirtualKeyboard:
    def __init__(self, font):
        self.font = font
        self.keys = "1234567890abcdefghijklmnopqrstuvwxyz=<>: "
        self.enter_key = Button(650, 400, 120, 40, "Enter", font)  # Always visible "Enter"

    def draw(self, screen, show_keyboard):
        """Render the virtual keyboard."""
        if show_keyboard:
            for i, char in enumerate(self.keys):
                key_x = 20 + (i % 10) * 50
                key_y = 400 + (i // 10) * 50
                pygame.draw.rect(screen, (0, 0, 0), (key_x, key_y, 40, 40), 2)
                key_surface = self.font.render(char, True, (0, 0, 0))
                screen.blit(key_surface, (key_x + 10, key_y + 10))

        # Always render the Enter key
        self.enter_key.draw(screen)

    def get_key_at(self, x, y):
        """Get the key pressed based on mouse coordinates."""
        if self.enter_key.is_clicked(x, y):
            return "Enter"
        if x < 20 or y < 400:
            return None  # Out of keyboard range
        for i, char in enumerate(self.keys):
            key_x = 20 + (i % 10) * 50
            key_y = 400 + (i // 10) * 50
            if key_x <= x <= key_x + 40 and key_y <= y <= key_y + 40:
                return char
        return None
