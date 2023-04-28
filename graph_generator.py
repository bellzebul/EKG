import matplotlib as mpl
import matplotlib.pyplot as plt
from kivy.metrics import dp
from get_graph_params import update_generated_plot_params

mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 1000

mpl.rcParams['font.family'] = 'Verdana'
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.linewidth'] = 1.0

font_size_axis_title = dp(13)
font_size_axis_tick = dp(15)


class GraphGenerator(object):
    """class that generate Matplotlib graph."""

    def __init__(self, current_params, n, alt=0.5, noise_lvl=0, alpha=None, width=None):

        super().__init__()

        self.current_params = current_params
        self.n = n

        self.fig, self.ax1 = plt.subplots(1, 1)

        if alt is not None:
            if alpha is not None:
                t, x, self.current_params = update_generated_plot_params(self.current_params, self.n, alt, noise_lvl,
                                                                         alpha)
            else:
                t, x, self.current_params = update_generated_plot_params(self.current_params, self.n, alt, noise_lvl,
                                                                         None, width)
        else:
            if alpha is not None:
                t, x, self.current_params = update_generated_plot_params(self.current_params, self.n, noise_lvl, alpha)
            else:
                t, x, self.current_params = update_generated_plot_params(self.current_params, self.n, alt, noise_lvl,
                                                                         None, width)

        self.line1, = self.ax1.plot(t, x, label='line1', color=[1, 0, 0.2, 0.7])

        self.xmin, self.xmax = self.ax1.get_xlim()
        if self.n > 6:
            self.ymin, self.ymax = -1 * self.n * 0.15, self.n * 0.25
        else:
            self.ymin, self.ymax = -1, 1.5
        self.fig.subplots_adjust(left=0.045, top=0.98, right=0.99, bottom=0.08)

        self.ax1.set_xlim(self.xmin, self.xmax)
        self.ax1.set_ylim(self.ymin, self.ymax)

        self.ax1.grid()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        # self.ax1.set_xlabel("Time [s]", fontsize=font_size_axis_title)
