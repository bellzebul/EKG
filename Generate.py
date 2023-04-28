import sys
from subprocess import Popen, PIPE

from kivy.core.window import Window
from kivymd.app import MDApp
from get_graph_params import update_generated_plot_params
from kivy.lang import Builder
from graph_generator import GraphGenerator
import kivy_matplotlib_widget

Window.size = (1100, 420)


class Master_2023(MDApp):
    lines = []
    current_idx = 0

    def build(self):
        self.screen = Builder.load_file('Generate.kv')
        with open('theme.txt', 'r') as file:
            if file.read() == 'Dark':
                self.theme_cls.theme_style = "Dark"
            elif file.read() == 'Light':
                self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return self.screen

    def on_start(self, *args):
        self.alt_val = 0.5
        self.noise_lvl = 0.0
        self.current_params = eval(sys.argv[1])
        # self.current_params = {'P': [0.11, 0.016, 0.008, 0.399],
        #                        'Q': [-0.15, 0.01, 0.002, 0.45],
        #                        'R': [1.15, 0.008, 0.007, 0.474],
        #                        'S': [-0.29, 0.006, 0.017, 0.495],
        #                        'ST': [0.025, 0.012, 0.0, 0.574],
        #                        'T': [0.25, 0.062, 0.072, 0.7]}
        self.n = 10
        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl)

        t, x, self.current_params = update_generated_plot_params(self.current_params, self.n)

        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

        self.screen.alter_lvl.bind(value=self.update_alt)
        self.screen.noise_lvl.bind(value=self.update_noise)

    def smoothing(self):
        process = Popen(
            ['python3', '/Users/bellzebull/Documents/КПИ/4й сем/AI/KP3/kivy_app/Smoothing.py',
             str(self.current_params), str(self.alt_val), str(self.noise_lvl)], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        # Печать вывода из stdout и stderr
        print(output.decode())
        print(error.decode())

    def change_amount(self, wid, val):
        cur_amount = int(self.screen.amount.text)
        if wid == 'right':
            self.n = cur_amount + int(val)
            self.screen.amount.text = str(self.n)

        if wid == 'left':
            if cur_amount > 1:
                self.n = cur_amount + int(val)
                self.screen.amount.text = str(self.n)

        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl)

        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

    def update_noise(self, instance, val):
        self.noise_lvl = val
        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl)
        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

    def update_alt(self, instance, val):
        self.alt_val = val
        self.mygraph = GraphGenerator(self.current_params, self.n, val, self.noise_lvl)
        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)


Master_2023().run()
