from fastapi import FastAPI, HTTPException
import pandas as pd
import psycopg2

# create FastAPI object
app = FastAPI()

# Ini function untuk bisa terhubung dengan database
def getConnection():
    # create connection
    conn = psycopg2.connect(
        dbname="neondb", user="neondb_owner", password="npg_sLfVg8iW4EwO",
        host="ep-steep-water-a102fmjl-pooler.ap-southeast-1.aws.neon.tech",
    )
    return conn

@app.get('/')
async def getWelcome():
    return {
        "msg": "sample-fastapi-pg"
    }

# Endpoint untuk menampilkan CSV
@app.get('/data')
def getData():
    # Untuk membaca data csv
    df = pd.read_csv('data.csv')
    # Untuk menampilkan hasil response harus menggunakan RETURN
    # Data harus dalam bentuk dict, makanya dari dataframe harus diubah
    return df.to_dict(orient="records") # orient ini utk bentuk datanya mau gimana, ada beberapa, bisa disesuaikan.

# Endpoint untuk menampilkan data yang di filter
# Pengaplikasian ada di lanjutan URL
@app.get('/data/{lokasi}')
def getData(lokasi:str): # Parameter diisi oleh filter diatas dan tipe datanya
    df = pd.read_csv('data.csv')

    # filter
    result = df.loc[df.lokasi == lokasi]
    
    # handle data error
    if result.shape[0] == 0:
        raise HTTPException(status_code=404, detail="Not Found") # Kalau mau nge return tapi untuk hasil yang error pakai RAISE
    
    # response
    return result.to_dict(orient="records")

# Menampilkan data dari database
@app.get('/profile')
async def getProfiles():
    # Menghubungkan dengan database dengan pakai function yang dibuat diatas
    connection = getConnection()

    # Membaca data sql
    df = pd.read_sql("select * from profiles;", connection)

    # response
    return df.to_dict(orient="records")

# @app.get(...)
# async def getProfileById():
#     pass


# @app.post(...)
# async def createProfile():
#     pass


# @app.patch(...)
# async def updateProfile():
#     pass


# @app.delete(...)
# async def deleteProfile():
#     pass
