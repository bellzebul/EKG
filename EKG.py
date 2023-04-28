import os.path
from subprocess import Popen, PIPE
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivy_garden.graph import Graph, LinePlot
from get_graph_params import update_plot_params
import random
import cv2


class Container(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prev_val = 0
        graph_theme = {
            'label_options': {'color': [0, 0, 0, 1],
                              'bold': False},
            'background_color': [1, 1, 1, 0.9],
            'border_color': [0, 0, 0, 1],
            'tick_color': [0, 0, 0, 0.5]

        }
        self.graph_p = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                             x_grid=True, y_grid=True,
                             draw_border=True,
                             x_grid_label=True, y_grid_label=True,
                             y_ticks_major=0.25, x_ticks_major=0.1,
                             xlabel="S", ylabel="mV", font_size=20,
                             **graph_theme)
        self.ids.graph_p.add_widget(self.graph_p)

        self.graph_q = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                             x_grid=True, y_grid=True,
                             draw_border=True,
                             x_grid_label=True, y_grid_label=True,
                             y_ticks_major=0.25, x_ticks_major=0.1,
                             xlabel="S", ylabel="mV", font_size=20,
                             **graph_theme)
        self.ids.graph_q.add_widget(self.graph_q)

        self.graph_r = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                             x_grid=True, y_grid=True,
                             draw_border=True,
                             x_grid_label=True, y_grid_label=True,
                             y_ticks_major=0.25, x_ticks_major=0.1,
                             xlabel="S", ylabel="mV", font_size=20,
                             **graph_theme)
        self.ids.graph_r.add_widget(self.graph_r)

        self.graph_s = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                             x_grid=True, y_grid=True,
                             draw_border=True,
                             x_grid_label=True, y_grid_label=True,
                             y_ticks_major=0.25, x_ticks_major=0.1,
                             xlabel="S", ylabel="mV", font_size=20,
                             **graph_theme)
        self.ids.graph_s.add_widget(self.graph_s)

        self.graph_st = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                              x_grid=True, y_grid=True,
                              draw_border=True,
                              x_grid_label=True, y_grid_label=True,
                              y_ticks_major=0.25, x_ticks_major=0.1,
                              xlabel="S", ylabel="mV", font_size=20,
                              **graph_theme)
        self.ids.graph_st.add_widget(self.graph_st)

        self.graph_t = Graph(xmin=0, xmax=1, ymin=-1, ymax=1.5,
                             x_grid=True, y_grid=True,
                             draw_border=True,
                             x_grid_label=True, y_grid_label=True,
                             y_ticks_major=0.25, x_ticks_major=0.1,
                             xlabel="S", ylabel="mV", font_size=20,
                             **graph_theme)
        self.ids.graph_t.add_widget(self.graph_t)

        self.plot_p = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)
        self.plot_q = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)
        self.plot_r = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)
        self.plot_s = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)
        self.plot_st = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)
        self.plot_t = LinePlot(color=[1, 0, 0.2, 0.7], line_width=1.5)

        t, x, self.current_params = update_plot_params()

        self.plot_p.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_q.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_r.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_s.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_st.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_t.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]

        self.graph_p.add_plot(self.plot_p)
        self.graph_q.add_plot(self.plot_q)
        self.graph_r.add_plot(self.plot_r)
        self.graph_s.add_plot(self.plot_s)
        self.graph_st.add_plot(self.plot_st)
        self.graph_t.add_plot(self.plot_t)

    def update_plot(self, current_pick, current_param, value, mode=0):
        if mode == 1:
            t, x, self.current_params = update_plot_params(current_pick, current_param, value, None)
        else:
            t, x, self.current_params = update_plot_params(current_pick, current_param, value, self.current_params)
        self.plot_p.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_q.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_r.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_s.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_st.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]
        self.plot_t.points = [(i, x[j]) for i, j in zip(t, range(len(t)))]

        self.prev_val = value

    def dropdown_file(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Reset",
                "on_release": lambda x="Reset": self.menu_callback_file(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Save",
                "on_release": lambda x="Save": self.menu_callback_file(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Theme",
                "on_release": lambda x="Theme": self.menu_callback_file(x)
            }
        ]
        self.menu = MDDropdownMenu(
            # position="bottom",
            caller=self.ids.file,
            items=self.menu_list,
            width_mult=3,
            max_height=300,
            ver_growth="down",
        )
        self.menu.open()

    def menu_callback_file(self, text_item):
        if text_item == "Reset":
            self.update_plot(None, None, None, 1)
            self.ids.ampl_p.value = self.get_default_slider_value('P', 0)
            self.ids.ampl_q.value = self.get_default_slider_value('Q', 0)
            self.ids.ampl_r.value = self.get_default_slider_value('R', 0)
            self.ids.ampl_s.value = self.get_default_slider_value('S', 0)
            self.ids.ampl_st.value = self.get_default_slider_value('ST', 0)
            self.ids.ampl_t.value = self.get_default_slider_value('T', 0)

            self.ids.time_p.value = self.get_default_slider_value('P', 3)
            self.ids.time_q.value = self.get_default_slider_value('Q', 3)
            self.ids.time_r.value = self.get_default_slider_value('R', 3)
            self.ids.time_s.value = self.get_default_slider_value('S', 3)
            self.ids.time_st.value = self.get_default_slider_value('ST', 3)
            self.ids.time_t.value = self.get_default_slider_value('T', 3)

            self.ids.b1_p.value = self.get_default_slider_value('P', 1)
            self.ids.b1_q.value = self.get_default_slider_value('Q', 1)
            self.ids.b1_r.value = self.get_default_slider_value('R', 1)
            self.ids.b1_s.value = self.get_default_slider_value('S', 1)
            self.ids.b1_st.value = self.get_default_slider_value('ST', 1)
            self.ids.b1_t.value = self.get_default_slider_value('T', 1)

            self.ids.b2_p.value = self.get_default_slider_value('P', 2)
            self.ids.b2_q.value = self.get_default_slider_value('Q', 2)
            self.ids.b2_r.value = self.get_default_slider_value('R', 2)
            self.ids.b2_s.value = self.get_default_slider_value('S', 2)
            self.ids.b2_st.value = self.get_default_slider_value('ST', 2)
            self.ids.b2_t.value = self.get_default_slider_value('T', 2)

        elif text_item == "Theme":
            with open('theme.txt', 'r') as file:
                cur_theme = file.read()
            with open('theme.txt', 'w') as file:
                file.write('Light' if cur_theme == 'Dark' else 'Dark')

        elif text_item == 'Save':

            num = random.randint(0, 1000000)
            filename = f'graph_{num}.png'
            self.export_to_png(os.path.join('graphs', filename))
            img = cv2.imread(os.path.join('graphs', filename))
            img = cv2.resize(img, (int(img.shape[1] // 1.5), int(img.shape[0] // 1.5)))
            cv2.imwrite(os.path.join('graphs', filename), img[50:690, 0:750])

    def dropdown_noise(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Generate",
                "on_release": lambda x="Generate": self.menu_callback_noise(x)
            },

        ]
        self.menu = MDDropdownMenu(
            # position="bottom",
            caller=self.ids.noise,
            items=self.menu_list,
            width_mult=3,
            max_height=112,
            ver_growth="down",
        )
        self.menu.open()

    def menu_callback_noise(self, text_item):
        if text_item == 'Generate':
            process = Popen(
                ['python3', '/Users/bellzebull/Documents/КПИ/4й сем/AI/KP3/kivy_app/Generate.py',
                 str(self.current_params)], stdout=PIPE, stderr=PIPE)
            output, error = process.communicate()

            # Печать вывода из stdout и stderr
            print(output.decode())
            print(error.decode())




    def get_default_slider_value(self, current_pick, current_param):
        _, _, params = update_plot_params()
        return params[current_pick][current_param]


class Master_2023(MDApp):
    def build(self):
        Builder.load_file('EKG.kv')
        with open('theme.txt', 'r') as file:
            if file.read() == 'Dark':
                self.theme_cls.theme_style = "Dark"
            elif file.read() == 'Light':
                self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Container()


if __name__ == "__main__":
    Master_2023().run()
