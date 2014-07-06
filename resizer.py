import os
import sys

MAXFILESIZE = 300 * 1024 # 300kb
IMAGEQUALITY = "80%"

def PrepareOriginalFolder(inputFolder, dryrun):
  if dryrun:
    os.system("mkdir %s/dry" % inputFolder)
  else:
    os.system("mkdir %s/original" % inputFolder)

def IterateAndResize(inputFolder, dryrun):
  spaceSaved = 0
  total = len(os.listdir("%s/" % inputFolder))
  count = 0
  print "Total %d files..." % total
  print "-----------------"

  for fn in os.listdir("%s/" % inputFolder):
    count = count + 1
    fullpath = "%s/%s" % (inputFolder, fn)
    if os.path.isfile(fullpath):
      if fullpath.lower().endswith(".jpg"):
        size = os.path.getsize(fullpath)
        if size > MAXFILESIZE:
          converted = ConvertJPG(inputFolder, fn, dryrun)
          spaceSaved = spaceSaved + converted
        else:
          print "Skip '%s/%s' (%.0fKB)" % (inputFolder, fn, size / 1024)
      elif fullpath.endswith(".gif"):
        ConvertGIF(inputFolder, fn, dryrun)

    if count % 10 == 0:
      print "(%d/%d)" % (count, total)
  return spaceSaved

def ConvertJPG(inputFolder, fn, dryrun):
  fullpath = "%s/%s" % (inputFolder, fn)
  sizeBefore = os.path.getsize(fullpath)
  message = ""
  if dryrun:
    os.system("convert %s -resize 970x970\\> %s/dry/%s" % (fullpath, inputFolder, fn))
    os.system("mogrify -quality 80%% %s/dry/%s" % (inputFolder, fn))
    sizeAfter = os.path.getsize("%s/dry/%s" % (inputFolder, fn))
    message = "DRYRUN: "
  else:
    os.system("convert %s -resize 970x970\\> %s.tmp" % (fullpath, fullpath))
    os.system("mogrify -quality 80%% %s.tmp" % fullpath)
    os.system("cp %s %s/original/%s" % (fullpath, inputFolder, fn))
    os.system("mv %s.tmp %s" % (fullpath, fullpath))
    sizeAfter = os.path.getsize(fullpath)

  print "%sConvert '%s' File completed. (%.0fKB -> %.0fKB)" % (message, fullpath, sizeBefore / 1024, sizeAfter / 1024)  
  return sizeBefore - sizeAfter

def ConvertGIF(inputFolder, fn, dryrun):
  fullpath = "%s/%s" % (inputFolder, fn)
  sizeBefore = os.path.getsize(fullpath)
  sizeAfter = 0
  message = ""
  if dryrun:
    os.system("cp %s %s/dry/%s" % (fullpath, inputFolder, fn))
    message = "DRYRUN: "
  else:
    os.system("mv %s %s/original/%s" % (fullpath, inputFolder, fn))

  print "%sMove '%s' File completed. (%.0fKB -> %.0fKB)" % (message, fullpath, sizeBefore / 1024, sizeAfter / 1024)  
  return sizeBefore - sizeAfter

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage:"
    print "python resizer.py (foldername) (-d)"
    print "  File jpg size over 300kb, resize it to width 970 and quality 80%"
    print "  and move original file under Origial folder"
    print "  -d option for dryrun"
  else:
    print "Jpg image resizer. v0.1"
    print "  by Magoja 20140702"
    print "-----------------------"

    dryrun = False
    if len(sys.argv) >= 3:
      dryrun = True

    inputFolder = sys.argv[1]
    if inputFolder.endswith("/"):
      inputFolder = inputFolder[:-1]

    PrepareOriginalFolder(inputFolder, dryrun)
    saved = IterateAndResize(inputFolder, dryrun)

    print "Total %.1fMB saved" % (saved / 1024 / 1024)
