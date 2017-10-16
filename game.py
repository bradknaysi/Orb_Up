# Bradley Knaysi (bak9cu) and Lillie Lyon (lal5kr)

import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)
character = gamebox.from_color(100, 100, "blue", 10, 10)
character2 = gamebox.from_color(100, 100, "cyan", 10, 10)
lives = 3
lives2 = 3
lives2_left = gamebox.from_text(680, 50, "p2 Lives: " + str(lives2), "Arial", 20, "Black")
lives_left = gamebox.from_text(680, 30, "p1 Lives: " + str(lives), "Arial", 20, "Black")
goal_size = gamebox.from_text(700, 70, "Goal Size: = 100", "Arial", 20, "Black")
respawn_zone = gamebox.from_color(20, 20, "grey", 40, 40)
game_over = False
game_on = False

orb_sound = gamebox.load_sound("wall.wav")
game_music = gamebox.load_sound("Pim Poy.wav")
game_music.play(-1)

orbs = []
for number in range(0, 30):
    size = random.randint(15, 50)
    small_size = random.randint(5, 10)
    colors = ["green", "red", "orange", "purple"]
    orbs.append(gamebox.from_color(random.randint(150, 700), random.randint(150, 500), colors[random.randint(0, 3)], size, size))
    orbs.append(gamebox.from_color(random.randint(150, 700), random.randint(150, 500), colors[random.randint(0, 3)], small_size, small_size))

for orb in orbs:
    orb.xspeed = random.randint(2, 4)
    orb.yspeed = random.randint(2, 4)

top_walls = [
    gamebox.from_color(400, 600, "yellow", 1000, 20),
    gamebox.from_color(400, 0, "yellow", 1000, 20),
]
side_walls = [
    gamebox.from_color(0, 300, "yellow", 20, 1000),
    gamebox.from_color(800, 300, "yellow", 20, 1000),
]

start_screen = gamebox.from_text(400, 150, "Orb Up", "Arial", 60, "blue")
computing_ID = gamebox.from_text(400, 200, "Bradley Knaysi (bak9cu) and Lillie Lyon (lal5kr)", "Arial", 20, "blue")
text = '''
P1 Controls: ASWD keys, P2: Controls: Arrow Keys
Eat orbs smaller than you to get larger... without touching orbs larger than you. Each player gets 3 lives.
The last player to survive or reach the size goal of 100 wins!!

Press SPACE to Start!

'''
instructions = gamebox.from_text(400, 350, "P1 Controls: ASWD keys, P2: Controls: Arrow Keys", "Arial", 20, "black")
instructions2 = gamebox.from_text(400, 380, "Eat orbs smaller than you to get larger...", "Arial", 20, "black")
instructions3 = gamebox.from_text(400, 410, "without touching orbs larger than you. Each player gets 3 lives.", "Arial", 20, "black")
instructions4 = gamebox.from_text(400, 440, "The last player to survive or reach the size goal of 100 wins!!", "Arial", 20, "black")

def start_game():
    camera.clear("white")
    camera.draw(start_screen)
    camera.draw(computing_ID)
    camera.draw(instructions)
    camera.draw(instructions2)
    camera.draw(instructions3)
    camera.draw(instructions4)
    camera.display()

start_game()



def tick(keys):
    global game_on, orbs, character, character2, lives, lives2, lives2_left, game_over, type, lives_left

    if game_on == False:
        inter_lives = gamebox.from_text(400, 200, "Press Space to Respawn!", "Arial", 50, "Black")
        camera.draw(inter_lives)
    if pygame.K_SPACE in keys:
        game_on = True
    if game_on:
        if pygame.K_UP in keys and character.y > 20:
            character.y -= 5
        if pygame.K_DOWN in keys and character.y < 580:
            character.y += 5
        if pygame.K_RIGHT in keys and character.x < 780:
            character.x += 5
        if pygame.K_LEFT in keys and character.x > 20:
            character.x -= 5
        if pygame.K_w in keys and character2.y > 20:
            character2.y -= 5
        if pygame.K_s in keys and character2.y < 580:
            character2.y += 5
        if pygame.K_d in keys and character2.x < 780:
            character2.x += 5
        if pygame.K_a in keys and character2.x > 20:
            character2.x -= 5

        for orb in orbs:
            orb.x += orb.xspeed
            orb.y += orb.yspeed

        for wall in top_walls:
            for orb in orbs:
                if orb.touches(wall):
                    orb.yspeed *= -1
        for wall in side_walls:
            for orb in orbs:
                if orb.touches(wall):
                    orb.xspeed *= -1
        for orb in orbs:
            if orb.touches(respawn_zone):
                orb.yspeed *= -1
                orb.xspeed *= -1
            if character.touches(orb) and character.width > orb.width:
                character.width += orb.width / 8
                character.height += orb.width / 8
                orb.xspeed, orb.yspeed = random.randint(2, 5), random.randint(2, 5)
                orb.x, orb.y = random.randint(150, 700), random.randint(150, 500)
                orb_sound.play()
            if character.touches(orb) and character.width < orb.width:
                lives -= 1
                lives_left = gamebox.from_text(680, 30, "p1 Lives: " + str(lives), "Arial", 20, "Black")
                character.width, character.height, character.x, character.y = 10, 10, 30, 30
                game_on = False
                orb_sound.play()
            if character2.touches(orb) and character2.width > orb.width:
                character2.width += orb.width / 8
                character2.height += orb.width / 8
                orb.xspeed, orb.yspeed = random.randint(2, 5), random.randint(2, 5)
                orb.x, orb.y = random.randint(150, 700), random.randint(150, 500)
                orb_sound.play()
            if character2.touches(orb) and character2.width < orb.width:
                lives2 -= 1
                lives2_left = gamebox.from_text(680, 50, "p2 Lives: " + str(lives2), "Arial", 20, "Black")
                character2.width, character2.height, character2.x, character2.y = 10, 10, 20, 20
                orb_sound.play()
                game_on = False
            if lives <= 0:
                game_on = False
                game_over = True
                type = 0
            if lives2 <= 0:
                game_on = False
                game_over = True
                type = 1
            if character.width >= 100:
                game_on = False
                game_over = True
                type = 2
            if character2.width >= 100:
                game_on = False
                game_over = True
                type = 3

        camera.clear("white")
        camera.draw(respawn_zone)
        camera.draw(character)
        camera.draw(character2)
        camera.draw(lives2_left)
        camera.draw(lives_left)
        camera.draw(goal_size)
        for wall in top_walls:
            camera.draw(wall)
        for wall in side_walls:
            camera.draw(wall)
        for orb in orbs:
            camera.draw(orb)
        if game_over:
            end_game(type)
        camera.display()


def end_game(type):
    if type == 0:
        camera.clear("black")
        end_screen = gamebox.from_text(400, 200, "Player 2 survived longer!!... game over!!", "Arial", 40, "red")
        camera.draw(end_screen)
    if type == 1:
        camera.clear("black")
        end_screen = gamebox.from_text(400, 200, "Player 1 survived longer!!... game over!!", "Arial", 40, "red")
        camera.draw(end_screen)
    if type == 2:
        camera.clear("black")
        end_screen = gamebox.from_text(400, 200, "You are the largest orb on screen... Player 1 wins!!", "Arial", 30, "green")
        camera.draw(end_screen)
    if type == 3:
        camera.clear("black")
        end_screen = gamebox.from_text(400, 200, "You are the largest orb on screen... Player 2 wins!!", "Arial", 30, "green")
        camera.draw(end_screen)

ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)