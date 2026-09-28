from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Bus, Route, Schedule, Booking, User
from extensions import db
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_buses = Bus.query.count()
    total_routes = Route.query.count()
    confirmed_bookings = Booking.query.filter_by(status='Confirmed').count()
    total_revenue = db.session.query(db.func.sum(Booking.total_amount))\
        .filter_by(status='Confirmed').scalar() or 0
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()
    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_bookings=total_bookings,
                           total_buses=total_buses,
                           total_routes=total_routes,
                           confirmed_bookings=confirmed_bookings,
                           total_revenue=total_revenue,
                           recent_bookings=recent_bookings)


# ── Bus Management ────────────────────────────────────────────────────────────
@admin.route('/buses')
@login_required
@admin_required
def buses():
    all_buses = Bus.query.all()
    return render_template('admin/buses.html', buses=all_buses)


@admin.route('/buses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_bus():
    if request.method == 'POST':
        bus = Bus(
            bus_number=request.form['bus_number'],
            bus_name=request.form['bus_name'],
            bus_type=request.form['bus_type'],
            total_seats=int(request.form['total_seats']),
            amenities=request.form.get('amenities', '')
        )
        db.session.add(bus)
        db.session.commit()
        flash('Bus added successfully!', 'success')
        return redirect(url_for('admin.buses'))
    return render_template('admin/add_bus.html')


@admin.route('/buses/edit/<int:bus_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    if request.method == 'POST':
        bus.bus_number = request.form['bus_number']
        bus.bus_name = request.form['bus_name']
        bus.bus_type = request.form['bus_type']
        bus.total_seats = int(request.form['total_seats'])
        bus.amenities = request.form.get('amenities', '')
        db.session.commit()
        flash('Bus updated successfully!', 'success')
        return redirect(url_for('admin.buses'))
    return render_template('admin/edit_bus.html', bus=bus)


@admin.route('/buses/delete/<int:bus_id>', methods=['POST'])
@login_required
@admin_required
def delete_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    db.session.delete(bus)
    db.session.commit()
    flash('Bus deleted.', 'success')
    return redirect(url_for('admin.buses'))


# ── Route Management ──────────────────────────────────────────────────────────
@admin.route('/routes')
@login_required
@admin_required
def routes():
    all_routes = Route.query.all()
    return render_template('admin/routes.html', routes=all_routes)


@admin.route('/routes/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_route():
    if request.method == 'POST':
        route = Route(
            source=request.form['source'],
            destination=request.form['destination'],
            distance_km=float(request.form['distance_km'])
        )
        db.session.add(route)
        db.session.commit()
        flash('Route added successfully!', 'success')
        return redirect(url_for('admin.routes'))
    return render_template('admin/add_route.html')


@admin.route('/routes/delete/<int:route_id>', methods=['POST'])
@login_required
@admin_required
def delete_route(route_id):
    route = Route.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    flash('Route deleted.', 'success')
    return redirect(url_for('admin.routes'))


# ── Schedule Management ───────────────────────────────────────────────────────
@admin.route('/schedules')
@login_required
@admin_required
def schedules():
    all_schedules = Schedule.query.order_by(Schedule.travel_date.desc()).all()
    return render_template('admin/schedules.html', schedules=all_schedules)


@admin.route('/schedules/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_schedule():
    buses = Bus.query.all()
    routes = Route.query.all()
    if request.method == 'POST':
        bus = Bus.query.get(int(request.form['bus_id']))
        schedule = Schedule(
            bus_id=int(request.form['bus_id']),
            route_id=int(request.form['route_id']),
            departure_time=datetime.strptime(request.form['departure_time'], '%H:%M').time(),
            arrival_time=datetime.strptime(request.form['arrival_time'], '%H:%M').time(),
            travel_date=datetime.strptime(request.form['travel_date'], '%Y-%m-%d').date(),
            price=float(request.form['price']),
            available_seats=bus.total_seats
        )
        db.session.add(schedule)
        db.session.commit()
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('admin.schedules'))
    return render_template('admin/add_schedule.html', buses=buses, routes=routes)


@admin.route('/schedules/delete/<int:schedule_id>', methods=['POST'])
@login_required
@admin_required
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    flash('Schedule deleted.', 'success')
    return redirect(url_for('admin.schedules'))


# ── Booking Management ────────────────────────────────────────────────────────
@admin.route('/bookings')
@login_required
@admin_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin/bookings.html', bookings=all_bookings)


@admin.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)
