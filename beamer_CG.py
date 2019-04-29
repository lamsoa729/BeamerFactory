#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import sys
import os
# Testing
import pdb
# import time, timeit
# import line_profiler
# Analysis
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pandas as pd
import yaml
import re
# from math import *
# Speed
# from numba import jit
# Other importing
# sys.path.append(os.path.join(os.path.dirname(__file__), '[PATH]'))

#  TODO: Add scripts to path <20-10-18, ARL> #
#        Add checking to filenames in tex file
#        Allow for insertion of new images without messing up tex file
#        Search for end of document
#        See if a tex file has always already been created


"""@package docstring
File: beamer_CG.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description: Make a beamer presentation tex file based off the image
files in the folder.
"""

bmr_hdr = """
\\documentclass{{beamer}}
\\usepackage{{lmodern}}
\\usetheme{{CambridgeUS}}
\\usecolortheme{{spruce}}

\\title[]{{{}}}
\\subtitle{{}}
\\author{{Adam Lamson}}
\\institute[CU Boulder]{{University of Colorado Boulder}}
\\date[\\today]{{\\today}}

\\begin{{document}}

\\begin{{frame}}
\\titlepage
\\end{{frame}}

\\begin{{frame}}[t]{{Outline}}
    \\tableofcontents
\\end{{frame}}

"""

bmr_frame = """
\\begin{{frame}}[t]{{{1}}}
  \\begin{{figure}}[htpb]
    \\centering
    \\includegraphics[width=0.8\linewidth]{{{0}}}
    \\caption{{{1}}}
    \\label{{fig:{0}}}
  \\end{{figure}}
\\end{{frame}}
"""

bmr_ftr = """
\\end{document}
"""


class BeamerGenerator(object):

    """!Code generator object for making or modifying beamer presentations."""

    def __init__(self, filename):
        """! Initialize BeamerGenerator object with filename

        @param filename: Name of tex file to be created

        """
        if '.tex' in filename:
            self._filename = filename
            self._title = filename.replace('.tex', '')
            print("Title of presentation is", self._title.replace("_", " "))
        else:
            self._title = filename
            self._filename = filename + '.tex'
            print("Filename is", self._filename)
        # Check to see if filename or filename.tex exists
        if os.path.exists(self._filename):
            with open(self._filename) as tex_file:
                self._latex_str = tex_file.read()
        else:
            self._latex_str = ''
            # self._latex_str =

    def MakeTexStr(self):
        """!Put together string to be read out to file
        @return: void, change _latex_str to compilable string for beamer
        beamer presentations.

        """
        if self._latex_str == '':
            self._latex_str += bmr_hdr.format(
                self._filename.replace('.tex', ''))
        else:
            # Get rid of ftr so new images maybe added
            self._latex_str = self._latex_str.split(bmr_ftr)[0]
        self.AddImageFrames()
        # print self._latex_str
        self._latex_str += bmr_ftr

    def WriteTexStr(self):
        """!Save _latex_str to a file so it can be compiled into a presentation
        @return: void, makes a file in the current directory of filename

        """
        with open(self._filename, 'w') as texf:
            texf.write(self._latex_str)

    def CollectImageFilenames(self):
        """!Make a list of names of all image files in current directory.
        Image files include .jpg, .png, .pdf(excluding _filename.pdf).
        @return: list of image file names

        """
        # Match all image extensions but not the filenmae of the of beamer pdf
        regex_img = re.compile(
            r'^(?!{}).*\.(jpg|png|pdf)'.format(self._filename.replace('.tex', '')))
        # regex_img = re.compile(r'^(?!test)'.format(self._filename.replace('.tex', '')))
        files = [f for f in os.listdir(os.getcwd())
                 if regex_img.search(f)]
        return files

    def AddImageFrames(self):
        """!Add frames with figures of images collected from CollectImageFilenames
        @return: void, Modifies _latex_str

        """
        img_lst = self.CollectImageFilenames()
        for img in img_lst:
            img_exist_ptrn = re.compile(r'.*({}).*'.format(img))
            if not img_exist_ptrn.search(self._latex_str):
                self._latex_str += bmr_frame.format(img, img.replace('_', ' '))
                print("Added image {}.".format(img))


##########################################
if __name__ == "__main__":
    bmrGC = BeamerGenerator(sys.argv[1])
    bmrGC.MakeTexStr()
    bmrGC.WriteTexStr()
