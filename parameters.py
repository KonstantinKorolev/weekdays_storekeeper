import pygame

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))

usr_width = 91
usr_height = 120
usr_x = display_width // 2.3
usr_y = display_height - usr_height

sale_width = 100
sale_height = 100

sale_x = 700
sale_y = display_height - sale_height

clock = pygame.time.Clock()
