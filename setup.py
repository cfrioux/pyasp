# Copyright (c) 2012, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of pyasp.
#
# pyasp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyasp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyasp.  If not, see <http://www.gnu.org/licenses/>.import random

# -*- coding: utf-8 -*-
#from distutils.core import setup
from setuptools import setup
import os
import sys
import platform
import distutils
import site
import urllib
import sysconfig

from setuptools.command.install import install as _install

class install(_install):
    def get_binaries(self, path):
        BASE_URL = "http://www.cs.uni-potsdam.de/~sthiele/bioasp/downloads/bin/"
        architecture = platform.architecture()[0][:-3]
        if sys.platform == 'darwin':
            if architecture == '32':
                print "clasp/claspD/gringo binaries are not yet available for Mac OS 32bits"
                exit()
                
            CLASP_URL = BASE_URL + "macos/clasp"
            CLASPD_URL = BASE_URL + "macos/claspD"
            GRINGO_URL = BASE_URL + "macos/gringo"
        else:
            CLASP_URL = BASE_URL + "linux-%s/clasp" % architecture
            CLASPD_URL = BASE_URL + "linux-%s/claspD" % architecture
            GRINGO_URL = BASE_URL + "linux-%s/gringo" % architecture
        
        urllib.urlretrieve(CLASP_URL, path + "/clasp")
        urllib.urlretrieve(CLASPD_URL, path + "/claspD")
        urllib.urlretrieve(GRINGO_URL, path + "/gringo")
        
    def run(self):
        _install.run(self)
        
        if '--user' in sys.argv[-1] :
            userdir = site.getusersitepackages()+"/pyasp/bin" 
            self.get_binaries(userdir)
            cmd="chmod +x "+userdir+"/*"
            print cmd
            os.system(cmd)
        else :
            py_version = "%s.%s" % (sys.version_info[0], sys.version_info[1])
            path1 = sys.prefix+"/lib/python%s/dist-packages/pyasp/bin" % py_version
            path2 = sys.prefix+"/lib/python%s/site-packages/pyasp/bin" % py_version
            path3 = sys.prefix+"/local/lib/python%s/dist-packages/pyasp/bin" % py_version
            path4 = sys.prefix+"/local/lib/python%s/site-packages/pyasp/bin" % py_version

            cmd = None
            if os.path.exists(path1):
                self.get_binaries(path1)
                cmd = "chmod +x "+path1+"/*"
            elif os.path.exists(path2):
                self.get_binaries(path2)
                cmd = "chmod +x "+path2+"/*"
            elif os.path.exists(path3):
                self.get_binaries(path3)
                cmd = "chmod +x "+path3+"/*"
            elif os.path.exists(path4):
                self.get_binaries(path4)
                cmd = "chmod +x "+path4+"/*"
            else:
                print "pyasp binaries path not found. You need to download and put in place the binaries for gringo, clasp and claspD in order to start using pyasp."
            
            if cmd:
                print cmd
                os.system(cmd)
                
setup(
    cmdclass={'install': install},
    name = 'pyasp',
    version = '1.0dev',
    url='http://pypi.python.org/pypi/pyasp/',
    license='GPLv3+',   
    description='A convenience wrapper for the ASP tool gringo, clasp, claspD',
    long_description=open('README').read(),
    author='Sven Thiele',
    author_email='sthiele78@gmail.com', 
    
    package_dir = { 'pyasp' : 'src'},
    package_data = {
        'pyasp' : ['query/*/*.gringo','query/*/*.lp','bin/*.txt']
    },
    packages = [
        'pyasp', 
        'pyasp.data', 
        'pyasp.ply',
        'pyasp.query',
    ]
)
