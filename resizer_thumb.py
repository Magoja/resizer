import os
import sys

MAXFILESIZE = 5 * 1024 # 5KB

def IterateAndResize(inputFolder):
  spaceSaved = 0
  total = len(os.listdir("%s/" % inputFolder))
  count = 0
  print "Total %d files..." % total
  print "-----------------"

  for fn in os.listdir("%s/" % inputFolder):
    count = count + 1
    fullpath = "%s/%s" % (inputFolder, fn)
    if os.path.isfile(fullpath):
      if fn.find(".") == -1:
        size = os.path.getsize(fullpath)
        if size > MAXFILESIZE:
          converted = ConvertThumb(inputFolder, fn)
          spaceSaved = spaceSaved + converted
        else:
          print "Skip '%s/%s' (%.0fKB)" % (inputFolder, fn, size / 1024)

    if count % 10 == 0:
      print "(%d/%d)" % (count, total)
  return spaceSaved

def ConvertThumb(inputFolder, fn):
  fullpath = "%s/%s" % (inputFolder, fn)
  sizeBefore = os.path.getsize(fullpath)
  os.system("convert %s %s.jpg" % (fullpath, fullpath))
  os.system("mv %s.jpg %s")
  sizeAfter = os.path.getsize(fullpath)

  print "Convert '%s' File completed. (%.0fKB -> %.0fKB)" % (fullpath, sizeBefore / 1024, sizeAfter / 1024)
  return sizeBefore - sizeAfter

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage:"
    print "python resizer_thumb.py (foldername)"
  else:
    print "Thumb image resizer. v0.1"
    print "  by Magoja 20140703"
    print "-----------------------"

    inputFolder = sys.argv[1]
    if inputFolder.endswith("/"):
      inputFolder = inputFolder[:-1]

    saved = IterateAndResize(inputFolder)

    print "Total %.1fMB saved" % (saved / 1024 / 1024)
