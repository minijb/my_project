import sys
import pygame

from setting import settings


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings  = settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #每次循环时都重新绘制屏幕
            #fill用这种背景色填充屏幕
            self.screen.fill(self.settings.bg_color)
            #最近绘制的屏幕可见
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()