from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ayurwellness_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ayurwellness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file is a valid image."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Models
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # herb, shrub, tree, root, fruit
    conditions = db.Column(db.String(255), nullable=False)  # comma-separated list of conditions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    procedure = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

# Routes
@app.route('/')
def index():
    plants = Plant.query.order_by(Plant.name).limit(3).all()
    treatments = Treatment.query.order_by(Treatment.name).limit(4).all()
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).limit(3).all()
    blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template('index.html', 
                          plants=plants, 
                          treatments=treatments, 
                          testimonials=testimonials, 
                          blog_posts=blog_posts)

@app.route('/plants')
def plants():
    plants = Plant.query.order_by(Plant.name).all()
    return render_template('plants.html', plants=plants)

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return render_template('plant_detail.html', plant=plant)

@app.route('/api/plants')
def api_plants():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    condition = request.args.get('condition', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    query = Plant.query
    
    if search:
        query = query.filter(Plant.name.ilike(f'%{search}%') | 
                             Plant.scientific_name.ilike(f'%{search}%') |
                             Plant.description.ilike(f'%{search}%'))
    
    if category:
        query = query.filter(Plant.category == category)
    
    if condition:
        query = query.filter(Plant.conditions.like(f'%{condition}%'))
    
    plants = query.order_by(Plant.name).paginate(page=page, per_page=per_page, error_out=False)
    
    result = {
        'plants': [{
            'id': plant.id,
            'name': plant.name,
            'scientific_name': plant.scientific_name,
            'description': plant.description,
            'image': plant.image,
            'category': plant.category,
            'conditions': plant.conditions.split(','),
        } for plant in plants.items],
        'total': plants.total,
        'pages': plants.pages,
        'current_page': plants.page
    }
    
    return jsonify(result)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        flash('Your message has been sent. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/admin/plants', methods=['GET', 'POST'])
def admin_plants():
    if request.method == 'POST':
        image_file = None
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
            else:
                flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif.', 'error')
                return redirect(url_for('admin_plants'))
        
        new_plant = Plant(
            name=request.form.get('name'),
            scientific_name=request.form.get('scientific_name'),
            description=request.form.get('description'),
            benefits=request.form.get('benefits'),
            usage=request.form.get('usage'),
            image=image_file,
            category=request.form.get('category'),
            conditions=','.join(request.form.getlist('conditions'))
        )
        
        db.session.add(new_plant)
        db.session.commit()
        
        flash('Plant added successfully!', 'success')
        return redirect(url_for('admin_plants'))
    
    plants = Plant.query.order_by(Plant.name).all()
    return render_template('admin/plants.html', plants=plants)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Create database tables and add initial data if empty
@app.before_first_request
def create_tables():
    db.create_all()  # Create tables if they do not exist
    if Plant.query.count() == 0:
        ashwagandha = Plant(
            name="Ashwagandha",
            scientific_name="Withania somnifera",
            description="A powerful adaptogen that helps the body manage stress and promotes overall vitality.",
            benefits="Reduces stress and anxiety, improves sleep, boosts immunity, enhances energy levels, and supports reproductive health.",
            usage="Available as powder, capsules, or liquid extract. Typically taken daily for stress management.",
            image="ashwagandha.jpg",
            category="herb",
            conditions="stress,immunity,energy,sleep"
        )
        
        turmeric = Plant(
            name="Turmeric",
            scientific_name="Curcuma longa",
            description="A powerful anti-inflammatory and antioxidant herb widely used in Ayurvedic medicine.",
            benefits="Reduces inflammation, supports joint health, improves digestion, and has antioxidant properties.",
            usage="Used in cooking, as supplements, or as a paste for external application. The bioavailability increases when combined with black pepper.",
            image="turmeric.jpg",
            category="root",
            conditions="inflammation,digestive,immunity,skin"
        )
        
        tulsi = Plant(
            name="Tulsi (Holy Basil)",
            scientific_name="Ocimum sanctum",
            description="Revered as 'The Queen of Herbs' in Ayurveda for its numerous health benefits.",
            benefits="Supports respiratory health, reduces stress, boosts immunity, and has antimicrobial properties.",
            usage="Can be consumed as tea, in cooking, or as supplements. Fresh leaves can be chewed daily.",
            image="tulsi.jpg",
            category="herb",
            conditions="stress,respiratory,immunity,skin"
        )
        
        db.session.add_all([ashwagandha, turmeric, tulsi])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
