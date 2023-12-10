def pre_process(df):
    types = {x: i for i, x in enumerate(sorted(list(set(list(df['type'])))))}
    families = {x: i for i, x in enumerate(sorted(list(set(list(df['family'])))))}

    df['malicious'] = df['type'].apply(lambda x: 0 if types[x] == 3 else 1)
    df['type'] = df['type'].apply(lambda x: types[x])
    df['family'] = df['family'].apply(lambda x: families[x])
    categorization_columns = ['malicious', 'type', 'family']
    metadata_columns = list(set(df.columns) - set(df.select_dtypes(include='number').columns))
    metadata_columns = [x for x in metadata_columns if x not in categorization_columns]
    df.drop([col for col in df.columns if col in metadata_columns], axis=1, inplace=True)
    df_features = df.drop([col for col in df.columns if col in categorization_columns], axis=1)
    df_categories = df[categorization_columns]
    print("Found the following types: ")
    for k, v in types.items():
        print(f"\t- {k}: {v}")
    print("Found the following families: ")
    for k, v in families.items():
        print(f"\t- {k}: {v}")
    return df, df_features, df_categories, types, families
