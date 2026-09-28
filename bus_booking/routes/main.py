import random
import string
from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Bus, Route, Schedule, Booking, Passenger
from extensions import db

main = Blueprint('main', __name__)


def generate_pnr():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@main.route('/')
def index():
    routes = Route.query.all()
    cities = sorted(set([r.source for r in routes] + [r.destination for r in routes]))
    today = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', cities=cities, now=today)


@main.route('/search')
def search():
    source = request.args.get('source', '').strip()
    destination = request.args.get('destination', '').strip()
    travel_date_str = request.args.get('travel_date', '').strip()
    num_seats = int(request.args.get('num_seats', 1))

    if not all([source, destination, travel_date_str]):
        flash('Please fill in all search fields.', 'warning')
        return redirect(url_for('main.index'))

    try:
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.', 'danger')
        return redirect(url_for('main.index'))

    schedules = Schedule.query.join(Route).join(Bus).filter(
        Route.source.ilike(f'%{source}%'),
        Route.destination.ilike(f'%{destination}%'),
        Schedule.travel_date == travel_date,
        Schedule.available_seats >= num_seats
    ).all()

    return render_template('search_results.html',
                           schedules=schedules,
                           source=source,
                           destination=destination,
                           travel_date=travel_date_str,
                           num_seats=num_seats)


@main.route('/book/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def book(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    num_seats = int(request.args.get('num_seats', 1))

    # Get booked seats for this schedule
    booked_seats = []
    for booking in schedule.bookings:
        if booking.status == 'Confirmed':
            for p in booking.passengers:
                booked_seats.append(p.seat_number)

    if request.method == 'POST':
        passengers_data = []
        seat_numbers = request.form.getlist('seat_number')
        names = request.form.getlist('passenger_name')
        ages = request.form.getlist('passenger_age')
        genders = request.form.getlist('passenger_gender')

        if len(names) != num_seats:
            flash('Passenger count mismatch.', 'danger')
            return redirect(url_for('main.book', schedule_id=schedule_id, num_seats=num_seats))

        # Validate seats not already taken
        for seat in seat_numbers:
            if seat in booked_seats:
                flash(f'Seat {seat} is already booked. Please choose another.', 'danger')
                return redirect(url_for('main.book', schedule_id=schedule_id, num_seats=num_seats))

        total_amount = schedule.price * num_seats
        pnr = generate_pnr()
        while Booking.query.filter_by(pnr=pnr).first():
            pnr = generate_pnr()

        booking = Booking(
            user_id=current_user.id,
            schedule_id=schedule.id,
            num_seats=num_seats,
            total_amount=total_amount,
            pnr=pnr
        )
        db.session.add(booking)
        db.session.flush()

        for i in range(num_seats):
            passenger = Passenger(
                booking_id=booking.id,
                name=names[i],
                age=int(ages[i]),
                gender=genders[i],
                seat_number=seat_numbers[i]
            )
            db.session.add(passenger)

        schedule.available_seats -= num_seats
        db.session.commit()
        flash('Booking confirmed!', 'success')
        return redirect(url_for('main.booking_confirmation', pnr=pnr))

    return render_template('book.html',
                           schedule=schedule,
                           num_seats=num_seats,
                           booked_seats=booked_seats,
                           total_seats=schedule.bus.total_seats)


@main.route('/confirmation/<pnr>')
@login_required
def booking_confirmation(pnr):
    booking = Booking.query.filter_by(pnr=pnr).first_or_404()
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('confirmation.html', booking=booking)


@main.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.booking_date.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)


@main.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('main.my_bookings'))
    if booking.status == 'Cancelled':
        flash('Booking already cancelled.', 'warning')
        return redirect(url_for('main.my_bookings'))

    booking.status = 'Cancelled'
    booking.schedule.available_seats += booking.num_seats
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('main.my_bookings'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
