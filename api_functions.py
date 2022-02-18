import pandas as pd
import requests
import random
import string
from html_file_template import edit_html_body

def set_table_content(year,ids,firstname,surname,category,motivation,share):
    table_content = f'''<tr>
                        <td>{year}</td>
                        <td>{ids}</td>
                        <td>{firstname}</td>
                        <td>{surname}</td>
                        <td>{category}</td>
                        <td>{motivation}</td>
                        <td>{share}</td>
                        </tr>
                    '''
    return table_content

def set_dropdown_content(value):

    dd_content = f'''<option value="{value}">{value}</option>'''
    return dd_content

def generate_secret_key(length):
    pool = string.ascii_letters + string.digits
    return ''.join([random.choice(pool) for i in range(length)])

def get_unique_cat_year(data):

    df = pd.DataFrame(data)
    year_list = [int(i) for i in df['year'].unique()]
    category_list = [str(i) for i in df['category'].unique()]
    return category_list,year_list

def clean_data(data):

    df = pd.DataFrame(data['prizes'])
    df = df.drop(df[df['laureates'].isna()].index)
    df['overallMotivation'] = df['overallMotivation'].fillna("")
    df['overallMotivation'] = df['overallMotivation'].apply(lambda x: x.strip() if x != "" else x)
    laureates_list = []
    for i in df.itertuples():
        year = i.year
        cat = i.category
        motiv = i.overallMotivation
        for j in i.laureates:
            ids = j.get("id",'')
            firstname = j.get("firstname",'')
            surname = j.get("surname",'')
            nob_motiv = j.get("motivation",'')
            share = j.get('share','')
            laureates_list.append(dict(year=year,category=cat,id=ids,firstname=firstname,
                                        surname=surname,motivation=nob_motiv,share=share,overallMotivation=motiv))
    main_df = pd.DataFrame(laureates_list)
    main_df['motivation'] = main_df['motivation'].apply(lambda x: x.strip('"') if x != "" else x)
    return main_df.to_dict(orient="records")

def get_all_base_data():

    r = requests.get('http://api.nobelprize.org/v1/prize.json')
    response_data = r.json()
    return clean_data(response_data)
    

def get_people_won_multiple(base_data=''):

    if base_data == '':
        base_data = get_all_base_data()

    main_df = pd.DataFrame(base_data)
    test_df = main_df[["id","year","firstname"]]
    test_df = test_df.groupby(["id"]).count().reset_index()
    maxi = test_df.loc[test_df['year']>1]
    more_than_1 = maxi['id'].unique()
    last = main_df[main_df['id'].isin(more_than_1)]
    last.drop_duplicates(inplace=True)
    base_data = last.to_dict(orient="records")
    table_data = ''
    for i in base_data:
        table_data = f"{table_data}{set_table_content(i['year'],i['id'],i['firstname'],i['surname'],i['category'],i['motivation'],i['share'])}"
    html_body = edit_html_body('Noble Laureates with more than one award','Noble Laureates with more than one award',table_data,'','')
    return html_body

def get_noble_laureates_data(base_data='',category="all",year="all"):

    if base_data == '':
        base_data = get_all_base_data()

    category_dd = ''
    year_dd = ''
    table_data = ''
    cat_list,year_list = get_unique_cat_year(base_data)
    for i in cat_list:
        category_dd = f"{category_dd}{set_dropdown_content(i)}"
    for i in year_list:
        year_dd = f"{year_dd}{set_dropdown_content(i)}"
    
    if category == 'all' or year == 'all':
        
        for i in base_data:
            table_data = f"{table_data}{set_table_content(i['year'],i['id'],i['firstname'],i['surname'],i['category'],i['motivation'],i['share'])}"
    
    else:
        df = pd.DataFrame(base_data)
        df = df.loc[(df['category'] == category) & (df['year'] == year)]
        base_data = df.to_dict(orient="records")
        for i in base_data:
            table_data = f"{table_data}{set_table_content(i['year'],i['id'],i['firstname'],i['surname'],i['category'],i['motivation'],i['share'])}"

    html_body = edit_html_body(category,year,table_data,category_dd,year_dd)
    return html_body