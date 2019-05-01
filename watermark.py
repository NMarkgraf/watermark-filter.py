#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Quick-Watermark-Filter: matermark.py

  (C)opyleft in 2019 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  1.0.0 - 01.05.2019 (nm) - Erster Aufschlag
 

  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ
    Bei *nix und macOS Systemen muss diese Datei als "executable" markiert
    sein!
    Also bitte ein
      > chmod a+x watermark.py
   ausfuehren!


  Lizenz:
  =======
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import panflute as pf  # panflute fuer den pandoc AST
import os as os  # check if file exists.
import re as re  # re fuer die Regulaeren Ausdruecke
import logging  # logging fuer die 'watermark.log'-Datei
import sys as sys

if sys.version_info < (3,6):
    print("Must use Python 3.6 or better.")
    sys.exit(1)

# Eine Log-Datei "watermark.log" erzeugen um einfacher zu debuggen
if os.path.exists("watermark.loglevel.debug"):
    DEBUGLEVEL = logging.DEBUG
elif os.path.exists("watermark.loglevel.info"):
    DEBUGLEVEL = logging.INFO
elif os.path.exists("watermark.loglevel.warning"):
    DEBUGLEVEL = logging.WARNING
elif os.path.exists("watermark.loglevel.error"):
    DEBUGLEVEL = logging.ERROR
else:
    DEBUGLEVEL = logging.ERROR  # .ERROR or .DEBUG  or .INFO

logging.basicConfig(filename='watermark.log', level=DEBUGLEVEL)


def getDeprecatedMark(txt, format):
  if format in ("latex", "beamer"):
      return pf.RawBlock("\\backgroundsetup{contents={"+txt+"}}\n\\BgMaterial", format="latex")
      

def action(elem, doc):
    """
    """
    if isinstance(elem, pf.Header):
        logging.debug("Header found: "+str(elem.content))
        if "include-only" in elem.attributes:
            lst = list(map(lambda x: x.strip(), elem.attributes["include-only"].split(",")))
            if "deprecated" in lst:
                return [elem, getDeprecatedMark("DEPRECATED!", doc.format)]
            if "master" in lst:
                return [elem, getDeprecatedMark("MASTER ONLY!", doc.format)]
            if "bachelor" in lst:
                return [elem, getDeprecatedMark("BACHELOR ONLY!", doc.format)]


def prepare(doc):
    pass


def finalize(doc):
    pass


def main(doc=None):
    """main function.
    """
    
    logging.debug("Start pandoc filter 'watermark.py'")
    mydoc = doc
    flag = False

    if isinstance(mydoc, pf.Doc):
        mydoc = doc.content
        flag = True

    ret = pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=mydoc)
    logging.debug("End pandoc filter 'watermark.py'")
    if flag:
        doc.content = ret
    else:
        doc = ret
    return doc
if __name__ == "__main__":
    main()
