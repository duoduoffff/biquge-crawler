#! /usr/bin/python3
# Applies to m.diyibanzhu.buzz

import bs4

def metadata():
    name = "一点斑竹移动视图适配"
    compatDomain = "m.diyibanzhu.buzz"
    protocol = "https"
    author = "notRachel"
    authorEmail = "florescence_hi@aliyun.com"
    splitChapterList = True # Whether the website shows chapter-indexes of a novel in multiple pages
    mobileLayout = True # This spec is now only for statistical purposes

    return {"name": name,
            "compatDomain": compatDomain,
            "author": author,
            "authorEmail": authorEmail,
            "protocol": protocol,
            "splitChapterList": splitChapterList,
            "mobileLayout": mobileLayout
            }

def cutNovelIdImpl(novelId):
    if isinstance(novelId, str) and novelId.isdigit():
        if(len(novelId)>2):
            return "{0}/{1}".format(novelId[:2], novelId)
        else:
            return novelId
    else:
        return ""

def getChapterListsPageCountImpl(containingString):
    # If website splits chapter-indexes in multiple pages, here is a function to get the page count of chapter indexes
    # (第14/14页)当前20条/页
    allPageString = containingString.split("/")[1]
    allPageString = allPageString.split(")")[0]
    curPageString = containingString.split("/")[0]

    curPage = ""
    for char in curPageString:
        if(char.isdigit()):
            curPage += char

    pageCt = ""
    for char in allPageString:
        if(char.isdigit()):
            pageCt += char

    if pageCt.isdigit() and curPage.isdigit():
        return {"cur": int(curPage), "total": int(pageCt)}
    else:
        raise Exception("Page count validation failed!")

def getChaptersOnPage(html):
    chaptersOnPage = []
    chapterList = html.select(".chapters")[0].contents
    pageCtStr = html.select(".page")[1].text
    pageCt = getChapterListsPageCountImpl(pageCtStr)
    chaptersOnPage.append(pageCt)
    for chapter in chapterList:
        if(isinstance(chapter, bs4.element.Tag)):
            link = chapter.find("a")
            n = link.get_text()
            l = link.get("href")
            chaptersOnPage.append({"name": n, "link": l})

    return chaptersOnPage

def getChapterCtt(html):
    # https://m.diyibanzhu.buzz/34/34844/1914887.html
    ctt = html.select("#novelcontent")[0].contents
    content = []
    for c in ctt:
        if(isinstance(c, bs4.element.NavigableString)):
            c = c.stripped_strings
            content.extend(c)
    contentStr = "\n".join(content)
    return contentStr

def getNovelName(html):
    name = html.select(".cataloginfo")[0].select("h3")[0].text
    return name

def compat(novelId=""):
    cutNovelId = cutNovelIdImpl(novelId)
    urlBase = "{0}://{1}".format(metadata()["protocol"], metadata()["compatDomain"])
    metadataUrl = "{0}/{1}/".format(urlBase, cutNovelId) # https://m.diyibanzhu.buzz/34/34844/
    chapterListSplitUrl = "{0}/{1}/all_$/".format(urlBase, cutNovelId) # https://m.diyibanzhu.buzz/34/34844/all_10/. Substitute dollar sign with page number!

    return {
            "urlBase": urlBase,
            "metadataUrl": metadataUrl,
            "chapterListSplitUrl": chapterListSplitUrl,
        }

if __name__ == '__main__':
    pass
