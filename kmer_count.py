#! /usr/bin/python
from sys import argv 
import os
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, output_file, show

script, readfolder, kmer_size = argv

oup_gen = open("generators","w")

readfiles = os.listdir(readfolder)

for inl in readfiles:
 if inl.endswith((".fq",".fastq",".fa",".fasta")):
     oup_gen.write("cat %s/%s\n"%(readfolder,inl))
 elif inl.endswith((".fq.gz",".fastq.gz",".fa.gz",".fasta.gz",".fq.gzip",".fastq.gzip",".fa.gzip",".fasta.gzip")):
     oup_gen.write("zcat %s/%s\n"%(readfolder,inl))
 else:
     pass

oup_gen.close()
kmer_size = 31
os.system("jellyfish count -m %s -s 100M -t 8 -C -g generators -G 2"%(kmer_size))
os.system("jellyfish histo mer_counts.jf > histo-kmer%s.txt"%kmer_size)

jelly_out = open("histo-kmer%s.txt"%kmer_size,"r")
jelly_data = [line[:-1].split(" ") for line in jelly_out]

plot_data = []

for j in jelly_data: #filter to scale the plot (remove very long tail of high freq kmer)
    if (int(j[1]) > 5):# value chosen arbitrarily
        plot_data.append(j)
    else:
        pass
        
x_data = [int(i[0]) for i in plot_data]
y_data = [int(i[1]) for i in plot_data]
TOOLTIPS = [("Frequency", "$x{0}"),("Count","$y{0}")]
output_file("k%s-frequency-plot.html"%kmer_size)

# create a new plot with a title and axis labels
p = figure(width = 800, height= 800, title="k-mer frequencies", x_axis_label='Frequency', tooltips=TOOLTIPS, y_axis_label='Count',x_range=(0,max(x_data)),y_range=(0,1.1*max(y_data[5:])))

# add a line renderer with legend and line thickness
p.line(x_data[5:], y_data[5:], legend="k-mer size = %s"%kmer_size, line_width=2)

# show the results
show(p)
  
