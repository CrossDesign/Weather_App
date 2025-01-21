from flask import Flask, render_template
import pandas as pd


stations_table = pd.read_csv('data/data_small/stations.txt', skiprows=17)
stations_table = stations_table[['STAID','STANAME                                 ']]

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('home.html', stations_table=stations_table.to_html())

    @app.route('/api/v1/<station>')
    def all_data(station):
        default_path = "data/data_small/TG_STAID"
        station_path = default_path + str(station).zfill(6) + '.txt'
        df = pd.read_csv(station_path,skiprows=20,parse_dates=['    DATE'])
        result = df.to_dict(orient='records')
        return result

    @app.route('/api/v1/yearly/<station>/<year>')
    def year_data(station,year):
        default_path = "data/data_small/TG_STAID"
        station_path = default_path + str(station).zfill(6) + '.txt'
        df = pd.read_csv(station_path,skiprows=20)
        df['    DATE'] = df['    DATE'].astype(str)
        df = df[df['    DATE'].str.startswith(str(year))]
        result = df.to_dict(orient='records')
        return result
    
    @app.route('/api/v1/<station>/<date>')
    def about(station, date):
        default_path = "data/data_small/TG_STAID"
        station_path = default_path + str(station).zfill(6) + '.txt'
        df = pd.read_csv(station_path,skiprows=20,parse_dates=['    DATE'])
        temperature = df.loc[df['    DATE'] == str(date)]['   TG'].squeeze() /10
        # Filter the data by date
        return {'date': date,
                'station': station,
                'temperature': temperature}
    
    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000,debug=True)
