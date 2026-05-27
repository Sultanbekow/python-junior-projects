import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

print("📊 Data Pipeline - CSV zu SQLite mit Bereinigung")

# 1. Generiere Beispieldaten
data = {
    'date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(100)],
    'sales': [random.randint(50, 500) for _ in range(100)],
    'category': random.choices(['A', 'B', 'C'], k=100),
    'invalid_col': [None if random.random() > 0.95 else x for x in range(100)]
}
df = pd.DataFrame(data)

# 2. Bereinigung
df.dropna(inplace=True)
df.drop('invalid_col', axis=1, inplace=True)
df['sales'] = df['sales'].astype(int)

print(f"✅ Bereinigt: {len(df)} Zeilen")

# 3. In SQLite speichern
conn = sqlite3.connect('sales.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()

print("💾 Gespeichert in sales.db")

# 4. Analyse
conn = sqlite3.connect('sales.db')
result = pd.read_sql("SELECT category, AVG(sales) as avg_sales FROM sales GROUP BY category", conn)
print("\n📈 Durchschnittsumsatz pro Kategorie:")
print(result)
conn.close()
