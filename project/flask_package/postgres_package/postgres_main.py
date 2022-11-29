

import psycopg2 as pg2
from flask_package import scraper_package

class MyDb:
    def __init__(self):
        self.conn = pg2.connect(database='scraper_db', user='daboii',password='123456')
        self.cur = self.conn.cursor()

    def query_table(self, table_name:str, num_row:int = 0 ):
        """This method query all the rows of any table from the scraper_db database.

        :param `db_name` Set the table name you want to query from in the `scraper_db` (require)
        :param `num_row` Set to number of rows you want back, (optional) if not set will return all  """

        try:
            self.cur.execute(f"SELECT * FROM {table_name};")
            if num_row == 0:
                data = self.cur.fetchall()
            else:
                data = self.cur.fetchmany(num_row)
                self.conn.close()
            return data
        except:
            return "Something went wrong"

    def insert_table(self, table_name:str, **values:str):
        """Insert into a table that's in the `scraper_db` database"""

        for i in values:
            query = f'''INSERT INTO {table_name}(country_name, country_capitals, country_population, country_area) VALUES {values[i]};'''

            self.cur.execute(query)
            self.conn.commit()

            print(f"{values[i]} Inserted ")

    def create_table(self):
        """Creates table for `scraper_db` db  """
        try: 
            query = """ 
            CREATE TABLE IF NOT EXISTS countries_info(
                id SERIAL PRIMARY KEY,
                country_name VARCHAR(50) UNIQUE NOT NULL,
                country_capitals VARCHAR(50) NOT NULL,
                country_population BIGINT NOT NULL,
                country_area DECIMAL NOT NULL,
                country_code SMALLINT ,
                iso_code VARCHAR(8)
                )
            """
            self.cur.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)

    def execute_query(self, query:str) -> bool:

        try:
            self.cur.execute(query)
            self.conn.commit()
            return "done"
        except Exception as error:
            return error

    def return_data_dict(self, table_name:str = "countries_info", num_rows:int = 0) -> list:
        """Returns a list of countries as a dictionary, use `num_rows` to set how many result back """

        try: 
            query = f"""SELECT * FROM {table_name} ORDER BY id ASC;"""
            if num_rows == 0:
                
                self.cur.execute(query)
                data = self.cur.fetchall()
            else:
                self.cur.execute(query)
                data = self.cur.fetchmany(num_rows)
        except:
            return "Something went wrong"

        list_countries = []
        for i in range(0, len(data)):
            my_dict = {
                "id": data[i][0],
                "country_name": data[i][1],
                "country_capital": data[i][2],
                "contry_population": data[i][3],
                "country_area": float(data[i][4]),
                "country_code": data[i][5],
                "iso_code": data[i][6]
                }
            list_countries.append(my_dict)
        
        return list_countries

    def get_by_name(self, name:str, table_name:str = "countries_info") -> list:
        query = f"""SELECT * FROM countries_info WHERE country_name = '{name.title()}'; """
        self.cur.execute(query)
        try:        
            data = self.cur.fetchall()
        except:
            return "Something went wrong"
        
        list_countries = []
        for i in range(0, len(data)):
            my_dict = {
                "id": data[i][0],
                "country_name": data[i][1],
                "country_capital": data[i][2],
                "contry_population": data[i][3],
                "country_area": float(data[i][4]),
                "country_code": data[i][5],
                "iso_code": data[i][6]
                }
            list_countries.append(my_dict)
        return list_countries
            
    def create_add_db(self) -> list:
        """Created the countries_info tbale and added all the countrie and their info"""
        self.create_table()

        scrape = scraper_package.Scaper()
        info = scrape.country_info()

        names = info["names"]
        capitals = [ i.replace("'", "") for i in info["capitals"] ]
        populations = info["populations"]
        areas = info["areas"]

        for i in zip(names, capitals, populations, areas):
            self.insert_table(table_name='countries_info', values=i)
    
    def adding_country_code_db(self, country_name:str, country_code:int) -> dict:
        """This method adds the country code to the database"""
        # TODO 1 format country name, check if country name exist in db, return error to client if not
        # TODO 2 check if country code alredy exist
        # TODO 3 if not add country code
        # TODO 4 return final result w country code included as dict 

        query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data != None:
            if data[5] == None:
                query = f""" UPDATE countries_info SET country_code = {country_code} WHERE country_name = '{country_name.title()}'; """
                self.cur.execute(query)
                self.conn.commit()

                query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
                self.cur.execute(query)
                data = self.cur.fetchone()

                my_dict = ["success", {
                        "id": data[0],
                        "country_name": data[1],
                        "country_capital": data[2],
                        "contry_population": data[3],
                        "country_area": float(data[4]),
                        "country_code": data[5],
                        "iso_code": data[6]
                    }
                ]
                return my_dict
            else:
                query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
                self.cur.execute(query)
                data = self.cur.fetchone()

                my_dict = ["Country code already filled", {
                        "id": data[0],
                        "country_name": data[1],
                        "country_capital": data[2],
                        "contry_population": data[3],
                        "country_area": float(data[4]),
                        "country_code": data[5],
                        "iso_code": data[6]
                    }
                ]
                return my_dict                
        else:
            return "Country doesnt exist, or got entered wrong"

    def adding_iso_code(self, country_name:str, iso_code:str):
        """This method adds the iso code for a country to the database"""
        query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data != None:
            if data[6] == None:
                query = f""" UPDATE countries_info SET iso_code = '{iso_code}' WHERE country_name = '{country_name.title()}'; """
                self.cur.execute(query)
                self.conn.commit()

                query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
                self.cur.execute(query)
                data = self.cur.fetchone()

                my_dict = ["success", {
                        "id": data[0],
                        "country_name": data[1],
                        "country_capital": data[2],
                        "contry_population": data[3],
                        "country_area": float(data[4]),
                        "country_code": data[5],
                        "iso_code": data[6]
                    }
                ]
                return my_dict
            else:
                query = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """ 
                self.cur.execute(query)
                data = self.cur.fetchone()

                my_dict = ["Country iso code already filled", {
                        "id": data[0],
                        "country_name": data[1],
                        "country_capital": data[2],
                        "contry_population": data[3],
                        "country_area": float(data[4]),
                        "country_code": data[5],
                        "iso_code": data[6]
                    }
                ]
                return my_dict                
        else:
            return "Country doesnt exist, or got entered wrong"
        
    def create_fun_fact_table(self):
        """creates fun fact table for all the countries"""
        query = """
        CREATE TABLE fun_fact(
            post_id SERIAL PRIMARY KEY,
            fun_fact_post VARCHAR(250) 
            country_id INTEGER REFERENCES countries_info(id)
            );
        """
    
    def add_fun_fact(self, country_name:str, fun_fact:str):
        query  = f""" SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """
        self.cur.execute(query)
        data = self.cur.fetchone()  

        if data != None:
            country_id = data[0]
            funfact = f"""SELECT * FROM fun_fact WHERE country_id = {country_id};"""
            self.cur.execute(funfact)
            funfact_country = self.cur.fetchone()

            if funfact_country == None:
                if len(fun_fact) < 250:
                    adding_funfact = f"""INSERT INTO fun_fact(fun_fact_post, country_id) VALUES ('{fun_fact}', {country_id})
                    """
                    try:
                        self.cur.execute(adding_funfact)
                        self.conn.commit()
                    except Exception as error:
                        self.conn.rollback()
                        return f"Something went wrong {error}"


                    info = f"""SELECT * FROM countries_info WHERE id = '{country_id}'"""
                    fun_info = f"""SELECT * FROM fun_fact WHERE country_id = '{country_id}'  """

                    self.cur.execute(info)
                    info_data = self.cur.fetchone()

                    self.cur.execute(fun_info)
                    fun_info = self.cur.fetchone()

                    to_return = [
                        "Success",
                        {
                            "id": info_data[0],
                            "country_name": info_data[1],
                            "country_capital": info_data[2],
                            "country_population": info_data[3],
                            "country_area": float(info_data[4]),
                            "country_code": info_data[5],
                            "iso_code": info_data[6],
                            "fun_fact": fun_info[1]

                        }
                    ]
                    return to_return
                else:
                    return "fun fact length needs to be under 250 character"
            else:
                info = [
                    "Country already has a funfact",
                    {
                        "id": data[0],
                        "country_name": data[1],
                        "country_capital": data[2],
                        "country_population": data[3],
                        "country_area": float(data[4]),
                        "country_code": data[5],
                        "iso_code": data[6],
                        "fun_fact": funfact_country[1]

                    }
                ]
                return info
        else:
            return "Country doesn't exist or country name is incorrect."

    def edit_fun_fact(self, country_name:str, new_fact:str):
        check_country = f"""SELECT * FROM countries_info WHERE country_name = '{country_name.title()}'; """
        self.cur.execute(check_country)
        result = self.cur.fetchone() 

        if result != None:
            country_id = result[0]
            get_country_funfact = f"""SELECT * FROM fun_fact WHERE country_id = {country_id}"""

            self.cur.execute(get_country_funfact)
            funfact = self.cur.fetchone() 
            if funfact == None:
                return f"{country_name} doesn't have a funfact, try adding one with a POST request"
            else:
                update_funfact = f"""UPDATE fun_fact SET fun_fact_post = '{new_fact}' WHERE country_id = {country_id}; """
                self.cur.execute(update_funfact)
                self.conn.commit()
                to_return = {
                    "SUCESS": {
                        "Old fun fact": funfact[1],
                        "New fun fact": new_fact
                    }
                }
                return to_return
        else:
            return "Country doesn't exist or country name incorrect"