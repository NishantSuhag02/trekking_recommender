import pandas as pd

class TrekRecommender:

    def __init__(self, db_path):
        import sqlite3
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def load_data(self):
        return pd.read_sql_query("SELECT * FROM Treks", self.conn)
    
    def filter_treks(self,df,month,difficulty,max_days,budget):
        df = df.copy()

        df = df[df['difficulty'] == difficulty]
        df = df[df['duration_days'] <= max_days]
        df = df[df['estimated_cost_inr'] <= budget]
        df = df[df['best_months'].str.contains(month, case=False)]


        return df
    
    def rank_treks(self,df):
        df = df.copy()

        df['score'] = (
            df['rating']*2 +
            (10000 / df['estimated_cost_inr']) +
            (6 / df['duration_days'])
        )

        return df.sort_values(by='score', ascending=False)
    
    def recommend(self,month,difficulty,max_days,budget):
        df = self.load_data()

        filtered = self.filter_treks(self,df,month,difficulty,max_days,budget)

        if filtered.empty:
            return []
        
        ranked = self.rank_treks(filtered)

        return ranked.head(5).to_dict(orient='records')
        