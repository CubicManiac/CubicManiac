# -----------------------------------------------------------------
# Sorting Algorithm Visualizer
#
# File: main.py
#
# Author: Siddharth Chhatbar
# -----------------------------------------------------------------
import pygame
import random, math

pygame.init()

class DrawInformation:
	# colors
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BLUE = 0, 0, 255
	LIGHT_GREY = 160, 160, 160
	GREY = 128, 128, 128
	DARK_GREY = 192, 192, 192
	BACKGROUND_COLOR = WHITE

	FONT = pygame.font.SysFont('times new roman', 25)
	LARGE_FONT = pygame.font.SysFont('times new roman', 35)

	# bar color
	GRADIENT = [LIGHT_GREY, GREY, DARK_GREY]

	# padding
	SIDE_PADDING = 100
	TOP_PADDING = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualizer")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_value = min(lst)
		self.max_value = max(lst)

		self.block_width = math.floor((self.width - self.SIDE_PADDING) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PADDING)/ (self.max_value - self.min_value))
		self.start_x = self.SIDE_PADDING // 2

def generate_starting_list(n, min_value, max_value):
	lst = []

	for i in range(n):
		val = random.randint(min_value, max_value)
		lst.append(val)

	return lst

def draw(draw_info, algorithm_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algorithm_name}  - {'Ascending' if ascending else 'Decending'}", 1, draw_info.BLUE)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 40))
	
	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 70))
	
	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)

		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_value) * draw_info.block_height
		
		color = draw_info.GRADIENT[i % 3]
		
		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst 

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i: draw_info.RED, i - 1: draw_info.GREEN}, True)
			yield True

	return lst

def main():
	run = True
	sorting = False
	ascending = True

	n = 50
	min_value = 0
	max_value = 100

	
	lst = generate_starting_list(n, min_value, max_value)
	clock = pygame.time.Clock()
	draw_info = DrawInformation(800, 600, lst)

	sorting_algorithm = bubble_sort
	algorithm_name = "Bubble Sort"
	algorithm_generator = None
	
	while run:
		clock.tick(60)

		if sorting:
			try:
				next(algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, algorithm_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_value, max_value)
				draw_info.set_list(lst)
				sorting = False

			elif event.key == pygame.K_SPACE and not sorting:
				sorting = True
				algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			
			elif event.key == pygame.K_d and not sorting:
				ascending = False

			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				algorithm_name = "Insertion Sort"

			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				algorithm_name = "Bubble Sort"

	pygame.quit()

if __name__ == '__main__':
    main()