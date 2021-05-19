import pandas as pd 
import numpy as np
import streamlit as st
import requests
from bs4 import BeautifulSoup
import base64
#import bitly_api

# Bitly Access Token
#BITLY_ACCESS_TOKEN = 'access token'
#access = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)

def main():
    # Create empty lists
    Name = []
    Price = []
    Rating = []
    Review = []
    Links = []
    Image = []
    
    header_text="""
    <style>
    .column {
      float: left;
      width: 33.33%;
      padding: 5px;
    }

    .row::after {
      content: "";
      clear: both;
      display: table;
    }

    .row {
      display: flex;
    }

    .column {
      flex: 33.33%;
      padding: 5px;
    }
    </style>

    <div class="row">
      <div class="column">
        <a href ="https://github.com/krishn-kant-raj/Fipkart-Mobile">
        <img src="https://pngimg.com/uploads/github/github_PNG28.png" alt="GitHub" style="width:20%">
        <b>  GitHub</b></a>
      </div>
      <div class="column">
        <a href="https://www.linkedin.com/in/krishnkantraj/">
        <img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG38.png" alt="Krishn Kant Raj Linkedin" style="width:25%">
        <b>Krishn Kant Raj</b></a>
      </div>
      <div class="column">
        <a href="https://www.linkedin.com/in/intekhabahmad/">
        <img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG38.png" alt="Intekhab Linkedin" style="width:25%">
        <b>Intekhab Ahmad</b></a>
      </div>
    </div>
    """
    st.markdown(header_text,unsafe_allow_html=True)
    st.markdown("![img](https://i.imgur.com/dqOEkud.png)")

    
    activities = ["Collect Data","Analyse"]    
    choice = st.sidebar.selectbox("Select Activities",activities)

    st.sidebar.markdown("""|Mobile Brand Names|
                           |                :----:            |
                           | Mi |
                           |Realme |
                           |Samsung |
                           |Infinix |
                           |Nokia |
                           |OPPO |
                           |Poco |
                           |Apple |
                           |Vivo |
                           |Honor |
                           |Asus |
                        """)
    if choice == 'Collect Data':
        "### Semi Automated WebSraping App for Flipkart *(Mobiles only)*"
        if st.checkbox("Click to start"):
            try:
                brand = st.text_input("Enter Mobile Brand Name (See examples in sidebar) ","")
                if not brand:
                  st.warning('Please input a name.')
                brand = brand.title().split()
                brand = brand[0]
            except IndexError as er:
                brand=""
            
            try:
    #     Dynamic URL
                flipkart_url = f'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D{brand}&otracker=nmenu_sub_Electronics_0_{brand}'.format(brand)
            except InvalidSchema as er:
                st.write(er)
                st.write('Invalid Input')
            if brand !="":    
                st.write('Verify your data on below link')
                st.write(flipkart_url)
                pg_num = st.slider('Select a range of values',1, 30,step=1)
                if st.checkbox("Start Scraping"):
                    for i in range(1,pg_num+1):
                        url = flipkart_url+"&page="+str(i)
                        try:
                            req = requests.get(url)
                        except (ConnectionError,SSLError) as er:
                            st.write('Please check your connection!')

                        soup = BeautifulSoup(req.content, 'html.parser')
                        name = soup.find_all('div',{"class":"_4rR01T"})

                        if len(name)==0:
                            st.write('**Invalid Brand Name or Data is not available**')
                            break
                        
                        price = soup.find_all('div',{"class":"_30jeq3 _1_WHN1"})
                        ratings_reviews = soup.find_all('span',{"class":"_2_R_DZ"})
                        links = soup.find_all('a',{'class':'_1fQZEK'})
                        img = soup.find_all('img',{'class':'_396cs4 _3exPp9'})
                        st.write("**[Scraped]** *Phones in Page *"+str(i)+'* is *'+str(len(name)))

                        for i in name:
                            Name.append(i.text)
                        for i in price:
                            Price.append(i.text)
                        for i in ratings_reviews:
                            Rating.append(i.span.span.text)
                            Review.append(i.span.text)
                        #st.write('[INFO] Shortening link...')
                        for i in links:
                            linktext = 'https://www.flipkart.com'+i.get('href')
                            # BitlyError due to Monthly Limit Exist
                            # short_url = access.shorten(linktext)
                            # Links.append(short_url['url'])
                            Links.append(linktext)
                        for i in img:
                            imglink = i.get('src')
                            Image.append(imglink)
                            
                        if len(name)<24:
                            st.write('**All available data of **',brand,'** mobile has scraped**')
                            break    
                    if len(Name)!=0:
                        if len(Name)==0:
                            st.write('*Try again! Nothing Scraped.*')
                        elif (len(Name)==len(Price) and len(Name)==len(Rating) and len(Name)==len(Review) and len(Name)==len(Links)):
                                st.write('**Woo hoo! No missing Data found**')
                        else:
                            if len(Name)==0 and len(Price)==0:
                                st.write('**Nothing Scraped! Check brand name speling.**')
                            else:
                                st.write("*[INFO]* **Some rows have missing values**")
                   
                            if len(Price)<len(Name):
                                for i in range(0,(len(Name)-len(Price))):
                                    Price.append('None')
                            if len(Rating)<len(Name):
                                for i in range(0,(len(Name)-len(Rating))):
                                    Rating.append('None')
                            if len(Review)<len(Name):
                                for i in range(0,(len(Name)-len(Review))):
                                    Review.append('None')
                            if len(Links)<len(Name):
                                for i in range(0,(len(Name)-len(Links))):
                                    Links.append('None')
                            st.write("*[INFO]* **Missing Data Filled with 'None'**")

                        st.write("*[Info]* Cleaning Price Data...")
                        clean_price = []
                        for i in range(len(Price)):
                            price = Price[i][1:].replace(',','')
                            clean_price.append(price)
                        st.write(clean_price[:5])
                        
                        st.write("*[Info]* Cleaning Reviews Data...")
                        clean_review = []
                        for i in range(len(Review)):
                            if Review[i]=='None':
                                clean_review.append('None')
                            else:
                                Review_str = Review[i].split('\xa0&\xa0',1)[1]
                                Review_str = Review_str.replace(' Reviews','').replace(',','')
                                clean_review.append(Review_str)
                        st.write(clean_review[:5])  

                        st.write("*[Info]* Cleaning Ratings Data...")
                        clean_rating = []
                        for i in range(len(Rating)):
                            if Rating[i]=='None':
                                clean_rating.append('None')
                            else:
                                Rating_str = Rating[i][:-1]
                                Rating_str = Rating_str.replace(' Ratings','').replace(',','')
                                clean_rating.append(Rating_str)
                        st.write(clean_rating[:5])

                        data = {
                            'Product_Name':Name,
                            'Price':clean_price,
                            'Rating':clean_rating,
                            'Review':clean_review,
                            'Product Link':Links,
                            'Image Link':Image
                        }
                        try:
                            data = pd.DataFrame(data)
                        except:
                            st.print('All columns are not of same length')
                            
                        data = data[~data.Rating.str.contains("None")]
                        data[['Price','Rating','Review']] = data[['Price','Rating','Review']].astype(int)
                        filename = brand+'-Mobile'+'.csv'
                        csv = data.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # some strings
                        button = f'<a href="data:file/csv;base64,{b64}" download="{filename}"><b>Download Data</b></a>'
                        st.markdown(button,unsafe_allow_html=True)


    elif choice=='Analyse':
        "### Upload collected data"
        data = st.file_uploader("Upload a Dataset", type=["csv"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())
            
            if st.checkbox("Show Shape"):
                    st.write(df.shape)

            if st.checkbox("Show Tail"):
                st.write(df.tail(5))

            if st.checkbox("Show Sample"):
                try:
                    st.write(df.sample(5))
                except ValueError as vl:
                    st.write('**No Data Found!**')

            if st.checkbox("Describe Data"):
                st.write(df.describe())

            if st.checkbox("Show Selected Columns"):
                all_columns = df.columns.to_list()
                selected_columns = st.multiselect("Select Columns",all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Drop Selected Columns"):
                all_columns = df.columns.to_list()
                selected_columns = st.multiselect("Select Columns to drop",all_columns)
                clean_data = df.drop(selected_columns, axis = 1)
                st.dataframe(clean_data)


                if st.checkbox('Download CSV File'):
                    filename = st.text_input("Enter File Name: ","")
                    if filename !="":
                        filename = filename+'.csv'
                        csv = clean_data.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  
                        button = f'<a href="data:file/csv;base64,{b64}" download="{filename}"><b>Download Data</b></a>' 
                        st.markdown(button,unsafe_allow_html=True)
                    else:
                        st.write("Enter File Name")
                
                        
            if st.checkbox("Show Product Summary"):
                if len(df)>100:
                    st.write('**Length of dataset is **',len(df))
                    st.write('*Showing First 10 Data...*')
                try:
                    for i in range(10):
                        st.image(df['Image Link'][i], width=100, caption=df['Product_Name'][i])
                        st.write('Price Rs. ',df['Price'][i])
                        st.write('Rating:',df['Rating'][i], 'Reviews:',df['Review'][i])
                        st.markdown("------")
                except :
                    st.write("**This feature is not available for selected dataset**")
    
if __name__ == '__main__':
    main()
