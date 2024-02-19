from tkinter import *
from main import top200_random
from main import poster
from main import movie_finder
from PIL import ImageTk

global nb_coeur
nb_coeur = 0
global nb_prec
nb_prec = 0
global nom_film
global fenetre1


# 2e technique en nettoyant la fenetre#
def fen2():
    for c in fenetre1.winfo_children():
        c.destroy()

    fenetre1.title("Fenêtre 2")

    # Background
    #picture = Label(fenetre1, image=imagebg)
    #picture.place(relx=0.5, rely=0.5, anchor=CENTER)

    fenetre1.config(bg="#ffffff")
    #fonction quib donne un film random et qui retourne le film
    #Image aléatoire
    nom_film = top200_random()
    print(nom_film)
    imagealeat = ImageTk.PhotoImage(poster(nom_film))
    
    # Bouton like
    Button(image=image_like,highlightthickness=0,bd=0, command=lambda: incre(nom_film)).place(relx=0.7, rely=0.9, anchor=CENTER)
    # Bouton croix
    Button(image=image_croix,borderwidth=0,highlightthickness=0, command=fen2).place(relx=0.3, rely=0.9, anchor=CENTER)

    aleat = Label(fenetre1, image=imagealeat,borderwidth=0)
    aleat.place(relx=0.5, rely=0.3, anchor=CENTER)
    label = Label(fenetre1, text=nom_film, font=("Ariel", 40, "italic", "bold",), fg='#ff655b', bg='#ffffff')
    label.place(relx=0.5, rely=0.7, anchor=CENTER)
    fen2.mainloop()

def incre(nom_film):
    global nb_coeur
    nb_coeur += 1
    tab[nb_coeur-1]=nom_film
    if nb_coeur == 3:
        nb_coeur = 0
        final()
    else:
        fen2()

def final():
    tab2 = [None]*3
    for c in fenetre1.winfo_children():
        c.destroy()

    fenetre1.title("Final")
    fenetre1.config(bg="#ffffff")

    label = Label(fenetre1, text="IT'S A", font=("Ariel", 50, "italic", "bold",), fg='#48e8c7', bg='#ffffff')
    label.pack()

    label = Label(fenetre1, text="MATCH", font=("Ariel", 100, "italic", "bold",), fg='#48e8c7', bg='#ffffff')
    label.pack()
    
    print(tab)
    tab2 = movie_finder(tab[0],tab[1],tab[2])
    print(tab2)
    
    imagematch1 = ImageTk.PhotoImage(poster(tab2[0]))
    imagematch2 = ImageTk.PhotoImage(poster(tab2[1]))
    imagematch3 = ImageTk.PhotoImage(poster(tab2[2]))

    # Film final
    match1 = Label(fenetre1, image=imagematch1)
    match1.place(relx=0.2, rely=0.5, anchor=CENTER)
    label = Label(fenetre1, text=tab2[0], font=("Ariel", 15, "italic", "bold",), fg='#fd297b', bg='#ffffff')
    label.place(relx=0.2, rely=0.8, anchor=CENTER)

    match2 = Label(fenetre1, image=imagematch2)
    match2.place(relx=0.5, rely=0.5, anchor=CENTER)
    label = Label(fenetre1, text=tab2[1], font=("Ariel", 15, "italic", "bold",), fg='#ff5864', bg='#ffffff')
    label.place(relx=0.5, rely=0.8, anchor=CENTER)

    match3 = Label(fenetre1, image=imagematch3)
    match3.place(relx=0.8, rely=0.5, anchor=CENTER)
    label = Label(fenetre1, text=tab2[2], font=("Ariel", 15, "italic", "bold",), fg='#ff655b', bg='#ffffff')
    label.place(relx=0.8, rely=0.8, anchor=CENTER)

    #Bouton retour
    suiv1 = Button(fenetre1, borderwidth=5, text="RECOMMENCER", font=("Arial", 15, "bold",), bg="#FF5864", fg="white",command=fen2)
    suiv1.place(relx=0.5, rely=0.9, anchor=CENTER)
    final.mainloop()



#Fonction main.................................................

# Créer fenetre 1
fenetre1 = Tk()
fenetre1.title("Fenêtre 1")
fenetre1.config(bg="white")

# Dimensions fenetre
fenetre1.minsize(1200,950)
fenetre1.geometry("1200x950")

# Logo image
logo = PhotoImage(file="logo_doc.png")

# Image like et croix
image_like = PhotoImage(file="coeur.png")
image_croix = PhotoImage(file="croix.png")
# Image film match


# Logo à mettre ici
picture = Label(fenetre1, image=logo, borderwidth=0)
picture.place(relx=0.5, rely=0.2, anchor=CENTER)

# Bouton pour clear la page
suiv1 = Button(fenetre1, borderwidth=5, text="START", font=("Arial", 15, "bold",), bg="#FF5864", fg="white",
                   command=fen2)
suiv1.place(relx=0.5, rely=0.5, anchor=CENTER)

tab=[None]*3


fenetre1.mainloop()