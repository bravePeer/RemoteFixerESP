from xml.etree.ElementInclude import include
import gzip
import os
import shutil

PATH_WEBSITE_HTML = "src/website/site.html"
PATH_WEBSITE_GZIP = "src/website/site.gzip"
PATH_WEBSITE_INCLUDE = "include/readysite.h"

def generateIncludeFromHTML():
    fin = open(PATH_WEBSITE_HTML, "r") 
    fout = open(PATH_WEBSITE_INCLUDE, "w")
    tmp = os.stat(PATH_WEBSITE_HTML).st_size
    fout.write(f'const size_t websiteSize = {tmp};\n')
    fout.write('const char websiteContent[] PROGMEM = R"=====(\n')
    for line in fin:
        fout.write(line)
    fout.write('\n)=====";')

def generateIncludeFromGZIP():
    fin = open(PATH_WEBSITE_GZIP, "rb") 
    fout = open(PATH_WEBSITE_INCLUDE, "w")
    tmp = os.stat(PATH_WEBSITE_GZIP).st_size
    fout.write(f'const size_t websiteSize = {tmp};\n')
    fout.write('const char websiteContent[] PROGMEM = {\n')
    
    while 1:
        data = fin.read(1024)
        for i in data:
            fout.write(f'{i},')
        if not data:
            break

    fout.write('};')

def compressWebsite():
    with open(PATH_WEBSITE_HTML, 'rb') as f_in:
        with gzip.open(PATH_WEBSITE_GZIP, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def printStats():
    website_html_size = os.stat(PATH_WEBSITE_HTML).st_size
    website_gzip_size = os.stat(PATH_WEBSITE_GZIP).st_size
    print("Website size:")
    print("html:", website_html_size)
    print("gzip:", website_gzip_size)
    print("Compression: ", website_html_size / website_gzip_size)

print("=====Generating=====")
# generateIncludeFromHTML()
compressWebsite()
printStats()
generateIncludeFromGZIP()
print("========Done========")
