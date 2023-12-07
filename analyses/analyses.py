import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image #lib pillow --> installation: https://pillow.readthedocs.io/en/latest/installation.html#basic-installation



def prepare_data():
    #importing JSON
    pd_object = pd.read_json("tensionterminator/analyses/data.json")
    df = pd.DataFrame(pd_object)

    #converting string to datetime datatype
    df["starttime"] = pd.to_datetime(df["starttime"])
    df["endtime"] = pd.to_datetime(df["endtime"])

    #time spent on tension terminator (in minutes)
    df['time_spent'] = (df["endtime"] - df["starttime"]) / pd.Timedelta(minutes=1)
    df['day'] = df["starttime"].dt.date #date of usage
    
    return df

def tool_usage_pieplot(df):
    #counting unique entries
    unique, counts = np.unique(df, return_counts=True)
    label_tool = 'DuoBalls', 'Trigger'

    fig, ax = plt.subplots(figsize=(8, 5))
    
    #calculating percentages for pie diagram
    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%"        #f"{absolute:d}"

    wedges, texts, autotexts = ax.pie(counts, autopct=lambda pct: func(pct, counts),
                                  textprops=dict(color="w"))
    ax.legend(wedges, label_tool, 
                title="tool usage", 
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.setp(autotexts, size=8, weight="bold")
    plt.title("distribution of tools used")
    plt.savefig('tensionterminator/analyses/tool_distribution.png')
        
    
    return

def time_spent_boxplot(df):    
    fig, ax = plt.subplots(figsize=(8, 5))

    #legend with min, mean, max values:
    props = dict(boxstyle='square', facecolor='wheat', alpha=0.5)
    min = df.min()
    max = df.max()
    mean = df.mean()
    textstr = '\n'.join((
        r'time spent in minutes:',
        r'$min=%.2f$' % (min, ),
        r'$mean=%.2f$' % (mean, ),
        r'$max=%.2f$' % (max, )))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    
    plt.boxplot(df, vert=False)
    plt.title("Time Spent")
    plt.xlabel("time(m)")
    plt.yticks([]) #to hide y-axis label
    plt.savefig("tensionterminator/analyses/time_spent.png")
    
    return
    


df = prepare_data()
#creating diagramms
tool_usage_pieplot(df[["tool"]])
time_spent_boxplot(df[["time_spent"]])


im1 = Image.open("tensionterminator/analyses/time_spent.png")
im2 = Image.open("tensionterminator/analyses/tool_distribution.png")

#array for future diagramms
images = [im2]
#saving all images in one PDF
im1.save("tensionterminator/analyses/diagrams.pdf", save_all=True, append_images=images)





