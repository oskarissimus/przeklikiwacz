import logging
import tkinter as tk



class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
             func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None





class Model:
    def __init__(self):
        self.currentAction = Observable("inicjacja currentAction")

    def currentAction_set(self, action):
        self.currentAction.set(action)







class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)



        self.clickerButton = tk.Button(self,
                                       height=3,
                                       width=15,
                                       bg="chartreuse3",
                                       fg="white",
                                       font='Helvetica 18 bold',
                                       text='PRZEKLIKUJ')
        self.clickerButton.pack(side="top")
        
        

        
        self.pauseButton = tk.Button(self,
                                     height = 3,
                                     width = 15,
                                     font='Helvetica 18 bold',
                                     text='PAUZA')
        self.pauseButton.pack(side="top")
      
        

        

#        self.edit = tk.Button(self, text="edytuj plik konfiguracyjny",width=25,font='Helvetica 11', command=self.open_config)
#        self.edit.pack()
#
#        self.reload = tk.Button(self, text="przeładuj konfigurację",width=25,font='Helvetica 11', command=self.reload_config)
#        self.reload.pack()
#
#        self.quit = tk.Button(self, text="QUIT", font='Helvetica 11', command=self.master.destroy)
#        self.quit.pack(side="bottom")
        
        self.infoBox = tk.Label(self,text="elo")
        self.infoBox.pack(side="top")


        
        
        self.winfo_toplevel().title("Przeklikiwacz 1.0")
        self.config(padx=30,pady=30)





    def currentAction_display(self, action):
        self.infoBox.configure(text=action)







class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View (root)
        
        ##przypinanie funkcji kontrolera do widoku
        self.view.clickerButton.config (command = lambda: self.currentAction_set('przeklikiwanie'))
        self.view.pauseButton.config   (command = lambda: self.currentAction_set('pauza'))

        ##przypinanie callback do observable        
        self.model.currentAction.addCallback (self.currentAction_changed)
        self.currentAction_changed('nic')
        
    def browser_click_targets_in_all_urls(self):
        logging.debug ('klikam niby')

    def currentAction_set(self, action):
        self.model.currentAction_set(action)

    def currentAction_changed(self, action):
        self.view.currentAction_display(action)
        self.browser_click_targets_in_all_urls()






if __name__ == '__main__':
    logging.basicConfig(filename='przeklikiwacz.log', filemode='w', level=logging.DEBUG)
    logging.info('przeklikiwacz started')
    root = tk.Tk()
    root.withdraw()
    logging.info('kontrolka')
    app = Controller(root)
    root.mainloop()


