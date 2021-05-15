import pandas as pd 
import numpy as np
import streamlit as st
import requests
from bs4 import BeautifulSoup
import base64
#import bitly_api

# Bitly Access Token
#BITLY_ACCESS_TOKEN = '749d6a714f1342aaced60e021f4a05ced8c7841d'
#access = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)

# Create empty lists
Name = []
Price = []
Rating = []
Review = []
Links = []
Image = []

def main():

    st.markdown("![img](https://i.imgur.com/dqOEkud.png)")
    "### Semi Automated WebSraping App for Flipkart *(Mobiles only)*"
    
    #activities = ["Collect and Clean Data"]
    
    #choice = st.sidebar.selectbox("Select Activities",activities)
    #if choice == 'Collect and Clean Data':
        #st.subheader("Collect Data of a Mobile Brand")
        
    if st.checkbox("Click to start"):
        try:
            brand = st.text_input("Enter Mobile Brand Name : ","")
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
            st.write(flipkart_url)
            
        if st.checkbox("Enter Number of Page to scrap"):
            try:    
                pg_num = st.text_input("Enter Numbers of Page to scrap: ",1)
                pg_num = int(pg_num)
            except (ValueError,TypeError) as er:
                pass
            if st.checkbox("Start Scraping"):
                for i in range(1,pg_num+1):
                    url = flipkart_url+"&page="+str(i)
                    try:
                        req = requests.get(url)
                    except ConnectionError as er:
                        st.write(er)
                        st.write('Please check your connection!')
                    
                    soup = BeautifulSoup(req.content, 'html.parser')
                    name = soup.find_all('div',{"class":"_4rR01T"})
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

                st.write("*[INFO] Raw data scraped.*")
                
                if st.checkbox("Show Counts"):
                        st.write('**Name Count=**',len(Name))
                        st.write('**Price Count=**',len(Price))
                        st.write('**Rating Count=**',len(Rating))
                        st.write('**Review Count=**',len(Review))
                        st.write('**Links Count=**',len(Links))
                        st.write('**Image Count=**',len(Image))
                        
                if st.checkbox("Check Missing Data"):
                    if (len(Name)==len(Price) and len(Name)==len(Rating) and len(Name)==len(Review) and len(Name)==len(Links)):
                        st.write('**Woo hoo! No missing Data found**')
                    else:
                        st.write("Some rows have *None* value")
                        
                        if st.checkbox("Fill Missing Data with None"):      
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

                            if st.checkbox("Remove None Rows"):
                                data = data[~data.Rating.str.contains("None")]
                                st.write("**Rows having 'None' values are removed.**")
                                st.write(data)

                            if st.checkbox("Show Count"):
                                st.write("Count after filled missing data")
                                st.write('**Name Count=**',len(Name))
                                st.write('**Price Count=**',len(Price))
                                st.write('**Rating Count=**',len(Rating))
                                st.write('**Review Count=**',len(Review))
                                st.write('**Links Count=**',len(Links))

                if st.checkbox("Clean Price Data"):
                    st.write("[Info] Cleaning Price Data...")
                    clean_price = []
                    for i in range(len(Price)):
                        price = Price[i][1:].replace(',','')
                        clean_price.append(price)
                    st.write(clean_price[:5])
                    

                if st.checkbox("Clean Reviews Data"):
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

                if st.checkbox("Clean Rating Data"):
                    st.write("[Info] Cleaning Rating Data...")
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
                        'Link':Links
                    }
                    data = pd.DataFrame(data)

                    if st.checkbox("Show Head"):
                        st.write(data.head(5))

                    if st.checkbox("Show Tail"):
                        st.write(data.tail(5))

                    if st.checkbox("Show Sample"):
                        st.write(data.sample(5))

                    if st.checkbox("Describe Data"):
                        st.write(data.describe())

                    if st.checkbox("Show Selected Columns"):
                        all_columns = data.columns.to_list()
                        selected_columns = st.multiselect("Select Columns",all_columns)
                        new_df = data[selected_columns]
                        st.dataframe(new_df)
                        
                    if st.checkbox("Convert to Numeric type"):
                        all_columns = data.columns.to_list()
                        selected_col = st.multiselect("Select Numeric Columns",all_columns)
                        data[selected_col] = data[selected_col].astype(int)
                        st.write(selected_col, "Converted to numeric value")
                                
                    if st.checkbox("Show Product Images"):
                        for i in range(len(Image)):
                            st.image(Image[i], width=100, caption=data['Product_Name'][i])

                        
                    download = st.button('Download CSV File')
                    if download:
                        'Download Started!'
                        csv = data.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # some strings
                        linko= f'<a href="data:file/csv;base64,{b64}" download="flipkart-mobile.csv">Download csv file</a>'
                        st.markdown(linko, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()
