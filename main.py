import pygame
import random

pygame.init()

#creates the variables for the game# window
clock = pygame.time.Clock()
fps = 60
bottom_panel = 180
screen_W = 1280
screen_H = 550 + bottom_panel
screen = pygame.display.set_mode((screen_W, screen_H))
pygame.display.set_caption("Planet Gorgon")
white = (255,255,255)
black = (0,0,0)
green = (0,0,255)
font = pygame.font.SysFont("Times new Roman", 26)
red = (255,0,0)
green = (0,255,0)

#loads grey boxes for main menu
play_img = pygame.image.load("img/Icons/Play Rect.png")
img = pygame.image.load("img/Icons/Options Rect.png")
options_img = pygame.transform.scale(img, (img.get_width() * .8, img.get_height()))
LB_img = pygame.image.load("img/Icons/Leaderboard Rect.png")
quit_img = pygame.image.load("img/Icons/Quit Rect.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("Times new Roman", size)

class Character():
    def __init__(self,x , y, name, max_hp,strength,armour,potions,xHB,yHB, hp,):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.armour = armour
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.action = 0  #0:idle, 1:attack, 2:hurt, 3:death
        self.frame_index = 0
        self.xHB = xHB
        self.yHB = yHB
        self.update_time = pygame.time.get_ticks()
        
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4 ))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4 ))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"img/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4 ))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f"img/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4 ))
            temp_list.append(img)
        self.animation_list.append(temp_list) 

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
        #update with new health
        #calculate health
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.xHB, self.yHB, 300, 35))
        pygame.draw.rect(screen, green, (self.xHB, self.yHB, 300 * ratio, 35))
    
    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed 
        #   current time        - last updated   if greater than 100ms time to update to the next image    
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #add in loop at end of images
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hit(self): # creates a random attack value
        return random.randint(1, 20)

    def attack(self,target):
        #deal damage
        strength = self.strength
        hit = self.hit()
        armour = target.armour
        #checks if initial attack is greater than armour class
        if hit > armour:
            damage = random.randint(1,strength)
            target.hp -= damage
            #run hurt animation
            target.hurt()
        #check death
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        #attack text
        damage_text= DamageText(target.rect.centerx, target.rect.y, str(hit), white)
        damage_text_group.add(damage_text)
        if hit > armour:
            #damage text
            damage_text = DamageText(target.rect.centerx, target.rect.y-50, str(damage), red)
            damage_text_group.add(damage_text)
        else:#Blocked text
            damage_text = DamageText(target.rect.centerx, target.rect.y-100, str("Blocked"),white)
            damage_text_group.add(damage_text)
        #attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()    
        
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    
    def update(self):
        #float away
        self.rect.y -= 1
        #deletes text
        self.counter += 1
        if self.counter > 60:
            self.kill()
damage_text_group = pygame.sprite.Group()

#Game button class
class GameButton():
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Main menu button class
class MainMenuButton():
	def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_colour, self.hovering_colour = base_colour, hovering_colour
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_colour)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
  #draw button
	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)
    
  #checks for click for on button position
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
    
  #changes colour on button highlight
	def changeColour(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_colour)
		else:
			self.text = self.font.render(self.text_input, True, self.base_colour)

def play():
    #define game variables
    current_fighter = 1
    total_fighters = 3
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    potion_effect = 20 
    clicked = False
    game_over = 0
    totalXP = 0

    #load images
    img = pygame.image.load("img/Background/background.png").convert_alpha()
    bg_img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() * 1.45 ))
    img = pygame.image.load("img/Icons/panel.png").convert_alpha()
    panel_img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() * 1.2 ))
    potion_img = pygame.image.load("img/Icons/potion.png").convert_alpha()
    sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()
    img = pygame.image.load("img/Icons/defeat.png").convert_alpha()
    defeat_img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() * 1.6 ))
    restart_img = pygame.image.load("img/Icons/restart.png").convert_alpha()
    quitgame_img = pygame.image.load("img/Icons/quit.png").convert_alpha()

    #drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #draw background
    def draw_bg():
        screen.blit(bg_img, (0,0))

    #draw panel
    def draw_panel():
        #draw panel rectangle
        screen.blit(panel_img, (0,screen_H - bottom_panel))
        #show Character stats
        draw_text(f"{knight.name} HP: {knight.hp}", font, green, 100, screen_H - bottom_panel + 10)
        for count, i in enumerate(current_enemies_list):
            draw_text(f"{i.name} HP: {i.hp}", font, red, 700, (screen_H - bottom_panel + 15) + count * 70)
    
    knight = Character(250, 390,"Knight", 50, 10, 12, 5, 150, screen_H - bottom_panel + 50, 50)
    current_enemies_list = []

    def spawn_level1():
        bandit1 = Character(900, 400, "Bandit",20, 1, 0, 0, 750, screen_H - bottom_panel + 50, 20)
        bandit2 = Character(1100, 400, "Bandit",20, 1, 0, 0, 750, screen_H - bottom_panel + 120, 20)
        current_enemies_list.append(bandit1)
        current_enemies_list.append(bandit2)

    def spawn_level2():
        bandit1 = Character(900, 400, "Bandit",20, 1, 0, 0, 750, screen_H - bottom_panel + 50, 20)
        current_enemies_list.append(bandit1)

    def spawn_level3():
        bandit1 = Character(900, 400, "Bandit",20, 1, 0, 0, 750, screen_H - bottom_panel + 50, 20)
        boss = Character(1100, 300, "Boss",40, 15,12, 0, 750, screen_H - bottom_panel + 120, 20)
        current_enemies_list.append(bandit1)
        current_enemies_list.append(boss)

    def spawn_level4():
        boss = Character(1100, 300, "Boss",40, 15,12, 0, 750, screen_H - bottom_panel + 120, 20)
        current_enemies_list.append(boss)

    
    #create buttons
    potions_button = GameButton(screen, 500, screen_H - bottom_panel + 70, potion_img, 64, 64)
    restart_button = GameButton(screen, 550, 160, restart_img, 180, 40)
    quit_button = GameButton(screen, 0,0, quitgame_img, 64, 64)

    game_level = random.randint(1,17)

    run = True
    while run:

        clock.tick(fps)
        draw_bg()
        draw_panel()
        knight.draw()
        knight.update()
        if not current_enemies_list:
            if game_level in range(1,6):
                spawn_level1()
            elif game_level in range(7,9):
                spawn_level2()
            elif game_level in range(9,11):
                spawn_level3()             
            elif game_level in range(11,14):
                spawn_level4()
            elif game_level in range(14,17):
                knight.potions += 2
        for enemy in current_enemies_list:
            enemy.draw()
            enemy.update()
    
        #draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #control player actions
        #reset action variables
        attack = False
        potion = False
        target = None
        #makes mouse visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, enemy in enumerate(current_enemies_list):
            if enemy.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword in place of mouse
                screen.blit(sword_img, pos)
                if clicked == True and enemy.alive == True:
                    attack = True
                    target = current_enemies_list[count]
                

        #button potions
        if potions_button.draw():
            potion = True
        #show number of potions 
        draw_text(str(knight.potions), font, white, 545, screen_H - bottom_panel + 70) 

        if quit_button.draw():
            main_menu()

        if game_over == 0:
            #player action
            if knight.alive:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack == True and target != None:
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0 
                        #potion
                    if potion == True:
                        if knight.potions > 0:
                            #check if potion heal beyond max hp
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)                        
                    
            else:
                game_over = -1

            #enemy action
            for count, enemy in enumerate(current_enemies_list):
                if current_fighter == 2 + count:
                    if enemy.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                            enemy.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                    else:
                        current_fighter += 1 
                    
            #reset after turn
            if current_fighter > total_fighters:
                current_fighter = 1

            n = len(current_enemies_list) - 1
            while n >= 0:
                if not current_enemies_list[n].alive:
                    current_enemies_list.pop(n)
                n -= 1

        #check if enemies are dead
        alive_bandits = 0
        
        for enemy in current_enemies_list:
            if enemy.alive == True:
                alive_bandits += 1
            if alive_bandits == 0:
                pass
        if alive_bandits == 1:
          totalXP += 5 
        elif  alive_bandits == 2:
          totalXP += 5
          
        #check if game is over
        if game_over != 0:
            screen.blit(defeat_img, (460, 40))
            if restart_button.draw():
                main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

    pygame.quit()
    
def LB():
    while True:
        screen.fill(black)
        LB_mouse_pos = pygame.mouse.get_pos()

        LB_text = get_font(80).render("LEADERBOARD", True, white)
        LB_rect = LB_text.get_rect(center=(640, 50))
        screen.blit(LB_text,LB_rect)

        LB_back = MainMenuButton(image=None, pos=(1160, 660), text_input="BACK", font=get_font(50), base_colour=white, hovering_colour="Green")

        LB_back.changeColour(LB_mouse_pos)
        LB_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LB_back.checkForInput(LB_mouse_pos):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        screen.fill(black)
        options_mouse_pos = pygame.mouse.get_pos()

        options_text = get_font(80).render("OPTIONS", True, white)
        options_rect = options_text.get_rect(center=(640, 50))
        screen.blit(options_text, options_rect,)

        options_back = MainMenuButton(image=None, pos=(1160, 660), text_input="BACK", font=get_font(50), base_colour=white, hovering_colour="Green")

        options_back.changeColour(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.fill(black)

        menu_pos = pygame.mouse.get_pos()

        menu_text = get_font(75).render("PLANET GORGON", True, white)
        menu_rect = menu_text.get_rect(center=(640, 50))

        play_button = MainMenuButton(play_img, pos=(640, 150),text_input="PLAY", font=get_font(35), base_colour=white, hovering_colour="Green")
        options_button = MainMenuButton(options_img, pos=(640, 300), text_input="OPTIONS", font=get_font(35), base_colour=white, hovering_colour="Green")
        LB_button = MainMenuButton(LB_img, pos=(640, 450), text_input="LEADERBOARD", font=get_font(35), base_colour=white, hovering_colour="Green")
        quit_botton = MainMenuButton(quit_img, pos=(640, 600),  text_input="QUIT", font=get_font(35), base_colour=white, hovering_colour="Green")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button,LB_button, quit_botton]:
            button.changeColour(menu_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_pos):
                    play()
                if options_button.checkForInput(menu_pos):
                    options()
                if LB_button.checkForInput(menu_pos):
                    LB()
                if quit_botton.checkForInput(menu_pos):
                    pygame.quit()

        pygame.display.update()

main_menu()
