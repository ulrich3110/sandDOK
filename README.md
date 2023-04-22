# sandDOK
Web Dokumente mit Bootstrap einfach erstellen

## Anwendung
Der Inhalt wird in einer Textdatei (.txt) verfasst, z.B. im Word.

### Textdatei
Der Text wird mit folgenden Struktur-Elementen formatiert:
- DOCU: Eigenschaften des Dokuments
- CHAP: Ein neues Kapitel mit Navbars
- PARA: Ein neuer Absatz ohne Navbars
- ----: Ende eines Inhalts
- ====: Ende eines Kapitels oder Absatzes
- ADDR: Adressblock
- LINK: Auflistung von Verknüpfungen
- LIST: Eine Liste
- TABL: Eine Tabelle
- TEXT: Ein Textblock
- NAVB: Eine Navigationsbar mit Pills
- IMAG: Ein Bild

Die Trennung der verschiedenen Werte erfolgt durch einen oder mehrere Tabstops (Tabulator Taste).

Der Textinhalt wird mit folgenden Inhalts-Elementen angegeben:
- tabt: Register Titel des Dokuemnts
- tit1: Linker H1 Titel
- tit2: Zentrierter H2 Untertitel
- tit3: Rechte Dokumentenbeschreibung
- file: Name der Ausgabedatei
- home: Name der Ursprungsadresse, gefolgt von einer URL der Ursprungsseite getrennt durch einen Tabstop. Dies wird für die Navigation verwendet.
- titl: Titel für Inhalte
- nvid: Eindeutige Id, wird gebraucht für die Navigation
- list: Eine Liste von Texten, getrennt mit Tabstops
- txur: Verknüpfungsname, gefolgt von der Verknüpfungsadresse, getrennt durch einen Tabstop
- ltyp: ul für ungeordnete Liste oder ol für mit Zahlen geordnete Liste
- head: Kopfzeile einer Tabelle, die Spalten der Spalten werden durch Tabstops getrennt
- cell: Zeilen einer Tabelle, die Spalten werden durch Tabstops getrennt
- text: Texte, Zeilen können durch Leerschläge getrennt werden, oder indem mehrere text Linien eingegeben werden.

Ein Zeilenende (Zeilenumbruch) schliesst ein Struktur- oder Inhaltselement ab.

Die Datei _sandDok/Template/index.txt_ kann als Vorlage verwendet und angepasst werden.

### Erzeugung des Webdokuments
Die 3 Python Scripte _web23dok.py_, _web23data.py_ und _web23input.py_ müssen sich im gleichen Verzeichnis befinden

In der Datei _web23dok.py_ befindet sich am Schluss der Eintrag für die Textdatei: `obImp.txFilePath = "sandDOK/Template/index.txt"`. Hier wird die Textdatei angegeben, in unserem Fall ist es _sandDOK/Template/index.txt_. Nach Ausführung von _web23dok.py_ wird das Webdokument erstellt.

## Beispiele

Unter [dok.erasand](https://dok.erasand.ch/) sind meine sandDOK Web Dokumente abgelegt.

----------------

Andreas Ulrich, 22. April 2023
