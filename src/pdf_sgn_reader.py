#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reads PBZ signed pdf reports.
"""

__author__ = "Davor Bokun"
__copyright__ = "Copyright (C) 2016 Davor Bokun <bokundavor@gmail.com>"
__credits__ = ["Davor Bokun"]
__license__ = "GPL"
__version__ = '0.1'
__maintainer__ = "Davor Bokun"
__email__ = "bokundavor@gmail.com"
__status__ = "Alpha"


import sys

if __name__!='__main__':
    # Do not allow importing as module
    sys.exit()

import argparse
from connector import SgnPdfXMLConnector


parser = argparse.ArgumentParser(description='PBZ signed pdf reader tool.')

parser.add_argument('input_file', 
                    type=str, 
                    help='input .pdf.sgn file')
parser.add_argument('-v', '--version', action='version', 
                    version='%(prog)s version ' + __version__)



args = parser.parse_args()


xmlcnn = SgnPdfXMLConnector(args.input_file)
xmlcnn.load()

# TODO
# xmlcnn.validate_sign()

xmlcnn.open_pdf()




