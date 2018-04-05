import json

import pandas as pd

def convert_to_df_with_github_url():
    """Converts the raw metadata JSON files to a pandas dataframe containing the metadata
    from the 'info' dict in the JSON, and adds a Github URL if found anywhere in the JSON"""
    files = os.listdir('all_metadata')

    s = []

    for filename in tqdm(files):
        # Read JSON file for package
        with open('all_metadata/' + filename) as f:
            json_string = f.read()
        # Search in the string for a github URL
        regex_result = re.search('github.com/([^\s;\(){}#]+?/[^\s`_.;\'\\\[\]\{\\}/\","><#!$\%&*)(]+)', json_string)
        # Try loading the JSON and skip if it fails
        try:
            j = json.loads(json_string)
        except:
            continue
        # Convert to a pandas Series
        json_series = pd.io.json.json_normalize(j['info'])
        # Add the github URL if one was found
        if regex_result:
            json_series['github_url'] = regex_result.group(1)
        
        # Add to a list
        s.append(json_series)

    # Concatenate the list of Series to create a DataFrame
    df = pd.concat(s)

    # Because of how we created the data frame, all entries have an index of 0, reset this to a standard
    # integer increasing index
    df.reset_index(drop=True)

    return df

def replace_UNKNOWN_and_blank(df, column):
    df.loc[df[column] == 'UNKNOWN', column] = ""
    df[column] = df[column].fillna("")

    return df

def preprocess_df(df):
    df = replace_UNKNOWN_and_blank(df, 'author')
    df = replace_UNKNOWN_and_blank(df, 'author_email')
    df = replace_UNKNOWN_and_blank(df, 'bugtrack_url')

    # Take the list of classifiers and convert it to a newline-separated string
    df['classifiers'] = df['classifiers'].apply(lambda x: "\n".join(x))

    df = replace_UNKNOWN_and_blank(df, 'description')
    df = replace_UNKNOWN_and_blank(df, 'docs_url')
    df = replace_UNKNOWN_and_blank(df, 'download_url')

    # Remove three columns that are always set to -1
    df = df.drop(['downloads.last_day', 'downloads.last_week', 'downloads.last_month'], axis=1)

    df = replace_UNKNOWN_and_blank(df, 'home_page')
    df = replace_UNKNOWN_and_blank(df, 'keywords')
    df = replace_UNKNOWN_and_blank(df, 'license')
    df = replace_UNKNOWN_and_blank(df, 'maintainer')
    df = replace_UNKNOWN_and_blank(df, 'maintainer_email')
    df = replace_UNKNOWN_and_blank(df, 'platform')
    df = replace_UNKNOWN_and_blank(df, 'project_url')
    df = replace_UNKNOWN_and_blank(df, 'release_url')

    # Take the list of requirements and convert to a newline separated string
    df['requires_dist'] = df['requires_dist'].fillna('')
    df['requires_dist'] = df['requires_dist'].apply(lambda x: "\n".join(x))

    df = replace_UNKNOWN_and_blank(df, 'requires_python')
    df = replace_UNKNOWN_and_blank(df, 'summary')
    df = replace_UNKNOWN_and_blank(df, 'version')

    return df

