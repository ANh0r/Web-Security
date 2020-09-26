import requests
import re
import chardet   #需要导入这个模块，检测编码格式

s = requests.Session()

url = "http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php"
html = s.get(url).content
encode_type = chardet.detect(html)
html = html.decode(encode_type['encoding']) #进行相应解码，赋给原标识符（变量）


reg = r'([0-9].+)=<'
pattern = re.compile(reg)
match = re.findall(pattern,html)

payload = {'v':eval(match[0])}
print(s.post(url,data=payload).content.decode())

"""
TypeError: cannot use a string pattern on a bytes-like object

最近写代码，python2和python3之间切换，难免会碰到一些问题，有些方法比如re模块的findall要求传入的是字符串格式的参数，urllib.request.urlopen(url).read()返回的是bytes类型（这个是python3中才有的类型，所以很多python2中的方法都相应更改了）的，这样传参就会报以上错误。

python3中Unicode字符串是默认格式（就是str类型），ASCII编码的字符串（就是bytes类型，bytes类型是包含字节值，其实不算是字符串，python3还有bytearray字节数组类型）要在前面加操作符b或B；python2中则是相反的，ASCII编码字符串是默认，Unicode字符串要在前面加操作符u或U

一劳永逸的解决方法就是根据你传进来的参数自动辨别编码格式，然后进行相应的解码，就搞定啦：

import chardet   #需要导入这个模块，检测编码格式
encode_type = chardet.detect(html)  
html = html.decode(encode_type['encoding']) #进行相应解码，赋给原标识符（变量）
1
2
3
从str到bytes:调用方法encode().
编码是把Unicode字符串以各种方式编码成为机器能读懂的ASCII字符串
从bytes到str:调用方法decode().
"""