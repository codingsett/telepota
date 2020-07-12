import sys
import time
import telepot
from telepot.text import apply_entities_as_markdown, apply_entities_as_html
import telepot.test_settings as st

TOKEN = st.TOKEN
USER_ID = int(st.USERID)

bot = telepot.Bot(TOKEN)

user_link = 'tg://user?id=' + str(USER_ID)

markdowns = [
    '*abc*de',
    'ab_cd_e',
    '[abcde](http://www.yahoo.com/)',
    '[user](' + user_link + ')',
    'a`bcd`e',
    '''Below is a function:
```text
def add(a, b):
    return a+b
```
Do you know what it does?''',
    'a_bc_de*f*g`hijk`lmno',
    'ab_cd_*efg*`h`[ijkl](http://www.yahoo.com/)',
    'a*bcdefg*h[user](' + user_link + ')',
    '''Markdown examples:
*1\\.* \\*bold text\\*
_2\\._ \\_italic text\\_
3\\. \\[inline URL\]\(http://www\.example\.com/\)
`4\\.` \\`inline fixed\-width code\\`''',

'''*bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```'''
]

print('Testing Markdown ...')
for s in markdowns:
    msg = bot.sendMessage(USER_ID, s, parse_mode='Markdown')
    u = apply_entities_as_markdown(msg['text'], msg['entities'])

    if s == u:
        print('Identical')
    else:
        print('Different:')
        print('Original ->', s)
        print('Applied ->', u)

    time.sleep(2)

htmls = [
    'a<b>bcd</b>e',
    '<i>ab</i>cde',
    'ab<a href="http://www.yahoo.com/">cde</a>',
    'ab<a href="' + user_link + '">user</a>',
    'a<code>bcd</code>e',
    '''Below is a function:
<pre>
def add(a, b):
    return a+b
</pre>
Do you know what it does?''',
    'a<i>bc</i>de<b>f</b>g<code>hijk</code>lmno',
    'ab<i>cd</i><b>efg</b><code>h</code><a href="http://www.yahoo.com/">ijkl</a>',
    'a<b>bcdefg</b>h<a href="' + user_link + '">user</a>',
    '''HTML examples:
<b>1.</b> &lt;b&gt;bold&lt;/b&gt;
<i>2.</i> &lt;i&gt;italic&lt;/i&gt;
3. &lt;a href="http://www.example.com/"&gt;inline URL&lt;/a&gt;
<code>4.</code> &lt;code&gt;inline fixed-width code&lt;/code&gt;''',
    '''<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=883163864">inline mention of a user</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>'''
]

print('Testing HTML ...')
for s in htmls:
    msg = bot.sendMessage(USER_ID, s, parse_mode='HTML')

    u = apply_entities_as_html(msg['text'], msg['entities'])

    if s == u:
        print('Identical')
    else:
        print('Different:')
        print('Original ->', s)
        print('Applied ->', u)

    time.sleep(0.5)
