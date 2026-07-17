import pygame,sys,math
import pymunk.pygame_util

from core.physics import Physics
from core.objs import Player,Ball,Ground


def main():

    Bg_sprite_path = "assets/sprites/DefineSprite_280/1.png"
    

    W,H = 802, 543
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W,H))

    score_font = pygame.font.Font("assets/fonts/199_InfoTextSemiboldTf Caps.ttf",70)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    

    Pl1 = Player(coordinates = (300, 260),
                 mass = 50,
                 size = 20,
                 speed = (250,500),
                 power = 200,
                 friction = 0,
                 elasticity = 0,
                 orientation = -1,
                 sprite_path = "assets/sprites/DefineSprite_262_SportsHeadsSoccerDist_fla.Heads_46/1.png",
                 sprite_leg_path = "assets/sprites/DefineSprite_268_SportsHeadsSoccerDist_fla.OPPRACKET2_48/1.png",
                 sprite_goal_path = "assets/sprites/DefineSprite_128_SportsHeadsSoccerDist_fla.GoalMC_43/1.png",
                )

    Pl2 = Player(coordinates = (500, 250),
                 mass = 50,
                 size = 20,
                 speed = (125,250),
                 power = 20,
                 friction = 0,
                 elasticity = 0,
                 orientation = 1,
                 sprite_path = "assets/sprites/DefineSprite_262_SportsHeadsSoccerDist_fla.Heads_46/1.png",
                 sprite_leg_path = "assets/sprites/DefineSprite_268_SportsHeadsSoccerDist_fla.OPPRACKET2_48/1.png",
                 sprite_goal_path = "assets/sprites/DefineSprite_128_SportsHeadsSoccerDist_fla.GoalMC_43/1.png",
                )

    Bal = Ball(coordinates = (W//2, H//2),
                 mass = 0.1,
                 size = 10,
                 friction = 0.9,
                 elasticity = 1.5,
                 sprite_path = "assets/sprites/DefineSprite_295/1.png",
                )

    Gro = Ground(first_position = (0, 543),
                 second_position = (802, 543),
                 size = 60,
                 friction = 0.9,
                 elasticity = 0.5,
                 sprite_path = "",
                )

    Phy = Physics((0, 900),0.99)
    # Phy = Physics((0, 700),0.95)
    
    Gro_obj = Phy.ground(Gro)
    Pl1_obj = Phy.player_and_ball(Pl1)
    Pl2_obj = Phy.player_and_ball(Pl2)
    Bal_obj = Phy.player_and_ball(Bal)
    
    Pl1_leg_obj = Phy.leg(Pl1_obj,Pl1.size)
    Pl2_leg_obj = Phy.leg(Pl2_obj,Pl2.size)

    walls_pos = [((0, 0), (0, 503)),((802, 0), (802, 503)),((5, 0), (797, 0))]
    walls = [Phy.ground(Ground(i,j,5,0.9,0.5,"")) for i,j in walls_pos]

    #Sprites
    Bg_sprite = pygame.image.load(Bg_sprite_path).convert_alpha()
    Pl1_sprite = pygame.image.load(Pl1.sprite_p).convert_alpha()
    Pl2_sprite = pygame.transform.flip(Pl1_sprite, True, False)
    Bal_sprite = pygame.image.load(Bal.sprite_p).convert_alpha()

    Pl1_leg_sprite = pygame.image.load(Pl1.sprite_l_p).convert_alpha()
    Pl2_leg_sprite = pygame.transform.flip(Pl1_leg_sprite, True, False)

    Pl1_goal_sprite = pygame.image.load(Pl1.sprite_g_p).convert_alpha()
    Pl2_goal_sprite = pygame.transform.flip(Pl1_goal_sprite, True, False)

    right_cor = (Pl1_goal_sprite.get_width(),H-Gro.size-Pl1_goal_sprite.get_height()+5)
    left_cor = (W-Pl2_goal_sprite.get_width(),H-Gro.size-Pl2_goal_sprite.get_height()+5)
    Pl1_goal_sprite_rect = Pl1_goal_sprite.get_rect(topright=right_cor)
    Pl2_goal_sprite_rect = Pl2_goal_sprite.get_rect(topleft=left_cor)

    Beam1 = Ground(first_position = (0, H-Gro.size-Pl1_goal_sprite.get_height()+5),
                 second_position = (Pl1_goal_sprite.get_width(), H-Gro.size-Pl1_goal_sprite.get_height()+5),
                 size = 2,
                 friction = 0.9,
                 elasticity = 0.5,
                 sprite_path = "",
                )
    Beam1_obj = Phy.ground(Beam1)

    Beam2 = Ground(first_position = (W-Pl2_goal_sprite.get_width(), H-Gro.size-Pl1_goal_sprite.get_height()+5),
                 second_position = (W, H-Gro.size-Pl1_goal_sprite.get_height()+5),
                 size = 2,
                 friction = 0.9,
                 elasticity = 0.5,
                 sprite_path = "",
                )
    Beam2_obj = Phy.ground(Beam2)

    Phy.space.on_collision(2,1,Phy.player1_and_ground_collide)
    Phy.space.on_collision(3,1,Phy.player2_and_ground_collide)

    Phy.space.on_collision(5,4,Phy.player1_leg_and_ball_collide)
    Phy.space.on_collision(6,4,Phy.player2_leg_and_ball_collide)

    running = True
    while running:
        
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                running = False
           
        keys = pygame.key.get_pressed()

        # 1st player keys 
        left = int(keys[pygame.K_a])
        up = int(keys[pygame.K_w])
        right = int(keys[pygame.K_d])
        kick = int(keys[pygame.K_SPACE])

        Phy.p1_on_gro = Pl1.motion(Pl1_obj,Phy.p1_on_gro,up,left,right)
        Pl1.motion_leg(Pl1_obj,kick,math.pi)

        # 2nd player keys
        left = int(keys[pygame.K_LEFT])
        up = int(keys[pygame.K_UP])
        right = int(keys[pygame.K_RIGHT])
        kick = int(keys[pygame.K_p])

        Phy.p2_on_gro = Pl2.motion(Pl2_obj,Phy.p2_on_gro,up,left,right)
        Pl2.motion_leg(Pl2_obj,kick,math.pi)

        # Goal check
        score = Bal.goal_check(Bal_obj,right_cor,left_cor,W,H)


        screen.fill(pygame.Color("white"))

        Phy.update(draw_options)

        screen.blit(Pl1_leg_sprite,(Pl1_obj.position.x-Pl1.size//2,Pl1_obj.position.y+Pl1.size))
        screen.blit(Bg_sprite, (0,0))
        screen.blit(Pl1_sprite, (Pl1_obj.position.x - (Pl1.size*1.4), Pl1_obj.position.y - (Pl1.size*1.4)))
        screen.blit(Pl2_sprite, (Pl2_obj.position.x - (Pl2.size*1.2), Pl2_obj.position.y - (Pl2.size*1.4)))     
        screen.blit(pygame.transform.rotate(Bal_sprite, -Bal_obj.angle * 180 / math.pi),
                    pygame.transform.rotate(Bal_sprite, -Bal_obj.angle * 180 / math.pi).get_rect(center=Bal_obj.position))
       
        screen.blit(pygame.transform.rotate(Pl1_leg_sprite, (-Pl1_obj.angle-(math.pi/2)*Pl1.ort) * 180 / math.pi),
        (Pl1_obj.position.x + math.sin(-Pl1_obj.angle)*Pl1.size - (Pl1_leg_sprite.get_width()//2),Pl1_obj.position.y + math.cos(Pl1_obj.angle)*Pl1.size - (Pl1_leg_sprite.get_height()//2)))
        screen.blit(pygame.transform.rotate(Pl2_leg_sprite, (-Pl2_obj.angle-(math.pi/2)*Pl2.ort) * 180 / math.pi),
        (Pl2_obj.position.x + math.sin(-Pl2_obj.angle)*Pl2.size - (Pl2_leg_sprite.get_width()//2),Pl2_obj.position.y + math.cos(Pl2_obj.angle)*Pl2.size - (Pl2_leg_sprite.get_height()//2)))

        screen.blit(Pl1_goal_sprite,Pl1_goal_sprite_rect)
        screen.blit(Pl2_goal_sprite,Pl2_goal_sprite_rect)

        screen.blit(score_font.render(f"{score[0]} - {score[1]}", True, (0, 0, 0)), score_font.render(f"{score[0]} - {score[1]}", True, (0, 0, 0)).get_rect(center=(W/2, H/2*0.5)))

        pygame.display.flip()
        clock.tick(60)
        pygame.display.set_caption("fps: " + str(int(clock.get_fps())))


if __name__ == "__main__":
    sys.exit(main())