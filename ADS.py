from ctypes import *
import os, sys

kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]

class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    '''
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]

class ADS:    # Alternate Data Streams
	
	def __init__(self, filename):
		
		self.filename = filename
		self.streams = self.initStreams()
	
	def __iter__(self): return iter(self.streams)
	
	def initStreams(self):
		
		'''
		HANDLE WINAPI FindFirstStreamW(
		  __in        LPCWSTR lpFileName,
		  __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
		  __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
		  __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
		);
		https://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
		'''
		
		file_infos = WIN32_FIND_STREAM_DATA()
		streamlist = list()
		
		findFirstStreamW = kernel32.FindFirstStreamW
		findFirstStreamW.restype = c_void_p
		
		myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
		
		p = c_void_p(myhandler)
		
		if file_infos.cStreamName:
			streamname = file_infos.cStreamName.split(":")[1]
			if streamname: streamlist.append(streamname)

			while kernel32.FindNextStreamW(p, byref(file_infos)):
				streamlist.append(file_infos.cStreamName.split(":")[1])
		
		kernel32.FindClose(p)  # Close the handle
		
		return streamlist
	
	def hasStreams(self): return len(self.streams) > 0
	
	def fullFilename(self, stream): return f'{self.filename}:{stream}'
	
	def addStreamFromFile(self, filename):
		if os.path.exists(filename):
			with open(filename, 'rb') as f:
				content = f.read()
			return self.addStreamFromString(filename, content)
		else:
			print(f'Could not find file: {filename}')
			return False
	
	def addStreamFromString(self, stream_name, string):
		fullname = self.fullFilename(os.path.basename(stream_name))
		if os.path.exists(fullname):
			print('Stream name already exists')
			resp = input('Do you want to replace content? [y/n]: ')
			if not resp.lower() in ['y', 'yes']:
				return False
		fd = open(fullname, 'wb')
		fd.write(string)
		fd.close()
		if not stream_name in self.streams:
			self.streams.append(stream_name)
		return True
	
	def deleteStream(self, stream):
		try:
			os.remove(self.fullFilename(stream))
			self.streams.remove(stream)
			return True
		except:
			return False
	
	def getStreamContent(self, stream):
		fd = open(self.fullFilename(stream), 'rb')
		content = fd.read()
		fd.close()
		return content


if __name__ == '__main__':
	
	ads = ADS('README.md')
	print(ads.streams)
	stream = ads.getStreamContent(ads.streams[0])
	print(stream)
