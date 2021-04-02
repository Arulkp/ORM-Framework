import os
from importlib import import_module
import inspect
from configs.models import Database as db
from configs.db_config import DB_CONFIG as dbcon
from configs.sanic import orm_main,ormConfig
from configs.tools import OrmTools as tools
from configs.models import Model


# ------------------------------Configs--------------------------------
root_entry = "/"
root_path = 'addons'
models_path = 'models'
route_path = 'routes'



#---------------------------Module Configurations------------------------------
from pathlib import Path

class ClassRegistry:

    @classmethod
    def Module_Loader(cls, package_dir):
        tbclassess = []
        parent_root = str(package_dir) + str(root_entry) + str(root_path)
        for pkgs in os.listdir(parent_root):
            if pkgs not in ['__pycache__', '__init__.py']:
                inside_root = parent_root + str(root_entry) + str(pkgs)
                for inside in os.listdir(inside_root):
                    if inside not in ['__pycache__', '__init__.py']:
                        if inside == str(models_path):
                            model_ins_root = inside_root + str(root_entry) + str(models_path)
                            for minside in os.listdir(model_ins_root):
                                print(minside)
                                if minside not in ['__pycache__', '__init__.py']:
                                    module = import_module(root_path + "." + pkgs + "." + models_path + "." + str(
                                        minside[:minside.index('.')]), ".")
                                    for m in inspect.getmembers(module, inspect.isclass):
                                        if Model in m[1].__bases__:
                                            classobj = getattr(module, str(m[0]))
                                            print(m, "=================")
                                            tbclassess.append(classobj)
        return tbclassess

    @classmethod
    def InstanceEnviron(cls, tbclass_l=[]):
        environ_dict = {}
        for clsobj in tbclass_l:
            if clsobj._migrate:
                environ_dict[clsobj._name] = clsobj()
        return environ_dict

    @classmethod
    def NewTablesParser(cls, tblist=[], tbobjdict={}):
        if tblist:
            return [tb for tb in list(tbobjdict.keys()) if str(tb).replace(".", "_") not in tblist[0]]
        else:
            return [tb for tb in list(tbobjdict.keys())]


async def create_new_tables(tblist=[]):
    newtables = ClassRegistry.NewTablesParser(tblist=list(tblist), tbobjdict=ormConfig.env)
    for tbl in newtables:
        tbclass = ormConfig.env.get(tbl)
        if tbclass._migrate:
            query = await tbclass.createtb()
            await ormConfig.environ._execute(query)



async def update_new_columns(tblist=[]):
    for tbls in tblist:
        cols = await ormConfig.environ.get_all_cols(tbls[0])
        colsl = tools.parse_same_key_list(cols)
        sqlq = ormConfig.env[str(tbls[0]).replace('_', '.')]._migrate_new_cols(existcolist=colsl.values())
        if sqlq:
            await ormConfig.environ._execute(sqlq)



@orm_main.listener('before_server_start')
async def register_db(orm_main, loop):

    modules = ClassRegistry.Module_Loader(package_dir= Path(__file__).resolve().parent)
    ormConfig['environ'] = db(dbuser=dbcon.get('dbuser'), userpass=dbcon.get('dbpass'), dbname=dbcon.get('dbname'),
                                  dbhost=dbcon.get('dbhost'), dbport=dbcon.get('dbport'), maxquery=4000,
                                  maxinclife=5000)
    ormConfig['envpool'] = await ormConfig.environ.register_db
    ormConfig['env'] = ClassRegistry.InstanceEnviron(tbclass_l=modules)

    tables = await ormConfig.environ.tables()
    tblist = tools.parse_same_key_list(keylist=tables)
    tblist = tblist.values() if tables else []
    await create_new_tables(tblist=tblist)
    await update_new_columns(tblist=tblist)
    vals = {'name': 'balavignesh', 'age': 24, 'department': 'IT', 'blood_group': 'A+'}
    # userobj = await ormConfig.env['res.partner'].create(vals=vals)
    search_ids = [1, 8, 10]
    # userobj = await ormConfig.env['res.partner'].browse(search_ids)
    # print(userobj)

    name = 'vignesh'
    age = 20

    # userobj = await ormConfig.env['res.partner'].search([('name', '=', name), '&', ('age', '=', age)])
    # for user in userobj:
    #     await user.write({'name': 'vignesh', 'age': 20})

    # userobj = await ormConfig.env['res.partner'].search([('name', '=', name), '&', ('age', '=', age)])
    # for user in userobj:
    #     await user.unlink()




if __name__ == '__main__':
    os.path.dirname(os.path.realpath('main.py'))
    orm_main.run()

