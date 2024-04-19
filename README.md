---

# Text Analysis

This document outlines the methodology adopted for performing text analysis to derive sentimental opinion, sentiment scores, readability, passive words, personal pronouns, and more.

## Table of Contents

1. [Sentimental Analysis]
   - [Cleaning using Stop Words Lists]
   - [Creating dictionary of Positive and Negative words]
   - [Extracting Derived variables]
2. [Analysis of Readability]
3. [Average Number of Words Per Sentence]
4. [Complex Word Count]
5. [Word Count]
6. [Syllable Count Per Word]
7. [Personal Pronouns]
8. [Average Word Length]

## Sentimental Analysis

Sentimental analysis involves determining whether a piece of writing is positive, negative, or neutral. The algorithm designed for financial texts consists of the following steps:

### Cleaning using Stop Words Lists

Stop Words Lists are utilized to clean the text, thereby enabling sentiment analysis by excluding the words found in the Stop Words List.

### Creating a dictionary of Positive and Negative words

A Master Dictionary is employed to create a dictionary of Positive and Negative words. Only words not found in the Stop Words Lists are added to the dictionary.

### Extracting Derived variables

The text is converted into a list of tokens using the NLTK tokenize module, which are then used to calculate the following variables:

- Positive Score
- Negative Score
- Polarity Score
- Subjectivity Score

## Analysis of Readability

Readability analysis is calculated using the Gunning Fox index formula, which includes:

- Average Sentence Length
- Percentage of Complex words
- Fog Index

## Average Number of Words Per Sentence

This is calculated using the formula:
Average Number of Words Per Sentence = total number of words / total number of sentences

## Complex Word Count

Complex words are those containing more than two syllables.

## Word Count

The total number of cleaned words present in the text is calculated by removing stop words and any punctuations like ? ! , . before counting.

## Syllable Count Per Word

The number of syllables in each word of the text is counted by counting the vowels present in each word, handling exceptions like words ending with "es" or "ed".

## Personal Pronouns

To calculate Personal Pronouns mentioned in the text, regex is used to find the counts of specific words. Special care is taken so that country names are not included in the count.

## Average Word Length

Average Word Length is calculated by summing the total number of characters in each word and dividing by the total number of words.

---

This README provides an overview of the text analysis methodology and the various metrics derived from the analysis.
