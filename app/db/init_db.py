from session import init_db

print("Creating tables in Azure SQL Database...")
init_db()
print("Tables created successfully!")

if __name__=="__main":
    init_db()