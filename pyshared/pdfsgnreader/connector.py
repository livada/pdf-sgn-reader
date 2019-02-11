import os.path
import lxml.etree

import base64
from tempfile import NamedTemporaryFile
from subprocess import call
from zipfile import ZipFile


class SgnPdfXMLConnectorError(Exception):
    pass


class SgnPdfXMLConnector:
    def __init__(self, xml_filepath=None):
        self._xml_filepath = xml_filepath
        
        self._pdf = None
        self._signature = None
        self._timestamp = None

    def load(self, xml_filepath=None):
        if xml_filepath is not None:
            self._xml_filepath = xml_filepath

        if self._xml_filepath is None or not os.path.isfile(self._xml_filepath):
            raise SgnPdfXMLConnectorError('XML file must be attached to connector')

        schema = lxml.etree.XMLSchema(
                        file=os.path.join(os.path.dirname(__file__), 'sgn.xsd')
                        )
        xmltree = lxml.etree.parse(
                        self._xml_filepath,
                        lxml.etree.XMLParser(schema=schema)
                        )
        
        if not schema(xmltree):
            raise SgnPdfXMLConnectorError('%s is not a recognized signed pdf file' % self._xml_filepath)
        
        xmlupload = xmltree.getroot()
        
        self._timestamp = xmlupload.findtext('TimeStamp').strip()
        
        xmlfile = xmlupload.find('File')
        xmlsigner = xmlupload.find('Signer')

        self._pdf = {
            'compression': xmlfile.get('compress'),
            'encoding': xmlfile.get('encoding'),
            'data': xmlfile.text,
        }

        self._signature = {
            'certificate': xmlsigner.findtext('Certificate').strip(),
            'sign': xmlsigner.findtext('Sign').strip(),
            'timestamp': xmlsigner.findtext('Time').strip(),
        }

    def open_pdf(self, reader='evince'):
        if not self._pdf:
            return
        
        data = self._pdf['data'].strip()
        
        if self._pdf['encoding'] == 'base64':
            data = base64.b64decode(data)
        
        if self._pdf['compression'] == 'zip':
            with NamedTemporaryFile() as _f:
                _f.write(data)
                with ZipFile(_f) as arch:
                    data = arch.read(arch.infolist()[0])

        with NamedTemporaryFile() as _f:
            _f.write(data)
            call([reader, _f.name])

    def validate_sign(self):
        # TODO
        pass


