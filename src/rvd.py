#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RVD - Raman spectra based RNA Virus Detection tool

author : Sanket Desai
date   : 22/04/2020
email  : desai[dot]sanket12[at]gmail[dot]com
licence: GNU GPL (refer to README of the project for details)
"""
from __future__ import division, absolute_import, unicode_literals, print_function
from Tkinter import Tk, StringVar, DISABLED, NORMAL, END, W, E, N, S
from ttk import Frame, Label, Button, Radiobutton, Entry
import tkFileDialog
import os
import argparse
import codecs
import io
import sys
import csv
from Tkinter import Menu
from Tkinter import Toplevel
import subprocess
import spc

class ProcessSPC:
    def __init__(self, master):
        self.master = master
        self.screen1=None
        master.title("RVD")
        #mf = Frame(master, padding="20")
        master.geometry('575x300')
        #self.menu=Menu(master)
        #file_item=Menu(self.menu)

        #self.menu.add_cascade(label='File', menu=file_item)
        #file_item.add_command(label='About', command=self.about)
        #file_item.add_separator()
        #file_item.add_command(label='Exit', command=self.master.quit)
        mf=Frame(master ,padding="15")
        mf.grid(column=0, row=0, sticky=(N, W, E, S))
        mf.columnconfigure(0, weight=1)
        mf.rowconfigure(0, weight=1)
        self.infomessage = "Raman spectra based RNA Virus Detection (RVD) program\n"
        self.developer= "\nDeveloped by Sanket Desai, Dutt laboratory, TMC-ACTREC"
        self.infolabel_text=StringVar()
        self.developer_text=StringVar()
        self.proname=StringVar()
        self.message = "Enter folder containing *.SPC files"
        self.label_text = StringVar()
        self.folder = StringVar()
        #self.output_fmt = StringVar()
        self.outputdir=StringVar()
        self.prolabel= Label(mf, text="Project name")
        self.infolabel_text.set(self.infomessage)
        self.developer_text.set(self.developer)
        self.label_text.set(self.message)
        self.ilabel=Label(mf, textvariable=self.infolabel_text)
        self.developerlabel=Label(mf, textvariable=self.developer_text)
        self.label = Label(mf, textvariable=self.label_text)
        self.folder_label = Label(mf, text="Input Directory")
        self.output_folder_label=Label(mf, text="Output Directory")
        #self.output_fmt_label = Label(mf, text="Output Format")
        #self.fmt_txt = Radiobutton(mf, text="TXT", variable=self.output_fmt, value='txt')
        #self.fmt_csv = Radiobutton(mf, text="CSV", variable=self.output_fmt, value='csv')

        self.proname_entry=Entry(mf, textvariable=self.proname)
        self.folder_entry = Entry(mf, textvariable=self.folder)
        self.sel_foler = Button(mf, text="Browse", command=self.ask_dir)
        self.folder_entry2= Entry(mf, textvariable=self.outputdir)
        self.sel_foler2 = Button(mf, text="Browse", command=self.ask_odir)
        self.convert_btn = Button(mf, text="Submit", command=self.convert)
        # map on grid
        #self.menu.grid(row=0,column=0, sticky=E)
        self.ilabel.grid(row=0, column=2, sticky=E)
        self.prolabel.grid(row=2, column=1 , sticky=E)
        self.proname_entry.grid(row=2, column=2, columnspan=2, sticky= W + E)
        self.label.grid(row=3, column=2, columnspan=4, sticky=W + E)
        self.folder_label.grid(row=4, column=1, sticky=E)
        #self.output_fmt_label.grid(row=3, column=0, sticky=E)
        self.folder_entry.grid(row=4, column=2, columnspan=2, sticky=W + E)
        #self.fmt_txt.grid(row=2, column=1, sticky=W)
        #self.fmt_csv.grid(row=2, column=2, sticky=W)
        self.sel_foler.grid(row=4, column=4, sticky=W)
        self.output_folder_label.grid(row=5, column=1, sticky=E)
        self.folder_entry2.grid(row=5, column=2,columnspan=2, sticky= W + E)
        self.sel_foler2.grid(row=5, column=4, sticky=W)
        self.convert_btn.grid(row=6, column=2, columnspan=2, sticky=W + E)
        self.developerlabel.grid(row=7, column=2, sticky=E)
        for child in mf.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def convert(self):
        self.fol_val = str(self.folder.get())
        outfol_val= str(self.outputdir.get())
        if not outfol_val.endswith("/"):
            outfol_val=outfol_val+"/"
        #self.fmt_val = str(self.output_fmt.get())
        #print("About to convert {} with {} ext".format(self.fol_val, self.fmt_val))
        exten = '.csv'
        delim = ','
        flist = []
        # only directory here
        ffn = os.path.abspath(self.fol_val)
        #ffn is the input folder name
        #print(ffn)
        #sys.exit(0)
        onlyfilename=[]
        ffn=ffn+"/"
        for f in os.listdir(ffn):
            flist.append(os.path.join(ffn, f))
            onlyfilename.append(f)
        # process files
        ind=0
        for ind in range(0, len(flist)):
            fpath=flist[ind]
            fname=onlyfilename[ind]
            if fpath.lower().endswith('spc'):
                foutp = fpath[:-4] + exten
                #foutp=outfol_val+fname[:-4]+exten
                try:
                    #print(fpath, end=' ')
                    f = spc.File(fpath)
                    f.write_file(foutp, delimiter=delim)
                    #print('Converted')
                except:
                    print('Error processing %s' % fpath)
                    print(fpath)
                    print(foutp)
                    sys.exit(0)
            #else:
            #    print('%s not spc file, skipping' % fpath)
        sampleinfo={}
        testind=1
        for f in onlyfilename:
            sampleinfo[f.replace(".spc",".csv")]="test"+str(testind)
            testind=testind+1
        print(sampleinfo)
        self.csvtoldamatrix(ffn, sampleinfo, outfol_val )
    def ask_dir(self):
        self.folder.set(tkFileDialog.askdirectory())
    def ask_odir(self):
        self.outputdir.set(tkFileDialog.askdirectory())
    def csvtoldamatrix(self, filefolder, sampleinfo, outputdir):
        sampleinfomap=sampleinfo
        flist = []
        featurelist=range(600,1800)
        pnm=str(self.proname.get()).strip().replace(" ","_")
        matoutputfile=outputdir+pnm+"_ldmat.csv"
        predoutputfile=outputdir+pnm+"_prediction.csv"
        outf=open(matoutputfile,'w')
        # add all files from input file name
        outf.write("sample,")
        for f in featurelist:
            outf.write("%d," %(int(f)))
        outf.write("class\n")
        #for fn in filefolder:
        #    ffn = os.path.abspath(fn)
            # or directories
        #print(filefolder)
        #sys.exit(0)
        if os.path.isdir(filefolder):
            for f in os.listdir(filefolder):
                fpath=os.path.join(filefolder, f)
                print("processing file %s" % f)
                if fpath.lower().endswith('csv'):
                    try:
                        sample=f
                        wave=[]
                        freq=[]
                        record=[]
                        record.append(sample)
                        print(fpath)
                        with open(fpath, 'rb') as spccsv:
                            spccsvreader=csv.reader(spccsv)
                            for ssr in spccsvreader: #directly splits it according to the delimiter
                                #ssr=sr.split(',')
                                if len(ssr) == 2:
                                    wave.append(float(ssr[0]))
                                    freq.append(float(ssr[1]))
                                else:
                                    print("Error in the SPC CSV file format! Please check file: %s" %f)
                                    sys.exit(0)
                        spccsv.close()
                        avgspectra=[]
                        outf.write("%s," % sample)
                        for f in featurelist:
                            counter=0
                            sumfreq=0
                            for iw in range(0,len(wave)):
                                if wave[iw] <= f+5 and wave[iw] >= f-5:
                                    counter=counter+1
                                    sumfreq=sumfreq+freq[iw]
                            avgspectra.append(float(sumfreq/counter))
                        if len(featurelist)==len(avgspectra):
                            for a in avgspectra:
                                outf.write("%f," %(a))
                        else:
                            print("File format error!! %s" %(sample) )
                            sys.exit(0)
                        try:
                            outf.write("%s\n" %(sampleinfomap[sample]) )
                        except KeyError:
                            print("Sample class annotation not found for sample: %s" %(sample))
                            sys.exit(0)
                    except Exception as e:
                        print(e)
                        print("Contact the developer!!")
                        sys.exit(0)
                else:
                    pass
        else:
            print("Directory or files not found!!")
            sys.exit(0)
        outf.close()
        self.prediction(matoutputfile, predoutputfile)
    def prediction(self, ldainputfi, outputfi):
        cmdline="Rscript "+ os.path.dirname(os.path.abspath(sys.argv[0])) +"/predict.Rscript "+ldainputfi+" "+outputfi
        try:
            subprocess.call(cmdline, shell=True)
            print("Prediction performed for the input SPC files. Plese refer to the output file \'%s\' for results. " %outputfi)
        except:
            print(cmdline)
            sys.exit(0)

if __name__ == "__main__":
    root = Tk()
    ProcessSPC(root)
    root.mainloop()
