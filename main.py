import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

import time



st.title('Streamlit 超入門')

st.write('プログレスバーの表示')
"Start!"

latest_iteration = st.empty()
bar = st.progress(0)


for i in range(100):
    latest_iteration.text(f'Iteration {i+1} ')
    bar.progress(i + 1)
    time.sleep(0.1)


left_column,right_column = st.columns(2)

button = left_column.button('右絡むに文字を表示')

if button:
    right_column.write("ここは右")

expander = st.expander("問い合わせ")
expander.write("問い合わせ内容を書く")

#text = st.text_input('あなたの趣味')
#'あなたの趣味:', text,'です。'



#ondition = st.slider('あなたの調子は',0,100,50)
#'コンディション:', condition """

# option = st.selectbox(
#     'あなたが好きな数字を教えてください',
#     list(range(1,11))
# )
# 'あなたの好きな数字は、', option, 'です。'



# if st.checkbox("Show Image"):
#     img = Image.open('100.png')
#     st.image(img,caption = 'uzu',use_column_width=True)
"""
# 章
## 節
### 項
```python
import streamlit as st
import numpy as np
import pandas as pd
```

"""