import pygame,pymunk ,math
import pymunk.pygame_util

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((802, 543))

draw_options = pymunk.pygame_util.DrawOptions(screen)

def zerovel(arbit,space,data):
    global obj_body,poly_bad
    print('1')
    obj_body.velocity = (0.0,0.0)
    # poly_bad.velocity = (0.0,0.0)

space = pymunk.Space()
space.gravity = (0,700)
space.damping = 0.95

b1 = space.static_body
segment1 = pymunk.Segment(b1, (0, 543), (802, 543), 40)
segment1.elasticity = 0.5
segment1.friction = 0.9


obj_body = pymunk.Body(mass=10, moment=pymunk.moment_for_circle(10, 0, 20))
obj_body.position = 500, 400

obj_shape = pymunk.Circle(obj_body, radius=20)
obj_shape.elasticity = 0.9
obj_shape.friction = 0

obj_body1 = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, 10))
obj_body1.position = 470, 400

obj_shape1 = pymunk.Circle(obj_body1, radius=10)
obj_shape1.elasticity = 1.5
obj_shape1.friction = 0.9




width, height = 10, 20
vs = [(0, 40), (0,0)]
poly_bad = pymunk.Poly(obj_body, vs)


obj_shape1.collision_type = 3
poly_bad.collision_type = 4


leg = 2
gro = 4
poly_bad.filter = pymunk.ShapeFilter(
    categories=leg,
    mask=pymunk.ShapeFilter.ALL_MASKS() ^ 1
)

segment1.filter = pymunk.ShapeFilter(
    categories=1,
    # mask=pymunk.ShapeFilter.ALL_MASKS() ^ leg
)

space.on_collision(3,4,separate=zerovel)


flag = True
obj_body.angle = -4
space.add(poly_bad,obj_body1,obj_body,obj_shape,segment1,obj_shape1)
running = True



while running:
    
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            running = False

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
                # obj_body.angular_velocity = 20.0

                # o = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, 10))
                # o.position = 470, 400
                
                # o_s = pymunk.Circle(o, radius=10)
                # o_s.elasticity = 0.9
                # o_s.friction = 0.9

                # o_s.collision_type = 3
                # space.add(o,o_s)
    keys = pygame.key.get_pressed()
    kick = keys[pygame.K_SPACE]

    if kick:     
        if 0.0 <= obj_body.angle < math.pi/2:
            obj_body.angular_velocity = 15

        else:
            obj_body.angular_velocity = 0.0
            obj_body.angle = math.pi/2 
    else:
        obj_body.angular_velocity = 0.0
        sign = abs(obj_body.angle+0.1) // (obj_body.angle+0.1)
        if abs(obj_body.angle-0.0)<0.1 or abs(obj_body.angle-2*math.pi*sign)<0.1:
                obj_body.angle = 0.0 
        else:
            if obj_body.angle > (2*math.pi*sign - obj_body.angle):
                obj_body.angle  += 0.1
            else:
                obj_body.angle -= 0.1 

        # obj_body.angle = 0.0
    #     if obj_body.angle != 0.0:
    #         sign =  obj_body.angle // abs(obj_body.angle)
    #         if abs(obj_body.angle-0.0)<0.1:
    #             obj_body.angle = 0.0 
    #         else:
    #             obj_body.angle -= 0.1 

    screen.fill(pygame.Color("white"))


    for _ in range(4):
        space.step(1/280.0)

    space.debug_draw(draw_options)


    # if abs(obj_body.angle) > 0.2 and flag:
    #     if abs(math.pi-obj_body.angle)>abs(obj_body.angle):
    #         obj_body.angle -= 0.01 * (abs(obj_body.angle) // obj_body.angle)
    #     else:
    #         obj_body.angle = (math.pi-obj_body.angle) - 0.01 * (abs(math.pi-obj_body.angle) // math.pi-obj_body.angle)
    # else:obj_body.angle = 0.0


    # if obj_body.angle < 0:
    #     obj_body.angular_velocity =0
    #     obj_body.angle = 0.0
        
    
    # print(obj_body.angle)
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(int(clock.get_fps())))