#! /usr/bin/python3

import json, re, os
from bs4 import BeautifulSoup

from Utility import file, network

# Dynamically load plugins
import importlib
from pathlib import Path
def load_compats():
    compats = {}
    compat_dir = Path(__file__).parent / "Compat"

    for pyfile in compat_dir.glob("*.py"):
        if pyfile.name == "__init__.py":
            continue

        module_name = pyfile.stem
        try:
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, pyfile)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 验证插件有效性
            if hasattr(module, "metadata"):
                compulsoryFunc = ["getChapterCtt", "getNovelName", "getChaptersOnPage", "compat"]
                for f in compulsoryFunc:
                    if not hasattr(module, f):
                       raise Exception("Warning: compulsoryFunc validation failed ({0}), skipping this compat.".format(f))
                meta = module.metadata()
                print("Found module {0}".format(meta["name"]))
                compats[meta["compatDomain"]] = module
                if(not meta.get("author") or not meta.get("authorEmail")):
                    print("Warning: Incomplete author information in plugin {0}".format(module_name))
        except Exception as e:
            print(f"Failed to load plugin {module_name}: {str(e)}")

    return compats

def applyCompat(url):
    from urllib.parse import urlparse
    compats = load_compats()
    domain = urlparse(url).netloc
    if domain not in compats:
        raise Exception(f"No eligible plugin for {domain}")

    compat = compats[domain]
    return compat

urlBase = input("Input urlBase here - https://")
urlBase = "https://{0}".format(urlBase)
compat = applyCompat(urlBase)

class Busin:
    def genericGet(webDoctUrl):
        headers = network.headers
        webDoctPld = network.prepareGenericRequest(webDoctUrl, {}, headers, "GET")

        if(webDoctPld.status_code == 200):
            webDoct = webDoctPld.text

            webDoctHtml = BeautifulSoup(webDoct, "html.parser")

            return webDoctHtml
        else:
            print("Web request has errored, server says: {0} ({1})".format(webDoctPld.reason, webDoctPld.status_code))
            return False

    def getNovelChapterList(urlBase, novelId):
        _chapterListSplitUrl = compat.compat(novelId=novelId)["chapterListSplitUrl"] # https://m.diyibanzhu.buzz/34/34844/all_$

        chapters = []
        if compat.metadata()["splitChapterList"] is True:
            chapterListSplitUrl = re.sub(r'\$', "1", _chapterListSplitUrl)
            print(chapterListSplitUrl)
            chapterListPage = Busin.genericGet(chapterListSplitUrl)
            pageCt = compat.getChaptersOnPage(chapterListPage)[0]["total"]
            curPageCt = 1
            while curPageCt:
                chapterListSplitUrl = re.sub(r'\$', str(curPageCt), _chapterListSplitUrl)
                chapterListPage = Busin.genericGet(chapterListSplitUrl)
                chaptersOnPage = compat.getChaptersOnPage(chapterListPage)
                del chaptersOnPage[0]
                chapters.extend(chaptersOnPage)
                curPageCt += 1
                if curPageCt > pageCt:
                    break
        else:
            chapterListSplitUrl = _chapterListSplitUrl
            chapterListPage = Busin.genericGet(chapterListSplitUrl)
            chapters = compat.getChaptersOnPage(chapterListPage)
            del chapters[0]

        return chapters

    def getNovelName(novelId):
        metaUrl = compat.compat(novelId=novelId)["metadataUrl"]
        webDoctHtml = Busin.genericGet(metaUrl)
        if webDoctHtml is not False:
            return compat.getNovelName(webDoctHtml)
        else:
            return False

    def getSingleChapter(singleChapterUrl):
        webDoctHtml = Busin.genericGet(singleChapterUrl)
        if webDoctHtml is not False:
            return compat.getChapterCtt(webDoctHtml)
        else:
            return False

    def crawlAllChapters(novelId):
        baseDir = "novels"
        novelName = Busin.getNovelName(novelId)
        print("Novel name: {0}".format(novelName))
        os.makedirs("{0}/{1}".format(baseDir, novelName), exist_ok=True)
        allChapters = Busin.getNovelChapterList(urlBase, novelId)
        for idx, item in enumerate(allChapters):
            print("Writing {0}".format(item["name"]))
            content = Busin.getSingleChapter(item["link"])
            if content is not False:
                content = re.sub(r' ', "\n", content)
                content = re.sub(r'\t', "\n", content)
                file.FileOperations.writeToFile(content, "{2}/{0}/{3}-{1}.txt".format(novelName, item["name"], baseDir, str(idx)))

class CI:
    def main():
        novelId = input("Enter novel ID you'd like to download: ")
        if not novelId.isdigit():
            raise Exception("Failed to validate novel ID, generally an integer is required.")
        novelName = Busin.getNovelName(novelId)
        if (novelName is not False):
            userConfirmation = input("Would you like to download {0}? (y/N)".format(novelName))
            if (userConfirmation in ["Y", "y"]):
                Busin.crawlAllChapters(novelId)
        else:
            print("Ineffective webpage content, no compatible plugins?")

if __name__ == '__main__':
    CI.main()
