# -*- coding: utf-8 -*-
import logging
from openerp.osv import orm, osv, fields
from openerp.addons.website.models.website import slugify
logger = logging.getLogger(__name__)

class website(osv.osv):

    _inherit = 'website'

    # Wang - 20150319
    def copy_page(self, cr, uid, name, current_page, ispage=True, context=None):

        # Wang - 20150320
        # Form fully qualified template name by concatenating module name with template name for current page to be copied.
        template = "website.%s" % (current_page)

        context = context or {}
        imd = self.pool.get('ir.model.data')
        view = self.pool.get('ir.ui.view')
        template_module, template_name = template.split('.')

        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)

        try:
            # For copied page, it should have been exist in database.
            imd.get_object_reference(cr, uid, template_module, page_name)

        except ValueError:
            _, template_id = imd.get_object_reference(cr, uid, template_module, template_name)

            page_id = view.copy(cr, uid, template_id, context=context)
            page = view.browse(cr, uid, page_id, context=context)
 
            # Wang - 20150401 Create records in database for the copied page with slugified page name.
            page.write({
                'arch': page.arch.replace(template, page_xmlid),
                'name': page_name,
                'page': ispage,
            })

            imd.create(cr, uid, {
                'name': page_name,
                'module': template_module,
                'model': 'ir.ui.view',
                'res_id': page_id,
                'noupdate': True
            }, context=context)

        return page_xmlid

    # Wang - 20150326
    def delete_page(self, cr, uid, name, ispage=True, context=None):

        # Set external template ID of the template to be deleted.
        template = "website.%s" % (name)

        context = context or {}
        imd = self.pool.get('ir.model.data')
        view = self.pool.get('ir.ui.view')
        template_module, template_name = template.split('.')

        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)

        # Retrieval of template ID from database based on slugified page name (refer to above copy_page function).
        _, template_id = imd.get_object_reference(cr, uid, template_module, page_name)

        try:
            view.unlink(cr, uid, template_id, context=context)
        except ValueError:
            # This can happen only when non-existing URL has been created by user manually in the prompt.
            logger.info("Page deletion has failed, external ID not found in the system: {%s}", template)

        return page_xmlid
