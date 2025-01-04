
from turtle import color
import streamlit as st
from data_manipulation import data
from streamlit_condition_tree import condition_tree, config_from_dataframe

df = data()



title = st.title('Free to play games analysis')

col1,col2,col3 = st.columns(3)

distinct_genre = df['genre'].drop_duplicates(keep='first').sort_values()


    

with col2:
    selected_genre = st.multiselect('Select Genree',distinct_genre)


filtered_data = df[['id','genre','title','platform','publisher','developer','release_date','thumbnail','release_year','release_month']]

with col3:
    selected_columns = st.multiselect('Select Columns',
                                      filtered_data.columns,
                                      default=['id'],
                                      placeholder="Choose columns to display data",
                                      help="""If you would like to see more data,
                                        please select columns, without id chart can't be displayed""")

filtered_data = df[selected_columns]
with col1:
    config = config_from_dataframe(filtered_data)
    query_string = condition_tree(
        config=config,
        always_show_buttons=True,
        placeholder='Filter',
        min_height=100

    )

filtered_data = filtered_data.query(query_string)

columns_list = filtered_data.columns


if len(selected_genre) != 0 and 'genre' in columns_list:
    filtered_data = filtered_data[
        (filtered_data['genre'].isin(selected_genre))
        ]
    table = st.dataframe(filtered_data,use_container_width=True)
elif len(selected_columns) == 0:
    st.info('Select columns to analyze')
else:


    table = st.dataframe(filtered_data,
                         use_container_width=True,
                         column_config={
                             'id' : st.column_config.TextColumn('id'),
                             'release_date' : st.column_config.DateColumn('Release date'),
                             'thumbnail' : st.column_config.ImageColumn('Thumbnail'),
                             'release_year' : st.column_config.NumberColumn('Release year',format="%d"),

                         })



col4,col5 = st.columns(2)


if 'id' not in selected_columns:
    st.info('To display chart you need to select id')
elif len(selected_columns) == 1 and 'id' in selected_columns:
    st.info('Please select one more column')
else:

    bar_chart_column_list = []

    for i in columns_list:
        if len(filtered_data[i].drop_duplicates(keep='first')) < 40:
            bar_chart_column_list.append(i)


    with col4:
        bar_chart_column_chooser = st.selectbox('Choose x - column',bar_chart_column_list,key='bar')
        st.subheader("Bar Chart")
        grouped_data = filtered_data.groupby(bar_chart_column_chooser)[df.columns[0]].count()
        grouped_data = grouped_data.reset_index()
        chart = st.bar_chart(grouped_data,x=bar_chart_column_chooser,y=df.columns[0])




with col5:

    line_chart_column_list = []
    for i in columns_list:
        if i in ['release_month','release_year','release_date']:
            line_chart_column_list.append(i)

    if len(line_chart_column_list) != 0:
    # if 'release_year' in columns_list and 'id' in columns_list:
        line_chart_column_chooser = st.selectbox('Choose x - column',line_chart_column_list,key='line')
        st.subheader("Release games per year")
        grouped_data = filtered_data.groupby(line_chart_column_chooser)[df.columns[0]].count()
        grouped_data = grouped_data.reset_index()
        print(grouped_data)
        line_chart = st.line_chart(grouped_data,x=line_chart_column_chooser,y='id')
    else:
        st.info("To display line chart add release year to columns")
    