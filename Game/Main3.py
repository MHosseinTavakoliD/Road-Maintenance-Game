import numpy as np
import pygame
import indexes
import time

# For Next update:
# Rule for salting: At 30F (surface temp T)  W= 140 lb/mile/lane is required,
# and At 15F 400 lb/mile/lane is required to melt the ice on the road, W = -17.3* T + 660

# Rule for velocity decrease:
# In "MDSS FUNCTIONAL PROTOTYPE " Page 32 pdf. Mobility index is defined based on the snow depth.

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
LIGHT_RED = pygame.Color(155, 0, 0)
GREEN = pygame.Color(0, 255, 0)
DARK_GREEN = pygame.Color(1, 50, 32)
BLUE = pygame.Color(0, 0, 128)
LIGHT_BLUE = pygame.Color(173, 216, 230)
ORANGE = pygame.Color(255,140,0)
GRAY = pygame.Color(119, 136, 153)
pygame.font.init()
X_screen = 800
Y_screen = 600
Veh_speed = 0.05
Initial_snow_depth = 0
Snow_depth = Initial_snow_depth


class MDSSEnv():
    def __init__(self):
        # Define game screen size
        self.frame_size_x = X_screen
        self.frame_size_y = Y_screen
        self.screen = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        self.X_Left_Snow = 0.05 * self.frame_size_x
        self.X_Right_Snow = 0.7 * self.frame_size_x
        self.Y_Up_Snow = 0.7 * self.frame_size_y
        self.Y_Down_Snow = 0.87 * self.frame_size_y
        self.Snow_depth = Snow_depth

    def reset(self):
        # CLear the screen
        self.screen.fill(WHITE)
        # # Draw the road lines
        self.Road_first_point01 = [0.05 * self.frame_size_x, 0.9 * self.frame_size_y]
        self.Road_last_point01 = [0.7 * self.frame_size_x, 0.9 * self.frame_size_y]
        pygame.draw.line(self.screen, BLACK, self.Road_first_point01, self.Road_last_point01, 2)

        # Draw the data text box
        TextBox_first_point = [0.75 * self.frame_size_x, 0.95 * self.frame_size_y]
        TextBox_2nd_point = [0.98 * self.frame_size_x, 0.95 * self.frame_size_y]
        TextBox_3rd_point = [0.98 * self.frame_size_x, 0.05 * self.frame_size_y]
        TextBox_4th_point = [0.75 * self.frame_size_x, 0.05 * self.frame_size_y]
        pygame.draw.lines(self.screen, BLUE, False, [TextBox_first_point,
                                                     TextBox_2nd_point, TextBox_3rd_point, TextBox_4th_point,
                                                     TextBox_first_point], 2)

        # Draw the Decision text box
        D_TextBox_first_point = [0.05 * self.frame_size_x, 0.05 * self.frame_size_y]
        D_TextBox_2nd_point = [0.05 * self.frame_size_x, 0.45 * self.frame_size_y]
        D_TextBox_3rd_point = [0.7 * self.frame_size_x, 0.45 * self.frame_size_y]
        D_TextBox_4th_point = [0.7 * self.frame_size_x, 0.05 * self.frame_size_y]
        pygame.draw.lines(self.screen, BLUE, False, [D_TextBox_first_point, D_TextBox_2nd_point,
                                                     D_TextBox_3rd_point, D_TextBox_4th_point,
                                                     D_TextBox_first_point], 2)
        # Draw the Decision text box contents (Column)
        text_font = pygame.font.Font('freesansbold.ttf', 12)
        # Before Storm
        Before_storm_text = text_font.render('Before Storm', True, DARK_GREEN)
        Before_storm_textRect = Before_storm_text.get_rect()
        Before_storm_textRect.center = (0.07 * self.frame_size_x, 0.17 * self.frame_size_y)
        self.screen.blit(Before_storm_text, Before_storm_textRect.center)
        # During Storm
        During_storm_text = text_font.render('During Storm', True, DARK_GREEN)
        During_storm_textRect = During_storm_text.get_rect()
        During_storm_textRect.center = (0.07 * self.frame_size_x, 0.27 * self.frame_size_y)
        self.screen.blit(During_storm_text, During_storm_textRect.center)
        # After Storm
        After_storm_text = text_font.render('After Storm', True, DARK_GREEN)
        After_storm_textRect = After_storm_text.get_rect()
        After_storm_textRect.center = (0.07 * self.frame_size_x, 0.38 * self.frame_size_y)
        self.screen.blit(After_storm_text, After_storm_textRect.center)

        # Draw the Decision text box contents (Row)
        # Plow
        Plow_text = text_font.render('Plowing', True, WHITE, BLUE)
        Plow_textRect = Plow_text.get_rect()
        Plow_textRect.center = (0.35 * self.frame_size_x, 0.08 * self.frame_size_y)
        self.screen.blit(Plow_text, Plow_textRect.center)
        # line under plow
        Plow_line_point1 = [0.25 * self.frame_size_x,0.12 * self.frame_size_y]
        Plow_line_point2 = [0.5* self.frame_size_x,0.12 * self.frame_size_y]
        pygame.draw.lines(self.screen, BLUE, False, [Plow_line_point1, Plow_line_point2] , 2)\
        # First run text
        Plow_1st_run_text = text_font.render('1st Run', True, BLACK, WHITE)
        Plow_1st_run_textRect = Plow_1st_run_text.get_rect()
        Plow_1st_run_textRect.center = (0.25 * self.frame_size_x, 0.14 * self.frame_size_y)
        self.screen.blit(Plow_1st_run_text, Plow_1st_run_textRect.center)
        # Second run text
        Plow_2nd_run_text = text_font.render('2nd Run', True, BLACK, WHITE)
        Plow_2nd_run_textRect = Plow_2nd_run_text.get_rect()
        Plow_2nd_run_textRect.center = (0.35 * self.frame_size_x, 0.14 * self.frame_size_y)
        self.screen.blit(Plow_2nd_run_text, Plow_2nd_run_textRect.center)
        # Third run text
        Plow_3rd_run_text = text_font.render('3rd Run', True, BLACK, WHITE)
        Plow_3rd_run_textRect = Plow_3rd_run_text.get_rect()
        Plow_3rd_run_textRect.center = (0.45 * self.frame_size_x, 0.14 * self.frame_size_y)
        self.screen.blit(Plow_3rd_run_text, Plow_3rd_run_textRect.center)

        # Salt
        Salt_text = text_font.render('Salting', True, WHITE, BLUE)
        Salt_textRect = Salt_text.get_rect()
        Salt_textRect.center = (0.6 * self.frame_size_x, 0.08 * self.frame_size_y)
        self.screen.blit(Salt_text, Salt_textRect.center)

        # Add CheckBoxes
        boxes = []
        self.chkbox_plow_beforeStorm1 = indexes.INDEX(self.screen, 0.27 * self.frame_size_x, 0.17 * self.frame_size_y, 0)
        self.chkbox_plow_beforeStorm2 = indexes.INDEX(self.screen, 0.37 * self.frame_size_x, 0.17 * self.frame_size_y, 0)
        self.chkbox_plow_beforeStorm3 = indexes.INDEX(self.screen, 0.47 * self.frame_size_x, 0.17 * self.frame_size_y, 0)
        self.chkbox_salt_beforeStorm = indexes.INDEX(self.screen, 0.62 * self.frame_size_x, 0.17 * self.frame_size_y, 1)

        self.chkbox_plow_duringStorm1 = indexes.INDEX(self.screen, 0.27 * self.frame_size_x, 0.27 * self.frame_size_y, 2)
        self.chkbox_plow_duringStorm2 = indexes.INDEX(self.screen, 0.37 * self.frame_size_x, 0.27 * self.frame_size_y, 2)
        self.chkbox_plow_duringStorm3 = indexes.INDEX(self.screen, 0.47 * self.frame_size_x, 0.27 * self.frame_size_y, 2)
        self.chkbox_salt_duringStorm = indexes.INDEX(self.screen, 0.62 * self.frame_size_x, 0.27 * self.frame_size_y, 3)

        self.chkbox_plow_afterStorm1 = indexes.INDEX(self.screen, 0.27 * self.frame_size_x, 0.38 * self.frame_size_y, 4)
        self.chkbox_plow_afterStorm2 = indexes.INDEX(self.screen, 0.37 * self.frame_size_x, 0.38 * self.frame_size_y, 4)
        self.chkbox_plow_afterStorm3 = indexes.INDEX(self.screen, 0.47 * self.frame_size_x, 0.38 * self.frame_size_y, 4)

        self.chkbox_salt_afterStorm = indexes.INDEX(self.screen, 0.62 * self.frame_size_x, 0.38 * self.frame_size_y, 5)
        boxes.append(self.chkbox_plow_beforeStorm1)
        boxes.append(self.chkbox_plow_beforeStorm2)
        boxes.append(self.chkbox_plow_beforeStorm3)
        boxes.append(self.chkbox_salt_beforeStorm)

        boxes.append(self.chkbox_plow_duringStorm1)
        boxes.append(self.chkbox_plow_duringStorm2)
        boxes.append(self.chkbox_plow_duringStorm3)
        boxes.append(self.chkbox_salt_duringStorm)

        boxes.append(self.chkbox_plow_afterStorm1)
        boxes.append(self.chkbox_plow_afterStorm2)
        boxes.append(self.chkbox_plow_afterStorm3)
        boxes.append(self.chkbox_salt_afterStorm)

        # Quit_Button
        X_quit = self.frame_size_x * 0.79
        Y_quit = self.frame_size_y * 0.87
        W_quit = 0.16 * self.frame_size_x
        H_quit = 0.05 * self.frame_size_y
        pygame.draw.rect(self.screen, LIGHT_BLUE, (X_quit, Y_quit, W_quit, H_quit))
        quit_B_center = ((X_quit + (W_quit / 2.5)), (Y_quit + (H_quit / 3.5)))
        quit_text_font = text_font.render("Quit", True, BLACK)
        self.screen.blit(quit_text_font, quit_B_center)

        # Vis_Button
        text_font = pygame.font.Font('freesansbold.ttf', 12)

        X_vis = self.frame_size_x * 0.79
        Y_vis = self.frame_size_y * 0.80
        W_vis = 0.16 * self.frame_size_x
        H_vis = 0.05 * self.frame_size_y
        pygame.draw.rect(self.screen, LIGHT_BLUE, (X_vis, Y_vis, W_vis, H_vis))
        vis_B_center = ((X_vis + (W_vis / 4.5)), (Y_vis + (H_vis / 3.5)))
        vis_text_font = text_font.render("Visualization", True, BLACK)
        self.screen.blit(vis_text_font, vis_B_center)

        # Display Data ################################################
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        Temperature_text = smallText.render('Temperature : ', True, DARK_GREEN)
        Temperature_textRect = Temperature_text.get_rect()
        Temperature_textRect.center = (0.77 * self.frame_size_x, 0.07 * self.frame_size_y)
        self.screen.blit(Temperature_text, Temperature_textRect.center)
        # Temperature
        # input temp ##################################################################
        Temperature = smallText.render('23', True, GREEN)
        Temperature_Rect = Temperature.get_rect()
        Temperature_Rect.center = (0.85 * self.frame_size_x, 0.12 * self.frame_size_y)
        self.screen.blit(Temperature, Temperature_Rect.center)

        # Weather_Condition
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        Weather_Condition_text = smallText.render('Weather Condition : ', True, DARK_GREEN)
        Weather_Condition_textRect = Weather_Condition_text.get_rect()
        Weather_Condition_textRect.center = (0.77 * self.frame_size_x, 0.17 * self.frame_size_y)
        self.screen.blit(Weather_Condition_text, Weather_Condition_textRect.center)
        # import Weather Condition####
        self.Weather_Condition_import = 'Snowy'
        Weather_Condition = smallText.render(self.Weather_Condition_import, True, GREEN)
        Weather_Condition_Rect = Weather_Condition.get_rect()
        Weather_Condition_Rect.center = (0.85 * self.frame_size_x, 0.22 * self.frame_size_y)
        self.screen.blit(Weather_Condition, Weather_Condition_Rect.center)

        # Surface_Temperature
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        Surface_Temperature_text = smallText.render('Surface Temperature : ', True, DARK_GREEN)
        Surface_Temperature_textRect = Surface_Temperature_text.get_rect()
        Surface_Temperature_textRect.center = (0.77 * self.frame_size_x, 0.27 * self.frame_size_y)
        self.screen.blit(Surface_Temperature_text, Surface_Temperature_textRect.center)
        # Input Surface Temp
        Surface_Temperature = smallText.render('29', True, GREEN)
        Surface_Temperature_Rect = Surface_Temperature.get_rect()
        Surface_Temperature_Rect.center = (0.85 * self.frame_size_x, 0.32 * self.frame_size_y)
        self.screen.blit(Surface_Temperature, Surface_Temperature_Rect.center)

        # Predicted_Snow_depth_text
        Predicted_Snow_depth_text = smallText.render('Prediceted Snow Depth', True, DARK_GREEN)
        Predicted_Snow_depth_text_Rect = Predicted_Snow_depth_text.get_rect()
        Predicted_Snow_depth_text_Rect.center = (0.77 * self.frame_size_x, 0.37 * self.frame_size_y)
        self.screen.blit(Predicted_Snow_depth_text, Predicted_Snow_depth_text_Rect.center)

        # Predicted_Snow_depth
        Prediceted_Snow_Depth_value = 10
        Predicted_Snow_depth = smallText.render(str(Prediceted_Snow_Depth_value), True, GREEN)
        Predicted_Snow_depth_Rect = Predicted_Snow_depth.get_rect()
        Predicted_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.42 * self.frame_size_y)
        self.screen.blit(Predicted_Snow_depth, Predicted_Snow_depth_Rect.center)

        # Current_Snow_depth
        # Current_Snow_depth_text
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        Current_Snow_depth_text = smallText.render('Current Snow depth', True, DARK_GREEN)
        Current_Snow_depth_text_Rect = Current_Snow_depth_text.get_rect()
        Current_Snow_depth_text_Rect.center = (0.77 * self.frame_size_x, 0.47 * self.frame_size_y)
        self.screen.blit(Current_Snow_depth_text, Current_Snow_depth_text_Rect.center)

        # Current_Snow_depth_value
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        self.Current_Snow_depth = smallText.render(str(self.Snow_depth), True, GREEN)
        self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
        self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
        self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)

        # Reward and punishments
        Reward_text = smallText.render('Reward: ', True, DARK_GREEN)
        Reward_text_Rect = Reward_text.get_rect()
        Reward_text_Rect.center = (0.77 * self.frame_size_x, 0.57 * self.frame_size_y)
        self.screen.blit(Reward_text, Reward_text_Rect.center)

        Punish_text = smallText.render('Punishments: ', True, DARK_GREEN)
        Punish_text_Rect = Punish_text.get_rect()
        Punish_text_Rect.center = (0.77 * self.frame_size_x, 0.63 * self.frame_size_y)
        self.screen.blit(Punish_text, Punish_text_Rect.center)

        Total_score_text = smallText.render('Total Score:', True, RED)
        Total_score_text_Rect = Total_score_text.get_rect()
        Total_score_text_Rect.center = (0.77 * self.frame_size_x, 0.7 * self.frame_size_y)
        self.screen.blit(Total_score_text, Total_score_text_Rect.center)
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                self.chkbox_plow_beforeStorm1.update_checkbox(event)
                self.chkbox_plow_beforeStorm2.update_checkbox(event)
                self.chkbox_plow_beforeStorm3.update_checkbox(event)
                self.chkbox_salt_beforeStorm.update_checkbox(event)

                self.chkbox_plow_duringStorm1.update_checkbox(event)
                self.chkbox_plow_duringStorm2.update_checkbox(event)
                self.chkbox_plow_duringStorm3.update_checkbox(event)
                self.chkbox_salt_duringStorm.update_checkbox(event)

                self.chkbox_plow_afterStorm1.update_checkbox(event)
                self.chkbox_plow_afterStorm2.update_checkbox(event)
                self.chkbox_plow_afterStorm3.update_checkbox(event)
                self.chkbox_salt_afterStorm.update_checkbox(event)

            self.chkbox_plow_beforeStorm1.render_checkbox()
            self.chkbox_plow_beforeStorm2.render_checkbox()
            self.chkbox_plow_beforeStorm3.render_checkbox()
            self.chkbox_salt_beforeStorm.render_checkbox()

            self.chkbox_plow_duringStorm1.render_checkbox()
            self.chkbox_plow_duringStorm2.render_checkbox()
            self.chkbox_plow_duringStorm3.render_checkbox()
            self.chkbox_salt_duringStorm.render_checkbox()

            self.chkbox_plow_afterStorm1.render_checkbox()
            self.chkbox_plow_afterStorm2.render_checkbox()
            self.chkbox_plow_afterStorm3.render_checkbox()
            self.chkbox_salt_afterStorm.render_checkbox()
            pygame.display.update()

            # Click mouse function
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if X_quit + W_quit > mouse[0] > X_quit and Y_quit + H_quit > mouse[1] > Y_quit:
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(X_quit, Y_quit, W_quit, H_quit))
                self.screen.blit(quit_text_font, quit_B_center)
                if click[0] == 1:
                    self.Quit()

            else:
                pygame.draw.rect(self.screen, LIGHT_BLUE, pygame.Rect(X_quit, Y_quit, W_quit, H_quit))
                self.screen.blit(quit_text_font, quit_B_center)

            if X_vis + W_vis > mouse[0] > X_vis and Y_vis + H_vis > mouse[1] > Y_vis:
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(X_vis, Y_vis, W_vis, H_vis))
                self.screen.blit(vis_text_font, vis_B_center)
                if click[0] == 1:
                    self.Visualization()
                    pygame.display.update()
                    time.sleep(1)
                    pygame.display.update()
            else:
                pygame.draw.rect(self.screen, LIGHT_BLUE, pygame.Rect(X_vis, Y_vis, W_vis, H_vis))
                self.screen.blit(vis_text_font, vis_B_center)


        pygame.display.update()
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    def Visualization(self):
        print("Visualization")
        Decision_Box = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        if self.chkbox_plow_beforeStorm1.checked:            Decision_Box[0] = 1
        if self.chkbox_plow_beforeStorm2.checked:            Decision_Box[1] = 1
        if self.chkbox_plow_beforeStorm3.checked:            Decision_Box[2] = 1
        if self.chkbox_salt_beforeStorm.checked:            Decision_Box[3] = 1

        if self.chkbox_plow_duringStorm1.checked:            Decision_Box[4] = 1
        if self.chkbox_plow_duringStorm2.checked:            Decision_Box[5] = 1
        if self.chkbox_plow_duringStorm3.checked:            Decision_Box[6] = 1
        if self.chkbox_salt_duringStorm.checked:            Decision_Box[7] = 1

        if self.chkbox_plow_afterStorm1.checked:            Decision_Box[8] = 1
        if self.chkbox_plow_afterStorm2.checked:            Decision_Box[9] = 1
        if self.chkbox_plow_afterStorm3.checked:            Decision_Box[10] = 1
        if self.chkbox_salt_afterStorm.checked:            Decision_Box[11] = 1
        self.Decion_Box = Decision_Box
        self.Pre_storm_Operations()

    def Pre_storm_Operations(self):
        self.Snow_depth = 0
        print("Pre_storm_Operations")
        print(self.Decion_Box)
        # Pre_storm_Operations:
        image2 = pygame.image.load('No_Clouds_BS.jpg')
        self.screen.blit(image2, (0.05 * self.frame_size_x, 0.50 * self.frame_size_y))
        if self.Decion_Box[0] == 1 or self.Decion_Box[1] == 1 or self.Decion_Box[2] == 1 or self.Decion_Box[3] == 1:
            self.Pre_strom_Num_Plowing_run = self.Decion_Box[0] + self.Decion_Box[1] + self.Decion_Box[2]
            # Pre_plowing (maybe not useful now)
            if self.Pre_strom_Num_Plowing_run >= 1:
                for i in range(0, self.Pre_strom_Num_Plowing_run):
                    Plow_image = pygame.image.load('Plowing.jpg')
                    for i in range(0, 70):
                        self.screen.blit(Plow_image, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67,
                            0.73 * self.frame_size_y))
                        pygame.display.update()
                        time.sleep(Veh_speed)
                        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                         self.X_Right_Snow - self.X_Left_Snow,
                                                                         (self.Y_Down_Snow - self.Y_Up_Snow) + 17), 0)
                    transparent = (0, 0, 0, 0)
                    Plow_image.fill(transparent)

            # Snow removal because of the plowing:
            if self.Pre_strom_Num_Plowing_run == 1: self.Snow_depth = self.Snow_depth*0.3
            if self.Pre_strom_Num_Plowing_run == 2: self.Snow_depth = self.Snow_depth * 0.1
            if self.Pre_strom_Num_Plowing_run == 3: self.Snow_depth = self.Snow_depth * 0.05
            #################################################################################
            # Change the snow depth on the board
            #clear the board:
            self.First_text_point = [0.85 * self.frame_size_x, 0.49 * self.frame_size_y]
            self.Last_text_point = [0.85 * self.frame_size_x, 0.54 * self.frame_size_y]
            pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
            # Change the snow depth
            smallText = pygame.font.SysFont("comicsansms.ttf", 18)
            self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
            self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
            self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
            self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
            pygame.display.flip()

            # Anti-Icing (pre salting)
            if self.Decion_Box[3] == 1:
                Salt_image = pygame.image.load('Salting.jpg')
                salt_label = pygame.image.load('salt_label.jpg')
                for i in range(0, 70):
                    self.screen.blit(Salt_image, (
                        0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67,
                        0.73 * self.frame_size_y + self.Snow_depth))
                    pygame.display.update()
                    time.sleep(Veh_speed)
                    pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                     self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                     (self.Y_Down_Snow - self.Y_Up_Snow) + 17), 0)
                    if i % 10 == 0:
                        self.screen.blit(salt_label, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 39, 0.93 * self.frame_size_y))
                transparent = (0, 0, 0, 0)
                Salt_image.fill(transparent)

                # Snow depth reduction because of the salting
                self.Snow_depth = self.Snow_depth * 0.5
                ## Now the ice on the road should disapear based on the road surface temp, amount of salt and amount of snow
                # Change the snow depth on the board
                # clear the board:
                pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)

        # Car Pass
        Car_image = pygame.image.load('Car.jpg')
        for i in range(0, 100):
            self.screen.blit(Car_image, (
                0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 77,
                0.76 * self.frame_size_y + self.Snow_depth))
            pygame.display.update()
            time.sleep(Veh_speed)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                 self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                 (self.Y_Down_Snow - self.Y_Up_Snow) + 3), 0)

        # Reward and punishment###############################################
        ######################################################################
        ######################################################################
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        self.Punishment_value = self.Decion_Box[0]+self.Decion_Box[1]+self.Decion_Box[2]+self.Decion_Box[3]+self.Decion_Box[4]+self.Decion_Box[5]+self.Decion_Box[6]+self.Decion_Box[7]+self.Decion_Box[8]+self.Decion_Box[9]+self.Decion_Box[10]+self.Decion_Box[11]
        Punishment_val = smallText.render(str(- 0.2*self.Punishment_value)[0:4], True, ORANGE)
        Punishment_val_Rect = Punishment_val.get_rect()
        Punishment_val_Rect.center = (0.85 * self.frame_size_x, 0.66 * self.frame_size_y)
        self.screen.blit(Punishment_val, Punishment_val_Rect.center)
        pygame.display.update()


        self.During_storm_Operations()

    def During_storm_Operations(self):
        print("During_storm_Operations")
        if self.Weather_Condition_import == 'Snowy':
            self.Snow_depth = 10
            self.Max_Speed = 70
            self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
            pygame.display.flip()
        # clear the board:
        self.First_text_point = [0.85 * self.frame_size_x, 0.49 * self.frame_size_y]
        self.Last_text_point = [0.85 * self.frame_size_x, 0.54 * self.frame_size_y]
        pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
        pygame.display.flip()
        # Change the snow depth
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
        self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
        self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
        self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
        pygame.display.flip()

        # Snowing:
        ## Define snowing situation based on the snow type
        # Snowing area
        self.Snow_flakes_positions = []
        image = pygame.image.load('Clouds.jpg')
        self.screen.blit(image, (0.05 * self.frame_size_x, 0.50 * self.frame_size_y))
        for i in range(0, 15):
            Snow_flake_Poistions = []
            self.Y_Snow_flake_Poistion = 0.7 * self.frame_size_y + i * 7
            for snow_flake in range(0, 5):
                self.X_Snow_flake_Poistion = np.random.uniform(low=self.X_Left_Snow, high=self.X_Right_Snow)
                pygame.draw.rect(self.screen, GRAY,
                                 pygame.Rect(self.X_Snow_flake_Poistion, self.Y_Snow_flake_Poistion, 3, 3))
                time.sleep(0.03)
                pygame.display.flip()
                self.Snow_flakes_positions.append((self.X_Snow_flake_Poistion, self.Y_Snow_flake_Poistion))

        # snow line points on the road
        Snow_OnRoad_point01_X = self.Road_first_point01[0]
        Snow_OnRoad_point01_y = self.Road_first_point01[1] - self.Snow_depth
        Snow_OnRoad_point02_X = self.Road_last_point01[0]
        Snow_OnRoad_point02_y = self.Road_last_point01[1] - self.Snow_depth

        self.First_Snow_point = [Snow_OnRoad_point01_X, Snow_OnRoad_point01_y]
        self.Last_Snow_point = [Snow_OnRoad_point02_X, Snow_OnRoad_point02_y]
        print (self.Snow_depth)
        pygame.draw.line(self.screen, GRAY, self.First_Snow_point, self.Last_Snow_point, int(self.Snow_depth))
        pygame.display.update()
        # clear the board:
        self.First_text_point = [0.85 * self.frame_size_x, 0.49 * self.frame_size_y]
        self.Last_text_point = [0.85 * self.frame_size_x, 0.54 * self.frame_size_y]

        # Change the snow depth on the board
        # clear the board:
        pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
        pygame.display.flip()
        # Change the snow depth
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
        self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
        self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
        self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
        pygame.display.flip()



        # Check if we had pre-salting:
        pygame.display.update()
        # time.sleep(5)
        if self.Decion_Box[3] == 1:
            # Snow depth reduction because of the salting
            self.Snow_depth = self.Snow_depth * 0.5
            ## Now the ice on the road should disapear based on the road surface temp, amount of salt and amount of snow
            # Change the snow depth on the board
            # clear the board:
            pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
            # Change the snow depth
            smallText = pygame.font.SysFont("comicsansms.ttf", 18)
            self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
            self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
            self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
            self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
            pygame.display.flip()
        # During_storm_Operations:
        # self.Snow_flakes_positions
        if self.Decion_Box[4] == 1 or self.Decion_Box[5] == 1 or self.Decion_Box[6] == 1 or self.Decion_Box[7] == 1:
            self.During_strom_Num_Plowing_run= self.Decion_Box[4] + self.Decion_Box[5] + self.Decion_Box[6]
            # Plowing_During_storm
            if self.During_strom_Num_Plowing_run>=1:
                for i in range(0, self.During_strom_Num_Plowing_run):
                    Plow_image = pygame.image.load('Plowing.jpg')
                    for i in range(0, 70):
                        self.screen.blit(Plow_image, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67, 0.71 * self.frame_size_y))
                        try:
                            for j in range(0, 100):
                                pygame.draw.rect(self.screen, GRAY,
                                                 pygame.Rect(self.Snow_flakes_positions[j][0],
                                                             self.Snow_flakes_positions[j][1], 3, 3))
                        except:
                            pass
                        pygame.display.update()
                        time.sleep(Veh_speed)
                        try:
                            for j in range(0, 100):
                                pygame.draw.rect(self.screen, WHITE,
                                                 pygame.Rect(self.Snow_flakes_positions[j][0],
                                                             self.Snow_flakes_positions[j][1], 3, 3))
                        except:
                            pass
                        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                         self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                         (self.Y_Down_Snow - self.Y_Up_Snow)), 0)
                    transparent = (0, 0, 0, 0)
                    Plow_image.fill(transparent)
                # Snow removal because of the plowing:
                if self.During_strom_Num_Plowing_run == 1: self.Snow_depth = self.Snow_depth * 0.3
                if self.During_strom_Num_Plowing_run == 2: self.Snow_depth = self.Snow_depth * 0.1
                if self.During_strom_Num_Plowing_run == 3: self.Snow_depth = self.Snow_depth * 0.05
                # Change the snow depth on the board
                # clear the board:
                pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
                # Change the snow depth
                smallText = pygame.font.SysFont("comicsansms.ttf", 18)
                self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
                self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
                self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
                self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
                pygame.display.flip()

            # Salting During storm
            if self.Decion_Box[7] == 1:
                Salt_image = pygame.image.load('Salting.jpg')
                salt_label = pygame.image.load('salt_label.jpg')
                for i in range(0, 70):
                    self.screen.blit(Salt_image, (
                        0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67, 0.72 * self.frame_size_y))
                    try:
                        for j in range(0, 100):
                            pygame.draw.rect(self.screen, GRAY,
                                             pygame.Rect(self.Snow_flakes_positions[j][0],
                                                         self.Snow_flakes_positions[j][1], 3, 3))
                    except:
                        pass
                    pygame.display.update()
                    time.sleep(Veh_speed)
                    try:
                        for j in range(0, 100):
                            pygame.draw.rect(self.screen, WHITE,
                                             pygame.Rect(self.Snow_flakes_positions[j][0],
                                                         self.Snow_flakes_positions[j][1], 3, 3))
                    except:
                        pass
                    pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                     self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                     (self.Y_Down_Snow - self.Y_Up_Snow) + 5), 0)

                    if i % 10 == 0:
                        self.screen.blit(salt_label, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 39, 0.93 * self.frame_size_y))
                transparent = (0, 0, 0, 0)
                Salt_image.fill(transparent)
                pygame.draw.line(self.screen, GRAY, self.First_Snow_point, self.Last_Snow_point, int(self.Snow_depth))
                # Snow depth reduction because of the salting
                self.Snow_depth = self.Snow_depth * 0.5
                # Change the snow depth on the board
                # clear the board:
                pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
                # Change the snow depth
                smallText = pygame.font.SysFont("comicsansms.ttf", 18)
                self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
                self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
                self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
                self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
                pygame.display.flip()

        # Car Pass
        for i in range(0, 100):
            Car_image = pygame.image.load('Car.jpg')
            try:
                for j in range(0, 100):
                    pygame.draw.rect(self.screen, GRAY,
                                     pygame.Rect(self.Snow_flakes_positions[j][0],
                                                 self.Snow_flakes_positions[j][1], 3, 3))
            except:
                pass
            self.screen.blit(Car_image, (
                0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 77,
                0.76 * self.frame_size_y + self.Snow_depth))
            time.sleep(Veh_speed)
            transparent = (0, 0, 0, 0)
            Car_image.fill(transparent)
            pygame.display.update()

        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0.05 * self.frame_size_x, 0.91 * self.frame_size_y,
                                                         0.68 * self.frame_size_x,
                                                         0.95 * self.frame_size_y), 0)

        # Reward and punishment###############################################
        ######################################################################
        ######################################################################
        self.Reward_1 = self.Speed_Snow_function() * 3
        print(self.Speed_Snow_function())
        Reward_Value_1 = smallText.render(str(self.Reward_1)[0:4], True, ORANGE)
        Reward_Value_1_Rect = Reward_Value_1.get_rect()
        Reward_Value_1_Rect.center = (0.85 * self.frame_size_x, 0.60 * self.frame_size_y)
        self.screen.blit(Reward_Value_1, Reward_Value_1_Rect.center)


        # Print Total Score:
        smallText = pygame.font.SysFont("comicsansms.ttf", 22)
        self.Total_Score_Value = self.Reward_1 - self.Punishment_value*0.2
        Total_Score_Value_Text = smallText.render(str(self.Total_Score_Value)[0:4], True, RED)
        Total_Score_Value_Text_Rect = Total_Score_Value_Text.get_rect()
        Total_Score_Value_Text_Rect.center = (0.85 * self.frame_size_x, 0.73 * self.frame_size_y)
        self.screen.blit(Total_Score_Value_Text, Total_Score_Value_Text_Rect.center)
        pygame.display.update()
        self.After_storm_Operations()

    def After_storm_Operations(self):
        print("After_storm_Operations")
        # After_storm_Operations:
        # After storm plowing
        if self.Decion_Box[8] == 1 or self.Decion_Box[9] == 1 or self.Decion_Box[10] == 1 or self.Decion_Box[11] == 1:
            self.After_strom_Num_Plowing_run = self.Decion_Box[8] + self.Decion_Box[9] + self.Decion_Box[10]
            image2 = pygame.image.load('No_Clouds_AS.jpg')
            self.screen.blit(image2, (0.05 * self.frame_size_x, 0.50 * self.frame_size_y))
            # After_storm_plowing
            if self.After_strom_Num_Plowing_run>=1 :
                for i in range(0, self.After_strom_Num_Plowing_run):
                    Plow_image = pygame.image.load('Plowing.jpg')
                    for i in range(0, 70):
                        self.screen.blit(Plow_image, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67, 0.71 * self.frame_size_y))
                        pygame.display.update()
                        time.sleep(Veh_speed)
                        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                         self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                         (self.Y_Down_Snow - self.Y_Up_Snow) ), 0)
            # Snow removal because of the plowing:
            if self.After_strom_Num_Plowing_run == 1: self.Snow_depth = self.Snow_depth * 0.3
            if self.After_strom_Num_Plowing_run == 2: self.Snow_depth = self.Snow_depth * 0.1
            if self.After_strom_Num_Plowing_run == 3: self.Snow_depth = self.Snow_depth * 0.05
            # Change the snow depth on the board
            # clear the board:
            pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
            # Change the snow depth
            smallText = pygame.font.SysFont("comicsansms.ttf", 18)
            self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
            self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
            self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
            self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
            pygame.display.flip()

            # After_storm salting
            if self.Decion_Box[11] == 1:
                Salt_image = pygame.image.load('Salting.jpg')
                salt_label = pygame.image.load('salt_label.jpg')
                for i in range(0, 70):
                    self.screen.blit(Salt_image, (
                        0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 67, 0.72 * self.frame_size_y))
                    pygame.display.update()
                    time.sleep(Veh_speed)
                    pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                                     self.X_Right_Snow - self.X_Left_Snow + 10,
                                                                     (self.Y_Down_Snow - self.Y_Up_Snow)+4), 0)
                    if i % 10 == 0:
                        self.screen.blit(salt_label, (
                            0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 39, 0.93 * self.frame_size_y))
                # transparent = (0, 0, 0, 0)
                # Salt_image.fill(transparent)
                ## Now the ice on the road should disappear based on the road surface temp, amount of salt and amount of snow
                # Snow depth reduction because of the salting
                self.Snow_depth = self.Snow_depth * 0.5
                # Change the snow depth on the board
                # clear the board:
                pygame.draw.line(self.screen, WHITE, self.First_text_point, self.Last_text_point, 50)
                # Change the snow depth
                smallText = pygame.font.SysFont("comicsansms.ttf", 18)
                self.Current_Snow_depth = smallText.render(str(self.Snow_depth)[0:4], True, GREEN)
                self.Current_Snow_depth_Rect = self.Current_Snow_depth.get_rect()
                self.Current_Snow_depth_Rect.center = (0.85 * self.frame_size_x, 0.52 * self.frame_size_y)
                self.screen.blit(self.Current_Snow_depth, self.Current_Snow_depth_Rect.center)
                pygame.display.flip()


        image2 = pygame.image.load('No_Clouds_AS.jpg')
        self.screen.blit(image2, (0.05 * self.frame_size_x, 0.50 * self.frame_size_y))
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                         self.X_Right_Snow - self.X_Left_Snow + 10,
                                                         (self.Y_Down_Snow - self.Y_Up_Snow)), 0)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0.05 * self.frame_size_x, 0.91 * self.frame_size_y,
                                                         0.68 * self.frame_size_x,
                                                         0.95 * self.frame_size_y), 0)
        # Car Pass
        Car_image = pygame.image.load('Car.jpg')
        for i in range(0, 100):
            self.screen.blit(Car_image, (
                0.05 * self.frame_size_x + 0.4 * self.frame_size_x * i / 77,
                0.76 * self.frame_size_y + self.Snow_depth))
            pygame.display.update()
            time.sleep(Veh_speed)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.X_Left_Snow, self.Y_Up_Snow,
                                                         self.X_Right_Snow - self.X_Left_Snow + 10,
                                                         (self.Y_Down_Snow - self.Y_Up_Snow) + 3), 0)
        # Reward and punishment###############################################
        ######################################################################
        ######################################################################
        # Clear the last reward text:
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0.83 * self.frame_size_x, 0.59 * self.frame_size_y,
                                                        0.1 * self.frame_size_x, 0.03 * self.frame_size_y), 0)
        # Print the new reward:
        smallText = pygame.font.SysFont("comicsansms.ttf", 18)
        self.Reward_2 = self.Speed_Snow_function()* 3 + self.Reward_1
        Reward_Value_2 = smallText.render(str(self.Reward_2)[0:4], True, ORANGE)
        Reward_Value_2_Rect = Reward_Value_2.get_rect()
        Reward_Value_2_Rect.center = (0.85 * self.frame_size_x, 0.60 * self.frame_size_y)
        self.screen.blit(Reward_Value_2, Reward_Value_2_Rect.center)

        # Clear the last total reward text:
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0.83 * self.frame_size_x, 0.73 * self.frame_size_y,
                                                         0.1 * self.frame_size_x, 0.03 * self.frame_size_y), 0)
        # Print Total Score:
        smallText = pygame.font.SysFont("comicsansms.ttf", 22)
        self.Total_Score_Value = self.Reward_2 - self.Punishment_value*0.2
        print("self.Total_Score_Value", self.Total_Score_Value)
        print("self.Reward_2", self.Reward_2)
        print("self.Punishment_value", self.Punishment_value)
        Total_Score_Value_Text = smallText.render(str(self.Total_Score_Value)[0:4], True, RED)
        Total_Score_Value_Text_Rect = Total_Score_Value_Text.get_rect()
        Total_Score_Value_Text_Rect.center = (0.85 * self.frame_size_x, 0.73 * self.frame_size_y)
        self.screen.blit(Total_Score_Value_Text, Total_Score_Value_Text_Rect.center)

        pygame.display.update()

    def Quit(self):
        pygame.quit()

    def Speed_Snow_function(self):
        if self.Snow_depth > 6: self.Speed_Index = 0.3
        if self.Snow_depth<=6 and self.Snow_depth>=4: self.Speed_Index = 0.4
        if self.Snow_depth< 4 and self.Snow_depth>=2: self.Speed_Index = 0.6
        if self.Snow_depth < 2 and self.Snow_depth >= 1: self.Speed_Index = 0.8
        if self.Snow_depth < 1: self.Speed_Index = 0.95
        
        return (self.Speed_Index)


M = MDSSEnv()
M.reset()
