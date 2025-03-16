import pymysql


class DB:
    def __init__(self, host: str, user: str, password: str, db: str):
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=db,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error occured {e}")

    def __del__(self):
        self.connection.close()
        self.cursor.close()

    def add_data(
        self,
        erosion_degree,
        soil_moisture,
        rainfall,
        river_discharge,
        rf_output,
        lr_output,
        svc_output,
        accuracy,
        prediction,
    ) -> bool:
        ok = False
        try:
            q = """
                INSERT INTO flood_data(erosion_degree,soil_moisture, rainfall,      river_discharge, rf_model, lr_model,svc_model, accuracy,prediction) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            """

            data = (
                erosion_degree,
                soil_moisture,
                rainfall,
                river_discharge,
                lr_output,
                rf_output,
                svc_output,
                accuracy,
                prediction,
            )

            self.cursor.execute(q, data)
            self.connection.commit()
            ok = True
        except Exception as e:
            print(f"An error occured: {str(e)}")
            return ok

        return ok

    def get_data(self):
        try:
            q = "SELECT * FROM flood_data ORDER BY created_at DESC LIMIT 1"
            rows = self.cursor.execute(q)
            if rows > 0:
                flood_details = self.cursor.fetchall()
                details = flood_details[0]
        except Exception as e:
            print(f"An error occured {str(e)}")
            return None
        return details
