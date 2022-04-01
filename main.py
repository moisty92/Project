from ast import Delete
import pygame
import random
import sys

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

#loads grey boxes for main menu
play_img = pygame.image.load("img/Icons/Play Rect.png")
img = pygame.image.load("img/Icons/Options Rect.png")
options_img = pygame.transform.scale(img, (img.get_width() * .8, img.get_height()))
LB_img = pygame.image.load("img/Icons/Leaderboard Rect.png")
quit_img = pygame.image.load("img/Icons/Quit Rect.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("Times new Roman", size)

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

    #define fonts
    font = pygame.font.SysFont("Times new Roman", 26)
    #define colours
    red = (255,0,0)
    green = (0,255,0)

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
        for count, i in enumerate(bandit_list):
            draw_text(f"{i.name} HP: {i.hp}", font, red, 700, (screen_H - bottom_panel + 15) + count * 70)
        

    class Character():
        def __init__(self,x , y, name, max_hp,strength,armour,potions):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.armour = armour
            self.start_potions = potions
            self.potions = potions
            self.alive = True
            self.animation_list = []
            self.action = 0  #0:idle, 1:attack, 2:hurt, 3:death
            self.frame_index = 0
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
            armour = self.armour
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
              damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
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

    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            #update with new health
            self.hp = hp
            #calculate health
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 300, 35))
            pygame.draw.rect(screen, green, (self.x, self.y, 300 * ratio, 35))
        
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

    knight = Character(250, 390,"Knight", 50, 10, 12, 5)
    bandit1 = Character(900, 400, "Bandit",20, 0, 0, 0)
    bandit2 = Character(1100, 400, "Bandit",20, 0, 0, 0)
    wizard = Character(1100, 400, "Wizard",40, 15,12, 0)

    bandit_list = []
    bandit_list.append(bandit1)
    bandit_list.append(bandit2)

    knight_HB = HealthBar(150, screen_H - bottom_panel + 50, knight.hp, knight.max_hp)
    bandit1_HB = HealthBar(750, screen_H - bottom_panel + 50, bandit1.hp, bandit1.max_hp)
    bandit2_HB = HealthBar(750, screen_H - bottom_panel + 120, bandit2.hp, bandit2.max_hp)
    wizard_HB = HealthBar(750, screen_H - bottom_panel + 120, wizard.hp, wizard.max_hp)

    #create buttons
    potions_button = GameButton(screen, 500, screen_H - bottom_panel + 70, potion_img, 64, 64)
    restart_button = GameButton(screen, 550, 160, restart_img, 180, 40)
    quit_button = GameButton(screen, 0,0, quitgame_img, 64, 64)

    run = True
    while run:

        clock.tick(fps)
        draw_bg()
        draw_panel()
        def draw_panel_level():
          knight_HB.draw(knight.hp)# draws the knights health bar
          panel_level = random.randint(1,14)
          if panel_level == 1 or 2 or 3 or 4 or 5:# will set the panel to 2 bandits
            bandit1_HB.draw(bandit1.hp)# draws the bandits health bar
            bandit2_HB.draw(bandit2.hp)
          if panel_level == 6 or 7 or 8:# will set the panel to a bandit
            bandit1_HB.draw(bandit1.hp)
          if panel_level == 9 or 10:# will set the panel to a wizard
            wizard_HB.draw(wizard.hp)# draws the wizard health bar
          if panel_level == 11:# will set the panel to a bandit and a wizard
            wizard_HB.draw(wizard.hp)
            bandit1_HB.draw(bandit1.hp)
          if panel_level == 12 or 13 or 14:# will give the knight 2 potions
            pass
          if bandit1.alive or bandit2.alive or wizard.alive == False:# will remove the health bar when they are dead
            pass
        draw_panel_level()
            
        def characterDraw(potions):
          knight.update()
          knight.draw()
          level = random.randint(1,14)
          if level == 1 or 2 or 3 or 4 or 5:# will draw 2 bandits
            for bandit in bandit_list:
              bandit.update()
              bandit.draw()
          elif level == 6 or 7 or 8:# will draw one bandit
            bandit1.update()
            bandit1.draw()
          elif level == 9 or 10:# will draw a wizard
            wizard.update()
            wizard.draw()
          elif level == 11:# will draw wizard and bandit
            wizard.update()
            wizard.draw()
            bandit1.update()
            bandit1.draw()
          elif level == 12 or 13 or 14:# will give the knight 2 potions
            potions += 2
            draw_text(("+2 Potions"), font, green, 900, 400)
        characterDraw(potion)
          
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
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword in place of mouse
                screen.blit(sword_img, pos)
                if clicked == True and bandit.alive == True:
                    attack = True
                    target = bandit_list[count]
                elif clicked == True and wizard.alive == True:
                    attack = True
                    target = wizard

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
            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                    else:
                        current_fighter += 1 
                    if wizard.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                            wizard.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                    else:
                        current_fighter += 1 

            #reset after turn
            if current_fighter > total_fighters:
                current_fighter = 1

        #check if enemies are dead
        alive_bandits = 0
        alive_wizard = 0
        for bandit in bandit_list:
            if bandit.alive == True:
                alive_bandits += 1
            if alive_bandits == 0:
                pass
        if wizard.alive == True:
            alive_wizard +=1
        if alive_wizard == 0:
            pass
        #gives XP bases on enemie death
        if alive_wizard == 1:
            totalXP += 15
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
    sys.exit()


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
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
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
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
      
def LB():
    while True:
        screen.fill(black)
        LB_mouse_pos = pygame.mouse.get_pos()

        LB_text = get_font(80).render("LEADERBOARD", True, white)
        LB_rect = LB_text.get_rect(center=(640, 50))
        screen.blit(LB_text,LB_rect)

        LB_back = MainMenuButton(image=None, pos=(1160, 660), text_input="BACK", font=get_font(50), base_color=white, hovering_color="Green")

        LB_back.changeColor(LB_mouse_pos)
        LB_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        options_back = MainMenuButton(image=None, pos=(1160, 660), text_input="BACK", font=get_font(50), base_color=white, hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        play_button = MainMenuButton(play_img, pos=(640, 150),text_input="PLAY", font=get_font(35), base_color=white, hovering_color="Green")
        options_button = MainMenuButton(options_img, pos=(640, 300), text_input="OPTIONS", font=get_font(35), base_color=white, hovering_color="Green")
        LB_button = MainMenuButton(LB_img, pos=(640, 450), text_input="LEADERBOARD", font=get_font(35), base_color=white, hovering_color="Green")
        quit_botton = MainMenuButton(quit_img, pos=(640, 600),  text_input="QUIT", font=get_font(35), base_color=white, hovering_color="Green")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button,LB_button, quit_botton]:
            button.changeColour(menu_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
