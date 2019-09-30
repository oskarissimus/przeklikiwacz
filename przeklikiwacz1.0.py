from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv
import tkinter as tk
import threading
import os
import sys
from urllib.parse import urlparse


frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
print( 'we are',frozen,'frozen')
print( 'bundle dir is', bundle_dir )
print( 'sys.argv[0] is', sys.argv[0] )
print( 'sys.executable is', sys.executable )
print( 'os.getcwd is', os.getcwd() )



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sites_targets_path = os.path.join(bundle_dir, 'sites_targets.csv')
        self.master = master
        self.pack(padx=30,pady=30,ipadx=20,ipady=20)
        self.create_widgets()
        self.thread_on = False
        self.thread_should_stop = False
        self.p_interval = 120 * 1000
        self.time = int(self.p_interval / 1000)
        self.to_close=[]
        self.pauza()
        self.open_browser()
        
    def open_browser(self):
        
        print (self.sites_targets_path)
        with open(self.sites_targets_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.sites_targets = list(csv_reader)
            self.sites_targets_dict = {rows[0]:rows[1] for rows in self.sites_targets}
            chromedriver_path = os.path.join(bundle_dir, 'chromedriver.exe')
            chromedriver_path = os.path.join(chromedriver_path, 'chromedriver.exe')
            print (chromedriver_path)
            self.browser = webdriver.Chrome(chromedriver_path)
            threading.Thread(target=self.open_tabs).start()


    def open_tabs(self):
        self.label.configure(text="ładuję konfigurację...")
        self.przeklikuj_button.config(state="disabled")
        self.pauza_button.config(state="disabled")
        self.edit.config(state="disabled")
        self.reload.config(state="disabled")
        self.currently_open_tabs = []
        for window in self.browser.window_handles:
            self.browser.switch_to.window(window) 
            self.currently_open_tabs.append(self.browser.current_url)
            if self.browser.current_url not in self.sites_targets_dict:
                self.to_close.append(window)
                print("oznaczam do ununięcia {}".format(window))
                
        
        for idx,row in enumerate(self.sites_targets):
            if row[0] not in self.currently_open_tabs:
                self.browser.execute_script("window.open('{}','_blank');".format(row[0]))
                print (row)
                
                
        for tab in self.to_close:
            sleep(1)
            try:
                self.browser.switch_to.window(tab)
                print("zamykam {}".format(window))
                self.browser.close()
                print("zamknięte")
                self.to_close.remove(tab)
            except:
                print ("nie da się zamknąć")
        self.przeklikuj_button.config(state="normal")
        self.pauza_button.config(state="normal")
        self.edit.config(state="normal")
        self.reload.config(state="normal")
        self.label.configure(text="konfiguracja załadowana")



        
        

    def create_widgets(self):
        self.przeklikuj_button = tk.Button(self, height=3, width=15, bg="chartreuse3", fg="white", font='Helvetica 18 bold')
        self.przeklikuj_button["text"] = "PRZEKLIKUJ"
        self.przeklikuj_button["command"] = self.przeklikuj_init
        self.przeklikuj_button.pack(side="top")

        self.pauza_button = tk.Button(self, height = 3, width = 15, font='Helvetica 18 bold')
        self.pauza_button["text"] = "PAUZA"
        self.pauza_button["command"] = self.pauza
        self.pauza_button.pack(side="top")
        self.label = tk.Label(text="")
        self.label.pack()

        self.edit = tk.Button(self, text="edytuj plik konfiguracyjny",width=25,font='Helvetica 11', command=self.open_config)
        self.edit.pack()

        self.reload = tk.Button(self, text="przeładuj konfigurację",width=25,font='Helvetica 11', command=self.reload_config)
        self.reload.pack()

        self.quit = tk.Button(self, text="QUIT", font='Helvetica 11', command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.winfo_toplevel().title("Przeklikiwacz 1.0")
        
        
        
    def open_config(self):
        threading.Thread(target=os.system, args=("notepad {}".format(self.sites_targets_path),)).start()
        
        
    def reload_config(self):
        with open(self.sites_targets_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.sites_targets = list(csv_reader)
            parsed_url = urlparse(rows[0])
            self.sites_targets_dict = {parsed_url.netloc:rows[1] for rows in self.sites_targets}
        threading.Thread(target=self.open_tabs).start()

        
        
        
    def przeklikuj_init(self):
        self.pauza(t="przeklikiwanie...")
        print("przeklikuj_init")
        self.t = threading.Thread(target=self.przeklikuj)
        self.t.do_run = True
        self.przeklikuj_button.config(state="disabled")
        self.pauza_button.config(state="normal")
        self.edit.config(state="disabled")
        self.reload.config(state="disabled")        
        self.t.start()
            

            
            
    def przeklikuj(self):
        self.t.do_run = True
        
        self.pauza(t="przeklikiwanie...")

        self.przeklikuj_button.config(state="disabled")
        self.pauza_button.config(state="normal")
        self.edit.config(state="disabled")
        self.reload.config(state="disabled")        

        print("przeklikuje")
        self.windows = self.browser.window_handles
        for idx,row in enumerate(self.sites_targets):
            #print ("jestem w pętli")
            if self.t.do_run:
                #print ("jestem w ifie")
                
                self.browser.switch_to.window(self.windows[idx])
#                print (self.browser.current_url)
                parsed_url = urlparse(self.browser.current_url)
                ntlc = parsed_url.netloc
                try:
                    self.browser.find_element_by_xpath(self.sites_targets_dict[ntlc]).click()
                    print ("kliknięto w {}".format(ntlc))

                except Exception as e:
                    print("nie można kliknąć w {} błąd:".format(ntlc))
                    print(e)
                    print("próbuję kliknąć w ramkach")
                    self.click_in_all_iframes(ntlc)
                    self.click_in_all_frames(ntlc)
        if self.t.do_run:
            self.time = int(self.p_interval / 1000)
            try:
                self.after_cancel(self.clock_id)
            except AttributeError:
                print ("nie ma self.clock_id")

            self.clock_id = self.after(1000,self.update_clock)
            self.id = self.after(self.p_interval,self.przeklikuj_init)



        
            
        
    def pauza(self, t="pauza"):
        print("pauzuje")
        self.label.configure(text=t)
        self.przeklikuj_button.config(state="normal")
        self.pauza_button.config(state="disabled")
        self.edit.config(state="normal")
        self.reload.config(state="normal")        
        
        
        try:
            self.after_cancel(self.id)
        except AttributeError:
            print ("nie ma self.id")
            
        try:
            self.after_cancel(self.clock_id)
        except AttributeError:
            print ("nie ma self.clock_id")
            
        if t == "pauza":
            try:    
                self.t.do_run = False
            except AttributeError:
                print ("nie ma self.t.do_run")
        
        
        
    def update_clock(self):
        self.time -= 1
        print (self.time)
        self.label.configure(text="następne przeklikiwanie za {} sek".format(self.time))
        self.clock_id = self.after(1000,self.update_clock)


    def find_all_iframes(self):
        iframes = self.browser.find_elements_by_xpath("//iframe")
        for index, iframe in enumerate(iframes):
            # Your sweet business logic applied to iframe goes here.
            
            self.browser.switch_to.frame(index)
            
            self.find_all_iframes(driver)
            self.browser.switch_to.parent_frame()

    def click_in_all_iframes(self, ntlc):
        iframes = self.browser.find_elements_by_xpath("//iframe")
        for index, iframe in enumerate(iframes):            
            self.browser.switch_to.frame(index)
            try:
                self.browser.find_element_by_xpath(self.sites_targets_dict[ntlc]).click()
                print ("kliknięto w ramce {}".format(index))
            except Exception as e:
                print ("nie można kliknąć w ramce {}".format(index))
                print (e)
            self.browser.switch_to.parent_frame()


    def click_in_all_frames(self, ntlc):
        iframes = self.browser.find_elements_by_xpath("//frame")
        for index, iframe in enumerate(iframes):            
            self.browser.switch_to.frame(index)
            try:
                self.browser.find_element_by_xpath(self.sites_targets_dict[ntlc]).click()
                print ("kliknięto w ramce {}".format(index))
            except Exception as e:
                print ("nie można kliknąć w ramce {}".format(index))
                print (e)
            self.browser.switch_to.parent_frame()




root = tk.Tk()
app = Application(master=root)
app.mainloop()

