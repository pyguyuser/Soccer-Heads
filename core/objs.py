class Player:
    def __init__(self,coordinates,mass,size,speed,power,
                    friction,elasticity,orientation,sprite_path,sprite_leg_path,sprite_goal_path):
        self.coord = coordinates            
        self.mass = mass
        self.size = size
        self.speed = speed
        self.power = power
        self.fric = friction
        self.elast = elasticity
        self.ort = orientation 
        self.sprite_p = sprite_path
        self.sprite_l_p = sprite_leg_path
        self.sprite_g_p = sprite_goal_path

    def motion(self,body,flag,up,left,right):
        if up and flag:
            body.velocity += (0,-self.speed[1]) 
            return False
        if left:
            body.velocity = (-self.speed[0],body.velocity.y)
        elif right:
            body.velocity = (self.speed[0],body.velocity.y)
        else:
            body.velocity = (0.0,body.velocity.y)
            
        return flag

    def motion_leg(self,body,kick,pi):
        if kick: 
            if 0.0 <= abs(body.angle) < pi/2:
                body.angular_velocity = self.power * self.ort
            else:
                body.angular_velocity = 0.0
                body.angle = pi/2 * self.ort
        else:
            body.angular_velocity = 0.0
            sign = abs(body.angle+0.1) // (body.angle+0.1)
            if abs(body.angle-0.0)<0.1 or abs(body.angle-2*pi*sign)<0.1:
                    body.angle = 0.0 
            else:
                if body.angle > (2*pi*sign - body.angle):
                    body.angle  += 0.1
                else:
                    body.angle -= 0.1 
        

class Ball:
    def __init__(self,coordinates,mass,size,
                    friction,elasticity,sprite_path):
        self.coord = coordinates 
        self.mass = mass
        self.size = size
        self.fric = friction
        self.elast = elasticity
        self.sprite_p = sprite_path

        self.score = (0,0)


    def goal_check(self,body,goal1_sur,goal2_sur,W,H):
        if (body.position.x < goal1_sur[0] and body.position.y > goal1_sur[1]): self.score = (self.score[0],) + (self.score[1]+1,)
        elif (body.position.x > goal2_sur[0] and body.position.y > goal2_sur[1]): self.score = (self.score[0]+1,) + (self.score[1],)
        else: return self.score
        body.angular_velocity = 0.0
        body.velocity = (0.0,0.0)
        body.position = (W//2,H//2)

        return self.score


class Ground:
    def __init__(self,first_position,second_position,size,
                    friction,elasticity,sprite_path):
        self.first_po = first_position
        self.second_po = second_position
        self.size = size
        self.fric = friction
        self.elast = elasticity
        self.sprite_p = sprite_path