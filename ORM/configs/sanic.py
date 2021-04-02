from sanic import Sanic
from sanic_auth import Auth
from sanic import Blueprint,response


# --------------------------Auth Configurations-------------------------------
orm_main = Sanic(__name__)
ormAuth = Auth(orm_main)
ormBlr = Blueprint
ClxRsp = response

ormBluePrint = orm_main.blueprint
ormConfig = orm_main.config









