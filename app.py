from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('trending.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scrore = pickle.load(open('similarity_scrore.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = popular_df['Book-Title'].values,
                           author = popular_df['Book-Author'].values,
                           image = popular_df['Image-URL-M'].values,
                           votes = popular_df['num_rating'].values,
                           rating = popular_df['avg_rating'].values
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scrore[index])),key= lambda x:x[1],reverse =True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    #data ko frontend per bhejne ke liye we will use & after this use jinja template 
    #return str(user_input)
    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__  == '__main__':
    app.run(debug=True)