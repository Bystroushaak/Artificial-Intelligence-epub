#! /usr/bin/env bash

which pip > /dev/null 2>&1
if [ $? -eq 1 ]; then
    echo "This script requires 'python-pip' package."
    sudo aptitude install python-pip || exit
fi

which ebook-convert > /dev/null 2>&1
if [ $? -eq 1 ]; then
    echo "This script requires 'calibre' package."
    sudo aptitude install calibre || exit
fi

python -c "import dhtmlparser" 
if [ $? -eq 1 ]; then
    echo "This script requires 'pydhtmlparser' python package."
    sudo pip install pydhtmlparser || exit
fi

python -c "import httpkie"
if [ $? -eq 1 ]; then
    echo "This script requires 'httpkie' python package."
    sudo pip install httpkie || exit
fi

echo "Downloading ebook data from web.."

cd Artificial_intelligence/OEBPS
python generate_epub.py

echo "Aplying patch for metadata.."

python -c "print open('content.opf').read().split('</metadata>')[-1]" > fix
cat ../../metadata_header.txt > content.opf
cat fix >> content.opf
rm fix

echo "Packing epub file.."
cd ..
zip -rg ../Artificial_intelligence_broken.epub mimetype .
cd ..

echo "Fixing problems with ebook.."
ebook-convert Artificial_intelligence_broken.epub Artificial_intelligence.epub
rm Artificial_intelligence_broken.epub