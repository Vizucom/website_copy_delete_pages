$(document).ready(function() {
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;

	// Wang - 20150319
	// Copy current page to another new page and create corresponding new entry in menu bar.
	// Current page to be copied will appear in the prompt for reference.
    website.EditorBarContent.include({	
	   copy_page: function() {
            website.prompt({
                id: "editor_copy_page",
                window_title: _t("Copy Current Page: " + window.location.href),
                input: _t("New Page Title"),
			}).then(function(val) { 
				if (val) {
					var current_page = window.location.href.replace(/^.*\//,'');
					var url = '/website/copy/' + encodeURIComponent(val) + "?current_page=" + encodeURIComponent(current_page);
					document.location = url;
				}
			}); 
        },

    	// Wang - 20150326
    	// Delete current page and associated menu entry from database.
    	// User is allowed to modified URL of current page to be deleted manually in the prompt.
	   delete_page: function() {
            website.prompt({
                id: "editor_delete_page",
                window_title: _t("Delete Current Page"),
                input: _t("URL"),
		default: window.location.href,
			}).then(function(val) { 
				if (val) {
					var val = val.replace(/^.*\//,'');
					var url = '/website/delete/' + encodeURIComponent(val);
					document.location = url;
				}
			}); 
        }
    });
});
