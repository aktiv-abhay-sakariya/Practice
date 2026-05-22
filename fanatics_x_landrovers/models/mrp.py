
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    knowledge_article_ids = fields.Many2many('knowledge.article', string='Knowledge Articles')


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'
    _description = 'Knowledge Article'

    def view_knowledge_article(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("knowledge.knowledge_article_action_form")
        action['res_id'] = self.id
        action['context'] = {'default_knowledge_article_ids': [(6, 0, [self.id])]}
        return action