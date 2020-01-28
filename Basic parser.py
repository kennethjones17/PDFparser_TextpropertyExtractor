import fitz
import pandas as pd
import re
from nltk.corpus import stopwords 

def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
        
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
        
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)

doc = fitz.open("webdownload.pdf")
page = doc[0]
labels = ['text','font', 'size', 'color']
df = pd.DataFrame(columns=labels)
punctuations = '''!()-[]{};:"\,<>./?$%^&*_~@#'''
i=0
stop_words = set(stopwords.words('english')) 
# read page text as a dictionary, suppressing extra spaces in CJK fonts
blocks = page.getText("dict", flags=11)["blocks"]
for b in blocks:  # iterate through the text blocks
    for l in b["lines"]:  # iterate through the text lines
        for s in l["spans"]:  # iterate through the text spans
            print("")
            font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                s["font"],flags_decomposer(s["flags"]),s["size"],s["color"])
            print("Text: '%s'" % s["text"])  # simple print of text
            k = re.split(' ',s["text"])
            if(len(k)>1):
                for i in k:
                    if i not in stop_words and i not in punctuations:
                        if i.isspace() == False:
                            if i:
                                df=df.append({'text':i,'font':s['font'],'size':s['size'],'color':s['color']},
                                                  ignore_index=True)
            else:
                df=df.append({'text':s['text'],'font':s['font'],'size':s['size'],'color':s['color']},
                                  ignore_index=True)
                