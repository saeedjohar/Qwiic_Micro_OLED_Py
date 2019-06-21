#-----------------------------------------------------------------------------
# moled_fonts.py
#
# Utilities to manage the fonts for the OLED display
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https:= www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:= www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
	
import sys
import os

import math

# Define storage for fonts

# map - map font index to font name
_fontIndexMap=[]

# font cache - maps name to font data
_fontCacheIndex = -1
_fontCache=None

_isInited = False



#-----------------------------------------
# Font Object - to manage a font

class MicroOLEDFont():

	def __init__(self, fontFile):
		self.width = 0
		self.height = 0
		self.start_char = 0
		self.total_char = 0
		self.map_width = 0

		# The font data is chunked - broken up into characters within a dictionary
		# Good for memory state (fragementation), but slightly slower.
		self._fontData = []

		self._loadFontFile(fontFile)

	def _loadFontFile(self, fontFile):

		fp = None

		try:
			fp = open(fontFile, 'rb')

		except Exception as exError:
			print("Error opening font file: %s" % fontFile)

			raise exError

		# read the font header
		fHeader = fp.read(6)
		self.width 		= fHeader[0]
		self.height 	= fHeader[1]
		self.start_char = fHeader[2]
		self.total_char = fHeader[3]
		self.map_width 	= fHeader[4]*100 + fHeader[5] #two bytes values into integer 16

		# build the list to store the fonts - list uses less mem than a dict. 
		self._fontData = [0]* (self.height//8 * self.total_char)	
		# Break font into rows - not as effeicent, but great for memory.
		# note: the fonts span rows - and each row is 8 bits. So i font height > 8,
		#       the font spans multiple rows.
		#
		# Double note: If the font is a single row - we add a byte to the row buffer
		#			   Seems no margin was encoded on this font, and this bust be added

		rowsPerChar = math.ceil(self.height/8)

		# do we add a pad byte?
		nPad = (rowsPerChar == 1)*1

		# read in font
		for iChar in range(self.total_char * rowsPerChar):

			try:
				self._fontData[iChar] = fp.read(self.width) + bytes( [0]*nPad )
			except Exception as exError:
				print("Error reading font data. Character: %d, File:%s" % (iChar, _loadFontFile))

				fp.close()
				# cascade this up
				raise exError

		fp.close()


	# method to override [] access for this object. 
	#
	# key => character index into the data. 

	def __getitem__(self, key):

		# key -> the absolute index into the font data array - not pretty, but that's fonts

		if key < 0 or key >= len(self._fontData):
			raise IndexError("Index (%d) out of range[0,%d]." % (key, len(self._fontData)))

		return self._fontData[key]


# handy util

def _getFontDir():

	return __file__.rsplit(os.sep, 1)[0] +  os.sep + "fonts"

#-----------------------------------------
# General Structure
#
# Fonts are stored in the fonts subfolder of this package. Uses filenames
# to deliniate the fonts.
#
# Name Structure
#      <fontnumber>_<fontname>.bin
#
# This system lists the filenames and builds the index map
#
# Only when font data is requested is the data loaded for that font.
# 
# 
def _initFontSystem():

	global _isInited, _fontIndexMap

	if _isInited:
		return

	_isInited = True

	fDir = _getFontDir()

	try: 
		tmpFiles = os.listdir(fDir)
	except:
		print("Micro OLED fonts do not exists - check your installation")
		return


	fontFiles = []

	for tFile in tmpFiles:
		if tFile.find('.bin') == -1:
			continue

		fontFiles.append(tFile)

	# get our font names 

	if len(fontFiles) == 0:
		print("Micro OLED - no fonts found")
		return


	# build our font index

	_fontIndexMap = [''] * len(fontFiles)

	for fBase in fontFiles:

		iSep = fBase.find('_')
		if iSep == -1:
			print("Invalid Font File: %s " % fBase)
			continue
		nFont = int(fBase[0:iSep])

		# stash the name, strip off the number and the suffix
		_fontIndexMap[nFont] = fBase[iSep+1:-4]

def count():

	if not _isInited:
		_initFontSystem()

	return len(_fontIndexMap)

def font_names():

	if not _isInited:
		_initFontSystem()

	return _fontIndexMap

def get_font(iFont):

	global _fontCache, _fontCacheIndex

	if not _isInited:
		_initFontSystem()

	if iFont != _fontCacheIndex:

		fFont = _getFontDir() + os.sep + str(iFont) + '_' + _fontIndexMap[iFont] + '.bin'

		_fontCache = MicroOLEDFont(fFont)
		_fontCacheIndex = iFont

	return _fontCache


