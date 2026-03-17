from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from Formula1.models import db, Driver


driver = Blueprint('driver', __name__, url_prefix='/driver', template_folder='templates')


@driver.route('/')
def index():
    
    search_query = request.args.get('search', '')
    
    if search_query:
        
        drivers = Driver.query.filter(
            (Driver.name.like(f'%{search_query}%')) | 
            (Driver.team.like(f'%{search_query}%'))
        ).all()
    else:
        
        drivers = Driver.query.all()
        
    return render_template('driver_list.html', drivers=drivers, search_query=search_query)


@driver.route('/add', methods=['GET', 'POST'])
@login_required 
def add():
    if request.method == 'POST':
        
        name = request.form.get('name')
        team = request.form.get('team')
        nationality = request.form.get('nationality')
        driver_number = request.form.get('driver_number')
        points = request.form.get('points', 0) 
        image_url = request.form.get('image_url')
        
        
        new_driver = Driver(
            name=name,
            team=team,
            nationality=nationality,
            driver_number=driver_number,
            points=points,
            image_url=image_url,
            user_id=current_user.id 
        )
        
        try:
            db.session.add(new_driver)
            db.session.commit()
            flash(f'เพิ่มข้อมูลของ {name} เรียบร้อยแล้ว!', 'success')
            return redirect(url_for('driver.index'))
        except:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการบันทึกข้อมูล', 'danger')
            
    return render_template('add_driver.html')


@driver.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    
    d = Driver.query.get_or_404(id)
    
    if request.method == 'POST':
        
        d.name = request.form.get('name')
        d.team = request.form.get('team')
        d.nationality = request.form.get('nationality')
        d.driver_number = request.form.get('driver_number')
        d.points = request.form.get('points')
        d.image_url = request.form.get('image_url')
        
        try:
            db.session.commit()
            flash(f'อัปเดตข้อมูลของ {d.name} สำเร็จ!', 'success')
            return redirect(url_for('driver.index'))
        except:
            db.session.rollback()
            flash('ไม่สามารถแก้ไขข้อมูลได้', 'danger')
            
    return render_template('edit_driver.html', driver=d)


@driver.route('/delete/<int:id>')
@login_required
def delete(id):
    d = Driver.query.get_or_404(id)
    
    try:
        db.session.delete(d)
        db.session.commit()
        flash('ลบข้อมูลนักแข่งเรียบร้อยแล้ว', 'info')
    except:
        db.session.rollback()
        flash('ไม่สามารถลบข้อมูลได้', 'danger')
        
    return redirect(url_for('driver.index'))