# -*- coding: utf-8 -*-
import logging
import re
import werkzeug.utils
import werkzeug.wrappers
import openerp
from openerp.addons.web import http
from openerp.http import request, Response

logger = logging.getLogger(__name__)

class Website(openerp.addons.web.controllers.main.Home):

    @http.route('/website/copy/<path:path>', type='http', auth="user", website=True)
    def pagecopy(self, path, noredirect=False, current_page=None):

        # FIXME: This would be better handled in the front-end (for example show the menu item only for Pages)
        try:
            xml_id = request.registry['website'].copy_page(request.cr, request.uid, path, current_page, context=request.context)
        except ValueError as ve:
            ve.message='Copy failed - please note that you can only copy pages (not e.g. products, shops or blogs) '
            raise

        model, id  = request.registry["ir.model.data"].get_object_reference(request.cr, request.uid, 'website', 'main_menu')

        # New menu entry for the copied page is created under parent menu ID in the database.
        # Take note that path variable contains original name as entered by user in prompt.
        
        request.registry['website.menu'].create(request.cr, request.uid, {
                'name': path,
                'url': "/page/" + xml_id,
                'parent_id': id,
        }, context=request.context)

        # Reverse action in order to allow shortcut for /page/<website_xml_id>
        url = "/page/" + re.sub(r"^website\.", '', xml_id)

        # Whether to redirect website to newly created page or just print result in plain text in current page.
        # Basically user is redirected to newly copied page.
        
        if noredirect:
            return werkzeug.wrappers.Response(url, mimetype='text/plain')
        return werkzeug.utils.redirect(url)

    # The function delete_page in webiste/models/website.py Python file is called to remove record from model ir.ui.view
    # Again return value from the function is XML ID (comprise of <module name>.<slugified page name>) of current page to
    # be deleted. Take note that to search for menu ID of menu entry belong to deleted page, url instead of path must
    # be used as the path name has been slugified but not the same as original path name as in above pagecopy function.

    @http.route('/website/delete/<path:path>', type='http', auth="user", website=True)
    def pagedelete(self, path, noredirect=False):

        # FIXME: This would be better handled in the front-end (for example show the menu item only for Pages)
        try:
            xml_id = request.registry['website'].delete_page(request.cr, request.uid, path, context=request.context)
        except ValueError as ve:
            ve.message='Delete failed - please note that you can only delete pages (not e.g. products, shops or blogs) '
            raise

        url = "/page/%s" % (xml_id)

        # Query database with url of page to be deleted as search index in SQL statement.
        id = request.registry["website.menu"].search(request.cr, request.uid, [("url","=",url)], context=request.context)

        # Remove submenu option from menu bar in user interface with index obtained from database.
        request.registry['website.menu'].unlink(request.cr, request.uid, id, context=request.context)

        # Since current page has been deleted, redirect user to home page.
        url = "/"

        if noredirect:
            return werkzeug.wrappers.Response(url, mimetype='text/plain')
        return werkzeug.utils.redirect(url)