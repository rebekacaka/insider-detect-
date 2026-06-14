-Insider Trading Detection System 
## Stock Market Basics: 

*Ticker - A short code that identifies a company on the stock market 
*Price- How much one share of a company costs at a given moment 
*Volume- How many shares of a company were traded in a single day. A sudden spike in volume before a major announcement is one of the core signals I will detect.
*Share- A single unit of ownership in a company. If Apple has 1 billion shares, and you own 1 then you own one billions of Apple 

## Regulatory Framework

A Form 4 is a document that insiders (CEOs, board members, and major shareholders) are legally required to file with the SEC withing 2 days of bying or selling shares in their own company. This provides SEC with the information about who traded, which comapny, how many shares and at what price and whether they bought or sold and the specific date. 

## Core Detection Signals for Insider Trading
First, normal volume is how many shares a stock trades on a typical day.BIg companies normally have a consister trading number of shares. A volume spike is when that number suddenly jumps way above normal. So something way above the consistent number.   
If someone who has insider information knows the company will announce smth huge- record profits etc- they will buy as many shares as possible before the announcment. That buing creates a volume spike. The announcement happens, the price jumps, they sell and make a fortune.The timing window is the key. We look at the 7, 14, and 30 days before any major announcement. If volume spiked during that window with no public explanation, that's a red flag.

## Standard Deviation

A Z-score shows how abnormal something is compared to its history. A statistical measure used to quantify how many standard deviations a stock's sudden trading volume spike is from its historical daily average, where a threshold of 2.5 or higher indicates a mathematically rare anomaly that triggers an automated flag for potential insider trading.