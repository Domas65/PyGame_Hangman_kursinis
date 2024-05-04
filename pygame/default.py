import pygame, random, sys
from pygame import mixer 

pygame.init()
mixer.init()
class Word():
    pass
def quitGame():
    pygame.quit()
    sys.exit()
def seperate_word(word):
    letters = [letter for letter in word]
    return letters
def hide_word(letters):
    hidden_word = ['_' for _ in letters]
    return hidden_word
def open_list():
    file =open('words_list.txt', 'r')
    words = file.readlines()
    words = [word.strip() for word in words]
    file.close()
    return words
def reveal_letter(word, hidden_word, letter, missed_letters):
    if letter in missed_letters:
        return True
    revealed = False
    for i, char in enumerate(word):
        if char == letter:
            hidden_word[i] = letter
            revealed = True
    if not revealed:
        missed_letters.append(letter)
    return revealed
def is_word_revealed(hidden_word):
    return '_' not in hidden_word
            

# Read the contents of the file

#print("GG-------------GG")
#print(words)
#print("GG-------------GG")
mixer.music.load("Spooky.mp3")
mixer.music.set_volume(0.7) 
mixer.music.play(-1) 

words = open_list()
random_word = random.choice(words)
print("Random word:", random_word)
separeted = seperate_word(random_word)
hidden_word = hide_word(separeted)

#values
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
fps = 30
X = 800
Y = 600
missed_letters = []
lifes = 6



#create display
display = pygame.display.set_mode((X, Y))
pygame.display.set_caption("HangMan")
pygame.display.update()

#text values
font = pygame.font.SysFont('freesansbold.ttf', 42)
font2 = pygame.font.SysFont('freesansbold.ttf', 64)
input_box = pygame.Rect(150, 400, 150, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
input_txt =''
active = False
clock = pygame.time.Clock()
bg = pygame.image.load("Background.png")


def display_hidden_word(hidden_word):
    # Display the hidden word on the screen
    font = pygame.font.SysFont('freesansbold.ttf', 42)
    text = font.render(' '.join(hidden_word), True, black)
    text_rect = text.get_rect(center=(X // 2, Y // 1.5))
    display.blit(text, text_rect)

    #pygame.display.flip()
#Update screen
open = True
while open:
    display.fill(white)
    display.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open = False

        if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                active = not active
            else:
                active = False
                # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if input_txt:
                        if not reveal_letter(random_word, hidden_word, input_txt, missed_letters):
                            lifes-=1

                    print(input_txt)
                    input_txt = ''
                    
                elif event.key == pygame.K_BACKSPACE:
                    input_txt = input_txt[:-1]
                else:
                    input_txt += event.unicode
                if len(input_txt)>1:
                    input_txt = input_txt[:-1]
        
        #pygame.display.update()
    
    #display.blit(text, textRect)
    display_hidden_word(hidden_word)
    txt_surface = font.render(input_txt, True, color)
        # Resize the box if the text is too long.
    width = max(20, txt_surface.get_width()+10)
    input_box.w = width
        # Blit the text.
    display.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.    
    pygame.draw.rect(display, color, input_box, 3)
    if missed_letters:
        text = font.render(f'You missed: {", ".join(missed_letters)}', True, (255, 0, 0))
        display.blit(text, (X // 2 - text.get_width() // 2, Y // 2 + 50))
        
    if is_word_revealed(hidden_word):
        text1 = font2.render(f'You won', True, blue)
        display.blit(text1, (X // 2 - text1.get_width() // 2, Y // 2 + 200))
    
    if lifes <=0:
        text2 = font2.render(f'You lose', True, green)
        display.blit(text2, (X // 2 - text2.get_width() // 2, Y // 2 + 150))
        text2 = font2.render(f'The word was: {random_word}', True, green)
        display.blit(text2, (X // 2 - text2.get_width() // 2, Y // 2 + 200))
    #pygame.mixer.music.play(-1)
    
    pygame.display.flip()
    clock.tick(fps)

quitGame()