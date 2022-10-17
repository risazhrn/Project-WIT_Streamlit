import streamlit as st
import pandas as pd
import datetime


st.set_page_config(layout="centered", page_icon=":cherry_blossom:",page_title="Cyber Women Community")


# Database
import sqlite3
conn = sqlite3.connect('women_community.db')
c = conn.cursor()

# Function Blog
def create_table_blog():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT, articles TEXT, postdate DATE)')

def add_data_blog(author,title,articles,postdate):
    c.execute('INSERT INTO blogtable(author,title,articles,postdate) VALUES (?,?,?,?)', (author,title,articles,postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def view_all_title():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data


def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}" '.format(title))
    data = c.fetchall()
    return data

def delete_data(title):
    c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
    conn.commit()

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

# Function Forum
def create_table_forum():
    c.execute('CREATE TABLE IF NOT EXISTS forum(nama TEXT,pesan TEXT, tgl DATE)')

def add_data_forum(nama, pesan, tgl):
    c.execute('INSERT INTO forum(nama, pesan, tgl) VALUES (?,?,?)', (nama, pesan, tgl))
    conn.commit()

def view_all_message():
    c.execute('SELECT * FROM forum')
    data = c.fetchall()
    return data

def drop():
    c.execute('DROP TABLE forum')


# Layout Templates
title_temp = """
<div style = "background-color:pink;padding:10px;margin:10px;border-radius:20px;border:1px solid #464e5f">
<div style="display:flex; padding:15px;background-color:#464e5f;border-radius:10px 10px 0px 0px">
<img src="https://i.pinimg.com/564x/25/96/13/25961379bae8246e53ae0f2ad5d3aef6.jpg" alt="Avatar" style="vertical-align:middle;float:left;width:50px;height:50px;border-radius:50px;">
<h5 style="color:pink;text-align:left;padding-left:10px;margin-top:10px;">{}</h5>
</div>

<h5 style="color:#464e5f;text-align:center;font-weight:700;margin-top:40px;">{}</h5>
<p style="color:#464e5f;text-align:justify;padding:20px;margin-bottom:20px;">{}</p>

</div>
<h6 style="text-align:right;padding:20px;">Post Date : {}</h6>

"""

search_temp = """
<div style="display:flex; padding:10px; background-color:pink; border-radius:20px;margin:10px;border:2px solid #464e5f">
<img src="https://i.pinimg.com/564x/25/96/13/25961379bae8246e53ae0f2ad5d3aef6.jpg" alt="Avatar" style="vertical-align:middle;float:left;width:50px;height:50px;border-radius:50px;">
<h5 style="text-align:left;padding-left:10px;margin-top:15px;font-weight:700;color:#464e5f">{}</h5>
</div>

<div style = "border:2px solid #464e5f;padding:10px;margin:10px;border-radius:20px;">


<h5 style="text-align:center;margin-top:20px;">{}</h5>
<p style="text-align:justify;padding:20px;margin-bottom:20px;">{}</p>

</div>
<h6 style="text-align:right;padding:20px;">Post Date : {}</h6>

"""


forum_temp = """

<div style = "background-color:pink;border:1px solid #464e5f;padding:10px;margin:10px;border-radius:20px;">

<h6 style="padding:2px;margin:8px">{}</h6>
<p style="padding:2px;margin:0px 0px 0px 8px">{}</p>

</div>
<p style="padding:2px;margin:2px 10px 10px 10px;float:right;">{}</p>

"""

chana_team_risa = """
<h5 style="text-align:center;padding:10px">Risa Zahrani</h5>

"""

chana_team_ana = """
<h5 style="text-align:center;padding:10px">Anastasia Santa Clara</h5>

"""

def main():
    st.title(":cherry_blossom: Cyber Women Community :cherry_blossom:")

    menu = ["Home",  "Feeds", "Search Article", "Add New Post", "Forum Discussion" , "Manage Feeds"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        space(2)
        st.subheader("Apa itu cyber women community?")
        st.text("""
            Cyber Women Community merupakan sebuah situs komunitas perempuan untuk sharing
            mengenai informasi cybercrime dan tips untuk menghindarinya,
            sehingga para wanita dapat lebih berhati - hati 
            terhadap kejahatan yang terjadi di dunia maya
        
        """)

        space(2)
        st.subheader("💖Chana Team")
        space(2)
        col1, col2 = st.columns(2)
        with col1: 
            st.image('./Risa.jpeg') 
            st.markdown(chana_team_risa, unsafe_allow_html=True)

        with col2:
            st.image('./anastasia.jpeg')
            st.markdown(chana_team_ana, unsafe_allow_html=True)




    if choice == "Add New Post":
        space(2)
        st.subheader("Add New Post")
        space(1)
        create_table_blog()
        blog_author = st.text_input("Nama Author", max_chars=50)
        blog_title = st.text_input("Judul Artikel")
        blog_articles = st.text_area("Isi Artikel")
        blog_post_date = st.date_input("Tanggal")

        if st.button("Tambah"):
            add_data_blog(blog_author,blog_title,blog_articles,blog_post_date)
            st.success("Artikel '{}' Berhasil di Posting".format(blog_title))


    if choice == "Feeds":
        space(2)
        result = view_all_notes()
        for i in result[::-1]:
            b_author = i[0]
            b_title = i[1]
            b_articles = i[2]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_author,b_title,b_articles,b_post_date), unsafe_allow_html=True)


    if choice == "Search Article":
        space(2)

        all_title = [i[0] for i in view_all_title()]

        if all_title == []:
            st.warning("Artikel Tidak Tersedia")
        
        elif all_title != [] :
            postlist = st.sidebar.selectbox("Judul Artikel", all_title)

            post_result = get_blog_by_title(postlist)
            for i in post_result:
                b_author = i[0]
                b_title = i[1]
                b_articles = i[2]
                b_post_date = i[3]
            st.markdown(search_temp.format(b_author,b_title,b_articles,b_post_date), unsafe_allow_html=True)


    if choice == "Forum Discussion":
        space(2)
        st.subheader("Forum Discussion")
        space(1)
        with st.expander("💬 Open Forum Discussion"):
            result = view_all_message()
            for i in result:
                f_nama = i[0]
                f_pesan = i[1]
                f_date = i[2]
                
                st.markdown(forum_temp.format(f_nama,f_pesan,f_date), unsafe_allow_html=True)

        with st.expander("💬 Send Message"):
            create_table_forum()

            nama = st.text_input("Nama", max_chars=50)
            pesan = st.text_area("Pesan")
            tgl = datetime.datetime.now().strftime("%x")

            if st.button("Kirim"):
                add_data_forum(nama,pesan,tgl)
                st.success("Pesan Terkirim")

        

    if choice == "Manage Feeds":
        space(2)
        st.subheader("Manage Feeds")

        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author","Title", "Articles","Post Date"])
        st.dataframe(clean_db)

        unique_titles = [i[0] for i in view_all_title()]
        delete_blog_by_title = st.selectbox("Hapus Artikel", unique_titles)

        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Artikel '{}' Berhasil di Hapus".format(delete_blog_by_title))




if __name__ == '__main__':
    main()