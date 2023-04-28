import numpy as np
from typing import Dict, List
from random import uniform


def update_plot_params(current_pick: str = None, current_param: int = None, value: float = None,
                       param_set: Dict[str, List[float]] = None):
    if param_set == None:
        params: Dict[str, List[float]] = {'P': [0.11, 0.016, 0.008, 0.399],
                                          'Q': [-0.15, 0.01, 0.002, 0.45],
                                          'R': [1.15, 0.008, 0.007, 0.474],
                                          'S': [-0.29, 0.006, 0.017, 0.495],
                                          'ST': [0.025, 0.012, 0.0, 0.574],
                                          'T': [0.25, 0.062, 0.072, 0.7]}
    else:
        params: Dict[str, List[float]] = param_set
        params[current_pick][current_param] = value

    time_points: Dict[str, List[float]] = {'P': [], 'Q': [], 'R': [], 'S': [], 'ST': [], 'T': []}

    def get_time(time_points: Dict[str, List[float]], params: Dict[str, List[float]]) -> Dict[str, list[float]]:
        for pick in time_points.keys():
            t1 = params[pick][3] - 3 * params[pick][1]
            t2 = params[pick][3] + 3 * params[pick][2]
            time_points[pick].append(t1)
            time_points[pick].append(t2)

        if time_points['R'][0] < time_points['Q'][1]:
            time_points['R'][0] = time_points['Q'][1]
        if time_points['S'][0] < time_points['R'][1]:
            time_points['S'][0] = time_points['R'][1]
        if time_points['ST'][0] < time_points['S'][1]:
            time_points['ST'][0] = time_points['S'][1]
        if time_points['T'][0] < time_points['ST'][1]:
            time_points['T'][0] = time_points['ST'][1]

        if time_points['T'][1] > t0:
            time_points['T'][1] = t0
        return time_points

    def b(t, pick: List[float]):
        if t <= pick[3]:
            return pick[1]
        else:
            return pick[2]

    def Gauss(pick: List[float], t) -> float:
        z = pick[0] * np.exp(- ((t - pick[-1]) ** 2) / (2 * b(t, pick) ** 2))
        return z

    fs = 60000
    t0 = 60 * 1000 / fs
    t = np.arange(0, t0, 0.001)
    x: List[float] = []

    get_time(time_points, params)

    for i in t:
        if time_points['P'][0] <= i < time_points['P'][1]:
            x.append(Gauss(params['P'], i))
        elif time_points['Q'][0] <= i < time_points['Q'][1]:
            x.append(Gauss(params['Q'], i))
        elif time_points['R'][0] <= i < time_points['R'][1]:
            x.append(Gauss(params['R'], i))
        elif time_points['S'][0] <= i < time_points['S'][1]:
            x.append(Gauss(params['S'], i))
        elif time_points['ST'][0] <= i < time_points['ST'][1]:
            x.append(Gauss(params['ST'], i))
        elif time_points['T'][0] <= i < time_points['T'][1]:
            x.append(Gauss(params['T'], i))
        else:
            x.append(0)

    return t, x, params


def update_generated_plot_params(param_set: Dict[str, List[float]], n: int, _alt_lvl: float = None,
                                 noise_lvl: float = 0, alpha=None, width=None):
    params = param_set
    time_points: Dict[str, List[float]] = {'P': [], 'Q': [], 'R': [], 'S': [], 'ST': [], 'T': []}
    if _alt_lvl is not None:
        alt_lvl = _alt_lvl
    else:
        alt_lvl = 0.5
    fs = 60
    t0 = 60 / fs
    t = np.arange(0, t0, 0.001)

    def get_time(time_points: Dict[str, List[float]], params: Dict[str, List[float]]) -> Dict[str, int]:

        for pick in time_points.keys():
            t1 = params[pick][3] - 3 * params[pick][1]
            t2 = params[pick][3] + 3 * params[pick][2]
            time_points[pick].append(t1)
            time_points[pick].append(t2)

            # if time_points['R'][0] < time_points['Q'][1]:
            #     time_points['R'][0] = time_points['Q'][1]
            # if time_points['S'][0] < time_points['R'][1]:
            #     time_points['S'][0] = time_points['R'][1]
            # if time_points['ST'][0] < time_points['S'][1]:
            #     time_points['ST'][0] = time_points['S'][1]
            # if time_points['T'][0] < time_points['ST'][1]:
            #     time_points['T'][0] = time_points['ST'][1]

        if time_points['T'][1] > t0:
            time_points['T'][1] = t0
        return time_points

    get_time(time_points, params)

    def b(t, pick: List[float]):
        if t <= pick[3]:
            return pick[1]
        else:
            return pick[2]

    def lamb(A, turn):
        return 1 + alt_lvl / A if turn == 0 else 1

    def Gauss(pick: List[float], t, turn=-1) -> float:
        key = [k for k, v in params.items() if v == pick][0]
        if key == 'T':
            z = pick[0] * lamb(pick[0], turn) * np.exp(- ((t - pick[-1]) ** 2) / (2 * b(t, pick) ** 2)) + \
                uniform(0, noise_lvl)
        else:
            z = pick[0] * np.exp(- ((t - pick[-1]) ** 2) / (2 * b(t, pick) ** 2)) + \
                uniform(0, noise_lvl)
        return z

    x: List[float] = []
    turn = 0
    for j in range(n):
        for i in t:
            if time_points['P'][0] <= i < time_points['P'][1]:
                x.append(Gauss(params['P'], i))
            elif time_points['Q'][0] <= i < time_points['Q'][1]:
                x.append(Gauss(params['Q'], i))
            elif time_points['R'][0] <= i < time_points['R'][1]:
                x.append(Gauss(params['R'], i))
            elif time_points['S'][0] <= i < time_points['S'][1]:
                x.append(Gauss(params['S'], i))
            elif time_points['ST'][0] <= i < time_points['ST'][1]:
                x.append(Gauss(params['ST'], i))
            elif time_points['T'][0] <= i < time_points['T'][1]:
                x.append(Gauss(params['T'], i, turn % 2))
            else:
                x.append(uniform(0, noise_lvl))
        turn += 1

    t_all = t
    for i in range(1, n):
        t_temp = [sample + t0 * i for sample in t]
        t_all = np.concatenate((t_all, t_temp))

    if alpha != None:
        x = exp_filter(x, alpha)

    if width != None:
        x = smoothing_filter(x, width)

    return t_all, x, params


def exp_filter(x, alpha):
    x_exp = [0]
    for k in range(1, len(x)):
        x_exp.append(x_exp[k - 1] + alpha * (x[k] - x_exp[k - 1]))
    return x_exp


def smoothing_filter(x, w):
    x_ad = [0]
    for k in range(1, len(x)):
        x_ad.append(x_ad[k - 1] + (x[k] - x[k - w]) / w)
    return x_ad
