# define pattern to match the html content
# store in csv file
import re
import os
import csv

path_to_file_dir = "/home/ashok/project/thesis/ukp/parser"


def open_csv():
    csv_file = open('text.csv','w')
    fieldnames = ['Incorrect', 'Correct', 'Suggestion']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    return writer


def match_pattern1(c,w):
    pattern = re.findall('<p><strong>[0-9].*?</strong></p>.*?<p>.*?:.*?</p>', c, re.DOTALL)
    if pattern is not None:
        for p in pattern:
            # sel = Selector(text=p, type="html")
            # print(sel.xpath('//p//text()').extract_first())
            sub_pattern = re.match('<p><strong>[0-9].(.*?)</strong></p>.*?<p>(.*?): (.*?)</p>', p, re.DOTALL)
            clean = re.compile('<.*?>')

            if sub_pattern is not None:
                w.writerow(
                    {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                     'Correct': re.sub(clean, '', sub_pattern.group(3)), \
                     'Suggestion': re.sub(clean, '', sub_pattern.group(2))})

def match_pattern2(c,w):
    pattern = re.findall('<p>incorrect:.*?correct:.*?</p>.*?<p>.*?</p>', c, re.DOTALL | re.IGNORECASE)
    if pattern is not None:
        for p in pattern:
            sub_pattern = re.match('<p>incorrect:(.*?)correct:(.*?)</p>.*?<p>(.*?)</p>', p, re.DOTALL | re.IGNORECASE)
            clean = re.compile('<.*?>')
            if sub_pattern is not None:
                w.writerow(
                    {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                     'Correct': re.sub(clean, '', sub_pattern.group(3)),\
                     'Suggestion': re.sub(clean, '', sub_pattern.group(2))})


def match_pattern3(c,w):
    pattern = re.findall('<p>.*?<strong>original.*?:</strong>.*?<strong>correct.*?:</strong>.*?</p>.*?<p>.*?</p>',\
                         c, re.DOTALL | re.IGNORECASE)

    if pattern is not None:
        for p in pattern:
            sub_pattern = re.match('<p>.*?<strong>original.*?:</strong>(.*?)<strong>correct.*?:</strong>(.*?)</p>.*?<p>(.*?)</p>',\
                                   p, re.DOTALL | re.IGNORECASE)
            clean = re.compile('<.*?>')
            if sub_pattern is not None:
                w.writerow(
                    {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                     'Correct': re.sub(clean, '', sub_pattern.group(3)), \
                     'Suggestion': re.sub(clean, '', sub_pattern.group(2))})


def main():
    # get files from the directory
    if os.path.exists(path_to_file_dir):
        file_list = sorted(os.listdir(path_to_file_dir))
        # get a list of files ending in 'html'
        file_list = [file for file in file_list if file.endswith('.html')]

        writer = open_csv()

        # loop through the files in file list and match the pattern
        if file_list is not None:
            for file in file_list:
                path_to_file = os.path.join(path_to_file_dir+file)
                html_file = open(path_to_file, 'r')
                content = html_file.read()
                html_file.close()
                match_pattern1(content, writer)
                match_pattern2(content, writer)
                match_pattern3(content, writer)


if __name__ == "__main__":
    main()



