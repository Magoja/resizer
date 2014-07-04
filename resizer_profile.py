import os
import sys

MAXFILESIZE = 80 * 1024 # 50KB

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
          converted = ConvertPNG(inputFolder, fn)
          spaceSaved = spaceSaved + converted
        else:
          print "Skip '%s/%s' (%.0fKB)" % (inputFolder, fn, size / 1024)

    if count % 10 == 0:
      print "(%d/%d)" % (count, total)
  return spaceSaved

def ConvertPNG(inputFolder, fn):
  fullpath = "%s/%s" % (inputFolder, fn)
  sizeBefore = os.path.getsize(fullpath)
  os.system("convert %s -resize 100x100\\> %s" % (fullpath, fullpath))
  sizeAfter = os.path.getsize(fullpath)

  print "Convert '%s' File completed. (%.0fKB -> %.0fKB)" % (fullpath, sizeBefore / 1024, sizeAfter / 1024)
  return sizeBefore - sizeAfter


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage:"
    print "python resizer_profile.py (foldername)"
    print "  Profile size over 80kb, resize it to width 100"
  else:
    print "PNG image resizer. v0.1"
    print "  by Magoja 20140703"
    print "-----------------------"

    inputFolder = sys.argv[1]
    if inputFolder.endswith("/"):
      inputFolder = inputFolder[:-1]

    saved = IterateAndResize(inputFolder)

    print "Total %.1fMB saved" % (saved / 1024 / 1024)