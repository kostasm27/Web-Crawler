import ast
import io
from urllib.parse import urlsplit
import re
import Project
from collections import deque
import concurrent.futures
import time

start = time.perf_counter()
IndexerFile = "DictionaryFile.txt"


def Create_Indexer(Dict, RestartValue):
    Dictionary = {}
    counter = 1
    for Text in Dict:
        String = Dict.get(Text).split()
        for (Number, Word) in enumerate(String):
            if Word not in Dictionary:
                Dictionary.setdefault(Word, [])
                Dictionary[Word].append(1)  # arxikopoise tis fores pou uparxei sto doc #Dictionary[Word[1]]
                # Dictionary[Word].append(["Doc" + str(counter),ενουμερατε Number + 1])
                Dictionary[Word].append(["Doc" + str(counter), 1])
            else:
                try:
                    # if Dictionary[Word][len(Dictionary[Word])-1][0] == "Doc" + str(counter):
                    #     Dictionary[Word][len(Dictionary[Word])-1].append(Number + 1)
                    # elif Dictionary[Word][counter][0] == "Doc" + str(counter):
                    #     Dictionary[Word][counter].append(Number + 1)
                    if Dictionary[Word][len(Dictionary[Word]) - 1][0] == "Doc" + str(counter):
                        Dictionary[Word][len(Dictionary[Word]) - 1][1] += 1
                    elif Dictionary[Word][counter][0] == "Doc" + str(counter):
                        Dictionary[Word][counter][1] += 1
                except IndexError:
                    Dictionary[Word][0] += 1
                    Dictionary[Word].append(["Doc" + str(counter), 1])
                    # Dictionary[Word].append(["Doc" + str(counter), Number + 1])
        counter += 1
    counter -= 1
    if RestartValue:
        with open("DictionaryFile.txt", 'r') as DictFile:
            LenOfDict = DictFile.readlines()
        MainDictionary = {}
        Size = int(LenOfDict[0].replace('\n', ''))
        counter += Size
        Temp = ''
        for (Number, Word) in enumerate(LenOfDict):
            if (Number + 1) % 3 == 0 and Number > 1:
                Temp = Word.replace('\n', '')
            elif Number % 3 == 0 and Number > 1 and Word != '\n':
                Word = Word.replace("\n", '')
                MainDictionary[Temp] = ast.literal_eval(Word)
        # tora exo to Main Dick
        # kai to kainourgio apo ton neo crawl
        # opote prepei na do an exoun vrethei lexeis sto kainourgio pou den iparoun sto palio
        for Word in Dictionary:
            if Word not in MainDictionary:
                MainDictionary.setdefault(Word, [])
                MainDictionary[Word].append(Dictionary[Word][0])
            else:
                MainDictionary[Word][0] += Dictionary[Word][0]
            for i in range(1, len(Dictionary[Word])):
                Dictionary[Word][i][0] = "Doc" + str(Size + int(Dictionary[Word][i][0].replace("Doc", '')))
                MainDictionary[Word].append(Dictionary[Word][i])
    # xrisimopoihthike mono stin proti fora gia na dimiourgithei o arxikos indexer
    with io.open(IndexerFile, 'w', encoding="utf-8") as f:
        f.write(str(counter) + '\n')
        if not RestartValue:
            for i in Dictionary:
                f.write("\n")
                f.write(i + '\n')
                f.write(str(Dictionary.get(i)))
                f.write('\n')
        else:
            for i in MainDictionary:
                f.write("\n")
                f.write(i + '\n')
                f.write(str(MainDictionary.get(i)))
                f.write('\n')


def Create_Threads(Link_List, Crawled, DictionaryForIndexer, Main_Link, Number_Of_Links, Number_of_Threads):
    with concurrent.futures.ThreadPoolExecutor() as Thread:
        for _ in range(Number_of_Threads):
            Thread.submit(BFS_Crawler, Link_List, Crawled, DictionaryForIndexer, Main_Link, Number_Of_Links)
    return


def BFS_Crawler(Link_List, Crawled, DictionaryForIndexer, Main_Link, Number_Of_Links):
    Link_Path = set()
    Link_Path.add(str(urlsplit(Main_Link).path))
    while len(Crawled) < Number_Of_Links:
        New_Link = Link_List.popleft()
        if New_Link not in Crawled:
            if urlsplit(New_Link).path is not None and str(urlsplit(New_Link).path) not in Link_Path:
                Link_Path.add(str(urlsplit(New_Link).path))
                html_data = Project.Get_data(New_Link)
                if html_data is not None and Project.IsEnglish(html_data) is not None:
                    Temp = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_data)
                    DictionaryForIndexer = Project.Get_Dictionary(DictionaryForIndexer, html_data, New_Link)
                    # olo vazo stin Link List links mexri na teleiosoun
                    Link_List.extend(deque(Temp))
                    Crawled.add(New_Link)
                    print(f"Len of Cralwled links {len(Crawled)}")
                    if len(Crawled) >= Number_Of_Links:
                        return
    return


def Crawler_Function(Main_Link, Number_Of_Links=200, RestartValue=0, Number_of_Threads=8):
    DictionaryForIndexer = {}
    Crawled = [Main_Link]
    Project.Restart_Files(RestartValue)
    html = Project.Get_data(Main_Link)
    if not Project.Is_Html_None(html):
        # H arxiki lista pou exei ola ta links apo tin afetiria mas
        Link_List = deque(set(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)))
        # Elegxo an to link einai Crawled diladi exei ginei eggrafi sto Paragraph File
        DictionaryForIndexer = Project.Get_Dictionary(DictionaryForIndexer, html, Main_Link)
        Create_Threads(Link_List, set(Crawled), DictionaryForIndexer, Main_Link, Number_Of_Links, Number_of_Threads)
        # polla links uparxoun ston crawler parolauta mpainoun #pali eno to elegxo
        Project.Write_The_Paragraphs_And_Urls(DictionaryForIndexer)
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')
    Create_Indexer(DictionaryForIndexer, RestartValue)
