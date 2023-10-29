import pygame
from Classes import *
from sys import exit
from tkinter import filedialog, Tk
import tkinter as tk
import pandas as pd
import numpy as np

width, height = 1920,1080
fps = 60
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Title")
clock = pygame.time.Clock()
running = True

#BUTTONS
buttons = []
get_file = Button('get_file', 'Open File', (width-200,height-100))
get_file.filepath = '/home/user/testpad/python/pygame/pandas/WeatherMapper/data/USW00024157.csv'
buttons.append(get_file)
make_chart = Button('make_chart', 'Make Chart', (width-200,height-200))
buttons.append(make_chart)

column_buttons = []

font = pygame.font.Font(None, 50)
hover_text = font.render('', False, '#000000', '#EEEEEE')
hover_rect = hover_text.get_rect(topleft = (0,0))

clicked = (False,False,False)
filepath = ''
file = None
chart_surf = pygame.image.load("output/temp.png").convert()
chart_rect = chart_surf.get_rect(center = (width//2,height//2))

# Boxes for dropping the `active_param` into
x_box = pygame.Rect(chart_rect.left, chart_rect.bottom - (int(chart_rect.height * 0.2)), chart_rect.width, int(chart_rect.height * 0.2))
y_box = pygame.Rect(chart_rect.topleft, (int(chart_rect.width * 0.2), chart_rect.height))
val_box = pygame.Rect(chart_rect.right - (int(chart_rect.width * 0.2)), chart_rect.top, (int(chart_rect.width * 0.2)), chart_rect.height)
param_box = pygame.Rect(0,0,int(width * .2), height)

active_param = None

chart_values = ['heatmap', get_file.filepath, None, None, None]

while running:
# GET EVENTS
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_o:
                    temp = Tk()
                    get_file.filepath = filedialog.askopenfilename()
                    temp.destroy()

        if event.type == pygame.MOUSEWHEEL:
            if param_box.collidepoint(pos):
                for button in column_buttons:
                    button.rect.bottom += event.y * 42
                    button.start_point = (button.start_point[0], button.start_point[1] + event.y * 42)
            print(event)

        # Mouse Motion
        if event.type == pygame.MOUSEMOTION:
            if clicked[0]:
                if active_param:
                    active_param.rect = active_param.text.get_rect(center = pos)
                # BUTTONS
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        button.is_clicked = True
                    else:
                        button.is_clicked = False
                    button.update()
                # PARAMS
                for button in column_buttons:
                    if button.rect.collidepoint(pos):
                        button.is_clicked = True
                    else:
                        button.is_clicked = False
                    button.update()
            # Check for hover text
            for button in column_buttons:
                if button.rect.collidepoint(pos):
                    if not button.is_clicked:
                        hover_text = font.render(button.head, False, '#000000', '#EEEEEE')
                        hover_rect = hover_text.get_rect(topleft = pos)
                    else: hover_rect = hover_text.get_rect(bottomright = (-1,-1))
                    break
                else: hover_rect = hover_text.get_rect(bottomright = (-1,-1))

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button != 5 and event.button != 4:
            # BUTTONS
            for button in buttons:
                if button.rect.collidepoint(pos):
                    button.is_clicked = True
                else:
                    button.is_clicked = False
                button.update()
            # PARAMS
            for button in column_buttons:
                if button.rect.collidepoint(pos):
                    active_param = button
                    active_param.rect = active_param.text.get_rect(center = pos)
                    button.is_clicked = True
                else:
                    button.is_clicked = False
                button.update()
            clicked = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONUP and event.button != 5 and event.button != 4:
            print(event)
            for button in buttons:
                if button.is_clicked:
                    if button.btype == 'get_file':
                        button.set_filepath()
                    elif button.btype == 'make_chart' and not any(item is None for item in chart_values):
                        chart = Chart(*chart_values)
                        chart_surf = pygame.image.load(chart.make_chart()).convert()

                button.is_clicked = False
                button.update()
            for button in column_buttons:
                if button.is_clicked:
                    if button.rect.colliderect(x_box):
                        chart_values[2] = button.string
                    elif button.rect.colliderect(y_box):
                        chart_values[3] = button.string
                    elif button.rect.colliderect(val_box):
                        chart_values[4] = button.string
                    print(chart_values)

                button.is_clicked = False
                button.update()
            if active_param:
                active_param.rect = active_param.text.get_rect(topleft = active_param.start_point)
                active_param = None
            clicked = (False,False,False)
# EVENTS OVER

    if get_file.filepath != filepath:
        print(get_file.filepath[-3:])
        column_buttons = []
        if get_file.filepath[-3:] == 'csv':
            print(get_file.filepath)
            file = pd.read_csv(get_file.filepath, low_memory=False)
            counter = 1
            for i in file.columns:
                text = ''
                for j in np.append(pd.unique(file[i])[:5], '...'):
                    text += str(j) + '\n'
                column_buttons.append(Button('param', i, (0 ,counter*38), text))
                counter += 1
        filepath = get_file.filepath
        chart_values[1] = get_file.filepath

    screen.fill((255,255,255))

    screen.blit(chart_surf, chart_rect)
    for button in buttons:
        screen.blit(button.text, button.rect)
    for button in column_buttons:
        screen.blit(button.text, button.rect)
    screen.blit(hover_text, hover_rect)
#    pygame.draw.rect(screen, 'Orange', x_box)
#    pygame.draw.rect(screen, 'Blue', y_box)
#    pygame.draw.rect(screen, 'Green', val_box)
    if active_param:
        screen.blit(active_param.text, active_param.rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
