import pygame
import random
import sys
import time
from pygame import mixer

class HangmanGame:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.words = self.open_word_list()
        self.random_word = random.choice(self.words)
        self.separated_word = self.separate_word(self.random_word)
        self.hidden_word = self.hide_word(self.separated_word)
        self.missed_letters = []
        self.lifes = 6
        print(self.random_word)
        self.game_over = False

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

    def open_word_list(self):
        with open('words_list.txt', 'r') as file:
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
        text_rect = text.get_rect(center=(800 // 1.3, 600 // 1.9))
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

            self.display_hidden_word()
            self.display_hearts(self.lifes)
            txt_surface = self.font.render(self.input_txt, True, self.color)
            self.input_box.w = max(100, txt_surface.get_width() + 10)
            self.input_box.h = max(80, 10)
            self.display.blit(txt_surface, (self.input_box.x + 38, self.input_box.y + 20))
            pygame.draw.rect(self.display, self.color, self.input_box, 3)

            if self.missed_letters:
                text = self.font.render(f'Missed letters: {", ".join(self.missed_letters)}', True, self.red)
                self.display.blit(text, (800 // 2 - text.get_width() // 2, 600 // 2 + 250))

            if self.is_word_revealed():
                text1 = self.font2.render('You won', True, self.grean)
                self.display.blit(text1, (800 // 2 - text1.get_width() // 2, 600 // 2 + 200))
                self.game_over = True
                return "reset"

            if self.lifes <= 0:
                text2 = self.font2.render('You lose', True, self.grean)
                self.display.blit(text2, (800 // 2 - text2.get_width() // 2, 600 // 2 + 150))
                text2 = self.font2.render(f'The word was: {self.random_word}', True, self.grean             )
                self.display.blit(text2, (800 // 2 - text2.get_width() // 2, 600 // 2 + 200))
                self.game_over =True
                return "reset"
            pygame.display.flip()
            self.clock.tick(30)

class WordFactory:
    @staticmethod
    def get_word():
        words = HangmanGame.open_word_list()
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
                time.sleep(5)
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
