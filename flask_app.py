from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextField, DateField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename="",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = "something only you know"

class food(db.Model):

    __tablename__ = "food"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    purchase = db.Column(db.Date)
    expiry = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    typequantity = db.Column(db.String(128))
    group = db.Column(db.String(128))

    def __repr__(self):
        return '<food: {}>'.format(self.name)

class InputForm(FlaskForm):
    name = TextField(
        'Name of Food', validators=[DataRequired(), Length(min=1, max=75)]
    )
    purchase = DateField(
        'Date of Purchase', format='%m/%d/%Y', validators=[DataRequired()]
    )
    expiry = DateField(
        'Date of Expiry',  format='%m/%d/%Y', validators=[DataRequired()]
    )
    quantity = IntegerField(
        'Quantity', validators=[DataRequired()]
    )
    typequantity = SelectField(
        'Type of Quantity', choices = [('Packets', 'Packets'), ('Kilograms', 'Kilograms'), ('Grams', 'Grams'), ('ml', 'Millilitre'), ('L', 'Litres'), ('N/A', 'N/A')], validators=[DataRequired()]
    )
    group = SelectField(
        'Food Group', choices = [('Dairy', 'Dairy'), ('Fruits', 'Fruits'), ('Vegetables', 'Vegetables'), ('Grain', 'Grain'), ('Meat', 'Meat'), ('Confectioneries', 'Confectioneries')], validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', food = food.query.order_by(food.expiry.asc()).all())

@app.route('/help/')
def settings():
        return render_template('help.html')

@app.route("/input/", methods=['GET', 'POST'])
def AddFood():
    form = InputForm()
    if form.validate_on_submit():
        item = food(name=form.name.data, purchase=form.purchase.data, expiry=form.expiry.data, quantity=form.quantity.data, typequantity=form.typequantity.data, group=form.group.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('input.html', action="Add", form=form)

@app.route('/edit/<int:id>/', methods=['GET','POST'])
def edit(id):
    item = food.query.get_or_404(id)
    form = InputForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.purchase = form.purchase.data
        item.expiry = form.expiry.data
        item.quantity = form.quantity.data
        item.typequantity = form.typequantity.data
        item.group = form.group.data
        db.session.commit()
        return redirect(url_for('index'))
    form.name.data = item.name
    form.purchase.data = item.purchase
    form.expiry.data = item.expiry
    form.quantity.data = item.quantity
    form.typequantity.data = item.typequantity
    form.group.data = item.group

    return render_template('input.html', action="Edit", item=item, form=form)



@app.route("/delete/<int:id>/", methods=['GET','POST'])
def delete(id):
    Item = food.query.get_or_404(id)
    db.session.delete(Item)
    db.session.commit()
    return redirect(url_for('index'))
    return render_template('input.html', Item=Item)
