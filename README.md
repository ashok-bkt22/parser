# Parser
# Crawl the links and check the defined pattern for text correction

# Procedure to run the script: 
  * 1. Install the scrapy library (https://docs.scrapy.org/en/latest/intro/install.html)
    * pip install scrapy  
  * 2. Download the html files to the data directory.
    * python main.py 
  * 3. Match pattern to parse the html files into a csv file (URL, Incorrect, Correct, Suggestion)
    * python match_pattern.py 
