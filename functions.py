### Libraries & Setup

import pandas as pd   # Data manipulation and analysis
import numpy as np    # Scientific Computing

import matplotlib.pyplot as plt   # Visualization

import warnings
warnings.filterwarnings('ignore')

###[1.1]

def distribution_summary_hist(variable, data_to_plot , nbins):

    '''
    Plot histogram and summary statistic table of the input variable
    '''

    plt.rcParams["figure.figsize"] = [10, 3]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.hist(data_to_plot, bins = nbins)
    try:
        df = pd.DataFrame(variable.describe().apply(lambda x: format(x, 'f')).values.astype(float).astype(int), variable.describe().apply(lambda x: format(x, 'f')).index , columns = ["Summary Statistics"])
    except ValueError:
        df = pd.DataFrame(variable.describe().apply(lambda x: format(x, 'f')).values, variable.describe().apply(lambda x: format(x, 'f')).index , columns = ["Summary Statistics"])
    ax2 = fig.add_subplot(122)
    font_size = 14
    bbox = [0, 0, 1, 1]
    ax2.axis('off')
    mpl_table = ax2.table(cellText=df.values, rowLabels=df.index, bbox=bbox, colLabels=df.columns ,rowColours= ["lightsteelblue"]*8, colColours= ["lightsteelblue"],loc='right')

    return

def pie_chart(values , labels, title):

    '''
    Plot pie and summary statistic table of the input categorical variable
    '''

    explode = (0, 0.2)
    fig1, ax1 = plt.subplots()
    _, _, autopcts  = ax1.pie(values, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90,textprops={'fontsize': 16,'color':"w"})
    plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':15})
    ax1.set_title(title,fontsize = 16) , ax1.axis('equal')
    plt.legend(labels, loc="upper left")

    return

###[1.2]

def plot_jaccard(similar_items, shingle_sets, jaccard_similarity):

    '''
    Plot distribution of Jaccard Similarity values between customers in the same bucket
    '''

    # Initialize count dictionary
    count = {x: 0 for x in [0, 0.2, 0.5, 1]}

    # Count the appearance of each unique value of Jaccard similarity between customers in the same bucket
    for custID, values in similar_items.items():
        for el in values:
            if custID!=el:
                sim = jaccard_similarity(shingle_sets[custID], shingle_sets[el])
                count[sim]+=1/2

    # Plot
    f = plt.figure()
    plt.xticks(range(4), ["0", "0.2", "0.5", "1"])
    plt.ylabel("Count", fontsize=14, labelpad=20)
    plt.xlabel("Jaccard Similarity", fontsize=14, labelpad=20)
    plt.title("Distribution of Jaccard Similarity values", fontsize=18, pad=15)
    plt.bar([y for y in range(4)], [x[1] for x in sorted(count.items())], width=0.8, color=['black', 'red', 'yellow', 'green'], ec="k")
    f.set_figwidth(14)
    f.set_figheight(8)

    return count

def s_curve(b, r):

    '''
    Plot the S-curve for the input b and r values
    '''

    # Plot
    f = plt.figure()
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.ylabel("Probability of becoming\n a candidate pair", fontsize=14, labelpad=20)
    plt.xlabel("Jaccard Similarity", fontsize=14, labelpad=20)
    plt.title("S-curve with b={} and r={} (t ≈ {})".format(b,r, round((1/b)**(1/r),2)), fontsize=18, pad=15)
    plt.plot([x for x in np.arange(0, 1.1, 0.1)], [1-(1-x**r)**b for x in np.arange(0, 1.1, 0.1)])
    plt.axvline(x=0.2, color='r', ls="--")
    plt.axvline(x=0.5, color='r', ls="--")
    f.set_figwidth(14)
    f.set_figheight(8)

    return

###[1.3]

def plot_query(result):

    '''
    Plot distribution of Jaccard Similarity values in query result
    '''

    sims = []

    # Count the appearance of each unique value of Jaccard similarity for each selected pair
    for custID, values in result.items():
        one = 0
        half = 0
        for el in values:
            if el[0]==1: one+=1
            if el[0]==0.5: half+=1
        sims.append((one, half))

    # Plot
    f = plt.figure()
    X_axis = np.arange(len(result))*1.5
    plt.xticks(X_axis, ["Q{}".format(i+1) for i in range(len(result))], rotation = 45)
    plt.yticks([y for y in range(0, len(list(result.values())[0])+1, 5)])
    plt.ylabel("Count", fontsize=14, labelpad=20)
    plt.xlabel("Query", fontsize=14, labelpad=20)
    plt.ylim(0, len(list(result.values())[0])*1.3)
    plt.title("Distribution of Jaccard Similarity values in query result", fontsize=18, pad=15)
    plt.bar(X_axis-0.25, [x[1] for x in sims], width=0.5, color=["yellow"], ec="k", label = "Jaccard Similarity = 0.5")
    plt.bar(X_axis+0.25, [x[0] for x in sims], width=0.5, color=["green"], ec="k", label = "Jaccard Similarity = 1")
    plt.legend()
    f.set_figwidth(20)
    f.set_figheight(4)

    return

###[2.1]

def age_intervals(data, intervals):
    age_intervals = []
    for i in data:
        if i < 23:
            age_intervals.append(intervals[0])
        elif i >22 and i <26:
            age_intervals.append(intervals[1])
        elif i >25 and i <30:
            age_intervals.append(intervals[2])
        elif i >29 and i <36:
            age_intervals.append(intervals[3])
        elif i >35 and i <46:
            age_intervals.append(intervals[4])
        elif i >45:
            age_intervals.append(intervals[5])
    return age_intervals

def quantiles(variable):
    q1 = variable.describe().astype(int).values[4]
    q2 = variable.describe().astype(int).values[5]
    q3 = variable.describe().astype(int).values[6]
    quartiles = []
    for i in variable:
        if i <= q1:
            quartiles.append("Q1")
        elif i >q1 and i <= q2:
            quartiles.append("Q2")
        elif i >q2 and i <= q3:
            quartiles.append("Q3")
        elif i > q3:
            quartiles.append("Q4")
    return quartiles

###[2.2]

def age_int(x):
    if x <= 22:
        return 0
    if 23 <= x <= 25:
        return 1
    if 26 <= x <= 29:
        return 2
    if 30 <= x <= 35:
        return 3
    if 36 <= x <= 45:
        return 4
    if x >= 46:
        return 5


def transaction_int(x):
    if x <= 160:
        return 0
    if 160 < x <= 450:
        return 1
    if 450 < x <= 1200:
        return 2
    if 1200 < x <= 5000:
        return 3
    if 5000 < x <= 20000:
        return 4
    if x > 20000:
        return 5


def balance_int(x):
    if x <= 1000:
        return 0
    if 1000 < x <= 5000:
        return 1
    if 5000 < x <= 10000:
        return 2
    if 10000 < x <= 15000:
        return 3
    if 15000 < x <= 25000:
        return 4
    if 25000 < x <= 35000:
        return 5
    if 35000 < x <= 50000:
        return 6
    if 50000 < x <= 100000:
        return 7
    if 100000 < x <= 250000:
        return 8
    if 250000 < x <= 500000:
        return 9
    if 500000 < x <= 1000000:
        return 10
    if 1000000 < x <= 5000000:
        return 11
    if 5000000 < x <= 10000000:
        return 12
    if x > 10000000:
        return 13


def scree_plot(per_var, cum_sum_exp):
    labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]
    plt.rcParams["figure.figsize"] = [15, 6]
    plt.plot([8, 8], [100, 0], linestyle='--', color='red')
    plt.plot([0, 8], [73, 73], linestyle='--', color='red')
    plt.step(range(0, len(cum_sum_exp)), cum_sum_exp, where='post', label='Cumulative explained variance')
    plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels, label='Individual explained variance')
    plt.yticks(cum_sum_exp[0:10])
    plt.legend(loc='best')
    plt.ylabel('Percentage of Explained Variance', {'color': 'black', 'weight': 'bold', 'fontsize': 15})
    plt.xlabel('Principal Components', {'color': 'black', 'weight': 'bold', 'fontsize': 15})
    plt.title('Scree Plot', {'color': 'black', 'weight': 'bold', 'fontsize': 15})

    return

###[2.3.2]

def elbow_method(inertia_values, max_clusters):

    '''
    Plot clustering inertia vs number of clusters K
    '''

    # Plot
    f = plt.figure()
    plt.xticks(range(1, max_clusters+1))
    plt.ylabel("Inertia / Sum of squared distances", fontsize=14, labelpad=20)
    plt.xlabel("K", fontsize=14, labelpad=20)
    plt.title("Elbow method for optimal number of clusters", fontsize=18, pad=15)
    plt.plot([x for x in range(1, max_clusters+1)], inertia_values, '--bo')
    f.set_figwidth(14)
    f.set_figheight(8)

    return

def silhouette_analysis(silhouette_values, max_clusters):

    '''
    Plot clustering silhouette score vs number of clusters K
    '''

    # Plot
    f = plt.figure()
    plt.xticks(range(1, max_clusters+1))
    plt.ylabel("Silhouette Coefficient", fontsize=14, labelpad=20)
    plt.xlabel("K", fontsize=14, labelpad=20)
    plt.title("Silhouette analysis for optimal number of clusters", fontsize=18, pad=15)
    plt.plot([x for x in range(1, max_clusters+1)], silhouette_values, '--go')
    f.set_figwidth(14)
    f.set_figheight(8)

    return