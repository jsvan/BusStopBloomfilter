import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import string


def plot_masked(ax):
    """Plots the image masked outside of a circle using masked arrays"""
    # Calculate the distance from the center of the circle
    ix, iy = np.meshgrid(np.arange(100), np.arange(100))
    distance = np.sqrt((ix - 0)**2 + (iy - 0)**2)

    # Mask portions of the data array outside of the circle


def draw_circle(ax, color):
    if color=='0':
        return
    pts = np.array([[0, 0],
                    [0, 0.25],
                    [0.25, 0] ])
    p = Polygon(pts, color="black")
    ax.add_patch(p)
    pts = np.array([[1, 0],
                    [1, 0.25],
                    [0.75, 0] ])
    p = Polygon(pts, color="black")
    ax.add_patch(p)
    pts = np.array([[1, 1],
                    [1, 0.75],
                    [0.75, 1] ])
    p = Polygon(pts, color="black")
    ax.add_patch(p)
    pts = np.array([[0, 1],
                    [0, 0.75],
                    [0.25, 1] ])
    p = Polygon(pts, color='black')
    ax.add_patch(p)


def draw_top_triangle(ax, color:str):
    # All shapes on a 5x5 square
    # ax = plt.gca() PASS IN, SHARED
    if color=='0':
        return
    pts = np.array([[0, 1],
                    [1, 1],
                    [0, 0] ])

    p = Polygon(pts, facecolor="pink", edgecolor="gray")
    ax.add_patch(p)


def draw_bot_triangle(ax, color:str):
    # All shapes on a 5x5 square
    # ax = plt.gca() PASS IN, SHARED
    if color=='0':
        return
    pts = np.array([[1, 0],
                    [1, 1],
                    [0, 0] ])

    p = Polygon(pts, facecolor="lightblue", edgecolor="gray")
    ax.add_patch(p)


def draw_stripe(ax, color:bool):
    # All shapes on a 5x5 square
    # ax = plt.gca() PASS IN, SHARED
    if color=='0':
        return
    pts = np.array([[0, 0.8],
                    [0, 1],
                    [.2, 1],
                    [1, .2],
                    [1, 0],
                    [.8, 0] ])

    p = Polygon(pts, facecolor="lightyellow", edgecolor="gray" )
    ax.add_patch(p)

def draw_left_dot(ax, appear:str):
    if appear == '0':
        return
    ax.text(0.05, 0.45, '.', fontsize=40, color='black')


def draw_right_dot(ax, appear:str):
    if appear == '0':
        return
    ax.text(0.8, 0.45, '.', fontsize=40, color='black')

def draw_letter(ax, letter):
    ax.text(0.4 if len(letter) == 1 else 0.3, 0.33, letter, fontsize=40, color="black", fontdict={'family':'monospace'})

#def plot_circle(ax, )







# TODO: Left side or right side letters
# Black or LIME color
class Canvas:

    def __init__(self):
        self.lettersize = 6  # triangle, triangle, stripe, corners, leftdot, rightdot
        self.allLetters = []
        LETS = list(string.ascii_uppercase) + ['?', "\$", "*","!", "%", "@"]
        lets = list(string.ascii_lowercase) + ['??', "\$\$", "**","!!", "%%", "@@"]
        for i in range(len(lets)):
            self.allLetters.append(LETS[i])
            self.allLetters.append(lets[i])
        self.alphabetsize = len(self.allLetters) * self.lettersize
        #print(len(self.allLetters))


    def getAlphabet(self, bitarray):
        #print("Alphabet size var is", self.alphabetsize, end='\t')
        #print("My given alphabetarray is", len(bitarray))
        for i in range(len(bitarray) // self.alphabetsize+1):
            alphabet = bitarray[i * self.alphabetsize: min((i + 1) * self.alphabetsize, len(bitarray))]
            yield alphabet


    """
    alphabet is the bit string of length 35*4 = 140, representing all the info of the alphabet
    """
    def getLetter(self, alphabet):
        for i in range(len(alphabet) // self.lettersize):
            letter = alphabet[ i * self.lettersize : min((i + 1) * self.lettersize, len(alphabet))]
            yield letter, self.allLetters[i]


    def interpretAlphabet(self, alphabetarray, allLetters, numletters=8):
        try:
            n_cols = 8
            n_rows =  min(8, numletters // n_cols)
            fig, axes = plt.subplots(n_rows, n_cols)

            letters = self.getLetter(alphabetarray)

            for row_num in range(n_rows):
                for col_num in range(n_cols):
                    letterbits, lettertext = next(letters)
                    ax = axes[row_num][col_num]
                    ax.set_xticks([])
                    ax.set_xlabel(None)
                    ax.set_yticks([])
                    ax.set_xlabel(None)
                    if allLetters or sum((1 for x in letterbits if x=="1")):
                        draw_top_triangle(ax, letterbits[0])
                        draw_bot_triangle(ax, letterbits[1])
                        draw_stripe(ax, letterbits[2])
                        draw_letter(ax, lettertext)
                        draw_left_dot(ax, letterbits[4])
                        draw_right_dot(ax, letterbits[5])
                        draw_circle(ax, letterbits[3])
        except StopIteration:
            return



    # allLetters is if you want every letter to be drawn, regardless of whether it has bits flipped.
    def visualizeByteString(self, bloomstop, title='', allLetters=False):
        bitstring = ''.join((format(x, '#034b')[2:] for x in bloomstop.backend.array_))
        alphabets = self.getAlphabet(bitstring)
        #print("Total bits is", len(bitstring), end='\t')
        for i, alphabet in enumerate(alphabets):
            if len(alphabet) < 1:
                continue
            #print(f"Alphabet {i} is {len(alphabet)}", end='\t')
            #plt.figure(i + 1)
            self.interpretAlphabet(alphabet, allLetters, len(bitstring)//self.lettersize)
        plt.suptitle(title)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

