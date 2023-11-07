import pygame
import random
import math


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("static/slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def choose_direction(self, player, method):
        if self.rect.top == player.rect.top and self.rect.bottom == player.rect.bottom:
            if self.rect.left - player.rect.left > self.rect.left - player.rect.right:
                return "right"
            return "left"
        elif self.rect.left == player.rect.left and self.rect.right == player.rect.right:
            if self.rect.top - player.rect.top > self.rect.top - player.rect.bottom:
                return "down"
            return "up"

        if method == "greedy":
            left_, right_, top_, down_ = self.choose_direction_with_greedy_method(player)
        else:
            left_, right_, top_, down_ = self.choose_direction_with_astar_method(player)

        min_value = min(left_, right_, top_, down_)

        if min_value == left_:
            return "right"
        elif min_value == right_:
            return "left"
        elif min_value == top_:
            return "down"
        else:
            return "up"

    def choose_direction_with_astar_method(self, player):

        left_ = abs(player.rect.left - self.rect.left) + min(
            abs(self.rect.top - player.rect.top),
            abs(self.rect.bottom - player.rect.bottom),
        )
        right_ = abs(player.rect.right - self.rect.right) + min(
            abs(self.rect.top - player.rect.top),
            abs(self.rect.bottom - player.rect.bottom),
        )
        top_ = abs(player.rect.top - self.rect.top) + min(
            abs(self.rect.left - player.rect.left),
            abs(self.rect.right - player.rect.right),
        )
        down_ = abs(player.rect.bottom - self.rect.bottom) + min(
            abs(self.rect.left - player.rect.left),
            abs(self.rect.right - player.rect.right),
        )

        return left_, right_, top_, down_

    def choose_direction_with_greedy_method(self, player):

        left_ = min(
            math.sqrt((self.rect.top - player.rect.top) ** 2 + (self.rect.left - 1 - player.rect.left) ** 2),
            math.sqrt((self.rect.bottom - player.rect.bottom) ** 2 + (self.rect.left - 1 - player.rect.left) ** 2)
        )
        right_ = min(
            math.sqrt((self.rect.top - player.rect.top) ** 2 + (self.rect.left + 1 - player.rect.left) ** 2),
            math.sqrt((self.rect.bottom - player.rect.bottom) ** 2 + (self.rect.left + 1 - player.rect.left) ** 2)
        )
        top_ = min(
            math.sqrt((self.rect.top - 1 - player.rect.top) ** 2 + (self.rect.left - player.rect.left) ** 2),
            math.sqrt((self.rect.top - 1 - player.rect.top) ** 2 + (self.rect.right - player.rect.right) ** 2)
        )
        down_ = min(
            math.sqrt((self.rect.top + 1 - player.rect.top) ** 2 + (self.rect.left - player.rect.left) ** 2),
            math.sqrt((self.rect.top + 1 - player.rect.top) ** 2 + (self.rect.right - player.rect.right) ** 2)
        )

        return left_, right_, top_, down_

    def update(self, horizontal_blocks, vertical_blocks, player):
        """
        This method is implemented with the Astar algorithm
        """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = 800
        elif self.rect.left > 800:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = 576
        elif self.rect.top > 576:
            self.rect.bottom = 0

        if self.rect.topleft in self.get_intersection_position():
            # direction = self.choose_direction(player, "greedy")
            direction = self.choose_direction(player, "astar")
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 3:
                    items.append((j * 32, i * 32))

        return items


def enviroment():
    grid = (
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
    )

    return grid


def draw_enviroment(screen):
    for i, row in enumerate(enviroment()):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(
                    screen, (0, 0, 255), [j * 32, i * 32], [j * 32 + 32, i * 32], 3
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    [j * 32, i * 32 + 32],
                    [j * 32 + 32, i * 32 + 32],
                    3,
                )
            elif item == 2:
                pygame.draw.line(
                    screen, (0, 0, 255), [j * 32, i * 32], [j * 32, i * 32 + 32], 3
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    [j * 32 + 32, i * 32],
                    [j * 32 + 32, i * 32 + 32],
                    3,
                )
