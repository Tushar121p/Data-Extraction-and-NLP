#!/usr/bin/env python
# coding: utf-8

# # Importing necessary libraries

# In[1]:


import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import warnings
warnings.filterwarnings(action = 'ignore')


# ## Reading all the data from their file location

# In[2]:


#Importing the data and creating a dataframe
df = pd.read_excel(input("Enter path to the input Excel file: "))       # C:\Users\tusha\Downloads\Input.xlsx


# In[3]:


#getting the location of the folder where stopwords files are located
stopwords_folder = input("Enter path to the folder where stopwords files are located: ") #C:\Users\tusha\Downloads\StopWords


# In[4]:


#Giving the positive words and negative words file's location
positive_file_path = input("Enter path to the positive words file: ")   #C:\Users\tusha\Downloads\positive-words.txt
negative_file_path = input("Enter path to the negative words file: ")   #C:\Users\tusha\Downloads\negative-words.txt


# In[5]:


Output_File_Location = input("Enter path to the Output_Data_Structure excel file: ")  #C:\Users\tusha\Downloads\Output Data Structure.xlsx


# In[6]:


#To display the max rows and columns
pd.set_option('display.max_columns' , None)
pd.set_option('display.max_rows', None)


# # Fetching the content from the URLs

# In[7]:


# Function to fetch text content for each URL
def fetch_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text()
            return text_content
        else:
            print(f'Failed to fetch the content from URL: {url} | status_code: {response.status_code}')
            return None


# In[8]:


# Add a new column 'content' to store text content for each URL
content = pd.DataFrame()
content['content'] = df['URL'].apply(lambda url: fetch_content(url))
content.reset_index(drop=True, inplace=True)


# In[9]:


content


# # Sentimental Analysis

# In[10]:


stopwords_files = []
for name in ["Generic", "Auditor", "Currencies", "DatesandNumbers", "GenericLong", "Geographic", "Names"]:
    # Construct the file path by concatenating folder path and filename
    stopwords_file = f"{stopwords_folder}\\StopWords_{name}.txt"
    stopwords_files.append(stopwords_file)


# In[11]:


stopwords = pd.DataFrame()  # Initialize an empty DataFrame
for file in stopwords_files:
    if "Currencies" in file:
        # For StopWords_Currencies file
        df_temp = pd.read_csv(file, sep='|', encoding='latin-1', header=None)  
        # Concatenate both columns on axis=0
        df_temp = pd.concat([df_temp[0], df_temp[1]], axis=0, ignore_index=True)
        stopwords = pd.concat([stopwords, df_temp], ignore_index=True, axis=0)  # Assign the result back to dfs
    elif "DatesandNumbers" in file or "Geographic" in file or "Names" in file:
        # For StopWords_DatesandNumbers, StopWords_Geographic, and StopWords_Names files
        df_temp = pd.read_csv(file, header=None, sep='|', usecols=[0])  
        stopwords = pd.concat([stopwords, df_temp], ignore_index=True, axis=0)  # Assign the result back to dfs
    elif "Generic" in file or "Auditor" in file or "GenericLong" in file:
        df_temp = pd.read_csv(file, header=None)  
        stopwords = pd.concat([stopwords, df_temp], ignore_index=True, axis=0)  # Assign the result back to dfs


# In[12]:


#creating a list of lowercase stopwords
stopwords_list = []
for word in stopwords[0]:
    if not pd.isna(word):  # Check if the value is not NaN
        stopwords_list.append(word.lower())


# In[13]:


stopwords_list


# ## Tokenizing the content extracted from URLs

# In[14]:


content['content'] = content['content'].astype(str)
content['token'] = content['content'].apply(lambda x:word_tokenize(x))


# ## Cleaning using Stop Words Lists

# In[15]:


content['token'] = content['token'].apply(lambda x: [i.lower() for i in x])


# In[16]:


content['text'] = content['token'].apply(lambda x: [word for word in x if word not in stopwords_list])
content.drop(columns=['token'], inplace=True)


# In[17]:


content['new_text'] = content['text'].apply(lambda x: [re.sub(r'[^\w\s]', '', word) for word in x])
content['clean_text']  = content['new_text'].apply(lambda x:[word for word in x if word != ''])


# In[18]:


content.drop(columns = ['text','new_text'], inplace =True)


# In[19]:


content


# ## Creating a dictionary of Positive and Negative words

# In[20]:


positive = pd.read_csv(positive_file_path, header=None)
negative = pd.read_csv(negative_file_path, header=None, encoding='latin-1')


# In[21]:


positive_dictonary = [words for words in positive[0] if words not in stopwords_list]
negative_dictonary = [words for words in negative[0] if words not in stopwords_list]


# ### Extracting Derived variables

# In[22]:


def positive_score(row, dictionary):
    Positive_Score = 0
    for word in row:
        if word in dictionary:
            Positive_Score += 1
    return Positive_Score


# In[23]:


def negative_score(row,dictonary):
    Negative_Score = 0
    for word in row:
        if word in dictonary:
            Negative_Score -= 1
        else:
            pass
    return Negative_Score*-1


# In[24]:


def polarity_score(p_score,n_score):
    Polarity_Score = (p_score - n_score) / ((p_score + n_score) + 0.000001)
    return Polarity_Score


# In[25]:


def subjectivity_score(text,p_score,n_score):
    Subjectivity_Score = (p_score + n_score)/ ((len(text)) + 0.000001)
    return Subjectivity_Score


# In[26]:


content['Positive_Score'] = content['clean_text'].apply(lambda x : positive_score(x, positive_dictonary))


# In[27]:


content['Negative_score'] = content['clean_text'].apply(lambda x : negative_score(x, negative_dictonary))


# In[28]:


content['Polarity_Score'] = content.apply(lambda row: polarity_score(row['Positive_Score'], row['Negative_score']), axis=1)


# In[29]:


content['Subjectivity_Score'] = content.apply(lambda row: subjectivity_score(row['clean_text'],row['Positive_Score'], row['Negative_score']), axis=1)


# In[30]:


content


# # Analysis of Readability

# In[31]:


def count_words(sentence):
    if type(sentence) == str:
        words = re.findall(r'\b\w+\b', sentence)  # Extract words using regex
    elif type(sentence) == list:
        words = []
        for word in sentence:
            words.extend(re.findall(r'\b\w+\b', word))
    return len(words)

def count_sentences(content):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', content)
    return len(sentences)


# In[32]:


def count_complex_words(words):
    # Consider words with length > 2 as complex words
    complex_words = [word for word in words if len(word) > 2]  
    return len(complex_words)

#Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

def fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)


# In[33]:


def count_syllables(word):
    # Remove trailing 'es' or 'ed' to handle exceptions
    word = re.sub(r'(es|ed)$', '', word)
    
    # Count the number of vowels
    vowels = re.findall(r'[aeiou]+', word)
    
    # Adjust the count for words with a single vowel at the end, not counting 'e' unless it's the only vowel
    if len(vowels) > 1 and vowels[-1] == 'e':
        vowels.pop()  # Remove the last 'e' if it's not the only vowel
    
    return len(vowels)


# In[34]:


def count_personal_pronouns(text):
    pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pattern, text)
    return len(matches)


# In[35]:


def average_word_length(text):
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text)
    # Calculate the total number of characters in all words
    total_characters = sum(len(word) for word in words)
    # Calculate the total number of words
    total_words = len(words)
    # Calculate the average word length
    if total_words != 0:
        return total_characters / total_words
    else:
        return 0  # Handle case where there are no words


# In[36]:


content['Average_Sentence_Length'] = content['content'].apply(lambda x: count_words(x) / count_sentences(x))


# In[37]:


content['Percentage_of_Complex_Words'] = content['clean_text'].apply(lambda x: 0 if count_complex_words(x) == 0 else 100*(count_complex_words(x) / len(x)))


# In[38]:


content['Fog_Index'] = fog_index(content['Average_Sentence_Length'], content['Percentage_of_Complex_Words'])


# In[39]:


content['Average_Number_of_Words_Per_Sentence'] = content.apply(lambda x : len(x['clean_text']) / count_sentences(x['content']),axis= 1)


# In[40]:


content['Complex_Word_Count'] = content['clean_text'].apply(lambda x:(count_complex_words(x)))


# In[41]:


content['Word_Count'] = content['clean_text'].apply(lambda x : len(x))


# In[42]:


content['Average_Syllable_Count_Per_Word'] = content['clean_text'].apply(lambda x: np.mean([count_syllables(i) for i in x]))


# In[43]:


content['Personal_Pronouns_Count'] = content['content'].apply(count_personal_pronouns)


# In[44]:


content['Average_Word_Length'] = content['content'].apply(average_word_length)


# In[45]:


content


# # Creating and saving output file in the desired format

# In[46]:


output_file = pd.concat([df, content], axis=1)


# In[47]:


output_file.drop(columns = ['content','clean_text'],inplace = True)
output_file


# In[48]:


output_file.to_excel(Output_File_Location, index = False)

