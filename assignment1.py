# This is the file you will need to edit in order to complete assignment 1
# You may create additional functions, but all code must be contained within this file


# Some starting imports are provided, these will be accessible by all functions.
# You may need to import additional items
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
import re
import seaborn as sns
import nltk
from nltk.corpus import stopwords

# You should use these two variable to refer the location of the JSON data file and the folder containing the news articles.
# Under no circumstances should you hardcode a path to the folder on your computer (e.g. C:\Chris\Assignment\data\data.json) as this path will not exist on any machine but yours.
datafilepath = 'data/data.json'
articlespath = 'data/football'


def task1():
    with open(datafilepath) as datafile:
        json_file = json.load(datafile)
    return sorted(json_file["teams_codes"])


def task2():
    t2file = open("task2.csv", "w")
    with open(datafilepath) as datafile:
        json_file = json.load(datafile)
    clubs = json_file["clubs"]
    teamcode = []
    scored_by = []
    scored_against = []
    for info in clubs:
        teamcode.append(info["club_code"])
        scored_by.append(info["goals_scored"])
        scored_against.append(info["goals_conceded"])
    file = pd.DataFrame(
        {"team_code": teamcode, "goals_scored_by_team": scored_by, "goals_scored_against_team": scored_against})
    new_file = (file.sort_values(by="team_code", ascending=True)).set_index("team_code")
    new_file.to_csv("task2.csv")
    t2file.close()
    return


def task3():
    t3file = open("task3.csv", "w")
    filename = []
    totalgoals = []
    for i in range(1, 266):
        if i < 10:
            filenum = "00" + str(i)
        elif i < 100:
            filenum = "0" + str(i)
        else:
            filenum = str(i)
        filepath = f'{articlespath}/{filenum}.txt'
        new_scorelist = []
        with open(filepath) as file:
            filename.append(f'{filenum}.txt')
            score_list = re.findall(r'[^\d](\d{1,2}-\d{1,2})[^\d]', file.read())
            if len(score_list) == 0:
                new_scorelist.append(0)
            for score in score_list:
                scores = score.split("-")
                new_scorelist.append((int(scores[0]) + int(scores[1])))
            goals = sorted(new_scorelist)[-1]
            totalgoals.append(goals)
    file = (pd.DataFrame({"filename": filename, "total_goals": totalgoals})).set_index("filename")
    file.to_csv("task3.csv")
    t3file.close()
    return


def task4():
    t3file = pd.read_csv("task3.csv")
    plt.boxplot(t3file["total_goals"])
    plt.title("Total goals reported in articles")
    plt.ylabel("Total goals in the match")
    plt.savefig("task4.png")
    return


def task5():
    t5file = open("task5.csv", "w")
    clubname = []
    mentionlist = []
    with open(datafilepath) as datafile:
        json_file = json.load(datafile)
    clubs = json_file["clubs"]
    for info in clubs:
        clubname.append(info["name"])
    for club in clubname:
        mention = 0
        for i in range(1, 266):
            if i < 10:
                filenum = "00" + str(i)
            elif i < 100:
                filenum = "0" + str(i)
            else:
                filenum = str(i)
            filepath = f'{articlespath}/{filenum}.txt'
            with open(filepath) as file:
                mentions = re.findall(f'({club})', file.read())
                if len(mentions) != 0:
                    mention += 1
        mentionlist.append(mention)
    file = ((pd.DataFrame({"club_name": clubname, "number_of_mentions": mentionlist})).sort_values(by="club_name",
                                                                                                   ascending=True)).set_index(
        "club_name")
    file.to_csv("task5.csv")
    t5file.close()
    bar_data = pd.read_csv("task5.csv")
    plt.bar(bar_data["club_name"], bar_data["number_of_mentions"])
    plt.xticks(rotation=50)
    plt.xlabel("Club")
    plt.ylabel("Number of mentions")
    plt.title("Number of articles mentioning each club")
    plt.savefig("task5.png")
    return


def task6():
    t5file = pd.read_csv("task5.csv")
    t2file = pd.read_csv("task2.csv")
    heatmap_array = []
    for club1 in t5file["club_name"]:
        heatmap_row = []
        for club2 in t5file["club_name"]:
            mention_both = 0
            for i in range(1, 266):
                if i < 10:
                    filenum = "00" + str(i)
                elif i < 100:
                    filenum = "0" + str(i)
                else:
                    filenum = str(i)
                filepath = f'{articlespath}/{filenum}.txt'
                with open(filepath) as file:
                    a = file.read()
                    mentions1 = re.findall(f'({club1})', a)
                    mentions2 = re.findall(f'({club2})', a)
                if len(mentions1) != 0 and len(mentions2) != 0:
                    mention_both += 1
            if club1 == "West Ham United" and club2 == "West Ham United":
                similarity = 0
            else:
                c1 = t5file.loc[t5file["club_name"] == club1, "number_of_mentions"]
                c2 = t5file.loc[t5file["club_name"] == club2, "number_of_mentions"]
                similarity = (2 * mention_both) / (c1.to_numpy()[0] + c2.to_numpy()[0])
            heatmap_row.append(similarity)
        heatmap_array.append(heatmap_row)
    df = pd.DataFrame(heatmap_array, index=t2file["team_code"], columns=t2file["team_code"])
    sns.heatmap(df)
    plt.title("Comparing clubs commonly mentioned in the same articles")
    plt.savefig("task6.png")
    return


def task7():
    t2file = pd.read_csv("task2.csv")
    t5file = pd.read_csv("task5.csv")
    plt.scatter(t2file["goals_scored_by_team"], t5file["number_of_mentions"])
    plt.title("Goals scored by team VS number of mentions")
    plt.xlabel("Goals scored by team")
    plt.ylabel("Number of mentions")
    plt.savefig("task7.png")
    return


def task8(filename):
    with open(filename) as f:
        new_file = re.sub(r'[\W\s\d]', " ", f.read())
    x = new_file.lower()
    wordList = nltk.word_tokenize(x)
    stopWords = set(stopwords.words('english'))
    final = []
    for word in wordList:
        if word not in stopWords and len(word) != 1:
            final.append(word)
    return final


def task9():
    # Complete task 9 here
    return