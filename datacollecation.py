# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pandas
#
#函数1：产生所有所有跟链接（rootlink）下的次链接links（儿子链接）
#
def parseListlinks(url):
    linklist =[]
    lurl = 'https://link.springer.com{}'#次链接左半部分
    soup = BeautifulSoup(rootlink.text, 'html.parser')
    links = soup.select('.title') #所有次链接右半部分
    count = len(links)
    for i in range(count):
        linklist.append(lurl.format(links[i]['href']))
    return linklist
#
# 函数2：通过次链接（）产生多个子链接
#
def suburls(url):#通过次链接(links)产生多个子链接(sublinks孙子链接)
    suburls = []
    lsurl = 'https://link.springer.com{}'#子链接左半部分
    res1 = requests.get(url)
    soup2 = BeautifulSoup(res1.text, 'html.parser')
    urlsub1s = soup2.select('.title a')#子链接右半部分
    for i in range(len(urlsub1s)):
        suburls.append(lsurl.format(urlsub1s[i]['href']))
    return suburls
#
# 函数3：通过次链接（link）及子链接（sublink）爬取最终结果集
#
def detailPaper(url,suburl):#以下函数生成结果集
    res0 = requests.get(url)
    soup0 = BeautifulSoup(res0.text, 'html.parser')
    res = requests.get(suburl) #修改处
    soup = BeautifulSoup(res.text, 'html.parser')
    result = {}
    volume = soup.select('.ArticleCitation_Volume') #get Volume
    if len(volume)==0:
        result['volume'] = 'N/A'
    else :
        result['volume'] = volume[0].text.strip()[:-1][-1]
        
    issue = soup.select('.ArticleCitation_Issue') #get Issue
    if len(issue)==0:
        result['issue'] = 'N/A'
    else :
        result['issue'] = issue[0].text.strip()[-1] #end
        
    pages = soup.select('.ArticleCitation_Pages') #get pages
    if len(pages)==0:
        result['pages'] = 'N/A'
    else :
        result['pages'] = pages[0].text.lstrip('pp ') #end
        
    year = soup.select('.ArticleCitation_Year') #Year
    if len(year)==0:
        result['year'] = 'N/A'
    else :
        result['year'] = year[0].text.lstrip('September ').strip()[:-1] #end
        
    ptype = soup0.select('.content-type') #在次链接中 Type 
    if len(ptype)==0:
        result['ptype'] = 'N/A'
    else :
        result['ptype'] = ptype[0].text.strip() #end
        
    title = soup.select('.ArticleTitle') #Title
    if len(title)==0:
        result['title'] = 'N/A'
    else :
        result['title'] = title[0].text.strip() #end

    author = soup.select('.authors__name') #Author
    if len(author)==0:
        result['author'] = 'N/A'
    else :
        result['author'] = author[0].text.strip() #end

    affiliations = soup.select('.affiliation__item') #Affiliations 
    if len(affiliations)==0:
        result['affiliations'] = 'N/A'
    else :
        result['affiliations'] = affiliations[0].text.strip()#end
        
    country = soup.select('.affiliation__country') #Country
    if len(country)==0:
        result['country'] = 'N/A'
    else :
        result['country'] = country[0].text.lstrip('(')[:-1].strip()#end

    share = soup.select('#socialmediamentions-count-number')  # share
    if len(share) == 0:
        result['share'] = '0'
    else:
        result['share'] = share[0].text.strip()  # end
    
    downloads = soup.select('.article-metrics__views') #Downloads
    if len(downloads)==0:
        result['downloads'] = 'N/A'
    else :
        result['downloads'] = downloads[0].text.strip()#end
        
    citations = soup.select('#citations-count-number') #Citations
    if len(citations)==0:
        result['citations'] = 'N/A'
    else :
        result['citations'] = citations[0].text.strip()#end
        
    doi = soup.select('#doi-url') #Doi
    if len(doi)==0:
        result['doi'] = 'N/A'
    else :
        result['doi'] = doi[0].text.lstrip('https://doi.org/')#end
    
    abstract = soup.select('.Para') #abstract
    if len(abstract) != 0:
        result['abstract'] = ' '.join(soup.select('.Para')[0].text.strip().split()[:25])                 
    else:
        result['abstract'] = 'N/A' #end
        
    
    word = soup.select('.Keyword') #Keyword
    inter = ''
    keyword = ''
    if len(word) > 1:
        for i in range(len(word)-1):
            inter = word[i].text+'|'
        result['keyword'] = inter.strip() + word[-1].text
    elif len(word) == 1:
        result['keyword'] = word[0].text.strip()
    else:
        result['keyword']='N/A' #end
    return result


rootlink = requests.get('https://link.springer.com/journal/volumesAndIssues/11192')  # 根目录
links = parseListlinks(rootlink)
# url = 'https://link.springer.com/journal/11192/1/1/page/1'#次链接
# print(links)
paper_total = []
for i in range(len(links)):##输出结果集
    sublinks = suburls(links[i])
    for sublink in sublinks:
        paperinfo = detailPaper(links[i], sublink)
        paper_total.append(paperinfo)

df = pandas.DataFrame(paper_total, columns=['volume', 'issue', 'pages', 'year', 'ptype', 'title','author','affiliations','country','share','downloads','citations','doi','abstract','keyword'])
# print(df)# 输出pandas结果集
df.to_csv('./datacollect.csv', index=False, encoding='utf_8_sig')


# df = pandas.DataFrame(paper_total) #展示结果
# df

