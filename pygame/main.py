import pygame
import random
import sys
import time
from pygame import mixer
import json

history = {"score": 0, "history": []}
with open('score_history.json', 'w') as file:
    json.dump(history, file)
class HangmanGame:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.first_run = True
        self.language = "Lietuvių"
        self.words = self.open_word_list(self.language)
        self.random_word = random.choice(self.words)
        self.separated_word = self.separate_word(self.random_word)
        self.hidden_word = self.hide_word(self.separated_word)
        self.missed_letters = []
        self.lifes = 6
        print(self.random_word)
        self.game_over = False
        self.history = None

        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Hangman")

        self.font = pygame.font.SysFont('freesansbold.ttf', 64)
        self.font2 = pygame.font.SysFont('freesansbold.ttf', 64)
        self.clock = pygame.time.Clock()

        self.input_box = pygame.Rect(150, 400, 150, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.grean = (0, 255, 0)
        self.black = (0, 0, 0)
        self.color = self.color_inactive
        self.input_txt = ''
        self.active = False

        self.bg = pygame.image.load("Background.png")
        self.billboard = pygame.image.load("13090.png")
        self.heart1 = pygame.image.load("heart1.png")
        self.plank = pygame.image.load("22649624_6631009.jpg")
        self.DEFAULT_IMAGE_SIZE = (200, 200)
        self.Small_Image_Size = (60, 60)
        self.billboard = pygame.transform.scale(self.billboard, self.DEFAULT_IMAGE_SIZE)
        self.heart1 = pygame.transform.scale(self.heart1, self.Small_Image_Size)

        mixer.music.load("Spooky.mp3")
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)



    def toggle_language(self):
        # Toggle between languages
        if self.language == "english":
            self.language = "Lietuvių"  
            print(self.random_word) 
        else:
            self.language = "english"    
            print(self.random_word)

        self.random_word = random.choice(self.words)
        self.separated_word = self.separate_word(self.random_word)
        self.hidden_word = self.hide_word(self.separated_word)
        self.missed_letters = []
        self.lifes = 6
        self.game_over = False


    def open_word_list(self, value):
        match value:
            case "english":
                with open('words_list.txt', 'r', encoding='utf-8') as file:
                    words = [word.strip() for word in file.readlines()]
                return words
            case "Lietuvių":
                with open('words_list2.txt', 'r', encoding='utf-8') as file:
                    words = [word.strip() for word in file.readlines()]
                return words

    def separate_word(self, word):
        return [letter for letter in word]

    def hide_word(self, letters):
        return ['_' for _ in letters]

    def reveal_letter(self, letter):
        if letter in self.missed_letters:
            return True
        revealed = False
        for i, char in enumerate(self.random_word):
            if char == letter:
                self.hidden_word[i] = letter
                revealed = True
        if not revealed:
            self.missed_letters.append(letter)
        return revealed

    def is_word_revealed(self):
        return '_' not in self.hidden_word

    def display_hidden_word(self):
        text = self.font.render(' '.join(self.hidden_word), True, self.black)
        text_rect = text.get_rect(center=(800 // 1.45, 600 // 1.9))
        resized_image = pygame.transform.scale(self.plank, (text_rect.width, text_rect.height))
        self.display.blit(resized_image, text_rect)
        self.display.blit(text, text_rect)

    def display_hearts(self, value):
        heart_x = 20
        heart_y = 20
        heart_spacing = 70
        for i in range(value):
            heart_position = (heart_x + i * heart_spacing, heart_y)
            self.display.blit(self.heart1, heart_position)
    
    def display_text(self, text,  x, y, color):
        display_the_text = self.font2.render(text, True, color)
        self.display.blit(display_the_text, (800 // 2 - display_the_text.get_width()//2 + x // 2, 600 // 2 + y))
    
    
    def save_score_history(self, won):
        # Load score and history
        try:
            with open('score_history.json', 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = {"score": 0, "history": []}

        # Update score and history
        self.history["history"].append({"word": self.random_word, "result": "won" if won else "lost"})
        if won:
            self.history["score"] += 1

        # Save updated data to file
        with open('score_history.json', 'w') as file:
            json.dump(self.history, file)

    def load_score(self):
        try:
            with open('score_history.json', 'r') as file:
                data = json.load(file)
            return data["score"]
        except FileNotFoundError:
            print("Score history file not found.")
            return 0   
    def run(self):
        while True:
            self.display.fill((255, 255, 255))
            self.display.blit(self.bg, (0, 0))
            self.display.blit(self.billboard, (100, 318))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.language_button_rect.collidepoint(event.pos):
                        self.toggle_language()
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive

                if event.type == pygame.KEYDOWN and self.game_over != True:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            if self.input_txt:
                                if not self.reveal_letter(self.input_txt):
                                    self.lifes -= 1
                                self.input_txt = ''

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_txt = self.input_txt[:-1]
                        else:
                            self.input_txt = event.unicode
                        if len(self.input_txt) > 1:
                            self.input_txt = self.input_txt[:-1]
                
            language_text = "EN" if self.language == "english" else "LT"
            language_button_text = self.font.render(language_text, True, (0, 0, 0))
            self.language_button_rect = language_button_text.get_rect(topright=(780, 550))
            pygame.draw.rect(self.display, (255, 255, 255), self.language_button_rect)
            self.display.blit(language_button_text, self.language_button_rect)

            self.display_hidden_word()
            self.display_hearts(self.lifes)
            txt_surface = self.font.render(self.input_txt, True, self.color)
            self.input_box.w = max(100, txt_surface.get_width() + 10)
            self.input_box.h = max(80, 10)
            self.display.blit(txt_surface, (self.input_box.x + 38, self.input_box.y + 20))
            pygame.draw.rect(self.display, self.color, self.input_box, 3)

            if self.missed_letters:
                self.display_text(f'Missed letters: {", ".join(self.missed_letters)}', 0, 250, self.red)

            if self.is_word_revealed():
                self.display_text('You won', 0, 200, self.grean)
                self.game_over = True
                self.save_score_history(True)
                return "reset"

            if self.lifes <= 0:
                self.display_text('You lose', 0, 150, self.grean)
                self.display_text(f'The word was: {self.random_word}', 0, 200, self.grean)
                self.game_over =True
                self.save_score_history(False)
                return "reset"
            
            self.display_text(f"Score: {self.load_score()}", 540, -275, self.red)

            pygame.display.flip()
            self.clock.tick(30)

class WordFactory:
    @staticmethod
    def get_word():
        words = HangmanGame.open_word_list("english")
        return random.choice(words)

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.init()
            mixer.init()
            mixer.music.load("Spooky.mp3")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
        return cls._instance

    def __init__(self):
        self.game = HangmanGame()

    def run(self):
         while True:
            result = self.game.run()
            if result == "reset":
                pygame.display.flip()
                time.sleep(1)
                #pygame.time.delay( 1000)
                self.restart_game()

    def restart_game(self):
        
        # Restart the game
        self.clear_screen()
        self.game = HangmanGame()
        self.run()
    def clear_screen(self):
        # Fill the screen with white color
        self.game.display.fill((255, 255, 255))
        pygame.display.flip() 

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
