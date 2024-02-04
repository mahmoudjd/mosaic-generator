import sys
import argparse
import os.path
from PIL import Image
from pprint import pprint
import PySimpleGUI as sg
from mosaic import MosaicGenerator


def main():
    """
    The above function is the main function of the program.
            It is responsible for the GUI of the program.
            It is responsible for the user's input and the program's output.
            It is responsible for the program's flow.
            It is responsible for the program's logic.
            It is responsible for the program's functionality.
            It is responsible for the program's behavior.
            It is responsible for the program's execution.
            It is responsible for the program's running.
            It is responsible for the program's operation.
            It is responsible for the program's work.
            It is responsible for the program's activity.
            It is responsible for the program's performance.
            It is responsible for the program's action.
            It is responsible for the program's process.
            It is responsible for the program's task.
            It is responsible for the program's job.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_img')
    parser.add_argument('-o', dest='output_img')
    parser.add_argument('-t', dest='tiles_dir')
    parser.add_argument('-x', dest='x', default=15)
    parser.add_argument('-y', dest='y', default=15)
    args = parser.parse_args()

    args.target_img = str(args.input_img)
    args.output_img = str(args.output_img)
    args.tiles_dir = str(args.tiles_dir)
    x = int(str(args.x))
    y = int(str(args.y))
    if len(sys.argv) > 1:
        if not os.path.isfile(args.target_img):
            print('[-] ERROR: Target image not found "{}"'.format(args.target_img))
        elif not os.path.isdir(args.tiles_dir):
            print('[-] ERROR: Tiles directory not found "{}"'.format(args.tiles_dir))
        else:
            mosaic = MosaicGenerator(args.target_img, args.output_img, args.tiles_dir, x, y)
            mosaic.create_Mosaic()

    else:
        pprint(args)
        sg.theme('dark grey 10')

        layout = [
            [sg.Text('Mosaic Generator ', font=("Helvetica", 24), text_color='yellow')],
            [sg.Text('Enter the information, if you wish to make a mosaic image')],
            [sg.Text('Choose the target image to make mosaic like it')],
            [sg.Text('Input', size=(15, 1)),
             sg.In(size=(50, 1), default_text="", enable_events=True,
                   key="target_img"), sg.FileBrowse()],
            [
                sg.Text('Enter the size of tiles (x, y): ', size=(30, 1))
            ],
            [
                sg.Text('x:'),
                sg.In(size=(5, 1), default_text="15", enable_events=True, key='x'),
                sg.Text('y:'),
                sg.In(size=(5, 1), default_text="15", enable_events=True, key='y')
            ],
            [sg.Text('Enter the directory name to extract tiles from it')],
            [sg.Text('Tiles Folder', size=(15, 1)), sg.In(size=(50, 2), default_text='./tiles', key='tiles_dir'),
             sg.FolderBrowse()],
            [sg.Text('Output File', size=(15, 1)), sg.In(size=(50, 2), default_text="mosaic.png", key='output_img')],
            [sg.Text('click on "Run" to start or click on "Close" to close the window')],
            [sg.Button('Run', key="Ok", button_color=('black', 'green')),
             sg.Button('Close', button_color=('black', 'Dark Red'))],

            [sg.Text('Finished', size=(15, 1)),
             sg.ProgressBar(100, orientation='h', bar_color='dark Red', size=(30, 20), key='progress_mosaic')
             ],
            [sg.Text('click on "View Result" to see the result')],
            [sg.Button('View Result', key='Yes')]
        ]

        window = sg.Window('Mosaic Generator', layout)
        view_ready = False
        while True:
            event, values = window.read(timeout=0)
            if event in (None, 'Close'):
                window.close()
                return
            if event == 'Yes' and not view_ready:
                sg.popup_error('Not yet created Mosaic!', font=('Helvetica', 14), text_color='red')

            if event == 'Ok':
                args.target_img = values["target_img"]
                args.tiles_dir = values['tiles_dir']
                args.output_img = str(values['output_img'])
                args.x = str(int(values["x"]))
                args.y = str(int(values["y"]))
                print(args.x, args.y)
                x = int(args.x)
                y = int(args.y)
                print(args.target_img, args.tiles_dir, args.output_img, x, y)

                if args.target_img == '':
                    sg.popup_error('input image was not entered, please enter an image!',
                                   font=('Helvetica', 10), text_color='Red')
                    continue

                mosaic = MosaicGenerator(args.target_img, args.output_img, args.tiles_dir, x, y)
                mosaic.create_Mosaic()

                view_ready = True

                for i in range(100):
                    window["progress_mosaic"].update_bar(i + 1)
                    window.refresh()

            if event == 'Yes' and view_ready:
                show_img(args.output_img)


def show_img(photo):
    """
    `show_img` takes a photo and displays it
    @param photo - the name of the photo you want to display
    """
    print(f'[(^_^)] {photo} is displaying...')
    img = Image.open(photo)
    img.show()


if __name__ == '__main__':
    main()
