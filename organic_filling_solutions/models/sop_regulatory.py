from odoo import models, fields, _


class LaboratoryRegulatory(models.Model):
    _name = "regulatory.laboratory"
    _description = "Laboratory"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    master_sop = fields.Binary(string="Master SOP File (PDF)", attachment=True)


class ProductionRegulatory(models.Model):
    _name = "regulatory.production"
    _description = "Production"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])
    related_file = fields.Binary(string="Related files (PDF) File",
                                 attachment=True)


class WarehouseRegulatory(models.Model):
    _name = "regulatory.warehouse"
    _description = "Warehouse"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    related_file_doc = fields.Binary(string="Related files (doc,XML,etc)",
                                     attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF) File",
                                     attachment=True)
    revisions = fields.Many2many('regulatory.revision.files', string="Revisions")


class RevisonFileRegulatory(models.Model):
    _name = "regulatory.revision.files"
    _description = "Revision Files"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    revision_file = fields.Binary(string="Revision File",
                                     attachment=True)

class GeneralRegulatory(models.Model):
    _name = "regulatory.general"
    _description = "General"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    related_file_doc = fields.Binary(string="Related files (doc,XML,etc)",
                                     attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF) File",
                                     attachment=True)


class QualityRegulatory(models.Model):
    _name = "regulatory.quality"
    _description = "Quality"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    related_file_doc = fields.Binary(string="Related files (doc,XML,etc)",
                                     attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF) File",
                                     attachment=True)


class ReworksRegulatory(models.Model):
    _name = "regulatory.reworks"
    _description = "Quality"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    related_file_doc = fields.Binary(string="Related files (doc,XML,etc)",
                                     attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF) File",
                                     attachment=True)


class HistoricalRegulatory(models.Model):
    _name = "regulatory.historical"
    _description = "Historical"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    type = fields.Selection(
        [('admin_compliance', 'Administrative and compliance'),
         ('fac_equipments', 'Facilities and equipment'),
         ('sanitation_hygiene', 'Sanitation and hygiene'),
         ('pest_ctrl', 'Pest control'),
         ('eq_cal_storage', 'Equipment calibration and storage'),
         ('storage_shipping', 'Storage and shipping'),
         ('package_label', 'Packaging and labeling'),
         ('process_product_eval', 'Process and product evaluation'),
         ('approved_suppliers', 'Approved suppliers'),
         ('receiving', 'Receiving'),
         ('inventory_control', 'Inventory Control'),
         ('training', 'Training'),
         ('erp_systems', 'ERP systems'),
         ('technical_diagrams', 'Technical Diagrams'),
         ('inspection_logs', 'Inspection Logs'),
         ('components_specfs', 'Components Specifications')])

    related_file_doc = fields.Binary(string="Related files (doc,XML,etc)",
                                     attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF) File",
                                     attachment=True)


class FDARegulatory(models.Model):
    _name = "regulatory.fda"
    _description = "FDA"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="Related file",
                                 attachment=True)

    related_file_image = fields.Binary(string="Related image",
                                       attachment=True)


class EPARegulatory(models.Model):
    _name = "regulatory.epa"
    _description = "EPA"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="Related file",
                                 attachment=True)

    related_file_image = fields.Binary(string="Related image",
                                       attachment=True)


class CaliforniaRegulatory(models.Model):
    _name = "regulatory.california"
    _description = "California"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="Related file",
                                 attachment=True)

    related_file_image = fields.Binary(string="Related image",
                                       attachment=True)


class TexasRegulatory(models.Model):
    _name = "regulatory.texas"
    _description = "Texas"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="Related file",
                                 attachment=True)

    related_file_image = fields.Binary(string="Related image",
                                       attachment=True)


class InternalAuditsRegulatory(models.Model):
    _name = "regulatory.internal.audits"
    _description = "Internal Audits"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")


class NSGRegulatory(models.Model):
    _name = "regulatory.nsf"
    _description = "NSF"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file_docs = fields.Binary(string="Related files (doc,XML,etc)",
                                      attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF)",
                                     attachment=True)


class WalmartRegulatory(models.Model):
    _name = "regulatory.walmart"
    _description = "Wal-Mart"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file_docs = fields.Binary(string="Related files (doc,XML,etc)",
                                      attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF)",
                                     attachment=True)


class HEBRegulatory(models.Model):
    _name = "regulatory.heb"
    _description = "HEB"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file_docs = fields.Binary(string="Related files (doc,XML,etc)",
                                      attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF)",
                                     attachment=True)


class ArchpointRegulatory(models.Model):
    _name = "regulatory.archpoint"
    _description = "Archpoint"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file_docs = fields.Binary(string="Related files (doc,XML,etc)",
                                      attachment=True)

    related_file_pdf = fields.Binary(string="Related files (PDF)",
                                     attachment=True)


class TrainingRegulatory(models.Model):
    _name = "regulatory.training"
    _description = "Training"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="File",
                                 attachment=True)
    video_url = fields.Char(string="Training Video Link")
    video_url2 = fields.Char(string="Training Video Link (2)")
    video_url3 = fields.Char(string="Training Video Link (3)")


class SupplierDocsRegulatory(models.Model):
    _name = "regulatory.supplier.docs"
    _description = "Supplier Docs"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    supplier_id = fields.Many2one('res.partner', string='Supplier')
    report_date = fields.Date(string='Report Date')
    file = fields.Binary(string=" New File",
                         attachment=True)


class OrgChartRegulatory(models.Model):
    _name = "regulatory.org.chart"
    _description = "Org Chart"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    org_file = fields.Binary(string="Org File",
                             attachment=True)


class RegistrationsRegulatory(models.Model):
    _name = "regulatory.registrations"
    _description = "Registrations"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file = fields.Binary(string="File(PDF)",
                         attachment=True)


class StatementRegulatory(models.Model):
    _name = "regulatory.statement"
    _description = "Statement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file = fields.Binary(string="File(any)",
                         attachment=True)


class RevisionsRegulatory(models.Model):
    _name = "regulatory.revisions"
    _description = "Revisions"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    revision_no = fields.Char(string="Revision No.")
    state = fields.Selection([
        ('retired', 'Retired'),
        ('in_force', 'In Force')], string="States")
    revision_file = fields.Binary(string="Revision File",
                                  attachment=True)


class SuppliersRegulatory(models.Model):
    _name = "regulatory.suppliers"
    _description = "Suppliers"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    supplier_id = fields.Many2one('res.partner', string='contact')


class ComplaintsRegulatory(models.Model):
    _name = "regulatory.complaints"
    _description = "Complaints"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    product_id = fields.Many2one('product.product', string='Product')
    mo_id = fields.Many2one('mrp.production', string='MO')
    state = fields.Selection([
        ('received', 'Received'),
        ('in_progress', 'In Progress'), ('resolved', 'Resolved')],
        string="Status")

    description = fields.Text(string='Description', translate=True)

    file_pdf = fields.Binary(string="File",
                             attachment=True)


class FormsRegulatory(models.Model):
    _name = "regulatory.forms"
    _description = "Statement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file = fields.Binary(string="File(any)",
                         attachment=True)


class MasterSchedulesRegulatory(models.Model):
    _name = "regulatory.master.schedules"
    _description = "Master Schedules"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file_pdf = fields.Binary(string="File(any)",
                             attachment=True)
    new_image = fields.Binary(string="New Image",
                              attachment=True)


class QuarterlyManagementReviewLogRegulatory(models.Model):
    _name = "regulatory.quarterly.review.log"
    _description = "Master Schedules"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file_pdf = fields.Binary(string="PDF",
                             attachment=True)


class MockRecallsRegulatory(models.Model):
    _name = "regulatory.mock.recalls"
    _description = "Mock Recalls"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file_new = fields.Binary(string="File New",
                             attachment=True)
    file_related = fields.Binary(string="Related File",
                                 attachment=True)
    new_image = fields.Binary(string="New Image",
                              attachment=True)


class CompanyPlansRegulatory(models.Model):
    _name = "regulatory.plans"
    _description = "Company Plans"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")

    file_pdf = fields.Binary(string="PDF(If Any)",
                             attachment=True)
    revision_ids = fields.Many2many('regulatory.revisions', string="Revisions")


class JobDescriptionRegulatory(models.Model):
    _name = "regulatory.job.description"
    _description = "Job Description"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    responsibilities = fields.Text(string="Responsibilities")


class SopTypeRegulatory(models.Model):
    _name = "regulatory.sop.type"
    _description = "Sop Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    sop_ids = fields.Many2many('regulatory.sop')


class SopRegulatory(models.Model):
    _name = "regulatory.sop"
    _description = "Sop"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    section = fields.Selection([
        ('lab', 'Laboratory'),
        ('prod', 'Production'),
        ('warehouse', 'Warehouse'),
        ('general', 'general'),
        ('qlty', 'Quality'),
        ('rework', 'Rework'),
        ('historical', 'Historical')],
        string="Section")

    sop_type_ids = fields.Many2many('regulatory.sop.type')
    file_excel = fields.Binary(string="File(excel)",
                             attachment=True)
    file_word = fields.Binary(string="File(word)",
                             attachment=True)
    file_pdf = fields.Binary(string="File(pdf)",
                             attachment=True)
