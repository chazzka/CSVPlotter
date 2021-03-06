import glob
import os
import subprocess
import sys


print("installing requirements...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib==3.3.1'], stdout=open(os.devnull, 'wb'))
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'plotly'], stdout=open(os.devnull, 'wb'))
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy==1.19.3'], stdout=open(os.devnull, 'wb'))

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print("installed packages: ")
print(installed_packages)

import csv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

from tkinter import *
from tkinter.filedialog import askdirectory
from pathlib import Path

import itertools
import threading
import time


def jednicka():
    mediany = []
    maxy = []
    miny = []
    meany = []
    deviace = []
    nazvy_funkci = []

    polePrumeruVsechFilu = []
    poleIndexuGlobal = []
    # start - make user select folders
    Tk().withdraw()
    openPath = askdirectory(title='Select folder with csv files')
    savePath = askdirectory(title='Select where to save results')

    # long process - animate loading
    done = False

    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rgeneruji vysledky ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rJsem hotov!     ')

    t = threading.Thread(target=animate)
    t.start()

    folder_path = openPath
    for filename in glob.glob(os.path.join(folder_path, '*.csv')):
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            poleCSV = []

            for radek in spamreader:
                poleCSV.append(radek)

        poleHodnotSloupcu = []

        polePrumeru = []
        for radek in poleCSV:
            radekPrumeru = radek.copy()
            radekPrumeru.reverse()
            radekPrumeru.pop()
            tempRadek = np.array(radekPrumeru)
            ciselnyTempRadek = tempRadek.astype(np.float)
            polePrumeru.append(min(ciselnyTempRadek))

        polePrumeruVsechFilu.append(polePrumeru)
        pocetSloupcu = len(poleCSV[0])
        for i in range(0, pocetSloupcu):
            poleSloupce = []
            for radek in poleCSV:
                ciselnaHodnota = float(radek[i])
                poleSloupce.append(ciselnaHodnota)
            poleHodnotSloupcu.append(poleSloupce)

        name_of_file = filename.split('\\')[1].split('.')[0]
        poleIndexu = poleHodnotSloupcu.pop(0)
        poleIndexuGlobal = poleIndexu.copy()
        poleVysledku = []

        Path(savePath + "/imgresults").mkdir(parents=True, exist_ok=True)
        plt.figure()
        for i in poleHodnotSloupcu:
            plt.plot(poleIndexu, i)
            plt.yscale('log')
            plt.xlabel('FES')
            plt.ylabel('Cost')
            plt.title(name_of_file)
            plt.savefig(savePath + '/imgresults/' + name_of_file)
            poleVysledku.append(i)
        plt.close()

        lastResults = []
        for run in poleHodnotSloupcu:
            lastResults.append(run[len(run) - 1])

        mediany.append(np.median(lastResults))
        maxy.append(np.max(lastResults))
        miny.append(np.min(lastResults))
        meany.append(np.mean(lastResults))
        deviace.append(np.std(lastResults))
        nazvy_funkci.append(name_of_file)

        Path(savePath + "/imgresults/prumery").mkdir(parents=True, exist_ok=True)
        # toto je jedno csv:
        plt.figure()
        plt.plot(poleIndexu, polePrumeru)
        plt.xlabel('FES')
        plt.ylabel('Cost')
        plt.yscale('log')
        plt.title(name_of_file + 'prumer')
        plt.savefig(savePath + '/imgresults/prumery/' + name_of_file)
        plt.close()

    fig = go.Figure(data=[go.Table(header=dict(values=['Nazev funkce', 'Median', 'Max', 'Min', 'Mean', 'STADEV']),
                                   cells=dict(values=[nazvy_funkci, mediany, maxy,
                                                      miny, meany,
                                                      deviace]))
                          ])

    Path(savePath + "/statresults").mkdir(parents=True, exist_ok=True)
    fig.write_html(savePath + "/statresults/statistika.html")

    plt.figure()
    if len(polePrumeruVsechFilu) > 1:
        for i in polePrumeruVsechFilu:
            plt.plot(poleIndexuGlobal, i)
            plt.xlabel('FES')
            plt.ylabel('Cost')
            plt.yscale('log')
            plt.title('prumery kombinace')
            plt.legend(['BC', 'C1', 'C3', 'C2', 'H1', 'H3', 'H2', 'Lun', 'Ros', 'RotSch'])
            plt.savefig(savePath + '/imgresults/prumery/prumeryJedneDimenze')

    plt.close()

    done = True


def dvojka():
    print("toto je dvojka")
    Tk().withdraw()
    open_path = askdirectory(title='Vyber slozky se stejnymi dimenzemi')
    save_path = askdirectory(title='Vyber kam se ulozi vysledky')
    #for testing
    #open_path = "C:/Users/admin/Documents/csv/10D"
    #save_path = "C:/Users/admin/Documents/grafy3"
    
    
    single_dimension_folders = []
    algnames = []
    for subdir, dirs, files in os.walk(open_path):
        for s in dirs:
            # složky s csvečky
            first = s
            algnames.append(first)
            second = os.path.join(subdir)
            glue = second + "/" + first
            single_dimension_folders.append(glue)

    prumery_vsech_algoritmu = []
    pole_nazvu_ke_slouceni = []
    # do for each folder in single_dimension_folders
    for folder_path in single_dimension_folders:
        prumery_jedne_slozky = []
        pole_nazvu = []
        for filename in glob.glob(os.path.join(folder_path, '*.csv')):
            with open(filename, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';')
                csv_as_array = []
                pole_nazvu.append(filename.split('\\')[1].split('.')[0])
                # NEAPENDUJ PRVNICH 100
                for i in range(0,100):
                    next(spamreader, None)

                for radek in spamreader:
                    csv_as_array.append(radek)
                        

                polePrumeru = []
                for radek in csv_as_array:
                    radek_prumeru = radek.copy()
                    radek_prumeru.reverse()
                    radek_prumeru.pop()
                    temp = np.array(radek_prumeru)
                    ciselny = temp.astype(np.float)
                    polePrumeru.append(min(ciselny))
                prumery_jedne_slozky.append(polePrumeru)
        prumery_vsech_algoritmu.append(prumery_jedne_slozky)
        pole_nazvu_ke_slouceni.append(pole_nazvu)

    hotove_nazvy = []
    #udelej si pole nazvu, pomuze ti jmenna konvence csveček
    if len(pole_nazvu_ke_slouceni) > 0:
        for nazev in pole_nazvu_ke_slouceni[0]:
            hotove_nazvy.append(nazev.split("_")[1])
    
    # data ready, ted grafy
    # zjisti který je největší
    best_len = 0
    for slozka_s_algoritmem in prumery_vsech_algoritmu:
        if len(slozka_s_algoritmem[0]) > best_len:
            best_len = len(slozka_s_algoritmem[0])

    res = zip(*prumery_vsech_algoritmu)
    res = tuple(res)
    print(hotove_nazvy)
    Path(save_path + "/imgresults/combine").mkdir(parents=True, exist_ok=True)
    plt.figure()
    if len(prumery_vsech_algoritmu) > 1:
        iterator = 0
        for dvojicka in res:
            for n in range(0,len(prumery_vsech_algoritmu)):
                vypocet_array = np.array(range(0, len(dvojicka[n])))
                konstanta = best_len / len(dvojicka[n])
                x_osa = np.dot(vypocet_array, konstanta)
                plt.plot(x_osa, dvojicka[n])
            plt.legend(algnames)
            plt.xlabel('FES')
            plt.ylabel('minCost')
            plt.title(hotove_nazvy[iterator])
            plt.savefig(save_path + '/imgresults/combine/' + hotove_nazvy[iterator])
            iterator += 1
            plt.close()

root = Tk()
i = IntVar()
j = IntVar()


def click_me():
    if i.get() == 1:
        jednicka()
    if j.get() == 1:
        dvojka()


c = Checkbutton(root, text="CSVčka stejné dimenze do grafu", variable=i)
c.pack()

a = Checkbutton(root, text="Průměry stejné dimenze více algoritmů do jednoho", variable=j)
a.pack()

b = Button(root, text="START", command=click_me)
b.pack()

root.mainloop()
