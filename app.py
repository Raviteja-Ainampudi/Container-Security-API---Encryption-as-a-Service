#!/usr/bin/python3

import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from DynamicEncryptionDecryption import EncryptionDecryption


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['POST', 'GET'])
def home_page():
    if request.method == 'POST':
        if all([key in request.form for key in ('fname', 'pwd', 'options')]):
            file_name = "?".join([str(ord(char)) for char in request.form['fname']])
            global password
            password = request.form['pwd']
            print(file_name, password)
            option = request.form['options']
            if file_name and password and option:
                if option.lower() == "encrypt":
                    return redirect(url_for('encryption', f_name=file_name))
                elif option.lower() == "decrypt":
                    return redirect(url_for('decryption', f_name=file_name))
    return render_template('home.html')


@app.route("/encrypt/<string:f_name>", methods=['GET', 'POST'])
def encryption(f_name=None):
    file_name = "".join(list(map(chr, list(map(int, f_name.split("?"))))))
    print(file_name)
    del_option = None
    if request.method == "POST":
        del_option, session['encryption_file_option'] = [request.form['deloptions']]*2
        ed_object = EncryptionDecryption.DynamicEncryptionAndDecryption()
        if not os.path.exists(file_name):
            flash(f"Given file {file_name} does not exist", "#800080")
        elif file_name.startswith("(Secured)"):
            flash(f"File {file_name} was already encrypted", "#800080")
        else:

            def file_encryption(file_name):
                output_file = ed_object.encrypt("{: <32}".format(password).encode(), file_name)
                flash(f"Done Encryption of {file_name}", "#00008B")
                flash(f"The Encrypted file name is {output_file}", "#006400")
                if del_option == "True":
                    os.remove(file_name)
                    flash(f"The file - {file_name} has been removed", "#2F4F4F")
                return
            if os.path.isfile(file_name):
                file_encryption(file_name)
            elif os.path.isdir(file_name):
                folder_files = ed_object.allfiles(file_name)
                print(folder_files)
                for Tfile in folder_files:
                    if os.path.isfile(Tfile):
                        file_encryption(Tfile)
                for Tfile in folder_files:
                    if os.path.isdir(Tfile):
                        os.rename(Tfile, Tfile + "(Secured)")
                os.rename(file_name, file_name + "(Secured)")
            else:
                pass

    return render_template('enc_result.html', del_option=del_option)


@app.route("/decrypt/<string:f_name>", methods=["POST", "GET"])
def decryption(f_name=None):
    file_name = "".join(list(map(chr, list(map(int, f_name.split("?"))))))
    print(file_name)
    del_option = None
    if request.method == "POST":
        del_option, session['encryption_file_option'] = [request.form['deloptions']] * 2
        ed_object = EncryptionDecryption.DynamicEncryptionAndDecryption()
        if not os.path.exists(file_name):
            flash(f"Given file {file_name} does not exist", "#800080")
        elif not file_name.split("/")[-1].startswith("(Secured)"):
            flash(f"File {file_name} was NOT encrypted", "#800080")
        else:

            def file_decryption(file_name):
                output_file = ed_object.decrypt("{: <32}".format(password).encode(), file_name)
                flash(f"Done Deryption of {file_name}", "#00008B")
                flash(f"The Decrypted file name is {output_file}", "#006400")
                if del_option == "True":
                    os.remove(file_name)
                    flash(f"The file - {file_name} has been removed", "#2F4F4F")
                return
            if os.path.isfile(file_name):
                file_decryption(file_name)
            elif os.path.isdir(file_name):
                folder_files = ed_object.allfiles(file_name)
                print(folder_files)
                for Tfile in folder_files:
                    if os.path.isfile(Tfile):
                        file_decryption(Tfile)
                for Tfile in folder_files:
                    if os.path.isdir(Tfile):
                        os.rename(Tfile, Tfile.replace("(Secured)", ''))
                os.rename(file_name, file_name.replace("(Secured)", ''))
            else:
                pass
    return render_template('dec_result.html', del_option=del_option)


@app.route("/listfiles", methods=['GET', 'POST'])
def list_files():
    ed_object = EncryptionDecryption.DynamicEncryptionAndDecryption()
    if request.method == "GET":
        available_files = ed_object.allfiles()
        default_folder = "Default Folder"
    elif request.method == "POST":
        path_name = request.form['foldername']
        available_files = ed_object.allfiles(path=path_name)
        default_folder = path_name
    else:
        return "Invalid HTTP Request"
    available_files = sorted(available_files)
    return render_template('list_files.html',
                           all_avail_files=available_files,
                           default_folder=default_folder)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000", debug=True)
