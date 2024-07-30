import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#to change the page titile and width e space baranor jonno
st.set_page_config(layout='wide',page_title='StartUp Analysis')

#some data manupulation
rd = pd.read_csv('startup-cleaned-data.csv')
rd['date']=pd.to_datetime(rd['date'],errors='coerce')
rd['year'] = rd['date'].dt.year
rd['month']=rd['date'].dt.month

#Sidebar Layout
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Startup','Analysis','Investor'])


#Overall Analysis function

def overall_analysis():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Total money invested on startups
        total = round(rd['amount'].sum())
        st.metric('Total',str(total) + ' '+'cr')

    with col2:
        # max
        max = round(rd.groupby('startup')['amount'].max().sort_values(ascending=False)[0])
        st.metric('Max', str(max) + ' ' + 'cr')

    with col3:
        #max
        avg = round(rd.groupby('startup')['amount'].sum().mean())
        st.metric('Avg', str(avg) + ' ' + 'cr')

    with col4:
        #total_funded_startup
        startup = rd['startup'].nunique()
        st.metric('Funded Startups', str(startup) + ' ' + 'cr')


    # Mom chart -> total/count

    st.header('MOM Graph')
    mom_option = st.selectbox('Select-Type',['Total','Startup-Count'])

    if mom_option == 'Total':
        temp_rd = rd.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_rd = rd.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_rd['x_axis'] = temp_rd['month'].astype('str') + '-' + temp_rd['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_rd['x_axis'], temp_rd['amount'])
    
    #Rotation and Font Size Adjustment of x-axis labels
    plt.xticks(rotation=45,fontsize=4.5)

    st.pyplot(fig5)

    #Top sector
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Top 5 Sectors')
        top_sector = rd.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
        # pie chart
        fig6, ax6 = plt.subplots()
        ax6.pie(top_sector, labels=top_sector.index, autopct="%0.01f%%")

        st.pyplot(fig6)

    # Common Type of Funding
    with col2:
        st.subheader('Common Type of Funding')
        type_of_funding = rd.groupby('round')['amount'].sum().sort_values(ascending = False).head(5)

        # pie chart
        fig7, ax7 = plt.subplots()
        ax7.pie(type_of_funding, labels=type_of_funding.index, autopct="%0.01f%%")

        st.pyplot(fig7)

    col1,col2=st.columns(2)
    with col1:
        #Top Startup Year wise

        st.subheader('Top Startup per year')
        yearly_startup = rd.groupby(['year','startup'])['amount'].sum().reset_index().sort_values(['year', 'amount'], ascending=[True, False]).groupby('year').head(1)
        st.dataframe(yearly_startup)
    with col2:

        #Top 5 Investors
        st.subheader('Top 5 Investors')
        top_investors = rd.groupby('investors')['amount'].sum().sort_values(ascending=False).head(5)

        # pie chart
        fig8, ax8 = plt.subplots()
        ax8.pie(top_investors, labels=top_investors.index, autopct="%0.01f%%")

        st.pyplot(fig8)

#investor details function
def investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')
    #recent five investments of an investor
    recent_investments = st.dataframe(rd[rd['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']])

    # Add vertical space between the rows
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Biggest Investment
    col1,col2 = st.columns(2)

    with col1:
        st.subheader('Biggest Investments')
        biggest_investment = st.dataframe(rd[rd['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head())

    with col2:
        #Biggest Investments Bar chart
        biggest_investment = rd[rd['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader("Biggest Investments")
        #bar chart
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)

        st.pyplot(fig)

    # Add vertical space between the rows
    st.markdown("<br><br>", unsafe_allow_html=True)

    col3,col4,col5 = st.columns(3)

    # General investments
    with col3:

        st.subheader('Investment Areas')
        investment_areas = rd[rd['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values\
            (ascending=False)

        #pie chart
        fig1, ax1 = plt.subplots()
        ax1.pie(investment_areas,labels=investment_areas.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    with col4:
        #round investment
        st.subheader('Investment Rounds')
        investment_rounds = rd[rd['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False)

        #pie chart
        fig2, ax2 = plt.subplots()
        ax2.pie(investment_rounds,labels=investment_rounds.index,autopct="%0.01f%%")

        st.pyplot(fig2)

    with col5:
        #city
        st.subheader('Common Cities')
        investment_city = rd[rd['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False)
        #pie chart
        fig3, ax3 = plt.subplots()
        ax3.pie(investment_city,labels=investment_city.index,autopct="%0.01f%%")

        st.pyplot(fig3)


    # Each year investment amount of an investor
    col6,col7=st.columns(2)

    with col6:

        per_year = rd[rd['investors'].str.contains(investor)].groupby('year')['amount'].sum()

        #plot
        st.subheader('Per Year Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(per_year.index,per_year.values)

        st.pyplot(fig4)

def startup_analysis(startup):
    st.title(startup)
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)

    with col1:
        industry = rd[rd['startup'].str.contains(startup)]['vertical'].values[0]
        st.subheader('Industry')
        st.write(industry)

    with col2:
        sub_industry = rd[rd['startup'].str.contains(startup)]['subvertical'].values[0]
        st.subheader('Sub-Industry')
        st.write(sub_industry)

    with col3:
        city = rd[rd['startup'].str.contains(startup)]['city'].values[0]
        st.subheader('Location')
        st.write(city)

    st.markdown("<br>", unsafe_allow_html=True)

    #Funding rounds(stage,date,investors)
    st.subheader('Funding Rounds')
    funding_rounds = rd[rd['startup'].str.contains(startup)][['round', 'investors', 'date']]
    funding_rounds.rename(columns={'round': 'stage'})
    st.dataframe(funding_rounds)

    st.markdown("<br>", unsafe_allow_html=True)
    #similar Companies
    st.subheader('Similar Companies')
    ver = rd.groupby('vertical')['startup']
    for vertical, companies in ver:
        companies.tolist()

    target_company = startup
    target_vertical = rd[rd['startup'] == target_company]['vertical'].values[0]

    similar_companies = rd[rd['vertical'] == target_vertical]['startup'].reset_index().drop(columns='index')
    similar_companies=similar_companies[~similar_companies['startup'].str.contains(target_company)]
    st.dataframe(similar_companies)


if option == 'Startup':
    startup_name = st.sidebar.selectbox('Select One',sorted(rd['startup'].unique()))
    btn1 = st.sidebar.button('Find Startup Details')

    if btn1:
        startup_analysis(startup_name)

elif option == 'Analysis':
    btn0 = st.sidebar.button('Overall Analysis')
    if btn0 or st.session_state.get('overall_analysis_active', False):
        st.session_state['overall_analysis_active'] = True
        st.title('Overall Analysis')
        overall_analysis()


elif option == 'Investor':
    investor_name = st.sidebar.selectbox('Select One', sorted(set(rd['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')

    if btn2:
        investor_details(investor_name)
