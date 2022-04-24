
import datetime
from connectdb import Database
from flask import Flask, session, render_template,request,redirect,url_for
app = Flask(__name__)

conn = Database('ksb-2022')


app.secret_key = 'ini rahasia!'

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('webix'))

@app.route('/daftar', methods=['GET','POST'])
def daftar():
    if (request.method == 'POST'):
        username1 = request.form.get('username')
        password1 = request.form.get('password')
        a = conn.select4("select username from frankie_672019165_login where username = '%s' "%(username1))
        if (a[0] != True):
            conn.crud("INSERT INTO  frankie_672019165_login VALUES(%s,%s) ", (username1, password1))
        else:
            session['gagal2'] = 'Username telah digunakan'
            return render_template('register.html',gagal=session['gagal2'])

        return redirect(url_for('webix'))

    return render_template('register.html')

# admin


@app.route('/admin', methods=['GET','POST'])
def admin():

    if (request.method == 'POST'):

        username1 = request.form.get('username')
        password1 = request.form.get('password')
        isi = conn.select("select * from frankie_672019165_admin where username=%s and passwrod =%s", (username1, password1))

        if isi is not None:

            if (isi[0] == username1 and isi[1] == password1):
                session['sukses'] = True
                session['admin'] = isi[0]
                return redirect(url_for('adminhome'))
        else:
            session['gagal'] = 'Username/Kata sandi salah'
            return render_template("loginadmin.html", gagal=session['gagal'])

    return render_template("loginadmin.html")


@app.route('/riwayatadmin', methods=['GET'])
def riwayatadmin():
    nim = conn.select2("SELECT  statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ','),tanggalnow,pemesan  FROM frankie_672019165_pesanan WHERE  statusnya = 'Selesai' or statusnya = 'Retur Disetujui' group by unik,statusnya, tanggalnow,pemesan order by unik desc")

    session['riwayat'] = nim

    return render_template("riwayatadmin.html", nim2=session['riwayat'], user=session['admin'])

@app.route('/tolak', methods=['GET'])
def tolak():
    nim = conn.select2("SELECT  statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ','),tanggalnow,pemesan  FROM frankie_672019165_pesanan WHERE  statusnya = 'Ditolak' or statusnya = 'Dibatalkan' or statusnya = 'Retur Ditolak'group by unik,statusnya, tanggalnow,pemesan order by unik desc")

    session['tolak'] = nim

    return render_template("tolak.html", nim2=session['tolak'], user=session['admin'])


@app.route('/adminhome', methods=['GET'])
def adminhome():

    return render_template("adminhome.html",user=session['admin'])

@app.route('/returadmin', methods=['GET'])
def returadmin():
    update = request.args.get('update')
    tolak = request.args.get('tolak')

    if (update != None):
        conn.crud2("UPDATE frankie_672019165_pesanan SET tanggalnow = now(), statusnya = 'Retur Disetujui' WHERE unik = '%s'" % (update))
    elif (tolak != None):
        conn.crud2("UPDATE frankie_672019165_pesanan SET tanggalnow = now(), statusnya = 'Retur Ditolak' WHERE unik = '%s'" % (tolak))

    nim = conn.select2("SELECT  pemesan,statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ',')  FROM frankie_672019165_pesanan WHERE  statusnya ='Menunggu Persetujuan' group by unik,statusnya,pemesan order by unik desc")

    session['returadmin'] = nim
    return render_template("returadmin.html", nim2=session['returadmin'], user=session['admin'])

@app.route('/editedit', methods=['GET'])
def editedit():
    ganti = request.args.get('ganti')
    hapus = request.args.get('hapus')
    id = session['idbuku']
    judul2 = request.args.get('judul')
    harga = request.args.get('harga')
    deskripsi = request.args.get('deskripsi')
    halaman = request.args.get('halaman')
    penerbit = request.args.get('penerbit')
    tanggal = request.args.get('tanggal')
    berat = request.args.get('berat')
    lebar = request.args.get('lebar')
    panjang = request.args.get('panjang')
    isbn = request.args.get('isbn')
    bahasa = request.args.get('bahasa')
    tema = request.args.get('tema')
    if ganti != None:
        conn.crud("UPDATE frankie_672019165_buku SET judul = %s, harga= %s, deskripsi = %s,halaman=%s,penerbit = %s, tanggal=%s,berat=%s,lebar=%s,panjang=%s,isbn=%s,bahasa=%s,tema=%s WHERE id = %s",(judul2, harga, deskripsi, halaman, penerbit, tanggal, berat, lebar, panjang, isbn, bahasa, tema,id))
    elif hapus != None:
        conn.crud("DELETE FROM frankie_672019165_buku WHERE id = %s",(hapus))

    return redirect(url_for('editbuku'))


@app.route('/editbuku', methods=['GET','POST'])
def editbuku():



    if (request.method == 'POST'):
        id = request.form.get('id')

        if (id != None):
            hasil = conn.select2("select * from frankie_672019165_buku where id = '%s'" % (id))
            session['idbuku'] = id
            if hasil != None:
                hasil2 = conn.select("select * from frankie_672019165_buku where id = %s", (id))
                if hasil2 != None:
                    session['id'] = hasil2[1]
                else:
                    session['id'] = 'Data Buku tidak ditemukan'
                session['hasil'] = hasil
                return render_template("editbuku.html", nim2=session['hasil'], id=session['id'])






    return render_template("editbuku.html",user=session['admin'])


@app.route('/tambahadmin', methods=['GET','POST'])
def tambahadmin():
    if (request.method == 'POST'):
        id = request.form.get('id')
        judul = request.form.get('judul')
        harga = request.form.get('harga')
        deskripsi = request.form.get('deskripsi')
        halaman = request.form.get('halaman')
        penerbit = request.form.get('penerbit')
        tanggal = request.form.get('tanggal')
        berat = request.form.get('berat')
        lebar = request.form.get('lebar')
        panjang = request.form.get('panjang')
        isbn = request.form.get('isbn')
        bahasa = request.form.get('bahasa')
        tema = request.form.get('tema')
        a = conn.select4("select id from frankie_672019165_buku where id = '%s' " % (id))
        if a[0] != True:
            conn.crud("INSERT INTO  frankie_672019165_buku VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (id, judul,harga,deskripsi,halaman,penerbit,tanggal,berat,lebar,panjang,isbn,bahasa,tema))
            session['pesan'] = ('Berhasil tambah data dengan ID %s'%(id))
            return render_template("tambahadmin.html", berhasil=session['pesan'])
        else:
            session['pesan'] = 'ID Telah Dipakai, Silahkan Mengganti ID yang lain'
            return render_template("tambahadmin.html",pesan=session['pesan'])





    return render_template("tambahadmin.html",user=session['admin'])



@app.route('/pesananadmin', methods=['GET'])
def pesananadmin():
    update = request.args.get('update')
    tolak = request.args.get('tolak')
    status1 = request.args.get('status1')
    status2 = request.args.get('status2')

    if(update != None):
        if status1 == 'Menunggu Konfirmasi':
            conn.crud2("UPDATE frankie_672019165_pesanan SET statusnya = 'Diproses' WHERE unik = '%s'"%(update))
        elif status1 == 'Diproses':
            conn.crud2("UPDATE frankie_672019165_pesanan SET tanggalnow = now(), statusnya = 'Selesai' WHERE unik = '%s'"%(update))
    elif (tolak != None):
        if status2 == 'Menunggu Konfirmasi':
            conn.crud2("UPDATE frankie_672019165_pesanan SET tanggalnow = now(),  statusnya = 'Ditolak' WHERE unik = '%s'"%(tolak))
        elif status2 == 'Diproses':
            conn.crud2("UPDATE frankie_672019165_pesanan SET tanggalnow = now(), statusnya = 'Dibatalkan' WHERE unik = '%s'"%(tolak))


    nim = conn.select2("SELECT  pemesan,statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ',')  FROM frankie_672019165_pesanan WHERE  statusnya !='Selesai' and statusnya != 'Dibatalkan' and statusnya != 'Ditolak' and statusnya != 'Menunggu Persetujuan' and statusnya != 'Retur Disetujui' and statusnya != 'Retur Ditolak' group by unik,statusnya,pemesan order by unik desc")

    session['pesananadnim'] = nim

    return render_template("pesananadmin.html", nim2=session['pesananadnim'], user=session['admin'])

# user

@app.route('/pesanan', methods=['GET'])
def pesanan():

    nim = conn.select2("SELECT  statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ',')  FROM frankie_672019165_pesanan WHERE pemesan = '%s' and statusnya ='Menunggu Konfirmasi' or pemesan = '%s' and statusnya ='Menunggu Persetujuan' or pemesan = '%s' and statusnya ='Ditolak' or pemesan = '%s' and statusnya ='Dibatalkan'   group by unik,statusnya order by unik desc"%(session['user'],session['user'],session['user'],session['user']))

    session['p'] = nim

    return render_template("pesanan.html",nim2=session['p'], user=session['user'])



@app.route('/keranjang', methods=['GET'])
def keranjang():
    tambah = request.args.get('tambah')
    kurang = request.args.get('kurang')
    jumlah = request.args.get('jumlah')
    pesan = request.args.get('pesan')

    if tambah != None:
        a = conn.crud("UPDATE frankie_672019165_order_buku SET jumlah = %s WHERE orderid = %s",
                          (int(jumlah) + 1, tambah))
    elif kurang != None:
        b = conn.crud("UPDATE frankie_672019165_order_buku SET jumlah = %s WHERE orderid = %s",
                          (int(jumlah) - 1, kurang))
        if int(jumlah) == 1:
            b = conn.crud2("DELETE FROM frankie_672019165_order_buku  WHERE orderid = '%s'"%(kurang))
    if pesan != None:
        unik = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data = conn.select2("select * from frankie_672019165_order_buku where pemesan = '%s'" % (session['user']))
        for x in data:
            hasil = conn.crud2("INSERT INTO frankie_672019165_pesanan(id,judul,harga,jumlah,pemesan,tanggal,statusnya,total,unik,tanggalnow) VALUES ('%d','%s', '%d','%d', '%s',now(),'Menunggu Konfirmasi','%d','%s',NULL)" % (int(x[1]), str(x[2]), int(x[3]), int(x[4]), str(x[5]) , int(x[3]*x[4]), unik))

        conn.crud2("Delete from frankie_672019165_order_buku where pemesan = '%s'" % (session['user']))

    nim = conn.select2("select * from frankie_672019165_order_buku where pemesan = '%s' order by orderid asc"%(session['user']))

    session['j'] = nim

    return render_template("keranjang.html", nim2=session['j'], user=session['user'])

@app.route('/detailadmin', methods=['GET'])
def detailadmin():
    detail2 = request.args.get('detail')
    nim = conn.select2("select * from frankie_672019165_pesanan where unik = '%s'"%(detail2))
    session['detail2'] = nim

    return render_template("detailadmin.html",user=session['admin'],nim2 =session['detail2'])

@app.route('/detailuser', methods=['GET'])
def detailuser():
    detail = request.args.get('detail')
    nim = conn.select2("select * from frankie_672019165_pesanan where unik = '%s'"%(detail))
    session['detail'] = nim

    return render_template("detailuser.html",user=session['user'],nim2 =session['detail'])

@app.route('/riwayat', methods=['GET'])
def riwayat():
    nim = conn.select2("SELECT  statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ','),tanggalnow  FROM frankie_672019165_pesanan WHERE pemesan = '%s' and statusnya = 'Selesai' or pemesan = '%s' and statusnya = 'Retur Disetujui' or pemesan = '%s' and statusnya = 'Retur Ditolak' group by unik,statusnya, tanggalnow order by unik desc" % (session['user'],session['user'],session['user']))

    session['riwayat'] = nim

    return render_template("riwayat.html", nim2=session['riwayat'], user=session['user'])

@app.route('/retur', methods=['GET'])
def retur():
    retur = request.args.get('retur')
    if retur != None:
        conn.crud2("UPDATE frankie_672019165_pesanan SET statusnya = 'Menunggu Persetujuan' WHERE unik = '%s'" % (retur))


    nim = conn.select2("SELECT  statusnya,unik,  SUM (jumlah), SUM (total),string_agg(judul, ','),tanggalnow  FROM frankie_672019165_pesanan WHERE pemesan = '%s' and statusnya = 'Selesai'  group by unik,statusnya, tanggalnow order by unik desc" % (session['user']))

    session['riwayat'] = nim

    return render_template("retur.html", nim2=session['riwayat'], user=session['user'])

@app.route('/sukses')
def sukses():

    id = request.args.get('tambah');
    judul = request.args.get('judul');
    harga = request.args.get('harga');
    user = request.args.get('user');
    search = request.args.get('search');
    if (id != None):
        a = conn.select4("select id from frankie_672019165_order_buku where id = '%s' and pemesan ='%s' "%(id,session['user']))
        if (a[0] != True):
            hasil = conn.crud("INSERT INTO frankie_672019165_order_buku(id,judul,harga,jumlah,pemesan)VALUES ( %s, %s, %s,1,%s)",(id, judul, harga, user))

    if search != None and search != "":
        nim = conn.select2("select * from frankie_672019165_buku where judul ILIKE '%"+search+"%'or tema ILIKE '%"+search+"%'")
        session['nim'] = nim
    else:
        nim = conn.select2("select * from frankie_672019165_buku ")
        session['nim'] = nim

    return render_template("data.html",nim2 = session['nim'],user = session['user'])

@app.route('/webix', methods=['GET','POST'])
def webix():
    if (request.method == 'POST'):
        username1 = request.form.get('username')
        password1 = request.form.get('password')
        isi = conn.select("select * from frankie_672019165_login where username=%s and psw =%s", (username1, password1))

        if isi is not None:
            if (isi[0] == username1 and isi[1] == password1):
                session['sukses'] = True
                session['user'] = isi[0]
                return redirect(url_for('sukses'))
        else:
            session['gagal'] = 'Nama / Kata sandi salah'
            return render_template('home.html', gagal=session['gagal'])

    return render_template('home.html')


@app.route('/keluar', methods=['GET'])
def keluar():
    session.clear()
    return redirect(url_for('admin'))

@app.route('/keluaruser', methods=['GET'])
def keluaruser():
    session.clear()
    return redirect(url_for('webix'))



if __name__ == '__main__':
    app.run(
        host='localhost',
        port= 8080,
        debug= True)