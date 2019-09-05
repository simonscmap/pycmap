"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-15

Function: Store the retrieved data/metadata on local machine.
"""


import os
from zipfile import ZipFile
from .cmap import API  # noqa
from .common import (
                     get_export_dir,
                     get_export_format
                    )



class Export(object):
    
    """Use this class to handle saving data locally."""

    def __init__(self, data, metadata, filename, exportDir=None, fileFormat=None):
        """
        :param dataframe data: data to be saved locally.
        :param dataframe metadata: metadata to be saved locally.
        :param str filename: base filename used for the exported files.
        :param str exportDir: path to local directory where the data and metadata files are saved.
        :param str fileFormat: data file format.
        """
        self.data = data
        self.metadata = metadata
        self.filename = filename
        if exportDir is None: exportDir = get_export_dir()
        self.exportDir = exportDir    
        if not os.path.exists(self.exportDir): os.makedirs(self.exportDir)
        if fileFormat is None: fileFormat = get_export_format()
        self.fileFormat = fileFormat.lower().strip()   
        return


    @staticmethod
    def save_as(df, path):
        ext = os.path.splitext(path)[1].lower().strip()
        if ext =='.json':
            df.to_json(path)
        else:
            df.to_csv(path, index=False)


    @staticmethod
    def zip(dataPath, metaPath, zipPath):
        """Zip the data and metadata files."""
        with ZipFile(zipPath, 'w') as ZIP:
            ZIP.write(dataPath)
            ZIP.write(metaPath)
        return


    def expPath(self):
        """Constructs the path to data, metadata, and zipfiles."""
        base = self.exportDir + self.filename          
        dataPath = base + self.fileFormat
        metaPath = base + '_meta' + self.fileFormat
        zipPath = base + '.zip'
        return dataPath, metaPath, zipPath


    def save(self):
        """Save data and metadata files as a single zipped file on local machine."""    
        dataPath, metaPath, zipPath = self.expPath()        
        self.save_as(self.data, dataPath)    
        self.save_as(self.metadata, metaPath)
        # zip(dataPath, metaPath, zipPath)
        # os.remove(dataPath)
        # os.remove(metaPath)
        return

