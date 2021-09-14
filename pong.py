import pygame as game
import random
import sys

# solid contribution

# Game state class, holds all information regarding the game
class GameState:

    # Defining the initial variables of the game window, colours and score
  
    screen_width = 1400
    screen_height = 800
    half_width = screen_width / 2
    half_height = screen_height / 2

    bg_colour = (0, 0, 0)
    white = (255, 255, 255)

    p1_score = 0
    p2_score = 0
    score_message = " "
    restart_message = "Press R to restart, or Q to quit"
    welcome_message = " "

    screen = game.display.set_mode((screen_width, screen_height))

    # Function to initialise the game window
    def pygame_init(self):
        game.init()
        game.font.init()

    def window_init(self):
        self.pygame_init()
        game.display.set_caption('Pong AI')
        self.screen.fill(self.bg_colour)
        game.display.flip()

    # Function to draw the dividing line of the game
    def middle_line(self):
        
        # For the range of the screen height, a white pixel is drawn if the floor division of 10 of that number is even
        # Therefore the middle dashed line should be 10 pixels of white followed by 10 pixels of black etc
        for x in range(0, self.screen_width):
            if (x // 10) % 2 == 0:
                game.draw.rect(self.screen, paddle.white, [self.screen_width/2, x, 1, 1])
            else: 
                game.draw.rect(self.screen, self.bg_colour, [self.screen_width/2, x, 1, 1])
        
        game.draw.rect(self.screen, paddle.white, [self.screen_width/2, 799, 1, 30])

    # Function to display the game score
    def game_score_display(self):

        p1_score_font = game.font.SysFont("calibri", 64)
        p1_score_text = p1_score_font.render(str(self.p1_score), True, self.white)
        self.screen.blit(p1_score_text, (self.screen_width / 4 , self.screen_height / 2))

        p2_score_font = game.font.SysFont("calibri", 64)
        p2_score_text = p2_score_font.render(str(self.p2_score), True, self.white)
        self.screen.blit(p2_score_text, (3/4 * self.screen_width, self.screen_height / 2))

        score_font = game.font.SysFont("calibri", 32)
        score_text = score_font.render(game_state.score_message, True, self.white)
        self.screen.blit(score_text, (self.half_width - 150, self.half_height))

        if self.game_over() == 1:
            game_over_font = game.font.SysFont("calibri", 32)
            game_over_text =  game_over_font.render(self.restart_message, True, self.white)
            self.screen.blit(game_over_text, (self.half_width - 200, 10))

        if paddle.level_select == 0:
            self.welcome_message = "Welcome to Pong, please select your difficulty: [1] - [2] - [3]"
        else:
            self.welcome_message = " "
            
        welcome_font = game.font.SysFont("calibri", 32)
        welcome_text =  welcome_font.render(self.welcome_message, True, self.white)
        self.screen.blit(welcome_text, (300, 10))


    # Function to reset the game's values back to the init state
    def game_reset(self):
        
        ball.x_ball_dir = GameState.screen_width / 2
        ball.y_ball_dir = GameState.screen_height / 2

        paddle.x_direction = paddle.x_origin
        paddle.y_direction = paddle.y_origin

        paddle.x_direction_op = 1250
        paddle.y_direction_op = paddle.y_origin

        paddle.level_select = 0

        ball.ball_velocity = 3
        ball.ball_movement_x = ball.ball_velocity

        game_state.p1_score = 0
        game_state.p2_score = 0

        game_state.score_message = " "
        
        game.time.delay(1000)
    
    def game_over(self):

        if ball.win_detect() == 1 or ball.win_detect() == 2:
            return 1

    # The game loop
    def game_loop(self):
        
        self.window_init()
        running = True
        while running:
            game.time.delay(2)
            paddle.move()
            for event in game.event.get():

                if event.type == game.QUIT: 
                    running = False
                    game.quit()
                    sys.exit()

            game_state.screen.fill(self.bg_colour)
            game_state.middle_line()
            game_state.game_score_display()
            ball.ball_init()
            ball.ball_move()
            ball.ball_deflect()
            ball.point_detect()
            ball.win_detect()
            paddle.move()
            paddle.paddle_create()
            paddle.border_check()
            paddle.paddle_AI()
            game_state.game_over()

# Class to hold all information regarding the pong ball
class Ball:
    
    x_ball_dir = GameState.half_width
    y_ball_dir = GameState.half_height

    ball_velocity = 3
    init_y = random.randint(1, 3)
    ball_movement_x = ball_velocity
    ball_movement_y = init_y


    def ball_init(self):
        game.draw.circle(game_state.screen, ((paddle.white)), (self.x_ball_dir, self.y_ball_dir), 8)

    def ball_move(self):
        
        if game_state.game_over() == 1 or paddle.level_select == 0:
            self.x_ball_dir = game_state.half_width
            self.y_ball_dir = game_state.half_height
        else:
            self.x_ball_dir += self.ball_movement_x
            self.y_ball_dir += self.ball_movement_y

        if self.x_ball_dir < paddle.x_direction + 20 and self.x_ball_dir > paddle.x_direction:
            if self.y_ball_dir > paddle.y_direction and self.y_ball_dir < paddle.y_direction + 115:
                self.ball_movement_x = self.ball_velocity
            
        elif self.x_ball_dir > paddle.x_direction_op and self.x_ball_dir < paddle.x_direction_op + 20:
            if self.y_ball_dir > paddle.y_direction_op and self.y_ball_dir < paddle.y_direction_op + 115:
                self.ball_movement_x = -self.ball_velocity
    
    def ball_deflect(self):

        if self.y_ball_dir > game_state.screen_height:
            self.ball_movement_y = - random.randint(1,3)
        if self.y_ball_dir < 0:
            self.ball_movement_y = random.randint(1,3)


    def point_detect(self):

        if self.x_ball_dir > game_state.screen_width + 10:
            self.x_ball_dir = game_state.half_width
            game_state.p1_score += 1
            game.time.delay(1000)
        
        if self.x_ball_dir < -10:
            self.x_ball_dir = game_state.half_width
            game_state.p2_score += 1
            game.time.delay(1000)

    
    def win_detect(self):

        if game_state.p1_score >= 2:
            game_state.score_message = "Game Over Player 1 wins"
            return 1
        
        if game_state.p2_score >= 2:
            game_state.score_message = "Game Over Player 2 wins"
            return 2

class Paddle:

    white = (255, 255, 255)
    velocity = 4

    x_origin = GameState.screen_width/2 - 550
    y_origin = GameState.screen_height/2 - 100

    x_direction_op = 1250
    y_direction_op = y_origin

    x_direction = x_origin
    y_direction = y_origin

    ai_speed = 0

    level_select = 0

    def paddle_create(self):

        game.draw.rect(GameState.screen, (self.white), [self.x_direction, self.y_direction, 20, 115] )
        game.draw.rect(GameState.screen, (self.white), [self.x_direction_op, self.y_direction_op, 20, 115] )

        game.display.flip()
    
    def paddle_AI(self):

        if ball.x_ball_dir > game_state.half_width:

            if ball.y_ball_dir > paddle.y_direction_op:
                self.y_direction_op += self.ai_speed

            if ball.y_ball_dir < paddle.y_direction_op:
                self.y_direction_op -= self.ai_speed


    def move(self):
        
        keys = game.key.get_pressed()

        if keys[game.K_w]:

            if game_state.game_over() != 1 and paddle.level_select != 0:
                self.y_direction -= self.velocity

        if keys[game.K_s]:
            if game_state.game_over() != 1 and paddle.level_select != 0:
                self.y_direction += self.velocity

        if keys[game.K_o]:
            self.y_direction_op -= self.velocity

        if keys[game.K_l]:
            self.y_direction_op += self.velocity
        
        if keys[game.K_1]:
            if self.level_select == 0:
                self.ai_speed = 3.2
                self.level_select += 1
        
        if keys[game.K_2]:
            if self.level_select == 0:
                self.ai_speed = 4.5
                self.level_select += 1

        if keys[game.K_3]:
            if self.level_select == 0:
                self.ai_speed = 5
                self.level_select += 1
        
        if keys[game.K_r]:
            game_state.game_reset()

        if keys[game.K_q]:
            game.quit()
    
    def border_check(self):

        if self.y_direction < 0:
            self.y_direction = 1
        
        if self.y_direction > game_state.screen_height - 115:
            self.y_direction = game_state.screen_height - 114

        if self.y_direction_op < 0:
            self.y_direction_op = 1
        
        if self.y_direction_op > game_state.screen_height - 115:
            self.y_direction_op = game_state.screen_height - 114

game_state = GameState()
paddle = Paddle()
ball = Ball()

game_state.game_loop()