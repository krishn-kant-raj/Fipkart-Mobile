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

    st.markdown("![img](https://i.imgur.com/dqOEkud.png)")
    "### Semi Automated WebSraping App for Flipkart *(Mobiles only)*"
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
        st.subheader("Flipkart Mobile Data Scraping...")
        if st.checkbox("Click to start"):
            try:
                brand = st.text_input("Enter Mobile Brand Name (See examples in sidebar) ","")
                brand = brand.title().split()
                brand = brand[0]
            except IndexError as er:
                pass
            
            try:
    #     Dynamic URL
                flipkart_url = f'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D{brand}&otracker=nmenu_sub_Electronics_0_{brand}'.format(brand)
            except InvalidSchema as er:
                st.write(er)
                st.write('Invalid Input')
                
            if st.checkbox("Show URL"):
                st.write('Verify your data on below link')
                st.write(flipkart_url)
                try:   
                    pg_num = st.text_input("Enter Numbers of Page to scrap: ")
                    if pg_num is not None or pg_num.isnumeric():
                        pg_num = int(pg_num)
                        if pg_num==0:
                            pg_num=1
                    elif pg_num.isalpha():
                        st.write('Please enter numeric value')
                except (ValueError,TypeError) as er:
                    st.write('Please enter numeric value')

                if st.checkbox("Start Scraping"):
                    for i in range(1,pg_num+1):
                        url = flipkart_url+"&page="+str(i)
                        try:
                            req = requests.get(url)
                        except ConnectionError as er:
                            st.write('Please check your connection!')

                        soup = BeautifulSoup(req.content, 'html.parser')
                        name = soup.find_all('div',{"class":"_4rR01T"})
                        
                        if len(name)==0:
                            break
                        
                        price = soup.find_all('div',{"class":"_30jeq3 _1_WHN1"})
                        ratings_reviews = soup.find_all('span',{"class":"_2_R_DZ"})
                        links = soup.find_all('a',{'class':'_1fQZEK'})
                        img = soup.find_all('img',{'class':'_396cs4 _3exPp9'})
                        st.write("*[INFO] Phones in Page *"+str(i)+'* is *'+str(len(name)))


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
                            
                    if len(Name)!=0:
                        if st.checkbox("Show Counts"):
                            if len(Name)==0:
                                st.write('*Try again! Nothing Scraped.*')
                            else:
                                st.write('**Name Count=**',len(Name))
                                st.write('**Price Count=**',len(Price))
                                st.write('**Rating Count=**',len(Rating))
                                st.write('**Review Count=**',len(Review))
                                st.write('**Links Count=**',len(Links))
                                st.write('**Image Count=**',len(Image))
                                if (len(Name)==len(Price) and len(Name)==len(Rating) and len(Name)==len(Review) and len(Name)==len(Links)):
                                    st.write('**Woo hoo! No missing Data found**')
                                else:
                                    if st.checkbox("Check Missing Data"):
                                        if len(Name)==0 and len(Price)==0:
                                            st.write('**Nothing Scraped! Check brand name speling.**')
                                    else:
                                        st.write("**Some rows have missing values**")
                               
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
                                        st.write("**Missing Data Filled with 'None'**")


                        if st.checkbox("Clean Raw Data"):
                            st.write("[Info] Cleaning Price Data...")
                            clean_price = []
                            for i in range(len(Price)):
                                price = Price[i][1:].replace(',','')
                                clean_price.append(price)
                            st.write(clean_price[:5])
                            
                            st.write("[Info] Cleaning Reviews Data...")
                            clean_review = []
                            for i in range(len(Review)):
                                if Review[i]=='None':
                                    clean_review.append('None')
                                else:
                                    Review_str = Review[i].split('\xa0&\xa0',1)[1]
                                    Review_str = Review_str.replace(' Reviews','').replace(',','')
                                    clean_review.append(Review_str)
                            st.write(clean_review[:5])  

                            clean_rating = []
                            for i in range(len(Rating)):
                                if Rating[i]=='None':
                                    clean_rating.append('None')
                                else:
                                    Rating_str = Rating[i][:-1]
                                    Rating_str = Rating_str.replace(' Ratings','').replace(',','')
                                    clean_rating.append(Rating_str)
                            st.write(clean_rating[:5])

                            if st.checkbox("Convert to DataFrame"):
                                data = {
                                    'Product_Name':Name,
                                    'Price':clean_price,
                                    'Rating':clean_rating,
                                    'Review':clean_review,
                                    'Product Link':Links,
                                    'Image Link':Image
                                }
                                data = pd.DataFrame(data)
                                    
                                data = data[~data.Rating.str.contains("None")]
                                data[['Price','Rating','Review']] = data[['Price','Rating','Review']].astype(int)
                                st.write(['Price','Rating','Review'], "**Numeric Columns Converted to numeric value**")

                                    
                                download = st.button('Download CSV File')
                                if download:
                                    'Download Started!'
                                    csv = data.to_csv(index=False)
                                    b64 = base64.b64encode(csv.encode()).decode()  # some strings
                                    linko= f'<a href="data:file/csv;base64,{b64}" download="flipkart-mobile.csv"><b>Download csv file<b></a>'
                                    st.markdown(linko, unsafe_allow_html=True)

    elif choice=='Analyse':
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
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

            if st.checkbox("Save this data"):
                download = st.button('Download CSV File')
                if download:
                    'Download Started!'
                    csv = clean_data.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()  # some strings
                    linko= f'<a href="data:file/csv;base64,{b64}" download="clean-data.csv"><b>Download csv file<b></a>'
                    st.markdown(linko, unsafe_allow_html=True)
            
                    
        if st.checkbox("Show Product Images"):
            try:
                for i in range(len(df['Image Link'])):
                    st.image(df['Image Link'][i], width=100, caption=df['Product_Name'][i])
                    st.write('Price Rs. ',df['Price'][i])
                    st.write('Rating:',df['Rating'][i], 'Reviews:',df['Review'][i])
                    st.markdown("------")
            except :
                st.write("**This feature is not available for selected dataset**")
    
if __name__ == '__main__':
    main()
