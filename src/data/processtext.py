import pandas as pd
import click

stop_words = ['Vote', 'Country', 'Name', 'First (5 points)', 'Second (3 points)', 'Third (1 point)']

def get_values_for(f, curr_word):
    processing_active = False
    for line in f:
        line = line.strip()
        if line.startswith(curr_word):
            processing_active = True
            continue

        if line=='':            
            processing_active = False
            continue
        
        if '/' in line:
            continue

        if processing_active:
            yield line
        
def file_to_data(fname):
    f = open(fname, 'r')

    data = dict()
    for word in stop_words:
        f.seek(0)
        data[word] = list(get_values_for(f, word))
    f.close()

    for k, v in data.items():
        print('{} --> {}'.format(k, len(v)))
    
    return data

def add_regions(df):
    url2 = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv'

    country_region = pd.read_csv(url2)
    country_region = country_region[['name', 'region', 'sub-region']]
    country_region.rename(columns={'name':'Country', 'region':'Region', 'sub-region': 'Sub-Region'}, inplace=True)
    country_region.set_index('Country', inplace=True)

    df_extend = df.join(country_region, on='Country', how='left')
    return df_extend

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def main(input_file, output_file):
    print('Processing {}  ==> {}'.format(input_file, output_file))

    data = file_to_data(fname=input_file)
    
    df = pd.DataFrame.from_dict(data, orient='columns')
    df.rename(columns={'First (5 points)': 'First', 'Second (3 points)': 'Second', 'Third (1 point)': 'Third'}, inplace=True)

    df =df[['Vote', 'Country', 'Name', 'First', 'Second', 'Third']]
    df.Vote.value_counts()

    df = add_regions(df)

    df.to_csv(output_file)

if __name__=="__main__":
    main()