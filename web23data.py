#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

'''
web23data.py - Data Objects for web23doc
Copyright (c) Andreas Ulrich, <http://erasand.ch>, <andreas@erasand.ch>

LIZENZ
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

DEUTSCHE ÜBERSETZUNG: <http://www.gnu.de/documents/gpl-3.0.de.html>
'''


class Page:
    ''' Data object for page informations '''

    def __init__(self):
        '''
        <txTab> = register title
        <txTitleLeft> = left sided page title
        <txTitleMid> = centered page title
        <txTitleRight> = right sided page title
        <lsChapters> = list with <Chapter> objects
        <txFilePath> = path for the html document
        '''
        self.txTab = ""
        self.txTitleLeft = ""
        self.txTitleMid = ""
        self.txTitleRight = ""
        self.lsChapters = []
        self.txFilePath = ""
        self.txHomeTitle = ""
        self.txHomeUrl = ""


class Chapter:
    ''' Data object for a page chapter '''

    def __init__(self):
        '''
        <txTitle> = "chapter title"
        <txId> = "id in page"
        <lsType> = list with content types:
            ["NAV", "type", ]
            lsType[0] is "NAV" for a chapter with navbar or
            None for a paragraph without navbar
        <lsCont> = list with dictionairy content of the types
            [{"id": "..", "homelist": [..], "navlist": [..]}, {}, ]
            lsCont[0] is always a dictionairy for a chapter with type
            "NAV" or None for a paragraph without navbar.
        '''
        self.txTitle = ""
        self.txId = ""
        self.lsType = ["NAV"]
        self.lsCont = [{"id": "", "homelist": [], "navlist": []}]

    def setNav(self, txHome, txUrl, lsChapters):
        '''
        Set navigation values
        <txHome> = text of home
        <txUrl> = url of home
        <lsChapters> = list with chapter objects: [<Chapter>, ]
        '''
        # Is a chapter with navbar or a paragraph without
        if self.lsType[0]:
            # Chapter with navbar, set id
            self.lsCont[0]["id"] = self.txId
            # Set home
            self.lsCont[0]["homelist"] = [txHome, txUrl]
            # Set navs
            self.lsCont[0]["navlist"] = []
            for obChapt in lsChapters:
                # Is a chapter with navbar or a paragraph without
                if obChapt.lsType[0]:
                    # Chapter with navbar, get id as url
                    txUrl = "#{0}".format(obChapt.txId)
                    # Check the active havigation
                    if self.txId == obChapt.txId:
                        # Current chapter is active
                        blActive = True
                    else:
                        # Current chapter is not active
                        blActive = False
                    # Add chapter to navs
                    self.lsCont[0]["navlist"].append([
                        obChapt.txTitle,
                        txUrl,
                        blActive
                    ])


if __name__ == '__main__':
    ''' Test routine '''
    #
    # Web23Page
    obPage = Page()
    obPage.txTab = "Test Page"
    obPage.txTitleLeft = "Web23"
    obPage.txTitleMid = "Page"
    obPage.txTitleRight = "Development"
    obPage.txFilePath = "test23.html"
    obPage.txHomeTitle = "erasand"
    obPage.txHomeUrl = "www.erasand.ch"
    print()
    print("Web23Page")
    print("------")
    print(obPage.txTab)
    print(obPage.txTitleLeft)
    print(obPage.txTitleMid)
    print(obPage.txTitleRight)
    print(obPage.txFilePath)
    print(obPage.txHomeTitle)
    print(obPage.txHomeUrl)
    # Web23Chapter
    obChapt = Chapter()
    obChapt.txTitle = "Web23 - Chapter"
    obChapt.txId = "w23"
    txTitle = "TEXT"
    dcContent = {
        "title": "Text",
        "list": ["1. Paragaraph", "2. Paragraph"]
    }
    obChapt.lsType.append(txTitle)
    obChapt.lsCont.append(dcContent)
    txTitle = "ADDRESS"
    dcContent = {
        "title": "Contact",
        "list": ["Andreas Ulrich", "Artherstrasse 13", "6300 Zug"]
    }
    obChapt.lsType.append(txTitle)
    obChapt.lsCont.append(dcContent)
    print()
    print("Web23Chapter")
    print("------------")
    print(obChapt.txTitle)
    print(obChapt.txId)
    print(obChapt.lsType)
    print(obChapt.lsCont)
    #
    # Test setNav()
    obCh2 = Chapter()
    obCh2.txTitle = "Navigation Test"
    obCh2.txId = "nav"
    txTitle = "TEXT"
    dcContent = {
        "title": "Text",
        "list": ["3. Paragaraph", "4. Paragraph"]
    }
    obCh2.lsType.append(txTitle)
    obCh2.lsCont.append(dcContent)
    obPage.lsChapters = [obChapt, obCh2]
    for obTestChapt in obPage.lsChapters:
        obTestChapt.setNav(
            "erasand",
            "https://www.erasand.ch/#erabim",
            obPage.lsChapters
        )
    print()
    print("Web23 Page & Web23Chapter")
    print("-------------------------")
    print(obPage.lsChapters)
    print(obChapt.txTitle)
    print(obChapt.lsType[0])
    print(obChapt.lsCont[0])
    print(obCh2.txTitle)
    print(obCh2.lsType[0])
    print(obCh2.lsCont[0])
