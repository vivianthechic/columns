# Vivian Zhang (18217735)
# ICS 32A Project 5
# Game Graphics

import pygame
import p5_mech

class ColumnsGame:
    
    def __init__(self):
        self._running = True
        self._state = p5_mech.GameState(12,6)



    def run(self) -> None:
        pygame.init()
        self._resize_surface((600,600))
        clock = pygame.time.Clock()
        self._draw_field(pygame.display.get_surface())
        count = 0
        while self._running:
            clock.tick(15)
            self._handle_events(count)
            self._redraw()
            count += 1
            if count == 16:
                count = 0
        pygame.quit()



    def _handle_events(self, counter: int) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                try:
                    if event.key == pygame.K_SPACE:
                        self._state.rotate_faller()
                except p5_mech.NoFallerError:
                    pass
                except p5_mech.InvalidMoveError:
                    pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._left()
        if keys[pygame.K_RIGHT]:
            self._right()
        if keys[pygame.K_DOWN]:
            self._down()
        if counter == 0:
            try:
                self._state.tick_time()
            except p5_mech.GameOverError:
                self._display_game_over()
                self._running = False

    def _left(self) -> None:
        try:
            self._state.move_left()
        except p5_mech.NoFallerError:
            pass
        except p5_mech.InvalidMoveError:
            pass


    def _right(self) -> None:
        try:
            self._state.move_right()
        except p5_mech.NoFallerError:
            pass
        except p5_mech.InvalidMoveError:
            pass

    
    def _down(self) -> None:
        try:
            self._state.move_down()
        except p5_mech.NoFallerError:
            pass
        except p5_mech.InvalidMoveError:
            pass

    

    def _redraw(self) -> None:
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(0, 0, 0))
        self._draw_field(surface)
        pygame.display.flip()



    def _display_game_over(self) -> None:
        surface = pygame.display.get_surface()
        width, height = surface.get_size()
        pygame.draw.rect(surface, pygame.Color(200, 100, 0),
                         (0, height/3, width, height/3))
        font = pygame.font.Font(None, width//5)
        text = font.render("GAME OVER", 1, (255, 255, 255))
        surface.blit(text,(width//12, height//2-40))
        pygame.display.flip()
        pause = pygame.time.wait(3000)



    def _draw_field(self, surface: pygame.Surface) -> None:
        contents = self._contents_with_faller()
        width, height = surface.get_size()
        x_coord = 0
        y_coord = 0
        jewel_length = 0
        if height > 2*width:
            x_coord = 0
            y_coord = height/2-width
            jewel_length = width/6
            pygame.draw.rect(surface, pygame.Color(100, 100, 100),
                             (x_coord, y_coord, width, 2*width))
        else:
            x_coord = width/2-height/4
            y_coord = 0
            jewel_length = height/12
            pygame.draw.rect(surface, pygame.Color(100, 100, 100),
                             (x_coord, y_coord, height/2, height))
        temp = x_coord
        for row in range(len(contents)):
            x_coord = temp
            for col in range(len(contents[row])):
                self._draw_jewel(surface, x_coord, y_coord, jewel_length,
                                 contents[row][col])
                x_coord += jewel_length
            y_coord += jewel_length



    def _draw_jewel(self, surface: pygame.Surface, x_coord: int, y_coord: int,
                    jewel_length: int, content: str) -> None:
        r, b, g = (0, 0, 0)
        if content == '   ':
            return
        elif content[1] == 'A':
            r, b, g = (255, 153, 153)
        elif content [1] == 'B':
            r, b, g = (255, 204, 153)
        elif content [1] == 'C':
            r, b, g = (255, 255, 153)
        elif content [1] == 'D':
            r, b, g = (204, 255, 153)
        elif content [1] == 'E':
            r, b, g = (153, 255, 153)
        elif content [1] == 'F':
            r, b, g = (153, 255, 255)
        elif content [1] == 'G':
            r, b, g = (153, 204, 255)
        elif content [1] == 'H':
            r, b, g = (153, 153, 255)
        elif content [1] == 'I':
            r, b, g = (204, 153, 255)
        elif content [1] == 'J':
            r, b, g = (255, 153, 255)
        if content[0] == '|':
            r -= 40
            b -= 40
            g -= 40
        elif content[0] == '*':
            if pygame.time.get_ticks()%2 == 0:
                r, b, g = (255, 255, 255)
        pygame.draw.rect(surface, pygame.Color(r, b, g),
                         (x_coord, y_coord, jewel_length, jewel_length))



    def _contents_with_faller(self) -> [list]:
        if self._state.get_faller() == None:
            return self._state.contents()
        else:
            game_state = self._state
            faller = self._state.get_faller()
            temp_field = []
            for content in range(len(game_state.contents())):
                temp = []
                for cont in range(len(game_state.contents()[content])):
                    temp.append(game_state.contents()[content][cont])
                temp_field.append(temp)
            for jewel in range(len(faller)):
                r = faller[jewel][1]
                c = faller[jewel][2]
                if r >= 0:
                    temp_field[r][c] = faller[jewel][0]
            return temp_field
        


    def _resize_surface(self, size: (int, int)) -> None:
        width, height = size
        if width < 300:
            width = 300
        if height < 300:
            height = 300
        pygame.display.set_mode((width, height), pygame.RESIZABLE)
        


if __name__ == '__main__':
    ColumnsGame().run()
