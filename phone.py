import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json
from PIL import Image


#Data frame Converttion

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Josunny",
                        database="phonepe",
                        port="5432")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                             "Transaction_count","Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts",
                                             "Registered_User","App_opens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                             "Registered_Users"))


#transaction Year based
def Transaction_amount_count_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyG=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyG, x="States",y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=700,width=600)
        
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyG, x="States",y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=600)
        
        st.plotly_chart(fig_count)
    

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyG, geojson=data1,locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyG["Transaction_amount"].min(),tacyG["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds= "locations",
                                height=700,width=500)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyG, geojson=data1,locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyG["Transaction_count"].min(),tacyG["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds= "locations",
                                height=700,width=500)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tacy

#transaction Quarter based
def Transaction_amount_count_Y_Q(df, Quarter):
    tacy=df[df["Quarter"]==Quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyG=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyG, x="States",y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Magenta_r, height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count=px.bar(tacyG, x="States",y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyG, geojson=data1,locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyG["Transaction_amount"].min(),tacyG["Transaction_amount"].max()),
                                hover_name="States",title=f"{tacy['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT",
                                fitbounds= "locations",
                                height=700,width=500)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyG, geojson=data1,locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyG["Transaction_count"].min(),tacyG["Transaction_count"].max()),
                                hover_name="States",title=f"{tacy['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT",
                                fitbounds= "locations",
                                height=700,width=500)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

#Aggregated Transaction type
def aggre_tran_transaction_type(df, state):
    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyG=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyG.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_pie_1= px.pie(data_frame= tacyG,names= "Transaction_type", values= "Transaction_amount",
                        width=500, title= f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2= px.pie(data_frame= tacyG,names= "Transaction_type", values= "Transaction_count",
                        width=500, title= f"{state.upper()}TRANSACTION COUNT", hole=0.5)

        st.plotly_chart(fig_pie_2)

#Aggre_user Year based
def Aggre_user_plot_1(df, year):   
    agg_user_Y=df[df["Years"]== year]
    agg_user_Y.reset_index(drop=True,inplace=True)

    agg_user_Y_G=pd.DataFrame(agg_user_Y.groupby("Brands")[["Transaction_count"]].sum())
    agg_user_Y_G.reset_index(inplace=True)

    fig_bar_1=px.bar(agg_user_Y_G, x="Brands", y="Transaction_count", 
                     title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_1)

    return agg_user_Y

#Agger_user_Quater Based
def Aggre_user_plot_2(df, quarter):
    agg_user_Y_Q=df[df["Quarter"]== quarter]
    agg_user_Y_Q.reset_index(drop=True,inplace=True)

    agg_user_Y_Q_G=pd.DataFrame(agg_user_Y_Q.groupby("Brands")["Transaction_count"].sum())
    agg_user_Y_Q_G.reset_index(inplace=True)


    fig_bar_1=px.bar(agg_user_Y_Q_G, x="Brands", y="Transaction_count", 
                     title=f"QUARTER {quarter}, BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.haline_r)

    st.plotly_chart(fig_bar_1)

    return agg_user_Y_Q

#Aggre_user_State wise
def Aggre_user_plot_3(df, state):
    aggre_user_Y_Q_S=df[df["States"]==state]
    aggre_user_Y_Q_S.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(aggre_user_Y_Q_S,x="Brands", y="Transaction_count", hover_data="Percentage",
                    title= f"{state.upper()}  BRANDS, TRANSACTION COUNT & PERCENTAGE", width=1000,markers=True,
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    
    st.plotly_chart(fig_line_1)

#Map Districts
def Map_insurance_districts(df, state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyG=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyG.reset_index(inplace=True)

    
    col1,col2=st.columns(2)

    with col1:

        fig_bar_1= px.bar(data_frame= tacyG, x= "Transaction_amount",y="Districts",orientation="h",
                        color_discrete_sequence= px.colors.sequential.Mint_r,height=600, 
                        title= f"{state.upper()}  DISTRICT AND TRANSACTION AMOUNT")

        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(data_frame= tacyG, x= "Transaction_count",y="Districts",orientation="h",
                        color_discrete_sequence= px.colors.sequential.Burgyl_r, height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT")


        st.plotly_chart(fig_bar_2)

#Map User Year plot 1
def map_user_plot_1(df, year):

    Map_user_Y=df[df["Years"]== year]
    Map_user_Y.reset_index(drop=True,inplace=True)

    Map_user_Y_G=Map_user_Y.groupby("States")[["Registered_User", "App_opens"]].sum()
    Map_user_Y_G.reset_index(inplace=True)

    fig_line_1=px.line(Map_user_Y_G,x="States", y=["Registered_User","App_opens"],
                        title= f"{year} REGISTERED USER AND APP OPENS", width=1000,markers=True,
                        height=800)
                        
    st.plotly_chart(fig_line_1)

    return Map_user_Y

#Map User Quarter plot 2
def map_user_plot_2(df, Quarter):

    Map_user_Y_Q=df[df["Quarter"]== Quarter]
    Map_user_Y_Q.reset_index(drop=True,inplace=True)

    Map_user_Y_Q_G=Map_user_Y_Q.groupby("States")[["Registered_User", "App_opens"]].sum()
    Map_user_Y_Q_G.reset_index(inplace=True)

    fig_line_1=px.line(Map_user_Y_Q_G,x="States", y=["Registered_User","App_opens"],
                        title= f" YEAR {df['Years'].min()}  OF {Quarter} QUARTER REGISTERED USER AND APP OPENS",
                        width=1000,markers=True,height=800,
                        color_discrete_sequence=px.colors.sequential.Rainbow
                        )
    st.plotly_chart(fig_line_1)

    return Map_user_Y_Q

# Map User states plot 3
def map_user_plot_3(df, states):
    map_user_Y_Q_S=df[df["States"]==states]
    map_user_Y_Q_S.reset_index(drop=True,inplace=True)

    fig_map_user_bar_1=px.bar(map_user_Y_Q_S,x= "Registered_User", y="Districts", orientation="h",
                            title= f"{states.upper()} DISTRICT WISE REGISTERED USER", height=800, 
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2=px.bar(map_user_Y_Q_S,x= "App_opens", y="Districts", orientation="h",
                            title=f"{states.upper()} DISTRICT WISE APP OPENS", height=800, 
                            color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_bar_2)

#Top state based pincode tranc amount and count
def Top_pincode_states_plot_1(df, state):
    
    Top_insurance_Y_S=df[df["States"]== state]
    Top_insurance_Y_S.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_Top_insurance_bar_1=px.bar(Top_insurance_Y_S,x= "Quarter", y="Transaction_amount",
                                    hover_data="Pincodes",
                                    title=  f"{state.upper()} TRANSACTION AMOUNT", height=650,width=600, 
                                    color_discrete_sequence=px.colors.sequential.Rainbow
                                    )
        st.plotly_chart(fig_Top_insurance_bar_1)
    
    with col2:

        fig_Top_insurance_bar_2=px.bar(Top_insurance_Y_S,x= "Quarter", y="Transaction_count", hover_data="Pincodes",
                                title=f"{state.upper()} TRANSACTION COUNT", height=650,width=600,  
                                color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_Top_insurance_bar_2)

# top user Year based
def top_user_year(df, year):   
    top_user_Y=df[df["Years"]== year]
    top_user_Y.reset_index(drop=True,inplace=True)

    top_user_Y_G=pd.DataFrame(top_user_Y.groupby(["States","Quarter"])["Registered_Users"].sum())
    top_user_Y_G.reset_index(inplace=True)

    fig_top_plot_1=px.bar(top_user_Y_G, x="States", y="Registered_Users", color="Quarter", 
                        color_discrete_sequence=px.colors.sequential.Burgyl, width=900, height=800,
                        hover_name="States",title=f"{year} REGISTERED USER"
                        )
    st.plotly_chart(fig_top_plot_1)

    return top_user_Y

#top user state based
def top_user_state(df, state):
    top_user_Y_S=df[df["States"]==state]
    top_user_Y_S.reset_index(drop=True,inplace=True)

    fig_top_1=px.bar(top_user_Y_S, x="Quarter", y= "Registered_Users", 
                     title=f"{state.upper()} REGISTERED USER, PINCODES AND QUARTERS",
                    width=1000, height=800, color="Registered_Users", hover_data= "Pincodes",
                    color_continuous_scale=px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_1)

#sql connection
#Transaction Amount
def chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''select "States", sum ("Transaction_amount") as transaction_amount 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States","Transaction Amount" ))

    col1, col2=st.columns(2)

    with col1:

        fig_bar_1=px.bar(df_1, x="States", y="Transaction Amount", title= "STATES AND TRANSACTION AMOUNT TOP 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Bluered_r,
                            hover_data="States")

        st.plotly_chart(fig_bar_1)

    #plot 2
    Query_2=f'''select "States", sum ("Transaction_amount") as transaction_amount 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_amount 
                LIMIT 10;'''

    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States","Transaction Amount" ))

    with col2:
        fig_bar_2=px.bar(df_2, x="States", y="Transaction Amount", title= "STATES AND TRANSACTION AMOUNT LAST 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Bluered,
                            hover_data="States")

        st.plotly_chart(fig_bar_2)

    #plot_3

    Query_3= f'''select "States", AVG ("Transaction_amount") as transaction_amount 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_amount;'''
            

    cursor.execute(Query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States","Transaction Amount" ))

    fig_bar_3=px.bar(df_3, y="States", x="Transaction Amount", title= "STATES AND TRANSACTION AMOUNT AVERAGE",
                        width=1000,height=800, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="States", orientation="h")

    st.plotly_chart(fig_bar_3)


#sql connection
#transaction count
def chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''select "States", sum ("Transaction_count") as transaction_count 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_count DESC
                LIMIT 10;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States","Transaction Count" ))

    col1, col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(df_1, x="States", y="Transaction Count", title= "TRANSACTION COUNT TOP 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Magenta_r,
                            hover_data="States")

        st.plotly_chart(fig_bar_1)

    #plot 2
    Query_2=f'''select "States", sum ("Transaction_count") as Transaction_count 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_count 
                LIMIT 10;'''

    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States","Transaction Count" ))

    with col2:
        fig_bar_2=px.bar(df_2, x="States", y="Transaction Count", title= "TRANSACTION COUNT LAST 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.GnBu_r,
                            hover_data="States")

        st.plotly_chart(fig_bar_2)

    #plot_3

    Query_3= f'''select "States", AVG ("Transaction_count") as Transaction_count 
                from {table_name}
                GROUP BY "States"
                ORDER BY Transaction_count;'''
            

    cursor.execute(Query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States","Transaction Count" ))

    fig_bar_3=px.bar(df_3, y="States", x="Transaction Count", title= "TRANSACTION COUNT AVERAGE",
                        width=1000,height=850, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="States", orientation="h")

    st.plotly_chart(fig_bar_3)

#sql connection
#Map Registered User
def chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''SELECT "Districts", SUM("Registered_User") AS Registered_User FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY Registered_User DESC
                LIMIT 10;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts","Registered_User"))

    col1,col2=st.columns(2)

    with col1:

        fig_bar_1=px.bar(df_1, x="Districts", y="Registered_User", title= "REGISTERED USER TOP 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Magenta_r,
                            hover_data="Districts")

        st.plotly_chart(fig_bar_1)

    #plot 2
    Query_2=f'''SELECT "Districts", SUM("Registered_User") AS Registered_User 
                FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY Registered_User 
                LIMIT 10;'''

    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts","Registered_User" ))

    with col2:

        fig_bar_2=px.bar(df_2, x="Districts", y="Registered_User", title= " REGISTERED USER LAST 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.GnBu_r,
                            hover_data="Districts")

        st.plotly_chart(fig_bar_2)

    #plot_3

    Query_3= f'''SELECT "Districts", AVG ("Registered_User") AS Registered_User FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY Registered_User '''

            

    cursor.execute(Query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts","Registered_User"))

    fig_bar_3=px.bar(df_3, y="Districts", x="Registered_User", title= " REGISTERED USER AVERAGE",
                        width=1000,height=850, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="Districts", orientation="h")

    st.plotly_chart(fig_bar_3)

#sql connection
#Map app opens
def chart_App_opens(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''SELECT "Districts", SUM("App_opens") AS App_opens FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY App_opens DESC
                LIMIT 10;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts","App_opens"))

    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(df_1, x="Districts", y="App_opens", title= "APP OPENS TOP 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Magenta_r,
                            hover_data="Districts")

        st.plotly_chart(fig_bar_1)

    #plot 2
    Query_2=f'''SELECT "Districts", SUM("App_opens") AS App_opens 
                FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY App_opens 
                LIMIT 10;'''

    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts","App_opens" ))

    
    with col2:

        fig_bar_2=px.bar(df_2, x="Districts", y="App_opens", title= " APP OPENS LAST 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.GnBu_r,
                            hover_data="Districts")

        st.plotly_chart(fig_bar_2)

    #plot_3

    Query_3= f'''SELECT "Districts", AVG ("App_opens") AS App_opens FROM {table_name}
                WHERE "States"='{state}'
                GROUP BY "Districts" 
                ORDER BY App_opens '''

            

    cursor.execute(Query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts","App_opens"))

    fig_bar_3=px.bar(df_3, y="Districts", x="App_opens", title= " APP OPENS AVERAGE",
                         width=1000,height=850, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="Districts", orientation="h")

    st.plotly_chart(fig_bar_3)

#sql connection
#TOP Registered User
def top_chart_registered_user(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''SELECT "States", SUM("Registered_Users") AS Registered_Users 
                FROM  {table_name}
                GROUP BY "States"
                ORDER BY Registered_Users DESC
                LIMIT 10;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States","Registered_Users"))

    col1,col2=st.columns(2)

    with col1:

        fig_bar_1=px.bar(df_1, x="States", y="Registered_Users", title= "REGISTERED USER TOP 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.Magenta_r,
                            hover_data="States")

        st.plotly_chart(fig_bar_1)

    #plot 2
    Query_2=f'''SELECT "States", SUM("Registered_Users") AS Registered_Users 
                FROM {table_name}
                GROUP BY "States"
                ORDER BY Registered_Users 
                LIMIT 10;'''

    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States","Registered_Users" ))

    with col2:

        fig_bar_2=px.bar(df_2, x="States", y="Registered_Users", title= " REGISTERED USER LAST 10",
                            width=600,height=650, color_discrete_sequence=px.colors.sequential.GnBu_r,
                            hover_data="States")

        st.plotly_chart(fig_bar_2)

    #plot_3

    Query_3= f'''SELECT "States", AVG ("Registered_Users") AS Registered_Users 
                    FROM {table_name}
                    GROUP BY "States"
                    ORDER BY Registered_Users ;'''

    cursor.execute(Query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States","Registered_Users"))

    fig_bar_3=px.bar(df_3, y="States", x="Registered_Users", title= " REGISTERED USER AVERAGE",
                        width=1000,height=850, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data="States", orientation="h")

    st.plotly_chart(fig_bar_3)

#sql connection
#Aggre Transaction type amount and count 
def chart_aggre_trans_type(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''SELECT "Transaction_type" ,SUM("Transaction_count") AS Transaction_count 
                FROM  {table_name}
                where "States" = '{state}'
                GROUP BY "Transaction_type"
                ORDER BY Transaction_count'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Transaction_type","Transaction_count"))

    

    fig_pie_1= px.pie(data_frame= df_1,names= "Transaction_type", values= "Transaction_count",
                    width=850, height=650,title= "TRANSACTION COUNT", hole=0.5,)


    st.plotly_chart(fig_pie_1)

    #plot 2 

    Query_2=f'''SELECT "Transaction_type" ,SUM ("Transaction_amount") AS Transaction_amount
                FROM  {table_name}
                where "States" = '{state}'
                GROUP BY "Transaction_type"
                ORDER BY Transaction_amount ;'''
               
    cursor.execute(Query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Transaction_type","Transaction_amount"))

  
    fig_pie_2= px.pie(data_frame= df_2,names= "Transaction_type", values= "Transaction_amount",
                    width=850,height=650, title= "TRANSACTION AMOUNT", hole=0.5,)


    st.plotly_chart(fig_pie_2)

#sql connection
#Aggre user brand and count 
def chart_aggre_user_type(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Josunny",
                            database="phonepe",
                            port="5432")
    cursor=mydb.cursor()

    #plot 1
    Query_1=f'''SELECT "Brands" ,SUM ("Transaction_count") AS Transaction_count
                FROM  {table_name}
                where "States" = '{state}' 
                GROUP BY "Brands"
                ORDER BY Transaction_count ;'''

    cursor.execute(Query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Brands","Transaction_count"))

    fig_pie_1= px.bar(df_1, x="Brands",y="Transaction_count", title="TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)


    st.plotly_chart(fig_pie_1)


#Streamlit Part

st.set_page_config(page_title= "PHONEPE DATA VISUALIZATION AND EXPLORATION",  
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                  )

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    select= option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS", "ABOUT"],
                        icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "20px", "text-align": "left", 
                                            "margin": "-2px", "--hover-color": "#6F36AD"},
                                            "nav-link-selected": {"background-color": "#6F36AD"}})

if select== "HOME":
    
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
        

    with col2:
        st.image("home.png")


elif select== "DATA EXPLORATION":
    
    
    tab1, tab2, tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        
        method=st.radio("Select the Method",["Insurance Analysis",
                                             "Transaction Analysis",
                                             "User Analysis"]
                                             )

        if method=="Insurance Analysis":
            
            #Year based transaction amount and count 
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year",Aggre_insurance["Years"].min(),
                                                    Aggre_insurance["Years"].max(),
                                                    Aggre_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            #Quarter based transaction amount and count 
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters",tac_Y["Quarter"].unique())
                                                    
            Transaction_amount_count_Y_Q(tac_Y, quarters)
            
            

        elif method=="Transaction Analysis":
            #Year based transaction amount and count 
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year",Aggre_transaction["Years"].min(),
                                                    Aggre_transaction["Years"].max(),
                                                    Aggre_transaction["Years"].min())
            aggre_tran_tac_y=Transaction_amount_count_Y(Aggre_transaction, years)
            
            #States based transaction type
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States for Transaction Type",
                                     aggre_tran_tac_y["States"].unique())

            aggre_tran_transaction_type(aggre_tran_tac_y, states)

            #Quarter based transaction amount and count 
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters",aggre_tran_tac_y["Quarter"].unique())
                                                   
            aggre_tran_tac_y_Q=Transaction_amount_count_Y_Q(aggre_tran_tac_y,quarters)

            #Quarter based transaction type 
            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Transaction Type(Quarters)",
                                     aggre_tran_tac_y_Q["States"].unique())

            aggre_tran_transaction_type(aggre_tran_tac_y_Q, states)

        elif method=="User Analysis":
            
            #Year based transaction count and brands
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year",Aggre_user["Years"].min(),
                                                    Aggre_user["Years"].max(),
                                                    Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user, years)

            #Quarter based transaction count and brands
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters",Aggre_user_Y["Quarter"].unique())
                                                    
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters )

            #State based Brands, Transaction count and percentage
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:

        method_2= st.radio("Select the Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            #Year based Transaction Amount and count
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Map Insurance",
                                                    Map_insurance["Years"].min(),
                                                    Map_insurance["Years"].max(),
                                                    Map_insurance["Years"].min())
                                                    
            Map_insurance_tac_y=Transaction_amount_count_Y(Map_insurance, years) 

            #State based District Transaction Amount and Count
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States for Map Insurance",
                                     Map_insurance_tac_y["States"].unique())

            Map_insurance_districts(Map_insurance_tac_y, states)

            #Quarters based Transaction Amount and count
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters for Map Insurance",
                                                    Map_insurance_tac_y["Quarter"].unique())
                                                    
            Map_insurance_tac_y_Q=Transaction_amount_count_Y_Q(Map_insurance_tac_y,quarters)

            #State based Quarter District Transaction Amount and Count
            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Quarter in Map Insurance", 
                                    Map_insurance_tac_y_Q["States"].unique())

            Map_insurance_districts(Map_insurance_tac_y_Q, states)


        elif method_2 == "Map Transaction":
            
            #Year based Transaction Amount and count
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Map transaction",
                                                    Map_transaction["Years"].min(),
                                                    Map_transaction["Years"].max(),
                                                    Map_transaction["Years"].min())
                                                    
            Map_transaction_tac_y=Transaction_amount_count_Y(Map_transaction, years) 

            #State based District Transaction Amount and Count
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States for Map transaction", 
                                    Map_transaction_tac_y["States"].unique())

            Map_insurance_districts(Map_transaction_tac_y, states)

            #Quarters based Transaction Amount and count
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters (District wise) for Map transaction",
                                                    Map_transaction_tac_y["Quarter"].unique())
            Map_transaction_tac_y_Q=Transaction_amount_count_Y_Q(Map_transaction_tac_y,quarters)

            #State based Quarter District Transaction Amount and Count
            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Quarter in Map transaction",
                                     Map_transaction_tac_y_Q["States"].unique())

            Map_insurance_districts(Map_transaction_tac_y_Q, states)

        elif method_2 == "Map User":
            
            # year based on Registered user and app opens
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Map User",Map_user["Years"].min(),
                                                    Map_user["Years"].max(),
                                                    Map_user["Years"].min())
                                                   
            Map_User_Y=map_user_plot_1(Map_user, years) 
            
            #Quarters based on Registered user and app opens
            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters for Map User",
                                                    Map_User_Y["Quarter"].unique())
                                                    
            Map_User_Y_Q=map_user_plot_2(Map_User_Y,quarters)

            #District wise Registered user and app opens
            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Quarter (District wise) in Map User",
                                     Map_User_Y_Q["States"].unique())

            map_user_plot_3(Map_User_Y_Q, states)

    with tab3:

        method_3=st.radio("Select the Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Top Insurance",
                                                    Top_insurance["Years"].min(),
                                                    Top_insurance["Years"].max(),
                                                    Top_insurance["Years"].min())
                                                    
            top_insurance_Y=Transaction_amount_count_Y(Top_insurance, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Top Insurance",
                                     top_insurance_Y["States"].unique())

            Top_pincode_states_plot_1(top_insurance_Y, states)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters for Top Insurance",
                                                    top_insurance_Y["Quarter"].unique())
                                                    
            Top_insurance_y_Q=Transaction_amount_count_Y_Q(top_insurance_Y, quarters)

        if method_3 == "Top Transaction":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Top Transaction",
                                                    Top_transaction["Years"].min(),
                                                    Top_transaction["Years"].max(),
                                                    Top_transaction["Years"].min())
                                                    
            top_transaction_tac_Y=Transaction_amount_count_Y(Top_transaction, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Top Transaction",
                                     top_transaction_tac_Y["States"].unique())

            Top_pincode_states_plot_1(top_transaction_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.selectbox("Select the Quarters for Top Transaction",
                                                    top_transaction_tac_Y["Quarter"].unique())
                                                    
            Top_transaction_y_Q=Transaction_amount_count_Y_Q(top_transaction_tac_Y, quarters)


        if method_3 == "Top User":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year for Top User",
                                                    Top_user["Years"].min(),
                                                    Top_user["Years"].max(),
                                                    Top_user["Years"].min())
                                                    
            Top_user_Y=top_user_year(Top_user, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the States for Top User",
                                     Top_user_Y["States"].unique())

            top_user_state(Top_user_Y, states)

elif select == "TOP CHARTS":
    

    question=st.selectbox("Select the question",
                          ["1. Transaction amount and count of Aggregated Insurance",
                        "2. Transaction amount and count of Aggregated Transaction",
                        "3. Transaction Count of Aggregated User",
                        "4. Transaction amount and count of Map Insurance",
                        "5. Transaction amount and count of Map Transaction",
                        "6. Registered Users of Map User",
                        "7. App Opens of Map user",
                        "8. Transaction amount and count of Top Insurance",
                        "9. Transaction amount and count of Top Transaction",
                        "10. Registered Users of Top User",
                        "11. Transaction Type of Aggregated Transaction",
                        "12. Brands and Transaction Count in Aggregated User"])
    
    if question== "1. Transaction amount and count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("aggregated_insurance")

    elif question== "2. Transaction amount and count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("aggregated_transaction")

    elif question== "3. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("aggregated_user")

    elif question== "4. Transaction amount and count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("map_insurance")
    
    elif question== "5. Transaction amount and count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("map_transaction")

    elif question== "6. Registered Users of Map User":

        states=st.selectbox("Select the States",
                            Map_user["States"].unique())
        st.subheader("REGISTERED USER")
        chart_registered_user("map_user", states)

    elif question== "7. App Opens of Map user":

        states=st.selectbox("Select the States",
                            Map_user["States"].unique())
        st.subheader("APP OPENS")
        chart_App_opens("map_user", states)

    elif question== "8. Transaction amount and count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("top_insurance")

    elif question== "9. Transaction amount and count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        chart_transaction_count("top_transaction")

    elif question== "10. Registered Users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_user("top_user")

    elif question=="11. Transaction Type of Aggregated Transaction":

        st.subheader("TRANSACTION TYPE AMOUNT AND COUNT")

        states=st.selectbox("Select the States",
                            Aggre_transaction["States"].unique())

        chart_aggre_trans_type("aggregated_transaction", states)

    elif question=="12. Brands and Transaction Count in Aggregated User":

        st.subheader("BRANDS AND TRANSACTION  COUNT")

        states=st.selectbox("Select the States",
                            Aggre_user["States"].unique())
        chart_aggre_user_type("aggregated_user", states)


elif select == "ABOUT":

    col1,col2=st.columns(2)
    with col1:
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.image("IM 1.jpg")

    col3,col4 = st.columns(2,gap="medium")
    with col3:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
    with col4:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.jpg")

    col5,col6=st.columns(2)
    
    with col5:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("images.jpg")
        
    with col6:
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across India")

        
    st.subheader("BENEFINTS OF PHONEPE")

    col7,col8= st.columns(2)
    
    with col7:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    with col8:
        
        st.image("Phonecol7.jpg",width=600)

    col9,col10= st.columns(2)

    with col9:

        
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col10:
        
        

        st.image("phonepecol9.jpg", width=450)

    