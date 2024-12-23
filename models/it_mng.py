import logging
from re import S 
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class IT_Hardware(models.Model):
    _name ='it.mng.hardware'

    name= fields.Char(string='Name', size=100, required=True)
    serial= fields.Char(string='Serial', size=30, required=True)
    model= fields.Char(string='Model', size=60, required=True)
    description= fields.Html(string='Description')
    photo= fields.Image(string='Photo', max_width=150, max_height=150)
    purchase= fields.Date(string='Purchase')
    area_id= fields.Many2one(string='Area', comodel_name='it.mng.area')
    brand_id= fields.Many2one(string='Brand', comodel_name='it.mng.brands')
    hardware_type_id= fields.Many2one(string='Hardware Type', comodel_name='it.mng.hardware.type')
    employee_id= fields.Many2one(string='Employee', comodel_name='hr.employee.public')
    father_id= fields.Many2one(string='Father',comodel_name='it.mng.hardware')
    child_ids= fields.One2many(string='Childs',comodel_name='it.mng.hardware', inverse_name="father_id")
    software_ids= fields.One2many(string='Software', comodel_name='it.mng.software.licence',inverse_name="hardware_id")
    ticket_ids= fields.One2many(string='Tickets', comodel_name='helpdesk.ticket', inverse_name='hardware_id')
    record_ids= fields.One2many(string='Record Type',comodel_name='it.mng.hardware.record',inverse_name='hardware_id')
    
    ticket_count = fields.Integer(
        string='Tickets Count',
        compute='_compute_ticket_count'
    )

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for record in self:
            record.ticket_count = len(record.ticket_ids)

    def action_view_tickets(self):
        self.ensure_one()
        return {
            'name': _('Tickets'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.ticket',
            'domain': [('hardware_id', '=', self.id)],
            'context': {'default_hardware_id': self.id},
        }
    
    @api.onchange('model', 'area_id', 'hardware_type_id')
    def _onchange_generate_name(self):
        if self.model and self.area_id and self.hardware_type_id:
            model_parts = self.model.split(' ')
            first_word_after_space = model_parts[1] if len(model_parts) > 1 else model_parts[0]
            self.name = f"{self.hardware_type_id.name} - {first_word_after_space} - {self.area_id.name}"

    @api.model    
    def create(self, vals,):
        hardware = super(IT_Hardware, self).create(vals)
        record_vals = {
            'hardware_id': hardware.id,
            'record_types_id': self.env['it.mng.record.type'].search([('initials', '=', 'CM')], limit=1).id,
            'description': 'Hardware creado automáticamente',
        }
        self.env['it.mng.hardware.record'].create(record_vals)

        return hardware

    
        
class IT_Hardware_record(models.Model):
    
    _name ='it.mng.hardware.record'

    hardware_id= fields.Many2one(string='Hardware', comodel_name='it.mng.hardware')
    record_types_id= fields.Many2one(string='Record Type', comodel_name= 'it.mng.record.type')
    description= fields.Html(string='Desription')
    link_id= fields.Char(string='Link ID') # TO DO DEFINIR CAMPO CORRECTO
    link_object_id= fields.Char(string='Link Object ID') # TO DO DEFINIR CAMPO CORRECTO
    
class IT_Record_types(models.Model):
    _name ='it.mng.record.type'

    name= fields.Char(string='Name', size=60, required=True)
    initials= fields.Char(string='Initials', size=3, required=True)

class IT_Software_types(models.Model):
    _name ='it.mng.software.types'

    name= fields.Char(string='Name', size=60, required=True)
    initials= fields.Char(string='Initials', size=3, required=True)


class IT_Software(models.Model):
    _name ='it.mng.software'

    name= fields.Char(string='Name', size=60, required=True)
    version= fields.Char(string='Version', size=15, required=True)
    software_type_id= fields.Many2one(string='Software type', comodel_name='it.mng.software.types')
    brand_id= fields.Many2one(string='Brand', comodel_name='it.mng.brands')
    
class IT_Brands(models.Model):
    _name ='it.mng.brands'

    name= fields.Char(string='Name', size=60, required=True)
    logo= fields.Image(string='Logo', max_width=150, max_height=150)
    
class IT_Software_licence(models.Model):
    _name ='it.mng.software.licence'

    license= fields.Char(string='License', size=120, required=True)
    hardware_id= fields.Many2one(string='Hardware',comodel_name='it.mng.hardware')
    software_id= fields.Many2one(string='Software',comodel_name='it.mng.software')
    
    @api.model
    def create(self, vals):
        software = super(IT_Software_licence, self).create(vals)
        record_vals = {
            'hardware_id': software.hardware_id.id,
            'record_types_id': self.env['it.mng.record.type'].search([('initials', '=', 'IS')], limit=1).id,
            'description': 'Installer Software',
        }
        self.env['it.mng.hardware.record'].create(record_vals) 
        return software


class IT_Hardware_type(models.Model):
    _name ='it.mng.hardware.type'    
    name= fields.Char(string='Name', size=60, required=True)
    initials= fields.Char(string='Initials', size=3, required=True)
    

class IT_Area(models.Model):
    _name ='it.mng.area' 
    name= fields.Char(string='Name', size=60, required=True)
    initials= fields.Char(string='Initials', size=3, required=True)
    father_id=fields.Many2one(string='Area', comodel_name='it.mng.area')
    father_ids=fields.One2many(string='Subareas', comodel_name='it.mng.area',inverse_name='father_id')

class Employee(models.Model):
    _inherit= 'hr.employee.public'
    hardware_ids=fields.One2many(string='Hardware',comodel_name='hr.employee.public',inverse_name='employee_id')
    
    
class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    hardware_id= fields.Many2one(string='Helpdesk',comodel_name='it.mng.hardware')