from .. import db,ma,auth

class Saved(db.Model):
    __tablename__="Saved"
    id=db.Column(db.Integer(),primary_key=True)
    pennies=db.Column(db.Integer())
    nickels=db.Column(db.Integer())
    dimes=db.Column(db.Integer())
    quarters=db.Column(db.Integer())
    dollar=db.Column(db.Integer())
    dollar5=db.Column(db.Integer())
    dollar10=db.Column(db.Integer())
    dollar20=db.Column(db.Integer())
    dollar50=db.Column(db.Integer())
    dollar100=db.Column(db.Integer())
    date=db.Column(db.String(length=20))
    def __repr__(self):
        return '''
        Saved(
            pennies={pennies},
            nickels={nickels},
            dimes={dimes},
            quarters={quarters},
            dollar={dollar},
            dollar5={dollar5},
            dollar10={dollar10},
            dollar20={dollar20},
            dollar50={dollar50},
            dollar100={dollar100},
            id={id},
            date={date}
        )'''.format(**dict(
            pennies=self.pennies,
            nickels=self.nickels,
            dimes=self.dimes,
            quarters=self.quarters,
            dollar=self.dollar,
            dollar5=self.dollar5,
            dollar10=self.dollar10,
            dollar20=self.dollar20,
            dollar50=self.dollar50,
            dollar100=self.dollar100,
            id=self.id),
            date=self.date
            )   
class SavedSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Saved
        fields=(
            "pennies",
            "nickels",
            "dimes",
            "quarters",
            "dollar",
            "dollar5",
            "dollar10",
            "dollar20",
            "dollar50",
            "dollar100",
            "id",
            "date"
            )      
    pennies=ma.auto_field()
    nickels=ma.auto_field()
    dimes=ma.auto_field()
    quarters=ma.auto_field()
    dollar=ma.auto_field()
    dollar5=ma.auto_field()
    dollar10=ma.auto_field()
    dollar20=ma.auto_field()
    dollar50=ma.auto_field()
    dollar100=ma.auto_field()
    date=ma.auto_field()
    id=ma.auto_field()
