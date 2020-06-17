import numpy as np

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style

# style.use('fivethirtyeight')

# class LivePlot:
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax1 = self.fig.add_subplot(1,1,1)

#         self.x = []
#         self.y = []

#     def plot(self):
#         self.animation = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)
#         self.ax1.plot(self.x, self.y)

#     def add_data(self, x, y):
#         self.x.append(x)
#         self.y.append(y)
        
#         self.update_plot()

#     def update_plot(self):

#         self.ax1.clear()
#         self.ax1.plot(self.x, self.y)



class Logger():

    def __init__(self):
        self.containers = {}

    def print_infos(self, obj):
        obj.print_infos()

    def add_var(self, name):
        self.containers[name] = []
    
    def add_var_value(self, name, value):
        self.containers[name].append(value)

    def print_var_mean(self, name):
        print("MEAN OF {}: {:.3f}".format(name, np.mean(self.containers[name])))

    def print_obj(self, msg, obj):
        print(f"{msg}: {obj}")



logger = Logger()