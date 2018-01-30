# -*- coding: utf-8 -*-

import odoo
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.controllers.main import QueryURL

class CustomHome(Website):
    @http.route()
    def index(self, **kw):
        request.env.cr.execute("SELECT id FROM product_template where website_published = TRUE ORDER BY id desc")
        product_ids = request.env.cr.fetchall()[0:6]
        latest_ids = []
        for product_id in product_ids:
            latest_ids.append(product_id[0])
        latest_products = request.env['product.template'].browse(latest_ids)
        keep = QueryURL("/shop")
        
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)
        return request.render('website.homepage', {
                                                    'latest_products': latest_products, 
                                                    'keep': keep, 
                                                    'compute_currency': compute_currency})
        