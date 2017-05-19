# define pattern to match the html content
# store in csv file
import re
import os
import csv
import json

def open_csv():
    csv_file = open('text.csv','w')
    fieldnames = ['Url', 'Incorrect', 'Correct', 'Suggestion']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    return writer


# matches general mistakes, consisting incorrect sentence in bold text
# and correct with in paragraph
# and suggestion after colon(:) within double quotes
def match_pattern1(url,c,w):
    pattern = re.findall('<p><strong>[0-9].*?</strong></p>.*?<p>.*?:.*?</p>', c, re.DOTALL)

    if len(pattern):
        for p in pattern:
            sub_pattern = re.match('<p><strong>[0-9].(.*?)</strong></p>.*?<p>(.*?): (.*?)</p>', p, re.DOTALL)
            if sub_pattern is not None:
                clean = re.compile('<.*>|\n+')
                sub_pattern.group(3)
                w.writerow({'Url': url,
                            'Incorrect': re.sub(clean, '', sub_pattern.group(1)),
                            'Correct': re.sub(clean, '', sub_pattern.group(3)),
                            'Suggestion': re.sub(clean, '', sub_pattern.group(2))
                            })
        return True

    return False



def match_pattern2(url,c,w):
    pattern = re.findall('<p>incorrect:.*?correct:.*?</p>.*?<p>.*?</p>', c, re.DOTALL | re.IGNORECASE)
    if len(pattern):
        for p in pattern:
            sub_pattern = re.match('<p>incorrect:(.*?)correct:(.*?)</p>.*?<p>(.*?)</p>', p, re.DOTALL | re.IGNORECASE)
            clean = re.compile('<.*>|\n+')
            if sub_pattern is not None:
                w.writerow({'Url': url,
                            'Incorrect': re.sub(clean, '', sub_pattern.group(1)),
                            'Correct': re.sub(clean, '', sub_pattern.group(3)),
                            'Suggestion': re.sub(clean, '', sub_pattern.group(2))
                            })
        return True

    return False


def match_pattern3(url,c,w):
    pattern = re.findall('<p>.*?<strong>original.*?:</strong>.*?<strong>correct.*?:</strong>.*?</p>.*?<p>.*?</p>',
                         c, re.DOTALL | re.IGNORECASE)


    if len(pattern):
        for p in pattern:
            sub_pattern = re.match(
                        '<p>.*?<strong>original.*?:</strong>(.*?)<strong>correct.*?:</strong>(.*?)</p>.*?<p>(.*?)</p>',
                         p, re.DOTALL | re.IGNORECASE)
            clean = re.compile('<.*?>|\n+')
            if sub_pattern is not None:
                w.writerow({'Url': url,
                            'Incorrect': re.sub(clean, '', sub_pattern.group(1)),
                            'Correct': re.sub(clean, '', sub_pattern.group(3)),
                            'Suggestion': re.sub(clean, '', sub_pattern.group(2))
                            })
        return True

    return False

# matches verb mistakes
def match_pattern4(url,c, w):
    check_title_and_get_suggestion = re.search('<h1>verb\s+mistakes.*?</h1>.*?<p>(.*?)</p>', c)
    if check_title_and_get_suggestion is not None:
        pattern = re.findall('<p>INCORRECT.*?:.*CORRECT.*?:.*?.</p>',
                             c,
                             re.DOTALL)

        if len(pattern):
            for p in pattern:
                sub_pattern = re.match('<p>INCORRECT.*?:(.*?)CORRECT.*?:(.*?)</p>', p, re.DOTALL)
                clean = re.compile('<.*?>|\n+')
                if sub_pattern is not None:
                    w.writerow(
                        {'Url' : url,
                         'Incorrect': re.sub(clean, '', sub_pattern.group(1)),
                         'Correct': re.sub(clean, '', sub_pattern.group(2)),
                         'Suggestion': re.sub(clean, '', check_title_and_get_suggestion)
                        })
        return True

    return False


# matches verb mistakes
def match_pattern5(url, c, w):
    check_title_and_get_suggestion = re.search('<h1>verb\s+mistakes.*?</h1>.*?<p>(.*?)</p>', c, re.IGNORECASE)
    if check_title_and_get_suggestion is not None:
        pattern = re.findall('<p><strong>Incorrect.*?:.*?</strong>.*?<strong>Correct.*:.*?</strong>.*?</p>',
                             c,
                             re.DOTALL)

        if len(pattern):
            for p in pattern:
                sub_pattern = re.match('<p><strong>Incorrect.*?:.*?</strong>(.*?)<strong>Correct.*:.*?</strong>(.*?)</p>',
                                       p,
                                       re.DOTALL)

                clean = re.compile('<.*?>|\n+')
                if sub_pattern is not None:
                    w.writerow(
                        {'Url' : url,
                         'Incorrect': re.sub(clean, '', sub_pattern.group(1)),
                         'Correct': re.sub(clean, '', sub_pattern.group(2)),
                         'Suggestion': re.sub(clean, '', check_title_and_get_suggestion)})
            return True

    return False


# match content with answers at the end
def match_pattern6(url, c, w):

    pattern1 = re.findall('<p><strong>\d.*?</strong>.*?[a]\).*?[b]\).*?</p>', c,
                          re.DOTALL | re.IGNORECASE | re.MULTILINE)
    pattern2 = re.findall('<p>\d.*?<strong>[a-z]\).*?</strong></p>.*?<p>.*?</p>', c, re.DOTALL|re.IGNORECASE|re.MULTILINE)

    if len(pattern1) and len(pattern2):
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
                {'Url' : url ,
                 'Incorrect': re.sub(clean, '', incorrect),
                 'Correct': re.sub(clean, '', sub_pattern2.group(1)),
                 'Suggestion': re.sub(clean, '', sub_pattern2.group(2))})
        return True

    return False


def main(path_to_file_dir):
    # get files from the directory to match the pattern
    if os.path.exists(path_to_file_dir):
        file_list = sorted(os.listdir(path_to_file_dir))
        # get a list of files ending in 'html'
        file_list = [file_name for file_name in file_list if file_name.endswith('.html')]

        # open csv file to write the matched content
        writer = open_csv()

        # loop through the files in file list and match the pattern
        if file_list is not None:
            # list and dictionary to store the unmatched url
            url_list = []
            url_dict = {}
            text_file_unmatch_url = open('unmatched_url.txt', 'a')

            for file_name in file_list:
                path_to_file = os.path.join(path_to_file_dir, file_name)
                html_file = open(path_to_file, 'r')
                content = html_file.read()
                html_file.close()
                # pattern matching begins from here
                # check if the title contains '<h2>Answers\s+and\s+Explanations.*?</h2>'
                # to distinguish pattern 1 and pattern 6 because both consist similar pattern incorrect / correct
                mp6 = None
                if re.search('<h2>Answers\s+and\s+Explanations.*?</h2>', content, re.DOTALL | re.IGNORECASE):
                    # pattern 6
                    mp6 = match_pattern6(file_name, content, writer)
                    if mp6:
                        print('matched file6')
                        continue
                else:
                    # pattern 1
                    mp1 = match_pattern1(file_name, content, writer)
                    if mp1:
                        print('matched file1')
                        continue

                # pattern 2
                mp2 = match_pattern2(file_name, content, writer)
                if mp2:
                    print('matched file2')
                    continue

                # pattern 3
                mp3 = match_pattern3(file_name, content, writer)
                if mp3:
                    print('matched file3')
                    continue

                # pattern 4
                mp4 = match_pattern4(file_name, content, writer)
                if mp4:
                    print('matched file4')
                    continue


                # pattern 5
                mp5 = match_pattern5(file_name, content, writer)
                if mp5:
                    print('matched file5')
                    continue

                # check if the pattern does not  match for any links and store these links
                if((not mp1) and (not mp2) and (not mp3) and (not mp4) and (not mp5) and (not mp6)):
                    url_list.append(file_name)
                    text_file_unmatch_url.write(file_name)
                    text_file_unmatch_url.write("\n")

            # Add the list to the dictionary
            url_dict['url'] = url_list

            with open('unmatched_url.json', 'w') as un :
                json.dump(url_dict, un)
            un.close()
            text_file_unmatch_url.close()


    else:
        print('Path does not exist. Please correct the path.')


if __name__ == "__main__":
    cwd = os.getcwd()
    path_to_file_dir = "%s/data/" % (cwd)
    main(path_to_file_dir)

