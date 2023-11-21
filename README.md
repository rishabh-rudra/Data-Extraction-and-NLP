# Data-Extraction-and-NLP
This Project is about to extract textual data from various web articles and then this data is then analyzed by calculating various variables and counts. This is done using Python programming language.

1. File 'input.xlsx' contain the list of urls of 114 web articles on which we have to perform textual analysis.
2. File 'positive-words.txt' and 'negative-words.txt' contain list of words which is needed to compare and compute positive scores or negative scores which is a part of textual analysis.

### Step-1: Data Extraction
1. First we load the data from 'input.xlsx' file to pandas dataframe so that we can use it in our code.
2. We iterate over the dataframe for each article, extract the data and we make use of 'BeautifulSoup' Python package which trim all html things and we can get our desired data content in UTF-8 format.
3. We save the data into variabales and write it into a text file.

### Step-2: Data Cleaning
1. We need to clean the textual data so that various analysis and count can be done.
2. Texts are splited into words using a function from NLTK package 'word tokenize'.
3. Then cleaning and filtering of words is done by not inlcuding words present in NLTK 'stop words' corpus.

### Step-3: Textual Analysis
1. Now we loop through each and every word of that article and keep count of variables we declared.
2. With these counts we calculate other values like polarity score, subjectivity index and fog index.
3. At the end of loop we append variables values to their specified list which we have already initialized.

### Step-4: Converting into Excel Format
1. All the list contaning variable values are saved in python dictionary with their respective column name as key.
2. Then we convert it into pandas dataframe which can be easily converted into excel using in-bult pandas 'to excel' method.

On executing the the main python file 'main.py' will create text file containing data(title and content) for each article in 'input.xlsx', along with it an output file in xlsx format will also be generated which contain all the counts and variable values for each article.

### Requirements Before Executing main.py:
1. Python Version 3 or abaove
2. Numpy and Pandas Module
3. Requests Python module
4. BeautifulSoup Python packaage
5. NLTK Python Package aong with 'stop-words' corpus of NLTK.
6. input file, positive-words file and negative word file should be in same folder of main.py file.

#### This Project task was a part of test (by Blackoffer Company) on data extraction and analysis.
