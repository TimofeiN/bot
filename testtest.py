import emoji

subs_res = {'79': 'price value 10.00%', '80': 'price value 23900.99$', '81': 'price value 5.00%', '82': 'price value 2.00%', '83': 'price value 10000.00$'}
data = '80'
symbol = emoji.emojize(':prohibited:')
subs_res[data] = f'{symbol} {subs_res[data]}'
print(subs_res)
