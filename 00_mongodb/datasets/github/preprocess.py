
import pandas as pd

df = pd.read_csv('github_dataset.csv')
df_repo = df['repositories'].str.split('/', expand=True).rename(columns={0: 'user_name', 1: 'repo_name'})
df = pd.concat([df_repo, df], axis=1)
df.drop(columns=['repositories'], inplace=True)
df.to_csv('github.csv', index=False)