from Tkinter import *
import tkFileDialog as filedialog
import ScrolledText as scrolledtext
import tkMessageBox
from pyproj import Proj
from shapely.geometry import shape
import sys, math, re, os
from math import cos, asin, sqrt

class Application(Frame):
    def cleartext(self):
        self.textbox.delete(1.0, END)

    def output(self):
        output = self.textbox.get('1.0', 'end-1c')
        if output == '':
            tkMessageBox.showinfo("Export Error", "There are no results to export yet!")
        elif output != '':
            with open("Geometry-Calc-Results.txt", "w") as f:
                f.write(output)
            location = os.getcwd()
            tkMessageBox.showinfo("Success!", "Your results were exported to...\n" + location +"/Geometry-Calc-Results.txt")

    def areaperim(self):
        filename = filedialog.askopenfilename()
        if filename != '':
            try:
                extension = filename.find(".")
                extension = filename[extension:]
                extension = extension.replace(".",'')
                jsonexts = ("geojson","GEOJSON","GeoJSON","GeoJson","json","JSON", "JS", "js")
                if extension in jsonexts:
                    with open(filename, 'r') as fout:
                        filedata = fout.read()
                        polycount = filedata.count('"coordinates"')
                        
                        if polycount == 1:
                            index = filedata.find('"coordinates"')
                            cords = filedata.replace(filedata[:index], '')
                            index = cords.find(":")
                            cords = cords.replace(cords[:index], '')
                            index = cords.find("},")
                            cords = cords.replace(cords[index:], '')
                            cords = cords.replace(":", '')
                            cords = cords.replace("}", '')
                            cords = cords.replace("[", '')
                            cords = cords.split(']')

                            lons = []
                            lats = []

                            for i in cords:
                                try:
                                    lonlat = i.strip("'\n'")
                                    lonlat = lonlat.strip()
                                    lonlat = lonlat.strip(",")
                                    lonlat = lonlat.strip("  ")
                                    lon = float(lonlat.split(",")[0])
                                    lat = float(lonlat.split(",")[1])
                                    lons.append(lon)
                                    lats.append(lat)
                                except:
                                    continue
                           
                            laflag = lats[0]+lons[0]
                            ltflag = lats[-1]+lons[-1]
                            
                            if laflag != ltflag:
                                lons.append(lons[0])
                                lats.append(lats[0])
                            
                            lonvertices = len(lons)-1
                            latvertices = len(lats)-1
                            loncenter = sum(lons[:-1])/lonvertices                  
                            latcenter = sum(lats[:-1])/latvertices

                            pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=latcenter +lon_0=loncenter")
                            x, y = pa(lons, lats)
                            cop = {"type": "Polygon", "coordinates": [zip(x, y)]}

                            area = shape(cop).area
                            areaKM2 = area/1000000
                            perimeter = shape(cop).length             
                            perimeterKM = perimeter/1000

                            text = "\nPOLYGON MEASUREMENTS FOR: %s \n%s " % (filename,"="*45)
                            self.textbox.insert(INSERT, text + "\n")
                        
                            lcnt=0
                            for i in range(len(lons[:-1])):
                                lcnt+=1
                                text = "%d (x,y) ---> (%4.6f, %4.6f)" % (lcnt,lons[i],lats[i])
                                self.textbox.insert(INSERT, text + "\n")
                                
                            text = "\n%4d vertices were read." % (lonvertices)
                            self.textbox.insert(INSERT, text + "\n")
                            
                            text = "\nArea of the polygon is : %6.2f km2" % (areaKM2)
                            self.textbox.insert(INSERT, text + "\n")
                            
                            text = "\nPerimeter of the polygon is : %6.2f km\n%s" % (perimeterKM,"~"*45)
                            self.textbox.insert(INSERT, text + "\n")

                        elif polycount > 1:
                            polys = filedata.split('"geometry"')
                            del polys[0]
                            pcnt = 1
                            for i in polys:
                                index = i.find('"coordinates"')
                                cords = i.replace(i[:index], '')
                                index = cords.find(":")
                                cords = cords.replace(cords[:index], '')
                                cords = cords.replace(":", '')
                                cords = cords.replace("}", '')
                                cords = cords.replace("[", '')
                                index = cords.find('"type"')
                                cords = cords.replace(cords[index:], '')
                                cords = cords.replace('"', '')
                                cords = cords.replace('{', '')
                                cords = cords.split("],")

                                lons = []
                                lats = []

                                for i in cords:
                                    lonlat = i.strip("'\n'")
                                    lonlat = lonlat.strip()
                                    lonlat = lonlat.replace("  ", '')
                                    lonlat = lonlat.replace("]", '')
                                    lon = float(lonlat.split(",")[0])
                                    lat = float(lonlat.split(",")[1])
                                    lons.append(lon)
                                    lats.append(lat)

                                laflag = lats[0]+lons[0]
                                ltflag = lats[-1]+lons[-1]
                                
                                if laflag != ltflag:
                                    lons.append(lons[0])
                                    lats.append(lats[0])
                                
                                lonvertices = len(lons)-1
                                latvertices = len(lats)-1
                                loncenter = sum(lons[:-1])/lonvertices                  
                                latcenter = sum(lats[:-1])/latvertices

                                pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=latcenter +lon_0=loncenter")
                                x, y = pa(lons, lats)
                                cop = {"type": "Polygon", "coordinates": [zip(x, y)]}

                                area = shape(cop).area
                                areaKM2 = area/1000000
                                perimeter = shape(cop).length             
                                perimeterKM = perimeter/1000

                                text = "\nMEASUREMENTS FOR POLYGON:%2d FROM %s\n%s " % (pcnt,filename,"="*45)
                                self.textbox.insert(INSERT, text + "\n")
                                
                                pcnt+=1
                                lcnt=0
                                for i in range(len(lons[:-1])):
                                    lcnt+=1
                                    text = "%d (x,y) ---> (%4.6f, %4.6f)" % (lcnt,lons[i],lats[i])
                                    self.textbox.insert(INSERT, text + "\n")
                                    
                                text = "\n%4d vertices were read." % (lonvertices)
                                self.textbox.insert(INSERT, text)
                                text = "\nArea of the polygon is : %6.2f km2" % (areaKM2)
                                self.textbox.insert(INSERT, text)
                                text = "\nPerimeter of the polygon is : %6.2f km\n%s\n" % (perimeterKM,"~"*45)
                                self.textbox.insert(INSERT, text)          

                        elif polycount == 0:
                            tkMessageBox.showinfo("File Error", "Looks like there are no polygons in this file")
                            
                elif extension not in jsonexts:
                    tkMessageBox.showinfo("File Error", "Please select a GeoJSON or JSON file")
            except:
                self.quit
        elif filename == '':
            self.quit
            
    def createWidgets(self):
        self.ap = Button(self, width = 60)
        self.ap["text"] = "Select File and Calculate the Area & Perimeter of your Polygon(s)"
        self.ap["command"] = self.areaperim
        self.ap.pack(side="top", padx=5, pady=10)

        self.export = Button(self, width = 60)
        self.export["text"] = "Export Results to .TXT File"
        self.export["command"] = self.output
        self.export.pack(side="bottom", padx=5, pady=5)

        self.clear = Button(self, width = 60)
        self.clear["text"] = "Clear Contents"
        self.clear["command"] = self.cleartext
        self.clear.pack(side="bottom", padx=5, pady=5)

        self.textbox = scrolledtext.ScrolledText(self)
        self.textbox.pack(side="bottom", padx=5, pady=10)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

window = Tk()

app = Application(master=window)

window.title("GeoPython App")
window.geometry('500x500')

app.mainloop()
