from configs.models import Model
from configs.fields import *


class ResPartner(Model):
    _name = 'res.partner'
    _id = 0
    _migrate = True

    name = Char(string="Name")
    age = Integer(string="Age")
    department = Char(string="Department")
    blood_group = Char(string="BloodGroup")
    create_dt = Datetime(string="CreateDt")
    write_dt = Date(string="WriteDt")
    salary = Float(string="Salary")