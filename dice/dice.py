import PySimpleGUI as sg
import images.data as dice
import random

d6 = [dice.D6_FACE_1, dice.D6_FACE_2, dice.D6_FACE_3, dice.D6_FACE_4, dice.D6_FACE_6, dice.D6_FACE_6]

def main():
    layout = [
              [sg.Image(d6[-1], key='-DIE-1-'), sg.Image(d6[-1], key='-DIE-2-')],
              [sg.Button('Roll \'em', key='-ROLL-BUTTON-', border_width=0, pad=10, metadata=False)],
              [sg.Text('test')]
             ]

    window = sg.Window('Dice Roller', layout, element_justification='center')

    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == '-ROLL-BUTTON-':  
            new_element = [sg.Text('New Text Element')]
            layout.append(new_element)
            window.Layout(layout)
            window['-DIE-1-'].update(source=dice.D6_ANIMATION)
            window['-DIE-2-'].update(source=dice.D6_ANIMATION)
            for _ in range(100):
                window['-DIE-1-'].update_animation(dice.D6_ANIMATION,  time_between_frames=10)
                window['-DIE-2-'].update_animation(dice.D6_ANIMATION,  time_between_frames=10)
                window.read(timeout=10)
            window['-DIE-1-'].update(source=d6[random.randint(0,len(d6)-1)])
            window['-DIE-2-'].update(source=d6[random.randint(0,len(d6)-1)])


            


    window.close()


if __name__ == '__main__':

    main()
