


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

def write_row(f,word,inflectioin=[],phonetic=' ',definition=' ',translation=' ',example=' '):
    row=[]
    definition=definition.replace('\\n','<br>')
    translation = translation.replace('\\n', '<br>')
    for i in [word,phonetic,'<br>'.join(inflectioin),definition,translation,example]:
        if len(i)==0:
            row.append(' ')
        else:
            row.append(i)
    f.write('|'.join(row)+'\n')

last_alpha=None

dictionary=load_dict()

with open('readme.md','w') as f,open('head.md') as h:
    for l in h:
        f.write(l)
    total=len( d.keys())
    f.write(f'### Total words:{total}\n\n')
    for a in range(ord('A'), ord('Z')+1):
        c=chr(a)
        f.write(f'[{c}](#{c})  ')
    f.write('\n\n');
    for i in d.keys():
            if i[0]!=last_alpha:
                write_head(i[0].upper(),f)
                last_alpha=i[0]
            w=d[i][0]
            if w in dictionary:
                o=dictionary[w]
                write_row(f,w,phonetic=o['phonetic'],inflectioin=d[i][1:],definition=o['definition'],translation=o['translation'])
            else:
                write_row(f, w, d[i][1:])

#
print('total words:',len(d.keys()))