#Projekt prostej gry z użyciem PyGame
#Autor: P. Wielopolski
#Projekt zwierząt: Platformer Art (more enemies and animations) by Kenney Vleugels (www.kenney.nl)
#Projekt drogi: AdebGameSoft www.adebgamesoft.be
#Projekt samochodów: looneybits https://www.reddit.com/r/looneybits/
#Projekt coinsa i serduszka: autorzy z OpenGameArt.org
#Elementy GUI: Cam Tatz //twitter: @CamTatz
#Dźwięki: flashkit.com

import pygame
from pygame.locals import *
import os.path
import random
import time

#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
WHITE = (255,255,255)
running = True
flag = str(random.randint(0,5))
clock = pygame.time.Clock()
difficulty = 1

#-----------------------------------------------------------------------
# Funkcje pomocnicze
#-----------------------------------------------------------------------
def loadImage(name, useColorKey=False):
    """ Załaduj obraz i przekształć go w powierzchnię.

    Funkcja ładuje obraz z pliku i konwertuje jego piksele 
    na format pikseli ekranu. Jeśli flaga useColorKey jest 
    ustawiona na True, kolor znajdujący się w pikselu (0,0)
    obrazu będzie traktowany jako przezroczysty (przydatne w 
    przypadku ładowania obrazów statków kosmicznych)
    Autor: J.Szwabiński
    """
    fullname = os.path.join("data",name)
    image = pygame.image.load(fullname)  #plik -> płaszczyzna
    image = image.convert() #przekonwertuj na format pikseli ekranu
    if useColorKey is True:
        colorkey = image.get_at((0,0)) #odczytaj kolor w punkcie (0,0)
        image.set_colorkey(colorkey,RLEACCEL) # ustaw kolor jako przezroczysty
        #flaga RLEACCEL oznacza lepszą wydajność na ekranach bez akceleracji
        #wymaga from pygame.locals import *
    return image


def play_Sound(name,volume = 1):
    """ Zagraj dźwięk. """
    fullname = os.path.join('data',name)
    sound = pygame.mixer.Sound(fullname)
    sound.set_volume(volume)
    sound.play()
    return

#-----------------------------------------------------------------------
# Klasy programu
#-----------------------------------------------------------------------

class Animal(pygame.sprite.Sprite):
    """ Klasa definiująca postać gracza (zwierzę). """
    ANIMALS = {'0':'snailL.png','1':'fishPinkL.png','2':'beeL.png','3':'spiderL.png','4':'ladyBugL.png','5':'mouseL.png'}
    def __init__(self,flag):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage(Animal.ANIMALS[flag],True)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2,0.95*SCREEN_HEIGHT)
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        # Zmiana obrazka dla chodzenia w prawo bądź lewo
        if self.x_velocity > 0:
            temp = Animal.ANIMALS[flag][:-5]+'R.png'
            self.image = loadImage(temp,True)
            self.rect.move_ip((self.x_velocity,self.y_velocity))
        elif self.x_velocity < 0:
            temp = Animal.ANIMALS[flag][:-5]+'L.png'
            self.image = loadImage(temp,True)
            self.rect.move_ip((self.x_velocity,self.y_velocity))
        else:
            self.rect.move_ip((self.x_velocity,self.y_velocity)) #move in-place

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Car(pygame.sprite.Sprite):
    """ Klasa definiująca jeżdżące samochody. """
    COLOR = {'0':'red_carR.png','1':'blue_carR.png','2':'black_carR.png','3':'yellow_carR.png'}
    VELO = 0
    RACE_CARS = ['race_car1.wav','race_car2.wav','race_car3.wav']
    def __init__(self, position ,direction, color = 1):
        """ direction: 1 - right, -1 - left """
    
        pygame.sprite.Sprite.__init__(self)
        color = str(color)
        self.direction = direction
        if self.direction == 1: 
            self.image = loadImage(Car.COLOR[color],True)
            self.x_velocity = Car.VELO + 3*round(random.random(),2)+difficulty
        elif self.direction == -1:
            temp = Car.COLOR[color][0:-5]+'L.png'
            self.image = loadImage(temp,True)
            self.x_velocity = - (Car.VELO + 3*round(random.random(),2)+difficulty)
        self.rect = self.image.get_rect()
        self.rect.center = (position)
        self.y_velocity = 0

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            temp_sound = random.choice(Car.RACE_CARS)
            play_Sound(temp_sound,0.15)
            

    def accelerate(self):
        """ Funkcja przyspieszająca samochód. """
        if self.direction == 1 and self.x_velocity <= 8:
            self.x_velocity += 0.3
        elif self.direction == -1 and self.x_velocity >= -8:
            self.x_velocity -= 0.3

class Coin(pygame.sprite.Sprite):
    """ Klasa reprezentująca monetę. """
    counter = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage('coin.png',True)
        self.rect = self.image.get_rect()
        Coin.counter += 1
        self.rect.center = (random.randint(100,700),300+(-1)**(Coin.counter)*random.randint(250,280))

class ScoreBoard(pygame.sprite.Sprite):
    """ Tablica wyników. Autor: J.Szwabiński """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.text = "Score: %4d" % self.score
        self.font = pygame.font.SysFont('Algerian',40)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.score += 1*difficulty
        self.text = "Score: %4d" % self.score
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()

class Heart(pygame.sprite.Sprite):
    """ Serduszko życia. """
    def __init__(self,number):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage('heart.png',True)
        self.rect = self.image.get_rect()
        self.rect.center = (800 - number*25,15)

class Explosion(pygame.sprite.Sprite):
    """ Animowana eksplozja. """
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,13):
            temp_name = 'Explosion'+str(i)+'.png'
            self.images.append(loadImage(temp_name))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(pos[0],pos[1],50,50)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
            self.kill()
        self.image = self.images[self.index]

class Highscore(pygame.sprite.Sprite):
    def __init__(self,name,score,position):
        pygame.sprite.Sprite.__init__(self)
        self.score = score
        self.name = name[:-1]
        self.text = '%4d  %s' %(self.score, self.name)
        self.font = pygame.font.SysFont('Algerian',40)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = position      
    
#-----------------------------------------------------------------------
# Główne funkcje programu
#-----------------------------------------------------------------------

def play(screen,name,flag = '0'):
    """ Main function of game. """
    #Variables
    addnewcarCounter1 = random.randint(240,250)
    addnewcarCounter2 = random.randint(240,250)
    addnewcarCounter3 = random.randint(240,250)
    addnewcarCounter4 = random.randint(240,250)
    newcarcolor = 0
    lives = 3
    
    #Setting background
    background = loadImage('background.png')
    screen.blit(background,(0,0))
    pygame.display.flip()

    #Setting sounds
    pops = ['pop1.wav','pop2.wav']
    
    # Inicjalizacja zwierzaka.
    animalSprite = pygame.sprite.RenderClear()
    animal = Animal(flag)
    animalSprite.add(animal)
    # Inicjalizacja pojemnika na auta
    carSprite = pygame.sprite.RenderClear()
    # Inicjalizacja monetki.
    coinSprite = pygame.sprite.RenderClear()
    coinSprite.add(Coin())
    # Inicjalizuj licznik trafień.
    scoreboardSprite = pygame.sprite.RenderClear()
    TablicaWynikow = ScoreBoard()
    scoreboardSprite.add(TablicaWynikow)
    scoreboardSprite.draw(screen)
    # Inicjalizacja licznika żyć.
    LivesSprite = pygame.sprite.RenderClear()
    LivesSprite.add(Heart(1),Heart(2),Heart(3))
    LivesSprite.draw(screen)
    # Inicjalizacja pojeminika na eksplozje.
    explosionSprite = pygame.sprite.RenderClear()
    pygame.display.flip()
    
    
    #Main loop of game.
    running = True
    while running:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                Car.VELO = 0
                check_score(name,TablicaWynikow.score)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    Car.VELO = 0
                    check_score(name,TablicaWynikow.score)
                elif event.key == K_SPACE:
                    addmenu(screen)
                    screen.blit(background,(0,0))
                    pygame.display.flip()
                elif event.key == K_LEFT:
                    animal.x_velocity = -4
                elif event.key == K_RIGHT:
                    animal.x_velocity = 4
                elif event.key == K_UP:
                    animal.y_velocity = -4
                elif event.key == K_DOWN:
                    animal.y_velocity = 4
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    animal.x_velocity = 0 
                elif event.key == K_RIGHT:
                    animal.x_velocity = 0
                elif event.key == K_UP:
                    animal.y_velocity = 0
                elif event.key == K_DOWN:
                    animal.y_velocity = 0

        #Dodanie kolejnego auta
        addnewcarCounter1 += random.randint(0,2)
        if addnewcarCounter1 >= 250:
            carSprite.add(Car((-60,475),1,newcarcolor))
            addnewcarCounter1 = 0
            newcarcolor = (newcarcolor+1)%4
        addnewcarCounter2 += random.randint(0,3)

        if addnewcarCounter2 >= 250:
            carSprite.add(Car((-60,375),1,newcarcolor))
            addnewcarCounter2 = 0
            newcarcolor = (newcarcolor+1)%4

        addnewcarCounter3 += random.randint(1,4)
        if addnewcarCounter3 >= 250:
            carSprite.add(Car((860,110),-1,newcarcolor))
            addnewcarCounter3 = 0
            newcarcolor = (newcarcolor+1)%4

        addnewcarCounter4 += random.randint(1,3)
        if addnewcarCounter4 >= 250:
            carSprite.add(Car((860,210),-1,newcarcolor))
            addnewcarCounter4 = 0
            newcarcolor = (newcarcolor+1)%4
        
        #Akutalizacja sprite'ów
        animalSprite.update()
        carSprite.update()
        explosionSprite.update()

        #Sprawdzanie kolizji
        for hit in pygame.sprite.groupcollide(animalSprite,carSprite,0,0):
            play_Sound('dead.wav')
            time.sleep(2)
            tempLive = LivesSprite.sprites()
            LivesSprite.remove(tempLive[0])
            lives -= 1
            animal.rect.center = (SCREEN_WIDTH/2,0.95*SCREEN_HEIGHT)    #Resetuje położenie zwierzaka
            if lives <=0:
                print('Koniec gry')
                Car.VELO = 0
                check_score(name,TablicaWynikow.score)
                running = False
                return
        
        #Sprawdzanie kraks
        Duszki = carSprite.sprites()                            #lista aut w pojemniku
        for el in carSprite.sprites():
            Duszki.remove(el)
            if pygame.sprite.spritecollideany(el,Duszki):       #jezeli aktualne auto coliduje z pozostalymi autami
                play_Sound('crash.wav',0.6)
                explosionSprite.add(Explosion(el.rect))         #wywolanie eksplozji auta
                carSprite.remove(el)                            #usuniecie auta z glownego pojemnika

        #Sprawdzenie zdobycia monety
        for hit in pygame.sprite.groupcollide(animalSprite,coinSprite,0,1):
            scoreboardSprite.update()           #aktualizacja wyniku
            coinSprite.add(Coin())              #dodanie nowej monety
            el = carSprite.sprites()            #lista aut w pojemniku
            for i in range(len(el)):
                el[i].accelerate()              #przyspieszenie wszystkich aktualnych aut
            if Car.VELO <= 4:
                Car.VELO += 0.2                 #przyspieszenie nowych aut
            temp_pop = random.choice(pops)      #losowanie dzwieku
            play_Sound(temp_pop,1)
            
        
        #Czyszczenie ekranu
        animalSprite.clear(screen, background)
        carSprite.clear(screen, background)
        coinSprite.clear(screen, background)
        scoreboardSprite.clear(screen, background)
        LivesSprite.clear(screen, background)
        explosionSprite.clear(screen, background)

        #Rysowanie sprite'ów
        animalSprite.draw(screen)
        carSprite.draw(screen)
        coinSprite.draw(screen)
        scoreboardSprite.draw(screen)
        LivesSprite.draw(screen)
        explosionSprite.draw(screen)
        pygame.display.flip()
                
    return

#-----------------------------------------------------------------------------
# Funkcje do menu
#-----------------------------------------------------------------------------

def addmenu(screen,flag = 0):
    """ Pause/help during game. """
    if flag == 0:
        image = loadImage('pause_menu.png')
    elif flag == 1:
        image = loadImage('help.png')
    screen.blit(image,(0,0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    running = False
    return

def set_menu(screen):
    """ Setting main menu. """
    background_image = loadImage('backgroundmenu.png')
    screen.blit(background_image,(0,0))
    pygame.display.flip()

def check_difficulty():
    if difficulty == 1:
        image = loadImage('upin.png')
    elif difficulty == 2:
        image = loadImage('midin.png')
    elif difficulty == 3:
        image = loadImage('downin.png')
    screen.blit(image,(0,0))
    pygame.display.flip()
    return

def level(screen):
    check_difficulty()
    running = True
    global difficulty
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    running = False
                elif event.key == K_1:
                    difficulty = 1
                    check_difficulty()
                elif event.key == K_2:
                    difficulty = 2
                    check_difficulty()
                elif event.key == K_3:
                    difficulty = 3
                    check_difficulty()

def get_scores():
    """ Getting scores. """
    tableofscores = []
    try:
        scores = open(os.path.join('data','highscores.txt'),'r+')
        for line in scores:
            datascore,dataname = line.split(' ')
            datascore = int(datascore)
            tableofscores.append([datascore,dataname])
        scores.close()
        tableofscores.sort()
        tableofscores.reverse()
        tableofscores = tableofscores[:3]
    except:
        print('Failed to get highscores')
    return tableofscores

def check_score(name,score):
    """ Sprawdzanie wyników. """
    tableofscores = get_scores()
    tableofscores.append([score,name+'\n'])
    tableofscores.sort()
    tableofscores.reverse()
    tableofscores = tableofscores[:3]
    newscores = open(os.path.join('data','highscores.txt'),'w+')
    for el in tableofscores:
        newscores.write(str(el[0])+' ' + str(el[1]))
    newscores.close()

def highscores(screen):
    image = loadImage('scores.png')
    screen.blit(image,(0,0))
    pygame.display.flip()
    highscoresSprite = pygame.sprite.RenderClear()
    tableofscores = get_scores()
    height = 220
    for el in tableofscores:
        highscoresSprite.add(Highscore(el[1],el[0],(200,height)))
        height += 100
    highscoresSprite.draw(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    running = False 

#-----------------------------------------------------------------------
# Program
#-----------------------------------------------------------------------
name = input('Please, write your name: ')
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Why do animals cross the road?')
set_menu(screen)

#Pętla menu
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_5:
                running = False
                pygame.quit()
            elif event.key == K_1:
                play(screen,name,flag)
                set_menu(screen)
            elif event.key == K_2:
                highscores(screen)
                set_menu(screen)
            elif event.key == K_3:
                addmenu(screen,1)
                set_menu(screen)
            elif event.key == K_4:
                level(screen)
                set_menu(screen)
                
