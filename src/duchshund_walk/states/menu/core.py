import pygame as pg
from duchshund_walk.settings import BLACK
from duchshund_walk.settings import BLUE
from duchshund_walk.settings import WHITE


class MenuCore:
    def __init__(self):
        self.selected_index = 0
        self.last_option = None
        self.selected_color = BLUE
        self.deselected_color = BLACK
        self.selected_size = 70
        self.deselected_size = 50

    def draw_menu(self, screen):
        """handle drawing of the menu options"""
        for i, opt in enumerate(self.rendered["deselected"]):
            opt[1].center = (
                self.screen_rect.centerx,
                self.from_bottom + i * self.spacer,
            )
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered["selected"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])

    def update_menu(self):
        self.change_selected_option()

    def get_event_menu(self, event):
        if event.type == pg.KEYDOWN:
            # select new index
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)

    def mouse_menu_click(self, event):
        """select menu option """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i, opt in enumerate(self.rendered["deselected"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break

    def pre_render_options(self):
        """setup render menu options based on selected or deselected"""
        font_deselect = pg.font.SysFont("arial", self.deselected_size)
        font_selected = pg.font.SysFont("arial", self.selected_size)

        rendered_msg = {"deselected": [], "selected": []}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, self.deselected_color)
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, self.selected_color)
            s_rect = s_rend.get_rect()
            rendered_msg["deselected"].append((d_rend, d_rect))
            rendered_msg["selected"].append((s_rend, s_rect))
        self.rendered = rendered_msg

    def select_option(self, i):
        """select menu option via keys or mouse"""
        if i == len(self.states_names_options):
            self.quit = True
        else:
            self.next = self.states_names_options[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, option_index_change=0):
        """
        Change highlighted menu option
        :param index_change: user might
         select lower or upper option if use arrows to change options
        possible values -1 , 0, 1

        """
        for i, opt in enumerate(self.rendered["deselected"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i
        if option_index_change:
            self.selected_index += option_index_change
            max_ind = len(self.rendered["deselected"]) - 1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0

    def draw(self, screen):
        screen.fill(WHITE)
        self.draw_menu(screen)
