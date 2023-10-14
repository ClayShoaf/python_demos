import PySimpleGUI as sg
import images.data as dice
import random

d6 = [dice.D6_FACE_1, dice.D6_FACE_2, dice.D6_FACE_3, dice.D6_FACE_4, dice.D6_FACE_6, dice.D6_FACE_6]

def main():
    layout = [
              [sg.Image(d6[-1], key='-DIE-1-'), sg.Image(d6[-1], key='-DIE-2-')],
              #[sg.Image(dice.D6_ANIMATION, key='-DIE-1-'), sg.Image(dice.D6_ANIMATION, key='-DIE-2-')],
              [sg.Button('Roll \'em', key='-ROLL-BUTTON-', border_width=0, pad=10, metadata=False)]
             ]

    window = sg.Window('Dice Roller', layout, element_justification='center')

    roll = 0
    while True:  # Event Loop
        event, values = window.read(timeout=10)
        if roll > 0:
            window['-DIE-1-'].update_animation(dice.D6_ANIMATION,  time_between_frames=10)
            window['-DIE-2-'].update_animation(dice.D6_ANIMATION,  time_between_frames=10)
            if roll == 1:
                window['-DIE-1-'].update(source=d6[random.randint(0,len(d6)-1)])
                window['-DIE-2-'].update(source=d6[random.randint(0,len(d6)-1)])
            roll -= 1
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == '-ROLL-BUTTON-':  # if the roll button is clicked
            window['-DIE-1-'].update(source=dice.D6_ANIMATION)
            window['-DIE-2-'].update(source=dice.D6_ANIMATION)
            roll = 100
            


    window.close()


if __name__ == '__main__':

    main()
