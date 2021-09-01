# Your imports go here
import re
import logging
import json

logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount
    Parameters:
    dirpath (str): directory path containing receipt and ocr output
    Returns:
    float: returns the extracted amount
    '''

def extract_amount(dirpath: str) -> float:
    logger.info('extract_amount called for dir %s', dirpath)
    with open(dirpath + "/ocr.json","r",encoding='utf-8') as file:
        data = file.read()
        file = json.loads(data)
    blocks = file['Blocks']
    substrng = {"purchase","amount paid","total","total:","theater and dance","order total","paid","payment","credit","debit"}
    for m,_ in enumerate(reversed(blocks)):
        try:
            if blocks[m]['Text'].lower() in substrng:
                a = 1
                while a<=2:
                    if any(i.isdigit() for i in blocks[m+a]['Text']) and blocks[m+a]['Text'].find('/')==-1 and blocks[m+a]['Text']!="1" and blocks[m+a]['Text'].find('-')==-1 :
                        amount = blocks[m+a]['Text'].replace(",", "")
                        return float(re.sub("[^0123456789.]","",amount))
                    elif(blocks[m-1]['Text'] == '$') and len(blocks[m-1]['Text']) == 1:
                        amount = blocks[m-2]['Text'].replace(",", "")
                        return float(amount)
                    else:
                        a+=1
                        
                        
        except KeyError:
            pass
    return float(amount)
