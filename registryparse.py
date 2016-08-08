import sys
import os
import base64
from Registry import Registry
import argparse
import calendar
import time
import binascii


reload(sys)
# Sets encoding
sys.setdefaultencoding('utf-8')
parser = argparse.ArgumentParser(description='Processes Registry Hives into relatively somewhat ok CSVs.')
parser.add_argument('-f','--filename', help='Parse a specific registry file')
parser.add_argument('-d','--directory', help='Parse everything in a folder')
args = parser.parse_args()
if args.filename == None and args.directory == None:
	parser.print_help()
	exit(1)

def determine_type(valtype):
	if valtype == Registry.RegSZ:
		return "RegSZ"
	elif valtype == Registry.RegExpandSZ:
		return "RegExSZ"
	elif valtype == Registry.RegBin:
		return "RegBin"
	elif valtype == Registry.RegDWord:
		return "RegDWord"
	elif valtype == Registry.RegNone:
		return "RegNone"
	elif valtype == Registry.RegLink:
		return "RegLink"
	elif valtype == Registry.RegFullResourceDescriptor:
		return "RegFullResourceDescriptor"
	elif valtype == Registry.RegQWord:
		return "RegQWord"
	elif valtype == Registry.RegResourceRequirementsList:
		return "RegResourceRequirementsList"
	elif valtype == Registry.RegResourceList:
		return "RegResourceList"
	elif valtype == Registry.RegMultiSZ:
		return "RegMultiSZ"
	else:
		return "N/A"

def clean(valuedata, valtype):
	# Specify what to do with common key types
	if determine_type(valtype) is "RegSZ" or "RegLink" or "RegResourceRequirementsList" or "RegResourceList" or "RegFullResourceDescriptor" or "RegExSZ" or "RegMultiSZ":
		return valuedata
	elif determine_type(valtype) is "RegDWord" or "RegQWord":
		return valuedata
	# If I don't know what to do, try to base64 it and if it's not ok with that (it'd be bc it's an int), return it
	else:
		try:
			return binascii.b2a_base64(valuedata)
		except TypeError:
			return valuedata

def change(timestamp):
	return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def rec(key, depth=0, resultname="output_default.csv"):
	
	
	for valueiter in key.values():
		if valueiter.value_type() is Registry.RegBin:
			f.write("{},{},{},{},{}\n".format(key.path(), change(key.timestamp()), valueiter.name(), determine_type(valueiter.value_type()), binascii.b2a_base64(valueiter.value()).replace('\n', '')))
		elif valueiter.value_type() is Registry.RegResourceRequirementsList:
			f.write("{},{},{},{},{}\n".format(key.path(), change(key.timestamp()), valueiter.name(), determine_type(valueiter.value_type()), binascii.b2a_base64(valueiter.value()).replace('\n', '')))
		elif valueiter.value_type() is Registry.RegResourceList:
			f.write("{},{},{},{},{}\n".format(key.path(), change(key.timestamp()), valueiter.name(), determine_type(valueiter.value_type()), binascii.b2a_base64(valueiter.value()).replace('\n', '')))
		else:
			f.write("{},{},{},{},{}\n".format(key.path(), change(key.timestamp()), valueiter.name(), determine_type(valueiter.value_type()), clean(valueiter.value(), valueiter.value_type())))
	for subkey in key.subkeys():
		rec(subkey, depth + 1, resultname)

if args.filename != None:
	resultname = "{}_{}.csv".format(os.path.basename(args.filename),str(calendar.timegm(time.gmtime())))
	f = open(resultname, 'a+')
	f.write("Path, Timestamp, Key Name, Key Type, Key Data\n")
	reg = Registry.Registry(args.filename)
	rec(reg.root(), 0, resultname)
	print "{} {}".format("Written data to",str(resultname))

if args.directory != None:

	directory = "{}{}".format("output_",calendar.timegm(time.gmtime()))
	if not os.path.exists(directory):
	    os.makedirs(directory)
	(_, _, filenames) = os.walk(args.directory).next()
	for file in filenames:
		reg = Registry.Registry(args.directory+"/"+file)
		resultname = directory+"/"+str(file+"_"+str(calendar.timegm(time.gmtime()))+".csv")
		f = open(resultname, 'a+')
		f.write("Path, Timestamp, Key Name, Key Type, Key Data")
		rec(reg.root(), 0, resultname)
		f.close()
		print "Written data to "+str(resultname)

