


from nltk.stem import PorterStemmer
porter = PorterStemmer()

def load_csv(top=None):
    words=set()
    with  open('source/results-20191210-170511.csv') as f:
        skip_head=True
        c=0
        for l in f:

            if skip_head:
                skip_head=False
                continue

            c=c+1
            if top and c>top:
                break
            (word,count)=l.split(',')
            words.add(word)

    return words


def load_word(fiilename):
    words=set()
    with open(fiilename) as f:
        for l in f:
            words.add(l.strip())


    return words

def load_include():
    return load_word('include/words_alpha.txt')


def load_exclude():
    words=set()
    with open('exclude/voa_words.txt') as f:
        for l in f:
            if len(l.strip())<2:
                continue
            w=l.split(' ')[0]
            st = porter.stem(w)
            words.add(w)
            words.add(st)
    common = load_word('exclude/common3000.txt')
    return words|common


def load_dict():
    import csv
    dict={}
    with open('dictionary/ecdict.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
           w=row['word']
           dict[w]=row
    return dict

words=load_csv(16000)

include=load_include()
words=words&include
exclude=load_exclude()

# common=voa|common
# r=r.union(top2000)

d={}
for w in sorted(words):
    st=porter.stem(w)
    if len(st) <=3 or st in exclude or w in exclude:
        continue
    if st in d:
        d[st].append(w)
    else:
        d[st]=[w]

def write_head(section,f):
    f.write('\n\n## '+section+'\n\n')
    f.write(f'<a name="{section}"></a>[TO Head](#A)\n\n')
    f.write('Word|Phonetic|Inflection|Definition|Translation|Example\n')
    f.write('----|--------|----------|----------|-----------|-------\n')

def write_row(f,word,inflection=[],phonetic=' ',definition=' ',translation=' ',example=' '):
    row=[]
    definition=definition.replace('\\n','<br>')
    translation = translation.replace('\\n', '<br>')
    for i in [word,phonetic,'<br>'.join(inflection),definition,translation,example]:
        if len(i)==0:
            row.append(' ')
        else:
            row.append(i)
    f.write('|'.join(row)+'\n')

last_alpha=None

dictionary=load_dict()
result_dict=[]

for i in d.keys():
    w=i
    if w in dictionary:
        o = dictionary[w]
        result_dict.append(
            {
                'word':w,
                'phonetic':o['phonetic'],
                'inflection':d[i][1:],
                'definition':o['definition'],
                'translation':o['translation']
            }
        )

    else:
        result_dict.append(
            {
                'word':w,
                'phonetic':' ',
                'inflection':d[i][1:],
                'definition':' ',
                'translation':' '
            }
        )


with open('readme.md','w') as f,open('head.md') as h:
    for l in h:
        f.write(l)
    total=len( d.keys())
    f.write(f'### Total words:{total}\n\n')
    for a in range(ord('A'), ord('Z')+1):
        c=chr(a)
        f.write(f'[{c}](#{c})  ')
    f.write('\n\n');
    for item in result_dict:
            word=item['word']
            if word[0]!=last_alpha:
                write_head(word[0].upper(),f)
                last_alpha=word[0]

            write_row(f, word, phonetic=item['phonetic'], inflection=item['inflection'], definition=item['definition'],
                      translation=item['translation'])


#
print('total words:',len(d.keys()))

import genanki
import copy
my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
      {'name': 'word'},
      {'name': 'phonetic'},
      {'name': 'definition'},
      {'name': 'translation'},
  ],
  templates=[
    {
        'name': 'Card 1',
        'qfmt': '<center><h1>{{word}}</h1><br>{{phonetic}}</center>',
        'afmt': '<center><h1>{{word}}</h1><br>{{phonetic}}</center><hr id="answer">{{definition}}<br>{{translation}}',
    },
  ])
my_deck = genanki.Deck(
  10591234111,
  'Simple-IT-English(en-cn)')

for item in result_dict:

    my_note = genanki.Note(
      model=my_model,
      fields=[item['word'],item['phonetic'],item['definition'],item['translation']])



    my_deck.add_note(copy.deepcopy(my_note))
genanki.Package(my_deck).write_to_file('Simple-IT-English(en-cn).apkg')



