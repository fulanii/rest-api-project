

from flask_package import app
from flask_package import postgres_package
from flask_package import scraper_package




if __name__ == "__main__":
    postgres_package.MyDb.create_table()
    postgres_package.MyDb.insert_table(table_name="countries_info", values=scraper_package.country_info())
    app.run(debug=True)