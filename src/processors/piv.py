import pandas as pd

# pivoting the table to get summaries by player
def pivot_it(df):
    nf = pd.DataFrame(df.First.value_counts())
    nf2 = pd.DataFrame(df.Second.value_counts())
    nf3 = pd.DataFrame(df.Third.value_counts())

    res = nf.join((nf2.join(nf3, how='outer')), how='outer')
    # for some reason some columns are float and not int
    res.fillna(0.0, inplace=True)
    return res.astype(int)

def add_points(df):
    # calculate number of votes and points according to FIFA rules (first == 5 pts, second = 3 pts, third = 1pt)
    res = df.copy()
    res['Occurances'] = df.First + df.Second + df.Third
    res['Points'] = df.First * 5 + df.Second * 3 + df.Third
    all_points = res.Points.sum()
    res['RelativePoints'] = res['Points'] / all_points
    return res

def get_results_for(df):
    return add_points(pivot_it(df))
