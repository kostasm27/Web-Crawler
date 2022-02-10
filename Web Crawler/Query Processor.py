import ast
import math
from tkinter import *

# import ast
#
# window = Tk()
# window.title("Query Processor")
# window.geometry('650x350')
# L = Label(window, text="what do you want to find? ", font=("Arial", 18))
# L.grid(column=0, row=0)
# Q = Entry(window, width=20)
# Q.focus()
# Q.grid(column=1, row=0)
# Label = Label(window, text="How many documents do you want? ", font=("Arial", 18))
# Label.grid(column=0, row=1)
# text = Entry(window, width=20)
# text.focus()
# text.grid(column=1, row=1)
#
#
# def clicked():
#     global k
#     global Query
#     temp = str(Q.get()).replace(",", " ").split()
#     # na valo orio xaraktiron
#     # na afaireso oti den xreiazetai kirios simeia stixis
#     Query = temp # bike,coffee
#     k = text.get()
#     window.destroy()
#
#
# buttonOk = Button(window, text="Ok", command=clicked)
# buttonOk.grid(column=2, row=1)
# window.mainloop()
#
Query = ["bike", "the"]
with open("DictionaryFile.txt", 'r') as DictFile:
    LenOfDict = DictFile.readlines()
MainDictionary = {}
Size = int(LenOfDict[0].replace('\n', ''))
Temp = ''
for (Number, Word) in enumerate(LenOfDict):
    if (Number + 1) % 3 == 0 and Number > 1:
        Temp = Word.replace('\n', '')
    elif Number % 3 == 0 and Number > 1 and Word != '\n':
        Word = Word.replace("\n", '')
        MainDictionary[Temp] = ast.literal_eval(Word)

with open("Paragraph File.txt", "r") as Pa:
    PAsize = Pa.readlines()

with open("Url_File.txt", "r") as U:
    Urls = U.readlines()

IDFt = {}
WTFtd = {}
WTFtq = []
for i in Query:
    if i not in MainDictionary:
        print(f"The word: {i} does not exist!")
    else:
        TimesInDocs = MainDictionary[i][0]
        IDFt[i] = [math.log(Size / (1.0 + TimesInDocs))]
for i in Query:
    WTFtd.setdefault(i, [])
    for j in range(1, len(MainDictionary[i])):
        Doc = int(str(MainDictionary[i][j][0]).replace('Doc', ''))
        WTFtd[i].append([Doc, 1 + math.log(int(MainDictionary[i][j][1]))])

CosineSimilarrityDoc = {}
counter = 0
for word in Query:
    for j in range(0, len(WTFtd[word])):
        counter = WTFtd[word][j][0]
        if counter not in CosineSimilarrityDoc:
            CosineSimilarrityDoc[counter] = (float(WTFtd[word][j][1] * IDFt[word][0]))
        else:
            CosineSimilarrityDoc[counter] += float(WTFtd[word][j][1] * IDFt[word][0])
for i in CosineSimilarrityDoc:
    j = PAsize.index(Urls[i - 1])
    doc = PAsize[j + 1].split()
    if len(doc) == 0:
        print(f"doc : {i - 1}  row paragraph {j + 1}  ")
    CosineSimilarrityDoc[i] = float(CosineSimilarrityDoc[i] / len(doc))

sorted_Cosine = sorted(CosineSimilarrityDoc.items(), key=lambda x: x[1], reverse=True)
k = 10
CorrectUrls = []
window = Tk()
window.title(f"results for {Query}: ")
window.geometry('900x700')
window.configure(background="light green")
la = Label(text="Welcome to....", font=("MV Boli", 18))
la.configure(background="light green")
la.place(height=200,width=550)
icon = PhotoImage(file="E:\csd\Ανάκτηση Πληροφορίας\ErgasiaAnaktisi")
icon = icon.subsample(5,5)
label = Label(window, image=icon)
label.configure(background="light green")
label.pack()
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)
canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)
canvas.configure(background="light green")
scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
second_frame = Frame(canvas)
second_frame.configure(background="light green")
canvas.create_window((0, 0), window=second_frame, anchor="nw")
Buttons = []

for i in range(k):
    var = IntVar()
    chk = Checkbutton(second_frame, text="Is this website relevant to your question? \n" + str(
        PAsize[PAsize.index(Urls[sorted_Cosine[i][0] - 1])]), variable=var, font=("MV Boli", 18),
                      background="light green")
    chk.pack(side="top")
    Buttons.append(var)


def clicked():
    window.destroy()
    for x in range(k):
        print(Buttons[x].get())


btn = Button(second_frame, text="Ok", font=("MV Boli", 20), background="light gray", command=clicked)
btn.pack(fill=BOTH)
btn2 = Button(second_frame, text="Quit", font=("MV Boli", 20), background="light gray", command=clicked)
btn2.pack(fill=BOTH)

# na mpoun ola terma aristera
# na diorthosoume ta buttons na mpoun dipla dipla
# na paixoume me ta xromata
# na doume giati exei lag sto scroll
#

window.mainloop()
