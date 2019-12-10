# Simple IT English

English is the only language of IT community.
I know it is how pain to learn english and remember the english words as a non-native speaker. 
Many talent engineer was kept out from community because lack of english skill.
Most public IT english words books is not related to IT community ,or too academic.
I try to create a basic english dictionary from community and for programmer/software engineer .
The assumption is developers are able to : 

1. [ x ] Read&Write posts in Stackoverflow.com

1. [ x ] Read [hackernews](https://news.ycombinator.com/)

1. [  ] Read&Write comments and readme from github.com. 
 
 
### Corpus


Source|Newest Post|Oldest Post|Row Count|Size
------|-----------|-----------|---------|----
HackerNews comments|2015-10-13 08:44:02 UTC|2006-10-09 19:51:01 UTC|8399417|3.41 GB
HackerNews stories|2015-10-13 08:44:34 UTC|2006-10-09 18:21:51 UTC|1959809|402.71 MB
StackOverflow answers|2019-09-01 05:22:21.463 UTC|2008-08-01 13:16:49.127 UTC|27665009|22.27 GB
StackOverflow questions|2019-09-01 05:23:41.743 UTC|2008-08-03 21:38:52.623 UTC|18154493|28.13 GB	

##### 48.8 GB processed

### Processes for clean & select words

1. [ x ] Select top 16000 most frequently used words from StackOverflow and HackerNews .
Thanks to Google cloud public dataset and BigQuery ,it save me some days and coffees. 
1.  [ x ] Select english words by [words list](https://github.com/dwyl/english-words/)
1.  [ x ] Exclude too simple english words from [voa special](https://en.wikipedia.org/wiki/Special_English) 
and [common 3000](https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/) 
1. [ x ]  Group the words inflection to root with nltk steam module.
1. [  ]  Fetch meaning from [opted dictionary](http://www.mso.anu.edu.au/~ralph/OPTED/).
1. [  ]  Fetch example sentence from StackOverflow post. 

# SITE: Simple IT English



