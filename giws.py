#!/usr/bin/python -u
#
# Matthieu WALTER - <gamo@tecp.info>
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
#
# This software is a computer program whose purpose is to generate C++ wrapper
# for Java objects/methods.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# For more information, see the file COPYING

import sys
import getopt
import os.path

from parseXMLEngine import parseXMLEngine
from configGiws import configGiws
from CXXFile import CXXFile
from CXXException import CXXException


class giws:
	config=configGiws()
	templateObj = None
	def __init__(self, argv=sys.argv):
		self.argv = argv
		self.config.setFullCommandLine(argv[1:])

		try:
			self.__parse_cmdline()
		except getopt.GetoptError as e:
			print ("%s: %s"%(e.__class__.__name__, str(e)))
			self.show_help(1)    # exit with EXIT_FAILURE return code

	"""
	load configuration from command line parameters
	"""
	def __parse_cmdline(self):
		opts, args = getopt.getopt(self.argv[1:], "f:o:b:gprsehv", ["description-file=","output-dir=","header-extension-file=","body-extension-file=","generate-exception-class","per-package","throws-exception-on-error","disable-return-size-array","enable-return-size-array","help","version"])

		# we know at least one options is required (-f file...)
		if len(opts)==0:
			raise getopt.GetoptError( "too few options")
		elif len(args):
			raise getopt.GetoptError( "too many arguments")

		for option, value in opts:
			if option in ("-f", "--description-file"):
				if os.path.isfile(value):
					self.config.setDescriptionFile(value)
				else:
					print("Deadly error: Cannot find file %s" % value)
					print ("")
					self.show_help(0)

			elif option in ("-o", "--output-dir"):
				if os.path.isdir(value):
					self.config.setOutput(value)
				else:
					print("Deadly error: Cannot find output dir %s" % value)
					print("")
					self.show_help(0)

			elif option in ("-p", "--per-package"):
				self.config.setSplitPerObject(False)

			elif option in ("-e","--throws-exception-on-error"):
				self.config.setThrowsException(True)

			elif option in ("-g","--generate-exception-class"):
				self.config.enableGenerateExceptionClass()

			elif option in ("-r","--disable-return-size-array"):
				self.config.setDisableReturnSize()

			elif option in ("-s","--enable-return-size-array"):
				self.config.setEnableReturnSize()

			elif option == '--header-extension-file':
				self.config.setCPPHeaderExtension(value)

			elif option == '--body-extension-file':
				self.config.setCPPBodyExtension(value)

			elif option in ("-v", "--version"):
				self.show_version(0)

			elif option in ("-h", "--help"):
				self.show_help(0)

		# check for some mandatory paramters
		if not self.config.getDescriptionFile() and not self.config.generateExceptionClass():
			raise getopt.GetoptError( "You have to specify a description file")

		if self.config.getDescriptionFile():
			templateObj=parseXMLEngine(self.config.getDescriptionFile())

			CXX=CXXFile(templateObj.getJpackage())
			CXX.generateCXXHeader(self.config)
			CXX.generateCXXBody(self.config)

		# this will be changed ... should not be called on the package itself
		#		.generateCXXHeader(self.config)
		#		templateObj.getJpackage().generateCXXBody(self.config)
		if self.config.generateExceptionClass():
			CXXExcep=CXXException()
			CXXExcep.generateCXXHeader(self.config)
			CXXExcep.generateCXXBody(self.config)


	def show_help(self, exit_status=0):
		print("Giws usage: %s <-f file|--description-file=file> [options]" % self.argv[0])
		print("")
		print("Options can be:")
		print("-f     --description-file=file    Description of the method of the Java Object")
		print("-o     --output-dir=dir           The directory where to export files")
		print("-p     --per-package              Generates CXX/HXX files per package")
		print("-e     --throws-exception-on-error       Throws a C++ exception instead of an exit(EXIT_FAILURE)")
		print("-g     --generate-exception-class        Generate the exception class (disable by default)")
		print(
			"-r     --disable-return-size-array       Disable the return of the size of the array/arrays through int*")
		print(
			"-s     --enable-return-size-array        Enable the return of the size of the array/arrays through int* (default)")
		print("--header-extension-file=ext       Specify the extension of the header file generated [Default : .hxx]")
		print("--body-extension-file=ext         Specify the extension of the body file generated [Default : .cpp]")
		print("-v     --version                  Display the version information")
		print("-h     --help                     Display the help")

		sys.exit(exit_status)

	def show_version(self, exit_status=0):
		print("GIWS %s" % self.config.getVersion())
		print("Copyright (C) 2007-2012 INRIA / Digiteo / Scilab Enterprises")
		print("""This software is governed by the CeCILL license under French law and
abiding by the rules of distribution of free software. You can use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
http://www.cecill.info/ . """)
		print("")
		print("Written by Sylvestre Ledru <sylvestre.ledru@scilab.org>")
		print("with the help of various developers.")
		sys.exit(exit_status)

if __name__ == '__main__':
	giws()

