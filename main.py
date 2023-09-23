from tkinter import Tk, ttk
from tkinter.messagebox import showerror

from powershall_commands import get_apps, run_powershell, delete_temp


class MyButton(ttk.Button):
    def __init__(self, master, number_of_button, *args, **kwargs, ) -> None:
        super().__init__(master, *args, **kwargs)
        self.number_of_button = number_of_button

    def __repr__(self) -> str:
        return f'Кнопка {self.number_of_button}'


class MainWindow:
    window = Tk()
    BUTTONS_ON_SCREEN = 10

    def __init__(self) -> None:
        self.apps = get_apps()

    def create_window(self):
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)
        # self.window.geometry(MainWindow.WINDOW_SIZE)
        self.window.title('Removing pre-installed applications')

    def create_main_label(self, text=None):
        self.label = ttk.Label(MainWindow.window,
                               width='40',
                               anchor='center',
                               justify='center',
                               wraplength=250)
        self.label.grid(row=0, column=0, columnspan=2)

    def create_frame_for_buttons(self):
        self.frame_for_btns = ttk.Frame(MainWindow.window,
                                        height=250,
                                        width=300)
        self.frame_for_btns.grid(row=1,
                                 column=0,
                                 columnspan=2,
                                 sticky='nsew',
                                 padx=10)
        self.frame_for_btns.pack_propagate(False)

    def init_buttons(self):
        self.buttons = []
        for i in range(0, len(self.apps)):
            self.buttons.append(
                MyButton(self.frame_for_btns,
                         text=f'{self.apps[i]}',
                         number_of_button=i,
                         command=lambda arg=i: self.click_btn(arg))
            )

    def click_btn(self, btn_num):
        err_message = ('An error has occurred. Restart the application \
                       and look at the list of standard applications')
        style = ttk.Style()
        style.map("OFF_btn.TButton", foreground=[('disabled', "red")])
        self.buttons[btn_num]['state'] = 'disabled'
        self.buttons[btn_num].configure(style='OFF_btn.TButton')
        result = run_powershell(self.buttons[btn_num]['text'])
        if result is not True:
            self.label['text'] = 'An error has occurred.'
            self.label['backgroun'] = 'red'
            showerror(title="Ошибка", message=err_message)
        else:
            self.label['text'] = 'All done!'
            self.label['backgroun'] = '#8cfac1'

    def create_app_buttons(self, position=0):
        if len(self.buttons) > 10:
            if position == 0:
                for i in range(10):
                    self.buttons[i].pack(fill='both')
            elif len(self.buttons) - position*10 >= 10:
                num = 0
                for i in range(position*10, position*10 + 10):
                    self.buttons[i].pack(fill='both')
                    num += 1
            else:
                num = 0
                for i in range(position*10, len(self.buttons)):
                    self.buttons[i].pack(fill='both')
                    num += 1
        else:
            num = 0
            for btn in self.buttons:
                btn.grid(row=num, column=0, columnspan=2, stick='nswe')
                num += 1

    def create_flipping_btns_widget(self):
        self.position = 0
        self.previous = ttk.Button(MainWindow.window,
                                   text='<<<',
                                   state=['disabled'],
                                   command=lambda: self.next_frame(-1))
        self.next = ttk.Button(MainWindow.window, text='>>>',
                               command=lambda: self.next_frame(1))
        self.previous.grid(row=2, column=0)
        self.next.grid(row=2, column=1)

    def next_frame(self, flip):
        if self.position == 0 and flip == -1:
            self.previous['state'] = 'disabled'
        elif (self.position == int(len(self.buttons) /
              MainWindow.BUTTONS_ON_SCREEN) and flip == 1):
            self.next['state'] = 'disabled'
        else:
            self.previous['state'] = 'anabled'
            self.next['state'] = 'anabled'
            self.position += flip
            for button in self.frame_for_btns.winfo_children():
                button.pack_forget()
            self.create_app_buttons(self.position)

    def start(self):
        self.create_window()
        self.create_main_label()
        self.create_frame_for_buttons()
        self.init_buttons()
        self.create_app_buttons(0)
        self.create_flipping_btns_widget()
        MainWindow.window.protocol(
            "WM_DELETE_WINDOW",
            lambda: (MainWindow.window.destroy(), delete_temp())
        )
        MainWindow.window.mainloop()


a = MainWindow()
a.start()
