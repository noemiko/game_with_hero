from background import Background


class Levels():
    def __init__(self):
        self.background = Background()

    def update(self, display_surface, game_duration: int):

        display_surface.blit(self.background.current,
                             (self.background.x, self.background.y))
        display_surface.blit(self.background.current,
                             (self.background.next_x, self.background.y))

        self.background.update()

        if game_duration == 60:
            self.background.change_image(1)
        elif game_duration == 120:
            self.background.change_image(2)
        elif game_duration == 240:
            self.background.change_image(3)
