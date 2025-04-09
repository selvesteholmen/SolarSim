import pygame
import tkinter as tk
from planet import Planet
from editor import Controller

class SolarSystemSimulation:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Solar System Simulation')
        self.BLACK = (0, 0, 0)

        self.sun = Planet(0, 0, 30, (255, 255, 0), 1.98892e30, "Sun")
        self.sun.sun = True

        self.earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742e24, "Earth")
        self.earth.y_vel = 29.783 * 1000

        self.mars = Planet(-1.1 * Planet.AU, 0, 10, (240, 0, 0), 5.9742e23, "Mars")
        self.mars.y_vel = (30.000 * 1000)

        self.planets = [self.sun, self.earth, self.mars]

        self.root = tk.Tk()
        self.controller = Controller(self.root, self)

    def update(self):
        for planet in self.planets:
            planet.update_position(self.planets)

    def draw(self):
        self.screen.fill(self.BLACK)
        for planet in self.planets:
            planet.draw(self.screen)
        pygame.display.update()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.controller.simulation_running:
                self.update()
                self.draw()

            self.root.update_idletasks()
            self.root.update()

        pygame.quit()

if __name__ == "__main__":
    simulation = SolarSystemSimulation()
    simulation.run()
