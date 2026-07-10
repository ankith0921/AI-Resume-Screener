def get_candidate(df, name):
    return df[df["Candidate"] == name].iloc[0]