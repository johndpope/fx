import pickle
import importlib
import logging
import os
import pickle
import re
import sys
import tempfile
import time
import zipfile

import backtrader as bt
import pycommon
from fxclient.data.test_data_source import TestDataSource
from kazoo.client import KazooClient
from fxclient.data.test_data_source import TestDataSource


pickle_file_path = "/tmp/strategt.zip"

x = pickle.load( open(pickle_file_path, "rb") )
x.plot()
print(x)
