# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Website - Copy and Delete Pages',
    'category': 'Website',
    'version': '1.0',
    'author': 'Wang Hee Shiong & Vizucom Oy',
    'website': 'http://www.vizucom.com',
    'depends': ['website'],
    'description': """
Website - Copy and Delete Pages
===============================
 * Provides the option to copy and delete website pages directly from Odoo frontend
 * Based on the module by Wang Hee Shiong, available at https://github.com/dapoaugury/odoo/tree/website_edit
 * See also https://www.odoo.com/en_UK/groups/community-framework-62/community-framework-11690036 
""",
    'data': [
        'views/website_templates.xml',
        'views/website_backend_navbar.xml',
    ],
}