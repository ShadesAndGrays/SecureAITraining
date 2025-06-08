import numpy as np
import pandas as pd

def main():
  print("Hello world")
  df = pd.read_csv('data/personality_dataset.csv')
  df = df.dropna()
  print(df.info())

  splits = np.array_split(df,10)
  for i,part in enumerate(splits):
    print(f"Part {i+1} size: {len(part)}")

  for i,part in enumerate(splits):
    part.to_csv(f'data/personality_dataset_part_{i+1}.csv',index=False)
  


if __name__ == "__main__":
  main()