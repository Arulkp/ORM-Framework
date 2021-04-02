from configs.sanic import orm_main,ormBlr,ClxRsp,ormBluePrint,ormConfig


print("succcess.......")



resusersaction = ormBlr('res_partner', url_prefix='/users')
@resusersaction.route('/user', methods=['GET'])
async def action_search_user(request):
     name = "vignesh"
     age = 20
     userobj_l = await ormConfig.env['res.partner'].search([('name', '=',name), '&', ('age', '=', age)])
     print(userobj_l)
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})


ormBluePrint(resusersaction)