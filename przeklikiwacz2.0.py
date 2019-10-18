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
        self.currentAction    = Observable("inicjacja currentAction")
        self.actionsEnabled   = Observable(["inicjacja ActionsEnabled"])
        self.actionsAvailable = ['przeklikiwanie','pauza','edit','reload','quit','ready']


    def currentAction_set(self, action):
        self.currentAction.set(action)


    def actionsEnabled_set(self, actions):
        self.actionsEnabled.set(actions)
        




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
      
        

        

        self.editButton = tk.Button(self,
                                    text="edytuj plik konfiguracyjny",
                                    width=25,
                                    font='Helvetica 11')
        self.editButton.pack(side="top")





        self.reloadButton = tk.Button(self,
                                      text="przeładuj konfigurację",
                                      width=25,
                                      font='Helvetica 11')
        self.reloadButton.pack(side="top")





        self.quitButton = tk.Button(self,
                                    text="QUIT",
                                    font='Helvetica 11')
        self.quitButton.pack(side="top")
        
        self.infoBox = tk.Label(self,text="elo")
        self.infoBox.pack(side="bottom")


        
        
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
        self.view.editButton.config    (command = lambda: self.currentAction_set('edit'))
        self.view.reloadButton.config  (command = lambda: self.currentAction_set('reload'))
        self.view.quitButton.config    (command = lambda: self.currentAction_set('quit'))

        ##przypinanie callback do observable        
        self.model.currentAction.addCallback  (self.currentAction_changed)

        self.model.actionsEnabled.addCallback (self.actionsEnabled_changed)

        
    def browser_click_targets_in_all_urls(self):
        logging.debug ('klikam niby')

    def currentAction_set(self, action):
        self.model.currentAction_set(action)

    def currentAction_changed(self, action):
        self.view.currentAction_display(action)
        if action == 'przeklikiwanie' :
            self.model.actionsEnabled_set(['pauza'])
            self.browser_click_targets_in_all_urls()
            
            
        if action == 'pauza' :
            self.model.actionsEnabled_set(['przeklikiwanie','edit','reload','quit'])
            self.browser_pause()
            
            
        if action == 'edit' :
            self.model.actionsEnabled_set([])
            self.config_edit()
            self.currentAction_set('ready')
            
            
        if action == 'reload' :
            self.model.actionsEnabled_set([])
            self.config_reload()
            self.currentAction_set('ready')
            
            
        if action == 'ready' :
            self.model.actionsEnabled_set(['przeklikiwanie','edit','reload','quit'])
            #ready state to set after some actions


        if action == 'quit' :
            self.model.actionsEnabled_set([])
            #quit program



    def actionsEnabled_changed(self, actions):
        if 'przeklikiwanie' in actions:
            self.view.clickerButton.config(state="normal")
        else:
            self.view.clickerButton.config(state="disabled")


        if 'pauza' in actions:
            self.view.pauseButton.config(state="normal")
        else:
            self.view.pauseButton.config(state="disabled")


        if 'edit' in actions:
            self.view.editButton.config(state="normal")
        else:
            self.view.editButton.config(state="disabled")


        if 'reload' in actions:
            self.view.reloadButton.config(state="normal")
        else:
            self.view.reloadButton.config(state="disabled")


        if 'quit' in actions:
            self.view.quitButton.config(state="normal")
        else:
            self.view.quitButton.config(state="disabled")



    def config_edit(self):
        #open config file in notepad
        return
    
    def config_reload(self):
        #load configfile to program state
        return




if __name__ == '__main__':
    logging.basicConfig(filename='przeklikiwacz.log', filemode='w', level=logging.DEBUG)
    logging.info('przeklikiwacz started')
    root = tk.Tk()
    root.withdraw()
    logging.info('kontrolka')
    app = Controller(root)
    root.mainloop()


