from flask import Flask
from config import config
from extensions import db, login_manager, migrate, csrf


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from routes.auth          import auth
    from routes.main          import main
    from routes.bookings      import bookings
    from routes.facilities    import facilities
    from routes.admin         import admin
    from routes.notifications import notifications_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(bookings)
    app.register_blueprint(facilities)
    app.register_blueprint(admin)
    app.register_blueprint(notifications_bp)

    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data():
    from models import User, Facility

    if not User.query.filter_by(role='admin').first():
        admin = User(
            student_number='ADMIN001',
            name='System',
            surname='Administrator',
            email='admin@campus.ac.za',
            role='admin',
        )
        admin.set_password('Admin@1234')
        db.session.add(admin)

    if Facility.query.count() == 0:
        sample = [
            Facility(name='Computer Lab A',  facility_type='lab',
                     location='Block A, Room 101', capacity=30,
                     description='Modern computer lab with 30 workstations.',
                     equipment='30 PCs, Projector, Whiteboard, WiFi'),
            Facility(name='Computer Lab B',  facility_type='lab',
                     location='Block A, Room 102', capacity=25,
                     description='Programming lab with Linux and Windows systems.',
                     equipment='25 PCs, Dual Monitors, Network Switch'),
            Facility(name='Main Hall',       facility_type='hall',
                     location='Admin Block, Ground Floor', capacity=300,
                     description='Large multipurpose hall for events.',
                     equipment='PA System, Projector, Stage, Chairs'),
            Facility(name='Seminar Room 1',  facility_type='hall',
                     location='Block B, Room 201', capacity=50,
                     description='Ideal for seminars and group presentations.',
                     equipment='Projector, Whiteboard, Conference Table'),
            Facility(name='Sports Hall',     facility_type='sports',
                     location='Sports Complex', capacity=100,
                     description='Indoor sports hall.',
                     equipment='Basketball Hoops, Volleyball Net, Scoreboards'),
            Facility(name='Soccer Field',    facility_type='sports',
                     location='Sports Grounds', capacity=200,
                     description='Full-size soccer field with floodlights.',
                     equipment='Goalposts, Floodlights, Changing Rooms'),
            Facility(name='Lecture Hall 1',  facility_type='lecture_room',
                     location='Block C, Room 001', capacity=120,
                     description='Large tiered lecture theatre.',
                     equipment='Projector, Microphone, Recording System'),
        ]
        for f in sample:
            db.session.add(f)

    db.session.commit()


app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
