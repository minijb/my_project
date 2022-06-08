with open('./learn/6/新闻文本分析/stopwords.txt','a') as f:
    for i in range (65,91):
        f.write(f'{chr(i)}\n')
    for i in range (97,123):
        f.write(f'{chr(i)}\n')

