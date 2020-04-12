from utils import get_images


class Background():
    def __init__(self):
        self.backgroundImg = get_images("backgrounds")
        self.current = self.backgroundImg[0]
        self.rectBg = self.current.get_rect()
        self.width = self.rectBg.width
        self.x = 0
        self.next_x = self.width
        self.y = 0
        self.dx = -15

    def change_image(self, image_index):

        self.current = self.backgroundImg[image_index]

        self.rectBg = self.current.get_rect()
        self.width = self.rectBg.width

    def update(self, ):
        self.x += self.dx
        if self.x <= -self.width:
            self.x = self.width
        self.next_x += self.dx
        if self.next_x <= -self.width:
            self.next_x = self.width
