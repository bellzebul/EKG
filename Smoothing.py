import sys

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
        self.screen = Builder.load_file('Smoothing.kv')
        with open('theme.txt', 'r') as file:
            if file.read() == 'Dark':
                self.theme_cls.theme_style = "Dark"
            elif file.read() == 'Light':
                self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return self.screen

    def on_start(self, *args):
        self.current_params, self.alt_val,  self.noise_lvl = eval(sys.argv[1]), eval(sys.argv[2]), eval(sys.argv[3])
        # self.alt_val = 0.5
        # self.noise_lvl = 0.0
        self.alpha_lvl = 0
        self.width = 0
        # self.current_params = eval(sys.argv[1])
        # self.current_params = {'P': [0.11, 0.016, 0.008, 0.399],
        #                        'Q': [-0.15, 0.01, 0.002, 0.45],
        #                        'R': [1.15, 0.008, 0.007, 0.474],
        #                        'S': [-0.29, 0.006, 0.017, 0.495],
        #                        'ST': [0.025, 0.012, 0.0, 0.574],
        #                        'T': [0.25, 0.062, 0.072, 0.7]}
        self.n = 10
        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl)

        t, x, self.current_params = \
            update_generated_plot_params(self.current_params, self.n, self.alt_val, self.noise_lvl)

        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

        self.screen.alpha.bind(value=self.exp_filter)
        self.screen.w_width.bind(value=self.width_filter)


    def width_filter(self, instance, val):
        self.width = val
        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl, None, self.width)
        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

    def exp_filter(self, instance, val):
        self.alpha_lvl = val
        self.mygraph = GraphGenerator(self.current_params, self.n, self.alt_val, self.noise_lvl, self.alpha_lvl)
        self.screen.figure_wgt.figure = self.mygraph.fig
        self.screen.figure_wgt.axes = self.mygraph.ax1
        self.screen.figure_wgt.xmin = self.mygraph.xmin
        self.screen.figure_wgt.xmax = self.mygraph.xmax
        self.screen.figure_wgt.ymin = self.mygraph.ymin
        self.screen.figure_wgt.ymax = self.mygraph.ymax
        self.screen.figure_wgt.fast_draw = False
        self.lines.append(self.mygraph.line1)

    def filter(self, val):
        if val == 'Exponential':
            self.screen.w_width.disabled = True
            self.screen.alpha.disabled = False
        elif val == 'Average':
            self.screen.alpha.disabled = True
            self.screen.w_width.disabled = False


Master_2023().run()
