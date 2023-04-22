#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import web23input

'''
web23doc.py - Create Online Documents with Bootstrap
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


def fSaveText(txPath, txText):
    ''' Save text <txText> with the path <txPath> '''
    # Normalize path
    txPath = os.path.normcase(os.path.normpath(txPath))
    # Save text
    try:
        obDatei = open(
            txPath,
            'w',
            encoding='utf-8',
            errors='ignore'
        )
        obDatei.write(txText)
        obDatei.close()
    except Exception as obErr:
        # Display error message
        txMsg = "ERROR, PATH: {0}, MESSAGE: {1}".format(
            txPath,
            str(obErr)
        )
        print(txMsg)


class WebDocA:
    ''' Object to create Bootstrap static documents, version A '''

    def __init__(self):
        ''' Initialize '''
        # List with content
        self.lsDatas = []
        # Dictionairy to create the index
        self.dcChapter = {}
        # Space between columns and rows, as string
        self.txPx = "px-4"
        self.txPy = "py-4"
        # String to specify the columns for 1, 2, 3 columns
        self.txCol = "col"
        # Line break
        self.txLf = "\n"
        # Page object
        self.obPage = None
        # Lightbox counter
        self.inLightBox = 0

    def mGetHead(self, txTitle):
        ''' Get the <head> section with the <txTitle> '''
        txHtml = ''.join([
            '<!doctype html>', self.txLf,
            '<html lang="en"', self.txLf,
            '<head>', self.txLf,
            '<meta charset="utf-8">', self.txLf,
            '<meta name="viewport" content="width=device-width, ',
            'initial-scale=1">', self.txLf,
            '<title>', txTitle, '</title>', self.txLf,
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@',
            '5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet"',
            ' integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/',
            'Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">',
            self.txLf,
            '</head>', self.txLf
        ])
        return(txHtml)

    def mGetBody(self, txLeft, txMid, txRight):
        '''
        Get the start of <body> section with the document header
        <txLeft> = left sided h1 text
        <txMid> = centered h2 text
        <txRight> = right sided h3 text
        '''
        # left sided: text-start, centered: text-center
        # right sided: text-end
        txHtml = ''.join([
            '<body>', self.txLf,
            '<div class="container-fluid">', self.txLf,
            '<div class="row ', self.txPy, '">', self.txLf,
            '<div class="col-4 ', self.txPx, ' text-start"><h1>',
            txLeft, '</h1></div>', self.txLf,
            '<div class="col-4 ', self.txPx, ' text-start"><h2>',
            txMid, '</h2></div>', self.txLf,
            '<div class="col-4 ', self.txPx, ' text-start ',
            'text-secondary"><h3>', txRight, '</h3></div>', self.txLf,
            '</div>', self.txLf
        ])
        return(txHtml)

    def mGetEnd(self):
        ''' Get the end of <body> section '''
        txHtml = ''.join([
            '</div>', self.txLf,
            '<script src="https://cdn.jsdelivr.net/npm/bootstrap@',
            '5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity=',
            '"sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZ',
            'giwxhTBTkF7CXvN" crossorigin="anonymous"></script>',
            self.txLf,
            '<script src="https://cdn.jsdelivr.net/npm/bs5-lightbox@',
            '1.8.3/dist/index.bundle.min.js"></script>',
            self.txLf,
            '</body>', self.txLf,
            '</html>', self.txLf
        ])
        return(txHtml)

    def mGetNav(self, txId, lsHome, lsNav):
        '''
        Get nav-pils for navigation
        <txId> = "id"
        <lsHome> = ["Text", "URL"]
        <lsNav> =  [["Text", "URL", Active], ]
                   Active = True/False
        '''
        # Header
        txText = lsHome[0]
        txUrl = lsHome[1]
        txHtml = ''.join([
            '<div id="', txId, '" class="row ', self.txPy, '">',
            self.txLf, '<ul class="nav nav-tabs ', self.txPx, '">',
            self.txLf, '<li class="nav-item"><a class="nav-link" ',
            'href="', txUrl, '">', txText, '</a></li>', self.txLf
        ])
        # Iterate navigation items
        for lsItem in lsNav:
            txText = lsItem[0]
            txUrl = lsItem[1]
            blAct = lsItem[2]
            txHtml = ''.join([
                txHtml,
                '<li class="nav-item">',
            ])
            if blAct:
                # Active item
                txHtml = ''.join([
                    txHtml,
                    '<a class="nav-link active" aria-current="page" ',
                    'href="', txUrl, '">', txText, '</a></li>',
                    self.txLf
                ])
            else:
                # Not a acitve item
                txHtml = ''.join([
                    txHtml,
                    '<a class="nav-link" href="', txUrl, '">', txText,
                    '</a></li>', self.txLf
                ])
        # End
        txHtml = ''.join([
            txHtml,
            '</ul>', self.txLf,
            '</div>', self.txLf
        ])
        return(txHtml)

    def mGetText(self, txTitle, lsText):
        '''
        Get Title and text
        <txTitle> = title
        <lsText> = ["paragraph", "paragraph", ..]
        '''
        # Title
        txHtml = ''.join(['<h3>', txTitle, '</h3>', self.txLf])
        # Iterate text list
        for txItem in lsText:
            txHtml = ''.join([txHtml, '<p>', txItem, '</p>', self.txLf])
        return(txHtml)

    def mGetAdress(self, txTitle, lsAddress):
        '''
        Get Title and address
        <txTitle> = title
        <lsAddress> = ["Name", "Address", ..]
        '''
        # Title
        txHtml = ''.join([
            '<h3>', txTitle, '</h3>', self.txLf,
            '<address>', self.txLf])
        # Iterate address list
        for txItem in lsAddress:
            txHtml = ''.join([txHtml, txItem, '<br>', self.txLf])
        # Address end
        txHtml = ''.join([txHtml, '</address>', self.txLf])
        return(txHtml)

    def mGetTable(self, txTitle, lsHeader, lsRows):
        '''
        Get Title and table
        <txTitle> = title
        <lsHeader> = ["head 1", "head 2", ..]
        <lsRows> = [["row1 col1", "row1 col2", ..],
                    ["row2 col1", "row2 col2", ..], ..]
        '''
        # Title and table start
        txHtml = ''.join([
            '<h3>', txTitle, '</h3>', self.txLf,
            '<table class="table">', self.txLf,
            '<thead>', self.txLf,
            '<tr>', self.txLf])
        # Iterate headers
        for txItem in lsHeader:
            txHtml = ''.join([
                txHtml, '<th scope="col">', txItem, '</th>', self.txLf
            ])
        # Table row start
        txHtml = ''.join([
            txHtml, '</tr>', self.txLf,
            '</thead>', self.txLf,
            '<tbody>', self.txLf])
        # Iterate rows
        for lsCells in lsRows:
            # Start row
            txHtml = ''.join([txHtml, '<tr>', self.txLf])
            # Iterate cells
            for txCell in lsCells:
                txHtml = ''.join([
                    txHtml, '<td>', txCell, '</td>', self.txLf
                ])
            # End row
            txHtml = ''.join([txHtml, '</tr>', self.txLf])
        # Table end
        txHtml = ''.join([
            txHtml, '</tbody>', self.txLf,
            '</table>', self.txLf
        ])
        return(txHtml)

    def mGetList(self, txTitle, txType, lsList):
        '''
        Get Title and list
        <txTitle> = title
        <txType> = "ul", "ol"
        <lsList> = ["Item", "Item", ..]
        '''
        # Title and List start
        txHtml = ''.join([
            '<h3>', txTitle, '</h3>', self.txLf,
            '<', txType, ' class="list-group list-group-flush'
        ])
        # Diference between unorddered and ordered
        if txType == "ul":
            txHtml = ''.join([txHtml, '">', self.txLf])
        else:
            txHtml = ''.join([
                txHtml, ' list-group-numbered">', self.txLf
            ])
        # Iterate list
        for txItem in lsList:
            txHtml = ''.join([
                txHtml, '<li class="list-group-item">', txItem,
                '</li>', self.txLf
            ])
        # List end
        txHtml = ''.join([txHtml, '</', txType, '>', self.txLf])
        return(txHtml)

    def mGetLinks(self, txTitle, lsLinks):
        '''
        Get Title and links in a list
        <txTitle> = title
        <lsLinks> = [["Text", "URL"], ["Text", "URL"], ..]
        '''
        # Title and List start
        txHtml = ''.join([
            '<h3>', txTitle, '</h3>', self.txLf,
            '<div class="list-group">', self.txLf
        ])
        # Iterate links
        for txText, txUrl in lsLinks:
            txHtml = ''.join([
                txHtml, '<a href="', txUrl, '" class="list-group-item ',
                'list-group-item-action list-group-item-info" ',
                'target="_blank">', txText, '</a>', self.txLf])
        # Link end
        txHtml = ''.join([txHtml, '</div>', self.txLf])
        return(txHtml)

    def mGetImg(self, txSource, txText):
        '''
        Get Image with a text
        <txSource> = link, url to the picture
        <txText> = text under the picture
        '''
        # Increase lightbox counter
        self.inLightBox += 1
        # Picture with lightbox
        txHtml = ''.join([
            '<a href="', txSource, '?image=', str(self.inLightBox),
            '" data-toggle="lightbox" data-caption="', txText, '">',
            '<img src="', txSource, '?image=', str(self.inLightBox),
            '" class="img-fluid img-thumbnail"></a>',
            self.txLf
        ])
        # Text under the picture
        txHtml = ''.join([txHtml, '<p>', txText, '</p>', self.txLf])
        return(txHtml)

    def mGetNavCol(self, dcNav, lsContent):
        ''' Get columns with leading navbar '''
        # Nav
        txHtml = self.mGetContent(dcNav)
        # Row
        txHtml = ''.join([
            txHtml, '<div class="row py-4">', self.txLf,
        ])
        # Iterate Columns
        for dcContent in lsContent:
            # Column
            txHtml = ''.join([
                txHtml,
                '<div class="', self.txCol, ' ', self.txPx, '">',
                self.txLf, self.mGetContent(dcContent), self.txLf,
                '</div>', self.txLf
            ])
        # End
        txHtml = ''.join([txHtml, '</div>', self.txLf])
        return(txHtml)

    def mGetCol(self, lsContent):
        ''' Get columns without navbar '''
        # Row
        txHtml = ''.join([
            '<div class="row py-4">', self.txLf,
        ])
        # Iterate Columns
        for dcContent in lsContent:
            # Column
            txHtml = ''.join([
                txHtml,
                '<div class="', self.txCol, ' ', self.txPx, '">',
                self.txLf, self.mGetContent(dcContent), self.txLf,
                '</div>', self.txLf
            ])
        # End
        txHtml = ''.join([txHtml, '</div>', self.txLf])
        return(txHtml)

    def mGetContent(self, dcContent):
        '''
        Get the Content
        <dcContent> = dictionairy of the datas, related to the content
                      type
                      Necessary keys: "type" = type of content
                                      "title" = content title
        '''
        if dcContent["type"] == "ADDRESS":
            # Get address content
            txHtml = self.mGetAdress(
                dcContent["title"],
                dcContent["list"]
            )
        elif dcContent["type"] == "IMAGE":
            # Get text content
            txHtml = self.mGetImg(
                dcContent["image"],
                dcContent["text"]
            )
        elif dcContent["type"] == "LINKS":
            # Get links content
            txHtml = self.mGetLinks(
                dcContent["title"],
                dcContent["list"]
            )
        elif dcContent["type"] == "LIST":
            # Get list content
            txHtml = self.mGetList(
                dcContent["title"],
                dcContent["listtype"],
                dcContent["list"]
            )
        elif dcContent["type"] == "NAV":
            # Get navbar content
            txHtml = self.mGetNav(
                dcContent["id"],
                dcContent["homelist"],
                dcContent["navlist"]
            )
        elif dcContent["type"] == "TABLE":
            # Get table content
            txHtml = self.mGetTable(
                dcContent["title"],
                dcContent["headerlist"],
                dcContent["rowlist"]
            )
        elif dcContent["type"] == "TEXT":
            # Get text content
            txHtml = self.mGetText(
                dcContent["title"],
                dcContent["list"]
            )
        else:
            # Unknown content
            print("Error, unknown content")
            txHtml = ""
        return(txHtml)

    def mCreateDoc(self):
        ''' Create the document as webPage '''
        # Page Start
        txHtml = ''.join([
            self.mGetHead(self.obPage.txTab),
            self.mGetBody(
                self.obPage.txTitleLeft,
                self.obPage.txTitleMid,
                self.obPage.txTitleRight)
        ])
        # Set Navigations
        for inIdx in range(len(self.obPage.lsChapters)):
            self.obPage.lsChapters[inIdx].setNav(
                self.obPage.txHomeTitle,
                self.obPage.txHomeUrl,
                self.obPage.lsChapters
            )
        # Iterate Chapters
        for obChapt in self.obPage.lsChapters:
            # Is chapter with nav or paragraph without
            if obChapt.lsType[0]:
                # Chapter with nav, set nav dictionairy
                dcNav = {"type": obChapt.lsType[0]}
                # Update nav dictionairy with current links
                dcNav.update(obChapt.lsCont[0])
            # Prepare content dictionairies in a list
            lsContent = []
            for inIdx in range(1, len(obChapt.lsType)):
                # Set content with type
                dcContent = {"type": obChapt.lsType[inIdx]}
                # Update with content from chapter
                dcContent.update(obChapt.lsCont[inIdx])
                # Add content dictionairy to list
                lsContent.append(dcContent)
            # Is chapter with nav or paragraph without
            if obChapt.lsType[0]:
                # Chapter with nav, add to html text
                txHtml = ''.join([txHtml, self.mGetNavCol(
                    dcNav,
                    lsContent
                )])
            else:
                # Paragraph without nav, add to html text
                txHtml = ''.join([txHtml, self.mGetCol(lsContent)])
        # Page end
        txHtml = ''.join([txHtml, self.mGetEnd()])
        # Save page
        fSaveText(self.obPage.txFilePath, txHtml)


if __name__ == '__main__':
    ''' Main routine '''
    # WebDocA object
    obWebDoc = WebDocA()
    # Get content with WebTextImportA object
    obImp = web23input.WebTextImportA()
    obImp.txFilePath = "sandDOK/Template/index.txt"
    obImp.mSetTextList()
    obImp.mParsing()
    # Set the Page object to the WebDocA object and create Page
    obWebDoc.obPage = obImp.obDoc
    obWebDoc.mCreateDoc()
