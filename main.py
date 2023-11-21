import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

data_df = pd.read_excel("input.xlsx")

# Loading positive words
with open("positive-words.txt" ,"r",  encoding="ISO-8859-1") as fh_pos:
    positive_words = fh_pos.read().lower()
positive_word_set = positive_words.split('\n')
positive_word_set.pop()
positive_word_set = set(positive_word_set)


# Loading negative words
with open("negative-words.txt" ,"r",  encoding="ISO-8859-1") as fh_neg:
    negative_words = fh_neg.read().lower()
negative_word_set = negative_words.split('\n')
negative_word_set.pop()
negative_word_set = set(negative_word_set)


#Loading stop words dictionary for removing stop words
stop_word_set = set(stopwords.words('english'))


#intilaizing various list to store all their values sequence wise
url_id_list = []
url_list = []
pos_score_list = []
neg_score_list = []
polarity_score_list =[]
subjective_score_list = []
avg_sentence_len_list = []
complex_word_percentage_list = []
fog_index_list = []
#Avg word per senence should be here but it is same as avg_sentence_len
complex_word_count_list = []
word_count_list = []
syllable_per_word_list = []
personal_pronoun_count_list = []
avg_word_len_list = []

print('Gathering Data of Each Article...')
for data in data_df.itertuples():
    url_id = data[1]
    url = data[2]
    url_id_list.append(url_id)
    url_list.append(url)


    response = requests.get(url)
    bs = BeautifulSoup(response.text,"html.parser")
    try:
        article_title = bs.find(name="h1").get_text()
        article_content = bs.find(attrs={"class":"td-post-content"})
        article_content = article_content.get_text().strip()

        temp_list = article_content.splitlines()
        temp_list.pop()
        article_content = "\n".join(temp_list)
        article_content_str = " ".join(temp_list)
        del temp_list

        sentence_count = article_content_str.count(".")
        article_content_str = article_content_str.replace("."," ")
        article_content_str = article_content_str.replace("’", "")
        article_content_str = article_content_str.replace("'","")
        article_content_str = article_content_str.lower()
        

        fh = open(str(url_id)+".txt", "w", encoding="utf-8")
        fh.write(article_title+"\n"+article_content)
        fh.close()



        #Converting text into tokens/words with ignoring non alphabetic characters
        tokens = word_tokenize(article_content_str, language='english')
        tokens = [x for x in tokens if x[0].isalnum()]


        #intializing variables to hold various counts
        word_count = 0
        pos_score = 0
        neg_score = 0
        total_syllable_count = 0
        total_char_count = 0
        complex_word_count = 0
        personal_pronoun_count = 0

        vowel_set = {'a','e','i','o','u'}
        personal_pronoun_set = {'i', 'we', 'my', 'ours', 'us'}


        #looping through all words for various counts
        for word in tokens:
            if word in personal_pronoun_set:
                personal_pronoun_count += 1

            total_char_count += len(word)
            if word not in stop_word_set:
                word_count += 1
                if word in positive_word_set: pos_score+=1
                elif word in negative_word_set: neg_score+=1

            syllable_count = 0
            for letter in word:
                if letter in vowel_set: syllable_count += 1

            if word.endswith(('es','ed')):syllable_count -= 1
            if syllable_count>2: complex_word_count += 1

            total_syllable_count += syllable_count
            

        #counts & scores
        avg_word_len = total_char_count/len(tokens)
        avg_sentence_len = len(tokens)/sentence_count
        syllable_per_word = total_syllable_count/len(tokens)
        complex_word_percentage = complex_word_count/len(tokens)
        fog_index = 0.4*(avg_sentence_len+complex_word_percentage)
        subjective_score = (pos_score+neg_score)/(word_count+0.000001)
        polarity_score = (pos_score-neg_score)/(pos_score+neg_score+0.000001)

        #Appending to their specific list
        pos_score_list.append(pos_score)
        neg_score_list.append(neg_score)
        polarity_score_list.append(polarity_score)
        subjective_score_list.append(subjective_score)
        avg_sentence_len_list.append(avg_sentence_len)
        complex_word_percentage_list.append(complex_word_percentage)
        fog_index_list.append(fog_index)
        #Avg word per senence should be here but it is same as avg_sentence_len
        complex_word_count_list.append(complex_word_count)
        word_count_list.append(word_count)
        syllable_per_word_list.append(syllable_per_word)
        personal_pronoun_count_list.append(personal_pronoun_count)
        avg_word_len_list.append(avg_word_len)

    except:
        print("Article not found on URL_ID:",url_id)

        pos_score_list.append(0)
        neg_score_list.append(0)
        polarity_score_list.append(0)
        subjective_score_list.append(0)
        avg_sentence_len_list.append(0)
        complex_word_percentage_list.append(0)
        fog_index_list.append(0)
        #Avg word per senence should be here but it is same as avg_sentence_len
        complex_word_count_list.append(0)
        word_count_list.append(0)
        syllable_per_word_list.append(0)
        personal_pronoun_count_list.append(0)
        avg_word_len_list.append(0)
print('Finished! Txt file for each article has been created.')


#Converting into python dictionary so that to be used as dataframe
excel_data_dict = {'URL_ID':url_id_list, 'URL':url_list, 'POSITIVE SCORE':pos_score_list, 'NEGATIVE SCORE':neg_score_list, 'POLARITY SCORE':polarity_score_list, 'SUBJECTIVITY SCORE':subjective_score_list, 'AVG SENTENCE LENGTH':avg_sentence_len_list, 'PERCENTAGE OF COMPLEX WORDS':complex_word_percentage_list, 'FOG INDEX': fog_index_list, 'AVG NUMBER OF WORDS PER SENTENCE':avg_sentence_len_list, 'COMPLEX WORD COUNT':complex_word_count_list, 'WORD COUNT':word_count_list, 'SYLLABLE PER WORD':syllable_per_word_list, 'PERSONAL PRONOUNS':personal_pronoun_count_list, 'AVG WORD LENGTH':avg_word_len_list}


#converting to dataframe
df_for_excel = pd.DataFrame(excel_data_dict)

#writing into excel
df_for_excel.to_excel('output.xlsx', index=False)

print('Textual Analysis done. Output file generated')
print('All files generated are located at this current working folder.')
print('Done.')