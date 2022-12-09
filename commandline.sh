#!/bin/bash

#-------------------First Question-----------------------
#select location column, then sort and count number of occurrences of each location, then sort again to obtain
#sorted list of most populare places

echo 'The location with the greatest number of transactions is:'
cut -d, -f5 bank_transactions.csv | sort | uniq -c | sort -nr | head -n 1

#-------------------Second Question----------------------
#select CustomerGender and Transaction Amount columns. Then select the rows that contain 'M', fianlly calculate sum and average of transactions. Finally repeat for the Females.

echo 'Total and Average Expenditure for Males:'
cut -d, -f4,9 bank_transactions.csv | grep 'M' | awk -F',' '{sum+=$2;}END{printf "%.0f %.1f\n", sum, (sum/NR);}'
echo 'Total and Average Expenditure for Females:'
cut -d, -f4,9 bank_transactions.csv | grep 'F' | awk -F',' '{sum+=$2;}END{printf "%.0f %.1f\n", sum, (sum/NR);}'


#------------------Third Question----------------------- 
#select CustomerID and TransactionAmount columns; sort them according to CustomerID; compute average transaction for each customer with awk; 
#finally sort the output according to the average transaction; select only the last row. 

echo 'The Customer with the highest average transaction, with his relative average, is:'
cut -d, -f2,9 bank_transactions.csv | sort -k1 | awk -F, '{sum[$1]+=$2; count[$1]++;}END{for(k in sum) printf "%s %.1f\n",  k, sum[k]/count[k]}' | sort -t$' ' -k2 -n | tail -1



