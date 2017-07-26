from app import db, jj

if __name__ == '__main__':
    db.create_all()
    jj.run(debug=True)
