# define pattern to match the html content
# store in csv file
import re
import os
import csv

def open_csv():
    csv_file = open('text.csv','w')
    fieldnames = ['Incorrect', 'Correct', 'Suggestion']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    return writer


# matches general mistakes
def match_pattern1(c,w):
    pattern = re.findall('<p><strong>[0-9].*?</strong></p>.*?<p>.*?:.*?</p>', c, re.DOTALL)
    if pattern is not None:
        for p in pattern:
            # sel = Selector(text=p, type="html")
            # print(sel.xpath('//p//text()').extract_first())
            sub_pattern = re.match('<p><strong>[0-9].(.*?)</strong></p>.*?<p>(.*?): (.*?)</p>', p, re.DOTALL)

            if sub_pattern is not None:
                clean = re.compile('<.*>|\n+')
                # suggestion = re.sub(clean, '', sub_pattern.group(2))

                w.writerow(
                    {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                     'Correct': re.sub(clean, '', sub_pattern.group(3)), \
                     'Suggestion': re.sub(clean, '', sub_pattern.group(2))})


def match_pattern2(c,w):
    pattern = re.findall('<p>incorrect:.*?correct:.*?</p>.*?<p>.*?</p>', c, re.DOTALL | re.IGNORECASE)
    if pattern is not None:
        for p in pattern:
            sub_pattern = re.match('<p>incorrect:(.*?)correct:(.*?)</p>.*?<p>(.*?)</p>', p, re.DOTALL | re.IGNORECASE)
            clean = re.compile('<.*>|\n+')
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
            clean = re.compile('<.*?>|\n+')
            if sub_pattern is not None:
                w.writerow(
                    {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                     'Correct': re.sub(clean, '', sub_pattern.group(3)), \
                     'Suggestion': re.sub(clean, '', sub_pattern.group(2))})


# matches verb mistakes
def match_pattern4(c, w):
    check_title_and_get_suggestion = re.search('<h1>verb\s+mistakes.*?</h1>.*?<p>(.*?)</p>', c)
    if check_title_and_get_suggestion is not None:
        pattern = re.findall('<p>INCORRECT.*?:.*CORRECT.*?:.*?.</p>', c, re.DOTALL)
        if pattern is not None:
            for p in pattern:
                sub_pattern = re.match('<p>INCORRECT.*?:(.*?)CORRECT.*?:(.*?)</p>', p, re.DOTALL)
                clean = re.compile('<.*?>|\n+')
                if sub_pattern is not None:
                    w.writerow(
                        {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                         'Correct': re.sub(clean, '', sub_pattern.group(2)), \
                         'Suggestion': re.sub(clean, '', check_title_and_get_suggestion)})


# matches verb mistakes
def match_pattern5(c, w):
    check_title_and_get_suggestion = re.search('<h1>verb\s+mistakes.*?</h1>.*?<p>(.*?)</p>', c, re.IGNORECASE)
    if check_title_and_get_suggestion is not None:
        pattern = re.findall('<p><strong>Incorrect.*?:.*?</strong>.*?<strong>Correct.*:.*?</strong>.*?</p>', c, re.DOTALL)
        if pattern is not None:
            for p in pattern:
                sub_pattern = re.match('<p><strong>Incorrect.*?:.*?</strong>(.*?)<strong>Correct.*:.*?</strong>(.*?)</p>', p, re.DOTALL)
                clean = re.compile('<.*?>|\n+')
                if sub_pattern is not None:
                    w.writerow(
                        {'Incorrect': re.sub(clean, '', sub_pattern.group(1)), \
                         'Correct': re.sub(clean, '', sub_pattern.group(2)), \
                         'Suggestion': re.sub(clean, '', check_title_and_get_suggestion)})

# match content with answers at the end
def match_pattern6(c,w):

    pattern1 = re.findall('<p><strong>\d.*?</strong>.*?[a]\).*?[b]\).*?</p>', c,
                          re.DOTALL | re.IGNORECASE | re.MULTILINE)
    pattern2 = re.findall('<p>\d.*?<strong>[a-z]\).*?</strong></p>.*?<p>.*?</p>', c, re.DOTALL|re.IGNORECASE|re.MULTILINE)

    if pattern1 and pattern2:
        for p1,p2 in zip(pattern1,pattern2):
            sub_pattern1 = re.match('<p><strong>\d.*?</strong>.*?[a]\)(.*?)[b]\)(.*?)</p>',
                                   p1, re.DOTALL|re.IGNORECASE|re.MULTILINE)

            sub_pattern2 = re.match('<p>\d.*?<strong>[a-z]\)(.*?)</strong></p>.*?<p>(.*?)</p>',
                                    p2, re.DOTALL|re.IGNORECASE|re.MULTILINE)

            if sub_pattern2.group(1) != sub_pattern1.group(1):
                incorrect = sub_pattern1.group(1)
            elif sub_pattern2.group(1) != sub_pattern1.group(2):
                incorrect = sub_pattern1.group(2)

            clean = re.compile('<.*?>|\n+')
            w.writerow(
                {'Incorrect': re.sub(clean, '', incorrect), \
                 'Correct': re.sub(clean, '', sub_pattern2.group(1)), \
                 'Suggestion': re.sub(clean, '', sub_pattern2.group(2))})


def main(path_to_file_dir):
    # get files from the directory
    if os.path.exists(path_to_file_dir):
        file_list = sorted(os.listdir(path_to_file_dir))
        # get a list of files ending in 'html'
        file_list = [file_name for file_name in file_list if file_name.endswith('.html')]

        writer = open_csv()

        # pattern_list = []

        # loop through the files in file list and match the pattern
        if file_list is not None:
            for file_name in file_list:
                path_to_file = os.path.join(path_to_file_dir, file_name)
                html_file = open(path_to_file, 'r')
                print path_to_file
                content = html_file.read()
                html_file.close()
                print content
                if re.search('<h2>Answers\s+and\s+Explanations.*?</h2>', content, re.DOTALL | re.IGNORECASE):
                    match_pattern6(content, writer)
                else:
                    match_pattern1(content, writer)
                match_pattern2(content, writer)
                match_pattern3(content, writer)
                match_pattern4(content, writer)
                match_pattern5(content, writer)
    else:
        print('Path does not exist. Please correct the path.')


if __name__ == "__main__":
    cwd = os.getcwd()
    path_to_file_dir = "%s/data/" % (cwd)
    main(path_to_file_dir)

