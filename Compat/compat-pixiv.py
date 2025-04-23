#! /usr/bin/python3
# Applies to www.pixiv.net

import bs4

def metadata():
    name = "Pixiv 小说区"
    compatDomain = "www.pixiv.net"
    protocol = "https"
    author = "notRachel"
    authorEmail = "florescence_hi@aliyun.com"
    splitChapterList = True # Whether the website shows chapter-indexes of a novel in multiple pages
    splitContentList = False # Whether the website shows chapter content in multiple pages
    mobileLayout = False # This spec is now only for statistical purposes
    requireSession = True # Whether the website requires session cookies to download

    return {"name": name,
            "compatDomain": compatDomain,
            "author": author,
            "authorEmail": authorEmail,
            "protocol": protocol,
            "splitChapterList": splitChapterList,
            "mobileLayout": mobileLayout,
            "requireSession": requireSession
            }

def getChapterListsPageCountImpl():
    return {"cur": 1, "total": 1}

def getChaptersOnPage(j):
    # https://www.pixiv.net/ajax/novel/series/12829135/content_titles?lang=en
    chaptersOnPage = []
    chapterList = j["body"]
    pageCt = getChapterListsPageCountImpl()
    chaptersOnPage.append(pageCt)
    for chapter in chapterList:
        n = chapter["title"]
        l = "{0}://{1}/ajax/novel/{2}?lang=en".format(metadata()["protocol"], metadata()["compatDomain"], chapter["id"])
        chaptersOnPage.append({"name":n, "link":l})

    return chaptersOnPage

def getChapterCtt(j):
    # print(j)
    # https://www.pixiv.net/ajax/novel/23402414?lang=en
    contentStr = j["body"]["content"]
    return {"content": contentStr, "unfinished": False}

def getNovelName(j):
    # https://www.pixiv.net/ajax/novel/series/12829135?lang=en
    name = j["body"]["title"]
    return name

def compat(novelId=""):
    urlBase = "{0}://{1}".format(metadata()["protocol"], metadata()["compatDomain"])
    metadataUrl = "{0}/ajax/novel/series/{1}?lang=en".format(urlBase, novelId) # https://m.diyibanzhu.buzz/34/34844/
    chapterListSplitUrl = "{0}/ajax/novel/series/{1}/content_titles?lang=en".format(urlBase, novelId) # https://m.diyibanzhu.buzz/34/34844/all_10/. Substitute dollar sign with page number!

    return {
            "urlBase": urlBase, # https://www.pixiv.net
            "metadataUrl": metadataUrl, # https://www.pixiv.net/ajax/novel/series/12829135?lang=en
            "chapterListSplitUrl": chapterListSplitUrl, # https://www.pixiv.net/ajax/novel/series/12829135/content_titles?lang=en
        }


if __name__ == '__main__':
    pass
