import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import pandas as pd

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App(ttk.Frame):

    __filename = {"turns": "turns_took.csv",
                   "weapon": "first_weapon.csv",
                   "first": "first_mob.csv",
                   "dead": "first_dead.csv",
                   "killed": "all_kills.csv"}
    
    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.__parent = parent
        self.__parent.title("Game Statistics")
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

        self.__data_base = {}
        self.load_data_base()

    def create_widgets(self):
        # creating a row with combobox widgets for filters
        self.frame_dist = ttk.LabelFrame(self, text="Select Distribution")
        self.frame_dist.grid(row=1, column=0, sticky="NEWS")


        self.choice = ttk.Combobox(self.frame_dist, state="readonly")
        self.choice['values'] = (
            'Turn took',
            'First weapon',
            'First monster',
            'First dead',
            'Kills before quit'
        )
        self.choice.bind('<<ComboboxSelected>>', self.update_dist)
        self.choice.grid(row=0, column=0, padx=10, pady=10)


        self.btn_quit = ttk.Button(self, text="Quit", command=self.__parent.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)
        self.btn_quit = ttk.Button(self, text="Quit", command=self.__parent.destroy)


        ## create Matplotlib figure and plotting axes
        self.fig_graph = Figure()
        self.fig_graph.set_size_inches(10, 7)
        self.ax_graph = self.fig_graph.add_subplot()


        # create a canvas to host the figure and place it into the main window
        self.fig_canvas = FigureCanvasTkAgg(self.fig_graph, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0,
                                             sticky="news", padx=10, pady=10)
        

    def load_data_base(self):
        for key, value in self.__filename.items():
            self.__data_base[key] = pd.DataFrame(pd.read_csv("database/"+ value))
    
    def show_turn_took(self):
        self.fig_graph.clf()
        self.ax_graph = self.fig_graph.add_subplot(111)

        df = self.__data_base['turns']
        self.ax_graph.set_title("Turns took to kill each mob (First encounter)")
        gb = df.groupby('Name')
        columns = ["Name", "Turns"]
        data = [[p, f"{int(gb["Turns"].mean()[p]):.1f}"] for p in df.Name.unique()]

        self.ax_graph.set_axis_off()

        table = self.ax_graph.table(cellText=data, colLabels=columns, loc='center', cellLoc='right')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        self.fig_canvas.draw()
    
    def show_first_dead(self):
        self.fig_graph.clf()
        self.ax_graph = self.fig_graph.add_subplot(111)

        data = self.__data_base['dead']
        mob_counts = data['Mob'].value_counts()

        custom_order = [
                        "SLIME", "GOBLIN", "DARK", "SCORPION", "BLUE", "PURPLE",
                        "MINOTAUR1", "MINOTAUR2", "MINOTAUR3",
                        "VAMPIRE1", "VAMPIRE2", "VAMPIRE3"
                    ]
        
        mob_counts = mob_counts.reindex(custom_order, fill_value=0)
        mob_counts.plot(kind='bar', ax=self.ax_graph, color='skyblue', edgecolor='black')

        self.ax_graph.set_title('First Dead Mob Counts')
        self.ax_graph.set_xlabel('Mob')
        self.ax_graph.set_ylabel('Count')
        self.ax_graph.set_xticks(range(len(mob_counts)))
        self.ax_graph.set_xticklabels(mob_counts.index, rotation=45, ha='right')

        max_val = mob_counts.max()
        self.ax_graph.set_ylim(0, max_val + 1)
        self.ax_graph.set_yticks(range(0, max_val + 2))
        self.ax_graph.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig_canvas.draw()

    def show_enemies_killed(self):
        self.fig_graph.clf()
        self.ax_graph = self.fig_graph.add_subplot(111)

        df = self.__data_base['killed']

        self.ax_graph.set_title("Enemies Killed Before Quitting the Game")
        self.ax_graph.set_xlabel("Number of Enemies Killed")
        self.ax_graph.set_ylabel("Frequency")

        bins = [0, 5, 10, 15, 20, 25, float('inf')]
        labels = ['0–4', '5–9', '10–14', '15–19', '20–24', '25+']

        df['Kill Range'] = pd.cut(df['Kills'], bins=bins, labels=labels, right=False)
        counts = df['Kill Range'].value_counts().reindex(labels, fill_value=0)

        x = list(range(len(labels)))
        self.ax_graph.bar(x, counts, color='skyblue', edgecolor='black')

        self.ax_graph.set_xticks(x)
        self.ax_graph.set_xticklabels(labels)
        self.ax_graph.grid(axis='y', linestyle='--', alpha=0.7)

        self.fig_canvas.draw()

    def show_first_monster(self):
        self.fig_graph.clf()
        self.ax_graph = self.fig_graph.add_subplot(111)
        df = self.__data_base['first']
        
        mob_counts = df['Mob'].value_counts().sort_values(ascending=False)

        wedges, texts, autotexts = self.ax_graph.pie(
            mob_counts,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=1.2, 
            textprops=dict(color="black"),
            wedgeprops=dict(edgecolor='black'),
        )

        for autotext in autotexts:
            autotext.set_fontsize(7)

        self.ax_graph.legend(
            wedges, 
            mob_counts.index, 
            title="Monster", 
            loc="center left", 
            bbox_to_anchor=(1, 0.5)
        )

        self.ax_graph.set_title("First Monster Encountered by Players")
        self.fig_canvas.draw()

    def show_first_weapon(self):
        self.fig_graph.clf()
        self.ax_graph = self.fig_graph.add_subplot(111)

        data = self.__data_base['weapon']
        w_count = data['Weapon'].value_counts()
        custom_order = ["Sword", "Knife", "Hammer"]
        
        w_count = w_count.reindex(custom_order, fill_value=0)
        w_count.plot(kind='bar', ax=self.ax_graph, color='skyblue', edgecolor='black')

        self.ax_graph.set_title('First Weapon')
        self.ax_graph.set_xlabel('Weapon')
        self.ax_graph.set_ylabel('Frequency')
        self.ax_graph.set_xticks(range(len(w_count)))
        self.ax_graph.set_xticklabels(w_count.index, rotation=45, ha='right')

        max_val = w_count.max()
        self.ax_graph.set_ylim(0, max_val + 1)
        self.ax_graph.set_yticks(range(0, max_val + 2))

        self.ax_graph.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig_canvas.draw()

    def update_dist(self, ev):
        dist = self.choice.get()
        if dist == 'Turn took':
            self.show_turn_took()
        elif dist == 'First weapon':
            self.show_first_weapon()
        elif dist == 'First monster':
            self.show_first_monster()
        elif dist == 'First dead':
            self.show_first_dead()
        elif dist == 'Kills before quit':
            self.show_enemies_killed()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matplotlib Integration")
    root.geometry("1200x900")
    app = App(root)
    root.mainloop()
