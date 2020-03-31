#library
import math

#init variable yang digunakan
class Lokasi:
  def __init__(self, nama, totalJarak, demand, kapasitas ,luasGudang,biayaBangun,biayaSewa,biayaFaslog,biayaSimpan):
    self.nama = nama
    self.totalJarak = totalJarak
    self.demand = demand
    self.kapasitas = kapasitas
    self.luasGudang = luasGudang
    self.biayaBangun = biayaBangun
    self.biayaSewa = biayaSewa
    self.biayaFaslog = biayaFaslog
    self.biayaSimpan = biayaSimpan

class Kendaraan:
  def __init__(self, nama, kapasitasAngkut, biayaBahanBakar, fixedCost):
    self.nama = nama
    self.kapasitasAngkut = kapasitasAngkut
    self.biayaBahanBakar = biayaBahanBakar
    self.fixedCost = fixedCost

class Transportasi:
  def __init__(self, namaKendaraan,frekuensi, ukuranLot, jumlahKendaraan,biayaBahanBakar,fixedCost):
    self.namaKendaraan = namaKendaraan
    self.frekuensi = frekuensi
    self.ukuranLot = ukuranLot
    self.jumlahKendaraan = jumlahKendaraan
    self.biayaBahanBakar = biayaBahanBakar
    self.fixedCost = fixedCost


#Data Jarak
maxJarak = 10
jumlahLokasi = 4
dataJarak = [[0,3,2,4],
             [3,0,5,3],
             [2,5,0,2],
             [4,3,3,0]]

listLokasi = []
# input data lokasi ke object dengan format 
# nama demand,kapasitas,luas,biayaBangunPerTahun,biayaSewaPerTahun,biayaFaslog,biayaSimpan
listLokasi.append(Lokasi("Lokasi 1",sum(dataJarak[0]),10,60,200,5000000,6000000,5000,10000))
listLokasi.append(Lokasi("Lokasi 2",sum(dataJarak[1]),15,50,160,4500000,4750000,3000,7500))
listLokasi.append(Lokasi("Lokasi 3",sum(dataJarak[2]),11,55,180,4750000,5000000,3500,8500))
listLokasi.append(Lokasi("Lokasi 4",sum(dataJarak[3]),14,65,180,5250000,6500000,6000,10500))

#total demand
totalDemand = sum(Lokasi.demand for Lokasi in listLokasi)


frekuensi = [1, 2, 3, 4]
pMax = 2
pMin = 1

#Data Kendaraan
jumlahKendaraan = 2

listKendaraan = []
# input data kendaraan ke object dengan format 
# kapasitasAngkut,biayaBahanBakar,fixedCost
listKendaraan.append(Kendaraan("Kendaraan 1",7,3000,10000))
listKendaraan.append(Kendaraan("Kendaraan 2",9,4000,11000))

#biaya transportasi
listTransportasi=[]
#ukuranlot,jumlahkendaraan,bahanbakar,fixedcost
for kendaraan in listKendaraan:
    for i in frekuensi:
        listTransportasi.append(Transportasi(kendaraan.nama,i,math.ceil(totalDemand/i),math.ceil(totalDemand/(i*kendaraan.kapasitasAngkut)),kendaraan.biayaBahanBakar,kendaraan.fixedCost))

#data Gudang
listBiayaTransportasi = []
for transportasi in listTransportasi:
    listBiaya=[]
    listBiaya.append([transportasi.namaKendaraan,transportasi.frekuensi])
    x=1
    for i in dataJarak: 
        biaya=0
        for ii in i:
            biaya = biaya + ii*transportasi.biayaBahanBakar*transportasi.frekuensi*transportasi.jumlahKendaraan+transportasi.jumlahKendaraan*transportasi.fixedCost    
        listBiaya.append(biaya)
        x=x+1
    listBiayaTransportasi.append(listBiaya)
        
         
#biaya faslog

biayaFaslogBangun=[]
#loop biaya yang bangun terlebih dahulu
for lokasi in listLokasi:
    biaya = lokasi.demand*lokasi.biayaFaslog+lokasi.biayaBangun
    biayaFaslogBangun.append(biaya)

biayaFaslogSewa=[]
#loop biaya yang sewa
for lokasi in listLokasi:
    biaya = lokasi.demand*lokasi.biayaFaslog+lokasi.biayaSewa
    biayaFaslogSewa.append(biaya)

#biaya simpan untuk yang bangun atau sewa
biayaSimpan = []
x=0
while(x<len(frekuensi)):
    for lokasi in listLokasi:
        biaya = []
        biaya.append([lokasi.nama,frekuensi[x]])
        biaya.append(lokasi.biayaSimpan*(listTransportasi[x].ukuranLot/2))
        biayaSimpan.append(biaya)
    x=x+1

#total Cost
totalCost=[]

#menggunakan batasan
min=float('inf')
lokasiMin = ""
kendaraanMin = ""
fMin = ""
typeMin = ""

#biaya yang bangun
print("Biaya untuk Bangun")
for i in listBiayaTransportasi:
    kendaraan = i[0][0]
    for biayasimpan in biayaSimpan:
        lokasi = int(biayasimpan[0][0].split("Lokasi ")[1])
        fBiayasimpan = biayasimpan[0][1]
        nBiayasimpan = biayasimpan[1]
        if (i[0][1]==fBiayasimpan):
            #print semua kecuali judul
            biayaTotal = i[lokasi]+biayaFaslogBangun[lokasi-1]+nBiayasimpan
            print("F = ",fBiayasimpan," ",biayasimpan[0][0]," ",kendaraan," ",biayaTotal)

            #batasan jarak tempuh
            if (min>biayaTotal and listLokasi[lokasi-1].totalJarak<=maxJarak):
                min = biayaTotal
                lokasiMin = biayasimpan[0][0]
                kendaraanMin = kendaraan
                fMin = " F = "+str(fBiayasimpan)
                typeMin = "Bangun"
print("\n\n")
                
#biaya yang Sewa
print("Biaya untuk Sewa")
for i in listBiayaTransportasi:
    kendaraan = i[0][0]
    for biayasimpan in biayaSimpan:
        lokasi = int(biayasimpan[0][0].split("Lokasi ")[1])
        fBiayasimpan = biayasimpan[0][1]
        nBiayasimpan = biayasimpan[1]
        if (i[0][1]==fBiayasimpan):
            #print semua kecuali judul
            biayaTotal = i[lokasi]+biayaFaslogSewa[lokasi-1]+nBiayasimpan
            print("F = ",fBiayasimpan," ",biayasimpan[0][0]," ",kendaraan," ",biayaTotal)
            
            #batasan jarak tempuh
            if (min>biayaTotal and listLokasi[lokasi-1].totalJarak<=maxJarak):
                lokasiMin = biayasimpan[0][0]
                kendaraanMin = kendaraan
                fMin = " F = "+str(fBiayasimpan)
                typeMin = "Sewa"

#hasil Akhir
print("")
print("Hasil Akhir : ")
print("Dengan pembatas jarak maximum adalah ",maxJarak)
print("")
print("Diperoleh hasil yang paling optimal : ")
#validasi jika data tidak ditemukan
if typeMin!="":
    print("Type :",typeMin," ",fMin," ",lokasiMin," ",kendaraanMin," ",min)
else:
    print("Hasil tidak dapat ditemukan")             



