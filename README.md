# WR_Rating

## Overview

**WR_Rating** is a project that collects and stores corporate credit rating data from multiple rating agencies in South Korea.  
It gathers credit ratings from sources such as **Korea Investors Service (KIS)**, **Korea Ratings (KR)**, and **NICE Investors Service**, then stores the data in a database for further analysis.

## Key Features

- Scrapes credit rating data from KIS, KR, and NICE.
- Utilizes **BeautifulSoup** and **Selenium** for web scraping.
- Processes the data in a structured format and stores it in an **MSSQL Server** database.
- Implements parallel processing to improve data collection efficiency.
