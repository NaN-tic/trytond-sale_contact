# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.modules.account_invoice_contact.invoice import ContactMixin

__all__ = ['ConfigurationRelationType', 'Configuration', 'Sale']


class ConfigurationRelationType(ModelSQL):
    'Sale Configuration - Party relation type'
    __name__ = 'sale.configuration-party.relation.type'

    relation = fields.Many2One('party.relation.type', 'Relation Type',
        required=True)
    config = fields.Many2One('sale.configuration', 'Config',
        required=True)


class Configuration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'

    relation_types = fields.Many2Many(
        'sale.configuration-party.relation.type', 'config',
        'relation', 'Contact types')


class Sale(ContactMixin, metaclass=PoolMeta):
    __name__ = 'sale.sale'
    _contact_config_name = 'sale.configuration'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.allowed_invoice_contacts.context = {'company': Eval('company', -1)}
        cls.allowed_invoice_contacts.depends.add('company')
        cls.invoice_contact.context = {'company': Eval('company', -1)}
        cls.invoice_contact.depends.add('company')

    def _get_invoice(self):
        invoice = super(Sale, self)._get_invoice()
        if self.invoice_contact:
            if self.invoice_contact in invoice.allowed_invoice_contacts:
                invoice.invoice_contact = self.invoice_contact
        return invoice
