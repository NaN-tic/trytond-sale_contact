# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_contact.tests.test_sale_contact import suite
except ImportError:
    from .test_sale_contact import suite

__all__ = ['suite']
