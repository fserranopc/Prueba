# -*- coding: utf-8 -*-
{
    'name'        :"Internal Stock On Website Product",
    'author'      :'Daniel Chuc',
    'category'    :'Website',
    'summary'     :"""Internal Stock On Product""",
    'description' :""" Internal Stock On Product """,
    'version'      :'15.0.0.0',
    'depends'     :['website_sale','website','sale_management'],
    'data'        :[
                    'views/internal_stock_template.xml',
                    'views/stock_location.xml',
                   ],
    'license': 'AGPL-3',
    'installable' :True,
    'application' :True,
    'auto_install':False,
}
