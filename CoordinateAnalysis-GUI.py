from Tkinter import *
import tkFileDialog as filedialog
import ScrolledText as scrolledtext
import tkMessageBox
import os

class Application(Frame):
    def cleartext(self):
        self.textbox.delete(1.0, END)
        if self.lonentry.get() != "lon. coordinate of sample area's SW corner.." and self.latentry.get() != "lat. coordinate of sample area's SW corner.." and self.lonentry2.get() != "lon. coordinate of sample area's NE corner.." and self.latentry2.get() != "lat. coordinate of sample area's NE corner..":
            self.lonentry.delete(0, END)
            self.latentry.delete(0, END)
            self.lonentry2.delete(0, END)
            self.latentry2.delete(0, END)

    def output(self):
        output = self.textbox.get('1.0', 'end-1c')
        if output == '':
            tkMessageBox.showinfo("Export Error", "There are no results to export yet!")
        elif output != '':
            with open("Coordinate-Check-Results.txt", "w") as f:
                f.write(output)
            location = os.getcwd()
            tkMessageBox.showinfo("Success!", "Your results were exported to...\n" + location +"/Coordinate-Check-Results.txt")

    def spatialbounds(self):
        valid = False
        if valid == False:
            try:
                SWlon = self.lonentry.get()
                SWlon = float(SWlon)
                SWlat = self.latentry.get()
                SWlat = float(SWlat)
                NElon = self.lonentry2.get()
                NElon = float(NElon)
                NElat = self.latentry2.get()
                NElat = float(NElat)
                valid = True
            except:
                tkMessageBox.showinfo("Entry Error", "Please enter decimal coordinates (e.g. 12.32443) in all entry fields")
                self.quit

        if valid == True:
            filename = filedialog.askopenfilename()
            if filename != '':
                try:
                    extension = filename.find(".")
                    extension = filename[extension:]
                    extension = extension.replace(".",'')
                    jsonexts = ("geojson","GEOJSON","GeoJSON","GeoJson","json","JSON", "js", "JS")
                    if extension in jsonexts:
                        with open(filename, 'r') as fout:
                            filedata = fout.read()
                            pointcount = filedata.count('"coordinates"')

                            if pointcount > 0:
                                points = filedata.split('"geometry"')
                                del points[0]

                                lons = []
                                lats = []

                                for i in points:
                                    index = i.find('[')
                                    cords = i.replace(i[:index], '')
                                    index = cords.find(']')
                                    cords = cords.replace(cords[index:], '')
                                    cords = cords.replace('[','')
                                    lon = float(cords.split(',')[0])
                                    lat = float(cords.split(',')[1])
                                    lons.append(lon)
                                    lats.append(lat)
  
                                text = "\nProcessing file: %s\n%s" % (filename,"-"*50)
                                self.textbox.insert(INSERT, text)
                                text = "\nCoordinates (%4.6f, %4.6f) - are Lower Limits" % (SWlon,SWlat)
                                self.textbox.insert(INSERT, text)
                                text = "\nCoordinates (%4.6f, %4.6f) - are Upper Limits\n%s" % (NElon, NElat, "-"*50)
                                self.textbox.insert(INSERT, text)

                                ibcount = 0
                                obcount = 0
                                vcount  = 0
                                
                                for i in range(len(lons)):
                                    
                                    vcount +=1
                                    
                                    if lons[i] < SWlon or lats[i] < SWlat or lons[i] > NElon or lats[i] > NElat:
                                        obcount += 1
                                        if lons[i] < SWlon and lats[i] < SWlat:
                                            text = "\nPoint: (%4.6f, %4.6f) - Longitude and latitude values were too LOW" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)
                                        elif lons[i] < SWlon:
                                            text = "\nPoint: (%4.6f, %4.6f) - Longitude value was too LOW" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)
                                        elif lats[i] < SWlat:
                                            text = "\nPoint: (%4.6f, %4.6f) - Latitude value was too LOW" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)
                                        elif lons[i] > NElon and lats[i] > NElat:
                                            text = "\nPoint: (%4.6f, %4.6f) - Longitude and latitude values were too HIGH" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)
                                        elif lons[i] > NElon:
                                            text = "\nPoint: (%4.6f, %4.6f) - Longitude value was too HIGH" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)
                                        elif lats[i] > NElat:
                                            text = "\nPoint: (%4.6f, %4.6f) - Latitude value was too HIGH" % (lons[i], lats[i])
                                            self.textbox.insert(INSERT, text)                 

                                    elif lons[i] > SWlon and lats[i] > SWlat and lons[i] < NElon and lats[i] <  NElat:
                                        ibcount +=1
                                        text = "\nPoint: (%4.6f, %4.6f) - is within bounds!" % (lons[i], lats[i])
                                        self.textbox.insert(INSERT, text)

                                text = "\n\n Summary \n%s" % ("="*42)
                                self.textbox.insert(INSERT, text)
                                text = "\n - %d vertices were found." % (vcount)
                                self.textbox.insert(INSERT, text)
                                text = "\n - %d vertices were inside sample area boundary." % (ibcount)
                                self.textbox.insert(INSERT, text)
                                text = "\n - %d vertices were outside sample area boundary.\n" % (obcount)
                                self.textbox.insert(INSERT, text)                                                    

                            elif pointcount == 0:
                                tkMessageBox.showinfo("File Error", "Looks like there are point features in this file friend")
                                
                    elif extension not in jsonexts:
                        tkMessageBox.showinfo("File Error", "Please select a GeoJSON, JSON, or JS file")
                except:
                    self.quit
            elif filename == '':
                self.quit
            
    def createWidgets(self):
        def on_entry_click(event):
            if self.lonentry.get() == "lon. coordinate of sample area's SW corner..":
               self.lonentry.delete(0, "end") # delete all the text in the entry
               self.lonentry.insert(0, '') #Insert blank for user input
               self.lonentry.config(fg = 'black')
        def on_focusout(event):
            if self.lonentry.get() == '':
                self.lonentry.insert(0, "lon. coordinate of sample area's SW corner..")
                self.lonentry.config(fg = 'grey')

        def on_entry_click2(event):
            if self.latentry.get() == "lat. coordinate of sample area's SW corner..":
               self.latentry.delete(0, "end") # delete all the text in the entry
               self.latentry.insert(0, '') #Insert blank for user input
               self.latentry.config(fg = 'black')
        def on_focusout2(event):
            if self.latentry.get() == '':
                self.latentry.insert(0, "lat. coordinate of sample area's SW corner..")
                self.latentry.config(fg = 'grey')

        def on_entry_click3(event):
            if self.lonentry2.get() == "lon. coordinate of sample area's NE corner..":
               self.lonentry2.delete(0, "end") # delete all the text in the entry
               self.lonentry2.insert(0, '') #Insert blank for user input
               self.lonentry2.config(fg = 'black')
        def on_focusout3(event):
            if self.lonentry2.get() == '':
                self.lonentry2.insert(0, "lon. coordinate of sample area's NE corner..")
                self.lonentry2.config(fg = 'grey')

        def on_entry_click4(event):
            if self.latentry2.get() == "lat. coordinate of sample area's NE corner..":
               self.latentry2.delete(0, "end") # delete all the text in the entry
               self.latentry2.insert(0, '') #Insert blank for user input
               self.latentry2.config(fg = 'black')
        def on_focusout4(event):
            if self.latentry2.get() == '':
                self.latentry2.insert(0, "lat. coordinate of sample area's NE corner..")
                self.latentry2.config(fg = 'grey')

        self.lonentry = Entry(self, width = 32)
        self.lonentry.insert(0, "lon. coordinate of sample area's SW corner..")
        self.lonentry.config(fg = "grey")
        self.lonentry.bind('<FocusIn>', on_entry_click)
        self.lonentry.bind('<FocusOut>', on_focusout)
        self.lonentry.grid(row=1, column=0, padx=5)
        
        self.latentry = Entry(self, width = 32)
        self.latentry.insert(0, "lat. coordinate of sample area's SW corner..")
        self.latentry.config(fg = "grey")
        self.latentry.bind('<FocusIn>', on_entry_click2)
        self.latentry.bind('<FocusOut>', on_focusout2)
        self.latentry.grid(row=1, column=1, padx=5)

        self.lonentry2 = Entry(self, width = 32)
        self.lonentry2.insert(0, "lon. coordinate of sample area's NE corner..")
        self.lonentry2.config(fg = "grey")
        self.lonentry2.bind('<FocusIn>', on_entry_click3)
        self.lonentry2.bind('<FocusOut>', on_focusout3)
        self.lonentry2.grid(row=2, column=0, pady=15, padx=5)

        self.latentry2 = Entry(self, width = 32)
        self.latentry2.insert(0, "lat. coordinate of sample area's NE corner..")
        self.latentry2.config(fg = "grey")
        self.latentry2.bind('<FocusIn>', on_entry_click4)
        self.latentry2.bind('<FocusOut>', on_focusout4)
        self.latentry2.grid(row=2, column=1, pady=15, padx=5)

        self.ap = Button(self, width = 60)
        self.ap["text"] = "Select File and Identify Location of Data Points Relative to the Sample Area"
        self.ap["command"] = self.spatialbounds
        self.ap.grid(row=3, column=0, columnspan=2)

        self.textbox = scrolledtext.ScrolledText(self)
        self.textbox.grid(row=4, column=0, columnspan=2, pady=10)

        self.clear = Button(self, width = 60)
        self.clear["text"] = "Clear Contents"
        self.clear["command"] = self.cleartext
        self.clear.grid(row=5, column=0, columnspan=2)

        self.export = Button(self, width = 60)
        self.export["text"] = "Export Results to .TXT File"
        self.export["command"] = self.output
        self.export.grid(row=6, column=0, columnspan=2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

window = Tk()

app = Application(master=window)

window.title("GeoPython App")
window.geometry('625x570')

app.mainloop()
