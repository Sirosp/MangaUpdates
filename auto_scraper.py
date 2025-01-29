from autoscraper import AutoScraper
import re

url = "https://manhuatop.org/manhua/worthless-regression-series/#page-1"
regex_pattern = re.compile(r'(?i)Chapter\s*\d+[^\s<]*')
wanted_list = [regex_pattern]
scraper = AutoScraper()
result = scraper.build(url,wanted_list)
print(result, "\n####################")

def determine_sequence(result):
    length = len(result)
    cut_point = None
    for i in range(length - 1, 0 , -1):
       
        chap_current = int(re.findall(r"\d+", result[i])[0])
        chap_next = int(re.findall(r"\d+", result[i-1])[0])
     
        if chap_next - chap_current != 1 and chap_next - chap_current not in range(0,1):
            print("found irregula \n")
            print(chap_current, "\n", chap_next,"\n")
            cut_point = i
            break
    if cut_point is not None:
        print("CUTTING\n")
        print(length, cut_point, "\n")
       
        del result[cut_point:]

    print(result)

determine_sequence(result)
