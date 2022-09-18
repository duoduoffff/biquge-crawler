#! /usr/bin/python3

import json, re, os
from bs4 import BeautifulSoup

from Utility import file, network

urlBase = "http://www.biqugse.com"

def genericGet(webDoctUrl):
    headers = network.headers
    webDoctPld = network.prepareGenericRequest(webDoctUrl, {}, headers, "GET")

    if(webDoctPld.status_code == 200):
        webDoct = webDoctPld.text
        
        webDoctHtml = BeautifulSoup(webDoct, "html.parser")

        return webDoctHtml
    else:
        return False

def getNovelChapterList(novelId):
    webDoctUrl = "{0}/{1}/".format(urlBase, novelId)
    webDoctHtml = genericGet(webDoctUrl)
    eligibleCells = webDoctHtml.find_all("dd")

    links = []
    for item in eligibleCells:
        link = {}
        chapterName = item.contents[0].text
        chapterLink = item.contents[0].get("href")
        link["chapterName"] = chapterName
        link["chapterLink"] = chapterLink
        links.append(link)

    links = [dict(t) for t in set([tuple(d.items()) for d in links])]

    return links

def getNovelName(novelId):
    webDoctUrl = "{0}/{1}/".format(urlBase, novelId)
    webDoctHtml = genericGet(webDoctUrl)
    if webDoctHtml is not False:
        eligibleCells = webDoctHtml.select("#info > h1")
        title = eligibleCells[0].text
        return title
    else:
        return False

def getSingleChapter(singleChapterUrl):
    url = "{0}/{1}".format(urlBase, singleChapterUrl)
    webDoctHtml = genericGet(url)
    if webDoctHtml is not False:
        eligibleCells = webDoctHtml.select("#content")
        return eligibleCells[0].text
    else:
        return False

def crawlAllChapters(novelId):
    baseDir = "novels"
    novelName = getNovelName(novelId)
    print("Novel name: {0}".format(novelName))
    os.mkdir("{0}/{1}".format(baseDir, novelName))
    allChapters = getNovelChapterList(novelId)
    for item in allChapters:
        print("Writing {0}".format(item["chapterName"]))
        content = getSingleChapter(item["chapterLink"])
        if content is not False:
            content = re.sub(r' ', "\n", content)
            content = re.sub(r'\t', "\n", content)
            file.FileOperations.writeToFile(content, "{2}/{0}/{0} - {1}.txt".format(novelName, item["chapterName"], baseDir))

if __name__ == '__main__':
    userPrompt = input("Select novel you'd like to download: ")
    novelName = getNovelName(userPrompt)
    if (novelName is not False):
        userConfirmation = input("Would you like to download {0}? (y/N)".format(novelName))
        if (userConfirmation == "Y" or userConfirmation == "y"):
            crawlAllChapters(userPrompt)
    else:
        print("Webpage not available")