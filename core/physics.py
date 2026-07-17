import pymunk

class Physics:
    def __init__(self,gravity,damping):
        self.space = pymunk.Space()
        self.space.gravity = gravity[0],gravity[1]
        self.space.damping = damping
        
        self.num_of_collision_objs = 0
        self.num_of_cat_objs = 0

        # collisions between players and ground
        self.p1_on_gro = False
        self.p2_on_gro = False

        # collisions between player's legs and ball
        self.p1_leg_ball = False
        self.p2_leg_ball = False



    def player_and_ball(self,obj):
        obj_body = pymunk.Body(mass=obj.mass, moment=pymunk.moment_for_circle(obj.mass, 0, obj.size))
        obj_body.position = obj.coord[0], obj.coord[1]

        obj_shape = pymunk.Circle(obj_body, radius=obj.size)
        obj_shape.elasticity = obj.elast
        obj_shape.friction = obj.fric

        self.num_of_collision_objs += 1
        obj_shape.collision_type = self.num_of_collision_objs


        self.space.add(obj_body,obj_shape)

        return obj_body

    def ground(self,obj):
        obj_body = self.space.static_body
        obj_seg = pymunk.Segment(obj_body, obj.first_po, obj.second_po, obj.size)
        obj_seg.elasticity = obj.elast
        obj_seg.friction = obj.fric

        self.num_of_collision_objs += 1
        obj_seg.collision_type = self.num_of_collision_objs

        self.num_of_cat_objs += 1
        obj_seg.filter = pymunk.ShapeFilter(categories=self.num_of_cat_objs)
        
        self.space.add(obj_seg)

        return obj_body

    def leg(self,obj,size):
        coords = [(0, size*1.5),(0,0)]
        obj_pol = pymunk.Poly(obj, coords)
        obj_pol.friction = 0.9

        self.num_of_collision_objs += 1
        obj_pol.collision_type = self.num_of_collision_objs

        self.num_of_cat_objs += 1
        obj_pol.filter = pymunk.ShapeFilter(categories=self.num_of_cat_objs,mask=pymunk.ShapeFilter.ALL_MASKS() ^ 1)

        self.space.add(obj_pol)

        return obj_pol

    def player1_and_ground_collide(self,arb,space,data):
        self.p1_on_gro = True
    
    def player2_and_ground_collide(self,arb,space,data):
        self.p2_on_gro = True

    def player1_leg_and_ball_collide(self,arb,space,data):
        self.p1_leg_ball = True

    def player2_leg_and_ball_collide(self,arb,space,data):
        self.p2_leg_ball = True


    def update(self,opt):
        for _ in range(4):
            self.space.step(1/280.0)

        self.space.debug_draw(opt)

    