#!/usr/bin/python3
# -*- coding: utf-8 -*-

import web23data

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


def fLoadText(txPath):
    '''
    Load text content from a specified file <txPath>
    '''
    # Error handling
    try:
        # Open file as object, read the text, close the file
        obFile = open(txPath, 'r')
        txContent = obFile.read()
        obFile.close()
    except Exception as obError:
        # Output of error message and set a empty text
        txError = "PATH: {0} -- ERROR: {1}".format(
            txPath,
            str(obError)
        )
        print(txError)
        txContent = ""
    return(txContent)


class WebTextImportA:
    ''' Import content from a .txt document '''

    def __init__(self):
        '''
        <txFilePath> = filepath of text file
        <lsText> = list with text
        <txItem> = current text line
        <txPars> = Type of current parsing as text
        <obDoc> = Object for the Web23 document
        <obChapt> = Object for the current chapter
        <txType> = Current content type
        <dcContent> = Current content dictionairy
        <lsCleaned> = Text list for <mSplitClean()>
        '''
        self.txFilePath = ""
        self.lsText = []
        self.txItem = ""
        self.txPars = ""
        self.obDoc = None
        self.obChapt = None
        self.txType = ""
        self.dcCont = {}
        self.lsCleaned = []

    def mSetTextList(self):
        ''' Read text from file, split text to list <lsText> '''
        txText = fLoadText(self.txFilePath)
        self.lsText = txText.splitlines()
        # print(self.lsText)

    def mParsing(self):
        '''
        Parse content from <lsText>

        Structure:
        web23data.Page
            .txTab = text
            .txTitleLeft = text
            .txTitleMid = text
            .txTitleRight = text
            .txFilePath = text
            .lsChapters = list with web23data.Chapter

        web23data.Chapter
            .txTitle = text
            .txId = text
            .lsType = list with texts, conent types
                      ["NAV", "..", ] with navbar
                      [None, "..", ]    wthout navbar
            .lsCont = list with dictionairies, content with navbar:
                      [{"id": "", "homelist": [], "navlist": []}, {..}]
                      without navbar:
                      [None, {..] ]

        Structure Types
        "DOCU" = document
        "CHAP" = chapter with navbar
        "PARA" = chapter (paragraph) without navbar
        "----" = end of type
        "====" = end of chapter

        Content Types and their dictionairy
        "ADDRESS", {"title": "", "list": ["", ]}
        "IMAGE", {"image": "", "text: ""}
        "LINKS", {"title": "", "list": [["", ""], ]}
        "LIST", {"title": "", "listtype": "", "list": ["", ]}
        "NAV", {"id": "", "homelist": ["", ""],
                "navlist": [["", "", True/False], ]}
        "TABLE", {"title": "", "headerlist": ["", ],
                "rowlist": [["", ], ]}
        "TEXT", {"title": "", "list": ["", ]}
        '''
        # Iterate list
        self.txPars = ""
        for self.txItem in self.lsText:
            # Remove leading whitespaces left and right
            self.txItem = self.txItem.strip()
            # Analyze Lines
            if not self.txPars:
                # Search content type
                if self.txItem.startswith("DOCU"):
                    # Document title
                    self.txPars = "DOCU"
                    self.obDoc = web23data.Page()
                elif self.txItem.startswith("CHAP"):
                    # New chapter
                    self.txPars = "CHAP"
                    self.obChapt = web23data.Chapter()
                elif self.txItem.startswith("PARA"):
                    # New chapter
                    self.txPars = "PARA"
                    self.obChapt = web23data.Chapter()
                    self.obChapt.lsType[0] = None
                    self.obChapt.lsCont[0] = None
                elif self.txItem.startswith("IMAG"):
                    # Address content
                    self.txPars = "IMAG"
                    self.txType = "IMAGE"
                    self.dcCont = {
                        "image": "",
                        "text": ""
                    }
                elif self.txItem.startswith("ADDR"):
                    # Address content
                    self.txPars = "ADDR"
                    self.txType = "ADDRESS"
                    self.dcCont = {
                        "title": "",
                        "list": []
                    }
                elif self.txItem.startswith("LINK"):
                    # Links content
                    self.txPars = "LINK"
                    self.txType = "LINKS"
                    self.dcCont = {
                        "title": "",
                        "list": []
                    }
                elif self.txItem.startswith("LIST"):
                    # List content
                    self.txPars = "LIST"
                    self.txType = "LIST"
                    self.dcCont = {
                        "title": "",
                        "listtype": "",
                        "list": []
                    }
                elif self.txItem.startswith("NAVB"):
                    # Navigation content
                    self.txPars = "NAVB"
                    self.txType = "NAV"
                    self.dcCont = {
                        "id": "",
                        "homelist": [],
                        "navlist": []
                    }
                elif self.txItem.startswith("TABL"):
                    # Table content
                    self.txPars = "TABL"
                    self.txType = "TABLE"
                    self.dcCont = {
                        "title": "",
                        "headerlist": [],
                        "rowlist": []
                    }
                elif self.txItem.startswith("TEXT"):
                    # Text content
                    self.txPars = "TEXT"
                    self.txType = "TEXT"
                    self.dcCont = {
                        "title": "",
                        "list": []
                    }
                elif self.txItem.startswith("===="):
                    # End of chapter
                    self.obDoc.lsChapters.append(self.obChapt)
            elif self.txPars == "DOCU":
                # Document values
                self.mSetDocuValues()
            elif self.txPars == "CHAP":
                # Chapters information
                self.mSetChaptValues()
            elif self.txPars == "PARA":
                # Paragraph information
                self.mSetParaValues()
            elif self.txPars == "ADDR":
                # Address content
                self.mSetAddressContent()
            elif self.txPars == "IMAG":
                # Address content
                self.mSetImageContent()
            elif self.txPars == "LINK":
                # Link content
                self.mSetLinkContent()
            elif self.txPars == "LIST":
                # List content
                self.mSetListContent()
            elif self.txPars == "NAVB":
                # NavBar content
                self.mSetNavBarContent()
            elif self.txPars == "TABL":
                # Table content
                self.mSetTableContent()
            elif self.txPars == "TEXT":
                # Text content
                self.mSetTextContent()

    def mSetDocuValues(self):
        '''
        Get Values for "DOCU" structure type
        "tabt" = <txTab>
        "tit1" = <txTitleLeft>
        "tit2" = <txTitleMid>
        "tit3" = <txTitleRight>
        "file" = <txtxFilePath>
        "home" = <txHomeTitle>, <txHomeUrl>
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("tabt"):
            # 2nd value is tab text
            self.obDoc.txTab = self.lsCleaned[1]
        elif self.txItem.startswith("tit1"):
            # 2nd value is left title
            self.obDoc.txTitleLeft = self.lsCleaned[1]
        elif self.txItem.startswith("tit2"):
            # 2nd value is center title
            self.obDoc.txTitleMid = self.lsCleaned[1]
        elif self.txItem.startswith("tit3"):
            # 2nd value is right title
            self.obDoc.txTitleRight = self.lsCleaned[1]
        elif self.txItem.startswith("file"):
            # 2nd value is filepath
            self.obDoc.txFilePath = self.lsCleaned[1]
        elif self.txItem.startswith("home"):
            # 2nd value is home title
            self.obDoc.txHomeTitle = self.lsCleaned[1]
            # 3rd value ist home url
            self.obDoc.txHomeUrl = self.lsCleaned[2]
        elif self.txItem.startswith("----"):
            # End of docu informations
            self.txPars = ""
            print("<web23data.Page>")
            print("txTab:", self.obDoc.txTab)
            print("txTitleLeft:", self.obDoc.txTitleLeft)
            print("txTitleMid:", self.obDoc.txTitleMid)
            print("txTitleRight:", self.obDoc.txTitleRight)
            print("txFilePath:", self.obDoc.txFilePath)
            print("txHomeTitle:", self.obDoc.txHomeTitle)
            print("txHomeUrl:", self.obDoc.txHomeUrl)
            print("----")

    def mSetChaptValues(self):
        '''
        Get values for "CHAP" structure type
        "titl" = <txTitle>
        "nvid" = <txId>
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.obChapt.txTitle = self.lsCleaned[1]
        elif self.txItem.startswith("nvid"):
            # 2nd value is id
            self.obChapt.txId = self.lsCleaned[1]
        elif self.txItem.startswith("----"):
            # End of chapter
            self.txPars = ""
            print("web23data.Chapter")
            print("txTitle:", self.obChapt.txTitle)
            print("txId:", self.obChapt.txId)
            print("----")

    def mSetParaValues(self):
        '''
        Get values for "PARA" structure type
        '''
        if self.txItem.startswith("----"):
            # End of chapter
            self.txPars = ""
            print("web23data.Paragraph")
            print("----")

    def mSetAddressContent(self):
        '''
        Get values of "ADDR" content
        "titl" = ["title"]
        "list" = ["list"]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.dcCont["title"] = self.mGetTitle()
        elif self.txItem.startswith("list"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Extend content list with text list
            self.dcCont["list"].extend(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetImageContent(self):
        '''
        Get values of "IMAG" content
        "imag" = ["image"]
        "text" = ["text"]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("imag"):
            # 2nd value is image
            self.dcCont["image"] = self.lsCleaned[1]
        elif self.txItem.startswith("text"):
            # 2nd value is text
            self.dcCont["text"] = self.lsCleaned[1]
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetLinkContent(self):
        '''
        Get values of "LINK" content
        "titl" = ["title"]
        "txur" = ["list"[txur[1], txur[2]]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.dcCont["title"] = self.mGetTitle()
        elif self.txItem.startswith("txur"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Append link text and url text to content list
            self.dcCont["list"].append(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetListContent(self):
        '''
        Get values of "LIST" content
        "titl" = ["title"]
        "ltyp" = ["listtype"]
        "list" = ["list"]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.dcCont["title"] = self.mGetTitle()
        elif self.txItem.startswith("ltyp"):
            # 2nd value is list type, ul or ol
            self.dcCont["listtype"] = self.lsCleaned[1]
        elif self.txItem.startswith("list"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Extend content list with text list
            self.dcCont["list"].extend(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetNavBarContent(self):
        '''
        Get values of "NAVB" content
        "urid" = ["id"]
        "home" = ["homelist"]
        "navl" = ["navlist"]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("urid"):
            # 2nd value is id
            self.dcCont["id"] = self.lsCleaned[1]
        elif self.txItem.startswith("home"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Extend home list with text list
            self.dcCont["homelist"].extend(self.lsCleaned)
        elif self.txItem.startswith("navl"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Add False for not active
            self.lsCleaned.append(False)
            # Extend navigation list with text list
            self.dcCont["navlist"].append(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetTableContent(self):
        '''
        Get values of "TABL" content
        "titl" = ["title"]
        "head" = ["headerlist"]
        "cell" = ["rowlist"[cell[1], cell[n]], ]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.dcCont["title"] = self.mGetTitle()
        elif self.txItem.startswith("head"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Extend haeder list with text list
            self.dcCont["headerlist"].extend(self.lsCleaned)
        elif self.txItem.startswith("cell"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Append cell texts to content list
            self.dcCont["rowlist"].append(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetTextContent(self):
        '''
        Get values of "TEXT" content
        "titl" = ["title"]
        "text" = ["list"]
        '''
        # Split text
        self.mSplitClean()
        # Read values
        if self.txItem.startswith("titl"):
            # 2nd value is title
            self.dcCont["title"] = self.mGetTitle()
        elif self.txItem.startswith("text"):
            # Remove 1st value, "list"
            del self.lsCleaned[0]
            # Extend content list with text list
            self.dcCont["list"].extend(self.lsCleaned)
        elif self.txItem.startswith("----"):
            self.mSetContentEnd()

    def mSetContentEnd(self):
        ''' End of content '''
        # Set content to chapter and reset txPars
        self.obChapt.lsType.append(self.txType)
        self.obChapt.lsCont.append(self.dcCont)
        print("Content type:", self.txType)
        print("Content:", self.dcCont)
        print("----")
        self.txPars = ""

    def mSplitClean(self):
        '''
        Split .txItem at Tabulators, "\t" and return the list with
        cleaned text:
        - No leading whitespaces left and rigth
        - No empty items
        '''
        lsSplit = self.txItem.split("\t")
        self.lsCleaned = []
        for txItem in lsSplit:
            # Removing leading whitespaces left and right
            txItem.strip()
            if txItem:
                # Item with content
                self.lsCleaned.append(txItem)

    def mGetTitle(self):
        '''
        Return the 2nd value in <lsCleaned> if exists,
        otherwise return ""
        '''
        if (len(self.lsCleaned) > 1):
            txTitle = self.lsCleaned[1]
        else:
            txTitle = ""
        return(txTitle)


if __name__ == '__main__':
    ''' Test routine '''
    obImp = WebTextImportA()
    obImp.txFilePath = "sandDOK/index.txt"
    obImp.mSetTextList()
    obImp.mParsing()
