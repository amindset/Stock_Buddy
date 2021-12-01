import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime as dt
from pandas_datareader import data as web
import plotly.graph_objects as go

# Goal algorithm
# Grab Last Week Price




# Grabs chart based on past 3 months
# Projects a trendline

st.set_page_config(page_title="Stock Buddy", page_icon=":bar_chart:", layout='wide'
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" target="_blank">Stock Buddy</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="https://robinhood.com/">Robinhood <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.webull.com/" target="_blank">WeBull</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)



st.title('Stock Buddy Projection')

#stock = input("Type a Stock! ")
#stock = st.sidebar.multiselect("Select a stock: ", options = data['Ticker'].unique(), default="AAPL")
left_column, right_column = st.columns(2)
with left_column:
    stock = st.text_input("Select a stock: ", value="AAPL")
    st.write("You have selected: " + str(stock).replace('[',"").replace(']',"").replace("'",""))
    #st.dataframe(data)
    #st.title('Stock Buddy Projection')


    #print("You have selected... " + stock.upper())
    #length = len(stock)
    #i = 0

    #while i < length:
    #print(stock[i])

    #ticker = stock

    # Grab Price
    stockPrice = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '/financials?mod=mw_quote_tab'
    response = requests.get(stockPrice)
    soup = BeautifulSoup(response.text, "lxml")
    price = float(soup.find_all('div', {'class':"intraday__data"})[0].find('bg-quote').text.replace(',',''))


    # Grab Price Change
    #stockRevenue = soup.find_all('td', {'class':"table__cell positive"})[1].text
    # PE Ratio
    #pratio = 'https://www.marketwatch.com/investing/stock/' + stock + '?mod=mw_quote_tab'
    #response = requests.get(pratio)
    #soup = BeautifulSoup(response.text, "lxml")
    #peRatio = float(soup.find_all('li', {'class':"kv__item"})[8].find('span').text)

    #newsData = 'https://www.marketwatch.com/investing/stock/' + stock + '?mod=quote_search'
    #response = requests.get(newsData)
    #soup = BeautifulSoup(response.text, "lxml")
    #stockNews = soup.find_all('h3',{'class':"article__headline"})[0].find('a').text
    #stockNews2 = soup.find_all('h3',{'class':"article__headline"})[1].find('a').text
    #stockNews3 = soup.find_all('h3',{'class':"article__headline"})[2].find('a').text

    # Total Assets
    # Total Assets Growth
    # Total Shareholders' Equity / Total Assets
    balanceSheet = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '/financials/balance-sheet/quarter'
    response = requests.get(balanceSheet)
    soup = BeautifulSoup(response.text, "lxml")
    totalAssets = soup.find_all('div', {'class':"cell__content"})[166].find('span').text
    lastQTRassets = soup.find_all('div', {'class':"cell__content"})[165].find('span').text
    lastYearAssets = soup.find_all('div', {'class':"cell__content"})[162].find('span').text

    assetsGrowth = soup.find_all('div', {'class':"cell__content"})[294].find('span').text
    LQassetsGrowth = soup.find_all('div', {'class':"cell__content"})[293].find('span').text
    shareholderEquity = soup.find_all('div', {'class':"cell__content"})[622].find('span').text.replace('%','')
    LQshareholderEquity = soup.find_all('div', {'class':"cell__content"})[621].find('span').text.replace('%','')
    LYshareholderEquity = soup.find_all('div', {'class':"cell__content"})[618].find('span').text.replace('%','')


    # Total Liabilities
    totalLiability = soup.find_all('div', {'class':"cell__content"})[390].find('span').text
    lastQTRliability = soup.find_all('div', {'class':"cell__content"})[389].find('span').text
    lastYearLiability = soup.find_all('div', {'class':"cell__content"})[386].find('span').text

    if totalAssets[-1] == 'B':
        totA = float(totalAssets.replace('B',''))
    elif totalAssets[-1] == 'M':
        totA = float(totalAssets.replace('M',''))
    else:
        st.write('None')

    if lastQTRassets[-1] == 'B':
        LQtotA = float(lastQTRassets.replace('B',''))
    elif lastQTRassets[-1] == 'M':
        LQtotA = float(lastQTRassets.replace('M',''))
    else:
        st.write('None')

    if lastYearAssets[-1] == 'B':
        LYtotA = float(lastYearAssets.replace('B',''))
    elif lastYearAssets[-1] == 'M':
        LYtotA = float(lastYearAssets.replace('M',''))
    else:
        st.write('None')

    if totalLiability[-1] == 'B':
        totL = float(totalLiability.replace('B',''))
    elif totalLiability[-1] == 'M':
        totL = float(totalLiability.replace('M',''))
    else:
        st.write('None')

    if lastQTRliability[-1] == 'B':
        LQtotL = float(lastQTRliability.replace('B',''))
    elif lastQTRliability[-1] == 'M':
        LQtotL = float(lastQTRliability.replace('M',''))
    else:
        st.write('None')

    if lastYearLiability[-1] == 'B':
        LYtotL = float(lastYearLiability.replace('B',''))
    elif lastYearLiability[-1] == 'M':
        LYtotL = float(lastYearLiability.replace('M',''))
    else:
        st.write('None')


    # Total Liabilities / Total Assets
    debtRatio = totL / totA
    LQdebtRatio = LQtotL / LQtotA
    LYdebtRatio = LYtotL / LYtotA
        

    # Total Revenue - Total Expense
    nincome = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '/financials/income/quarter'
    response = requests.get(nincome)
    soup = BeautifulSoup(response.text, "lxml")
    netIncome = soup.find_all('div', {'class':"cell__content"})[318].find('span').text
    lastQTRnetIncome = soup.find_all('div', {'class':"cell__content"})[317].find('span').text
    lastYearnetIncome = soup.find_all('div', {'class':"cell__content"})[314].find('span').text

    if netIncome[-1] == 'B':
        netIn = float(netIncome.replace('B',''))*1000000000
        
    elif netIncome[-1] == 'M':
        netIn = float(netIncome.replace('M',''))*1000000

    elif netIncome[-2] == 'B':
        netIn = float(netIncome[1:-2])*1000000000
        
    elif netIncome[-2] == 'M':
        netIn = float(netIncome[1:-2])*1000000
        
    else:
        st.write('None')


    if lastQTRnetIncome[-1] == 'B':
        netQTR = float(lastQTRnetIncome.replace('B',''))*1000000000
        
    elif lastQTRnetIncome[-1] == 'M':
        netQTR = float(lastQTRnetIncome.replace('M',''))*1000000

    elif lastQTRnetIncome[-2] == 'B':
        netQTR = float(lastQTRnetIncome[1:-2])*1000000000

        
    elif lastQTRnetIncome[-2] == 'M':
        netQTR = float(lastQTRnetIncome[1:-2])*1000000

    else:
        st.write('None')


    if lastYearnetIncome[-1] == 'B':
        netYear = float(lastYearnetIncome.replace('B',''))*1000000000
        
    elif lastYearnetIncome[-1] == 'M':
        netYear = float(lastYearnetIncome.replace('M',''))*1000000

    elif lastYearnetIncome[-2] == 'B':
        netYear = float(lastYearnetIncome[1:-2])*1000000000

    elif lastYearnetIncome[-2] == 'M':
        netYear = float(lastYearnetIncome[1:-2])*1000000
        
    else:
        st.write('None')


    marktetVol = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '?mod=over_search'
    response = requests.get(marktetVol)
    soup = BeautifulSoup(response.text, "lxml")
    todayVol = soup.find_all('li',{'class':'kv__item'})[-1].find('span').text

    if todayVol[-1] == 'M' or todayVol[-1] == 'B':
        tVol = float(todayVol.replace(todayVol[-1],""))*1000000

    else:
        st.write("error") 

    # Number of Analyst Ratings
    # Analyst Price
    # Analyst Buy Rating
    # Analyst Hold Rating
    # Analyst Sell Rating
    analystInfo = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '/analystestimates?mod=mw_quote_tab'
    response = requests.get(analystInfo)
    soup = BeautifulSoup(response.text, "lxml")
    analystRating = int(soup.find_all('td', {'class':"table__cell w25"})[2].text)
    analystPrice = float(soup.find_all('td', {'class':"table__cell w25"})[1].text)
    analystBuy = int(soup.find_all('div', {'class':"bar-chart"})[2].find('span').text)
    analystHold = int(soup.find_all('div', {'class':"bar-chart"})[8].find('span').text)
    analystSell = int(soup.find_all('div', {'class':"bar-chart"})[14].find('span').text)

    # Current Quarter Estimates
    # Year Ago Earnings
    # Last Quarter's Earnings
    currentQTRearnings = float(soup.find_all('td', {'class':"table__cell w25"})[6].text)
    yearAGOearnings = float(soup.find_all('td', {'class':"table__cell w25"})[5].text)
    lastQTRearnings = float(soup.find_all('td', {'class':"table__cell w25"})[4].text)
    currentYEARearnings = float(soup.find_all('td', {'class':"table__cell w25"})[7].text)
    nextFiscalYearEst = float(soup.find_all('td', {'class':"table__cell w25"})[8].text)
    q12022EPSestTrends = (soup.find_all('td', {'class':"table__cell w25"})[46].text).replace("$","")
    q1Trends = float(q12022EPSestTrends.replace("$",""))


    # Performance Rating
    trendsInfo = 'https://www.marketwatch.com/investing/stock/' + str(stock).replace('[',"").replace(']',"").replace("'","") + '?mod=over_search'
    response = requests.get(trendsInfo)
    soup = BeautifulSoup(response.text, "lxml")
    trendLines5D = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find('li').text.replace('%',''))
    trendLines1M = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[1].find('li').text.replace('%',''))
    trendLines3M = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[2].find('li').text.replace('%',''))
    trendLinesYTD = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[3].find('li').text.replace('%','').replace(',',''))
    trendLines1Y = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[4].find('li').text.replace('%','').replace(',',''))

    # EPS
    currentEPS = float(soup.find_all('li', {'class':"kv__item"})[9].find('span').text.replace('$',''))


    # Add the score
    # Project a score for the stock
    # Create a txt file called watchlist
    # Add specific stocks to watchlist
    
    # Print stock info
    st.subheader("**Earnings**")
    st.write("Current earnings projections are " + str(currentQTRearnings))
    st.write("Last quarter earnings projections are " + str(lastQTRearnings))
    st.write("Year ago earnings projections are " + str(yearAGOearnings))
    st.write('')
    st.subheader("**Trends**")
    st.write("5 Days ago " + str(stock) + " has been trending at " + str(trendLines5D) + "%")
    st.write("1 Month ago " + str(stock) + " has been trending at " + str(trendLines1M) + "%")
    st.write("3 Months ago " + str(stock) + " has been trending at " + str(trendLines3M) + "%")

    Stock_points = 0

    # Add the calculations
    # Total Liabilities / Total Assets (Debt Ratio)
    # The lower the better

    # Volume Check
    if tVol > 1000000:
        st.write(str(stock) + " Passed The Volume Test!")
    else:
        st.write("Error")

    # Analyst price is greater than current price
    if analystPrice > price+10:
        Stock_points += 4.5
    elif analystPrice > price+5:
        Stock_points += 2.25
    elif analystPrice > price+2:
        Stock_points += 0
    elif analystPrice > price-2:
        Stock_points += -2.25
    else:
        Stock_points += -4.5

    # Analyst Rating Score
    if analystRating > 10:
        Stock_points += 2.5
    elif analystRating > 5:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Buy Score
    if analystBuy > 59:
        Stock_points += 2.5
    elif analystBuy > 40:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Hold Score
    if analystHold > 59:
        Stock_points += 2.5
    elif analystHold > 40:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Sell Score
    if analystSell > 59:
        Stock_points += -2.5
    elif analystSell > 40:
        Stock_points += -1.25
    else:
        Stock_points += 0

    # Debt Ratio vs Last Quarter Score
    if debtRatio < LQdebtRatio:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Ratio vs Last Year Score
    if debtRatio < LYdebtRatio:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Equity vs Last Quarter Score
    if shareholderEquity < LQshareholderEquity:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Equity vs Last Year Score
    if shareholderEquity < LYshareholderEquity:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income vs Last Quarter Score
    if netIn > netQTR:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income vs Last Year Score
    if netIn > netYear:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income Difference Score
    if netIn > 5000000000:
        Stock_points += 6
    elif netIn > 2500000000:
        Stock_points += 3
    elif netIn > 1000000000:
        Stock_points += 1.5
    elif netIn > 0:
        Stock_points += -1.5
    elif netIn > -1000000000:
        Stock_points += -3
    else:
        Stock_points += -6

    # Trendlines Score 5 Days
    if price > 0:
        if trendLines5D > 10:
            Stock_points += 5.5
        elif trendLines5D > 0:
            Stock_points += 2.75
        elif trendLines5D > -10:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 1 Month
    if price > 0:
        if trendLines1M > 10:
            Stock_points += 5.5
        elif trendLines1M > 0:
            Stock_points += 2.75
        elif trendLines1M > -10:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 5 Days
    if price > 0:
        if trendLines3M > 20:
            Stock_points += 5.5
        elif trendLines3M > 0:
            Stock_points += 2.75
        elif trendLines3M > -20:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score Year To Date
    if price > 0:
        if trendLinesYTD > 40:
            Stock_points += 5.5
        elif trendLinesYTD > 0:
            Stock_points += 2.75
        elif trendLinesYTD > -40:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 1 Year
    if price > 0:
        if trendLines1Y > 49:
            Stock_points += 5.5
        elif trendLines1Y > 0:
            Stock_points += 2.75
        elif trendLines1Y > -51:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0


    # PE Ratio Score
    #if peRatio > 100:
        #Stock_points += 9.375
    #elif peRatio > 50:
        #Stock_points += 6.25
    #elif peRatio > 25:
        #Stock_points += 3.125
    #else:
        #Stock_points += 0


    # Current Earnings vs Last Quarter Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > lastQTRearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Last Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > yearAGOearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Current Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > currentYEARearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Next Fiscal Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > nextFiscalYearEst:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6


    # Current Earnings vs Q1 2022 EPS Est Trends
    if currentQTRearnings > 0: 
        if currentQTRearnings > q1Trends:
            Stock_points += 5.5
        else:
            Stock_points += -5.5
    else:
        Stock_points += -5.5


    if currentEPS > 0:
        Stock_points += 3
    else:
        Stock_points += -3

    if Stock_points > 29:
        Total_Points = Stock_points + 50
    elif Stock_points < 21:
        Total_Points = Stock_points
    else:
        Total_Points = 50

    # What is the play
    if Stock_points < 21:
        st.write('=========================')
        st.write('This Stock Score is ' + str(Total_Points) + '%!')
        st.write("Place a **PUT** option!")
        st.write('=========================')
        #print(stockNews)
        #print(stockNews2)
        #print(stockNews3)
    elif Stock_points > 79:
        st.write('=========================')
        st.write('This Stock Score is ' + str(Total_Points) + '%!')
        st.write('Place a **CALL** option!')
        st.write('=========================')
        #print(stockNews)
        #print(stockNews2)
        #print(stockNews3)
    else:
        st.write('=========================')
        st.write('This Stock Score is only ' + str(Total_Points) + '%!')
        st.write('Do not pick neither one!')
        st.write('=========================')

    #i+=1
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()

    stocks = web.DataReader(stock, 'yahoo', start, end)
    stocks_close = pd.DataFrame(web.DataReader(stock, 'yahoo', start, end)['Close'])

    
    # Visualize Chart
    area_chart = px.area(stocks_close, title = stock + ' SHARE PRICE (2021-2022)')
    fig = go.Figure()
    area_chart.update_xaxes(title_text = 'Date')
    area_chart.update_yaxes(title_text = stock + ' Close Price', tickprefix = '$')
    area_chart.update_layout(showlegend = False)
    area_chart.update_layout(plot_bgcolor = 'black')

    #area_chart.show()
    st.plotly_chart(area_chart)
    #turquoise
    #lightgray
    #





with right_column:
    stock3 = st.text_input("Select a stock: ", value="TSLA")

    st.write("You have selected: " + str(stock3).replace('[',"").replace(']',"").replace("'",""))
    #st.dataframe(data)
    #st.title('Stock Buddy Projection')


    #print("You have selected... " + stock.upper())
    #length = len(stock)
    #i = 0

    #while i < length:
    #print(stock[i])

    #ticker = stock

    # Grab Price
    stockPrice = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '/financials?mod=mw_quote_tab'
    response = requests.get(stockPrice)
    soup = BeautifulSoup(response.text, "lxml")
    price = float(soup.find_all('div', {'class':"intraday__data"})[0].find('bg-quote').text.replace(',',''))


    # Grab Price Change
    #stockRevenue = soup.find_all('td', {'class':"table__cell positive"})[1].text
    # PE Ratio
    #pratio = 'https://www.marketwatch.com/investing/stock/' + stock + '?mod=mw_quote_tab'
    #response = requests.get(pratio)
    #soup = BeautifulSoup(response.text, "lxml")
    #peRatio = float(soup.find_all('li', {'class':"kv__item"})[8].find('span').text)

    #newsData = 'https://www.marketwatch.com/investing/stock/' + stock + '?mod=quote_search'
    #response = requests.get(newsData)
    #soup = BeautifulSoup(response.text, "lxml")
    #stockNews = soup.find_all('h3',{'class':"article__headline"})[0].find('a').text
    #stockNews2 = soup.find_all('h3',{'class':"article__headline"})[1].find('a').text
    #stockNews3 = soup.find_all('h3',{'class':"article__headline"})[2].find('a').text

    # Total Assets
    # Total Assets Growth
    # Total Shareholders' Equity / Total Assets
    balanceSheet = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '/financials/balance-sheet/quarter'
    response = requests.get(balanceSheet)
    soup = BeautifulSoup(response.text, "lxml")
    totalAssets = soup.find_all('div', {'class':"cell__content"})[166].find('span').text
    lastQTRassets = soup.find_all('div', {'class':"cell__content"})[165].find('span').text
    lastYearAssets = soup.find_all('div', {'class':"cell__content"})[162].find('span').text

    assetsGrowth = soup.find_all('div', {'class':"cell__content"})[294].find('span').text
    LQassetsGrowth = soup.find_all('div', {'class':"cell__content"})[293].find('span').text
    shareholderEquity = soup.find_all('div', {'class':"cell__content"})[622].find('span').text.replace('%','')
    LQshareholderEquity = soup.find_all('div', {'class':"cell__content"})[621].find('span').text.replace('%','')
    LYshareholderEquity = soup.find_all('div', {'class':"cell__content"})[618].find('span').text.replace('%','')


    # Total Liabilities
    totalLiability = soup.find_all('div', {'class':"cell__content"})[390].find('span').text
    lastQTRliability = soup.find_all('div', {'class':"cell__content"})[389].find('span').text
    lastYearLiability = soup.find_all('div', {'class':"cell__content"})[386].find('span').text

    if totalAssets[-1] == 'B':
        totA = float(totalAssets.replace('B',''))
    elif totalAssets[-1] == 'M':
        totA = float(totalAssets.replace('M',''))
    else:
        st.write('None')

    if lastQTRassets[-1] == 'B':
        LQtotA = float(lastQTRassets.replace('B',''))
    elif lastQTRassets[-1] == 'M':
        LQtotA = float(lastQTRassets.replace('M',''))
    else:
        st.write('None')

    if lastYearAssets[-1] == 'B':
        LYtotA = float(lastYearAssets.replace('B',''))
    elif lastYearAssets[-1] == 'M':
        LYtotA = float(lastYearAssets.replace('M',''))
    else:
        st.write('None')

    if totalLiability[-1] == 'B':
        totL = float(totalLiability.replace('B',''))
    elif totalLiability[-1] == 'M':
        totL = float(totalLiability.replace('M',''))
    else:
        st.write('None')

    if lastQTRliability[-1] == 'B':
        LQtotL = float(lastQTRliability.replace('B',''))
    elif lastQTRliability[-1] == 'M':
        LQtotL = float(lastQTRliability.replace('M',''))
    else:
        st.write('None')

    if lastYearLiability[-1] == 'B':
        LYtotL = float(lastYearLiability.replace('B',''))
    elif lastYearLiability[-1] == 'M':
        LYtotL = float(lastYearLiability.replace('M',''))
    else:
        st.write('None')


    # Total Liabilities / Total Assets
    debtRatio = totL / totA
    LQdebtRatio = LQtotL / LQtotA
    LYdebtRatio = LYtotL / LYtotA
        

    # Total Revenue - Total Expense
    nincome = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '/financials/income/quarter'
    response = requests.get(nincome)
    soup = BeautifulSoup(response.text, "lxml")
    netIncome = soup.find_all('div', {'class':"cell__content"})[318].find('span').text
    lastQTRnetIncome = soup.find_all('div', {'class':"cell__content"})[317].find('span').text
    lastYearnetIncome = soup.find_all('div', {'class':"cell__content"})[314].find('span').text

    if netIncome[-1] == 'B':
        netIn = float(netIncome.replace('B',''))*1000000000
        
    elif netIncome[-1] == 'M':
        netIn = float(netIncome.replace('M',''))*1000000

    elif netIncome[-2] == 'B':
        netIn = float(netIncome[1:-2])*1000000000
        
    elif netIncome[-2] == 'M':
        netIn = float(netIncome[1:-2])*1000000
        
    else:
        st.write('None')


    if lastQTRnetIncome[-1] == 'B':
        netQTR = float(lastQTRnetIncome.replace('B',''))*1000000000
        
    elif lastQTRnetIncome[-1] == 'M':
        netQTR = float(lastQTRnetIncome.replace('M',''))*1000000

    elif lastQTRnetIncome[-2] == 'B':
        netQTR = float(lastQTRnetIncome[1:-2])*1000000000

        
    elif lastQTRnetIncome[-2] == 'M':
        netQTR = float(lastQTRnetIncome[1:-2])*1000000

    else:
        st.write('None')


    if lastYearnetIncome[-1] == 'B':
        netYear = float(lastYearnetIncome.replace('B',''))*1000000000
        
    elif lastYearnetIncome[-1] == 'M':
        netYear = float(lastYearnetIncome.replace('M',''))*1000000

    elif lastYearnetIncome[-2] == 'B':
        netYear = float(lastYearnetIncome[1:-2])*1000000000

    elif lastYearnetIncome[-2] == 'M':
        netYear = float(lastYearnetIncome[1:-2])*1000000
        
    else:
        st.write('None')


    marktetVol = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '?mod=over_search'
    response = requests.get(marktetVol)
    soup = BeautifulSoup(response.text, "lxml")
    todayVol = soup.find_all('li',{'class':'kv__item'})[-1].find('span').text

    if todayVol[-1] == 'M' or todayVol[-1] == 'B':
        tVol = float(todayVol.replace(todayVol[-1],""))*1000000

    else:
        st.write("error") 

    # Number of Analyst Ratings
    # Analyst Price
    # Analyst Buy Rating
    # Analyst Hold Rating
    # Analyst Sell Rating
    analystInfo = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '/analystestimates?mod=mw_quote_tab'
    response = requests.get(analystInfo)
    soup = BeautifulSoup(response.text, "lxml")
    analystRating = int(soup.find_all('td', {'class':"table__cell w25"})[2].text)
    analystPrice = float(soup.find_all('td', {'class':"table__cell w25"})[1].text)
    analystBuy = int(soup.find_all('div', {'class':"bar-chart"})[2].find('span').text)
    analystHold = int(soup.find_all('div', {'class':"bar-chart"})[8].find('span').text)
    analystSell = int(soup.find_all('div', {'class':"bar-chart"})[14].find('span').text)

    # Current Quarter Estimates
    # Year Ago Earnings
    # Last Quarter's Earnings
    currentQTRearnings = float(soup.find_all('td', {'class':"table__cell w25"})[6].text)
    yearAGOearnings = float(soup.find_all('td', {'class':"table__cell w25"})[5].text)
    lastQTRearnings = float(soup.find_all('td', {'class':"table__cell w25"})[4].text)
    currentYEARearnings = float(soup.find_all('td', {'class':"table__cell w25"})[7].text)
    nextFiscalYearEst = float(soup.find_all('td', {'class':"table__cell w25"})[8].text)
    q12022EPSestTrends = (soup.find_all('td', {'class':"table__cell w25"})[46].text).replace("$","")
    q1Trends = float(q12022EPSestTrends.replace("$",""))


    # Performance Rating
    trendsInfo = 'https://www.marketwatch.com/investing/stock/' + str(stock3).replace('[',"").replace(']',"").replace("'","") + '?mod=over_search'
    response = requests.get(trendsInfo)
    soup = BeautifulSoup(response.text, "lxml")
    trendLines5D = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find('li').text.replace('%',''))
    trendLines1M = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[1].find('li').text.replace('%',''))
    trendLines3M = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[2].find('li').text.replace('%',''))
    trendLinesYTD = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[3].find('li').text.replace('%','').replace(',',''))
    trendLines1Y = float(soup.find_all('table', {'class':"table table--primary no-heading c2"})[0].find_all('tr',{'class':"table__row"})[4].find('li').text.replace('%','').replace(',',''))

    # EPS
    currentEPS = float(soup.find_all('li', {'class':"kv__item"})[9].find('span').text.replace('$',''))


    # Add the score
    # Project a score for the stock
    # Create a txt file called watchlist
    # Add specific stocks to watchlist
    
    
    # Print stock info
    st.subheader("**Earnings**")
    st.write("Current earnings projections are " + str(currentQTRearnings))
    st.write("Last quarter earnings projections are " + str(lastQTRearnings))
    st.write("Year ago earnings projections are " + str(yearAGOearnings))
    st.write('')
    st.subheader("**Trends**")
    st.write("5 Days ago " + str(stock3) + " has been trending at " + str(trendLines5D) + "%")
    st.write("1 Month ago " + str(stock3) + " has been trending at " + str(trendLines1M) + "%")
    st.write("3 Months ago " + str(stock3) + " has been trending at " + str(trendLines3M) + "%")
    

    Stock_points = 0

    # Add the calculations
    # Total Liabilities / Total Assets (Debt Ratio)
    # The lower the better

    # Volume Check
    if tVol > 1000000:
        st.write(str(stock3) + " Passed The Volume Test!")
    else:
        st.write("Error")

    # Analyst price is greater than current price
    if analystPrice > price+10:
        Stock_points += 4.5
    elif analystPrice > price+5:
        Stock_points += 2.25
    elif analystPrice > price+2:
        Stock_points += 0
    elif analystPrice > price-2:
        Stock_points += -2.25
    else:
        Stock_points += -4.5

    # Analyst Rating Score
    if analystRating > 10:
        Stock_points += 2.5
    elif analystRating > 5:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Buy Score
    if analystBuy > 59:
        Stock_points += 2.5
    elif analystBuy > 40:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Hold Score
    if analystHold > 59:
        Stock_points += 2.5
    elif analystHold > 40:
        Stock_points += 1.25
    else:
        Stock_points += 0

    # Analyst Sell Score
    if analystSell > 59:
        Stock_points += -2.5
    elif analystSell > 40:
        Stock_points += -1.25
    else:
        Stock_points += 0

    # Debt Ratio vs Last Quarter Score
    if debtRatio < LQdebtRatio:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Ratio vs Last Year Score
    if debtRatio < LYdebtRatio:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Equity vs Last Quarter Score
    if shareholderEquity < LQshareholderEquity:
        Stock_points += 4
    else:
        Stock_points += -4

    # Debt Equity vs Last Year Score
    if shareholderEquity < LYshareholderEquity:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income vs Last Quarter Score
    if netIn > netQTR:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income vs Last Year Score
    if netIn > netYear:
        Stock_points += 4
    else:
        Stock_points += -4

    # Net Income Difference Score
    if netIn > 5000000000:
        Stock_points += 6
    elif netIn > 2500000000:
        Stock_points += 3
    elif netIn > 1000000000:
        Stock_points += 1.5
    elif netIn > 0:
        Stock_points += -1.5
    elif netIn > -1000000000:
        Stock_points += -3
    else:
        Stock_points += -6

    # Trendlines Score 5 Days
    if price > 0:
        if trendLines5D > 10:
            Stock_points += 5.5
        elif trendLines5D > 0:
            Stock_points += 2.75
        elif trendLines5D > -10:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 1 Month
    if price > 0:
        if trendLines1M > 10:
            Stock_points += 5.5
        elif trendLines1M > 0:
            Stock_points += 2.75
        elif trendLines1M > -10:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 5 Days
    if price > 0:
        if trendLines3M > 20:
            Stock_points += 5.5
        elif trendLines3M > 0:
            Stock_points += 2.75
        elif trendLines3M > -20:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score Year To Date
    if price > 0:
        if trendLinesYTD > 40:
            Stock_points += 5.5
        elif trendLinesYTD > 0:
            Stock_points += 2.75
        elif trendLinesYTD > -40:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0

    # Trendlines Score 1 Year
    if price > 0:
        if trendLines1Y > 49:
            Stock_points += 5.5
        elif trendLines1Y > 0:
            Stock_points += 2.75
        elif trendLines1Y > -51:
            Stock_points += -2.75
        else:
            Stock_points += -5.5
    else:
        Stock_points += 0


    # PE Ratio Score
    #if peRatio > 100:
        #Stock_points += 9.375
    #elif peRatio > 50:
        #Stock_points += 6.25
    #elif peRatio > 25:
        #Stock_points += 3.125
    #else:
        #Stock_points += 0


    # Current Earnings vs Last Quarter Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > lastQTRearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Last Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > yearAGOearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Current Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > currentYEARearnings:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6

    # Current Earnings vs Next Fiscal Year Score
    if currentQTRearnings > 0: 
        if currentQTRearnings > nextFiscalYearEst:
            Stock_points += 6
        else:
            Stock_points += -6
    else:
        Stock_points += -6


    # Current Earnings vs Q1 2022 EPS Est Trends
    if currentQTRearnings > 0: 
        if currentQTRearnings > q1Trends:
            Stock_points += 5.5
        else:
            Stock_points += -5.5
    else:
        Stock_points += -5.5


    if currentEPS > 0:
        Stock_points += 3
    else:
        Stock_points += -3

    if Stock_points > 29:
        Total_Points = Stock_points + 50
    elif Stock_points < 21:
        Total_Points = Stock_points
    else:
        Total_Points = 50

    # What is the play
    if Stock_points < 21:
        st.write('=========================')
        st.write('This Stock Score is ' + str(Total_Points) + '%!')
        st.write("Place a **PUT** option!")
        st.write('=========================')
        #print(stockNews)
        #print(stockNews2)
        #print(stockNews3)
    elif Stock_points > 79:
        st.write('=========================')
        st.write('This Stock Score is ' + str(Total_Points) + '%!')
        st.write('Place a **CALL** option!')
        st.write('=========================')
        #print(stockNews)
        #print(stockNews2)
        #print(stockNews3)
    else:
        st.write('=========================')
        st.write('This Stock Score is only ' + str(Total_Points) + '%!')
        st.write('Do not pick neither one!')
        st.write('=========================')

    #i+=1


    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()

    stocks = web.DataReader(stock3, 'yahoo', start, end)
    stocks_close = pd.DataFrame(web.DataReader(stock3, 'yahoo', start, end)['Close'])

    # Visualize Chart
    area_chart = px.area(stocks_close, title = stock3 + ' SHARE PRICE (2021-2022)')
    area_chart.update_xaxes(title_text = 'Date')
    area_chart.update_yaxes(title_text = stock3 + ' Close Price', tickprefix = '$')
    area_chart.update_layout(showlegend = False)
    area_chart.update_layout(plot_bgcolor = 'black')

    #area_chart.show()
    st.plotly_chart(area_chart)
    

