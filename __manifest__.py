
{
    'name': 'Bike_rent',
    'description': """Module for Versada task 1""",
    'author': 'Stasys Civilis',
    'depends': ['product','mail','sale'],
    'application': True,
    'summary': 'Versada task1',
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/inherit_views.xml',
        'views/template.xml',
        ],
    'demo': ['demo/demo_data.xml'],
}
