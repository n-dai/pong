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

        p1_score_font = game.font.SysFont("calibri", 70)
        p1_score_text = p1_score_font.render(str(self.p1_score), True, self.white)
        self.screen.blit(p1_score_text, (self.half_width - 100 , (self.screen_height / 2) - 300))

        p2_score_font = game.font.SysFont("calibri", 70)
        p2_score_text = p2_score_font.render(str(self.p2_score), True, self.white)
        self.screen.blit(p2_score_text, (self.half_width + 68, (self.screen_height / 2) - 300))

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
        ball.init_y = 2.5

        ball.rally_count = 0
        ball.special_ability_y = 0

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
            game_state.game_over()
            ball.ball_init()
            ball.point_detect()
            ball.special_ability()
            ball.ball_move()
            ball.ball_deflect_y_direction()
            ball.win_detect()
            paddle.move()
            paddle.paddle_create()
            paddle.border_check()
            paddle.paddle_AI()

# Class to hold all information regarding the pong ball
class Ball:
    
    green = (0, 255, 0)
    special_colour = (0, 0, 0)
    ball_colour =(255, 255, 255)
    x_ball_dir = GameState.half_width
    y_ball_dir = GameState.half_height

    ball_velocity = 4
    init_y = 2.5
    ball_movement_x = ball_velocity
    ball_movement_y = init_y

    rally_count = 0
    special_ability_y = 0
    special_ability_x = 0
    special_velocity = 0
    special_hit = 0
    special_1_count = 0
    special_3_count = 0
    special_3_count_ai = 0
    abilities = random.randint(1,2)

    ability_text = " "

    def ball_init(self):
        game.draw.circle(game_state.screen, ((ball.ball_colour)), (self.x_ball_dir, self.y_ball_dir), 8)

        if self.special_1_count == 1:
            ball.ball_colour = (255, 0, 0)
        
        if self.special_1_count == 0:
            ball.ball_colour = (255, 255, 255)

    def ball_move(self):
        
        if game_state.game_over() == 1 or paddle.level_select == 0:
            self.x_ball_dir = game_state.half_width
            self.y_ball_dir = game_state.half_height
        else:
            self.x_ball_dir += self.ball_movement_x
            self.y_ball_dir += self.ball_movement_y

        # If the ball hits the middle of the paddle, the x velocity is increased by 25%, if the ball hits the ends of the paddle
        # the y velocity is increased by 50% and the x velocity is decreased by 10%

    #---------------------------- Ball movement for player paddle -----------------------------------#
        if self.x_ball_dir - 8 < paddle.x_direction + 20 and self.x_ball_dir - 8 > paddle.x_direction + 10:
            if self.y_ball_dir > paddle.y_direction and self.y_ball_dir < paddle.y_direction + 38:
                self.ball_movement_x = 0.9 * self.ball_velocity

                if self.ball_movement_y > 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = 1.1 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = - (1.1 * self.init_y)

                self.rally_count += 1
                self.special_3_count = 0
                self.special_1_count = 0
        
        if self.x_ball_dir - 8 < paddle.x_direction + 20 and self.x_ball_dir - 8 > paddle.x_direction + 10:
            if self.y_ball_dir > paddle.y_direction + 39 and self.y_ball_dir < paddle.y_direction + 77:
                self.ball_movement_x = 1.2 * self.ball_velocity

                if self.ball_movement_y > 0:
                    self.init_y = 0.9 * self.init_y
                    self.ball_movement_y = 0.9 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 0.9 * self.init_y
                    self.ball_movement_y = - (0.9 * self.init_y)

                self.rally_count += 1
                self.special_3_count = 0
                self.special_1_count = 0

        if self.x_ball_dir - 8 < paddle.x_direction + 20 and self.x_ball_dir - 8 > paddle.x_direction + 10:
            if self.y_ball_dir > paddle.y_direction + 78 and self.y_ball_dir < paddle.y_direction + 115:
                self.ball_movement_x = 0.9 * self.ball_velocity
                
                if self.ball_movement_y > 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = 1.1 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = - (1.1 * self.init_y)
                
                self.rally_count += 1
                self.special_3_count = 0
                self.special_1_count = 0
        
        #---------------------------- Ball movement for computer paddle -----------------------------------#
        if self.x_ball_dir + 8 > paddle.x_direction_op and self.x_ball_dir + 8 < paddle.x_direction_op + 10:
            if self.y_ball_dir > paddle.y_direction_op + 39 and self.y_ball_dir < paddle.y_direction_op + 77:
                self.ball_movement_x = - ( 1.2 * self.ball_velocity)

                if self.ball_movement_y > 0:
                    self.init_y = 0.9 * self.init_y
                    self.ball_movement_y = 0.9 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 0.9 * self.init_y
                    self.ball_movement_y = - (0.9 * self.init_y)

                self.rally_count += 1
                self.special_3_count_ai = 0
                self.special_1_count = 0

        if self.x_ball_dir + 8 > paddle.x_direction_op and self.x_ball_dir + 8 < paddle.x_direction_op + 10: 
            if self.y_ball_dir > paddle.y_direction_op + 78 and self.y_ball_dir < paddle.y_direction_op + 115:
                self.ball_movement_x = - (0.9 * self.ball_velocity)
                
                if self.ball_movement_y > 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = 1.1 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = - (1.1 * self.init_y)
                
                self.rally_count += 1
                self.special_3_count_ai = 0
                self.special_1_count = 0
    
        if self.x_ball_dir + 8 > paddle.x_direction_op and self.x_ball_dir + 8 < paddle.x_direction_op + 10: 
            if self.y_ball_dir > paddle.y_direction_op and self.y_ball_dir < paddle.y_direction_op + 38:
                self.ball_movement_x = - (0.9 * self.ball_velocity)
                
                if self.ball_movement_y > 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = 1.1 * self.init_y
                elif self.ball_movement_y < 0:
                    self.init_y = 1.1 * self.init_y
                    self.ball_movement_y = - (1.1 * self.init_y)

                self.rally_count += 1
                self.special_3_count_ai = 0
                self.special_1_count = 0
    
    # Function to handle the ball deflection on the y axis
    def ball_deflect_y_direction(self):

        if self.y_ball_dir > game_state.screen_height:
            self.ball_movement_y = -1 * self.init_y
        if self.y_ball_dir < 0:
            self.ball_movement_y = self.init_y

    # Function to handle the game state when a point is scored by either opponent 
    def point_detect(self):

        if self.x_ball_dir > game_state.screen_width + 10:
            self.x_ball_dir = game_state.half_width
            self.y_ball_dir = game_state.half_height
            game_state.p1_score += 1
            self.rally_count = 0
            self.special_hit = 0
            self.ball_movement_x = 4
            self.special_3_count_ai = 0
            self.special_1_count = 0
            self.special_ability_y = 0
            self.init_y = random.randint(1,3)
            self.ball_movement_y = self.init_y
            self.ball_velocity = 4
            game.time.delay(1000)
        
        if self.x_ball_dir < -10:
            self.x_ball_dir = game_state.half_width
            self.y_ball_dir = game_state.half_height
            game_state.p2_score += 1
            ball.rally_count = 0
            self.special_hit = 0
            self.ball_movement_x = - 4
            self.special_3_count = 0
            self.special_1_count = 0
            self.special_ability_y = 0
            self.init_y = random.randint(1,3)
            self.ball_movement_y = self.init_y
            self.ball_velocity = 4
            game.time.delay(1000)

    
    # Function to detect a win, if any side scores 7 points they win
    def win_detect(self):

        if game_state.p1_score >= 7:
            game_state.score_message = "Game Over Player 1 wins"
            return 1
        
        if game_state.p2_score >= 7:
            game_state.score_message = "Game Over Player 2 wins"
            return 2    
    
    # Function to handle the special abilities of the game
    def special_ability(self):

        self.special_ability_y += self.special_velocity

        if self.abilities == 1:
            self.special_colour = (255, 0, 0)
            self.ability_text ="2x Speed"
        
        # if self.abilities == 2:
        #     self.special_colour = (0, 255, 0)
        #     self.ability_text = "Not"
        
        if self.abilities == 2:
            self.special_colour = (0, 255, 255)
            self.ability_text = "Freeze"

        if self.rally_count > 7:
            game.draw.circle(game_state.screen, (self.special_colour), (game_state.half_width, self.special_ability_y), 30)

            ability_font = game.font.SysFont("calibri", 12)
            ability_text =  ability_font.render(self.ability_text, True, game_state.white)
            game_state.screen.blit(ability_text, (game_state.half_width - 15, self.special_ability_y - 5))

            if self.special_ability_y > GameState.screen_height:
                self.special_velocity = -0.5
        
            if self.special_ability_y < 1:
                self.special_velocity = 0.5

        # Conditions to make the special ability circle dissapear  
        if self.x_ball_dir < game_state.half_width + 30 and self.x_ball_dir > game_state.half_width - 30 and self.special_hit != 1:
            if self.y_ball_dir < self.special_ability_y + 30 and self.y_ball_dir > self.special_ability_y - 30:
                self.special_hit += 1
                self.rally_count = 0
                self.special_colour = (0, 0, 0)
                self.special_ability_y = -35
                self.special_velocity = 0

                if self.abilities == 1 and self.ball_movement_x < 0:
                    self.ball_movement_x = - 8
                    self.special_1_count += 1
                    self.special_hit = 0
                
                if self.abilities == 1 and self.ball_movement_x > 0:
                    self.ball_movement_x = 8
                    self.special_1_count += 1
                    self.special_hit = 0
                
                if self.abilities == 2 and self.ball_movement_x < 0:
                    self.special_3_count += 1
                    paddle.paddle_colour = (0, 255, 255)
                    self.special_hit = 0
                
                if self.abilities == 2 and self.ball_movement_x > 0:
                    self.special_3_count_ai += 1
                    paddle.paddle_colour_ai = (0, 255, 255)
                    self.special_hit = 0
                
                self.abilities = random.randint(1,2)
        
class Paddle:

    white = (255, 255, 255)
    paddle_colour = (255, 255, 255)
    paddle_colour_ai = (255, 255, 255)
    velocity = 4

    x_origin = GameState.screen_width/2 - 570
    y_origin = GameState.screen_height/2 - 100

    x_direction_op = 1270
    y_direction_op = y_origin

    x_direction = x_origin
    y_direction = y_origin

    ai_speed = 0

    level_select = 0

    # Function to draw the paddles
    def paddle_create(self):

        if ball.special_3_count == 0:
            self.paddle_colour = (255, 255, 255)

        if ball.special_3_count_ai == 0:
            self.paddle_colour_ai = (255, 255, 255)

        game.draw.rect(GameState.screen, (self.paddle_colour), [self.x_direction, self.y_direction, 20, 115] )
        game.draw.rect(GameState.screen, (self.paddle_colour_ai), [self.x_direction_op, self.y_direction_op, 20, 115] )

        game.display.flip()
    
    # Simple AI that tracks the position of the ball's y position
    def paddle_AI(self):

        if ball.x_ball_dir > game_state.half_width:

            if ball.y_ball_dir > paddle.y_direction_op + 50 and ball.special_3_count_ai == 0:
                self.y_direction_op += self.ai_speed

            if ball.y_ball_dir < paddle.y_direction_op and ball.special_3_count_ai == 0:
                self.y_direction_op -= self.ai_speed


    # Function to handle keybinds of the game
    def move(self):
        
        keys = game.key.get_pressed()
    #----- Movement --------#
        if keys[game.K_w]:

            if game_state.game_over() != 1 and paddle.level_select != 0 and ball.special_3_count == 0:
                self.y_direction -= self.velocity

        if keys[game.K_s]:
            if game_state.game_over() != 1 and paddle.level_select != 0 and ball.special_3_count == 0:
                self.y_direction += self.velocity

        if keys[game.K_o]:
            self.y_direction_op -= self.velocity

        if keys[game.K_l]:
            self.y_direction_op += self.velocity
        
        #----- Level selector --------#
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
            self.y_direction = game_state.screen_height - 120

        if self.y_direction_op < 0:
            self.y_direction_op = 1
        
        if self.y_direction_op > game_state.screen_height - 115:
            self.y_direction_op = game_state.screen_height - 114

game_state = GameState()
paddle = Paddle()
ball = Ball()

game_state.game_loop()