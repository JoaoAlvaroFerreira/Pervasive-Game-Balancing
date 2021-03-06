import tkinter as tk
import os
from main import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

  
def plotMapTest():
        plotmap()

def simTest():
            sim()

def createTest():
            create()

def plotTest():
       a = plot()

       
       kid = []
       young = []
       adult = []
       elderly = []

       for ch in a.gameplay_moments:
           if ch.player.Demographic.Age == "Kid":
               kid.append(ch)
           elif ch.player.Demographic.Age == "Adult":
               adult.append(ch)
           elif ch.player.Demographic.Age == "Elderly":
               elderly.append(ch)
           else:
               young.append(ch)
       
       return {'Age': ['Kid','Adult','Elderly','Young'],
         'Challenges Completed': [len(kid), len(adult), len(elderly), len(young)]
        }


class DataPlatform(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.winfo_toplevel().title("Pervasive Game Data Platform Analysis")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
        
        




class StartPage(tk.Frame):

    

    def __init__(self, master):
        tk.Frame.__init__(self, master)
    


        tk.Button(self,
            text="Create",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command=createTest
        ).pack()

        tk.Button(self,
            text="Simulate",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command=simTest
        ).pack()

        tk.Button(self,
            text="Analysis",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command=lambda: master.switch_frame(AnalysisPage)
        ).pack()

        tk.Button(self,
            text="Interactive Maps",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command=plotMapTest
        ).pack()


        tk.Button(self,
                text="Comprehensive ML Analysis",
                width=25,
                height=5,
                bg="white",
                fg="black",
                command=lambda: master.switch_frame(PageOne)
            ).pack()


       



        

        

app = DataPlatform()

class PageOne(tk.Frame):

    

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
        self.T = tk.Text(self, height = 40, width = 300)
        self.T.pack()
        # ensure a consistent GUI size
        self.grid_propagate(False)
        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        scrollb = tk.Scrollbar(self, command=self.T.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.T['yscrollcommand'] = scrollb.set

        
        tk.Button(self, text="Comprehensive Analysis",
                  command=self.ML_analysis).pack()
        
    def ML_analysis(self):
            a = full_ML()
            self.T.insert(tk.END, a)


        


      
        




class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        figure2 = plt.Figure(figsize=(5,4), dpi=100)

        data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }
        df2 = pd.DataFrame(data2,columns=['Year','Unemployment_Rate'])

        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self)
        line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
        ax2.set_title('Year Vs. Unemployment Rate')

class PageThree(tk.Frame):
     def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Test display").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        data1 = plotTest()
        df1 = pd.DataFrame(data1,columns=['Age','Challenges Completed'])
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = df1[['Age','Challenges Completed']].groupby('Age').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Challenges Completed per Age')

       


class AnalysisPage(tk.Frame):

    def analysisTest(self):
        analysisText = analyse()
        self.T.insert(tk.END, analysisText)


    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the analysis page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
        tk.Button(self,
            text="Analysis",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command= self.analysisTest
        ).pack()

        tk.Button(self,
            text="Graphs",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command= lambda: master.switch_frame(PageThree)
        ).pack()

        self.T = tk.Text(self, height = 40, width = 300)
        self.T.pack()
        # ensure a consistent GUI size
        self.grid_propagate(False)
        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        scrollb = tk.Scrollbar(self, command=self.T.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.T['yscrollcommand'] = scrollb.set

        tk.Button(self, text="Filter Analysis",
                  command=lambda: master.switch_frame(PageOne)).pack()

        
        tk.Button(self, text="Machine Learning with Filtering",
                  command=lambda: master.switch_frame(MLPage)).pack()
        
        

class MLPage(tk.Frame):

    


    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Test display").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        
        
        OPTIONS = [
        "Challenges Done", "Lifetime Value", "Sessions"
        ] #etc

        OPTIONS2 = [
        "Max",
        "Min"
        ] #etc

        canvas1 = tk.Canvas(self, width = 400, height = 300)
        canvas1.pack()
        self.variableString = tk.StringVar(self)
        self.variableString.set(OPTIONS[0]) # default value

        w = tk.OptionMenu(self, self.variableString, *OPTIONS)
        w.pack()

        self.variableMinMax = tk.StringVar(self)
        self.variableMinMax.set(OPTIONS2[0]) # default value

        z = tk.OptionMenu(self, self.variableMinMax, *OPTIONS2)
        z.pack()

        self.entry1 = tk.Entry(self) 
        self.entry1.insert(tk.END, 0)
        canvas1.create_window(200, 140, window=self.entry1)

        
        self.T = tk.Text(self, height = 40, width = 200)
        self.T.pack()
       
       





        tk.Button(self,
            text="Go ML Go",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command=self.MLtest
        ).pack()

    def MLtest(self):
            variableStringT = self.variableString.get()
            variableMinMaxT = self.variableMinMax.get()
            a = ML(variableStringT,self.entry1.get(), variableMinMaxT)
            self.T.insert(tk.END, a)
       


        



app.mainloop()

