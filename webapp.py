import streamlit as st 
import pandas as pd 

from src.visualization import (render_passenger_airlines, 
                               render_passenger_overtime,render_passenger_region)


st.title('Welcome to Our Page')


# page_navi = st.sidebar.radio('Page Navigation',options=['Air Traffic Dashboard', 'Air Traffic Prediction',
#                                             'Air Traffic API Docs'])
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
#         width: 250px;
#     }
#     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
#         width: 100px;
#         margin-left: 50px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# if page_navi == 'Air Traffic Dashboard' : 
#     #this page will provide 
st.plotly_chart(render_passenger_region())
st.plotly_chart(render_passenger_overtime())
st.plotly_chart(render_passenger_airlines())

# # if page_navi == 'Air Traffic Prediction' : 
# st.write('We are currently working in this section')


# # if page_navi == 'Air Traffic API Docs' : 
# st.write('We are currently working in this section')